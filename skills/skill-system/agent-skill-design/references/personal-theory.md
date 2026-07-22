# Personal Theory Of Agent Skill Design

This reference captures the owner's current theory of skill design. Load it when the task needs the theory behind a redesign, not for every small skill edit.

## Root Thesis

A skill is a progressive behavioral interface for agents.

It combines invocation metadata, behavior-shaping guidance, optional reference depth, deterministic tools, and continuation-aware outputs. It controls when an agent receives judgment, how much context it receives, when it should use deterministic tools, and how outputs should guide the next agent step.

The purpose of a skill is to make agent behavior more reliable while preserving the flexible semantic judgment that makes agents useful.

## Core Model

### Invocation Contract

The most important skill content is the metadata, especially `name` and `description`.

Because skills use progressive disclosure, the agent sees metadata before it sees the body. Metadata earns the skill a chance to load; the body refines behavior after loading. A long "When To Use" section in `SKILL.md` is usually misplaced trigger design.

Good metadata describes concrete situations, symptoms, artifacts, and decisions more precisely than a broad topic label.

### Behavioral Kernel

The body of a skill should contain the behavior-changing kernel:

- the judgment the agent should make;
- the failure modes it should recognize;
- the degree of freedom it should preserve or remove;
- the output shape that helps the task finish;
- the resource map for optional depth.

General articles about the domain usually belong in references.

### Skill Shape

A skill's shape should emerge from the behavior it is meant to improve. Use lenses as the primary shape drivers:

- **Behavior center:** the agent behavior that should become more stable, sharper, or more aligned with personal taste.
- **Boundary hardness:** the parts that need fixed contracts and the parts that should preserve semantic freedom.
- **Fit boundary:** whether case evidence should generalize the skill, narrow its scope, become an example, or stay local.
- **Context timing:** what belongs in metadata, `SKILL.md`, references, scripts, assets, or CLI output.
- **Deterministic substrate:** repeated, fragile, or side-effecting work that belongs in scripts or CLIs.
- **Continuation surface:** outputs that must preserve enough state for the next agent step.
- **Validation surface:** realistic prompts that show whether the skill changed behavior.

This still allows recognizable forms. Repeated processes may need ordered checks. Judgment-heavy skills may need lenses and gradients. Taste-heavy skills may need principles, vocabulary, and examples. Tool-assisted skills may need scripts and CLI help. These forms are design consequences.

### Soft Boundary

Traditional software engineering often prefers fixed schemas, scripts, APIs, and state machines. Agent work often operates on softer boundaries: partial meaning, evolving concepts, uncertain evidence, personal taste, design intent, or semi-structured artifacts.

Skill design chooses the right degree of formalization for each boundary.

Hard boundaries are useful when correctness, safety, repeatability, parsing, or external side effects matter. Soft boundaries are useful when the work requires interpretation, taste, exploration, or evolving semantics.

### Principle-First Iteration

Skill iteration should clarify the governing principle.

When new feedback arrives, first look for the higher-level concept it reveals. Fold it into a clearer axiom, sharper vocabulary, better medium split, or structural rewrite. Local prohibitions and exception clauses are useful only when a concrete failure mode needs to stay visible as a diagnostic term.

A mature skill becomes simpler as it absorbs feedback. It gains stronger concepts and fewer warnings.

### Fit Boundary

Real cases are evidence first.

Skill iteration should decide what kind of evidence a case provides:

| Case signal | Design response |
|---|---|
| Repeated structural issue | Generalize into an axiom, lens, diagnostic term, or medium split. |
| Scope-specific stability need | Narrow the skill's invocation contract or keep the guidance in a personal/local skill. |
| Helpful illustration | Move the example to references or keep it short in `SKILL.md` only when it changes behavior every time. |
| Validation pressure | Turn the case into a test prompt or review scenario. |
| One-off local detail | Preserve it outside the skill. |

Local fit can be correct. A skill designed for a private workflow, specific tool, or fragile process may intentionally fit that context closely. General skills need a stronger fit boundary: case details should become principles only when they represent a repeatable structure.

### Context Economy

Designing a skill is designing when information is read.

- `metadata` is always visible and must control invocation.
- `SKILL.md` is loaded after invocation and must earn its token cost.
- `references/` holds material that is useful only in some cases.
- `scripts/` holds deterministic operations that are better executed reliably.
- `assets/` holds output materials.

The central question is: "When should this information be loaded?"

### Continuation Surface

Agent-facing CLI and script output is context for the next agent step.

Good output should say what happened, whether the result is complete, what was ambiguous, where artifacts were written, and what the likely next action is. A script used by an agent should provide continuation context.

### Deterministic Substrate

If skill execution involves heavy, fragile, repeated, or side-effecting operations, prefer a CLI or script.

Scripts are appropriate for:

- linking or copying skill directories;
- validating skill metadata;
- generating repeated files;
- parsing structured artifacts;
- formatting or transforming files;
- operations that need dry-run, force, or safety checks.

Keep judgment in the skill. Put deterministic work in deterministic media.

## Diagnostic Terms

- **Invocation burial:** trigger logic hidden in the body.
- **Description shortcut:** metadata contains enough workflow detail that the agent may skip reading the body.
- **Topic wrapper:** a skill organized around a broad domain instead of a concrete agent situation.
- **Behavior gap:** useful information that does not change agent behavior.
- **Workflow cosplay:** a non-procedural skill forced into a generic sequence.
- **Context sediment:** optional material that accumulated in `SKILL.md`.
- **Patch sediment:** local prohibitions, exceptions, and "don't do X" clauses added during iteration without being absorbed into clearer principles or structure.
- **Case overfit:** local examples, names, exceptions, or scenario details absorbed into a general skill as if they were durable principles.
- **Determinism overreach:** premature hardening of a soft semantic boundary.
- **Softness leak:** flexibility preserved without any judgment lenses or constraints.
- **Execution prose:** fragile repeatable work described in prose instead of automated.
- **Dead output:** CLI or script output that gives a result but no continuation context.

## Practical Test

A skill is probably worth keeping when it passes these questions:

1. Would the metadata cause the skill to load in the right real tasks?
2. Does the body make the agent behave differently?
3. Is the skill using the right medium for each kind of information?
4. Does it preserve soft judgment where hard contracts would be premature?
5. Does it add deterministic tooling where prose would be unreliable?
6. Does iteration absorb feedback into clearer principles instead of accumulating patch sediment?
7. Does case feedback have an explicit fit boundary?
8. Can a realistic prompt expose whether the skill works?
