# Agent Instructions

This repository maintains personal agent skills. Keep the project small and easy to scan.

## Repository Layout

- `skills/engineering/` contains reusable skills for software engineering workflows.
- `skills/personal/` contains skills tied to personal setup, private workflows, local tools, or preferences.
- `CLAUDE.md` is a symlink to this file so Claude-oriented tools read the same rules.

## Skill Layout

Each skill must live in its own directory:

```text
skills/<bucket>/<skill-name>/
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

## Index Rules

- Keep the top-level `README.md` useful for people installing skills from this repository.
- Include `npx skills@latest add Biaoo/skills` as the primary install command unless the GitHub repository changes.
- Update the top-level `README.md` when adding stable, generally useful skills.
- Update the relevant bucket README when adding any skill to that bucket.
- Personal skills may stay out of the top-level README if they are only useful to the owner.

## Maintenance Rules

- Prefer concise skill instructions over broad background material.
- Move long reference material out of `SKILL.md` into `references/`.
- Do not add install, sync, release, or package-management tooling until requested.
- Keep repository scripts conservative: include help text, support dry-run when writing outside the repo, and do not overwrite non-symlink user files unless explicitly forced.
- If the correct bucket is unclear, ask before creating the skill.
