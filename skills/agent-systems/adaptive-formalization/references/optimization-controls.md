# Optimization Controls

Use this framing when a design choice is contested or when Codex is tempted to make a schema because it is easier to implement.

## Objective

Choose the representation level that maximizes real product capability while preserving enough control for the current boundary:

```text
maximize:
  capability_value
  + evidence_traceability
  + user_outcome_quality
  + interoperability
  + auditability_when_needed
  + evolvability

minimize:
  premature_formalization_loss
  + semantic_compression_loss
  + ambiguity_risk
  + schema_debt
  + local_convergence_risk
  + operational_risk
```

Do not collapse this into one numeric score unless the project already has calibrated metrics. Use it as a review checklist.

## Loss Signals

### Premature formalization loss

High when uncertainty is high, real scenario evidence is weak, but the proposed representation is F3/F4.

Ask: "What evidence proves these fields are stable product concepts rather than first-pass implementation guesses?"

### Semantic compression loss

High when natural language reasoning, source context, conflict, uncertainty, or alternatives are collapsed into a narrow enum, boolean, or score.

Ask: "Could a reviewer reconstruct why the Agent made this judgment?"

### Ambiguity risk

High when many consumers depend on high-freedom text with no validation, ownership, source refs, or mutation rules.

Ask: "Could two consumers interpret this artifact differently in a way that breaks product behavior?"

### Local convergence risk

High when implementation has green tests but no realistic Agent capability loop, live-like input, or evidence pack.

Ask: "Are we optimizing the data path, or the user-visible capability?"

### Schema debt

High when a schema is likely to migrate often, has many optional fields, uses vague names, or encodes current UI shape as durable truth.

Ask: "If this abstraction is wrong, how expensive is correction?"

## Tuning Mechanisms

- Raise formalization when authorization, audit, external integration, stable UI/API consumption, or operational safety requires it.
- Lower formalization when product semantics are still exploratory or the Agent needs broad context to produce useful output.
- Add provenance before adding rigidity when the problem is trust rather than structure.
- Add lifecycle rules before adding fields when the problem is mutation or ownership.
- Prefer projections over truth records when UI needs display but the underlying interpretation is still evolving.
- Require capability evidence before durable schema for Agent-native behavior.
