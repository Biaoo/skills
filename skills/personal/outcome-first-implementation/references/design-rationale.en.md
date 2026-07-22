# Should Engineering Complexity Still Be a Core Consideration in Agentic Coding?

My answer is no, at least not with the same meaning and weight it had in conventional software development.

Agentic Coding has changed the basic division of development work. Much of the coding, technical learning, solution exploration, and repeated revision once performed by human engineers can now be delegated to an agent. Both implementation capacity and implementation cost have changed structurally.

Yet I have found that the technical choices and broader trade-offs agents make have not fully caught up with this change in development paradigm.

## Implementation Has Entered a New Paradigm; Trade-Offs Have Not

In one project, I asked AI to implement a frontend animation. It proposed several technical routes and compared them much like an experienced human engineer would: by code volume, implementation difficulty, familiarity, and maintenance cost. It clearly favored a route that was easier and required less work but was also more conservative in visual quality.

I replied:

> Do not factor technical or implementation complexity into this choice. The technology stack is open; treat frontend visual quality as the primary objective.

I was explicitly telling the agent not to bring its own implementation workload into this visual decision.

That exchange made a mismatch visible. The execution model had entered Agentic Coding, while solution selection still followed engineering habits inherited from the previous development paradigm.

The agent still treated how much code it would need to write, whether the technology was familiar, and whether the implementation path was short as major constraints. It still defaulted to KISS, incremental development, and MVP scope. It still reduced the objective or chose a more conservative result to save implementation work.

## What the Old Engineering Habits Were Pricing

Those habits made sense in conventional software development.

Humans wrote the code, learned the technology, and spent finite time and attention debugging it. A more difficult implementation meant a longer schedule, greater coordination cost, and more work that might never be completed. Engineering complexity therefore described more than the technology itself: it also priced scarce human labor, time, attention, and learning capacity.

KISS, incremental development, and MVPs often emerged from those resource conditions. They did not only keep systems simple; they also reduced how much work a human team had to perform directly.

Agentic Coding changes that premise. When an agent performs most of the implementation, writing hundreds more lines, trying several routes, or using technology unfamiliar to a human engineer no longer maps automatically to the same labor cost.

If an agent continues to weight those factors as before, it is applying a human-engineering cost model to its own execution work. It then brings that unrequested cost into solution selection and lowers the objective on my behalf.

This is the cost-model mismatch I see:

> Implementation capacity has become agentic, while solution selection remains centered on human engineering hours.

## The Paradigm Shift Is More Than Faster Coding

Agentic Coding does not merely make the same engineer faster. It changes where the human sits in the development process.

Previously, I had to decide both what I wanted and whether I or my team could afford to build it. Objective design and implementation budget were entangled in the same decision.

Now I can concentrate more of my attention on the objective, experience, boundaries, and acceptance criteria while delegating solution search and implementation to the agent. I no longer need to reduce the objective in advance merely because the agent must write more code, attempt several approaches, or use unfamiliar technology.

This creates a clear decision principle: when substantially more agent implementation work can produce a materially better result, the better result should take priority. Work borne only by the agent should not become a product constraint by default.

## Engineering Complexity Must Be Split Apart

The question is therefore not whether to keep or discard engineering complexity as a consideration. The problem is treating it as one indivisible cost.

Some complexity does not propagate into the final result: the agent may search more routes, generate and rewrite intermediate implementations, use tools unfamiliar to human engineers, or perform more rounds of revision. As long as that work does not change a user-relevant outcome, the agent should absorb it internally.

Other complexity persists in the resulting system. It changes runtime performance, verification difficulty, user experience, integration, security, reversibility, or long-term evolution. These are not questions of implementer effort; they change the result itself and therefore still belong in solution selection.

Agentic Coding reprices the first kind of complexity. It does not remove the consequences of the second.

This also changes the role of KISS and MVPs. Simplicity should not become the default objective before outcomes are compared; it should decide between routes whose results are materially equivalent. An MVP should not be used to reduce the agent's implementation work; it should be an information-gathering instrument when requirements, aesthetic direction, technical assumptions, or risk need validation.

## Why I Created This Skill

I created `outcome-first-implementation` to override this default cost model that no longer fits Agentic Coding.

The Skill requires an agent to optimize first for the result I explicitly declare, not for implementer convenience. Complexity borne only by the agent and not propagated into the result should be absorbed by the agent. Complexity that materially changes the result can then enter the trade-off in which I need to participate.

For me, this is not a special instruction for one frontend animation. It is how collaboration in Agentic Coding should work:

> Do not price the agent's own execution work as traditional human engineering labor, and do not replace the result I actually want with one that is merely easier to implement unless I ask for that trade-off.
