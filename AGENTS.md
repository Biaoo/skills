# Agent Instructions

This repository maintains personal agent skills. Keep the project small and easy to scan.

## Repository Layout

- `skills/agent-systems/` contains skills whose primary subject is Agent or AI-native systems, interfaces, and evaluation.
- `skills/thinking/` contains skills that help the user externalize, examine, or develop their thinking.
- `skills/agent-behavior/` contains cross-domain preferences for how an Agent should work.
- `skills/writing/` contains skills whose primary output is written content or documentation.
- `skills/skill-system/` contains skills for designing, maintaining, and improving the skill collection itself.
- `CLAUDE.md` is a symlink to this file so Claude-oriented tools read the same rules.

Classify a skill by the primary object it improves, not by the fact that an Agent uses it. All skills in this repository are Agent-executed, so `agentic` alone is not a useful category boundary. For example, a skill that designs an Agent system belongs in `agent-systems`, while a skill that designs a user interface belongs in a future `ui-design` category.

Give each skill one primary category. Keep secondary relationships in its description or the repository index rather than duplicating the skill or adding a tag schema prematurely.

## Skill Layout

Each skill must live in its own directory:

```text
skills/<category>/<skill-name>/
└── SKILL.md
```

Use lowercase, hyphenated skill names. The skill directory name should match the `name` field in `SKILL.md`.

Optional resources inside a skill:

- `agents/openai.yaml` for UI metadata.
- `references/` for documentation loaded only when needed.
- `scripts/` for deterministic helper scripts.
- `assets/` for templates, images, fonts, or other output resources.

Do not add `README.md`, changelogs, or installation guides inside individual skill directories unless explicitly requested.

## Skill Feedback Hook

Every skill except `report-biaoo-skill-feedback` must end with this exact section:

```markdown
## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
```

Keep the section at the end of `SKILL.md`. Do not duplicate the reporting workflow there; `report-biaoo-skill-feedback` owns authorization, session isolation, privacy, duplicate handling, and GitHub submission.

When interpreting or acting on feedback issues, read `docs/skill-feedback-as-observation.en.md` or the matching Chinese version, `docs/skill-feedback-as-observation.zh.md`. Do not turn a case-specific proposal directly into a general rule, and do not discard the Agent behavior it reveals merely because the issue's conclusion is wrong.

## Index Rules

- Keep the top-level `README.md` useful for people installing skills from this repository.
- Include `npx skills@latest add Biaoo/skills` as the primary install command unless the GitHub repository changes.
- Update the top-level `README.md` when adding stable, generally useful skills.
- Update the relevant category README when adding any skill to that category.
- Owner-specific skills may stay out of the top-level README if they are only useful to the owner.

## Maintenance Rules

- Prefer concise skill instructions over broad background material.
- Move long reference material out of `SKILL.md` into `references/`.
- Do not add install, sync, release, or package-management tooling until requested.
- Keep repository scripts conservative: include help text, support dry-run when writing outside the repo, and do not overwrite non-symlink user files unless explicitly forced.
- Add a new category only when a skill has a stable primary target not represented by an existing category. Domain categories such as `ui-design` or `research` may be added as the collection grows.
- If the correct primary category is unclear, ask before creating the skill.
