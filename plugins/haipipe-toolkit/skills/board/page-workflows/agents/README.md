# The six producers, one per phase

One agent per phase since 260819, the same day each display unit got one.
`haipipe-page-creator-agent` (plugin root `agents/`) is the shared BASE: the
packet shape, the procedure, the house rules and the return contract live there
and only there. These five bind `phase` and name the skill chain, nothing more.

    ① haipipe-page-outline-agent    also the PREPARE fold-back (workflow §🧭)
    ② haipipe-page-probe-agent
    ③ haipipe-page-evidence-agent   display lane fans out via
                                    haipipe-display-unit-agent (caller dispatches)
    ④ haipipe-page-draft-agent
    ⑤ haipipe-page-revise-agent     ⑥ COMPILE folded in
    ⑦ haipipe-page-check-agent      read-only judge of ONE page version;
                                    base + whole-board reviews stay with
                                    haipipe-board-reviewer-agent

## Stand-in rule

Agent types register at session start, so a type added or renamed mid-session
is not dispatchable by name until a new session. The caller then dispatches a
general-purpose stand-in whose FIRST action is to read this folder's agent
file as its identity, plus
`../haipipe-page-workflow/ref/producer-contract.md`. The receipt's `actor`
names the ROLE (the agent file's `name:`), not the stand-in. The 260819 run
used exactly this pattern.
