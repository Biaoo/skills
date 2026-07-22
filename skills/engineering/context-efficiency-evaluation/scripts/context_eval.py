#!/usr/bin/env python3
"""Deterministic CLI for generic context-evaluation artifacts."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from context_eval_runtime.canonical import canonical_json, parse_contract_json, snapshot_tree
from context_eval_runtime.contracts import ContractError, validate_document
from context_eval_runtime.evaluate import EvaluationError, evaluate
from context_eval_runtime.normalize import events_jsonl, normalize_jsonl, validate_normalization_options
from context_eval_runtime.workspace import (
    initialize_workspace, load_workspace, prepare_normalized, publish_normalized_events, publish_report,
    publish_tree, validate_slug,
)

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_IO = 3
EXIT_CONTRACT = 4
EXIT_EVALUATION = 5
EXIT_INTERNAL = 6


class StrictParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def parser() -> argparse.ArgumentParser:
    root = StrictParser(description="Validate, normalize, snapshot, and evaluate generic context evidence.")
    commands = root.add_subparsers(dest="command", required=True, parser_class=StrictParser)

    init = commands.add_parser("init", help="initialize an immutable evaluation workspace")
    init.add_argument("evaluation_id")
    init.add_argument("--root", type=Path)
    init.add_argument("--reuse", action="store_true")

    validate = commands.add_parser("validate", help="validate one versioned JSON document")
    validate.add_argument("input", type=Path, help="JSON file, or - for stdin")
    validate.add_argument("--contract", choices=("ctxeval.input.v1", "ctxeval.event.v1", "ctxeval.tree.v1", "ctxeval.report.v1", "ctxeval.workspace.v1"))

    normalize = commands.add_parser("normalize", help="normalize native JSONL into event documents")
    normalize.add_argument("input", type=Path, help="native JSONL file")
    normalize.add_argument("--attempt-id", required=True)
    destination = normalize.add_mutually_exclusive_group(required=True)
    destination.add_argument("--blobs-dir", type=Path)
    destination.add_argument("--workspace", type=Path)
    normalize.add_argument("--artifact-slug")
    normalize.add_argument("--inline-limit-bytes", type=int, default=65_536)

    snapshot = commands.add_parser("snapshot", help="snapshot a filesystem tree")
    snapshot.add_argument("root", type=Path)
    snapshot.add_argument("--exclude", action="append", default=[], metavar="RELATIVE_PATH")
    snapshot.add_argument("--workspace", type=Path)
    snapshot.add_argument("--artifact-slug")
    snapshot.add_argument("--label")

    evaluate_command = commands.add_parser("evaluate", help="evaluate a ctxeval.input.v1 document")
    evaluate_command.add_argument("input", type=Path, help="JSON file, or - for stdin")
    evaluate_command.add_argument("--workspace", type=Path)
    return root


def _read_json(path: Path) -> Any:
    text = sys.stdin.read() if str(path) == "-" else path.read_text(encoding="utf-8")
    return parse_contract_json(text)


def _emit(value: Any) -> None:
    sys.stdout.write(canonical_json(value) + "\n")


def _require_together(args: argparse.Namespace, names: tuple[str, ...]) -> None:
    present = [getattr(args, name) is not None for name in names]
    if any(present) and not all(present):
        raise ContractError("workspace publication requires " + ", ".join("--" + name.replace("_", "-") for name in names))


def run(arguments: list[str] | None = None) -> int:
    args = parser().parse_args(arguments)
    try:
        if args.command == "init":
            workspace = initialize_workspace(args.evaluation_id, args.root, args.reuse)
            print(
                "warning: .context-evaluation is not auto-ignored; explicitly exclude it from project snapshots",
                file=sys.stderr,
            )
            _emit({"workspace": os.fspath(workspace)})
        elif args.command == "validate":
            if args.input.is_dir():
                if args.contract not in (None, "ctxeval.workspace.v1"):
                    raise ContractError("workspace directory validation requires ctxeval.workspace.v1")
                document = load_workspace(args.input)
            else:
                document = _read_json(args.input)
                validate_document(document, args.contract)
            _emit(document)
        elif args.command == "normalize":
            validate_normalization_options(args.attempt_id, args.inline_limit_bytes)
            if args.workspace is None:
                if args.artifact_slug is not None:
                    raise ContractError("--artifact-slug requires --workspace")
                events = normalize_jsonl(args.input, args.blobs_dir, args.attempt_id, args.inline_limit_bytes)
            else:
                if args.artifact_slug is None:
                    raise ContractError("--workspace requires --artifact-slug")
                normalized_fd, blobs_fd = prepare_normalized(args.workspace, args.artifact_slug)
                try:
                    events = normalize_jsonl(args.input, blobs_fd, args.attempt_id, args.inline_limit_bytes)
                    publish_normalized_events(normalized_fd, events_jsonl(events))
                finally:
                    os.close(blobs_fd)
                    os.close(normalized_fd)
            _emit(events)
        elif args.command == "snapshot":
            _require_together(args, ("workspace", "artifact_slug", "label"))
            tree = snapshot_tree(args.root, args.exclude)
            if args.workspace is not None:
                validate_slug(args.artifact_slug, "artifact slug")
                publish_tree(args.workspace, args.artifact_slug, args.label, tree)
            _emit(tree)
        elif args.command == "evaluate":
            report = evaluate(_read_json(args.input))
            if args.workspace is not None:
                publish_report(args.workspace, report)
            _emit(report)
        return EXIT_OK
    except (OSError, UnicodeError) as error:
        print(f"I/O error: {error}", file=sys.stderr)
        return EXIT_IO
    except EvaluationError as error:
        print(f"evaluation error: {error}", file=sys.stderr)
        return EXIT_EVALUATION
    except (ContractError, ValueError) as error:
        print(f"contract error: {error}", file=sys.stderr)
        return EXIT_CONTRACT
    except Exception as error:  # pragma: no cover - last-resort stable boundary
        print(f"internal error: {error}", file=sys.stderr)
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(run())
