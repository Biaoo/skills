"""Strict validators for the versioned runtime contracts."""

from __future__ import annotations

import datetime as dt
import math
import re
from typing import Any

from .canonical import MAX_SAFE_INTEGER, normalize_relative_path, sha256_json

INPUT_VERSION = "ctxeval.input.v1"
EVENT_VERSION = "ctxeval.event.v1"
TREE_VERSION = "ctxeval.tree.v1"
REPORT_VERSION = "ctxeval.report.v1"
WORKSPACE_VERSION = "ctxeval.workspace.v1"
GATE_NAMES = ("telemetry", "correctness", "safety", "evidenceCoverage")
OUTCOMES = ("success", "failed", "refused", "timed_out", "permission_denied", "infrastructure_failed")
GATE_STATUSES = ("pass", "fail", "unknown", "not_applicable")
PROVENANCE = ("native", "derived", "adjudicated")
UNAVAILABLE_REASONS = ("missing_from_attempt", "explicitly_missing_value", "non_native_metric", "incompatible_unit", "incompatible_measurement")
INELIGIBLE_REASONS = ("baseline_not_resource_eligible", "treatment_not_resource_eligible")


class ContractError(ValueError):
    """Raised when a document violates a runtime boundary contract."""


def _error(path: str, message: str) -> None:
    raise ContractError(f"{path}: {message}")


def _object(value: Any, path: str, required: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        _error(path, "must be an object")
    missing = required - set(value)
    extra = set(value) - required
    if missing:
        _error(path, f"missing required field(s): {', '.join(sorted(missing))}")
    if extra:
        _error(path, f"unknown field(s): {', '.join(sorted(extra))}")
    return value


def _string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value:
        _error(path, "must be a non-empty string")
    return value


def _integer(value: Any, path: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        _error(path, f"must be an integer >= {minimum}")
    return value


def _number(value: Any, path: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _error(path, "must be an integer in the safe JSON range or a finite float")
    if isinstance(value, int) and abs(value) > MAX_SAFE_INTEGER:
        _error(path, f"integer must be within [-{MAX_SAFE_INTEGER}, {MAX_SAFE_INTEGER}]")
    if isinstance(value, float) and not math.isfinite(value):
        _error(path, "must be an integer in the safe JSON range or a finite float")
    return value


def _nullable_string(value: Any, path: str) -> str | None:
    return None if value is None else _string(value, path)


def _references(value: Any, path: str, required: bool = False) -> None:
    if not isinstance(value, list):
        _error(path, "must be an array")
    for index, item in enumerate(value):
        _string(item, f"{path}[{index}]")
    if len(value) != len(set(value)):
        _error(path, "must not contain duplicates")
    if required and not value:
        _error(path, "must contain at least one evidence reference")


def _digest(value: Any, path: str) -> str:
    digest = _string(value, path)
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        _error(path, "must be a lowercase SHA-256 digest")
    return digest


def _validate_gate(gate: Any, path: str, include_name: bool = False, expected_name: str | None = None) -> dict[str, Any]:
    fields = {"status", "evidence", "note"} | ({"name"} if include_name else set())
    item = _object(gate, path, fields)
    if include_name and item["name"] != expected_name:
        _error(path + ".name", f"must equal {expected_name!r}")
    if item["status"] not in GATE_STATUSES:
        _error(path + ".status", f"must be one of {', '.join(GATE_STATUSES)}")
    _references(item["evidence"], path + ".evidence", item["status"] in ("pass", "fail"))
    _nullable_string(item["note"], path + ".note")
    return item


def _validate_metric(metric: Any, path: str) -> dict[str, Any]:
    item = _object(metric, path, {"value", "unit", "provenance", "compatibilityKey", "missingReason", "evidence"})
    number = item["value"]
    if number is not None:
        _number(number, path + ".value")
    _string(item["unit"], path + ".unit")
    if item["provenance"] not in PROVENANCE:
        _error(path + ".provenance", f"must be one of {', '.join(PROVENANCE)}")
    _nullable_string(item["compatibilityKey"], path + ".compatibilityKey")
    missing_reason = _nullable_string(item["missingReason"], path + ".missingReason")
    if (number is None) != (missing_reason is not None):
        _error(path, "value null requires a missingReason; present value requires missingReason null")
    _references(item["evidence"], path + ".evidence", number is not None)
    return item


def _validate_metrics(metrics: Any, path: str) -> dict[str, Any]:
    if not isinstance(metrics, dict):
        _error(path, "must be an object")
    for name, metric in metrics.items():
        _string(name, path + " key")
        _validate_metric(metric, path + f".{name}")
    return metrics


def validate_input(document: Any) -> dict[str, Any]:
    obj = _object(document, "$", {"schemaVersion", "attempts", "pairs"})
    if obj["schemaVersion"] != INPUT_VERSION:
        _error("$.schemaVersion", f"must equal {INPUT_VERSION!r}")
    if not isinstance(obj["attempts"], list):
        _error("$.attempts", "must be an array")
    attempt_ids: set[str] = set()
    for index, attempt in enumerate(obj["attempts"]):
        path = f"$.attempts[{index}]"
        item = _object(attempt, path, {"attemptId", "outcome", "gates", "metrics"})
        attempt_id = _string(item["attemptId"], path + ".attemptId")
        if attempt_id in attempt_ids:
            _error(path + ".attemptId", "must be unique")
        attempt_ids.add(attempt_id)
        if item["outcome"] not in OUTCOMES:
            _error(path + ".outcome", f"must be one of {', '.join(OUTCOMES)}")
        gates = _object(item["gates"], path + ".gates", set(GATE_NAMES))
        for name in GATE_NAMES:
            _validate_gate(gates[name], path + f".gates.{name}")
        _validate_metrics(item["metrics"], path + ".metrics")
    if not isinstance(obj["pairs"], list):
        _error("$.pairs", "must be an array")
    pair_ids: set[str] = set()
    for index, pair in enumerate(obj["pairs"]):
        path = f"$.pairs[{index}]"
        item = _object(pair, path, {"pairId", "baselineAttemptId", "treatmentAttemptId"})
        pair_id = _string(item["pairId"], path + ".pairId")
        if pair_id in pair_ids:
            _error(path + ".pairId", "must be unique")
        pair_ids.add(pair_id)
        for field in ("baselineAttemptId", "treatmentAttemptId"):
            if _string(item[field], path + "." + field) not in attempt_ids:
                _error(path + "." + field, "must reference an existing attempt")
        if item["baselineAttemptId"] == item["treatmentAttemptId"]:
            _error(path, "baseline and treatment must be distinct")
    return obj


def validate_event(document: Any) -> dict[str, Any]:
    fields = {"schemaVersion", "eventId", "attemptId", "monotonicIndex", "nativeLine", "lineTerminator", "type", "actorId", "parentId", "payload", "payloadBlob", "parseStatus"}
    obj = _object(document, "$", fields)
    if obj["schemaVersion"] != EVENT_VERSION:
        _error("$.schemaVersion", f"must equal {EVENT_VERSION!r}")
    for field in ("eventId", "attemptId", "type"):
        _string(obj[field], "$." + field)
    _integer(obj["monotonicIndex"], "$.monotonicIndex", 1)
    _integer(obj["nativeLine"], "$.nativeLine", 1)
    if obj["lineTerminator"] not in ("none", "lf", "crlf"):
        _error("$.lineTerminator", "must be none, lf, or crlf")
    _nullable_string(obj["actorId"], "$.actorId")
    _nullable_string(obj["parentId"], "$.parentId")
    if obj["parseStatus"] not in ("parsed", "invalid_json"):
        _error("$.parseStatus", "must be parsed or invalid_json")
    blob = obj["payloadBlob"]
    if blob is not None:
        blob = _object(blob, "$.payloadBlob", {"sha256", "bytes"})
        _digest(blob["sha256"], "$.payloadBlob.sha256")
        _integer(blob["bytes"], "$.payloadBlob.bytes")
    if blob is not None and obj["payload"] is not None:
        _error("$", "blob-backed events must have a null inline payload")
    if blob is None and obj["parseStatus"] != "parsed":
        _error("$.payloadBlob", "invalid JSON must be preserved as a blob")
    return obj


def validate_tree(document: Any) -> dict[str, Any]:
    obj = _object(document, "$", {"schemaVersion", "entries", "excludedPaths", "treeSha256"})
    if obj["schemaVersion"] != TREE_VERSION:
        _error("$.schemaVersion", f"must equal {TREE_VERSION!r}")
    if not isinstance(obj["entries"], list):
        _error("$.entries", "must be an array")
    paths: list[str] = []
    for index, entry in enumerate(obj["entries"]):
        path = f"$.entries[{index}]"
        item = _object(entry, path, {"bytes", "path", "sha256", "type"})
        try:
            paths.append(normalize_relative_path(item["path"]))
        except ValueError as error:
            _error(path + ".path", str(error))
        if item["type"] not in ("file", "symlink"):
            _error(path + ".type", "must be file or symlink")
        _integer(item["bytes"], path + ".bytes")
        _digest(item["sha256"], path + ".sha256")
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        _error("$.entries", "paths must be unique and sorted")
    if not isinstance(obj["excludedPaths"], list):
        _error("$.excludedPaths", "must be an array")
    excluded: list[str] = []
    for index, value in enumerate(obj["excludedPaths"]):
        try:
            excluded.append(normalize_relative_path(value))
        except ValueError as error:
            _error(f"$.excludedPaths[{index}]", str(error))
    if excluded != sorted(excluded) or len(excluded) != len(set(excluded)):
        _error("$.excludedPaths", "must be unique and sorted")
    digest = _digest(obj["treeSha256"], "$.treeSha256")
    if digest != sha256_json({key: value for key, value in obj.items() if key != "treeSha256"}):
        _error("$.treeSha256", "does not match canonical tree content")
    return obj


def validate_report(document: Any) -> dict[str, Any]:
    obj = _object(document, "$", {"schemaVersion", "attempts", "pairs"})
    if obj["schemaVersion"] != REPORT_VERSION:
        _error("$.schemaVersion", f"must equal {REPORT_VERSION!r}")
    if not isinstance(obj["attempts"], list):
        _error("$.attempts", "must be an array")
    attempts: dict[str, dict[str, Any]] = {}
    for index, attempt in enumerate(obj["attempts"]):
        path = f"$.attempts[{index}]"
        item = _object(attempt, path, {"attemptId", "outcome", "gates", "metrics", "resourceEligible"})
        attempt_id = _string(item["attemptId"], path + ".attemptId")
        if attempt_id in attempts:
            _error(path + ".attemptId", "must be unique")
        if item["outcome"] not in OUTCOMES:
            _error(path + ".outcome", f"must be one of {', '.join(OUTCOMES)}")
        if not isinstance(item["gates"], list) or len(item["gates"]) != len(GATE_NAMES):
            _error(path + ".gates", "must contain the four ordered gates")
        for gate_index, name in enumerate(GATE_NAMES):
            _validate_gate(item["gates"][gate_index], path + f".gates[{gate_index}]", True, name)
        _validate_metrics(item["metrics"], path + ".metrics")
        expected = item["outcome"] == "success" and all(gate["status"] == "pass" for gate in item["gates"])
        if not isinstance(item["resourceEligible"], bool) or item["resourceEligible"] != expected:
            _error(path + ".resourceEligible", f"must equal {expected}")
        attempts[attempt_id] = item
    if not isinstance(obj["pairs"], list):
        _error("$.pairs", "must be an array")
    pair_ids: set[str] = set()
    for index, pair in enumerate(obj["pairs"]):
        path = f"$.pairs[{index}]"
        item = _object(pair, path, {"pairId", "baselineAttemptId", "treatmentAttemptId", "resourceEligible", "ineligibleReasons", "comparableMetrics", "unavailableMetrics"})
        pair_id = _string(item["pairId"], path + ".pairId")
        if pair_id in pair_ids:
            _error(path + ".pairId", "must be unique")
        pair_ids.add(pair_id)
        refs = []
        for field in ("baselineAttemptId", "treatmentAttemptId"):
            ref = _string(item[field], path + "." + field)
            if ref not in attempts:
                _error(path + "." + field, "must reference a report attempt")
            refs.append(attempts[ref])
        if item["baselineAttemptId"] == item["treatmentAttemptId"]:
            _error(path, "baseline and treatment must be distinct")
        expected_reasons = [reason for reason, attempt in zip(INELIGIBLE_REASONS, refs) if not attempt["resourceEligible"]]
        if item["ineligibleReasons"] != expected_reasons:
            _error(path + ".ineligibleReasons", f"must equal {expected_reasons!r}")
        eligible = not expected_reasons
        if not isinstance(item["resourceEligible"], bool) or item["resourceEligible"] != eligible:
            _error(path + ".resourceEligible", f"must equal {eligible}")
        if not isinstance(item["comparableMetrics"], list) or not isinstance(item["unavailableMetrics"], list):
            _error(path, "comparableMetrics and unavailableMetrics must be arrays")
        if not eligible and (item["comparableMetrics"] or item["unavailableMetrics"]):
            _error(path, "ineligible pairs must not contain metric comparisons")
        expected_comparable: list[dict[str, Any]] = []
        expected_unavailable: list[dict[str, str]] = []
        if eligible:
            left_metrics, right_metrics = refs[0]["metrics"], refs[1]["metrics"]
            for name in sorted(set(left_metrics) | set(right_metrics)):
                left, right = left_metrics.get(name), right_metrics.get(name)
                reason = None
                if left is None or right is None:
                    reason = "missing_from_attempt"
                elif left["value"] is None or right["value"] is None:
                    reason = "explicitly_missing_value"
                elif left["provenance"] != "native" or right["provenance"] != "native":
                    reason = "non_native_metric"
                elif left["unit"] != right["unit"]:
                    reason = "incompatible_unit"
                elif left["compatibilityKey"] is None or left["compatibilityKey"] != right["compatibilityKey"]:
                    reason = "incompatible_measurement"
                if reason:
                    expected_unavailable.append({"metric": name, "reason": reason})
                else:
                    try:
                        delta = right["value"] - left["value"]
                    except (ArithmeticError, OverflowError) as error:
                        _error(path + ".comparableMetrics", f"metric {name!r} difference is not representable: {error}")
                    if isinstance(delta, float) and not math.isfinite(delta):
                        _error(path + ".comparableMetrics", f"metric {name!r} has a non-finite difference")
                    expected_comparable.append({"baseline": left["value"], "delta": delta, "metric": name, "treatment": right["value"], "unit": left["unit"]})
        metric_names: set[str] = set()
        for metric_index, metric in enumerate(item["comparableMetrics"]):
            metric_path = path + f".comparableMetrics[{metric_index}]"
            value = _object(metric, metric_path, {"metric", "baseline", "treatment", "delta", "unit"})
            name = _string(value["metric"], metric_path + ".metric")
            if name in metric_names:
                _error(metric_path + ".metric", "must be unique across pair metrics")
            metric_names.add(name)
            baseline = _number(value["baseline"], metric_path + ".baseline")
            treatment = _number(value["treatment"], metric_path + ".treatment")
            delta = _number(value["delta"], metric_path + ".delta")
            _string(value["unit"], metric_path + ".unit")
            if not math.isfinite(treatment - baseline) or delta != treatment - baseline:
                _error(metric_path + ".delta", "must equal the finite treatment-minus-baseline difference")
        for metric_index, metric in enumerate(item["unavailableMetrics"]):
            metric_path = path + f".unavailableMetrics[{metric_index}]"
            value = _object(metric, metric_path, {"metric", "reason"})
            name = _string(value["metric"], metric_path + ".metric")
            if name in metric_names:
                _error(metric_path + ".metric", "must be unique across pair metrics")
            metric_names.add(name)
            if value["reason"] not in UNAVAILABLE_REASONS:
                _error(metric_path + ".reason", f"must be one of {', '.join(UNAVAILABLE_REASONS)}")
        if item["comparableMetrics"] != expected_comparable:
            _error(path + ".comparableMetrics", "must exactly match eligible compatible native attempt metrics")
        if item["unavailableMetrics"] != expected_unavailable:
            _error(path + ".unavailableMetrics", "must exactly match unavailable attempt metrics")
    return obj


def validate_workspace(document: Any) -> dict[str, Any]:
    obj = _object(document, "$", {"schemaVersion", "evaluationId", "localDate", "createdAt"})
    if obj["schemaVersion"] != WORKSPACE_VERSION:
        _error("$.schemaVersion", f"must equal {WORKSPACE_VERSION!r}")
    evaluation_id = _string(obj["evaluationId"], "$.evaluationId")
    if len(evaluation_id) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", evaluation_id):
        _error("$.evaluationId", "must be a lowercase ASCII slug of at most 64 characters")
    local_date = _string(obj["localDate"], "$.localDate")
    try:
        parsed_date = dt.date.fromisoformat(local_date)
    except ValueError as error:
        _error("$.localDate", f"must be a real ISO calendar date: {error}")
    if parsed_date.isoformat() != local_date:
        _error("$.localDate", "must use YYYY-MM-DD format")
    created_at = _string(obj["createdAt"], "$.createdAt")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})", created_at):
        _error("$.createdAt", "must be RFC3339 with an explicit UTC offset")
    try:
        parsed_time = dt.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as error:
        _error("$.createdAt", f"must be RFC3339: {error}")
    if parsed_time.tzinfo is None or parsed_time.utcoffset() is None:
        _error("$.createdAt", "must include an explicit UTC offset")
    if parsed_time.date() != parsed_date:
        _error("$.createdAt", "local date must equal localDate")
    return obj


def validate_document(document: Any, expected: str | None = None) -> dict[str, Any]:
    if not isinstance(document, dict):
        _error("$", "must be an object")
    version = document.get("schemaVersion")
    if expected is not None and version != expected:
        _error("$.schemaVersion", f"must equal {expected!r}")
    validators = {INPUT_VERSION: validate_input, EVENT_VERSION: validate_event, TREE_VERSION: validate_tree, REPORT_VERSION: validate_report, WORKSPACE_VERSION: validate_workspace}
    if version not in validators:
        _error("$.schemaVersion", "unsupported contract version")
    return validators[version](document)
