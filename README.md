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
npx skills@latest add Biaoo/skills --skill report-biaoo-skill-feedback
```

List available skills before installing:

```bash
npx skills@latest add Biaoo/skills --list
```

This repository currently contains the skills listed below.

## Structure

Skills are grouped by the primary object they improve:

- `skills/agent-systems/` - Agent and AI-native systems, interfaces, and evaluation.
- `skills/thinking/` - the user's thinking, articulation, and analysis.
- `skills/agent-behavior/` - cross-domain preferences for how an Agent should work.
- `skills/writing/` - written content and documentation.
- `skills/skill-system/` - the design and evolution of the skill collection itself.

All skills are Agent-executed, so categories do not describe whether work is
agentic. New domains such as `ui-design` should become categories when a skill's
primary output belongs there.

## Skills

### Agent Systems

- [adaptive-formalization](./skills/agent-systems/adaptive-formalization/SKILL.md) - choose the right formalization level for AI-native entities, schemas, artifacts, and agent outputs.
- [ai-friendly-cli-design](./skills/agent-systems/ai-friendly-cli-design/SKILL.md) - design CLI commands that agents can inspect, parse, and continue from safely.
- [context-efficiency-evaluation](./skills/agent-systems/context-efficiency-evaluation/SKILL.md) - evaluate agent context efficiency only after correctness, safety, and evidence gates.
- [design-agentic-content-generation](./skills/agent-systems/design-agentic-content-generation/SKILL.md) - design trustworthy Agentic content-generation projects with local routes, proportional controls, and explicit human intervention.

### Thinking

- [externalize-thinking](./skills/thinking/externalize-thinking/SKILL.md) - externalize fuzzy intuitions and calibrate human-AI co-thinking.
- [mechanism-guided-analysis](./skills/thinking/mechanism-guided-analysis/SKILL.md) - trace surface signals to plausible mechanisms, better designs, and discriminating validations.

### Agent Behavior

- [calibrated-assertiveness](./skills/agent-behavior/calibrated-assertiveness/SKILL.md) - preserve clear intent without defensive caveats, scope reduction, or weakened verification.
- [outcome-first-implementation](./skills/agent-behavior/outcome-first-implementation/SKILL.md) - prioritize requested outcomes over implementer convenience when AI owns the implementation.

### Writing

- [living-documentation](./skills/writing/living-documentation/SKILL.md) - keep active documentation current and route valuable history to separate, on-demand records.

### Skill System

- [agent-skill-design](./skills/skill-system/agent-skill-design/SKILL.md) - design agent skills as progressive behavioral interfaces.
- [report-biaoo-skill-feedback](./skills/skill-system/report-biaoo-skill-feedback/SKILL.md) - return observations from real skill use to Biaoo/skills without disrupting the active task.

## Maintenance

Create each skill as a self-contained directory:

```text
skills/<category>/<skill-name>/
└── SKILL.md
```

Optional skill resources can be added when needed:

```text
skills/<category>/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
└── assets/
```

After adding a stable skill, update this README and the relevant category README.

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

Link only one category:

```bash
scripts/link-skills.sh --target codex --category agent-systems
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
