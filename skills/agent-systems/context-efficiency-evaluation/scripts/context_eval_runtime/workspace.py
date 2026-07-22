"""Safe, immutable evaluation workspace creation and publication."""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .canonical import canonical_json, parse_contract_json
from .contracts import ContractError, WORKSPACE_VERSION, validate_workspace

_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_WORKSPACE_DIRECTORY = ".context-evaluation"


def validate_slug(value: str, subject: str = "slug") -> str:
    if not isinstance(value, str) or len(value) > 64 or not _SLUG.fullmatch(value):
        raise ContractError(f"{subject} must be a lowercase ASCII slug of at most 64 characters")
    return value


def _directory_flags() -> int:
    return os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)


def _open_directory(path: Path) -> int:
    """Open a directory by walking every supplied component without following links."""
    raw = os.fspath(path)
    absolute = os.path.isabs(raw)
    anchor = os.open("/" if absolute else ".", _directory_flags())
    current = anchor
    try:
        parts = Path(raw).parts
        if absolute and parts and parts[0] == os.path.sep:
            parts = parts[1:]
        for part in parts:
            if part in ("", "."):
                continue
            try:
                child = os.open(part, _directory_flags(), dir_fd=current)
            except OSError as error:
                raise ContractError(
                    f"workspace path component cannot be opened safely: {part}: {error}"
                ) from error
            os.close(current)
            current = child
        if not stat.S_ISDIR(os.fstat(current).st_mode):
            raise ContractError("workspace path is not a directory")
        return current
    except Exception:
        os.close(current)
        raise


def _mkdir_at(parent_fd: int, name: str, exclusive: bool) -> int:
    try:
        os.mkdir(name, 0o700, dir_fd=parent_fd)
    except FileExistsError:
        if exclusive:
            raise ContractError(f"workspace entry already exists: {name}")
    try:
        return os.open(name, _directory_flags(), dir_fd=parent_fd)
    except OSError as error:
        raise ContractError(f"workspace entry is not a safe directory: {name}: {error}") from error


def _open_child(parent_fd: int, name: str) -> int:
    try:
        return os.open(name, _directory_flags(), dir_fd=parent_fd)
    except OSError as error:
        raise ContractError(f"workspace entry is not a safe directory: {name}: {error}") from error


def _read_regular_at(parent_fd: int, name: str) -> bytes:
    try:
        before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise ContractError(f"workspace entry is not a regular file: {name}")
        descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
    except OSError as error:
        raise ContractError(f"workspace entry cannot be read safely: {name}: {error}") from error
    try:
        opened = os.fstat(descriptor)
        chunks = []
        while True:
            chunk = os.read(descriptor, 65_536)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) != (
            before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns
        ) or (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) != (
            opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns
        ):
            raise ContractError(f"workspace entry changed while reading: {name}")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _require_missing_at(parent_fd: int, name: str) -> None:
    try:
        os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    except OSError as error:
        raise ContractError(f"workspace artifact cannot be inspected: {name}: {error}") from error
    raise ContractError(f"workspace artifact already exists: {name}")


def _exclusive_write(parent_fd: int, name: str, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(name, flags, 0o600, dir_fd=parent_fd)
    except FileExistsError as error:
        raise ContractError(f"workspace artifact already exists: {name}") from error
    except OSError as error:
        raise ContractError(f"workspace artifact cannot be published: {name}: {error}") from error
    try:
        offset = 0
        while offset < len(data):
            offset += os.write(descriptor, data[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def find_project_root(start: Path | None = None) -> Path:
    current = Path.cwd() if start is None else start
    current = Path(os.path.abspath(current))
    if not current.is_dir():
        raise ContractError("workspace root must be an existing directory")
    for candidate in (current, *current.parents):
        marker = candidate / ".git"
        try:
            marker.lstat()
        except FileNotFoundError:
            continue
        return candidate
    return current


def _clock_now(clock: Callable[[], dt.datetime] | None) -> dt.datetime:
    value = (clock or (lambda: dt.datetime.now().astimezone()))()
    if value.tzinfo is None or value.utcoffset() is None:
        raise ContractError("workspace clock must return a timezone-aware datetime")
    return value


def initialize_workspace(evaluation_id: str, root: Path | None = None, reuse: bool = False,
                         clock: Callable[[], dt.datetime] | None = None) -> Path:
    evaluation_id = validate_slug(evaluation_id, "evaluation ID")
    now = _clock_now(clock)
    local_date = now.date().isoformat()
    manifest = {
        "createdAt": now.isoformat(timespec="seconds"),
        "evaluationId": evaluation_id,
        "localDate": local_date,
        "schemaVersion": WORKSPACE_VERSION,
    }
    validate_workspace(manifest)
    project = find_project_root(root)
    base_fd = _open_directory(project)
    opened: list[int] = [base_fd]
    try:
        container_fd = _mkdir_at(base_fd, _WORKSPACE_DIRECTORY, False); opened.append(container_fd)
        date_fd = _mkdir_at(container_fd, local_date, False); opened.append(date_fd)
        try:
            evaluation_fd = _mkdir_at(date_fd, evaluation_id, True)
        except ContractError:
            if not reuse:
                raise
            path = project / _WORKSPACE_DIRECTORY / local_date / evaluation_id
            load_workspace(path)
            return path
        opened.append(evaluation_fd)
        subject_fd = _mkdir_at(evaluation_fd, "subject", True); opened.append(subject_fd)
        evaluator_fd = _mkdir_at(evaluation_fd, "evaluator", True); opened.append(evaluator_fd)
        _exclusive_write(evaluation_fd, "manifest.json", (canonical_json(manifest) + "\n").encode("utf-8"))
        return project / _WORKSPACE_DIRECTORY / local_date / evaluation_id
    except Exception:
        # Deliberately leave partial state visible; never recursively delete evidence.
        raise
    finally:
        for descriptor in reversed(opened):
            os.close(descriptor)


@dataclass
class WorkspaceHandle:
    evaluation_fd: int
    subject_fd: int
    evaluator_fd: int
    manifest: dict[str, Any]

    def close(self) -> None:
        for descriptor in (self.evaluator_fd, self.subject_fd, self.evaluation_fd):
            if descriptor >= 0:
                os.close(descriptor)
        self.evaluation_fd = self.subject_fd = self.evaluator_fd = -1

    def __enter__(self) -> "WorkspaceHandle":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def _validated_workspace_handle(path: Path) -> WorkspaceHandle:
    absolute = Path(os.path.abspath(path))
    evaluation_fd = _open_directory(path)
    subject_fd = evaluator_fd = -1
    try:
        raw = _read_regular_at(evaluation_fd, "manifest.json")
        try:
            manifest = parse_contract_json(raw.decode("utf-8"))
        except (UnicodeError, ValueError) as error:
            raise ContractError(f"workspace manifest is invalid: {error}") from error
        validate_workspace(manifest)
        if absolute.name != manifest["evaluationId"] or absolute.parent.name != manifest["localDate"]:
            raise ContractError("workspace manifest identity does not match its path")
        if absolute.parent.parent.name != _WORKSPACE_DIRECTORY:
            raise ContractError("workspace path must be under .context-evaluation/date/id")
        subject_fd = _open_child(evaluation_fd, "subject")
        evaluator_fd = _open_child(evaluation_fd, "evaluator")
        return WorkspaceHandle(evaluation_fd, subject_fd, evaluator_fd, manifest)
    except Exception:
        for descriptor in (evaluator_fd, subject_fd, evaluation_fd):
            if descriptor >= 0:
                os.close(descriptor)
        raise


def load_workspace(path: Path) -> dict[str, Any]:
    with _validated_workspace_handle(path) as workspace:
        return workspace.manifest


def _ensure_path(root_fd: int, parts: tuple[str, ...]) -> int:
    current = os.dup(root_fd)
    try:
        for part in parts:
            child = _mkdir_at(current, part, False)
            os.close(current)
            current = child
        return current
    except Exception:
        os.close(current)
        raise


def normalized_locations(path: Path, artifact_slug: str) -> tuple[Path, Path]:
    validate_slug(artifact_slug, "artifact slug")
    load_workspace(path)
    base = Path(os.path.abspath(path)) / "subject" / "attempts" / artifact_slug / "normalized"
    return base / "events.jsonl", base / "blobs"


def prepare_normalized(path: Path, artifact_slug: str) -> tuple[int, int]:
    validate_slug(artifact_slug, "artifact slug")
    with _validated_workspace_handle(path) as workspace:
        attempts_fd = _ensure_path(workspace.subject_fd, ("attempts",))
        try:
            attempt_fd = _mkdir_at(attempts_fd, artifact_slug, False)
        finally:
            os.close(attempts_fd)
        try:
            normalized_fd = _mkdir_at(attempt_fd, "normalized", True)
        finally:
            os.close(attempt_fd)
        try:
            blobs_fd = _mkdir_at(normalized_fd, "blobs", True)
            return normalized_fd, blobs_fd
        except Exception:
            os.close(normalized_fd)
            raise


def publish_normalized_events(normalized_fd: int, text: str) -> None:
    _exclusive_write(normalized_fd, "events.jsonl", text.encode("utf-8"))


def publish_tree(path: Path, artifact_slug: str, label: str, document: Any) -> None:
    validate_slug(artifact_slug, "artifact slug")
    validate_slug(label, "snapshot label")
    with _validated_workspace_handle(path) as workspace:
        trees_fd = _ensure_path(workspace.subject_fd, ("attempts", artifact_slug, "trees"))
        try:
            _exclusive_write(trees_fd, label + ".json", (canonical_json(document) + "\n").encode("utf-8"))
        finally:
            os.close(trees_fd)


def publish_report(path: Path, document: Any) -> None:
    with _validated_workspace_handle(path) as workspace:
        _exclusive_write(workspace.evaluator_fd, "report.json", (canonical_json(document) + "\n").encode("utf-8"))
