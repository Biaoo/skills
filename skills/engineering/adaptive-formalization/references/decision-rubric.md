# Decision Rubric

Use this rubric when the representation level is not obvious.

## Freedom Dimensions

Score each dimension qualitatively as high, medium, or low freedom:

| Dimension | High Freedom | Low Freedom |
|---|---|---|
| Structure freedom | Markdown, notes, loose blocks | strict schema, DB constraints |
| Semantic freedom | hypotheses, conflicts, nuance | normalized states, enums, scores |
| Mutation freedom | Agent can rewrite freely | append-only, review-gated, audited |
| Truth freedom | exploratory or candidate | committed platform fact |
| Consumer freedom | Agent-local | stable API/UI/external consumers |
| Validation freedom | scenario review, lint | schema validation, migrations, constraints |
| Lifecycle freedom | temporary / evolving | versioned, retained, rollback-aware |

The recommended level should match the strictest real boundary, not the strictest imagined future.

## Level Selection Signals

### F0 - Raw semantic note

Use when the entity is:

- temporary, local, exploratory, or discarded after a run;
- not consumed by UI/API/workflows;
- useful mainly because it preserves rich context.

Avoid F0 when the entity is reused across sessions or affects user-visible behavior.

### F1 - Guided semantic artifact

Use when the entity:

- helps an Agent remember, reason, plan, summarize, or reflect;
- contains uncertainty, hypotheses, open questions, or conflicting evidence;
- needs minimal metadata such as purpose, scope, source refs, owner, or timestamp.

Typical shape: frontmatter or small JSON header plus Markdown body.

### F2 - Semi-structured projection

Use when the entity:

- is shown in UI, passed to another Agent, or used by a workflow;
- has some recurring fields, but product semantics are still evolving;
- should be regenerable or correctable from richer evidence.

Typical shape: JSON object with flexible sections, `sourceRefs`, confidence, and `notes`.

### F3 - Contracted schema object

Use when the entity:

- has stable fields across repeated real scenarios;
- has stable consumers and compatibility expectations;
- needs validation, migrations, contract tests, or API compatibility.

Do not use F3 solely because it makes tests or CRUD implementation easier.

### F4 - Audited platform truth

Use when the entity:

- affects authorization, formal submissions, evaluations, delivery, billing, compliance, or irreversible user-visible state;
- must be audit logged, retained, permissioned, or reviewable;
- is the source of truth for other systems.

F4 should preserve provenance. Even hard truth often needs `sourceRefs`, actor, timestamp, revision, and decision boundary.

## Promotion Criteria

Promote to a stricter level when several of these are true:

- repeated real scenarios produce the same stable fields;
- downstream consumers require compatibility;
- manual review confirms the semantics are stable;
- operational risk increases;
- audit, permission, or external integration requires it;
- the structure improves capability without compressing important meaning.

## Demotion Triggers

Demote or loosen representation when:

- schema fields force unsupported certainty;
- Agent outputs become narrower or less useful;
- explanations, evidence, conflicts, or alternatives are lost;
- tests pass but real scenario capability does not improve;
- product behavior changes faster than migrations can keep up;
- most fields become optional, overloaded, or filled with placeholder values.
