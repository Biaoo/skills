---
name: skill-crafting
description: Use when creating, rewriting, extracting, diagnosing, or polishing an agent skill; helps Codex judge whether an idea should become a skill, shape SKILL.md around durable principles, identify skill smells, and preserve context economy through progressive disclosure.
metadata:
  short-description: Craft high-quality agent skills
---

# Skill Crafting

Use this skill as a taste guide for writing and improving agent skills. It is not a checklist. It is a set of judgment principles for turning repeated expertise, documents, prompts, or workflows into a skill that reliably changes agent behavior.

## Golden Principles

A skill is not a knowledge dump. A skill is a behavior shaper.

The test for a skill is not "does this contain useful information?" The test is "will this make the agent act differently and better at the moment it matters?"

Frontmatter earns the skill a chance to load. The body must justify the context it consumes.

Put stable triggering language in `description`. Put behavioral judgment in `SKILL.md`. Put details that are only sometimes needed in `references/`. Put deterministic fragile work in `scripts/`. Put output materials in `assets/`.

Prefer a small skill with sharp judgment over a broad skill with exhaustive advice.

## What A Skill Is For

A good skill helps with at least one of these:

- Teaches an agent a domain-specific way to judge a situation.
- Provides a workflow the model would otherwise execute unreliably.
- Encodes local taste, policy, vocabulary, or constraints that are not obvious from general knowledge.
- Points to bundled resources at the exact moment they are useful.
- Prevents a common failure mode that normal prompting repeatedly misses.

If the material only restates generic best practices, it probably belongs in the conversation, not in a skill.

## Good Skill Signals

Good skills usually have:

- A narrow, vivid trigger.
- A clear behavioral center of gravity.
- Enough constraints to prevent common mistakes, without removing useful agent judgment.
- Strong verbs and concrete situations instead of abstract categories.
- A small number of durable principles that apply across many instances.
- Optional references that are discoverable without being loaded by default.
- A natural output shape when the skill should produce an artifact, decision, critique, or plan.

The best skills feel like a senior practitioner looking over the agent's shoulder at the few decisions that matter.

## Skill Smells

Trigger smells:

- The description names a topic but not the user situations that should trigger it.
- The skill competes with many adjacent skills because its boundary is too broad.
- The skill can be invoked for almost any work in a domain.

Body smells:

- The body explains the domain but does not change the agent's actions.
- The skill starts with a long "When To Use" section that repeats the frontmatter.
- The main structure is a generic workflow that could apply to any task.
- The text tells the agent to "consider" or "ensure" things without saying what changes in behavior.
- Examples are longer than the principles they support.

Resource smells:

- `SKILL.md` contains reference material that is only needed sometimes.
- `references/` is used as storage, but `SKILL.md` does not say when to load each file.
- Scripts are described in prose even though a deterministic helper would be safer.

Maintenance smells:

- The skill cannot be tested against a realistic prompt.
- A reader cannot tell whether the skill belongs in `personal` or `engineering`.
- The skill requires private context but is presented as generally reusable.
- The skill needs a README inside its own directory to explain why it exists.

## Rewrite Moves

When improving a skill, prefer these moves:

- Replace topic summaries with judgment principles.
- Replace generic workflows with decision lenses.
- Move rare details into `references/`.
- Collapse repeated advice into one sharp rule.
- Rename broad skills around the action they improve.
- Add one concrete output shape only when it helps the agent finish the task.
- Split a skill when two different situations need different triggers or different judgment.
- Delete content that a capable model already knows.

If a skill feels too long, do not summarize it first. Identify which parts should not be in the loaded body at all.

## Progressive Disclosure Taste

`SKILL.md` should contain what the agent needs every time the skill triggers:

- the core judgment;
- the failure modes to avoid;
- the resource map;
- the expected artifact or response shape, if any.

References should contain what the agent needs only for some cases:

- detailed rubrics;
- long examples;
- provider-specific instructions;
- domain background;
- templates that would crowd the main skill.

Scripts should contain work where correctness matters more than improvisation.

Assets should contain files used to produce the final output, not explanatory material.

## Naming And Triggering

Name the skill after the durable action or judgment it improves. A broad crafting skill should cover creating, rewriting, extracting, and diagnosing skills, not just reviewing finished ones.

The `description` should answer:

- What kind of task should trigger this?
- What artifact or decision is being shaped?
- What failure mode does the skill prevent?

The body should not depend on the user naming the skill perfectly. If the user asks to turn a document, repeated workflow, local rule, or prompt into a skill, this skill should help shape the result.

## Output When Helping

When helping craft or diagnose a skill, keep the response compact and practical:

```text
Skill Crafting Notes
- Core purpose:
- Main skill smell:
- Recommended shape:
- What to remove:
- What to move to references:
- Trigger rewrite:
- Validation idea:
```

Use the full shape only when useful. For small edits, a direct rewrite plus one or two notes is better.
