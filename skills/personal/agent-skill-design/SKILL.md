---
name: agent-skill-design
description: Use when creating, extracting, naming, rewriting, diagnosing, splitting, or polishing an agent skill, especially when aligning metadata, SKILL.md, references, scripts, assets, CLI output, and soft-boundary judgment around a clear behavior-changing principle.
metadata:
  short-description: Design agent skills as behavioral interfaces
---

# Agent Skill Design

Use this skill to design agent skills as progressive behavioral interfaces. The goal is to turn repeated judgment, workflow, taste, or tool use into a skill that loads at the right time and changes agent behavior at the moment it matters.

Core thesis:

> A skill is a progressive behavioral interface for agents: metadata controls invocation, the body carries judgment, references manage context depth, scripts provide deterministic substrate, and outputs preserve continuation context.

## Design Axioms

- **Invocation contract:** `name` and `description` decide whether the skill is read at all. Put trigger conditions in metadata where they can influence loading.

- **Behavioral kernel:** the body should teach the agent what to judge, what to preserve, what to tighten, and how to act differently. Topic explanation usually belongs in reference material.

- **Boundary design:** add fixed contracts where reliability matters. Preserve flexible judgment where the work is interpretive, immature, or taste-dependent.

- **Context economy:** `SKILL.md` should contain what every invocation needs. `references/` should hold optional depth. `scripts/` should handle deterministic or fragile work. `assets/` should contain output materials.

- **Continuation surface:** agent-facing scripts and CLIs should report the result and preserve enough state, ambiguity, paths, and next actions for the next agent step.

- **Principle-first iteration:** fold new feedback into cleaner concepts, sharper vocabulary, better medium split, or a stronger structure before adding local prohibitions.

- **Fit boundary:** real cases are evidence. Let a case generalize the skill, narrow the skill, move into references, or remain local according to the fit boundary it reveals.

## Skill Shape Lenses

A skill's shape should emerge from the behavior it is meant to improve: the judgment it carries, the boundary it sets, the context it loads, and the deterministic work it delegates.

Use these lenses while designing or revising:

- **Behavior center:** What agent behavior should become more stable, sharper, or more aligned with the user's taste?
- **Boundary hardness:** Which parts need a fixed contract, and which parts should preserve semantic freedom?
- **Fit boundary:** Should the case evidence generalize the skill, narrow its scope, become an example, or remain local?
- **Context timing:** Which information should be visible in metadata, loaded in `SKILL.md`, or deferred to references?
- **Deterministic substrate:** Which repeated, fragile, or side-effecting work belongs in scripts or CLIs?
- **Continuation surface:** Which outputs need to guide the next agent step?
- **Validation surface:** What realistic prompt would show that the skill changed behavior?

## Diagnostic Vocabulary

Use diagnostic terms to explain concrete structural issues:

- **Invocation burial:** trigger conditions live in the body instead of `description`.
- **Description shortcut:** metadata summarizes the workflow so strongly that an agent may act from metadata alone instead of reading the body.
- **Topic wrapper:** the skill names a domain but not the situations that should trigger it.
- **Behavior gap:** the skill contains useful information but does not change what the agent will do.
- **Workflow cosplay:** a judgment or taste skill is forced into generic steps.
- **Context sediment:** `SKILL.md` accumulates optional examples, background, or long explanation that should be in references.
- **Patch sediment:** iteration adds local prohibitions, exceptions, and "don't do X" clauses instead of absorbing feedback into clearer principles or structure.
- **Case overfit:** a general skill absorbs local names, examples, exceptions, or scenario details as if they were durable principles.
- **Determinism overreach:** flexible semantic work is prematurely forced into a schema, enum, script, or rigid process.
- **Softness leak:** a flexible boundary is preserved, but no lenses or constraints help the agent handle it responsibly.
- **Execution prose:** fragile repeatable work is described in text instead of captured in a script or CLI.
- **Dead output:** a helper produces a result but gives no completeness signal, ambiguity note, artifact path, or next action.

## Medium Split

Use this default medium split:

- `name`: short searchable action or judgment, matching the directory.
- `description`: concrete invocation contract; include all durable trigger conditions here.
- `SKILL.md`: core theory, decision lenses, failure vocabulary, resource map, output shape.
- `references/`: optional theory, long examples, source docs, detailed rubrics, provider-specific notes.
- `scripts/`: deterministic heavy work, fragile file operations, validation, linking, generation.
- `assets/`: templates or media used in outputs, not explanatory material.

## Rewrite Moves

When improving a skill, prefer structural moves over wording polish:

- Move trigger language from body to `description`.
- Replace topic summaries with a behavioral kernel.
- Let the skill's shape follow the behavior, boundary, context timing, and deterministic substrate it needs.
- Classify case feedback as general principle, scope narrowing, reference example, validation prompt, or local context.
- Turn generic steps into lenses, contracts, or deterministic scripts.
- Move optional depth into `references/` and state when to read it.
- Add a script when correctness depends on repeated file, CLI, parsing, or validation work.
- Make helper output agent-friendly: result, completeness, ambiguity, artifact paths, and next action.
- Split a skill when two trigger surfaces need different behavior.
- Remove content that a capable model already knows.
- Convert patch sediment into a stronger positive principle, diagnostic term, or structural rewrite.

For bloated skills, identify which material belongs in a different medium.

## Naming Taste

Name the skill after the durable behavior, judgment, or design surface it improves.

Prefer names that expose one of these:

- **Action:** what the agent is doing repeatedly.
- **Judgment:** what decision the skill makes sharper.
- **Artifact:** what object the skill shapes.
- **Failure mode:** what recurring drift the skill corrects.
- **Medium:** what tool or interface the skill operates through, when that is the real trigger.

A good name should help the metadata trigger correctly before the body is loaded.

## Output When Helping

When helping design or diagnose a skill, keep the response compact:

```text
Agent Skill Design Notes
- Invocation contract:
- Behavioral kernel:
- Shape lenses:
- Fit boundary:
- Medium split:
- Soft boundary:
- Main smell:
- Rename or split:
- Validation prompt:
```

Use the full shape only when useful. For small edits, a direct rewrite plus one or two notes is better.

## References

Load `references/personal-theory.md` when doing a broad redesign, choosing between competing skill names, explaining the theory behind a recommendation, or turning a user's raw taste and experience into a reusable skill design system.

## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
