# Routing and Patterns

Load this reference when a live decision depends on mixed routes, operating envelopes, legacy Profiles, significant variants, inheritance, continuous or batch behavior, recipe conflicts, or nontrivial artifact lineage. Enter at the relevant uncertainty; do not traverse the document to make a simple design look complete.

## Find the Relevant Routing Uncertainty

Common entry points include:

- the useful routing unit changes with scale, cadence, or disposition;
- project-wide descriptions hide consequential local differences;
- several sources or outputs branch, merge, inherit, or become stale differently;
- a legacy Profile is being treated as a project type;
- a recipe, obligation, assurance control, and runtime mechanism are being conflated;
- no artifact clearly owns semantic intent, evidence, decision, projection, or release truth.

Inquiry may move laterally among envelope, route, artifact, evidence, and authority. Use only the sections that can change the current design decision.

## Understand the Operating Envelope

The envelope helps identify a useful routing unit. Consider only facts that can change a route or control:

- **Operation:** one-shot, batch, continuous, real-time, event-driven, or mixed.
- **Routable unit:** claim, section, artifact, version, locale, audience archetype, cohort, instance, event, decision, exception, or a better local unit.
- **Scale and change:** volume, arrival rate, freshness, deadlines, dependency churn, and expected lifetime.
- **Inheritance:** what a policy, recipe, review, or validation result may cover and what must be rechecked locally.
- **Available dispositions:** generate, hold, label, suppress, revise, reject, publish, correct, retract, notify, or another local action.

The envelope is not another classification dimension or fixed enum. Its purpose is to expose assumptions such as routing every page independently or treating one approval as permanent across changing instances.

## Select Lenses That Can Change the Route

The six lenses below are optional, overlapping prompts—not a required baseline or complete ontology.

| Live uncertainty | A useful lens may ask | Possible consequence |
|---|---|---|
| Nature of the knowledge change | Is the system retrieving, transforming, synthesizing, specifying, generating, evaluating, discovering, personalizing, curating, or doing something locally different? | source access, semantic responsibility, evaluator choice |
| Behavior of the artifact | Is the result read, rendered, interacted with, executed, or continuously served? | packaging, runtime tests, accessibility, failure surface |
| Change over time | What recurs, expires, drifts, or arrives as an event? | freshness, versioning, monitoring, reopening |
| Branching and merging | How do sources, outputs, populations, and inherited decisions relate? | artifact authority, coverage, propagation, delta validation |
| Evidence and consequence | What can be wrong, who is affected, and can the effect be reversed or remedied? | evidence burden, independence, containment, safe state |
| Control relationship | Who may propose, verify, decide, interrupt, authorize, and execute? | interfaces, authority, escalation, runtime enforcement |

Use natural-language, multivalued, disputed, or unknown answers. A project summary expresses only shared facts. Route-, instance-, population-, or action-level facts override it when their consequences differ.

Do not derive total risk, maturity, readiness, or autonomy; require one value per lens; serialize these prompts as stable fields without a demonstrated consumer; or discuss a lens whose answer changes nothing.

When a vague term controls a consequential branch, make its local meaning testable. An optional reasoning shape is:

```text
Term → observable condition → affected scope → triggered action
     → evidence that could reverse the judgment → narrower reversible default if unresolved
```

This is an inquiry aid, not a persisted contract.

## Keep Obligations Authoritative

Policies, licenses, privacy constraints, domain standards, formal evaluation rules, and security requirements are not recipes or risk labels. Use one semantic source for each applicable obligation, preserving its source and authority, scope, consequence, override conditions, unresolved conflict, and triggered action.

Recipes and assurance controls may reference an obligation; they must not duplicate or silently reinterpret it. If authorities conflict, do not invent a universal priority order. Narrow or block the affected action until an authorized local decision resolves the conflict.

## Locate Consequential Route Units

A separate route unit is useful only when at least one consequential property changes:

- intended outcome or consumer;
- evidence or freshness requirement;
- artifact authority or lineage;
- human or system authority;
- reversibility, remedy, or blast radius;
- validator or acceptance claim;
- disposition, recovery, correction, or propagation behavior.

A route unit may be a stage, branch, feedback path, audience archetype, release action, exception, or another local view. It is not a required object type.

Capture only enough to support the live decision. Useful prompts may include purpose and scope, inputs and dependencies, operation or decision, artifacts or effects, applicable obligations, observable result, validator, disposition, continuation, invalidation, and route-back. Omission is appropriate when the missing detail cannot change the present decision; preserve it as an unknown when it might.

## Distinguish Route, Recipe, Overlay, Rule, and Runtime

- **Artifact-lifecycle route:** a mutually exclusive disposition for the same object and transition, such as reuse/configure/derive/create/reject or draft/publish/retract.
- **Recipe or preset:** composable defaults that add useful behavior for a recurring, scoped situation.
- **Assurance overlay:** a control applied across relevant routes, such as provenance, independent verification, accessibility equivalence, immutable release, sampling, or monitoring.
- **Domain rule:** an obligation owned by the relevant policy or authority.
- **Runtime control:** an implemented state, permission, queue, lock, authorization, or executor owned by the production system.

A recipe does not own policy truth, a Markdown receipt does not authorize execution, and an inquiry method does not own runtime state.

## Treat Legacy Profiles as Recipe Aliases

The former research-report, structured-knowledge, visual-narrative, interactive-learning, and executable-discovery Profiles are shorthand for choices that sometimes co-occur. They are neither mutually exclusive project classes nor a completeness claim.

When continuity requires a legacy Profile, preserve its original name, source, version, and meaning; translate its useful assumptions into observable route fragments, artifacts, controls, and validation expectations; restrict those defaults to their actual scope; override them with local evidence and authority; combine recipes where behaviors genuinely mix; and retire the alias when direct local reasoning is clearer.

Do not designate a primary Profile. If the original meaning is unavailable, treat migration as unresolved rather than inventing a replacement definition.

A useful recipe is falsifiable. It should make its applicability, behavioral increment, expected benefit, important requirements, counterexamples, evidence, and exit or retirement conditions understandable at the resolution the current decision needs. It does not need a universal record shape. Compare alternatives only where consequential alternatives are genuinely available or disputed.

## Model Artifact Authority and Lineage Locally

Ask which artifact or system carries which kind of authority:

- semantic intent;
- source evidence;
- approved decision;
- machine-consumable projection;
- channel rendition;
- runtime package;
- release record.

A project may have several authoritative artifacts for different concerns. “Canonical” does not require one file, and “derived” does not mean unimportant.

When lineage can change a decision, preserve the writer or decision owner, derivation relation, consumers and version lock, mutation policy, invalidation event, affected descendants, and regeneration, correction, withdrawal, or notification direction.

For batch or personalized outputs, a standing decision covers only an explicit eligible population and stable invariants. Preserve instance deltas, exclusions, expiry, and local invalidation rather than copying a complete review record. A systemic failure may expand review or invalidate an affected archetype and descendants; it does not automatically reopen unrelated routes.

## Recognize Useful Topologies Without Building a Universal Machine

A project may use any combination of:

- a controlled linear transformation;
- branching channel, locale, audience, or personalized variants;
- many-source synthesis with coverage and disagreement handling;
- continuous maintenance reopened by dependency change, freshness expiry, feedback, or drift;
- evidence repair returning to acquisition, claim revision, or scope reduction;
- human return for a decision, exception, or correction;
- event-driven containment separated from final investigation and disposition.

These are descriptive patterns, not stages or a project-wide state machine.

## Leave a Continuable Route Decision

For route work that remains provisional, preserve the current unit and disposition, unresolved branch, inherited versus locally revalidated facts, evidence needed next, owning decision, invalidation event, and affected descendants. New evidence should reopen the earliest owning decision and only its dependent envelope.

Examples of expected behavior:

- a mixed project may compose several recipes without selecting a primary Profile;
- one consequential action may require stronger authority and recovery without upgrading unrelated routes;
- a simple one-shot transformation may need no explicit route model;
- a stale dependency or new variant reopens only decisions that depended on the changed fact.

These examples test the method; they are not cases every invocation must analyze.

## Failure Signals

Revise the design when it exhibits:

- **Profile reification:** a legacy name determines controls without local evidence.
- **Project averaging:** a global label hides a consequential local decision.
- **Lens completion theater:** every prompt is discussed although most change nothing.
- **Variant flattening:** variants are treated as independently generated or equally covered without evidence.
- **Canonical absolutism:** one file is forced to own incompatible kinds of truth.
- **Hidden ordering:** descriptive routes or lenses become required stages.
- **Stage-override burial:** a local exception cannot affect validation or authority.
- **Workflow cosplay:** a fixed pipeline exists mainly because workflows look systematic.
- **Agent proliferation:** a responsibility distinction becomes another Agent without an execution need.
- **Inheritance without eligibility:** a review is claimed to cover a population whose invariants were never defined.
- **Global reopening:** one changed fact invalidates unrelated decisions without a dependency path.
