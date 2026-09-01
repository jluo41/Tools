# The five producers, one per phase, two cycles each

One agent per phase since 260819, the same day each display unit got one;
since 260901 a phase agent owns the two CYCLES of its phase
(`haipipe-page-workflow` §🔁: the OUTLINE part SHAPE · SURVEY · LAND · EMBED,
the DRAFT part WRITE · CHECK). `haipipe-page-creator-agent` (plugin root
`agents/`) is the shared BASE: the packet shape, the procedure, the house rules
and the return contract live there and only there. These bind `phase`, name
the skill chain, and nothing more.

    haipipe-page-outline-agent    SHAPE · SURVEY   the plan, then the item table
    haipipe-page-evidence-agent   LAND · EMBED     the runs, then the fold; display
                                                   lane fans out via
                                                   haipipe-display-unit-agent
                                                   (caller dispatches)
    haipipe-page-draft-agent      WRITE step 1
    haipipe-page-revise-agent     WRITE step 2     COMPILE folded in
    haipipe-page-check-agent      CHECK, and WRITE's pre-check; read-only judge
                                                   of ONE page version; base +
                                                   whole-board reviews stay with
                                                   haipipe-board-reviewer-agent
    _old/haipipe-page-probe-agent retired 260901: MATCH → SURVEY, dispatch → LAND

## Stand-in rule

Agent types register at session start, so a type added or renamed mid-session
is not dispatchable by name until a new session. The caller then dispatches a
general-purpose stand-in whose FIRST action is to read this folder's agent
file as its identity, plus
`../haipipe-page-workflow/ref/producer-contract.md`. The receipt's `actor`
names the ROLE (the agent file's `name:`), not the stand-in. The 260819 run
used exactly this pattern.
