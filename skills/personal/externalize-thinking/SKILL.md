---
name: externalize-thinking
description: Use when the user wants to externalize a fuzzy intuition, unnamed judgment, unease about an AI response, or meta-cognitive question into candidate language, a cognitive map, validation probe, grounded principle, prompt, or reusable framework. Trigger when something feels missing or too smooth, the user cannot explain why a framing feels wrong, wants to analyze their thinking or AI collaboration, is overloaded by abstraction, needs to distinguish levels from dimensions, roles, states, or operations, or wants an abstract principle to change concrete action. Do not use for ordinary brainstorming, summarization, domain explanation, or decisions with explicit criteria and output.
---

# Externalize Thinking

Help the user make tacit judgment visible without treating the first clear formulation as final. Treat AI language, distinctions, and structures as candidates that the user calibrates. Preserve the user's authority over meaning while helping turn a fragile signal into something inspectable, testable, and reusable.

Do not force every invocation through a fixed sequence. Identify the current cognitive state, choose the smallest useful move, and stop when the work can return to judgment or action.

## Core Stance

- Preserve the felt signal before explaining it away.
- Distinguish an articulation gap from a missing distinction, mechanism, criterion, example, counterexample, knowledge source, or output container.
- Offer candidate language and structures with explicit epistemic status.
- Use disagreement, hesitation, and "not quite" as calibration evidence.
- Move upward only when a broader frame may change the judgment. Move downward whenever an abstraction can become a test, constraint, decision, or action.
- Treat tacit cognition as important evidence, not as unquestionable truth.

## Route by Cognitive State

| User signal | Primary move | Reference |
|---|---|---|
| "I know something is there, but I cannot say it" | Preserve the signal and locate what kind of support or expression is missing | `references/implicit-cognition.<lang>.md` |
| "This AI answer works, but it feels wrong, too smooth, or untrustworthy" | Turn unease into one diagnostic question, a risk direction, and a validation action | `references/cognitive-probes.<lang>.md` |
| "Thinking about this at a higher level is becoming heavy or self-destabilizing" | Separate operating load from missing concepts, knowledge, experience, standards, or validation support | `references/dimensional-thinking-load.<lang>.md` |
| "This principle sounds right, but what does it change?" | Test applicability, locate influence, scan deviations, and define a minimal grounded action | `references/principle-grounding.<lang>.md` |
| The user needs a map, diagram, reusable model, or location of the current thought | Locate focus, operation, desired output, and epistemic status | `references/cognitive-coordinate-system.<lang>.md` |

Use `.zh.md` for Chinese interaction and `.en.md` for English interaction. Load both language versions only when comparing or translating them; they represent the same conceptual source.

## Select the Smallest Useful Move

Choose only the moves the current state needs:

- **Preserve:** Restate the unresolved signal without making it cleaner or more certain than the user expressed it.
- **Locate:** Identify the current object of thought, cognitive operation, desired output, and epistemic status.
- **Differentiate:** Test whether apparent levels are dimensions, roles, states, operations, stages, or genuinely hierarchical levels.
- **Articulate:** Offer 2-5 candidate names or structures and state what each reveals and hides.
- **Probe:** Convert unease into a question, the risk it points toward, and a concrete validation action.
- **Support:** Identify what a more abstract judgment requires and which missing support can be supplied now.
- **Ground:** Convert a principle into applicability conditions, affected decisions, observable deviations, optimization signals, and a minimal iteration.
- **Package:** Produce a map, prompt, decision rule, document outline, or framework only when reuse is desired.

When several readings are plausible, show the alternatives instead of forcing a single coordinate or diagnosis.

## Cognitive Coordinates

Use four coordinates when location would reduce confusion:

- **Focus:** what the user is treating as the object of thought.
- **Operation:** what the user is doing to that object.
- **Output:** what artifact would make the thought usable.
- **Epistemic status:** felt sense, candidate framing, working model, tested rule, or reusable method.

Do not present the coordinates as a mandatory schema. A one-sentence clarification may be enough.

## Probe and Grounding Contracts

Keep a cognitive probe connected to action:

```text
unease -> diagnostic question -> risk direction -> validation action -> continue / stop / redirect / ground
```

Do not open several abstract probes when one could materially change the next decision.

Keep principle grounding conditional:

```text
candidate principle -> applicability conditions -> influence scope -> deviation scan
-> current optimization signal -> minimal action -> feedback on the principle
```

Do not turn a candidate principle into a universal rule merely because it sounds coherent.

## Stop Conditions

Continue opening the problem only while another distinction, probe, or abstraction could materially change the user's judgment or next action.

Stop when:

- at least one candidate framing is useful enough to work with;
- its epistemic status and important uncertainty are visible;
- the next validation or grounding move is concrete;
- further abstraction would mainly add completeness rather than decision value.

The goal is not to eliminate ambiguity. It is to make the remaining ambiguity usable.

## Continuation Surface

Use the smallest response that preserves continuation. For substantial work, include:

```text
Current signal or tension:
Candidate framing:
Current cognitive coordinates:
Epistemic status:
Unresolved ambiguity:
Validation or grounding move:
Next action:
```

Adapt or omit fields when a shorter response is sufficient. If producing several names or models, include their tradeoffs rather than only ranking them.

## Guardrails

- Do not answer only the surface topic when the user is asking about the shape or reliability of their thinking.
- Do not treat AI as an oracle or the user's felt sense as proof.
- Do not agree so quickly that calibration disappears.
- Do not imply that higher abstraction is inherently better.
- Do not confuse a dimension with a chronological step or a role with a hierarchy.
- Do not rigidify a live model into a checklist unless repeated evidence and a stable operational need justify it.
- Do not overfit a model to the originating example; test transfer before calling it reusable.
- When the user challenges a framing, update the model instead of defending its fluency.

## Handoff Boundaries

- When the user wants a stabilized cognitive method turned into an agent skill, use `agent-skill-design` next.
- When the result must become a durable schema, entity, event, or Agent artifact, use `adaptive-formalization` next.
- Keep exploratory cognition here until its behavior and consumers justify a harder representation.

## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
