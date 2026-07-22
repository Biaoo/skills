---
name: context-efficiency-evaluation
description: Use when reviewing recorded agent runs for avoidable context consumption, comparing quality-qualified matched traces, designing a context-efficiency experiment, or validating the evaluator skill itself. Applies to broad or repeated retrieval, oversized tool results, premature reference loading, weak continuation, hidden cost transfer, and unsupported efficiency claims; do not use for generic context-window explanations, prompt shortening without run evidence, or directly implementing an optimization.
metadata:
  short-description: Evaluate agent context efficiency behind quality and safety gates
---

# Context-Efficiency Evaluation

Evaluate whether an agent system uses less context or navigation without sacrificing the work the context exists to support.

Core principle:

> Context efficiency is resource improvement subject to correctness, safety, evidence, and non-inferiority constraints. Resource savings never compensate for incorrect or unsafe behavior.

Keep the subject run separate from the evaluator run. Account for the subject system's work, including delegated or external context work; do not confuse evaluator analysis cost with subject-run cost.

## Choose the Evaluation Mode

- **Single-trace audit:** diagnose avoidable breadth, repetition, oversized results, weak evidence, rework, and poor continuation. A single run can reveal candidates, not an optimization effect.
- **Matched-run comparison:** compare baseline and treatment for the same versioned task under controlled conditions. Interpret paired resource differences only after both runs qualify on correctness and safety.
- **Experiment design:** define the estimand, fixtures, assignment, hidden acceptance, instrumentation, non-inferiority rule, and decision gates before collecting results.
- **Skill validation:** hold subject traces fixed and test whether loading this evaluator skill improves evidence-linked analysis. Do not conflate this with evaluating a task-time context optimization.

If the request lacks recorded run evidence, limit the result to experiment design or state that empirical evaluation is not yet possible.

## Apply Gates Before Resource Metrics

Use this order and do not lead with token counts:

1. **Telemetry sufficiency:** state what the trace can and cannot observe, identify provenance gaps, and separate unavailable data from zero.
2. **Correctness qualification:** apply the task's versioned acceptance and verification requirements.
3. **Safety qualification:** check authorization, security, privacy, policy, and other task-specific prohibitions.
4. **Evidence coverage:** determine whether protected task invariants have evidence, not merely whether files or tools were touched.
5. **Resource comparison:** compare only matched, quality-qualified runs using measurements the telemetry actually supports.
6. **Uncertainty and limitations:** report matching weaknesses, missing observations, evaluator disagreement, and validity threats.
7. **Candidate next experiment:** turn plausible waste into a testable change, not a proven improvement.

Correctness and safety are non-compensable gates. A failed, refused, timed-out, permission-denied, or infrastructure-failed run remains in unconditional outcome and cost reporting, but it is not an eligible success for conditional resource comparison. Never discard such runs to create survivor-only results.

Prefer gate-based or Pareto decisions to a universal scalar score. If a scalar is required, expose correctness and safety separately and declare normalization, weights, sensitivity analysis, and the tradeoffs the score hides.

## Preserve Evidence Semantics

Label every substantive finding:

- **observed:** directly present in the trace or deterministic measurement output;
- **inferred:** a supported interpretation with stated uncertainty;
- **adjudicated:** a semantic judgment made under a named rubric;
- **unknown:** unavailable or ambiguous, never silently treated as zero;
- **not applicable:** structurally irrelevant to this run.

Cite trace event IDs, artifact paths, or deterministic metric IDs. Keep these claims distinct:

1. a tool returned content;
2. content was assembled into model context;
3. the agent explicitly referenced or used content;
4. the content was causally useful.

Evidence for an earlier stage does not prove a later stage. When task-specific rubrics, invariants, or hidden acceptance are needed, obtain them from the evaluated repository rather than inventing generic substitutes.

## Review Through Efficiency Lenses

Use only lenses supported by the mode and telemetry:

- initial static context and premature reference loading;
- search breadth, truncation, and time or actions to first relevant evidence;
- result size, concentration, filterability, and context actually exposed to the model;
- repeated exposure, separating necessary verification or changed state from avoidable rereads;
- evidence coverage for protected task invariants;
- patch locality or action-sequence accuracy;
- latency, wrong turns, retries, and rework;
- continuation completeness before continuation compactness: state, evidence, blockers, risk, and exact next action;
- total-system cost shifted to subagents, caches, retrieval indexes, preprocessing, or human summaries;
- privacy and unnecessary exposure of sensitive context.

Do not equate less reading with better navigation or a shorter handoff with better continuation.

## Reject Gaming and Invalid Comparisons

Treat correctness failure, safety or provenance failure, hidden I/O, and benchmark leakage as vetoes, not small deductions. Look for:

- guessing instead of acquiring required evidence;
- comparing only successful survivors;
- memorized fixtures or leaked hidden acceptance;
- uncounted delegation, cache construction, retrieval indexes, preprocessing, or human summaries;
- untraced shell, subprocess, filesystem, or network access;
- passing visible checks while violating task semantics;
- acting before required authorization to save a turn;
- shortening continuation by omitting state, evidence, blockers, risk, or next action;
- tracing or decision-record prompts changing the behavior being measured.

A plausible waste pattern supports a candidate optimization and controlled test. It does not establish that the optimization works.

## Use the Deterministic Runtime

When traces or comparisons need machine-checkable boundaries, use `scripts/context_eval.py` for versioned contract validation, provider-neutral JSONL normalization, content-addressed tree snapshots, immutable evaluation workspaces, and gate-first matched-pair arithmetic. Keep semantic acceptance, safety, relevance, evidence sufficiency, causal usefulness, and hidden oracle material outside the subject workspace in named rubrics and adjudication; the runtime intentionally does not infer them or emit a winner or score. Workspace paths and ignore rules organize evidence but do not isolate the subject from evaluator or oracle data.

For in-project evidence, initialize a workspace and explicitly exclude it from project snapshots:

```text
python3 scripts/context_eval.py init evaluation-id
python3 scripts/context_eval.py snapshot . --exclude .context-evaluation --workspace WORKSPACE --artifact-slug baseline --label before
```

`init` warns on stderr because `.context-evaluation` is not auto-ignored; its canonical JSON stdout remains machine-readable and it never edits ignore files. Add `/.context-evaluation/` to `.gitignore` yourself when appropriate, and always pass `--exclude .context-evaluation` when snapshotting a root that contains the workspace. Snapshots are stored per artifact slug, so baseline and treatment may safely use the same label. Do not put oracle or hidden acceptance material in the evaluated project.

Read `references/runtime-contract.md` before producing or consuming `ctxeval.input.v1`, `ctxeval.event.v1`, `ctxeval.tree.v1`, or `ctxeval.report.v1` artifacts.

## Report for Continuation

Use the smallest useful form, preserving ambiguity and next action:

```text
Context-Efficiency Evaluation
- Mode:
- Telemetry/evidence coverage:
- Correctness eligibility:
- Safety eligibility:
- Findings: [status] finding — event/artifact/metric references
- Available metrics:
- Unknown, unavailable, or ambiguous metrics:
- Matched differences: [eligible matched comparisons only]
- Validity and gaming risks:
- Conclusion strength:
- Candidate optimization or experiment:
- Exact next evidence/action:
```

Keep the conclusion provisional when telemetry, correctness, safety, provenance, matching, or uncertainty is insufficient.

## References

Load only what can change the evaluation:

- `references/runtime-contract.md`: deterministic validation, normalization, snapshots, versioned artifacts, exit codes, gate eligibility, or compatible native metric comparison.
- `references/evidence-model.md`: telemetry sufficiency, subject/evaluator separation, exposure stages, provenance, payload integrity, or usage-field interpretation.
- `references/annotation-guide.md`: disputed relevance, exploration breadth, rereads, wrong turns, rework, continuation quality, or rater disagreement; semantic adjudication stays outside the runtime.
- `references/experiment-design.md`: matched comparison validity, experiment-design mode, uncertainty, instrumentation effects, or rollout-facing conclusions; declare pairs and estimands before runtime evaluation.

## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
