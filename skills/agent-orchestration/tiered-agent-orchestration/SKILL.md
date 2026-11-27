---
name: tiered-agent-orchestration
description: Use in Antigravity when planning or executing multi-file coding, refactoring, batch bug fixes, or high-risk changes and deciding whether to complete work locally (L1), delegate bounded implementation to an external coding CLI such as codex-delegate (L2), or add an independent read-only cross-model review such as dsh-review (L3), including batch sizing, isolation, and convergence guardrails. Designed for Antigravity as the coordinator; do not use from Codex to self-delegate.
metadata:
  short-description: Route and coordinate L1/L2/L3 multi-agent delivery for Antigravity
---

# Tiered Agent Orchestration (for Antigravity)

Use this skill in Antigravity when acting as the coordinator control plane for software delivery—deciding which work stays local, which bounded coding tasks go to an external executor, and when to trigger an independent cross-model review gate. (Do not invoke from Codex to self-delegate.)

> The coordinator owns problem framing, batching, isolation, integration, independent verification, and user escalation; external executors and reviewers are bounded specialists, never autonomous loops.

## Tiered Routing Matrix (L1 / L2 / L3)

- **L1 — Local Direct Execution**: Q&A, docs or copy edits, small config tweaks, single-file micro-fixes, and exploratory browser/UI work. Handle directly in the coordinator without external CLI overhead.
- **L2 — Plan → Delegate Execution → Verify**: Clear-spec feature modules, multi-file refactors, batch bug fixes, test scaffolding, and 0→1 prototypes. The coordinator designs contracts and writable file boundaries, delegates bounded execution via `codex-delegate` (or an equivalent coding CLI), and independently runs lint, typecheck, tests, and build.
- **L3 — L2 + Independent Cross-Model Review Gate**: Core business logic, auth/security boundaries, concurrency or state machines, schema/data migrations, large refactors, and pre-merge PR gates. After implementation and verification pass, invoke `dsh-review` (or an equivalent strictly read-only cross-family reviewer), verify findings against source code, filter false positives, and present material risks for user sign-off.

## Batching and Scope Discipline

- **Separate bugs from open decisions**: split clear, deterministic bug fixes away from unresolved product or design choices before delegating—never delegate open ambiguity to an executor.
- **One focused batch per repository**: advance one scoped repository or subsystem batch at a time instead of fanning out unrelated changes across multiple repos in a single delegation.
- **Right-size for cache and timeout budgets**: keep batches small enough that delegation and review converge cleanly within active prompt-cache windows and execution timeout budgets.

## Non-Negotiable Coordination Guardrails

1. **Write Isolation**: never let two agents edit the same working tree concurrently. Use stable, reusable `git worktree` paths for regular repositories, and `git clone --shared` (never external `worktree add`) for Git submodules.
2. **Strict Read-Only Review**: external reviewers must never mutate repository files; verify `git status` cleanliness before and after running a review.
3. **Single-Round Convergence**: cap automated cross-review at 1 round by default. The coordinator must verify every finding against actual source code, drop false positives, and escalate confirmed risks for user decision—never enter an automated write→review→rewrite loop.
4. **Independent Verification & Honest Fallback**: always run repository verification commands independently after delegation. If an external reviewer fails (credentials, timeout, or outage), a manual diff audit may serve as fallback ONLY with an explicit disclosure to the user that independent cross-model review did not execute.
5. **Runtime & Cache Hygiene**: align repository runtime versions before delegating, keep CLI/MCP flags constant across related runs, and resume the existing executor thread for targeted follow-up fixes on the same task.

## Model & Reasoning Defaults

- **Precedence**: explicit user request → global/workspace `AGENTS.md` → local CLI configuration (`~/.codex/config.toml` or `~/.dsh/profiles/headless`).
- **Executor (`codex-delegate`)**: prefer a coding-focused model at `high` or `xhigh` reasoning effort (e.g., `-m gpt-6.1-sol -c model_reasoning_effort="xhigh"` when available on the account, otherwise the local CLI default).
- **Reviewer (`dsh-review`)**: use a different model family from the executor, configured at `low` reasoning effort in `~/.dsh/profiles/headless` so cross-model reviews converge cleanly within the timeout budget.
- **Graceful fallback**: if the preferred model is unavailable on the current account or CLI version, state the limitation explicitly before falling back to an available model from the local catalog or CLI default.

## End-to-End Delivery Loop

1. **Frame & Tier**: separate clear bugs from open decisions, pick L1/L2/L3, and size one focused batch.
2. **Isolate & Delegate**: prepare an isolated worktree/clone if needed, align runtime toolchain, and invoke `codex-delegate` with explicit writable boundaries and verification commands.
3. **Independently Verify**: inspect `git status` / `git diff --stat` for boundary compliance, then run lint, typecheck, tests, and build directly from the coordinator.
4. **Cross-Review Gate (L3)**: run `dsh-review` against the verified diff + intent summary, enforcing read-only guards and hard timeouts.
5. **Triage & Escalate**: verify any reported findings against source code, filter noise, apply or delegate only confirmed fixes, and present a concise ship/decision summary to the user.
