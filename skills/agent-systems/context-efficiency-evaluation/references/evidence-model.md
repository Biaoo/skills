# Evidence Model

For deterministic artifact fields, explicit missingness, normalization blobs, immutable workspaces, and native metric compatibility, also read `runtime-contract.md`. Workspace organization and ignore configuration are not evidence that the subject was isolated from evaluator or oracle data; hidden acceptance must remain outside the evaluated project.

Load this reference when the evaluation depends on telemetry sufficiency, payload lineage, provider usage fields, or the distinction between what a subject agent did and what the evaluator can observe.

## Separate the Runs

- **Subject run:** the agent-system execution being evaluated, including subagents, retrieval infrastructure, preprocessing, caches constructed for the task, and attributable human preparation.
- **Evaluator run:** the later process that normalizes measurements, inspects traces, applies rubrics, and writes findings.

Report their costs separately. Evaluator cost is part of evaluation overhead, not evidence that the subject run consumed more context. Conversely, work delegated by the subject is not evaluator overhead and must not disappear from total-system accounting.

## Declare Trace Capability

Before judging efficiency, state whether the trace provides each capability and at what granularity:

- stable run, event, actor, parent, and attempt identity;
- timestamps or monotonic ordering;
- model requests and responses;
- system, user, assistant, and tool-message boundaries;
- tool arguments, result payloads, truncation, filters, and pagination;
- subagent, subprocess, filesystem, cache, retrieval, and network provenance;
- provider-native input, output, cache, and billing usage fields;
- artifact versions, workspace identity, and relevant environment state;
- authorization, verification, acceptance, failure, timeout, and retry outcomes;
- payload hashes, external payload references, redaction, and integrity status.

Use `observed`, `partially observed`, `not observed`, or `unknown` rather than assuming a uniform trace format. A missing capability limits the claim; it does not imply no cost or no event.

## Track Exposure Stages

Context can pass through several stages:

1. **Available:** existed in the workspace, store, cache, or retrieval corpus.
2. **Retrieved:** selected or returned by a tool or subsystem.
3. **Exposed:** assembled into a model request.
4. **Referenced:** explicitly cited, quoted, or relied on in the agent's visible reasoning or action.
5. **Useful:** adjudicated as contributing causally to a correct, safe outcome.

These stages are not interchangeable. Tool-result bytes may bound retrieved payload but not model exposure. Model input proves exposure but not attention or usefulness. A citation may show explicit use but not that the evidence was necessary. Causal usefulness usually remains adjudicated unless the experiment isolates it.

When exact inclusion is unavailable, report defensible lower and upper bounds and name the unobserved transition.

## Preserve Identity and Provenance

A matched claim requires enough identity to establish that baseline and treatment addressed the same versioned task under comparable state. Record or locate:

- task and fixture version;
- initial workspace or artifact identity;
- model, runtime, tool policy, and relevant configuration;
- condition assignment and attempt identity;
- external dependency versions when material;
- acceptance rubric and safety policy versions.

For large or sensitive payloads, traces may store a path, object reference, hash, size, media type, redaction status, and access boundary instead of inline content. A hash supports identity or integrity, not semantic relevance. Redaction protects data but may make later adjudication indeterminate; state that limitation.

## Keep Native Measurements Native

Retain provider-native usage fields with their original names, units, scope, and provenance. Do not merge cache reads, cache writes, billed tokens, model-visible tokens, bytes, characters, or estimated tokens into one supposedly universal count unless a validated conversion is declared.

For matched comparisons, use like-for-like measurements from the same instrumentation contract. If contracts differ, report them side by side or restrict the estimand. Estimated measurements must identify the estimator and uncertainty.

Useful deterministic metric IDs can cover properties such as event counts, payload bytes, elapsed durations, exact duplicate hashes, or declared overlap calculations. Semantic labels such as relevance, necessity, and wrong turn remain adjudications unless their rubric makes them mechanically testable.

## State What Tracing Cannot Prove

Even complete-looking traces may not establish:

- that no uninstrumented I/O occurred;
- that exposed content was attended to;
- that referenced content was necessary or causally useful;
- that an omitted action would have preserved correctness or safety;
- that tracing, logging, or decision-record prompts left behavior unchanged;
- that hidden acceptance was not leaked through another channel;
- that provider usage fields are comparable across models or runtimes.

Use instrumentation ablation, hidden acceptance, independent provenance checks, or controlled experiments when these limitations matter. Otherwise weaken the conclusion rather than filling gaps with inference.
