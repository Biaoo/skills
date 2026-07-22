# How Documentation Slowly Becomes a Graveyard

In long-running projects maintained with agents, I keep seeing the same pattern. A project often begins with clean documentation. It tells anyone joining later what the system is, how it works, and which constraints matter.

Then the project encounters its first problem. The agent fixes the code and adds a sentence to the documentation: “Do not do this, because it once caused an error.” Later, an approach is abandoned, and the document gains an explanation of why the old solution should no longer be used. A misunderstanding is corrected, leaving another warning for future agents.

Every change looks reasonable in isolation. It preserves experience and appears to reduce the chance of recurrence. The problem emerges over time: new material keeps being appended while obsolete material is rarely rewritten or removed.

The system has healed, but the documentation still carries the scar.

## As the Tombstones Accumulate

When this style of maintenance continues, documentation begins to revolve around past problems. It records where something once failed, which approach died, what an earlier agent misunderstood, and what no one should ever try again.

I call this Tombstone Documentation. Each tombstone marks a resolved problem or an abandoned approach. As the markers accumulate, the living system is pushed into the background.

A later agent often cannot tell from the text alone whether those passages still apply today. A repair note becomes a current prohibition. An abandoned design continues to occupy space and attention. A warning written for a one-time misunderstanding becomes a lasting rule. To appear cautious, the next agent layers still more explanations and exceptions onto those old passages.

The agent reads more and more context while becoming less certain about what is still valid. I call this Contextual Entropy: accumulated context makes the signal of what is current harder to distinguish.

## Separating the Current Layer from History

Projects still need history. Architecture decisions, incident reviews, migrations, correction records, and version changes can retain long-term value.

Two decisions need to be separated: whether a piece of history is worth preserving, and whether it should be loaded into the agent's working context by default.

> Preservation is an archival decision; default loading is a collaboration decision.

The best cleanup is not periodic tombstone relocation. It is deciding at write time whether a passage states a current rule or merely records a repair that is already complete.

Living documentation should describe the system as it now stands: how it behaves, which decisions still hold, which constraints remain, and which questions are unresolved. When the system changes, the document should be rewritten with it rather than patched with another layer of explanation.

History worth preserving can be recorded separately in an ADR, postmortem, changelog, or migration record, or under a path such as `docs/history/`. These records should be consulted when needed, not loaded by default into every design or implementation task. If a historical reason still informs a current decision, a concise current rule or link is enough in the active document.

Not every correction deserves an archive entry. Text about a one-time misunderstanding, an expired warning, or obsolete material with no continuing value can simply be removed. A lesson that remains valid should become a current rule. Only records that support traceability, retrospectives, migrations, or future decisions need a historical home.

Collecting every mistake in a single `historical-errors.md` would merely rebuild the graveyard elsewhere. History should be retained according to purpose, not accumulated because deletion feels uncomfortable.

I now prefer the name `living-documentation` over a phrase such as “current truth.” I do not need a document to claim permanent correctness. I need it to evolve with the system: rewrite when reality changes, remove what has expired, and archive what remains useful.

That does not leave the project without memory. Active documentation stays clear, historical records preserve how the project got here, and the two are connected only when the work calls for it—not by inertia.

I want active documentation to help later contributors understand the system quickly and give agents the same clear starting point in future tasks. When someone needs to investigate an incident or understand an old decision, the relevant historical record should be easy to find. A new task should not have to cross a graveyard of past errors before reaching the living system.
