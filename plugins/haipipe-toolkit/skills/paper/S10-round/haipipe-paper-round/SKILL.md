---
name: haipipe-paper-round
description: "Manage dated paper work rounds as first-class Board S pages under `0-lifecycle/7-round/`. Subcommands enter|new|triage|apply|close open or resume an S-Round page, create the next page, turn discussion/review into its Items queue, route work, record applied history in its Log, and close it with an explicit receipt. No latest pointer or round sidecars. Trigger: paper round, work round, round todo, decisions, applied, latest round, open a round, triage review."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-07-26"
  summary: "Rounds are one-page Board work units: `0-lifecycle/7-round/S-Round-<n>-<vYYMMDD>.md`, with discussion, queue, decisions, applied history, and closing receipt on the same face. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-round
==========================

Rounds are paper working memory expressed in the same Board grammar as every
other lifecycle unit. One round equals one page:

```text
0-lifecycle/7-round/
├── S-Round-0-v260726.md
├── reviewer-letter-v260726.md   # optional received material beside its page
└── ...
```

There is no `latest.md`, `todo.md`, `decisions.md`, `discussion.md`, or
`applied.md`. Those would duplicate the S face and drift.

Page contract
-------------

Each `S-Round-<n>-<vYYMMDD>.md` uses the Board S-page structure:

- `state:` is `🔴`/`🟡` while work remains and `✅` only after close approval.
- `## Content` records source, purpose, accepted decisions, and applied summary.
- `## Items to Finish` is the only queue. Every item names its target.
- `## Discussion` holds raw discussion, anchored comments, and received-letter pointers.
- `## Where we are` is the current concise handoff.
- `## Log` holds dated triage/application events and the close receipt.

Triage routes
-------------

| Item | Target |
|---|---|
| claim unsupported / too strong | `0-lifecycle/1-work/S-Work-1-claims.md`, then that stage's PROBE |
| display missing / stale | DR row in `0-lifecycle/3-display/_DISPLAY_REQUEST.md` |
| paragraph placement unclear | owning `0-lifecycle/4-main/S-Main-*.md` page |
| appendix issue | owning `0-lifecycle/5-appendix/S-Appendix-*.md` page |
| wording / flow / style | owning S page, then its declared REVISE/CHECK sequence |
| citation / value evidence | owning Q-consumer, then that stage's PROBE collector route |
| reviewer response | `haipipe-paper-rebuttal` plus this S-Round page |

Subcommands
-----------

```text
/haipipe-paper round enter [paper-dir]
/haipipe-paper round new [paper-dir] [source/purpose]
/haipipe-paper round triage [paper-dir] [S-Round page]
/haipipe-paper round apply [paper-dir] [S-Round page]
/haipipe-paper round close [paper-dir] [S-Round page]
```

### enter

Read all `0-lifecycle/7-round/S-Round-*.md` pages. Derive the active round from
non-green state plus date/unit order; never read or create a stored pointer.
Show its source, `Where we are`, and open Items. Then open the paper Board at
that page.

### new

Confirm source/purpose if missing. Allocate the next unused numeric unit and
today's `vYYMMDD`; never overwrite an existing page. Create one S page with
real Question/Boundary/Content/Items/Where/Discussion/Log sections and rebuild
the Board. Received material is copied or linked beside the page only when the
user supplied it.

### triage

Read the page's Discussion and any received letters it names. Add accepted
decisions to Content and actionable work to Items, each with one target from
the table above. Triage does not execute the work.

### apply

Route each selected Item to its owning lifecycle stage. Evidence always enters
through that stage's Q-consumer and PROBE worker/collector chain. Record what
changed and which item it closes in this page's `## Log`; keep unresolved work
visible.

### close

Require every Item to be checked or explicitly parked with a reason. Present
the close summary and ask for approval. Only after approval set the first state
token to `✅` and append the gate receipt with actor/date to `## Log`.
No round pointer is updated.

Routing and return
------------------

```text
1. First token in {enter,new,triage,apply,close} -> that subcommand.
2. Else if a non-green S-Round page exists       -> enter.
3. Else                                          -> ask whether to create a new round.
```

Return the Paper closing block from `../../haipipe-paper/SKILL.md`, deep-linked
to the active S-Round page. Do not append a second Board status strip.
