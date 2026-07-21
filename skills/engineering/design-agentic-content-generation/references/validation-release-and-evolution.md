# Validation, Release, and Evolution

Load this reference when a live decision depends on what a validator proves, which failure could change the design, how evidence returns to an owning decision, what adoption is justified, or whether repeated experience should change the project or the method. Do not use it as a universal completion checklist.

## Test the Claim That Matters

Use the lightest validator that can actually test the live claim:

- **Deterministic checks:** identity, hash, Schema, syntax, references, file consistency, transformation invariants, package integrity, permissions, and reproducible computation.
- **Runtime checks:** rendering, interaction, accessibility behavior, performance, failure recovery, side effects, and environment compatibility.
- **Evidence checks:** source existence, provenance, freshness, claim support, coverage, counterevidence, and dependency validity.
- **Semantic or domain evaluation:** meaning, pedagogy, methodology, safety interpretation, audience fit, and value judgments.
- **Outcome monitoring:** real use, drift, complaints, correction, withdrawal, downstream error, and unintended effects.

A validator must state what it proves and what it does not prove. Citation existence does not establish claim support; package validity does not establish semantic quality; provenance integrity does not establish factual truth; human review does not establish correctness.

## Close Only the Necessary Local Loop

Where a result or action is consequential, connect its intended claim to observable evidence and freshness, an applicable validator and criterion, a disposition and authority, useful feedback, an owning route-back or reopen point, and evidence for stopping with any retained disagreement.

This is design meaning, not a required record or universal state machine. A useful failure message identifies the violated criterion, supporting evidence, what must change and remain stable, how the change will be revalidated, and which descendants become stale.

Retry only after information gain: new input, evidence, constraint, method, capability, or a materially revised hypothesis. An unchanged retry is not a control strategy. Stopping is supported by decision-relevant evidence and acceptable residual uncertainty—not a fixed iteration count, average score, absence of objections, or producer confidence.

## Separate Validation, Decision, Authorization, and Execution

- **Producer:** proposes or creates a result.
- **Validator:** tests a specified property.
- **Reviewer or evaluator:** judges a property the producer cannot self-certify.
- **Decision authority:** issues a binding disposition.
- **Release authority:** authorizes an exact action on an exact version.
- **Executor:** performs that action.

One person or runtime component may hold several non-conflicting responsibilities in a low-impact project. The design must still reveal what is self-checked, independently checked, decided, authorized, and executed.

Stronger independence may be necessary when the producer benefits from passing, evidence selection could bias evaluation, a decision is consequential or externally authoritative, the same model or context would reproduce a blind spot, or policy requires separation of duties. An evaluator need not be another Agent: prefer deterministic tools for mechanical claims and qualified humans for values, disputes, authority, and affected-party context.

## Bind Evidence Without Turning It into Authorization

When a validation receipt matters, bind it to the validator and version, exact subject version, relevant dependencies and evidence, policy or rubric, material environment, result and exclusions, timestamp, and invalidation conditions.

A changed artifact or dependency cannot inherit an unrelated receipt. Revalidate only the affected envelope and descendants when possible. A receipt is evidence about a check—not a release token, audit truth, safety guarantee, or transferable authorization.

## Challenge by Plausible Failure, Not Assurance Tier

Select a failure hypothesis because it could overturn a route, expose uncovered scope, change a validator or control, narrow adoption, or block an action. Consequence, uncertainty, exposure, reversibility, remedy, and plausible mechanism determine which challenge has decision value.

Possible hypotheses include stale evidence, authority mismatch, version race, queue overload, variant drift, unreviewed population, inaccessible veto, timeout, containment failure, incomplete downstream correction, or a simpler baseline outperforming the proposed collaboration.

Preserve enough to understand the hypothesis, affected route and population, expected control, observed or missing evidence, resulting design change or blocker, and still-uncovered scope. This is optional continuation meaning, not a challenge report template. A test that cannot revise, narrow, block, or reopen the design is not useful assurance.

## Design Recovery Before Consequential Adoption

Where failure can matter, consider detection, containment or hold, owner and authority, earliest owning decision or artifact, correction or regeneration, downstream propagation and notification, revalidation, reopen and closure evidence, and remedy when technical rollback cannot reverse harm.

Technical reversibility, distribution reversibility, decision reversibility, harm reversibility, and remedy availability are different. “We can roll back the database” is not a complete recovery argument.

## Reopen Decisions from New Evidence

Reopen a decision when a material dependency changes: content or source evidence, freshness, policy or obligation, authority, consent, license, population, artifact version, material configuration, operating envelope, observed outcome, or control effectiveness.

Route the evidence to the earliest decision that depended on the changed fact. Preserve the previous rationale and identify:

- what changed and what the new evidence does not prove;
- the owning decision and current disposition;
- affected descendants and unrelated units that remain valid;
- revalidation or new evidence needed;
- who owns the next decision;
- closure, continued hold, or further reopening conditions.

Do not treat approval as permanent, and do not restart the whole project without a dependency reason.

## Leave a Continuation Surface

When validation is incomplete, preserve what was tested and not tested, the validity or freshness window, retained disagreement, current disposition, next discriminating evidence, blocked action, affected scope, and next owner or authority. Express this in the project's useful form rather than a universal assessment template.

A later human or Agent should be able to continue the live decision without repeating unrelated inquiry or mistaking a provisional result for production authorization.

## Separate Design Adoption from Production Authorization

This Skill may recommend further inquiry, a prototype, a bounded pilot, constrained adoption, a blocked decision pending evidence or authority, or retirement of an unhelpful route, recipe, or control.

It must not declare a system production-ready, safe, fair, compliant, or authorized. Any adoption recommendation should make its route/population/channel scope, relevant versions, duration and exclusions, monitoring, stop or reopen triggers, unresolved evidence, and responsible owner understandable at the resolution the consequence requires.

Publish, deprecate, suppress, correct, retract, reinstate, notify, or execute are actions owned by the domain system and its authorized people. The method designs their boundaries but does not perform them.

## Learn at the Owning Level

New evidence can justify different kinds of change:

- **Instance or artifact correction:** one result or version was wrong.
- **Project decision revision:** a route, validator, control, or adoption boundary changes locally.
- **Scoped recipe or example change:** a recurring situation has a useful, bounded default or counterexample.
- **Lens or fit-boundary revision:** repeated cases expose a systematic blind spot or non-applicable domain.
- **Behavioral-kernel revision:** heterogeneous projects repeatedly show the same structural failure and the change reliably improves design decisions.
- **No method change:** the case is explainable by existing guidance or remains exceptional.

Do not turn every incident into another universal field, gate, prohibition, or Agent role. Before changing the core method, look for recurrence across heterogeneous projects, a shared mechanism, observable decision improvement, and regressions in simple or counterexample cases.

Useful operating evidence includes misroutes, missed local red lines, unnecessary gates, reviewer burden, user corrections, evaluator disagreement, stale dependency and propagation failures, downstream consumption, rework, withdrawal, correction, appeal, harm, and whether controls changed actual decisions.

## Formalize and Retire Locally

Begin with the least formal representation that preserves the decision and continuation context. Promote a local projection or deterministic helper only when it repeats across heterogeneous real cases, has a named consumer, free text causes observable errors, version and ownership semantics are known, and validation and failure responsibility are testable.

Candidates may include a route summary, review-queue projection, artifact dependency map, or validation receipt. Stable authorization and release facts belong in dedicated audited systems, not in a design note.

Loosen, merge, or remove a representation, recipe, lens, or control when users bypass it, unknown values expose forced classification, independent designers cannot reproduce its decision, it erases uncertainty, maintenance cost exceeds benefit, it duplicates an authoritative system, no consumer uses it, or it changes no outcome beyond adding explanation.

## Regression Probes

Use these examples when evaluating a method change, not as cases every project must analyze:

- a narrow reversible internal transformation remains narrow rather than triggering a complete assessment;
- one rights-affecting action receives local authority, recovery, and appeal treatment without upgrading unrelated routes;
- a stale dependency reopens only its owning decision and descendants;
- a legacy Profile remains a recipe alias rather than a project class;
- a mechanical invariant goes to a deterministic validator rather than another Agent or human reviewer;
- an approval click without scoped authority and evidence cannot authorize release;
- an unchanged retry stops or changes its evidence, method, input, constraint, or hypothesis;
- a systems lens that changes no decision is omitted;
- another Agent can continue from preserved scope, epistemic state, owner, next evidence, and reopening conditions;
- one unusual local case does not become a universal method rule without repeated cross-case evidence.

A method revision is suspect if it makes simple cases burdensome, lets flexibility bypass hard boundaries, or recreates a hidden workflow through mandatory lenses, fields, or examples.
