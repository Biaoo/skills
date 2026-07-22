# AI-Friendly CLI Design Reference

This reference preserves the source guide that `SKILL.md` was distilled from. Load it when the short skill body is not enough for a broad CLI design change.

CLI is the first-class interface for Agents. Treat each command as both an execution tool and a context delivery tool.

This document defines design expectations for public Agent-facing CLI commands. It is not a command reference and should not duplicate every option from `--help`.

## 1. Design Contract

An AI-friendly CLI should let an Agent answer five questions quickly:

- What can this command do?
- What input shape does it expect?
- What exactly did it return?
- Is the result complete, partial, ambiguous, or failed?
- What is the safest next action?

The CLI should optimize for repeated Agent loops: inspect, choose, run, validate, and hand off. Human-readable output may contain guidance. Machine-readable output must remain stable and parseable.

## 2. Help Is Part of the Interface

Agents should be able to discover safe usage directly from the CLI.

- Global help should explain the overall workflow and available command families.
- Command help should explain purpose, when to use the command, required inputs, optional inputs, output modes, examples, and likely next steps.
- Help should be concise enough to fit into an Agent context window without crowding out the task.
- Help should distinguish stable machine-readable output from human-readable output.
- Help should describe ambiguity and failure modes when they are common.
- Help examples should be copyable and should use realistic identifiers rather than placeholders that hide the expected shape.

Avoid help text that only lists flags. A command's help should answer: "Why would an Agent call this, what does it need, what will it receive, and what should it do next?"

## 3. Output Is Context, Not Just Result

CLI output is often pasted or streamed directly into an Agent context window. The output should carry enough state for the Agent to continue without reconstructing hidden context.

Good output should usually include:

- the key identifier or object the command operated on
- whether the result is complete, filtered, paginated, or partial
- a concise summary before large details
- short guidance for the likely next action
- stable structured data when `--format json` is used

Avoid decorative banners, progress noise, repeated prose, or logs in normal output. These consume context without helping the Agent decide.

Recommended human-readable shape:

```text
<short result title>

Summary:
- <what was selected, created, changed, or validated>
- <important completeness or ambiguity note>

Next:
- <one or two likely next commands or decisions>
```

The exact wording can vary, but the ordering should stay predictable: result first, context second, next action last.

## 4. Token-Aware Defaults

Default output should be small enough for repeated Agent use.

- Long collections should not print in full by default.
- Prefer pagination, filters, depth limits, or explicit detail flags.
- Large generated artifacts should be written to a file, with the CLI printing the path and a short summary.
- Commands should make truncation, pagination, filtering, or file output explicit.
- Detailed output should be opt-in and discoverable from help.

The goal is not minimal output; the goal is useful output with a predictable context cost.

For long result sets, default to a small page size and include:

- current page and page size
- total count when known
- whether more results are available
- the exact command or flags to continue

For long generated content, prefer writing the artifact to disk and printing:

- output path
- artifact type
- short summary
- validation status if available
- next command to inspect or publish it

## 5. Next Actions Should Be Discoverable

Agent-facing commands should reduce planning ambiguity.

- If there is a natural next command, include it in human-readable output.
- If there are multiple plausible next actions, summarize the choice.
- If a command cannot make a safe decision, return candidates and explain selection criteria.
- If required information is missing, say exactly what is missing and show the expected input shape.
- If output is incomplete, say how to continue.

Do not silently choose among ambiguous candidates just to keep the command moving.

Next-action guidance should stay operational. Avoid broad advice such as "review the output carefully" unless the command also says what to review and why.

## 6. Separate Data Modes From Reading Modes

Different consumers need different output.

- Machine-readable modes should be stable, parseable, and free of non-data banners.
- Human-readable modes should be concise, explanatory, and next-step oriented.
- JSON output should not be mixed with logs, warnings, or npm banners on stdout.
- Documentation should use silent invocation patterns when the output is meant to be parsed.
- If warnings matter for machine consumers, include them as structured fields or write them to stderr.

Human-readable output may evolve more freely. JSON output is a contract and should change additively whenever possible.

Recommended modes:

- default: concise human-readable output with next-step guidance
- `--format json`: stable structured output for automation
- `--output <path>`: write large or durable artifacts to a file
- `--verbose`: opt-in diagnostic detail

Do not make `--verbose` necessary for normal Agent decision-making.

## 7. Prefer Deterministic Interactions

Agents are stronger when commands reduce uncertainty rather than hide it.

- Prefer explicit ids, mappings, filters, selectors, and scopes.
- Make heuristic or fuzzy results clearly marked as candidates.
- Return confidence, match type, or reason fields when the command performs interpretation.
- Do not let a command's default behavior depend on private workspace state, shell aliases, or untracked local files.
- When deterministic resolution exists, prefer it over search-like behavior.

If the command is exploratory, the output should say it is exploratory.

## 8. Error Messages Are Guidance

Errors are part of the interface.

- Say what failed.
- Say which input was missing, malformed, ambiguous, or unsupported.
- Show the expected shape when practical.
- Keep the message short enough to be useful in an Agent loop.
- Exit non-zero on failure.
- Use distinct exit codes when callers can reasonably react differently.

Good:

```text
Use --classification <system>:<version>:<code>, for example cpc:3.0:01111
```

Avoid:

```text
Invalid input
```

## 9. Feedback and Handoff

When a command helps collect improvement feedback, it should produce a durable handoff artifact rather than only a chat-like message.

Good feedback flows should:

- collect source, evidence, proposed change, affected object, and uncertainty
- generate issue-ready text or a file path
- avoid opening network resources or submitting issues unless explicitly requested
- keep user-provided evidence separate from generated interpretation
- include enough context for maintainers to reproduce the finding

Feedback commands should guide contribution without letting runtime consumers mutate canonical records directly.

## 10. Design For Repeated Agent Loops

Agents often run a command, inspect output, then run another command. CLI design should make that loop stable.

- Keep command names and JSON field names stable.
- Include enough state in each response that the next command can be constructed.
- Avoid output that requires fragile string scraping when structured output is available.
- Keep compatibility commands when a concept remains valid.
- Add tests for help, pagination, JSON shape, and actionable errors when public behavior changes.

The most important test is behavioral: after reading normal output, an Agent should know whether to stop, continue with a specific command, ask for input, or create a handoff artifact.
