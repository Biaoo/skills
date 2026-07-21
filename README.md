# Skills

This repository is for maintaining personal agent skills.

## Install

Install skills from this repository with the Skills CLI:

```bash
npx skills@latest add Biaoo/skills
```

Install a specific skill by name:

```bash
npx skills@latest add Biaoo/skills --skill <skill-name>
```

For example:

```bash
npx skills@latest add Biaoo/skills --skill adaptive-formalization
npx skills@latest add Biaoo/skills --skill ai-friendly-cli-design
npx skills@latest add Biaoo/skills --skill context-efficiency-evaluation
npx skills@latest add Biaoo/skills --skill design-agentic-content-generation
npx skills@latest add Biaoo/skills --skill agent-skill-design
```

List available skills before installing:

```bash
npx skills@latest add Biaoo/skills --list
```

This repository currently contains the skills listed below.

## Structure

- `skills/engineering/` - reusable skills for software engineering work.
- `skills/personal/` - skills tied to personal workflows, local tools, or private context.

## Skills

### Engineering

- [adaptive-formalization](./skills/engineering/adaptive-formalization/SKILL.md) - choose the right formalization level for AI-native entities, schemas, artifacts, and agent outputs.
- [ai-friendly-cli-design](./skills/engineering/ai-friendly-cli-design/SKILL.md) - design CLI commands that agents can inspect, parse, and continue from safely.
- [context-efficiency-evaluation](./skills/engineering/context-efficiency-evaluation/SKILL.md) - evaluate agent context efficiency only after correctness, safety, and evidence gates.
- [design-agentic-content-generation](./skills/engineering/design-agentic-content-generation/SKILL.md) - design trustworthy Agentic content-generation projects with local routes, proportional controls, and explicit human intervention.

### Personal

- [agent-skill-design](./skills/personal/agent-skill-design/SKILL.md) - design agent skills as progressive behavioral interfaces.

## Maintenance

Create each skill as a self-contained directory:

```text
skills/<bucket>/<skill-name>/
└── SKILL.md
```

Optional skill resources can be added when needed:

```text
skills/<bucket>/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
└── assets/
```

After adding a stable skill, update this README and the relevant bucket README.

## Local Scripts

List skills in this repository:

```bash
scripts/list-skills.sh --format table
```

Link skills into a local agent skills directory:

```bash
scripts/link-skills.sh --target codex
scripts/link-skills.sh --target claude
```

Link only one bucket:

```bash
scripts/link-skills.sh --target codex --bucket engineering
```

Preview link changes without writing files:

```bash
scripts/link-skills.sh --target codex --dry-run
```
