# Capability Evidence Pack

Use this pack to verify that a representation decision supports a real Agent capability, not only a clean data flow.

## Minimal Template

```text
Capability Evidence Pack
- Target scenario:
- Realistic input:
- Agent action:
- Output:
- Evidence/source refs:
- User value:
- Uncertainty or failure notes:
- Representation decision:
- Validation result:
```

## What Counts As Evidence

Good evidence includes:

- real or realistic transcripts, documents, artifacts, tasks, or user inputs;
- before/after outputs from an Agent run;
- source references that support the Agent's conclusion;
- reviewer notes explaining whether the result helped the target workflow;
- screenshots or CLI/test logs when UI, API, or deployment behavior matters.

Weak evidence includes:

- mock-only tests with no realistic input;
- scripts that only prove serialization or dispatch;
- schema validation without scenario validation;
- hand-written ideal examples that were never processed by the Agent.

## Acceptance Questions

Before calling the feature complete, answer:

- Did the Agent capability improve in the target scenario?
- Can the result be traced to source material or run evidence?
- Is uncertainty preserved where the system should not claim truth?
- Are consumers using an appropriate representation level?
- If the current representation is wrong, is there a clear promotion, demotion, or migration path?
