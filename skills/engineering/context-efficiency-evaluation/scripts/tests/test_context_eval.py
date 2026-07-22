from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from context_eval_runtime.canonical import canonical_json, path_is_within, snapshot_tree
from context_eval_runtime.contracts import ContractError, validate_document
from context_eval_runtime.evaluate import EvaluationError, evaluate
from context_eval_runtime.normalize import normalize_jsonl
import context_eval_runtime.normalize as normalize_runtime
import context_eval_runtime.workspace as workspace_runtime
from context_eval_runtime.workspace import (
    find_project_root, initialize_workspace, load_workspace, prepare_normalized,
    publish_normalized_events,
)


class RuntimeTests(unittest.TestCase):
    def input_document(self):
        return json.loads((FIXTURES / "input.json").read_text(encoding="utf-8"))

    def test_evaluate_matches_golden_and_preserves_gate_order(self):
        report = evaluate(self.input_document())
        expected = (FIXTURES / "report.golden.json").read_text(encoding="utf-8").rstrip("\n")
        self.assertEqual(canonical_json(report), expected)
        self.assertEqual([gate["name"] for gate in report["attempts"][0]["gates"]], ["telemetry", "correctness", "safety", "evidenceCoverage"])
        self.assertFalse(report["attempts"][2]["resourceEligible"])
        self.assertEqual(report["pairs"][0]["comparableMetrics"][0]["delta"], -300)
        self.assertNotIn("winner", report["pairs"][0])
        self.assertNotIn("score", report["pairs"][0])

    def test_explicit_missingness_is_required(self):
        document = self.input_document()
        document["attempts"][0]["metrics"]["output_tokens"]["missingReason"] = None
        with self.assertRaisesRegex(ContractError, "missingReason"):
            validate_document(document)

    def test_report_validation_rejects_nested_unknowns_and_inconsistency(self):
        report = evaluate(self.input_document())
        report["attempts"][0]["winner"] = True
        with self.assertRaisesRegex(ContractError, "unknown field.*winner"):
            validate_document(report)
        report = evaluate(self.input_document())
        report["pairs"][0]["resourceEligible"] = False
        with self.assertRaisesRegex(ContractError, "resourceEligible"):
            validate_document(report)
        report = evaluate(self.input_document())
        report["pairs"][0]["comparableMetrics"][0]["delta"] = 1
        with self.assertRaisesRegex(ContractError, "delta"):
            validate_document(report)

    def test_evidence_is_required_for_pass_fail_and_present_metrics(self):
        document = self.input_document()
        document["attempts"][0]["gates"]["telemetry"]["evidence"] = []
        with self.assertRaisesRegex(ContractError, "at least one evidence"):
            validate_document(document)
        document = self.input_document()
        document["attempts"][0]["metrics"]["context_bytes"]["evidence"] = []
        with self.assertRaisesRegex(ContractError, "at least one evidence"):
            validate_document(document)

    def test_finite_metric_subtraction_overflow_is_evaluation_error(self):
        document = self.input_document()
        document["attempts"][0]["metrics"]["context_bytes"]["value"] = -1e308
        document["attempts"][1]["metrics"]["context_bytes"]["value"] = 1e308
        with self.assertRaisesRegex(EvaluationError, "not finite"):
            evaluate(document)

    def test_normalization_preserves_framing_nonfinite_json_and_unique_ids(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "native.jsonl"
            source.write_bytes(b'{"id":"a:000002"}\r\n{}\n{"id":"dup"}\r\n{"id":"dup"}\nNaN\nbare\rcontent')
            events = normalize_jsonl(source, root / "blobs", "a")
            self.assertEqual([event["lineTerminator"] for event in events], ["crlf", "lf", "crlf", "lf", "lf", "none"])
            self.assertEqual(events[1]["eventId"], "a:000002:1")
            self.assertEqual(events[3]["eventId"], "a:000004")
            self.assertEqual(len({event["eventId"] for event in events}), len(events))
            self.assertEqual(events[4]["parseStatus"], "invalid_json")
            self.assertNotIn(b"\r", (root / "blobs" / events[4]["payloadBlob"]["sha256"]).read_bytes())
            self.assertIn(b"\r", (root / "blobs" / events[5]["payloadBlob"]["sha256"]).read_bytes())

    def test_blob_integrity_rejects_symlink_and_mismatched_existing_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "native.jsonl"
            source.write_bytes(b"not-json")
            digest = __import__("hashlib").sha256(b"not-json").hexdigest()
            blobs = root / "blobs"
            blobs.mkdir()
            target = root / "target"
            target.write_bytes(b"not-json")
            (blobs / digest).symlink_to(target)
            with self.assertRaisesRegex(ContractError, "not a regular file"):
                normalize_jsonl(source, blobs, "a")
            (blobs / digest).unlink()
            (blobs / digest).write_bytes(b"wrong")
            with self.assertRaisesRegex(ContractError, "does not match"):
                normalize_jsonl(source, blobs, "a")

    def test_blob_verification_rejects_digest_path_replacement_after_read(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "native.jsonl"
            source.write_bytes(b"not-json")
            digest = __import__("hashlib").sha256(b"not-json").hexdigest()
            blobs = root / "blobs"
            blobs.mkdir()
            digest_path = blobs / digest
            digest_path.write_bytes(b"not-json")
            real_stat = normalize_runtime.os.stat
            matching_stats = 0

            def replace_before_post_stat(path, *args, **kwargs):
                nonlocal matching_stats
                if path == digest and kwargs.get("dir_fd") is not None:
                    matching_stats += 1
                    if matching_stats == 2:
                        digest_path.rename(blobs / "verified-original")
                        digest_path.write_bytes(b"corrupt")
                return real_stat(path, *args, **kwargs)

            with mock.patch.object(normalize_runtime.os, "stat", side_effect=replace_before_post_stat):
                with self.assertRaisesRegex(ContractError, "changed while verifying"):
                    normalize_jsonl(source, blobs, "a")
            self.assertEqual(digest_path.read_bytes(), b"corrupt")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            valid = root / "valid.jsonl"
            valid.write_bytes(b'{"text":"kept"}\r')
            valid_event = normalize_jsonl(valid, root / "valid-blobs", "a", inline_limit_bytes=0)[0]
            self.assertEqual(valid_event["lineTerminator"], "none")
            valid_blob = root / "valid-blobs" / valid_event["payloadBlob"]["sha256"]
            self.assertEqual(valid_blob.read_bytes(), b'{"text":"kept"}\r')
            self.assertEqual(valid_event["parseStatus"], "parsed")
            invalid = root / "invalid.jsonl"
            invalid.write_bytes(b"not-json\r")
            invalid_event = normalize_jsonl(invalid, root / "invalid-blobs", "a")[0]
            self.assertEqual(invalid_event["lineTerminator"], "none")
            invalid_blob = root / "invalid-blobs" / invalid_event["payloadBlob"]["sha256"]
            self.assertEqual(invalid_blob.read_bytes(), b"not-json\r")

    def test_safe_integer_validation_and_out_of_range_rejection(self):
        document = self.input_document()
        limit = 9_007_199_254_740_991
        document["attempts"][0]["metrics"]["context_bytes"]["value"] = limit - 7
        document["attempts"][1]["metrics"]["context_bytes"]["value"] = limit
        validate_document(document)
        report = evaluate(document)
        self.assertEqual(report["pairs"][0]["comparableMetrics"][0]["delta"], 7)
        document["attempts"][1]["metrics"]["context_bytes"]["value"] = limit + 1
        with self.assertRaisesRegex(ContractError, "must be within"):
            validate_document(document)

    def test_report_rejects_self_pair(self):
        report = evaluate(self.input_document())
        report["pairs"][0]["treatmentAttemptId"] = report["pairs"][0]["baselineAttemptId"]
        with self.assertRaisesRegex(ContractError, "must be distinct"):
            validate_document(report)

    def test_blob_directory_symlink_is_rejected_without_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "native.jsonl"
            source.write_bytes(b"not-json")
            target = root / "target"
            target.mkdir()
            linked = root / "linked"
            linked.symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(ContractError, "non-symlink directory"):
                normalize_jsonl(source, linked, "a")
            self.assertEqual(list(target.iterdir()), [])

    def test_scalar_null_is_preserved_without_wrapper(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "null.jsonl"
            source.write_bytes(b"null\n42\n\"text\"")
            events = normalize_jsonl(source, root / "blobs", "a")
            self.assertIsNone(events[0]["payload"])
            self.assertIsNone(events[0]["payloadBlob"])
            self.assertEqual(events[1]["payload"], 42)
            self.assertEqual(events[2]["payload"], "text")
            for event in events:
                validate_document(event)

    def test_empty_attempt_id_publishes_no_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "native.jsonl"
            source.write_bytes(b"not-json")
            blobs = root / "blobs"
            with self.assertRaisesRegex(ContractError, "non-empty"):
                normalize_jsonl(source, blobs, "")
            self.assertFalse(blobs.exists())

    def test_segment_aware_containment(self):
        self.assertTrue(path_is_within("cache/items/a", "cache"))
        self.assertFalse(path_is_within("cache-old/a", "cache"))

    def test_snapshot_is_deterministic_and_excludes_contained_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "keep").mkdir()
            (root / "keep" / "a.txt").write_text("a", encoding="utf-8")
            (root / "cache").mkdir()
            (root / "cache" / "ignored.txt").write_text("ignored", encoding="utf-8")
            (root / "cache-old").mkdir()
            (root / "cache-old" / "kept.txt").write_text("kept", encoding="utf-8")
            first = snapshot_tree(root, ["cache"])
            second = snapshot_tree(root, ["cache"])
            self.assertEqual(first, second)
            validate_document(first)
            self.assertEqual([item["path"] for item in first["entries"]], ["cache-old/kept.txt", "keep/a.txt"])
            tampered = dict(first)
            tampered["entries"] = list(first["entries"])
            tampered["entries"][0] = dict(tampered["entries"][0], bytes=999)
            with self.assertRaisesRegex(ContractError, "treeSha256"):
                validate_document(tampered)

    def test_normalization_blobs_invalid_and_oversized_lines(self):
        with tempfile.TemporaryDirectory() as temporary:
            blobs = Path(temporary)
            events = normalize_jsonl(FIXTURES / "native.jsonl", blobs, "attempt", inline_limit_bytes=80)
            self.assertEqual([item["monotonicIndex"] for item in events], [1, 2, 3])
            self.assertEqual(events[0]["eventId"], "native-1")
            self.assertEqual(events[1]["parseStatus"], "invalid_json")
            self.assertIsNotNone(events[1]["payloadBlob"])
            self.assertIsNotNone(events[2]["payloadBlob"])
            self.assertEqual(len(list(blobs.iterdir())), 2)


class WorkspaceTests(unittest.TestCase):
    NOW = dt.datetime(2026, 7, 22, 9, 10, 11, tzinfo=dt.timezone(dt.timedelta(hours=-7)))

    def test_manifest_contract_rejects_bad_fields_dates_slugs_and_clock(self):
        valid = {"schemaVersion": "ctxeval.workspace.v1", "evaluationId": "pilot-1", "localDate": "2026-07-22", "createdAt": "2026-07-22T09:10:11-07:00"}
        validate_document(valid)
        for changed in (
            dict(valid, hostPath="/tmp/private"), dict(valid, evaluationId="Bad_ID"),
            dict(valid, evaluationId="a" * 65), dict(valid, localDate="2026-02-30"),
            dict(valid, createdAt="2026-07-22T09:10:11"),
        ):
            with self.assertRaises(ContractError):
                validate_document(changed)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ContractError, "timezone-aware"):
                initialize_workspace("pilot", Path(temporary), clock=lambda: dt.datetime(2026, 7, 22))

    def test_vcs_root_and_cwd_fallback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            nested = root / "a" / "b"; nested.mkdir(parents=True)
            self.assertEqual(find_project_root(nested), nested)
            (root / ".git").write_text("gitdir: elsewhere", encoding="utf-8")
            self.assertEqual(find_project_root(nested), root)

    def test_init_layout_reuse_identity_and_partial_states(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            workspace = initialize_workspace("pilot-1", root, clock=lambda: self.NOW)
            self.assertEqual(workspace.relative_to(root).as_posix(), ".context-evaluation/2026-07-22/pilot-1")
            self.assertTrue((workspace / "subject").is_dir())
            self.assertTrue((workspace / "evaluator").is_dir())
            manifest = load_workspace(workspace)
            self.assertEqual(set(manifest), {"schemaVersion", "evaluationId", "localDate", "createdAt"})
            with self.assertRaisesRegex(ContractError, "already exists"):
                initialize_workspace("pilot-1", root, clock=lambda: self.NOW)
            self.assertEqual(initialize_workspace("pilot-1", root, reuse=True, clock=lambda: self.NOW), workspace)
            (workspace / "manifest.json").write_text(json.dumps(dict(manifest, evaluationId="other")), encoding="utf-8")
            with self.assertRaises(ContractError):
                initialize_workspace("pilot-1", root, reuse=True, clock=lambda: self.NOW)

    def test_symlinks_non_directories_and_missing_layout_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            container = root / ".context-evaluation"
            target = root / "target"; target.mkdir()
            container.symlink_to(target, target_is_directory=True)
            with self.assertRaises(ContractError):
                initialize_workspace("pilot", root, clock=lambda: self.NOW)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / ".context-evaluation").write_text("not dir", encoding="utf-8")
            with self.assertRaises(ContractError):
                initialize_workspace("pilot", root, clock=lambda: self.NOW)
        with tempfile.TemporaryDirectory() as temporary:
            workspace = initialize_workspace("pilot", Path(temporary).resolve(), clock=lambda: self.NOW)
            (workspace / "subject").rmdir()
            with self.assertRaises(ContractError):
                load_workspace(workspace)
    def test_workspace_ancestor_symlink_is_rejected_for_validation_and_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            real = root / "real"
            real.mkdir()
            workspace = initialize_workspace("pilot", real, clock=lambda: self.NOW)
            linked = root / "linked"
            linked.symlink_to(real, target_is_directory=True)
            redirected = linked / workspace.relative_to(real)
            with self.assertRaises(ContractError):
                load_workspace(redirected)
            before = list((workspace / "subject").iterdir())
            with self.assertRaises(ContractError):
                prepare_normalized(redirected, "baseline")
            self.assertEqual(list((workspace / "subject").iterdir()), before)

    def test_publication_retains_validated_subject_descriptor(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            workspace = initialize_workspace("pilot", root, clock=lambda: self.NOW)
            tree_root = root / "tree"
            tree_root.mkdir()
            (tree_root / "a").write_text("a", encoding="utf-8")
            tree = snapshot_tree(tree_root, [])
            real_validate = workspace_runtime._validated_workspace_handle

            def swap_subject(path):
                handle = real_validate(path)
                subject = workspace / "subject"
                subject.rename(workspace / "subject-original")
                subject.mkdir()
                return handle

            with mock.patch.object(workspace_runtime, "_validated_workspace_handle", side_effect=swap_subject):
                workspace_runtime.publish_tree(workspace, "baseline", "before", tree)
            original = workspace / "subject-original" / "attempts" / "baseline" / "trees" / "before.json"
            self.assertEqual(json.loads(original.read_text()), tree)
            self.assertEqual(list((workspace / "subject").iterdir()), [])

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            workspace = initialize_workspace("pilot", root, clock=lambda: self.NOW)
            normalized_fd, blobs_fd = prepare_normalized(workspace, "baseline")
            try:
                moved = workspace.with_name("pilot-moved")
                workspace.rename(moved)
                replacement = initialize_workspace("pilot", root, clock=lambda: self.NOW)
                publish_normalized_events(normalized_fd, "retained\n")
                self.assertEqual((moved / "subject" / "attempts" / "baseline" / "normalized" / "events.jsonl").read_text(), "retained\n")
                self.assertFalse((replacement / "subject" / "attempts" / "baseline").exists())
            finally:
                os.close(blobs_fd)
                os.close(normalized_fd)


class CliTests(unittest.TestCase):
    def run_cli(self, *arguments, input_text=None):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "context_eval.py"), *map(str, arguments)],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
            env={"PYTHONDONTWRITEBYTECODE": "1"},
        )

    def init_cli_workspace(self, root):
        result = self.run_cli("init", "pilot", "--root", root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return Path(json.loads(result.stdout)["workspace"])

    def test_init_warns_without_editing_gitignore(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            gitignore = root / ".gitignore"
            gitignore.write_text("existing\n", encoding="utf-8")
            result = self.run_cli("init", "pilot", "--root", root)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "warning: .context-evaluation is not auto-ignored; explicitly exclude it from project snapshots\n")
            self.assertEqual(gitignore.read_text(encoding="utf-8"), "existing\n")
            self.assertEqual(set(json.loads(result.stdout)), {"workspace"})

    def test_snapshot_cli_excludes_workspace_but_keeps_similarly_prefixed_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            workspace = self.init_cli_workspace(root)
            (workspace / "subject" / "evidence.txt").write_text("exclude", encoding="utf-8")
            similar = root / ".context-evaluation-old"
            similar.mkdir()
            (similar / "keep.txt").write_text("keep", encoding="utf-8")
            result = self.run_cli("snapshot", root, "--exclude", ".context-evaluation")
            self.assertEqual(result.returncode, 0, result.stderr)
            paths = [entry["path"] for entry in json.loads(result.stdout)["entries"]]
            self.assertEqual(paths, [".context-evaluation-old/keep.txt"])

    def test_workspace_cli_publication_fixed_paths_and_immutability(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            workspace = self.init_cli_workspace(root)
            validated_workspace = self.run_cli("validate", workspace, "--contract", "ctxeval.workspace.v1")
            self.assertEqual(validated_workspace.returncode, 0, validated_workspace.stderr)
            self.assertEqual(json.loads(validated_workspace.stdout)["evaluationId"], "pilot")
            normalized = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "semantic/id", "--workspace", workspace, "--artifact-slug", "baseline", "--inline-limit-bytes", "80")
            self.assertEqual(normalized.returncode, 0, normalized.stderr)
            base = workspace / "subject" / "attempts" / "baseline" / "normalized"
            self.assertEqual((base / "events.jsonl").read_text(encoding="utf-8"), "".join(canonical_json(event) + "\n" for event in json.loads(normalized.stdout)))
            self.assertEqual(len(list((base / "blobs").iterdir())), 2)
            duplicate = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "semantic/id", "--workspace", workspace, "--artifact-slug", "baseline", "--inline-limit-bytes", "80")
            self.assertEqual(duplicate.returncode, 4)
            self.assertEqual(duplicate.stdout, "")
            tree_root = root / "tree"; tree_root.mkdir(); (tree_root / "a").write_text("a", encoding="utf-8")
            snap = self.run_cli("snapshot", tree_root, "--workspace", workspace, "--artifact-slug", "baseline", "--label", "after", "--exclude", ".context-evaluation")
            self.assertEqual(snap.returncode, 0, snap.stderr)
            baseline_tree = workspace / "subject" / "attempts" / "baseline" / "trees" / "after.json"
            self.assertEqual(json.loads(baseline_tree.read_text()), json.loads(snap.stdout))
            treatment = self.run_cli("snapshot", tree_root, "--workspace", workspace, "--artifact-slug", "treatment", "--label", "after", "--exclude", ".context-evaluation")
            self.assertEqual(treatment.returncode, 0, treatment.stderr)
            treatment_tree = workspace / "subject" / "attempts" / "treatment" / "trees" / "after.json"
            self.assertEqual(json.loads(treatment_tree.read_text()), json.loads(snap.stdout))
            treatment_normalized = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "treatment/id", "--workspace", workspace, "--artifact-slug", "treatment", "--inline-limit-bytes", "80")
            self.assertEqual(treatment_normalized.returncode, 0, treatment_normalized.stderr)
            self.assertTrue((workspace / "subject" / "attempts" / "treatment" / "normalized" / "events.jsonl").is_file())
            self.assertTrue(treatment_tree.is_file())
            report = self.run_cli("evaluate", FIXTURES / "input.json", "--workspace", workspace)
            self.assertEqual(report.returncode, 0, report.stderr)
            self.assertEqual((workspace / "evaluator" / "report.json").read_text(), report.stdout)
            duplicate_report = self.run_cli("evaluate", FIXTURES / "input.json", "--workspace", workspace)
            self.assertEqual(duplicate_report.returncode, 4)
            self.assertEqual(duplicate_report.stdout, "")
            self.assertFalse((workspace / "oracle").exists())
            self.assertFalse((workspace / "index").exists())

    def test_normalize_workspace_prevalidates_and_never_reuses_claimed_slot(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            workspace = self.init_cli_workspace(root)
            attempts = workspace / "subject" / "attempts"
            empty_id = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "", "--workspace", workspace, "--artifact-slug", "empty")
            negative = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "a", "--workspace", workspace, "--artifact-slug", "negative", "--inline-limit-bytes", "-1")
            self.assertEqual((empty_id.returncode, negative.returncode), (4, 4))
            self.assertFalse(attempts.exists())

            partial = attempts / "partial" / "normalized"
            partial.mkdir(parents=True)
            occupied = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "different", "--workspace", workspace, "--artifact-slug", "partial")
            self.assertEqual(occupied.returncode, 4)
            self.assertEqual(occupied.stdout, "")
            self.assertEqual(list(partial.iterdir()), [])

            missing = root / "missing.jsonl"
            failed = self.run_cli("normalize", missing, "--attempt-id", "first", "--workspace", workspace, "--artifact-slug", "failed")
            self.assertEqual(failed.returncode, 3)
            retry = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "second", "--workspace", workspace, "--artifact-slug", "failed")
            self.assertEqual(retry.returncode, 4)
            self.assertTrue((attempts / "failed" / "normalized" / "blobs").is_dir())

    def test_workspace_option_contract_and_legacy_stdout_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            legacy = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "a", "--blobs-dir", temporary, "--inline-limit-bytes", "80")
            self.assertEqual(legacy.stdout, (FIXTURES / "normalize.legacy.stdout.golden").read_text(encoding="utf-8"))
            self.assertEqual(legacy.stderr, "")
            missing_slug = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "a", "--workspace", temporary)
            self.assertEqual(missing_slug.returncode, 4)
            self.assertEqual(missing_slug.stdout, "")
            partial_snapshot = self.run_cli("snapshot", temporary, "--workspace", temporary, "--label", "x")
            self.assertEqual(partial_snapshot.returncode, 4)
            self.assertEqual(partial_snapshot.stdout, "")
            incompatible = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "a", "--blobs-dir", temporary, "--workspace", temporary, "--artifact-slug", "a")
            self.assertEqual(incompatible.returncode, 2)
            self.assertEqual(incompatible.stdout, "")

    def test_evaluate_cli_is_canonical_and_golden(self):
        result = self.run_cli("evaluate", FIXTURES / "input.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (FIXTURES / "report.golden.json").read_text(encoding="utf-8"))
        self.assertEqual(result.stderr, "")

    def test_validate_supports_stdin(self):
        source = (FIXTURES / "input.json").read_text(encoding="utf-8")
        result = self.run_cli("validate", "-", "--contract", "ctxeval.input.v1", input_text=source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), json.loads(source))

    def test_strict_argparse_uses_exit_two(self):
        result = self.run_cli("evaluate", FIXTURES / "input.json", "extra")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_io_and_contract_exit_codes(self):
        missing = self.run_cli("evaluate", FIXTURES / "missing.json")
        self.assertEqual(missing.returncode, 3)
        with tempfile.TemporaryDirectory() as temporary:
            invalid = Path(temporary) / "invalid.json"
            invalid.write_text("{}", encoding="utf-8")
            result = self.run_cli("evaluate", invalid)
        self.assertEqual(result.returncode, 4)

    def test_evaluation_overflow_uses_exit_five(self):
        document = RuntimeTests().input_document()
        document["attempts"][0]["metrics"]["context_bytes"]["value"] = -1e308
        document["attempts"][1]["metrics"]["context_bytes"]["value"] = 1e308
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "overflow.json"
            source.write_text(json.dumps(document), encoding="utf-8")
            result = self.run_cli("evaluate", source)
        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.stdout, "")
        self.assertIn("evaluation error", result.stderr)

    def test_oversized_integer_is_contract_error_not_exit_six(self):
        source_document = (FIXTURES / "input.json").read_text(encoding="utf-8")
        oversized = "1" * 5001
        source_document = source_document.replace('"value":1200', f'"value":{oversized}', 1)
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "huge.json"
            source.write_text(source_document, encoding="utf-8")
            validated = self.run_cli("validate", source, "--contract", "ctxeval.input.v1")
            evaluated = self.run_cli("evaluate", source)
        self.assertEqual(validated.returncode, 4)
        self.assertEqual(evaluated.returncode, 4)
        self.assertNotEqual(validated.returncode, 6)
        self.assertIn("outside supported range", validated.stderr)

    def test_normalize_cli_emits_json_array_and_blobs(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = self.run_cli("normalize", FIXTURES / "native.jsonl", "--attempt-id", "a", "--blobs-dir", temporary, "--inline-limit-bytes", "80")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)), 3)
            self.assertEqual(len(list(Path(temporary).iterdir())), 2)


if __name__ == "__main__":
    unittest.main()
