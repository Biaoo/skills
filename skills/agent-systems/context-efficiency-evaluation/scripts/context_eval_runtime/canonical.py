"""Canonical JSON, hashing, and filesystem-tree helpers."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

MAX_SAFE_INTEGER = 9_007_199_254_740_991


def canonical_json(value: Any) -> str:
    """Return one deterministic, UTF-8-safe JSON line without a newline."""
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def parse_contract_json(text: str) -> Any:
    """Parse JSON with deterministic constants and integer-domain failures."""
    def parse_integer(raw: str) -> int:
        digits = raw.lstrip("-")
        if len(digits) > 16:
            raise ValueError(f"integer outside supported range [-{MAX_SAFE_INTEGER}, {MAX_SAFE_INTEGER}]")
        value = int(raw)
        if abs(value) > MAX_SAFE_INTEGER:
            raise ValueError(f"integer outside supported range [-{MAX_SAFE_INTEGER}, {MAX_SAFE_INTEGER}]")
        return value

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number: {value}")

    return json.loads(text, parse_int=parse_integer, parse_constant=reject_constant)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def normalize_relative_path(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("path must be a non-empty string")
    if "\\" in value:
        raise ValueError("path must use '/' separators")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError("path must be a normalized relative POSIX path")
    return value


def path_is_within(path: str, parent: str) -> bool:
    path = normalize_relative_path(path)
    parent = normalize_relative_path(parent)
    return path == parent or path.startswith(parent + "/")


def _excluded(path: str, excluded_paths: Iterable[str]) -> bool:
    return any(path_is_within(path, item) for item in excluded_paths)


def _identity(info: os.stat_result) -> tuple[int, int, int, int]:
    return info.st_dev, info.st_ino, info.st_mode, info.st_size


def _read_stable_file(parent_fd: int, name: str, initial: os.stat_result, relative: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(name, flags, dir_fd=parent_fd)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or _identity(before) != _identity(initial):
            raise OSError(f"snapshot entry changed before read: {relative}")
        chunks = []
        while True:
            chunk = os.read(descriptor, 65_536)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if (_identity(before) != _identity(after) or _identity(after) != _identity(current)
                or before.st_mtime_ns != after.st_mtime_ns or after.st_mtime_ns != current.st_mtime_ns):
            raise OSError(f"snapshot entry changed during read: {relative}")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _walk_directory(directory_fd: int, prefix: str, excluded: list[str], entries: list[dict[str, Any]]) -> None:
    with os.scandir(directory_fd) as iterator:
        names = sorted(entry.name for entry in iterator)
    for name in names:
        relative = f"{prefix}/{name}" if prefix else name
        if _excluded(relative, excluded):
            continue
        initial = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if stat.S_ISLNK(initial.st_mode):
            target = os.readlink(name, dir_fd=directory_fd)
            current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if _identity(initial) != _identity(current):
                raise OSError(f"snapshot symlink changed during read: {relative}")
            raw = target.encode("utf-8", errors="surrogateescape")
            entries.append({"bytes": len(raw), "path": relative, "sha256": sha256_bytes(raw), "type": "symlink"})
        elif stat.S_ISDIR(initial.st_mode):
            flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
            child_fd = os.open(name, flags, dir_fd=directory_fd)
            try:
                if _identity(os.fstat(child_fd)) != _identity(initial):
                    raise OSError(f"snapshot directory changed before traversal: {relative}")
                _walk_directory(child_fd, relative, excluded, entries)
                current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                if _identity(os.fstat(child_fd)) != _identity(current):
                    raise OSError(f"snapshot directory changed during traversal: {relative}")
            finally:
                os.close(child_fd)
        elif stat.S_ISREG(initial.st_mode):
            data = _read_stable_file(directory_fd, name, initial, relative)
            entries.append({"bytes": len(data), "path": relative, "sha256": sha256_bytes(data), "type": "file"})
        else:
            raise OSError(f"unsupported filesystem entry: {relative}")


def snapshot_tree(root: Path, excluded_paths: Iterable[str] = ()) -> dict[str, Any]:
    """Create a fail-closed deterministic manifest without following entries."""
    excluded = sorted({normalize_relative_path(item) for item in excluded_paths})
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(root, flags)
    try:
        if not stat.S_ISDIR(os.fstat(root_fd).st_mode):
            raise OSError(f"snapshot root is not a directory: {root}")
        entries: list[dict[str, Any]] = []
        _walk_directory(root_fd, "", excluded, entries)
    finally:
        os.close(root_fd)
    tree = {"entries": entries, "excludedPaths": excluded, "schemaVersion": "ctxeval.tree.v1"}
    tree["treeSha256"] = sha256_json(tree)
    return tree
