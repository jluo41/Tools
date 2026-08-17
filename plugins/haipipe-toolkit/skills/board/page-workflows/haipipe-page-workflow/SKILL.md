---
name: haipipe-page-workflow
description: >-
  The RUN router of the page family: the head skill of page-workflows/, combining OUTLINE, DRAFT, PROBE, EVIDENCE, REVISE, COMPILE, and CHECK into one bounded, auditable, non-linear loop over ONE Board Page. It owns the raw-material packet, the phase receipt written under <board>/_runs/page/, the producer/judge role separation, and the stop rules; the sibling contracts own their phases, haipipe-page owns what a page IS, and haipipe-board owns the executable machinery. RUN is deliberately not ADVANCE: a Page may repeat a phase, branch, HOLD, or return to DRAFT in a new round, and only CHECK may CLOSE. Use when one Page must be driven through the automatic loop, when a run receipt must be audited, or when a workflow surface needs the page lifecycle's one authoritative state source. Trigger: run a page, run page lifecycle, automatic page loop, audit page workflow, page run receipt, RUN router, DERC, DPRC, page workflow head, /haipipe-page-workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-17"
  summary: "The lifecycle now names the Point-to-sentence-to-evidence handoff: DRAFT writes scaffolds, PROBE performs PageX/MATCH, EVIDENCE lands the bundle, and REVISE realizes the final prose."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-workflow · the phases, combined into one auditable RUN

`haipipe-page` is the door for ONE PAGE and says what a page IS.
This skill is the head of the page WORKFLOW: it drives one existing Page through the phases as a bounded loop and leaves a receipt.
It moved here from `haipipe-page`'s RUN verb on 260815, so the workflow pattern reads the same in every family: one folder, one head skill, its member skills beside it.

**Who owns what**:

```
haipipe-page               what a page IS · CREATE · WORK ON
haipipe-page-workflow      RUN · the packet · the receipt · the stop rules
page-workflows/ members    each phase's own authority
haipipe-board              the machinery this skill calls, never contains
```

## 🔁 The shape of the loop

**The routing grammar**: authority-selected, never a conveyor belt.

```
🧭 OUTLINE ─▶ ✏️ DRAFT ─▶ 📮 PROBE ─▶ 🃏 EVIDENCE ─▶ 🖊 REVISE ─▶ 📄 COMPILE ─▶ ✅ CHECK ─▶ CLOSE
   🚧gate       │           (skippable)   ⚖️count       │            │            │
   ▲            │                                       │            │            │
   └────────────┴───── CHECK routes back to any of them ┴────────────┴────────────┘

   the shape     the promise   ask the bank   land the cards   write it   build it   judge it
   🧭 tab, a     purpose ·     Q → QA file    📚 🔢 🖼 lanes    cite each  latex ·    the BUILT
   person says   Aims · what                  in parallel      by id      pdf · word artifact
   yes           each division
                 must establish
```

Each phase may repeat, PROBE is skipped when the Page promises no claim it cannot already support, and CHECK may route back to any earlier phase.
Which phase runs next is decided by AUTHORITY (`haipipe-page`'s authority test), not by position, which is why the verb is RUN and not ADVANCE.

**Seven members** (JL 260817, splitting the four; the three merges are named below):

```
phase       authority                                          load
────────────────────────────────────────────────────────────────────────────────
OUTLINE 🚧  writes <page>/outline/<stem>-outline-v<N>.md, the    ../haipipe-page-outline
            plan down to the POINT and its obligations, each     (the file's shape is
            bullet marked
            🎯aim ✅have ​📚cite 🔢value 🖼display 🧮proof ·       haipipe-plugin-outline §📐)
            exits ONLY on a person ticking `approved:`
 DRAFT       define purpose + Aims; instantiate each Point as   ../haipipe-page-draft
            one or more sentence scaffolds with visible holes
 PROBE       run PageX/MATCH before new work; turn each          ../haipipe-page-probe
            🔢 mark into probe/PP<NN>-<slug>/, write its
            `serves:` backlink, dispatch the stripped question
 EVIDENCE ⚖️ land answer/proof, citation, and frozen Display      ../haipipe-page-evidence
            intake; expose the derived Evidence Bundle
 REVISE      realize the scaffolds as final prose, cite landed   ../haipipe-page-revise
            cards by id, render/select/build Display units
 COMPILE     rebuild latex · pdf · word from that prose          ../haipipe-page-revise
                                                                 (until split out)
CHECK       judge the BUILT version and route its authority     ../haipipe-page-check
```

**Why each split, and every one is a real 260817 failure, not a theory:**

```
was            became             the failure it allowed
──────────────────────────────────────────────────────────────────────────────
DRAFT          OUTLINE + DRAFT    one phase agreed the shape AND wrote the page,
                                  so the outline table got pasted into ## Content
EVIDENCE       PROBE + EVIDENCE   raising a card and landing it counted as one
                                  act, so four cards sat `raised`, bound to a
                                  QA bank that did not exist, and it read as done
REVISE         REVISE + COMPILE   "the prose is right" was reported as done while
                                  the PDF carried raw <!-- --> and literal **
```

## 🃏 One hole, five phases, and only ONE of them opens a file

The commonest question about this loop is where an evidence card is born, and
until 260817 three member skills answered it three different ways. One rule now,
and it reads down the loop:

```text
① OUTLINE   the MARK      `- B4 · the four coordinates    🔢`   nothing on disk
② DRAFT     the AIM +     sentence scaffold with `<VALUE HOLE>` and its
            SCAFFOLD      Aim/State owner; no card yet
③ PROBE     the CARD      PageX/MATCH → probe/PP<NN>-<slug>/ · serves: C4.P1.B4
④ EVIDENCE  the ANSWER    target: <QA path> · proof/ pulled · bundle ready
⑤ REVISE    the SENTENCE  replaces holes and cites the card by id
```

**Why the file waits until ③.** A plan is rejectable in ten seconds and must
leave nothing behind, so ① may not; the mark IS the proposal, so a card at ②
would be a second copy of it (§🪞 below). The deciding reason is the STAKE: a
card's `consumer/` side carries what the page loses, that is an Aim, and Aims are
written at ②. ③ is the first phase where a complete card can exist.

**The display unit is the one exception, and it goes LATER, not earlier.** Its
`intake/` freezes FROM a `proof/` that does not exist until an answer does, so
④ EVIDENCE creates it. Declaring a unit that nothing can fill yet is how a page
shipped "1 display declared · 0 unit folders on disk" (260817).

**⚖️ EVIDENCE is three LANES, not three steps.** They run at once, each with its own hand and its own exit test; the phase ends when all three pass, and no lane waits on another. The result is a derived Evidence Bundle keyed by the Point, not a fourth storage plugin.

```
lane          hand        exit test
──────────────────────────────────────────────────────────────────────────────
📚 citation   a person    the bib key is landed AND a person marked it verified
🔢 value      the bank    binding names a real QA file AND probe/<id>/answer/
                          holds its extract  🚫 `answered` with an empty proof/
🖼 display    a person/   intake/ frozen from that answer/ AND a renderer
              machine     is named; rendering and selection belong to REVISE
```

⚠️ **The display lane freezes inputs here, then realizes them in REVISE.** QPf5's five-step walk splits across the phases: ① INTAKE is EVIDENCE's, ② RENDER and ③ PICK are REVISE's, ④ BUILD is REVISE/COMPILE's, and ⑤ ACCEPT is CHECK's. A plan carries only the bare `🖼 owed` mark until EVIDENCE has a Probe `proof/` from which to freeze intake.

## 🪞 The page never writes prose about what a plugin already holds

Every phase can fail the same way, and on 260817 one page failed it three times in one session (`QC1-visitlbp`, CMSRegBoard). The failure is writing a SENTENCE where a THING belongs.

```text
what got written into the page body        what already held it        what happened
────────────────────────────────────────────────────────────────────────────────────
the DRAFT outline table, pasted into       🧭 the outline plugin,      two copies, and the
`## Content`                                which derives it from       body copy goes stale
                                            the ### headings            the next edit
"Evidence owed: probe/PP03-…, state        🚪 the probe surface,       the sentence carries a
raised."                                    which renders the card      `state:` the card owns
                                            and its live state          and will contradict
"evidence owed: 🖼 display"                 🖼 the display surface      🚨 ZERO units existed.
                                                                        The sentence WAS the
                                                                        whole deliverable.
```

**The rule.** A plugin owns a kind of material and a surface that shows it. The page's prose CITES that material by id and never restates it. `Display1` in a sentence is a citation; "a display is owed here" is prose pretending to be work.

**The rule that catches the third row, and it is the one that matters.** A phase may not report done while it DECLARED an artifact it did not CREATE. Declaring is free; the receipt must record the count.

```text
  ✅ 4 cards declared · 4 card.md on disk
  🚨 1 display declared · 0 unit folders on disk   ← the phase is NOT done
```

`haipipe-page-check` already rules that a declared unit which never rendered is a CHECK finding. That rule never fired here because CHECK never ran: the work was called done at DRAFT. So the count moves EARLIER, into every phase's own receipt, and a phase whose declared-versus-created counts disagree stops rather than reports.

**And the third failure of the same session, for the receipt to catch too**: verify the artifact the READER opens, not the one you just wrote. That session checked the built HTML and shipped a PDF full of raw `<!--` comments and literal `**`; checked `build.py`'s exit and served a page four minutes stale; and guessed at a CSP instead of opening the screenshot that showed the tab rail working perfectly. Wire green is not UI green (JL, standing rule).

## 🔁 run one Page lifecycle

RUN is the automatic, bounded loop. Use it when the process itself must be
exercised and audited, rather than when one known edit is enough.

1. Read `ref/page-run-contract.md` and assemble its raw-material packet. Resolve
   the Page Type from the filename. For a new Page, CREATE and register it first
   (that verb stays with `haipipe-page`), then start at DRAFT. For an existing
   Page with no known next authority, start at CHECK. Before each phase dispatch,
   materialize that phase's Related Board Pages packet with
   `haipipe-board/cli/pagecontext.py`; an invalid row or missing scope is a
   named HOLD, never omitted context.
2. Invoke `haipipe-board/ref/page-lifecycle.workflow.js` with the packet. The
   workflow dispatches a phase-scoped producer for OUTLINE, DRAFT, PROBE,
   EVIDENCE, REVISE, or COMPILE, a mechanical builder/version snapshot, and a
   fresh read-only reviewer for CHECK.
3. Follow returned routes rather than a prescribed order. Only CHECK may CLOSE.
   A route to DRAFT from another phase begins a new round only when purpose or an
   Aim reopened.
4. Stop at CLOSE, explicit HOLD, a missing input, a version mismatch, a required
   human gate, `max_steps`, or `max_rounds`. A limit stop means the run did not
   converge; it never means quality passed.
5. Write the exact Workflow result to
   `<board>/_runs/page/<page-id>/<run-id>.json`. Do not append the terminal CHECK
   result to the Page, because that would mutate the approved version.
6. Run `haipipe-board/cli/pageflow.py audit <receipt.json>`. Report the terminal
   route, checked version, traversed edges, deterministic finding count,
   semantic finding count, human-gate state, and residual risk.

RUN never lets one hidden pass write, judge, fix, and approve. The producer and
judge have different actor identities, and every changed version returns
through CHECK before CLOSE.

## 🧾 The receipt is the workflow's one state source

`<board>/_runs/page/<page-id>/<run-id>.json` is where a run's history lives, in the exact shape `ref/page-run-contract.md` fixes.
A surface that shows where a page stands in its lifecycle reads these receipts and nothing else, the same way the labeling stepper reads `## States`.
That surface ships: the 🪜 Workflow menu's `📄 Page phases` stepper (`haipipe-board/assets/js/10-drawer/65-plugin-pageflow.js`) draws the loop along the bottom of the split viewer, fed by `GET /_board/pageruns` (`live/pageruns.py`), which matches receipts by their own `page` field.
A page with no receipts is not an error: its next authority is the contract's own default, CHECK for an existing page, DRAFT for a new one, and the stepper states exactly that.

## 📂 Files

**This skill's own files**: what ships in the folder, and what each part is for.

```
haipipe-page-workflow/
├── SKILL.md            this contract
├── CHANGELOG.md        version history
└── ref/
    └── page-run-contract.md   the packet + receipt spec RUN and its members share
```

The executable machinery stays under `haipipe-board`: `ref/page-lifecycle.workflow.js` (the controller), `src/page_lifecycle.py` (the deterministic auditor), and `cli/pageflow.py` (the audit CLI).
The non-interactive dispatch target is `agents/haipipe-page-orchestrator-agent.md`, which invokes this contract in a fresh context.
