"""Gate-first, noncompensable evaluation of generic attempts and pairs."""

from __future__ import annotations

import math
from typing import Any

from .contracts import GATE_NAMES, REPORT_VERSION, validate_input, validate_report


class EvaluationError(ValueError):
    """Raised when valid input cannot be evaluated without forbidden inference."""


def _attempt_report(attempt: dict[str, Any]) -> dict[str, Any]:
    gates = []
    eligible = attempt["outcome"] == "success"
    for gate_name in GATE_NAMES:
        gate = attempt["gates"][gate_name]
        gate_passed = gate["status"] == "pass"
        eligible = eligible and gate_passed
        gates.append({"evidence": gate["evidence"], "name": gate_name, "note": gate["note"], "status": gate["status"]})
    return {
        "attemptId": attempt["attemptId"],
        "gates": gates,
        "metrics": attempt["metrics"],
        "outcome": attempt["outcome"],
        "resourceEligible": eligible,
    }


def _pair_metrics(baseline: dict[str, Any], treatment: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    comparable: list[dict[str, Any]] = []
    unavailable: list[dict[str, str]] = []
    names = sorted(set(baseline["metrics"]) | set(treatment["metrics"]))
    for name in names:
        left = baseline["metrics"].get(name)
        right = treatment["metrics"].get(name)
        reason: str | None = None
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
            unavailable.append({"metric": name, "reason": reason})
            continue
        try:
            delta = right["value"] - left["value"]
            representable = not isinstance(delta, float) or math.isfinite(delta)
        except (ArithmeticError, OverflowError) as error:
            raise EvaluationError(f"metric {name!r} subtraction is not representable") from error
        if not representable:
            raise EvaluationError(f"metric {name!r} subtraction is not finite")
        comparable.append({
            "baseline": left["value"],
            "delta": delta,
            "metric": name,
            "treatment": right["value"],
            "unit": left["unit"],
        })
    return comparable, unavailable


def evaluate(document: dict[str, Any]) -> dict[str, Any]:
    validate_input(document)
    attempts = [_attempt_report(item) for item in document["attempts"]]
    attempts_by_id = {item["attemptId"]: item for item in attempts}
    pairs: list[dict[str, Any]] = []

    for pair in document["pairs"]:
        baseline = attempts_by_id[pair["baselineAttemptId"]]
        treatment = attempts_by_id[pair["treatmentAttemptId"]]
        reasons: list[str] = []
        if not baseline["resourceEligible"]:
            reasons.append("baseline_not_resource_eligible")
        if not treatment["resourceEligible"]:
            reasons.append("treatment_not_resource_eligible")
        eligible = not reasons
        comparable, unavailable = _pair_metrics(baseline, treatment) if eligible else ([], [])
        pairs.append({
            "baselineAttemptId": baseline["attemptId"],
            "comparableMetrics": comparable,
            "ineligibleReasons": reasons,
            "pairId": pair["pairId"],
            "resourceEligible": eligible,
            "treatmentAttemptId": treatment["attemptId"],
            "unavailableMetrics": unavailable,
        })

    report = {"attempts": attempts, "pairs": pairs, "schemaVersion": REPORT_VERSION}
    validate_report(report)
    return report
