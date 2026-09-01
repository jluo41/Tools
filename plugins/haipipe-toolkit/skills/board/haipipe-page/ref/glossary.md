# The page family's words, each with the path it names

Born 260820 when JL asked "cards <--- what is cards? do we have this glossary?"
after four replies used the word. We did not: every term was defined inside
whichever skill section introduced it, so a reader met them one at a time and
never side by side.

**The rule this file serves** is `haipipe-board/ref/writing-rules.md`: every
phrase is either the source document's own wording or is defined where the
reader can find it. A term with no path is a coined word, and coined words are
the failure that rule exists to stop.

Read it as: **TERM** — what it is. `the path it actually names`.

## 🧱 Things that exist on disk

- **Board** — one topic, one folder, one markdown page per question or stage.
  `<project>/diagram/<NN>-<Name>-<date>/`
- **Page** — one question (Q) or one lifecycle stage (S), and the folder that
  holds everything it owns. `<board>/<group>/<PageId>-<slug>/<PageId>-<slug>.md`
- **Page Type** — which KIND of page this is (task, section, venue, narrative,
  dash …), fixed for the page's life. `board/page-types/haipipe-page-for-*`
- **plan**, also **the outline file** — the agreed SHAPE of a page, written and
  approved before any prose. `<page>/outline/<stem>-outline-v<N>.md`
- **bullet** — one POINT in the plan: a short capitalized HEAD, then one folded
  line (`Note:` authored, `Answered:`/`Drawn:` appended when evidence lands),
  then its mark. Addressed by POSITION, never by a name.
- **address** — `C3.P1.B2` = section 3, paragraph 1, bullet 2. It is the
  bullet's only id, so moving a bullet renames it, on purpose.
- **mark** — the one symbol at the end of a bullet saying what it still owes:
  🎯 an aim · 📮 a question to ask · 🧮 a number to pull · 📚 a citation to
  land · 🖼 a picture to draw.
- **item row** — one record per mark in `outline/<stem>-items.md`, written at
  SURVEY: what is owed, which run in tasks/ answers it (`found · rerun ·
  new-run · new-task · new-job · new-block · person · none`), and a person's
  Decide. Its Status is derived (`owed → bound → landed → folded → accepted`).
- **card**, also **probe card** — ONE question this page needs answered by
  someone else, as a folder. Raised at LAND only when the question LEAVES the
  page; a `found` row never mints one.
  `<page>/evidence/probe/PP<NN>-<slug>/` holding `card.md`, `consumer/`,
  `executor/`, `proof/`.
- **display unit**, often shortened to **unit** — ONE picture and everything
  needed to rebuild it. Created at LAND, one per 🖼 mark.
  `<page>/evidence/display/<PageId>-Display<N>-<slug>/` holding `intake/`,
  `recipe/`, `assets/`, `float.tex`, `preview.pdf`, `README.md`.
- **intake** — the unit's FROZEN inputs plus their sha256 hashes, so a moved
  source file is caught rather than silently redrawn. `<unit>/intake/`
- **bibex entry** — one reference, landed by a person, never invented.
  `<page>/evidence/bibex/<stem>.bib`
- **receipt** — the machine-readable record of one phase pass: who acted, which
  phase, which round, where it routed. `<board>/_runs/page/<page>/<stamp>.json`
- **the bank** — the task and discovery folders that ANSWER questions, and know
  nothing about who asked. `tasks/<group>/<folder>/QA/<n>-<slug>.md` and
  `discoveries/<group>/<folder>/QA/<n>-<slug>.md`
- **QA file** — one answer in the bank, written in general language with no
  page, claim or stake in it, so any consumer can read it. Its number is only
  the ORDER that task folder answered questions in, never a rank or a version:
  `5-reported-trait-coefficients-mme-outcomes.md` is simply the fifth question
  that folder has been asked.
  ⛔ **Never abbreviate one as "QA/5" in a reply.** It reads as a section
  number and names nothing a person can open (JL 260820: "what is the QA/5?
  how to understand it?"). Say the file: the folder it lives in, then its name.

## 🗣 The four words inside a card, and why there are four

A card is split so a question can cross to the bank without carrying what the
page hopes the answer will be. That hope is the **stake**, and it never crosses.

- **q-consumer** — the question WITH its stake: what this page loses if the
  answer goes the wrong way. Stays home. `<card>/consumer/q-consumer.md`
- **q-executor** — the same question STRIPPED: no page, no claim id, no hoped-for
  answer. The only part that crosses. `<card>/executor/q-executor.md`
- **a-executor** — the answer as the executor gives it, plus the raw evidence
  pulled into `<card>/proof/`. `<card>/executor/a-executor.md`
- **a-consumer** — what the page MAKES of that answer. Stake-aware, so it is the
  consumer's to write, never the executor's.

## 🚦 Words for state, and who may write them

- **tick** — a box only a PERSON may check. Four of them, and a machine may
  transcribe one only on an explicit instruction in chat, saying so in the line:
  `approved:` on a plan · `read:` on a card · `verified` on a bibex entry ·
  `accepted:` on a display unit.
- **state:** — the card's own line, DERIVED from what exists, never asserted:
  `planned` → `commissioned` → `working` → `answered` (or `answered-local` when
  the page's own reading of shipped output settled it) → `read`. `blocked-*`
  names what is missing instead of pretending progress.
- **serves:** — the backlink from a card or unit to the bullets it answers,
  e.g. `serves: C4.P1.B4`. Without it, evidence exists but nothing uses it.
- **target:** — the card's pointer at the QA file in the bank that answered it,
  written by PATH so it can be opened and checked.

## ⏱️ Words for time, and none substitutes for another

Defined once in `page-workflows/haipipe-page-workflow` §🔤; repeated here only
as pointers, because that section is the authority.

- **workflow** — which LOOP this is. Never repeats.
- **phase** — which AUTHORITY is acting: 🧭 OUTLINE · 🃏 EVIDENCE · ✏️ DRAFT ·
  🖊 REVISE (📄 COMPILE folded) · ✅ CHECK. REPEATS, which is why it is not
  called a step.
- **cycle** — the named pass inside a phase: SHAPE · SURVEY (OUTLINE) · LAND ·
  EMBED (EVIDENCE) · WRITE (DRAFT + REVISE) · CHECK. The OUTLINE part is the
  first four; the DRAFT part the last two. Never a letter code, never a
  circled number.
- **step** — WHERE in this run, a number that never repeats.
- **round** — which PROMISE era; repeats when a page is reopened.
- **RUN, not ADVANCE** — a page may repeat a phase, branch, HOLD, or go back;
  which phase runs next is chosen by AUTHORITY, never by position.

## 🧑‍🔧 Words for who acts

- **producer** — the hand that WRITES in one phase. One per phase.
  `board/page-workflows/agents/haipipe-page-<phase>-agent`
- **judge** — the cold read of a BUILT version at CHECK (and, in pre-check
  mode, inside WRITE's loop). May never be the
  same actor that produced it. `haipipe-page-check-agent`
- **haipipe-probe-q-executor-agent** — the ONE agent allowed to hand stripped
  questions to the bank, shared by every consumer family (JL 260820). Called
  by exactly one caller per family; for a page that is
  `haipipe-page-probe-agent`.
- **orchestrator** — the bank's own dispatcher, `haipipe-task-orchestrator-agent`
  or `haipipe-discovery-orchestrator-agent`. No page-side hand calls one
  directly.

## 📏 Two counts that are easy to confuse

- **📐 a diagram** — an ascii block inside the markdown. Costs nothing, renders
  as text, is not a display unit.
- **🖼 a display unit** — a FOLDER that builds a real picture into the PDF.
  A page that DECLARED a unit and created no folder is not done, and the phase
  receipt must record both counts.
