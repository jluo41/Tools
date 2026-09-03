## 0.18.3 · 2026-09-03

- Include `new-job` in LAND's complete planned Supporting-route vocabulary.

## 0.18.2 · 2026-09-03

- Keep SURVEY inventory-only: it classifies existing, rerun, and new-design
  routes without allocating Tickets or `rNN` ids.
- Move allocation, Ticket scaffolding, and execution of planned Supporting and
  local Evidence Item Runs into LAND.

## 0.18.1 · 2026-09-03

- Clarify that VALUE, CITE, and DISPLAY are Result types rather than copy
  directories; real payloads stay at their local or Supporting Result paths.

## 0.18.0 · 2026-09-03

- Load typed evidence authority from the Outline skill and keep all material
  lanes under `outline/evidence/`.
- Forbid recreating a root Evidence category or standalone Evidence tab; actual
  local execution remains in sibling `runs/` and `results/` folders.

## 0.16.0 · 2026-09-02

- LAND now validates every SURVEY-selected PageX binding beside the declared
  Supporting Results before freezing one Local Input and executing exactly one
  local Page Evidence Item Run.
- Define PageX as an exact accepted cross-Folder source authority, not a Run or
  fourth Result type. LAND closes only after supports, PageX bindings, the
  frozen input, and the accepted typed local Result are all valid.

## 0.15.1 · 2026-09-02

- Route CITE Evidence Item work to `haipipe-plugin-evidence`, which now owns
  citation/Bib authority.

## 0.15.0 · 2026-09-01

- LAND executes one dependency graph per typed Evidence Item: validate 0..N
  Supporting Results, freeze one local input, execute exactly one Page
  Evidence Item Run, and bind its ready Result. EMBED reads only that local
  Result. Discovery is a family; reuse/rerun/new-* are actions.

## 0.14.0 · 2026-09-01

- Owns the OUTLINE part's two machine-gated cycles: LAND (make every ☑ make
  row's run in the REAL tasks/ tree, fill the lanes, append ` → <result>` to
  the row; a card under evidence/probe/ only when a question leaves the page,
  with the stake wall and the one courier moved here from the retired
  haipipe-page-probe) and EMBED (write the numbers and their reading into
  plan v<N+1> as Answered:/Drawn:, fill never restructure, always back to
  SHAPE; `stale` reopens). The run-anchored law stated at the top.

## 0.13.2 · 2026-08-31

- Name the three canonical Folder-native lanes explicitly as
  `evidence/bibex/`, `evidence/probe/`, and `evidence/display/`.

## 0.13.1 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).


## 0.13.0 · 2026-08-31

Value lane: when the page has a collection job (`task/haipipe-task-for-page`),
④ POINT binds `target:` to its QA file and value rows copy from its
`values.yaml`; a refresh-run diff that drifts a bound value re-lands here and
is absorbed at OUTLINE.

## 0.12.0 — 2026-08-20

- **0.12.0 shipped in SKILL.md with no entry here.** Reconstructed from the
  frontmatter: EVIDENCE lands the bibex and display lanes plus Probe's QA
  returns, and its PageX branch is NOT its own — that lane already ran in
  OUTLINE. Recorded 260822 in a version-vs-changelog sweep.

## 0.11.0 — 2026-08-19

- **Landing `## Values` creates fold debt**: the asking bullet owes its answer,
  appended in place by the next ① fold with the value ids inline; this phase's
  return lists every landed card so the fold knows what owes what (JL 260819:
  "在 probe 回答问题之后，需要 evidence 去把这个问题给填上去").
- **Coherence sweep (260819)**: the receipt routes `EVIDENCE | OUTLINE | HOLD`
  (§🔀 already said → ① OUTLINE, always); §✍️ writes recipe/ and assets/ too,
  since RENDER · PICK · BUILD moved here; the exit is DRAWN and previewable,
  no longer "a named renderer"; §🖼's unclosed fence no longer swallows the
  §✍️ heading.

## 0.10.4 — 2026-08-19

- The kinds table names the plan's 📮 mark as what ② PROBE creates the value
  card from — 📮 probe and 🧮 value separated (JL: "I want to separate them").

## 0.10.3 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.

## 0.10.2 — 2026-08-19

- **The kinds table stopped saying a display is drawn in REVISE** — RENDER ·
  PICK · BUILD have been this phase's since 260819, and §🖼 twelve sections
  later already said so.
- **Stale numbers**: the loop line still read `OUTLINE · DRAFT · PROBE …`; the
  five-step table and the footer still numbered PROBE ③ and EVIDENCE ④. Found
  by the Display3 rebuild agent.

## 0.10.1 — 2026-08-19

- **§🔀's route table said `→ REVISE` and `→ DRAFT`**, contradicting §🔁 written the
  same day. Corrected: whatever comes back goes to ① OUTLINE. Found by the display
  agent rebuilding `QPw00-Display2`, which derived the route relation from the
  contracts and had to choose between two blocks in this one file.

## 0.10.0 — 2026-08-19

- **EVIDENCE routes back to ① OUTLINE, never forward to DRAFT.** An answer is not
  a confirmation: it goes to the plan, and the plan decides whether it still wants
  what it asked for (JL 260819).
- The PREPARE loop's exit is the plan's four checks: coverage, address, value,
  shape. Nothing in this phase may declare the loop finished.

## 0.9.0 — 2026-08-19

- **EVIDENCE stated as TWO stages, MAKE then BIND**, both inside the plugin
  folders (JL 260819). Neither touches the page's `## Content`: this phase
  changes what the page KNOWS and REVISE changes what it SAYS. A person's tick
  belongs to BIND, because it is what turns a made thing into a quotable one.
- **RENDER, PICK and BUILD move to EVIDENCE.** JL 260819: "这个不应该是 evidence
  里的这个 display 开始画图吗？REVISE 主要 work 还是 work 在这个 sentence 上面去".
  They sat in REVISE on the reasoning that a caption and a choice of rows are
  ARGUMENT. That was right about the caption and wrong about the drawing, and
  the asymmetry it produced is what exposed it: a citation lane returned a bib
  key, a value lane returned a bound number, and the display lane returned an
  unrendered intake folder. Two of three landed something a page could use.
  A lane that performs one step out of five is not a lane.
- REVISE keeps the argument half: the sentence that cites the unit by id, the
  caption that ties the figure to this page's claim, and both projections.
  EVIDENCE keeps the unit's factual `claim:` row and may not say what it proves.
- **A unit's KIND decides whether its intake waits**, stated for the first time.
  A data unit (table, figure) freezes from a probe card's `proof/` and cannot
  exist before its card is answered. A concept unit (diagram, tex, illustration)
  freezes a listing of source files and has nothing to wait for. Every phase
  contract had only the first case, which read as if no unit could ever be built
  early.

## 0.8.0 — 2026-08-19

- **🧮 proof RETIRED.** JL 260819: "我从开始到最后都没有说 proof，我一直说
  probe". The mark came from ONE transcribed quote ("citation, display, values
  and proofs") and no Log row ever ruled it. Going to a task folder or a
  discovery folder for the evidence behind a claim IS a probe, which is 🔢.
  It was the only mark with no plugin, no folder, no lane, no id and no
  backlink, and that was the symptom rather than a design.
  ⚠️ `proof/` the FOLDER is untouched: it belongs to a probe card.

- **0.7.3 is WITHDRAWN.** It stated a four-marks-against-three-lanes rule, and
  the fourth mark no longer exists. Three marks now meet three lanes.

## 0.7.3 — 2026-08-18

- **The FOUR outline marks against the THREE lanes**, stated here for the first
  time. A plan marks citation, value, display and PROOF; only the first three
  become lanes in this phase, and proof never does. Found by JL reading the
  QPw00 plan: "you should say that the four evidence card types. You don't have
  it for now, right?" — correct, no phase contract said it. The rule itself was
  already ruled (260817, proof earns no folder, `haipipe-page-probe` §🧭); what
  was missing was the lane that does not exist being named where the lanes are.

## 0.7.2 — 2026-08-18

- Pointer added to `../haipipe-page-workflow/ref/phase-cards.md` §④, which
  states this phase and every sibling in the SAME six fields
  (`❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`). This
  contract still owns the reasoning; the card is the readable-across-phases
  summary, and the contract wins when they disagree.
- Board backlink retargeted: `QPw7`/`QPw8`/`QPw9` became `QPw00a`/`QPw00r`/
  `QPw00g` when JL ruled that pages which are not phases may not carry
  phase numbers.


## 0.7.1 — 2026-08-18

Added the Board page backlink: the page that argues this contract, created 260818 when JL ruled one page per workflow step.

## 0.7.0 — 2026-08-17

Exposes the derived Evidence Bundle at the frozen Point address and makes the
EVIDENCE→REVISE handoff explicit for sentence realization and Display render.

## 0.6.0 — 2026-08-17

**The card is created at PROBE, not by DRAFT.** §🧾's "a card may arrive already
PROPOSED … DRAFT is allowed to create any of the three in OWED state" is
replaced by a per-kind table: 🔢 created by PROBE from the outline's mark, 📚
landed by a person (PROBE opens a card only when the key is UNKNOWN), 🖼 created
HERE and nowhere earlier, because a unit's `intake/` freezes FROM a `proof/`
that does not exist until an answer does.

- §🔎's six-step loop keeps all six steps and now names their owners: ①②③ are
  `haipipe-page-probe`'s, because they end when the question leaves, and ④⑤⑥ are
  this phase's, because they begin when something comes back.
- §🪪 corrected: `PROBE` is a LIVE phase again and is NOT this one. The alias
  holds only for receipts written before 260817, which is also how
  `65-plugin-pageflow.js` now resolves the token.
- §🔀 enters from PROBE rather than from DRAFT.

## 0.5.0 — 2026-08-16

RENAMED from `haipipe-page-probe`, and the scope moved with the name (JL 260816).

- The phase token is `EVIDENCE`; `PROBE` is normalized wherever a phase or route
  is read (`src/page_lifecycle.py`, `src/page_context.py`, the pageflow stepper),
  so the two receipts already on disk and every `· PROBE ·` Related-Pages row keep
  auditing and parsing unchanged.
- WIDENED from one evidence kind to three: a CITATION (bibex entry), a VALUE
  (probe card bound to its QA file), and a DISPLAY INTAKE (frozen snapshot plus
  the named renderer). They are one phase because they chain: bank answer ->
  probe card -> display intake -> float.tex -> latex/word.
- A card may arrive already PROPOSED by DRAFT; EVIDENCE fills it and never
  opens a second one for the same unknown. EVIDENCE may also propose a card when
  gathering reveals a claim the outline missed.
- Added step ⑥ CARD to the loop, and made it the EXIT TEST: "every claim the
  outline promised has its card on disk, and every declared display unit has a
  frozen intake and a named renderer". The old exit, "the answer came back", is
  what let QV2-lbp-regression-results reach LaTeX with 5 declared units and 2
  rendered.
- Declared the display walk's SPLIT so no step is unowned: ① INTAKE is EVIDENCE's,
  ②③④ RENDER/PICK/BUILD are REVISE's, ⑤ ACCEPT stays the human gate at CHECK.
- Receipt gains `cards` and `renderers` rows. A frozen intake with no named
  renderer is a HOLD, not a pass.
- DESIGN was weighed as the new name and rejected: `page-types/haipipe-page-for-design`
  already holds the word, and a DESIGN phase would carry DRAFT's authority over
  purpose and Aims.

haipipe-page-probe · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.4.0 - 2026-08-06

The lifecycle runs COLLECT-first on evidence pages (JL 260806): collect the
new Q-consumer into the owning topic's E0 queue → translate it into an E<n>
division + its QA-probe (① ORGANIZE) → dispatch → copy the A-executor back
into the QA-probe → write each A-consumer under the division's `####
consumers` rows (⑤ INTERPRET). Vocabulary finalized: QA-probe / QA-bank, four
capital slot words; the write-surfaces table names the E0 queue and E<n>
division parts explicitly.

## 0.3.3 - 2026-08-06

Wording sweep for JL ruling B (260806: "an entry is a source file the topic
page points at, like a PDF; the board renders the topic page, never the
entry"): the persisted surface's vocabulary entry is now the probe QA (the
entry record), a hidden `<n>-<slug>.md` source record below the topic page's
probes/ folder, never a board page; one conversation, two QAs: the bank QA is
the original, the probe QA is the consumer's copy that points at it. The
family-contract and Files closings name the probe QA instead of a Probe Page.

## 0.3.2 - 2026-08-05

Load-order slot reworded for thin-paper phase 2: the last slot is the family
DOOR's probe tooling (paper: `paper/haipipe-paper/probe/`), and the family DOOR
owns the persisted Probe Page shape and checker (was: "family workers own...").

## 0.3.1 - 2026-08-05

- The description leads with the plain job before the four coined Q/A terms, per the no-undefined-jargon rule.

## 0.3.0 - 2026-08-04

- Adds the shared RUN receipt boundary: PROBE records the unknown, executor and
  consumer artifacts, evidence bindings, limits, and one legal route.
- Allows an unchanged target-Page hash only when the separate probe artifacts
  make the work auditable; PROBE still cannot CLOSE.

## 0.2.0 - 2026-08-04

- Renamed from `haipipe-board-page-for-probe-entry` and moved under `page-phases/`.
- PROBE is now a Page phase rather than an Entry Page Type.
- Retains the canonical Q-consumer, Q-executor, A-executor, and A-consumer model from `haipipe-probe`, including one Q-executor serving several Q-consumers.
- Uses `Probe Page` for the optional persisted Board surface and treats older `entry` labels as implementation vocabulary rather than another lifecycle concept.

## 0.1.0 - 2026-08-04

**Created** (JL: "ok, I agree, please go ahead and make them.").

Split out of the family workers so the four-phase loop has ONE rulebook instead of
one per family. Measured 260804: the paper and application families each shipped
their own draft/probe/revise/check hubs (1,263 lines against 531), and NONE of the
eight loaded `haipipe-page` at all, so each had copied the page grammar from
memory. `haipipe-paper-draft` still named `## Items to Finish` five times, a
section renamed that morning.

- Host-agnostic on purpose: names no venue, no markup, no checker. A family worker
  adds its artifact knowledge and obeys this file.
- Settles `QC6 A4.1`: paper and application share a CONTRACT, not folder names.
