# Systems Lenses

Load this reference only when a named design mechanism remains unclear and a systems lens could change a hypothesis, evidence requirement, artifact, route, validator, interaction, authority, control, or stopping decision. Do not perform a tour of theories.

## Admit a Lens by Decision Value

A lens is useful only when the design has a live uncertainty, a baseline position, an unclear mechanism, and evidence that could discriminate the lens's predicted design difference. These are admissibility considerations, not a preliminary procedure or required record.

Theory may produce a hypothesis, explanation, counterexample, or test. It is not evidence that the mechanism holds in this project. A source found after a decision may explain the decision but does not retroactively strengthen its evidential basis.

Remove a lens when it changes no engineering decision, acceptance evidence, or reopening condition.

## When the Target State Is Unclear

**Trigger:** the proposal starts with models, Agents, prompts, tools, or stages but cannot state the intended change or minimum success evidence.

Possible questions:

- What initial state should become what target state?
- For whom, under what conditions, and with what observable success?
- Which constraints are intrinsic, authoritative requirements, current technical limits, unverified assumptions, or preferences?
- What is the smallest system that could produce useful value and support justified correction?

Possible design moves include clarifying the state transformation, non-goals, assumptions, minimum trustworthy loop, and deferred formalization; or removing components that contribute neither value nor a required control.

Evidence can come from a narrower baseline, representative use, or a test showing whether removing a component causes an observable product or control failure.

This check is informed by first-principles reasoning, but the result is an engineering boundary rather than a philosophical essay.

## When Meaning May Be Lost in Transformation

**Trigger:** sources are summarized, translated, projected, reformatted, personalized, merged, or converted into machine structures.

Possible questions:

- Which decision-relevant information must survive each boundary?
- Which transformation is intentionally lossy?
- Where can ambiguity, noise, or stale context enter?
- Which artifact owns semantic intent, evidence, decision, or delivery truth?
- Can a consumer detect missing, uncertain, or outdated context?

Possible design moves include distinguishing canonical and derived authority, preserving provenance and context, marking uncertainty and excluded information, binding dependency freshness, and defining invalidation, regeneration, and correction direction.

Useful evidence compares source and result on information that affects decisions, tests lineage after upstream change, and observes whether downstream consumers detect incompleteness. A field-for-field match is not sufficient if the representation changes meaning or hides uncertainty.

This lens uses information-preservation ideas; it does not require calculating entropy.

## When the Process Cannot Observe or Correct Itself

**Trigger:** quality language is vague, validation measures an easy proxy, retries repeat unchanged, or feedback cannot reach an owning decision.

Possible questions:

- What observable state is the design trying to regulate?
- Does the validator measure the claim or merely a convenient proxy?
- Which action can correct each detected deviation?
- Where should the failure return?
- What information gain would justify another attempt?
- What evidence supports stopping, reopening, or maintaining the current disposition?

Possible design moves include a local trustworthy loop, explicit criterion and disposition, local route-back, information-gain retry, stale-evidence handling, and a version-bound validation receipt.

Useful evidence includes seeded defects, representative traces, route-back tests, stale-dependency tests, and correction under realistic failure. More feedback or more iterations can destabilize a process when the signal is delayed, noisy, conflicting, or attached to the wrong action.

Control theory is useful here only insofar as it produces local control choices; it does not justify one universal state machine.

## When Human Attention Must Be Allocated

**Trigger:** human judgment is costly, review volume is high, equal intervention is infeasible, or the value of another review is uncertain.

Possible questions:

- What information, expertise, context, standpoint, or authority does a person add?
- Which errors have high consequence, irreversibility, novelty, evidence conflict, or blast radius?
- Which obligations require review regardless of confidence?
- What random exploration could reveal confident unknown failures?
- What are review capacity and opportunity cost?

Possible design moves include locally prioritizing uncertainty, consequence, irreversibility, novelty, and evidence conflict; combining targeted review with random sampling; and defining capacity, escalation, and narrower safe defaults.

Evidence may include defect detection, judgment shift, queue load, correction rate, missed harms, and comparison with the better solo performer. Do not convert these factors into a universal score. Human involvement can have negative value when it adds no independent information or authority.

## When the Interface May Distort Judgment

**Trigger:** reviewers see model-selected evidence, rankings, confidence, polished drafts, visual comparisons, or time-pressured queues.

Possible questions:

- Does the interface anchor a person before independent judgment?
- Can they inspect original evidence and missing coverage?
- Are alternatives presented neutrally?
- Can they disagree, pause, request evidence, narrow scope, or exercise an accessible veto?
- Is the task feasible under actual ability, language, bandwidth, and time conditions?

Possible design moves include independent-first or source-first review, blind comparison, explicit counterevidence, accessible diffs, layered context, adjustable timing, and clear authority and no-response effects.

Useful evidence compares decisions with and without model exposure, uses seeded defects, tests accessible task completion, and observes disagreement quality and workload. Override counts and time-on-screen do not establish effective review.

## When Incentives or Interests Can Corrupt a Gate

**Trigger:** the producer benefits from passing, reviewers are rewarded for throughput, affected parties lack recourse, or evidence and metrics can be selected strategically.

Possible questions:

- Who benefits from each disposition and who bears errors or review burden?
- Can a participant hide failure, choose the easiest metric, or pressure a reviewer?
- Does the evaluator depend on the producer's framing, evidence, or model?
- Can an affected person contest and reverse the decision?

Possible design moves include producer-evaluator separation, blind or held-out evaluation, source-selection audit, conflict-of-interest controls, non-retaliation, appeal, and control-effectiveness measurement.

Useful evidence includes bypass tests, held-out performance, appeal reversals, disagreement traces, and comparison of reported with independently observed quality. Not every collaboration is adversarial; add mechanism controls only where incentives or authority plausibly distort behavior.

## When Long-Term Operation and Ownership Are Unclear

**Trigger:** the system is continuous, crosses teams or institutions, relies on recurring labor, or needs correction after release.

Possible questions:

- Who owns freshness, dependencies, policy changes, incidents, corrections, and retirement?
- What response time is realistic and resourced?
- Who can pause, retract, restore, and notify?
- Whose hidden labor or knowledge sustains the system?
- How are contribution, privacy, attribution, consent, and remedy handled?

Possible design moves include assigning owners with actual authority and resources; defining maintenance, handoffs, correction, retraction, communication, labor protections, and retirement conditions.

Useful evidence comes from operational traces, queues, incidents, dependency updates, staffing coverage, correction completion, and affected-party feedback. Naming an owner without authority, resources, or remedy capability is responsibility laundering.

## Preserve What the Lens Changed

When a lens changes a consequential decision, preserve in a locally useful form:

- the live uncertainty and baseline position;
- the mechanism hypothesis and its applicability limit;
- the changed design choice or evidence requirement;
- observations that would support, overturn, reopen, or retire it;
- the affected scope and next owner.

This is continuation meaning, not a required Theory-to-Decision template. Keep one primary engineering owner for the problem; additional lenses may add a distinct prediction or test but should not create parallel reports.

Repeated usefulness across heterogeneous cases may justify promoting a lens or example. One unusual case normally remains local. Repeated irrelevance, non-discriminating predictions, or explanation without decision change is evidence to narrow or retire the lens.
