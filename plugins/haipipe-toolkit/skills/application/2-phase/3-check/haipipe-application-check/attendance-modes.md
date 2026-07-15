Attendance Modes — Who Clicks "Accept" at Each CHECK
======================================================

The CHECK phase pauses for a decision. `--unattended[=Ns]` controls how
long that pause lasts and whether a human is expected. With no flag,
CHECK is attended (copilot default).

ONLY applies to the application-side CHECK phase. HARSH gates upstream
(e.g. task CODE_REVIEW) do not auto-accept under any timeout.


Three modes
============

| Value     | Mode             | Behavior at every gate                                     |
|-----------|------------------|------------------------------------------------------------|
| `null`    | 🧑 attended      | Wait indefinitely for a human reply (A/B/C/D/E).           |
| `N > 0`   | ⏳ timed         | Print proposal + countdown; wait up to N seconds; if no    |
|           |                  | reply, auto-accept the proposal verbatim (= reply A).      |
| `0`       | 🤖 unattended    | No wait. Auto-accept the proposal immediately.             |

`null` (attended) is the default for new sessions.


Reply vocabulary at each gate
==============================

A human reply is one of:

```
A   accept gate's recommendation (apply proposed outcome verbatim)
B   override with own feedback string → outcome = revise [feedback]
C   approve as-is (force approve regardless of proposal)
D   done / jump to report (valid only at late gates — see HARSH rules)
E   cancel session
```

Auto-accept is equivalent to reply A.


Banner statuses
================

```
🧑 attended      "awaiting"                      → "approved" / "revise→plan" / "done"
⏳ timed         "awaiting (auto in {N}s)"       → above OR "auto-accepted" when timer fires
🤖 unattended    "auto-accepted"                 (no awaiting state)
```


Auto-accept rules (cannot be bypassed)
========================================

Auto-accept applies the gate's proposal **verbatim**. The gate's own
rules still hold:

```
- `done` outcome valid only at late gates (G-post and equivalents)
  Auto-accepting a `done` proposal at an early gate is still rejected
  by the orchestrator with the same message a human would see.

- MAX_REVISIONS = 3 still fires. An auto-accepted `revise` past the
  cap triggers the force-approve audit trail (gate file gets a
  **FORCED APPROVAL** banner; gates[] entry records original_outcome).

- HARSH gates upstream (task CODE_REVIEW, probe review)
  never auto-accept. They block until met. If a SOFT gate sits
  in front of a HARSH gate, the SOFT gate can auto-accept but the
  HARSH one will still block.
```


Audit banners
==============

Auto-accepted gate files include a banner at the top:

```
**AUTO-ACCEPTED** (mode: timed, timeout: 60s, fired at 2026-05-25T14:32:01)
```

The proposal itself is unchanged — only the auto-accept fact is
recorded: the Gate Ledger row's `By` column reads `persona:<preset>`
and its Notes carry `auto-accepted (timed, 60s)`.


CLI flags
==========

```
--unattended           equivalent to --unattended=0  (🤖 immediate)
--unattended=30s       30-second timer per gate       (⏳ timed)
--unattended=300s      5-minute timer per gate        (⏳ timed)
(omitted)              attended; gate waits forever   (🧑 default)

Legacy: --auto         alias for --unattended=0
```


When to use which
==================

```
🧑 attended      You're driving an exploratory question and want every
                 phase boundary in front of you.
                 → Most interactive sessions.

⏳ timed         You're running stage work in the background but want
                 the option to intervene.
                 → "Advance the lifecycle while I'm in another meeting;
                    auto-accept if I haven't responded in 5 minutes."

🤖 unattended    You're certain the persona is tuned right and want
                 zero pauses (e.g. batch-advancing several interventions).
```


Default
========

With no flag: attended (CHECK waits for the human). The deprecated
`--auto` flag is accepted as an alias for `--unattended=0`.
