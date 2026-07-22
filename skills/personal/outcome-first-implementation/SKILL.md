---
name: outcome-first-implementation
description: Use when choosing or designing an implementation path and the agent may trade away requested quality, fidelity, capability, or completeness to reduce implementation effort, code volume, technical unfamiliarity, or default to KISS or MVP. Encodes the user's preference to give the agent's own execution effort little weight unless it creates a concrete user-relevant consequence or violates an explicit budget. Do not use when the user explicitly prioritizes speed, minimum change, or lowest cost.
---

# Outcome-First Implementation

Treat the agent's own implementation effort as a low-weight internal cost, not a user-facing reason to lower the requested result.

- Prefer a materially stronger expected result even when it requires substantially more implementation work.
- Do not reduce requested scope, fidelity, capability, or completeness merely because a route is difficult, unfamiliar, code-heavy, or expensive for a human engineer.
- Absorb reversible, implementation-local burden. Surface trade-offs only when they affect feasibility, verification, runtime, integration, security, reversibility, maintenance, or an explicit budget.
- Prefer simplicity when expected result quality is effectively tied; never add complexity without a concrete benefit.
- Use MVPs or staged delivery to learn, validate, or contain risk, not as an undeclared reduction of the final quality bar.

When revising or explaining this skill, read the matching `references/design-rationale.zh.md` or `references/design-rationale.en.md`. Normal implementation tasks do not require either reference.

## How to Improve This Skill

If real use reveals a possible improvement, keep the task moving and use `report-biaoo-skill-feedback`. If unavailable, retain a privacy-safe `Biaoo/skills` issue draft rather than submitting from this session.
