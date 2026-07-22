"""Normalize provider-neutral JSONL while preserving native evidence."""

from __future__ import annotations

import json
import os
import secrets
import stat
from pathlib import Path
from typing import Any

from .canonical import canonical_json, sha256_bytes
from .contracts import ContractError, EVENT_VERSION, validate_event


def _native_string(parsed: Any, key: str) -> str | None:
    if isinstance(parsed, dict) and isinstance(parsed.get(key), str) and parsed[key]:
        return parsed[key]
    return None


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _framed_lines(raw: bytes) -> list[tuple[bytes, str]]:
    if not raw:
        return []
    parts = raw.split(b"\n")
    records: list[tuple[bytes, str]] = []
    for index, part in enumerate(parts):
        split_by_lf = index < len(parts) - 1
        if not split_by_lf and part == b"":
            continue
        if split_by_lf and part.endswith(b"\r"):
            records.append((part[:-1], "crlf"))
        else:
            records.append((part, "lf" if split_by_lf else "none"))
    return records


def _blob_error(subject: str, message: str) -> ContractError:
    return ContractError(f"blob {subject}: {message}")


def _open_blob_directory(directory: Path) -> int:
    absolute = Path(os.path.abspath(directory))
    try:
        absolute.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass
    info = absolute.lstat()
    if not stat.S_ISDIR(info.st_mode) or absolute.is_symlink():
        raise _blob_error(str(directory), "blob directory must be a non-symlink directory")
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(absolute, flags)
    except OSError as error:
        raise _blob_error(str(directory), f"cannot open blob directory safely: {error}") from error
    opened = os.fstat(descriptor)
    current = absolute.lstat()
    if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
        os.close(descriptor)
        raise _blob_error(str(directory), "blob directory changed while opening")
    return descriptor


def _verify_blob(directory_fd: int, name: str, expected: bytes, digest: str) -> None:
    try:
        entry = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except OSError as error:
        raise _blob_error(digest, f"cannot inspect existing blob safely: {error}") from error
    if not stat.S_ISREG(entry.st_mode):
        raise _blob_error(digest, "existing digest path is not a regular file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(name, flags, dir_fd=directory_fd)
    except OSError as error:
        raise _blob_error(digest, f"cannot open existing blob safely: {error}") from error
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise _blob_error(digest, "existing digest path is not a regular file")
        chunks = []
        while True:
            chunk = os.read(descriptor, 65_536)
            if not chunk:
                break
            chunks.append(chunk)
        data = b"".join(chunks)
        try:
            after = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        except OSError as error:
            raise _blob_error(digest, f"digest path changed while verifying: {error}") from error
        identity = lambda value: (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns)
        if identity(entry) != identity(info) or identity(after) != identity(info):
            raise _blob_error(digest, "digest path changed while verifying")
    finally:
        os.close(descriptor)
    if len(data) != len(expected) or sha256_bytes(data) != digest or data != expected:
        raise _blob_error(digest, "existing blob content does not match digest, length, and bytes")


def _store_blob(directory_fd: int, data: bytes, digest: str) -> None:
    temporary = f".{digest}.{secrets.token_hex(12)}"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(temporary, flags, 0o600, dir_fd=directory_fd)
    try:
        written = 0
        while written < len(data):
            written += os.write(descriptor, data[written:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    try:
        try:
            os.link(temporary, digest, src_dir_fd=directory_fd, dst_dir_fd=directory_fd, follow_symlinks=False)
        except FileExistsError:
            pass
        _verify_blob(directory_fd, digest, data, digest)
    finally:
        try:
            os.unlink(temporary, dir_fd=directory_fd)
        except FileNotFoundError:
            pass


def _unique_event_id(candidate: str | None, attempt_id: str, index: int, reserved: set[str]) -> str:
    if candidate and candidate not in reserved:
        return candidate
    base = f"{attempt_id}:{index:06d}"
    generated = base
    probe = 1
    while generated in reserved:
        generated = f"{base}:{probe}"
        probe += 1
    return generated


def validate_normalization_options(attempt_id: str, inline_limit_bytes: int) -> None:
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ContractError("attemptId must be a non-empty string")
    if inline_limit_bytes < 0:
        raise ValueError("inline limit must be >= 0")


def normalize_jsonl(native_path: Path, blobs_directory: Path | int, attempt_id: str, inline_limit_bytes: int = 65_536) -> list[dict[str, Any]]:
    validate_normalization_options(attempt_id, inline_limit_bytes)
    raw = native_path.read_bytes()
    records = _framed_lines(raw)
    owns_directory = not isinstance(blobs_directory, int)
    directory_fd = _open_blob_directory(blobs_directory) if owns_directory else os.dup(blobs_directory)
    try:
        native_ids: set[str] = set()
        parsed_records: list[tuple[bytes, str, Any, str]] = []
        for line, terminator in records:
            status = "parsed"
            try:
                parsed = json.loads(line.decode("utf-8"), parse_constant=_reject_constant)
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
                parsed = None
                status = "invalid_json"
            native_id = _native_string(parsed, "id")
            if native_id:
                native_ids.add(native_id)
            parsed_records.append((line, terminator, parsed, status))

        events: list[dict[str, Any]] = []
        reserved = set(native_ids)
        assigned: set[str] = set()
        for index, (line, terminator, parsed, parse_status) in enumerate(parsed_records, start=1):
            digest = sha256_bytes(line)
            payload: Any = parsed
            payload_blob: dict[str, Any] | None = None
            if parse_status == "invalid_json" or len(line) > inline_limit_bytes:
                _store_blob(directory_fd, line, digest)
                payload = None
                payload_blob = {"bytes": len(line), "sha256": digest}
            native_id = _native_string(parsed, "id")
            event_id = native_id if native_id and native_id not in assigned else _unique_event_id(None, attempt_id, index, reserved | assigned)
            assigned.add(event_id)
            event = {
                "actorId": _native_string(parsed, "actorId"), "attemptId": attempt_id, "eventId": event_id,
                "lineTerminator": terminator, "monotonicIndex": index, "nativeLine": index,
                "parentId": _native_string(parsed, "parentId"), "parseStatus": parse_status,
                "payload": payload, "payloadBlob": payload_blob, "schemaVersion": EVENT_VERSION,
                "type": _native_string(parsed, "type") or parse_status,
            }
            validate_event(event)
            events.append(event)
        if len(assigned) != len(events):
            raise ContractError("normalized event IDs must be stream-unique")
        return events
    finally:
        os.close(directory_fd)


def events_jsonl(events: list[dict[str, Any]]) -> str:
    return "".join(canonical_json(event) + "\n" for event in events)
