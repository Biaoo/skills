# Cognitive Probes: How Unease Becomes A Question

## Contents

- [Current Understanding](#current-understanding)
- [Where It Comes From](#where-it-comes-from)
- [What It Is Not](#what-it-is-not)
- [The Lifecycle Of A Probe](#the-lifecycle-of-a-probe)
- [Common Probe Clusters](#common-probe-clusters)
- [Relation To Upward And Downward Moves](#relation-to-upward-and-downward-moves)
- [Value In AI Collaboration](#value-in-ai-collaboration)
- [Risks](#risks)
- [Better Use](#better-use)
- [Open Questions](#open-questions)

When AI gives me an output, I do not always know immediately where the problem is.

Sometimes it looks like the task is done, the code runs, and the explanation is smooth. But I still feel uneasy: did it only complete the surface function? Did it drift away from my intent? Did it implement a requirement that should not exist in the first place? Is it following my idea instead of giving a real judgment?

At first, these uneasy signals are not systematic checks or stable dimensions. They are more like temporary questions that appear in the live thinking situation.

For now, I call these questions: cognitive probes.

## Current Understanding

A cognitive probe is a temporary follow-up question triggered by uncertainty.

Its role is not to produce a conclusion immediately, but to extend attention toward a possible direction of risk, gap, misalignment, or better possibility.

It usually does not appear in order, and it does not appear every time. A more realistic situation is: something makes me uneasy, and then a question appears.

```text
result uncertainty -> Did it actually work?
solution uncertainty -> Why did it do this?
intent uncertainty -> Is it aligned with what I meant?
standard uncertainty -> What counts as good here?
AI reliability uncertainty -> Is it analyzing objectively, or agreeing with me?
requirement uncertainty -> Is this a false need?
self-capability uncertainty -> Is there a gap in my judgment or knowledge structure?
```

These questions are not necessarily parallel or sequential. Sometimes they appear randomly. Sometimes they do not appear at all. What they share is not membership in one clean taxonomy, but the fact that each is responding to some uncertainty.

## Where It Comes From

Cognitive probes usually do not come from rational classification. They come from a pre-linguistic unease.

This unease may feel like:

```text
Something seems wrong.
Not quite.
Too smooth.
It looks done, but I do not feel settled.
Is this direction drifting?
Did this answer close the problem too early?
Is AI agreeing with me?
Have I also not thought this through?
```

These feelings are not yet questions. They are signals.

Only when I try to catch the signal does it become a question:

```text
Something seems wrong
-> Where exactly is it wrong?

Too smooth
-> Did it make a complex problem sound too complete?

Not settled
-> Did it actually solve the real problem?

AI may be agreeing with me
-> If I did not provide my preference, would it give a different judgment?

Maybe I have not thought clearly
-> Am I missing knowledge, experience, criteria, or expression?
```

So cognitive probes are not deduced from a complete theory. They grow out of uncertainty.

## What It Is Not

A cognitive probe is not a checklist.

A checklist is a pre-fixed inspection process. It is useful for stable, repeated tasks with clear boundaries.

A cognitive probe is triggered in the moment. It appears only when uncertainty shows up somewhere. It is not trying to cover every aspect. It is trying to probe a specific risk point.

A cognitive probe is also not a conclusion.

When I ask "Is this requirement false?", it does not mean the requirement is definitely false. It only means there is a risk here that needs to be probed.

A cognitive probe is also not a mature dimension.

A dimension is the later name for a family of probes. Only after probes repeatedly point in a certain direction may we call that direction result dimension, solution dimension, requirement dimension, intent dimension, or self-calibration dimension.

More precisely:

```text
A probe is a question that appears in the live situation.
A dimension is the later name for the landing point of probes.
A checklist is the process formed after things become stable.
```

If probes are organized into a dimension table or checklist too early, they may become prematurely fixed and lose their initial randomness, risk sensitivity, and live judgment.

## The Lifecycle Of A Probe

A cognitive probe roughly goes through this process:

```text
vague unease
-> a question appears
-> it points toward a risk direction
-> it forms a validation action
-> feedback arrives
-> stop / redirect / move upward / move downward
```

For example:

```text
vague unease:
This feature seems done, but I do not feel settled.

question:
Did it actually solve the real problem?

risk direction:
It may have only completed the surface requirement.

validation action:
Write a real use scenario and see whether this feature actually creates value.

feedback:
If the scenario holds, continue improving the implementation.
If the scenario does not hold, return to the requirement itself.
```

Another example:

```text
vague unease:
AI's solution looks reasonable, but I feel it may be following my preference.

question:
If my preference were ignored, would it recommend another approach?

risk direction:
AI may be agreeing with me instead of comparing objectively.

validation action:
Ask AI to argue for my approach, its approach, and a third approach, and list the failure conditions of each.

feedback:
If the costs of the three approaches become clear, then decide whether to adjust direction.
```

The value of a probe is not that it keeps asking forever. Its value is that it turns vague unease into a verifiable action.

## Common Probe Clusters

The following are not fixed categories. They are clusters of probes that often appear.

### Result Probes

When I am not sure whether AI actually completed the task, result probes appear.

```text
Was this feature implemented?
What effect did it achieve?
Is there an observable behavior change?
Is there a test or real scenario that proves it works?
Is it actually usable, or does it only look done?
```

### Solution Probes

When I am not sure whether the implementation path is reasonable, solution probes appear.

```text
What is the technical approach?
Why choose this route?
Is there a simpler, safer, more locally consistent approach?
What complexity did it introduce?
Is it solving the core problem, or taking a detour?
```

### Design Philosophy Probes

When I am not sure whether the principle behind the solution is right, design philosophy probes appear.

```text
What design principle does this solution express?
Does it favor fast delivery, long-term maintainability, simplicity, or abstraction and extension?
Is it consistent with the existing design philosophy of the system?
Does it increase clarity, or introduce hidden complexity?
Does it solve a local problem while damaging the long-term structure?
```

### Intent Alignment Probes

When I am not sure whether AI understood my real priority, intent alignment probes appear.

```text
Did it drift away from my expectation?
What is my first priority?
Is the current implementation aligned with what I wanted?
Where is the difference?
Is AI's solution better, or is my idea better?
Should I tell AI my design intent?
```

### Implicit Cognition Probes

When I realize that my dissatisfaction comes from some judgment I cannot yet express, implicit cognition probes appear.

```text
Why do I think this way?
Why do I feel this design is wrong?
What judgment criteria have I not expressed?
Do these judgments come from experience, values, system sense, or a knowledge gap?
Should I tell AI these implicit judgments?
If I tell AI, will it understand me better, or agree with me more easily?
```

### AI Reliability Probes

When I am not sure whether AI is analyzing objectively or following me, AI reliability probes appear.

```text
If I share my idea, will AI compare objectively or agree with me?
Is my input providing crucial constraints, or contaminating its judgment?
Can it point out where my solution is worse than its solution?
Is there a third approach that neither I nor AI has considered?
Is it doing real comparison, or producing analysis that only looks balanced?
```

### Requirement Reality Probes

When I am not sure whether the feature itself is worth building, requirement reality probes appear.

```text
What real problem is this feature meant to solve?
Is there a real use scenario?
What is the real loss if this feature is not built?
Was this requirement imagined?
Could this be a false need?
Am I mistaking the solution for the problem itself?
```

### Self-Calibration Probes

When AI's solution may be better than mine, or when I find that I cannot make a stable judgment, self-calibration probes appear.

```text
If AI's solution is better, where is my weakness?
Am I missing knowledge, experience, system design ability, abstraction ability, or expression ability?
Should my judgment criteria be made explicit?
Is my idea too local, too idealized, or missing context?
What is my current capability gap?
Can this gap be trained through ordinary methods?
```

## Relation To Upward And Downward Moves

Cognitive probes are related to upward and downward moves, but they should not be organized into a hierarchy too early.

An upward move is not simply standing in a higher place. It happens when the current direction of observation cannot explain the uncertainty, so a new direction is introduced.

For example:

```text
I first ask: Did the feature work?
But even if it worked, I still feel uneasy.
Then new probes appear:
Is this requirement valid?
Is this implementation consistent with the system's design philosophy?
Is AI simply following my preference?
```

This is not movement from low to high. It is risk perception forcing thought to switch coordinates.

A downward move means: the probe has located enough of the risk, so the complex judgment is compressed into a concrete action.

For example:

```text
The requirement may be false
-> write a real use scenario

The solution may drift away from the design philosophy
-> compare the current implementation against the design principles

AI may be agreeing with me
-> ask it to argue for my solution, its solution, and a third solution

I may be missing knowledge
-> identify which assumptions my current judgment depends on, and which assumptions need evidence
```

So upward and downward moves are not fixed routes. They are temporary interpretation and grounding moves formed after probes move among different uncertainties.

## Value In AI Collaboration

Cognitive probes let the person do more than accept AI's output. They allow the person to keep questioning around uncertainty.

Their value has several forms.

First, they help me avoid being carried away by AI fluency. AI can easily make an unfinished problem sound complete. A probe can reopen "looks complete" and ask whether it really holds.

Second, they help me detect whether AI and my intent have drifted apart. Often, AI completes the task as it understands it, not necessarily the problem I truly wanted to solve.

Third, they help me make implicit cognition explicit. When I feel "wrong," probes let me ask: where is it wrong? What am I relying on? Should these grounds be told to AI?

Fourth, they help me discover better possibilities. A probe is not only suspicion toward the current solution. It may open a third approach, a counterexample, a boundary condition, or a more reasonable design principle.

Fifth, they help me calibrate myself. AI output sometimes exposes gaps in my knowledge, judgment criteria, expression, or system design ability. Probes make these gaps visible.

## Risks

Cognitive probes also have risks.

First, excessive doubt. Every AI output can be questioned endlessly, making it impossible to accept any result.

Second, inability to stop. One probe can trigger another, moving from implementation to requirement reality, design philosophy, AI reliability, and self-capability gaps, until action becomes impossible.

Third, overcomplication. Some tasks only require result verification. They do not need to be lifted into system philosophy or personal capability structure.

Fourth, being overfit again by AI's polished classification. AI can easily turn these living probes into a clean dimension table, making it seem like a complete theory has been formed. That may erase their initial randomness, risk sensitivity, and live judgment.

Fifth, mistaking a probe for a conclusion. A probe only asks whether there is a problem. It does not prove that there is one.

## Better Use

The better approach is not to turn cognitive probes into a checklist. When uncertainty appears, ask:

```text
What exactly am I uneasy about?
What kind of risk does this unease point to?
What question do I need in order to probe it?
After probing it, how do I return to action?
```

A shorter loop is:

```text
unease
-> ask one question
-> do one validation
-> decide whether to continue, stop, redirect, or ground it
```

This keeps probes from becoming a rigid process or endless suspicion.

It preserves the liveness of thought while allowing the random questions that appear in conversation to gradually become reviewable, developable, and reusable cognitive assets.

## Open Questions

When should a probe continue, and when should it stop?

When multiple probes appear at the same time, how should the main risk be identified?

How can I give a probe to AI without making AI over-agree?

When probes repeatedly appear, when can they be stably named as dimensions?

Can a person's probe system be trained? If so, is the training about knowledge, experience, judgment criteria, or stopping ability?

How can I distinguish high-quality alertness from overcomplication?

How can I distinguish "my implicit cognition is warning me" from "I am just anxious because of uncertainty"?
