---
name: ai-friendly-cli-design
description: Use when designing or changing public CLI command behavior, help text, output shape, pagination, JSON modes, file-output behavior, error messages, or Agent-facing next-action guidance; guides Codex to make CLI commands useful as both execution tools and context delivery tools.
metadata:
  short-description: Design CLIs that agents can safely inspect and continue from
---

# AI-Friendly CLI Design

Use this skill when public CLI behavior affects how an Agent discovers safe usage, runs a command, reads the result, recovers from failure, or chooses the next action.

Core judgment:

> A CLI command is not only an execution surface. It is a context delivery surface for the next Agent step.

## Golden Principles

Help is part of the interface. A command's help should explain why an Agent would call it, what input shape it expects, what output modes exist, what can go wrong, and what a likely next step looks like.

Output is context, not just result. Normal output should carry enough state for an Agent to continue without reconstructing hidden context.

Defaults should be token-aware. Repeated Agent loops need useful, bounded output by default; detail should be opt-in and discoverable.

JSON stdout is a contract. Machine-readable output must stay parseable, stable, and free of logs, banners, or prose.

Ambiguity belongs in the output. If a command is matching, guessing, filtering, truncating, or returning candidates, say so directly.

Errors are guidance. A useful error names the failed input, explains the expected shape, and exits non-zero.

Large artifacts belong in files. Print a path, summary, validation status, and next command instead of flooding the context window.

## Good CLI Signals

Good Agent-facing commands usually have:

- copyable examples with realistic identifiers;
- a concise default output with result, completeness signal, and next action;
- `--format json` for automation;
- `--output <path>` for large or durable artifacts;
- pagination or filters for long collections;
- clear candidate lists instead of silent fuzzy selection;
- stderr for diagnostics that must not pollute structured stdout;
- tests for help text, JSON shape, pagination, file output, and actionable errors.

## CLI Smells

Help smells:

- Help only lists flags and never explains when to use the command.
- Examples hide the real input shape behind vague placeholders.
- Machine-readable and human-readable modes are not distinguished.

Output smells:

- Normal output is decorative, noisy, or too large for repeated Agent loops.
- The result does not say whether it is complete, partial, filtered, paginated, or ambiguous.
- The next action is missing, vague, or only says to review carefully.
- JSON output is mixed with warnings, logs, npm banners, or progress text.

Behavior smells:

- The command silently chooses among ambiguous candidates.
- Default behavior depends on private workspace state, aliases, untracked files, or hidden configuration.
- A command writes durable or network-visible changes without making the action explicit.
- `--verbose` is required for normal decision-making.

Error smells:

- The error says only `Invalid input`.
- Missing, malformed, unsupported, and ambiguous inputs all fail the same way.
- The command exits successfully after failing to do the requested work.

## Design Moves

When improving a CLI, prefer these moves:

- Put the result first, context second, and next action last.
- Add a compact `Summary` and `Next` block to human-readable output.
- Add explicit completeness fields to JSON: pagination, truncation, filters, candidates, warnings, or confidence.
- Move logs and diagnostics to stderr when stdout may be parsed.
- Add `--output <path>` for generated reports, drafts, bundles, or other long artifacts.
- Show the exact command to continue pagination or inspect a written artifact.
- Return candidates with match reasons instead of guessing when resolution is unsafe.
- Add targeted tests around public behavior whenever help, output shape, or exit behavior changes.

## Human Output Shape

Use this shape when a command has a natural next step:

```text
<short result title>

Summary:
- <what was selected, created, changed, returned, or validated>
- <completeness, pagination, filtering, ambiguity, or failure note>

Next:
- <one or two likely next commands or decisions>
```

Do not force the shape when a one-line result is clearer.

## CLI Design Notes

When helping design or diagnose a CLI, keep the response compact:

```text
CLI Design Notes
- Command surface:
- Main CLI smell:
- Output contract:
- Completeness signal:
- Ambiguity handling:
- Error behavior:
- Next-action guidance:
- Validation idea:
```

Use the full shape only when it clarifies the change. For narrow edits, a direct recommendation is better.

## Reference

Load `references/ai-friendly-cli-design.md` when making a broad CLI design change, when tradeoffs are contested, or when you need the full source guide behind these principles.

## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
