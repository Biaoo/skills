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
npx skills@latest add Biaoo/skills --skill calibrated-assertiveness
npx skills@latest add Biaoo/skills --skill externalize-thinking
npx skills@latest add Biaoo/skills --skill living-documentation
npx skills@latest add Biaoo/skills --skill mechanism-guided-analysis
npx skills@latest add Biaoo/skills --skill outcome-first-implementation
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
- [calibrated-assertiveness](./skills/personal/calibrated-assertiveness/SKILL.md) - preserve clear intent without defensive caveats, scope reduction, or weakened verification.
- [externalize-thinking](./skills/personal/externalize-thinking/SKILL.md) - externalize fuzzy intuitions and calibrate human-AI co-thinking.
- [living-documentation](./skills/personal/living-documentation/SKILL.md) - keep active documentation current and route valuable history to separate, on-demand records.
- [mechanism-guided-analysis](./skills/personal/mechanism-guided-analysis/SKILL.md) - trace surface signals to plausible mechanisms, better designs, and discriminating validations.
- [outcome-first-implementation](./skills/personal/outcome-first-implementation/SKILL.md) - prioritize requested outcomes over implementer convenience when AI owns the implementation.

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

Preview the container installation:

```bash
scripts/one-shot-container-install.sh
```

Run the installation:

```bash
scripts/one-shot-container-install.sh --execute
```

The script installs one skill in one disposable container. It can be run again
after a successful installation; concurrent runs are rejected to avoid reusing
the same container name.
