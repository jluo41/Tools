## 0.9.0 — 2026-08-19

- **0.9.0 shipped in SKILL.md with no entry here.** Reconstructed from the
  frontmatter: Aims joined the authority test and now live in the plan file, and
  the version rule was stated as protecting a PROMISE and never a FORMAT — so an
  old-grammar plan is rewritten on its next pass rather than frozen, and
  `checks/outline.py` fails `bullet-missing-note`. Recorded 260822 in a
  version-vs-changelog sweep.

## 0.8.0 — 2026-08-20

- **The fold marks self-referential values `· recount`** (JL: "看看哪里可以去
  优化"): a value counting the run's own artifacts (receipts, findings, a
  pinned hash) drifts as phases append, so its `Answered:` line carries the
  mark and DRAFT re-reads only those cards (haipipe-page-draft §📖).
- **A head or Note states the PRESENT, never the past** (JL: "content 永远
  只包含最新的东西"): a renumber or reversal rewrites the bullet clean; the
  old state lives in `## Log` and receipts, never beside the new one.

## 0.7.0 — 2026-08-19

- **The version rule protects a PROMISE, never a FORMAT** (JL: "remove all
  the legacy-grammar, I don't want to maintain the old things"): an
  old-grammar plan is rewritten into the current grammar on its next OUTLINE
  pass — in place while unapproved, as `v<N+1>` when ticked. Found on
  `QC1-visitlbp`: a fold pass appended onto 260817 long-sentence bullets and
  every check stayed green, so `checks/outline.py` now FAILS
  `bullet-missing-note` on any bullet lacking its `Note:`/`Answered:`/`Drawn:`
  line, every plan, no legacy carve-out.
- **The Aims enter the authority test**: agreed at OUTLINE, living in the
  plan file with `Done when:` tests (haipipe-plugin-outline 0.14.0 owns the
  grammar); plus a pointer to the plugin's §✂️ bullet grammar, stated once
  there.

## 0.6.0 — 2026-08-19

- **有问有答: an answered ask is appended in place** — when a 📮 bullet's card
  lands its `## Values`, the same bullet gains the answer with each value id
  quoted inline; no new bullet, mark stays. Landing values obliges the next ①
  fold to write the append (`haipipe-page-evidence` 0.11.0 carries the
  producing side of the same rule).
- **The same night's extensions**: 🖼 bullets gain `Drawn: <claim>` once their
  unit is built, transcribed from the unit's README; and the tick's meaning is
  BREAK-not-bless — the person hunts for what is wrong, and the tick records
  that the hunt failed.
- **Coherence sweep (260819)**: §🔀 routes the four-pass plan through the
  🧑 LOOK before ② PROBE and ③ EVIDENCE run; §🕳's example heads are
  Capitalized per the plugin's §✂️ bullet style; §📦 counts five marks, not
  six (✅ retired).

## 0.5.0 — 2026-08-19

- **COVERAGE (§🚦 test ①) now runs BOTH directions of the plan⇄disk join**
  (JL, on seeing Display4 under "on disk, cited by no bullet": "you should try
  to make every display to be used", and when its README back-pointer was
  offered as the fix: "you should cite it"): every display unit on disk must
  be CITED BY A BULLET'S MARK — a `serves:` line inside the unit's README is
  not citing, because the plan's reader never sees it. A README may carry a
  `retired:` line to take the unit out of the plan deliberately.

## 0.4.0 — 2026-08-19

- **📮 probe and 🧮 value are now SEPARATE marks** (JL: "You mean you put the
  probe and values together? I want to separate them"). 📮 = this point needs
  a QUESTION answered — bare before ② raises the card, `📮 PP<NN>` after; the
  answer may be a finding or a folder of numbers. 🧮 = this point QUOTES one
  value, `PP<NN>.v<n>`, out of an answered card's `## Values` block, and
  `checks/values.py` re-computes it. 📮 deliberately shares phase ②'s glyph
  (same concept) and is end-anchored in the scanners so prose about the phase
  never reads as a mark.

## 0.3.1 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.

## 0.3.0 — 2026-08-19

- **OUTLINE is now the head of a PREPARE loop.** JL 260819: "outline 之后就直接
  probe 准备证据，基于证据我们再改 outline，直到 outline 自己是自洽的." OUTLINE →
  PROBE → EVIDENCE repeats, and only the plan's own gate lets DRAFT start.
- **Self-consistent is FOUR checkable things**: coverage, address, value, shape.
  All four run before the person is asked, so the human tick answers direction
  rather than arithmetic.
- **A tick belongs to the version it ticked.** Evidence that changes an approved
  plan makes a `v<N+1>`. On 260819 the tick stayed on `v2` through five more
  edits, and all three stale `serves:` addresses came from that.

## 0.2.0 — 2026-08-19

- **The Page Type's `outline:` block is now READ.** All eleven surviving types
  already declared a mode (`fixed` | `grammar` | `resolved`) under `metadata:`,
  and nothing in this phase looked at it, so a plan's shape was whatever its
  author felt like.
- OUTLINE now has TWO exits, and the machine one runs first: the plan's shape must
  match the declared mode, THEN a person ticks `approved:`. A plan that
  contradicts its own type wastes the one gate that is supposed to be cheap.
- `checks/outline.py` owes a `plan-shape-off-type` rule.
- No `page-type:` key stays the flexible default: base section order only, which
  is 247 of 274 pages.

## 0.1.2 — 2026-08-18

- Pointer added to `../haipipe-page-workflow/ref/phase-cards.md` §①, which
  states this phase and every sibling in the SAME six fields
  (`❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`). This
  contract still owns the reasoning; the card is the readable-across-phases
  summary, and the contract wins when they disagree.
- Board backlink retargeted: `QPw7`/`QPw8`/`QPw9` became `QPw00a`/`QPw00r`/
  `QPw00g` when JL ruled that pages which are not phases may not carry
  phase numbers.


## 0.1.1 — 2026-08-18

Added the Board page backlink: the page that argues this contract, created 260818 when JL ruled one page per workflow step.
haipipe-page-outline · Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions
match SKILL.md frontmatter `version:`. Newest first.

## 0.1.0 — 2026-08-17

First contract. OUTLINE becomes phase ① of the page workflow (JL 260817:
"Outline 现在要成为这个 workflow 的一部分"), overturning
`haipipe-plugin-outline` 0.1.0, which had ruled in these words that *"the answer
to 'should there be an outline phase before DRAFT' is no."*

- The authority moves OUT of `haipipe-page-draft`, whose §🗂 had owned the
  outline. DRAFT keeps purpose, Aims and the page's own promise.
- The deliverable is `<page>/outline/<stem>-outline-v<N>.md`; its shape,
  addressing and marks stay in `haipipe-plugin-outline` and are not restated.
- The exit is a HUMAN GATE: a person ticks `approved:` on the 🧭 tab. No machine
  may write that tick.
- Before the tick the file is a working document: rewrite it, delete a wrong
  bullet, no version and no record. `v2` means the work MOVED ON, not that `v1`
  was wrong, which is why `v1` is kept rather than corrected.
- A named hole is the phase working: OUTLINE marks what a bullet owes and
  STOPS. Raising the card is PROBE's and landing it is EVIDENCE's.

**Why a phase and not a step**: one phase owning both "agree the shape" and
"write the page" let a single done-report cover both, and the plan was pasted
into the page's own `## Content`, where it went stale immediately
(`QC1-visitlbp`, CMSRegBoard, 260817). Changing a section list before the prose
costs one line; after the prose it costs the prose.
