# Agent Orchestration Skills

Skills for multi-agent task routing, external CLI delegation, and cross-agent verification or review. A skill belongs here when it coordinates work across distinct agent runtimes rather than designing a standalone system or general behavior.

- [codex-delegate](./codex-delegate/SKILL.md) - delegate bounded coding, refactoring, or test tasks to local OpenAI Codex CLI (`codex exec`).
- [dsh-review](./dsh-review/SKILL.md) - run independent, strictly read-only cross-model code review via local DeepSeek Harness (`dsh --profile headless`).
