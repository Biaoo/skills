# Experiment Design

After declaring estimands and matched pairs, use the versioned boundaries and immutable workspace slots in `runtime-contract.md` for deterministic qualification and compatible native metric arithmetic. Keep oracle and hidden acceptance material outside the evaluated project: an in-project workspace or ignore rule does not isolate it from the subject.

Load this reference for experiment-design mode, disputed matched-comparison validity, instrumentation effects, uncertainty analysis, or conclusions intended to support rollout.

## Define the Estimand Before Metrics

State the causal question and unit of comparison. Examples include the effect of a context router on quality-qualified model input, or the effect of structured continuation on time to first relevant evidence.

A run should bind one versioned task instance to one assigned condition under a declared model, runtime, tool policy, initial state, and acceptance contract. Repeated stochastic attempts on the same fixture are nested observations, not independent task instances.

Pre-register:

- primary and secondary estimands;
- correctness acceptance and verification;
- safety vetoes and authorization boundaries;
- telemetry capabilities and total-system cost boundary;
- matching variables and exclusion rules;
- timeout, refusal, permission-denial, and infrastructure-failure handling;
- non-inferiority margins and resource decision thresholds;
- stopping rules and uncertainty method.

Keep evaluator manifests, hidden acceptance, expected paths, and solution annotations outside the subject agent's visible context.

## Build Comparable Conditions

Prefer paired assignment of each fixture across baseline and treatment when carryover can be prevented. Freeze or record model, runtime, tools, workspace state, dependencies, and policy. Use fresh sessions unless session history is the factor under study.

Randomize or counterbalance condition order to reduce temporal, learning, and infrastructure effects. Separate cold-cache and warm-cache studies; disclose whether cache construction and maintenance are counted. Do not let treatment-specific preprocessing disappear from the resource boundary.

When static routing and runtime continuation may contribute independently, a 2×2 design can separate main and interaction effects:

| Condition | Static context routing | Runtime continuation |
|---|---|---|
| S0-R0 | baseline | baseline |
| S1-R0 | treatment | baseline |
| S0-R1 | baseline | treatment |
| S1-R1 | treatment | treatment |

Use this only when both factors are real interventions and the study has enough fixtures and repetitions to interpret the interaction. A simpler paired study is preferable when one factor is the actual question.

## Protect Quality and Safety

Judge unconditional outcomes first: success, task failure, safety violation, refusal, timeout, permission denial, and infrastructure failure, with attributable resource cost. Then form a conditional resource comparison only among runs that meet pre-registered correctness and safety eligibility.

A treatment with lower resource use but worse acceptance or a safety veto is not more context-efficient. Non-inferiority requires a declared margin justified by the task's consequence and measurement resolution; absence of statistical significance is not proof of non-inferiority.

Use hidden acceptance where visible tests can be gamed. Include held-out task families to detect fixture memorization and report external-validity limits.

## Treat Instrumentation as an Intervention

Tracing can alter latency, tool behavior, prompting, deliberation, or the agent's willingness to record decisions. Before trusting trace-derived effects, compare traced and untraced behavior or run a suitable ablation, such as:

- tracing on versus off;
- structural event logging versus content logging;
- normal execution versus decision-record prompting.

The untraced condition still needs independent outcome and safety observation. If instrumentation effects cannot be bounded, limit the conclusion to behavior under the traced condition.

## Analyze at the Fixture Level

Prefer fixture-level paired differences and show the distribution, not only a pooled total. Report task-family results when families differ materially. Repeated attempts within a fixture require cluster-aware uncertainty or fixture-level aggregation.

For each metric, state:

- unit, scope, and provenance;
- whether it is observed, estimated, or adjudicated;
- paired sample count and missingness;
- center and spread or interval;
- sensitivity to failed-run handling, outliers, and matching choices.

Do not invent values for missing model-context inclusion, cache semantics, subagent cost, or payload size. Use bounds or mark the metric unavailable.

## Use Decision Gates, Not Universal Thresholds

A deployment policy can combine gates such as:

```text
Correctness qualifies
AND safety qualifies
AND quality is non-inferior within the registered margin
AND a registered resource or navigation target is met
```

Any numerical margin or reduction threshold is a local, pre-registered policy calibrated to the task family, instrumentation, and cost of error. It is not a universal scientific constant.

Conclude with the exact next evidence required: more fixtures, a held-out family, stronger provenance, an instrumentation ablation, a narrower intervention, or a replicated paired study. A single audit finding is a hypothesis source, not rollout evidence.
