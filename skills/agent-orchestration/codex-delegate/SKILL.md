---
name: codex-delegate
description: Use when delegating bounded implementation, multi-file refactoring, or test-scaffolding tasks from a coordinator agent (such as Antigravity) to local OpenAI Codex CLI via `codex exec`, including worktree isolation, boundary contracts, and coordinator verification.
metadata:
  short-description: Delegate bounded coding tasks to local Codex CLI
---

# Codex Delegate

Use this skill when a coordinator agent plans the change, defines hard file boundaries, and delegates bounded code execution to local OpenAI Codex CLI (`codex exec`), then integrates and verifies the result.

> The coordinator owns architecture, file ownership, integration, and final verification. Codex owns self-contained execution inside the assigned boundary.

## When to Delegate vs. Keep Local

Delegate to `codex exec` when the task has:
- Clear specifications and acceptance criteria (e.g., implementing a self-contained module, refactoring a bounded subsystem, generating unit tests, or prototyping from 0 to 1).
- Non-trivial code volume where parallel or isolated execution pays off.

Keep local in the coordinator when the task is:
- A small config tweak, single-file micro-edit, or documentation polish.
- Tightly coupled to live browser/UI inspection, external SaaS MCP tools, or exploratory debugging where context changes every step.

## Pre-Flight Checks

1. Verify Codex CLI auth without reading or printing `~/.codex/auth.json`:
   ```bash
   codex login status
   ```
2. Check the target repository's working tree:
   ```bash
   git -C "$REPO" status -s
   ```
3. **Isolate parallel writes**: never let the coordinator and Codex edit the same working directory concurrently. If parallel edits are needed, isolate by repository layout:
   - **Regular Git repo** (`.git` is a directory): create a `git worktree` using a stable, reusable path (avoid random/timestamped paths so `<environment_context>` stays consistent):
     ```bash
     git -C "$REPO" worktree add ../repo-codex -b codex/task-slug
     ```
   - **Git submodule** (`.git` is a file, not a directory): **never** run `git worktree add` to an external directory—submodules inherit a relative `core.worktree` path in `.git/modules/<name>/config`, causing `git` commands, hooks, and tests to fail with `fatal: cannot chdir to '../../../...'`. Create an isolated clone instead (pointing `origin` back to the real remote URL if needed):
     ```bash
     git clone --shared "$REPO" ../repo-codex
     ```
4. **Align runtime environment**: if the target repository declares a required runtime or package manager (e.g., `.nvmrc`, `package.json#engines`), switch to it in the invoking shell before calling `codex exec` (e.g., `nvm use`) and state the expected toolchain in the Brief.

## Delegation Brief Contract

Every delegation prompt must specify all five elements so Codex cannot drift:

1. **Goal & Definition of Done**: what must change and what concrete outcome counts as complete.
2. **Allowed Writable Paths**: explicit files or directories Codex may create or modify.
3. **Out-of-Scope / Invariants**: files not to touch, existing uncommitted user changes to preserve, and contracts not to break.
4. **Key Context Files**: exact paths to specs, types, or existing patterns Codex should read first.
5. **Verification Commands**: exact lint, typecheck, or test commands Codex should run before finishing.

## Shell Execution Patterns

Requires `codex-cli >= 0.150` (check `codex exec --help` if flags differ on your version). Always pass `-C` for the working root and `-s workspace-write` for bounded edits. Never default to `--dangerously-bypass-approvals-and-sandbox`. Run `codex exec` as a foreground process in the coordinator's shell tool (never append `&` or `nohup`) so the host manages backgrounding, timeout notifications, and completion wakeup cleanly. For substantial tasks, set a reasonable host timeout notification (e.g., `NotificationTimeoutSeconds=600`) when invoking through the coordinator's shell tool so long runs neither stall silently nor trigger premature termination.

### Recommended: Brief via Stdin + Capture Final Message

Writing the brief to a temp file and piping it into `-` avoids shell-quoting hazards and prevents stdin hang in background shells. Keep the static contract at the top and volatile task details at the bottom, and never insert timestamps, random IDs, or temp paths inside the prompt prefix. Omitting `--ephemeral` preserves local session logs under `~/.codex/sessions/` so you can inspect or continue later with `codex resume` (note: non-interactive `codex exec` runs are hidden from the Codex Desktop App sidebar by default).

```bash
REPO="/path/to/repo-or-worktree"
BRIEF=$(mktemp /tmp/codex-brief.XXXXXX)
OUT=$(mktemp /tmp/codex-out.XXXXXX)

cat <<'EOF' > "$BRIEF"
Execution & reporting contract:
Work strictly inside the allowed writable paths, preserve unrelated git changes, run the listed verification commands, and report changed files, verification outcomes, and caveats.

Read first / repo conventions:
<key context files and durable conventions>

Allowed writable paths: <explicit paths>
Out of scope: <files/behaviors to leave untouched>
Verify with: <lint/typecheck/test commands>
Task goal & definition of done:
<concrete goal and acceptance criteria>
EOF

codex exec \
  -C "$REPO" \
  -s workspace-write \
  -o "$OUT" \
  - < "$BRIEF"

STATUS=$?
[ -s "$OUT" ] && cat "$OUT"
rm -f "$BRIEF" "$OUT"
exit "$STATUS"
```

### Compact One-Liner (Short Prompts)

Always append `</dev/null` when running non-interactively without piped stdin:

```bash
OUT=$(mktemp /tmp/codex-out.XXXXXX)
codex exec -C "$REPO" -s workspace-write -o "$OUT" "<concise structured brief>" </dev/null
STATUS=$?
[ -s "$OUT" ] && cat "$OUT"
rm -f "$OUT"
exit "$STATUS"
```

### Useful Optional Flags

- Pass model and reasoning effort flags when specified by the user or global/workspace `AGENTS.md` (otherwise inherit `~/.codex/config.toml`):
  `-m <model>` or `-c model_reasoning_effort="high"`
- **Fallback on `model_not_in_accessible_catalog`**: if Codex fails with `model_not_in_accessible_catalog`, inspect `~/.codex/models_cache.json` (`visibility: "list"`) before retrying rather than blindly dropping `-m` (since `~/.codex/config.toml` may also default to an inaccessible model).
- Emit structured JSONL events to stdout for script parsing: `--json`
- Skip persisting the session transcript to disk: `--ephemeral`
- Resume the same delegation session if a follow-up fix is needed:
  `codex exec resume --last "<follow-up fix>" </dev/null`

## Prompt Cache & Session Reuse

- **Static prefix first**: keep invariant instructions and repo conventions above per-task goals and file lists; never put timestamps, random IDs, or temp file paths at the start of the prompt.
- **Stable root & flags**: always invoke from the canonical repo root (or a reusable worktree path) and keep `-m`, `-c`, `--enable`/`--disable`, `-s`, and MCP configuration constant across related runs so the system prompt and tool catalog stay cache-stable.
- **Resume on follow-ups, fresh on unrelated tasks**: each new `codex exec` mints a new thread ID (`prompt_cache_key`) and starts cold; for follow-up fixes on the same task (e.g., addressing review findings), prefer `codex exec resume <session-id>` (or `--last`) with the same `-C` path and flags to reuse the warm prefix cache. Start a fresh `codex exec` for unrelated tasks to avoid stale context bloat.

## Post-Run Verification and Handoff

1. Read `$OUT` to inspect Codex's reported changes, checks, and caveats.
2. Audit boundary compliance before trusting the output:
   ```bash
   git -C "$REPO" status -s
   git -C "$REPO" diff --stat
   ```
   If Codex touched out-of-scope files, revert or split those edits before continuing.
3. Independently run the project's verification suite (`lint`, `typecheck`, `test`) from the coordinator—never rely solely on a delegate's self-report.
4. Clean up temp files (and remove temporary `git worktree` after merging if one was created).
5. Present a concise summary to the user: changed files, verification results, and any remaining risks or next actions.
