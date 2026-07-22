---
name: adaptive-formalization
description: Use when designing or changing AI/Agent-native product entities, schemas, database models, JSON schemas, DTOs, events, workspace artifacts, memories, profiles, plans, evaluations, or agent outputs; guides Codex to choose the right degree of formalization and freedom instead of defaulting to either rigid schema or unbounded text.
metadata:
  short-description: Choose the right formalization level for AI-native entities
---

# Adaptive Formalization

Use this skill to guide representation design in AI/Agent-native software systems. The goal is not to avoid schemas. The goal is to choose the degree of formalization that fits the entity's current product role, evidence maturity, consumer needs, and risk.

Core principle:

> Choose the right degree of formalization for the entity's current product role. Preserve Agent semantic freedom where it creates product value, and add structure where system boundaries, consumers, validation, or auditability require it.

Reach for this skill when creating or materially changing durable representations: DB tables, ORM models, API DTOs, JSON schemas, events, config schemas, state machines, Agent memories, plans, profiles, evaluations, workspace artifacts, or outputs that may become UI state or workflow input. Do not use it for routine internal refactors where no representation boundary changes.

## Formalization Gradient

Treat schema objects and Agent artifacts as points on a gradient, not as opposing categories:

| Level | Name | Use When |
|---|---|---|
| F0 | Raw semantic note | The entity is exploratory, local, temporary, or mainly for Agent thinking. |
| F1 | Guided semantic artifact | The entity needs light metadata, evidence links, uncertainty, or lifecycle hints while preserving natural language body. |
| F2 | Semi-structured projection | The entity is consumed by a UI, workflow, or another Agent, but semantics are still evolving. |
| F3 | Contracted schema object | The entity has stable consumers, repeatable fields, tests, versioning, and migration expectations. |
| F4 | Audited platform truth | The entity affects authorization, submission, delivery, formal evaluation, billing, compliance, or irreversible user-visible state. |

Prefer the lowest level that satisfies current product boundaries. Raise the level when risk, consumers, or evidence justify it. Lower the level when a schema compresses meaning, hides uncertainty, or narrows the Agent capability prematurely.

## Formalization Lenses

Use these lenses to choose the lowest level that satisfies the real boundary:

- **Product role:** Agent thinking, user-facing projection, workflow coordination, cross-service contract, or platform truth.
- **Consumers:** Agent only, UI, API, scheduler, evaluator, human reviewer, or external system.
- **Evidence maturity:** real scenarios, traces, outputs, source refs, repeated product behavior, or only mock examples.
- **Truth status:** candidate interpretation, reviewable projection, durable contract, or audited source of truth.
- **Mutation freedom:** freely rewritable, append-only, review-gated, versioned, or audited.
- **Semantic risk:** whether fields collapse uncertainty, disagreement, source evidence, or interpretive judgment.
- **Evolution path:** promotion criteria, demotion triggers, migration cost, and validation loop.

If uncertain, choose a higher-freedom representation with explicit promotion criteria.

## Representation Decision

When this skill triggers, include a concise decision record before implementing representation changes:

```text
Representation Decision
- Entity:
- Product role:
- Current maturity:
- Primary consumers:
- Truth status:
- Recommended freedom level:
- Recommended representation:
- Required evidence:
- Allowed mutations:
- Promotion path:
- Demotion trigger:
- Validation loop:
```

Keep the decision short. It should guide implementation, not become a design essay.

## Default Biases

- Agent reasoning, observations, hypotheses, drafts, reflections, and candidate profiles usually start as F1 guided semantic artifacts.
- UI previews and read models usually fit F2 until field stability is proven by repeated real scenarios.
- Durable APIs, shared event contracts, and persisted workflow state usually require F3.
- Authorization, formal submissions, evaluation decisions, delivery records, and audit logs require F4.
- If a field represents uncertainty, disagreement, weak evidence, or interpretive judgment, preserve `sourceRefs`, confidence, unresolved questions, or review status instead of collapsing it to a bare enum or boolean.

## References

Load references only when they change the decision:

- `references/decision-rubric.md`: use when the F0-F4 level is not obvious.
- `references/optimization-controls.md`: use when a schema choice is contested or Codex is formalizing mainly because implementation would be easier.
- `references/capability-evidence-pack.md`: use when an Agent-facing representation needs evidence that it improves a real capability loop.

## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
