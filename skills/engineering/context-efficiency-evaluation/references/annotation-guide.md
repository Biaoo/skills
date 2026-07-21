# Annotation Guide

Load this reference when semantic adjudication is needed for context relevance, exploration breadth, rereads, wrong turns, rework, or continuation quality.

## Anchor the Rubric to the Task

Start from versioned task acceptance, safety boundaries, protected invariants, and allowed evidence paths. Keep domain-specific rubrics and hidden fixtures in the evaluated repository.

Do not require one canonical navigation path. Several evidence paths may support the same invariant, and exploratory work can be reasonable before the relevant location is known. Annotate the smallest defensible unit—an event, payload segment, action, or continuation field—and cite it.

## Classify Context

Use these labels only where the trace exposes enough content:

- **Relevant:** supports a task invariant, safe action, verification, recovery, or required continuation.
- **Distractor:** exposed context has no plausible task contribution under the stated rubric.
- **Unknown:** content is unavailable, redacted, truncated, ambiguous, or requires unsupported causal judgment.
- **Not applicable:** the classification does not apply to this event or payload.

Relevance does not prove necessity. A relevant item can still be overly broad, and an apparently irrelevant item can be part of reasonable hypothesis testing. Record the rationale and confidence rather than collapsing both judgments into one label.

## Judge Breadth Relative to Information Available

Broad retrieval is **reasonable exploration** when it follows a plausible hypothesis, the repository or tool offers no narrower discovery surface, and the agent narrows after receiving discriminating evidence.

It is an **avoidable breadth candidate** when a narrower known filter, index, symbol lookup, pagination boundary, or targeted path would likely have supplied the required evidence with less exposure and no loss of coverage. This remains inferred or adjudicated until a matched test establishes the alternative.

Record truncation and concentration. A large result containing one useful segment is different from a large result whose sections are broadly relevant. Do not count unseen truncated content as exposed.

## Classify Repeated Exposure

For repeated reads or tool results, distinguish:

- **state-change reread:** the source may have changed since prior observation;
- **verification reread:** rechecking exact content is justified by consequence or fragile state;
- **navigation reread:** revisiting context to locate or reconnect evidence;
- **recovery reread:** needed after interruption, compaction, handoff, or failed state transfer;
- **unchanged avoidable reread:** substantially identical content is exposed again without new state, verification need, or information gain;
- **unknown:** identity, timing, or purpose is insufficient to classify.

Exact payload hashes can identify duplicate candidates but cannot decide whether repetition was necessary. Similarity measures must state their unit and threshold.

## Identify Wrong Turns and Rework

A wrong turn is not merely an unsuccessful action. Adjudicate it when the action followed a weakly supported hypothesis, ignored available discriminating evidence, or expanded scope without expected information value.

Rework is repeated effort caused by an earlier avoidable omission, incorrect assumption, unsafe action, poor handoff, or failure to preserve state. Separate it from normal iteration driven by new evidence or changed requirements.

For each finding record:

```text
Annotation
- Label and epistemic status:
- Event or artifact references:
- Task invariant or hypothesis:
- Evidence available at the time:
- Why reasonable, avoidable, or indeterminate:
- Counterinterpretation:
- Confidence or disagreement:
```

## Evaluate Continuation for Completeness First

A continuation surface is adequate when the next actor can resume without reconstructing material state. Depending on the task, inspect whether it preserves:

- current result, scope, and exact subject version;
- evidence obtained and verification already performed;
- unresolved ambiguity, blockers, safety concerns, and failed attempts;
- artifacts created or changed and where to inspect them;
- actions still unauthorized or incomplete;
- the exact next evidence, command, or decision.

Compactness is beneficial only after these needs are met. Mark a short handoff that omits material state as a continuation failure even if it saves tokens. Mark unavailable requirements as unknown rather than assuming every task needs every field.

## Preserve Disagreement

Use at least two independent ratings when conclusions depend heavily on relevance, necessity, wrong-turn, or continuation judgments and the decision is consequential. Calibrate with examples from the evaluated task family, not examples embedded in this generic skill.

Report agreement at the unit being annotated and preserve material dissent. If raters apply different task assumptions, resolve the rubric or mark the outcome indeterminate; averaging incompatible judgments does not create evidence.
