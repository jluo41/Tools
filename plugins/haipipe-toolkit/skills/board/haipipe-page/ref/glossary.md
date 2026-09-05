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
- **Folder kind** — the stable domain kind whose workflow phase or canonical
  family skill owns the Folder and its Page Face. `workflow/phase.yaml`
  `current.folder-kind` or the Page's `folder-kind:` field.
- **Page Type** — the compatibility key used by an unmigrated Page. New Pages
  resolve their Page Face through Folder kind; `page-type:` and
  `board/page-types/haipipe-page-for-*` remain fallbacks.
- **Context record** — the generated PREPARE projection of the governing
  identity, ownership, policy, requirements, related information, feedback,
  decisions, and Page records. `<page>/outline/<stem>-context.md`
- **plan**, also **the outline file** — the agreed SHAPE of a page, written and
  approved before any prose. `<page>/outline/<stem>-outline-v<N>.md`
- **bullet** — one POINT in the plan: a short capitalized HEAD, then one folded
  line (`Note:` authored, `Answered:`/`Drawn:` appended when evidence lands),
  then its mark. Addressed by POSITION, never by a name.
- **address** — `C3.P1.B2` = section 3, paragraph 1, bullet 2. It is the
  bullet's only id, so moving a bullet renames it, on purpose.
- **Evidence Item** — one named, typed thing an outline bullet expects:
  `E<NN>-VALUE|CITE|DISPLAY-<slug>`. SHAPE writes its expected ready payload and
  acceptance; SURVEY plans Supporting Runs and exactly one local Run in
  `outline/<stem>-evidence-items.md`. Status is derived (`specified → planned →
  ready → folded → accepted`).
- **Supporting Run** — an Execution or Discovery Run whose detailed Result is
  frozen into an Evidence Item's one local input envelope. Zero or more per item.
- **Local Input** — one immutable envelope containing the Evidence Item
  contract, exact Supporting Result paths and hashes, and any governed
  page-local static sources allowed by SURVEY. It is frozen by LAND.
- **local Evidence Item Run** — the one Page · Evidence Item Run that converts
  the frozen input into a focal ready VALUE/CITE/DISPLAY Result for EMBED.
- **Result** — the output artifact of one allocated Run. A Supporting Result
  remains detailed reusable upstream output; an accepted local Evidence Item
  Result is the focal VALUE, CITE, or DISPLAY payload that EMBED may interpret.
- **Run item** — one reader-facing presentation of a mapped Supporting or local
  Run. It displays the global Run identity and its purpose, availability, next
  action, Run path, and Result path; it does not create another Ticket.
- **display unit**, often shortened to **unit** — ONE picture and everything
  needed to rebuild it. LAND supplies its Page-owned directory directly to the
  renderer; the governed DISPLAY Result envelope points to the unit and records
  its source Run, resolved Result path, and hashes. CHECK administers its later
  human `accepted:` gate. One per 🖼 mark.
  `<page>/outline/evidence/display/<PageId>-Display<N>-<slug>/` holding `intake/`,
  `recipe/`, `assets/`, `float.tex`, `preview.pdf`, `README.md`.
- **intake** — the unit's FROZEN inputs plus their sha256 hashes, so a moved
  source file is caught rather than silently redrawn. `<unit>/intake/`
- **bibex entry** — one citation file or source-metadata projection.
  `<page>/outline/evidence/bibex/<stem>.bib`. The person's CITE verification
  is `Verified:` on the authored Evidence Item row, not a second bibex gate.
- **receipt** — the machine-readable record of one phase pass: who acted, which
  phase, which round, where it routed. `<board>/_runs/page/<page>/<stamp>.json`
- **the bank** — the task and discovery folders that ANSWER questions, and know
  nothing about who asked. `tasks/<block>/<job>/<task>/QA/<n>-<slug>.md` and
  `discoveries/bNN_<block>/jNN_<job>/tNN_<task>/QA/<n>-<slug>.md`
- **QA file** — one answer in the bank, written in general language with no
  page, claim or stake in it, so any consumer can read it. Its number is only
  the ORDER that task folder answered questions in, never a rank or a version:
  `5-reported-trait-coefficients-mme-outcomes.md` is simply the fifth question
  that folder has been asked.
  ⛔ **Never abbreviate one as "QA/5" in a reply.** It reads as a section
  number and names nothing a person can open (JL 260820: "what is the QA/5?
  how to understand it?"). Say the file: the folder it lives in, then its name.

## 🗂 Evidence and Run presentation

- **Evidence Workspace** — the Outline plugin's joined view of Evidence Item
  contracts, mapped Runs, citation material, values, displays, and their
  provenance. Its authority remains the records under `<page>/outline/`.
- **Evidences lens** — the contract-first view: what each Evidence Item is for,
  what ready payload it expects, and how acceptance will be checked.
- **Runs lens** — the execution-first view: every mapped Supporting or local
  Run is one Run item, grouped beneath each Evidence Item it supports. A shared
  Run may appear in several groups while retaining one global identity.
- **Run & Result paths** — the collapsed detail that exposes the exact Ticket
  and Result locations. `Run` and `Result` are the reader-facing labels.
- **legacy Probe or PageX material** — read-only migration input. Existing
  files may still be rendered or audited, but new Page work creates neither a
  `probe/` lane nor an active PageX binding; cross-Folder evidence enters via a
  Supporting Run Result.

## 🚦 State, action, and person-reserved acts

- **Evidence state** — a derived Evidence Item progression:
  `specified → planned → ready → folded → accepted`. It is computed from the
  contract, Run graph, Result binding, plan fold, and applicable acceptance;
  it is never a manually typed generic Status.
- **Availability** — what physically exists for a Run item:
  `Planned` · `Run exists · Result missing` · `Run + Result` ·
  `Paths unresolved`.
- **Next action** — what should happen to that Run item:
  `Allocate and run` · `Run` · `Rerun` · `Reuse Result` · `Resolve path`.
  Availability and Next action are independent; `new`, `rerun`, `run only`,
  and `ready` never form one status scale.
- **Target** — the Evidence Item's stable Bullet address, such as `C2.P1.B4`.
  It states which planned reader move the ready Result must serve.
- **person-reserved act** — an authored decision a machine may only transcribe
  from explicit durable human input: `approved:` on an outline version;
  per-item `Decide` (`make | defer | drop`) during SURVEY; `Verified:` on a
  CITE Evidence Item during LAND; Page/display `accepted:` and any declared
  Folder-owner ruling during CHECK. A legacy `read:` receipt may remain visible
  while old outbound material is migrated, but it is not created by new work.

## ⏱️ Words for time, and none substitutes for another

Defined once in `page-workflows/haipipe-page-workflow` §🔤; repeated here only
as pointers, because that section is the authority.

- **workflow** — which LOOP this is. Never repeats.
- **phase** — which AUTHORITY is acting: `00 CONTEXT` · `01 OUTLINE` ·
  `02 EVIDENCE` · `03 CONTENT` · `04 CHECK`. REPEATS, which is why it is not
  called a step. DRAFT and REVISE are CONTENT movements, never phase ids.
- **cycle** — the named pass inside a phase: PREPARE (CONTEXT) · SHAPE and
  SURVEY (OUTLINE) · LAND and EMBED (EVIDENCE) · WRITE
  (Draft · Revise · Build · Pre-check inside CONTENT) · CHECK. Never a letter
  code, never a circled number.
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
- **phase producer** — the current writer for CONTEXT, OUTLINE, EVIDENCE, or
  CONTENT. The active roster is `haipipe-page-context-agent`,
  `haipipe-page-outline-agent`, `haipipe-page-evidence-agent`, and
  `haipipe-page-content-agent`; Draft, Revise, and Probe are not phase-agent
  identities.
- **orchestrator** — the bank's own dispatcher, `haipipe-task-orchestrator-agent`
  or `haipipe-discovery-orchestrator-agent`. No page-side hand calls one
  directly.

## 📏 Two counts that are easy to confuse

- **📐 a diagram** — an ascii block inside the markdown. Costs nothing, renders
  as text, is not a display unit.
- **🖼 a display unit** — a FOLDER that builds a real picture into the PDF.
  A page that DECLARED a unit and created no folder is not done, and the phase
  receipt must record both counts.
