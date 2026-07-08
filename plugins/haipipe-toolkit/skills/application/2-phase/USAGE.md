2-phase — how to use it (application)
======================================

Concrete recipes for the application phase engine (thin mirror of `../../paper/2-phase/USAGE.md`). You never invoke a phase worker directly: you run a **stage skill** from `1-lifecycle/` and it drives DRAFT → PROBE → REVISE internally, then stops at CHECK for you. Worker contracts live in each worker's SKILL.md; this page is a map. Paths below use a real bench intervention:

```
INT=examples/ProjApp-SMSDesign/applications/04_bench_timing_report
```

TL;DR
-----

```
1. /haipipe-application claims                 → stage skill runs DRAFT → PROBE → REVISE (automatic)
2. It stops at CHECK: checker output (check-probe-cards.sh + checks.sh) + probe flags
3. You reply in the stage doc as  > USER: …  threads, or decide: proceed / restart / accept / park
4. Ask to apply → the stage restarts the affected phase, re-runs everything downstream, re-CHECKs
5. Loop until the gate is green → explicit approval → Gate Ledger row → next stage
```

Same engine behind every stage: `seed | claims | venue | pitch | narrative | display | section-edit` — venue-GATED stages (narrative, display, section-edit) fire only if the pinned venue requires them.

A. Run a stage (the normal path)
---------------------------------

- **DRAFT** 🤖 — `haipipe-application-draft` settles structure + sentences in the stage doc (`$INT/0-lifecycle/<stage>/<stage>.md`); it may WebSearch as DRAFT-only scoping fuel and buffers `status: planned` PPNN skeletons in the stage's `_PROBE/` ("DRAFT may search; PROBE must dispatch"). Content decisions are negotiated with you here.
- **PROBE** 🤖 — `haipipe-application-probe` consumes the buffer: BOOKKEEP → DISPATCH (`Agent(haipipe-probe-orchestrator-agent)` per card) → TRANSLATE (venue-scaled harvest lanes, see `README.md`) → VERIFY (`check-probe-cards.sh`). Agent-only; nothing gates on you.
- **REVISE** 🤖 — `haipipe-application-revise` changes the text directly for venue + audience fit, leaving why-comments. No comment-first pause.
- **CHECK** 🧑 — `haipipe-application-check` re-runs the card checker + runs `checks.sh`, seeds `> CHECK:` threads in the STAGE DOC (artifact findings go to Gate Ledger notes), and presents the gate. This is where you come in.

B. Review a CHECK report
-------------------------

| You say | Meaning |
|---------|---------|
| proceed | stage done — explicit approval writes the Gate Ledger row |
| restart <phase> | rerun that phase and everything after it (recipe C) |
| accept with edits | reply in `> USER:` threads under the flagged lines, then ask to apply |
| park | leave the stage as-is, flags stay open |

Gate depth is venue-scaled (`../wiki/08-stage-gate.md`): simple venues (sms/push/reminder) confirm inline, complex venues (dashboard/report) get the full report — the explicit-approval rule never changes.

C. Restart a phase after CHECK feedback
----------------------------------------

Phase order is fixed (draft → probe → revise → check), so a restart re-runs the named phase **and everything downstream**. Restarting DRAFT reopens content decisions with you; PROBE/REVISE restarts run automatic and land back at CHECK.

D. The effort dial
-------------------

- **Light** — read the CHECK report, answer proceed/restart. Minutes per stage (the whole path, for simple venues).
- **Medium** — thread `> USER:` comments on specific lines in the stage doc, ask to apply.
- **Heavy** — reopen DRAFT, renegotiate the stage contract, run multiple CHECK rounds (complex venues).

E. Boundaries (always true)
----------------------------

- DRAFT is the only phase that negotiates content with you; PROBE and REVISE never wait on a human.
- No number is invented and no inline search happens in PROBE — evidence dispatches through the gateway per PP card, and you verify in CHECK.
- Unresolved `> USER:` threads keep a stage open; silence is not consent.
- `> CHECK:` threads live in stage docs only; `0-artifacts/*.md` stay clean — artifact findings land in the Gate Ledger notes column.
