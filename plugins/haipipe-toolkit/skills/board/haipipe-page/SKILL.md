---
name: haipipe-page
description: >-
  The PAGE contract and router of a Board: one Page combines a stable Page
  Type with a current Page Phase (OUTLINE, DRAFT, PROBE, EVIDENCE, REVISE,
  COMPILE, CHECK). Three verbs: CREATE scaffolds a Page, WORK ON repairs one,
  RUN hands off to haipipe-page-workflow. Trigger: create a page, new page,
  update a page, run page lifecycle, Page Type, Page Phase, /haipipe-page.
metadata:
  version: "0.39.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page · one shape every page keeps

`haipipe-board` is the door you walk through to RUN a board. This skill is the
door for ONE PAGE, and the spec that page is measured against. Say
`create a new page on <topic>`, `working on <page>`, or `run <page>`; load it
with no board open and it is a pure contract. Its consumers need these rules
with no board open: the routing verb deciding "which page, which section", the
chat drawer priming a per-page session, and the variant authors in other
families.

**Who owns what**: this skill holds the spec, `haipipe-board` holds the
machinery.

```text
haipipe-page                     haipipe-board
──────────────────────────       ──────────────────────────────
what a page IS                   rendering it (src/page_question.py)
the section contract             serving and write-back (cli/serve.py)
where a write may land           the checker (cli/check.py)
the base/variant model           the template file (ref/page-template.md)
```

This skill never CONTAINS the renderer, the server or the checker. It CALLS
them, because a reader asking for one page should not have to know which
script does what. The authoritative template stays
`haipipe-board/ref/page-template.md`; this contract cites it and never forks
it.

## 📁 What a page is on disk

A Page is one markdown file plus the plugin folders it actually uses. The
`.md` is this contract's; every sibling folder belongs to a plugin, and the
roster of legal folder names is `haipipe-plugin`'s `ref/roster.md`.

```text
<page>/
├── <page>.md      the argument and its bindings · THIS contract
├── outline/       the frozen, approved plan for the current round
├── pagex/         Probe's accepted-Page lane: files borrowed from other Pages
├── probe/         Probe's Task/Discovery lane: cards, proof, and values
├── bibex/         citation cards, source notes, the page's own .bib
├── display/       zero or more independently accepted display units
├── latex/ word/   generated projections, when requested
└── …              every other lane on the plugin roster
```

A folder is created only when it is used. Its absence means "not needed" only
when the Page says so; it must never mean "forgotten". Values have a surface
but no folder of their own: each lives inside one probe card's `## Values`
block and is cited from prose as `PP<NN>.v<n>`.

## 🧬 One key claims a page

**A property every page carries cannot tell one kind of page from another.**
That is the admission test, and it decides what earns a Page Type. A page
shows something, cites something, states a number; so display, literature and
value are PLUGINS, because a property shared by all pages changes no page's
closing rule, and a kind that changes no closing rule is plugin material. A
key is what a page carries when its shape is genuinely special enough to earn
a contract, and a contract earns its key by stating how that page CLOSES.

**No `page-type:` key is the DEFAULT and the most flexible case.** A page with
no key owes the base section order and nothing more. Carrying a key to say "I
am ordinary" would make the default a thing you declare, which is not a
default.

**Type resolution**: one table for ALL types. Resolve ① to ⑤ in order and stop
at the first key that matches.

```text
step  machine-readable key                    Page Type          contract
──────────────────────────────────────────────────────────────────────────
①     filename QBv<n>-                        venue              for-venue
②     ─ retired · `route:` is a PLUGIN key now, not a type key ─
③     frontmatter `page-type: <key>`          the key names it   for-<key>
④     filename S-<Family>-<unit>-<slug>       stage              for-stage
⑤     filename Q<group><n>[<face>]-<slug>     Q decision         base only
```

EXACTLY ONE step may claim a page, or the page is defective: a page no key
matches, or one carrying two keys that disagree, is fixed on the page, never
in the resolver. Step ③'s key is REQUIRED on every type that has one, and it
BEATS the filename. `route: outward` / `route: inward` still parses and still
says which evidence lane a page's cards belong to; what it no longer does is
pick a contract, so a page carrying it falls through to ④ or ⑤ and resolves by
filename like any other page. `src/common.py` may still recognize legacy
filename prefixes: membership is the glob's whole job, and a legacy prefix
whose former type was deleted falls back to the base contract or to its own
plugin.

**A discovery folder does not get its own type.** It is a special task, so
`task` carries which kind of folder it reads rather than a sibling contract
repeating its shape.

### The inventory is derived, never written by hand

Three places hold it, and a hand-written table cannot stay equal to all three:
the shipped `*/page-types/` folders say who MAINTAINS a key, `check.py`'s
`PAGE_TYPE_VALUES` says what RESOLVES, and the boards say what is IN USE.

```bash
python3 <haipipe-board>/cli/pagetypes.py           # the table, with live page counts
python3 <haipipe-board>/cli/pagetypes.py --write   # rewrite the block below
python3 <haipipe-board>/cli/pagetypes.py --check   # exit 1 on any drift
```

A key with live pages and no contract, or a key the engine accepts that
nothing ships and nothing uses, is a FINDING, not a paragraph, and `--check`
is the tooth. The block below carries only the structural facts, which change
when a key is born or dies; the page COUNTS stay in the command's own output,
because a number that moves whenever anyone writes a page would show this
contract as modified on days nobody touched it.

<!-- BEGIN GENERATED page-type-inventory -->
```text
key          owner         engine  resolved by
───────────────────────────────────────────────
brief        application   ✓       `page-type:` line
collection   —             ✓       `page-type:` line
dash         —             ✓       `page-type:` line
data         application   ✓       `page-type:` line
design       application   ✓       `page-type:` line
display      —             ✓       `page-type:` line
ideation     paper         ✓       `page-type:` line
information  application   ✓       `page-type:` line
insight      task          ✓       `page-type:` line
knowledge    application   ✓       `page-type:` line
labeling     —             ✓       `page-type:` line
meta         application   ✓       `page-type:` line
narrative    paper         ✓       `page-type:` line
opening      —             ✓       `page-type:` line
principle    application   ✓       `page-type:` line
question     application   ✓       `page-type:` line
roadmap      paper         ✓       `page-type:` line
round        paper         ✓       `page-type:` line
section      paper         ✓       `page-type:` line
seed         paper         ✓       `page-type:` line
slide        —             ✓       `page-type:` line
stage        board         ✓       filename S-<Family>-<unit>-
task         task          ✓       `page-type:` line
venue        paper         ✓       filename QBv<n>-
view         —             ✓       `page-type:` line
wisdom       application   ✓       `page-type:` line
```
<!-- END GENERATED page-type-inventory -->

### A variant extends the base and never redefines it

A Page Type used by one consumer family is a VARIANT of the base: it defines
Content and may populate fixed extension points in Aims, States, and Stage
Contract, but it never redefines, adds, removes, or reorders the frame
sections.

**A variant ships under the `page-types/` folder of the SKILL SET THAT OWNS
IT**, so the folder a variant sits in names its owner and nothing else has to.
This skill owns the BASE those variants extend, and only the variants that
belong to no one artifact. Load the matching variant before writing or fixing
any Page of its type. When a variant moves, its installed symlink still points
at the old folder, so re-run `install.sh --global` or the skill silently stops
resolving.

## 🎭 Phases, independent of type

A Page persists while the authority acting on it changes. The current phase is
not another Page Type and is not inferred from the edit operation.

```text
phase       authority                                     load
─────────────────────────────────────────────────────────────────────────────
OUTLINE 🚧  agree the SHAPE, exit only on a person's tick page-workflows/haipipe-page-outline
PROBE       turn each outline mark into a card and ask     page-workflows/haipipe-page-probe
EVIDENCE    land every promised claim's card across the evidence wall
                                                          page-workflows/haipipe-page-evidence
DRAFT       define purpose/Aims and write from landed evidence
                                                          page-workflows/haipipe-page-draft
REVISE      improve the current promise while purpose and Aims stay fixed
                                                          page-workflows/haipipe-page-revise
COMPILE     rebuild latex · pdf · word from that prose     page-workflows/haipipe-page-revise
CHECK       judge one version and route its next authority page-workflows/haipipe-page-check
```

Resolve one invocation in this order:

```text
base Page contract
  → matching Page Type, when one exists
  → current Page Phase
  → Page-local plugins and family craft required by the resolved artifact
```

The phases form a routing grammar, not a conveyor belt. Each may repeat, PROBE
and EVIDENCE may be skipped when the Page promises no claim it cannot support,
and CHECK may route to any earlier phase. Returning to DRAFT because purpose or
Aims changed starts a new round on the same Page. Why each phase was split from
its neighbour, and the failure each split prevents, is
`page-workflows/haipipe-page-workflow`.

Use the authority test when the visible operation is ambiguous:

```text
the section list itself is being agreed  → OUTLINE
purpose or Aims change                   → DRAFT
a marked hole has no card open for it    → PROBE
a card is open and its answer must land  → EVIDENCE
the same purpose and Aims are improved   → REVISE
a concrete version is judged             → CHECK
```

Adding, deleting, moving, and rewriting may be DRAFT or REVISE; the reason for
the change decides. `RUN` is the router verb, deliberately not `ADVANCE`: a
Page can repeat a phase, branch, HOLD, or return to DRAFT in a new round. RUN
is OWNED by `page-workflows/haipipe-page-workflow`, and the shared packet,
receipt, version, role-separation and stop rules live in its
`ref/page-run-contract.md`.

## 📑 The sections, in fixed order

The AUTHORITY is `haipipe-board/ref/board-form.md` §4, which fixes the ON-STAGE
order as five, `Opening → Diagram → Content → Aims → States`, with Files after
them and the folds last. This skill adds no section to that list; the table
below names the same run plus what a machine may write into each.

```text
#   section    owes the reader                     phase authority
─────────────────────────────────────────────────────────────────────────────
1   Opening    the lead question + why it matters  DRAFT defines · REVISE clarifies
2   Diagram    the figure; ids in it are links     DRAFT/REVISE, within type rules
3   Content    the substance, ### divisions        DRAFT defines · REVISE realizes
4   Aims       durable Content-linked targets      DRAFT; changing intent starts a round
5   States     one factual current State per Aim   any phase, from inspectable evidence
6   Files      action map + scoped Page context    DRAFT/REVISE maintain
7   folds      Discussion · Law · Lesson · Glossary · Log
                                                   the phase owning the record
```

Each section answers ONE reader question, and the same five rows define every
section's contract: **conveys**, the reader question it answers · **holds**,
the elements it must contain · **source**, how the author writes it ·
**rules**, what binds a write · **omit**, when it may be absent. The full five
rows per section live on the design board's `QB4`; the authoritative source
form stays `haipipe-board/ref/page-template.md`.

```text
section            conveys · the reader question                omit
──────────────────────────────────────────────────────────────────────
🧭 Opening          what is this page, why should I care?        never
   ### Writing Style  how the NEXT writer should write it        allowed
🖼 Diagram          can I see the whole subject at once?         when no figure helps
📚 Content          what does this page actually establish?      Q may · S never
🎯 Aims             what should become true, and for which
                    Content division?                            never
📍 States           what is true now for each Aim, and what waits? never
📎 Files            which few files continue this work?          allowed, advised against
🗃 folds            what was ruled, learned, changed, if needed  each optional
```

A sentence answering another section's question is MISPLACED, and the protocol
names its home: substance found in Opening moves to Content, Required Inputs
and Venue move to Stage Contract, prose rules move to Opening's
`### Writing Style`, intended outcomes move to Aims, and current facts move to
States. Temporary next steps become an Aim's optional Plan.

There is NO `## Boundary` section. What a page covers is the Opening's job;
point at a neighbouring page from the prose that needs it, as a
`**Covered elsewhere**:` part in the Opening's drawer. `src/common.py` ALIASES
the retired names `## Question`, `## Items to Finish` and `## Where we are`, so
a page on the old vocabulary keeps rendering; `check.py` reports each as
`retired-section`, which is the only reason a forgiving renderer does not hide
the drift.

## 🎯 One Aim, one State, joined by id

`## Aims` owns durable targets and their `Done when:` tests. `## States` owns
the current factual status of those targets. Every Aim id appears exactly once
in States, so intent stays stable while status may change without rewriting it.

```markdown
## Aims
- A6.2 · Decide whether COMPILE remains folded into REVISE.
  **Done when:** the decision is scored against the four split tests.

## States
- ✅ A6.2 · Met 260819. §6.4 records the score and owning decision Page.
```

The tick and current fact live only in States: `✅` met · `🔨` being worked on ·
`🧠` waiting on a ruling · `⬜` not met · `❄️` deliberately held. Each says its
meaning by SHAPE; the old `🟡` `🟠` `⏸️` still parse. This is the AIM
vocabulary and NOT the page `state:` line, which keeps its own ✅ 🟡 🔴 ⏸️ set
and is checked apart. The section is a snapshot, so the reason for a transition
belongs in Log. A State row carrying no Aim id is a note, not a status; move it
to the Aim's optional Plan, the Log, or out of the Page.

The frozen outline declares each Aim and its `Done when:` test but does not
cache changing status. DRAFT transcribes the target and test into Aims; later
phases update the matching States row from inspectable evidence.

An Aim is not a task. Write `- A3.1 · target` for a result owned by Content
part 3, under the group `### A3`, and `P1` only for a target that genuinely
crosses parts. One division may have zero, one, or many Aims. Each Aim has a
testable `Done when` and may carry a temporary `Plan`; changing Plan does not
change the Aim. The strict one-to-one relationship is Aim to current State row,
never Content division to Aim.

An Aims or States group is `### A<n> · <emoji> <name>`, taking the NUMBER, NAME
and EMOJI of the Content part it answers, so the three sections line up by eye
as well as by id (`C<n>` still resolves). Ordinary Files groups are a MENU of
actions, taken as they apply: ⚙️ Engines what RUNS the subject · 📋 Contracts
what CARRIES a rule to other pages · 🧪 Checks what CATCHES a page breaking one
· 📥 Input files what the work READS · 📤 Output files what a BUILD writes.
Their names state an ACTION, never a subject, because a subject-named group
rots the moment its subject leaves the page.

`### 🔗 Related Board Pages` is the one fixed Files group. It is a selective
context map between Pages, not a file dependency graph and not configuration
inheritance. The fixed name gives the checker a parser boundary; each row
begins with the action-like relation that ordinary Files groups put in their
heading:

```markdown
### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · EVIDENCE` · [QB7 §3](QB-research/QB7-literature.md)
  Read the evidence boundary before resolving this Page's consequential unknown.
```

The four relations are `reads`, `constrained by`, `continues`, and `contrasts`.
The phase is `DRAFT`, `EVIDENCE`, `REVISE`, `CHECK`, or `ALL`. The target is a
Board-root-relative Page source, and its visible id must match that Page. Scope
is `page` or one direct Content division such as `§3` or `§3.2`; a division read
automatically carries the target Page's identity, Opening, and matching
Aims/States group so the fragment does not arrive without its promise and
current state. When one packet selects several divisions from the same target
Page, identity and Opening are emitted once rather than repeated per row.

Read the current Page whole first. Then run
`python3 <board-skill>/cli/pagecontext.py <current-page.md> --phase <PHASE>`
and load only the returned packet. The reader follows one hop: it never
traverses Related Board Pages declared by a target Page. Cycles are therefore
harmless, context stays bounded, and a phase sees only rows written for it or
for `ALL`. `check.py` rejects a malformed row, a path outside the Board, a dead
Page, a mismatched Page id, or a missing scope before an agent can silently
work without that context.

## 🚪 Create · work on · run

Say any of these and this skill runs it. You never call the engine yourself.

```text
📄 CREATE     /haipipe-page create a new page on <topic>   [on <board>]
🔧 WORK ON    /haipipe-page working on <page>              or just the path
🔁 RUN        /haipipe-page run <page> [from <phase>]
```

### Create a new page on a topic

1. Resolve the board folder and the group the page belongs to. Ask ONLY if the
   group is genuinely ambiguous.
2. Pick the id (`Q<group><n>-<slug>`, or `S-<Family>-<unit>-<slug>` for a
   lifecycle stage) and copy `haipipe-board/ref/page-template.md` to it. Never
   retype the shape from memory: the template's guide sentences ARE the
   contract.
3. Write the title so it states the page's PURPOSE, in sentence case.
4. Write the Opening: the visible paragraph above the first blank line,
   everything else below it.
5. Write Content as numbered parts, each opening with a caption, a
   `/diagram-ascii` figure and a short intro.
6. Write Aims, their States, and Files. When another Page supplies necessary
   context, add only the exact Related Board Pages row and scope the current
   phase needs.
7. Register the page in the board's `board.md` roster.
8. Build, check, and read the RENDER. Report the page's finding count, not the
   fact that you finished.

### Work on an existing page

ONE page is the deliverable, and steps 7 and 8 are what bound it. They exist
because scope is the one thing this verb got measured on and failed: three
fresh agents each given one sentence all drove their page to zero findings,
then disagreed completely about how far to reach, one writing to a single file
and another to fifteen including four shipped `SKILL.md` files and six sibling
pages. Neither was wrong on the merits; the skill simply never said where to
stop.

1. Read the whole target file first, including Content, Aims, States, Files and
   the settled folds. If Files declares Related Board Pages, resolve the current
   phase with `cli/pagecontext.py` and read that one-hop packet before changing
   prose.
2. Run the checker on it and work its list. Every finding names the rule it
   breaks and the part it is in, so nothing has to be read to know what to do.
3. Fix the MECHANICAL findings first, in bulk: dead `## Files` paths, a part
   with no figure, a figure with no caption, a group name that drifted. None
   needs judgment.
4. Then read for what no checker reaches: the weak-English axis, whether each
   part still answers one question, whether the Opening's visible paragraph says
   anything the title did not.
5. If a fix reveals a rule nobody wrote down, write it in three places: the
   owning page, `haipipe-board/ref/page-template.md`, and this file. A repair
   that stops at one page will be needed again next week.
6. Build, check, read the render, and report the before and after counts.
7. A write outside the target page is allowed only when the page CANNOT be made
   correct without it, and every such write is named in the report, with the
   reason, file by file.
8. Never rewrite a sibling page's content. Repointing a citation your own
   renumbering broke is repair; rewriting the page that citation lands in is a
   second job, and it belongs to that page's own turn.

### Run one page lifecycle

RUN is the automatic, bounded loop, and it lives with the workflow it drives:
saying `run <page>` here loads `page-workflows/haipipe-page-workflow` and
follows its procedure.

🚫 **The dispatch stays in the session you typed it in.** A subagent is not
handed the `Workflow` tool, so `run <page>` may not be handed off to any agent;
an agent dispatched to do it returns `blocked` with 0 steps. The packet,
receipt, role-separation and stop rules are that skill's
`ref/page-run-contract.md`; the receipts land under
`<board>/_runs/page/<page-id>/`. This door keeps only the two rules a caller
needs before handing off: a NEW Page is CREATEd and registered here first and
then RUN starts at OUTLINE, and an existing Page with no known next authority
starts at CHECK.

The engine the direct verbs call, so nobody has to remember it:

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^<PAGE>'
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --summary
```

`watch.py` rebuilds on any `.md` save, so "build" is usually already done; a
change to `.py`, `.css` or `.js` is not watched and needs the build run once.

## ✍️ What a write may touch

Load this skill and `haipipe-board/ref/writing-rules.md` directly before
writing. Do not copy their requirements into an assignment prompt: a copied
checklist becomes a second prose authority and drifts.

**A CHANGE IS FINISHED WHEN IT IS ON THE RENDERED PAGE**, and nobody is asked
for permission on the way. The unit of work is a visible page, not an edit.
Carry every change all the way through: write the source, propagate the rule to
`haipipe-board/ref/page-template.md` and to this file so a new page inherits it,
run `check.py`, then confirm the RENDER rather than the markdown. Stopping
mid-way to ask for a go leaves the change half-applied, which is strictly worse
than either finishing or not starting. Verify on the artifact a reader opens:
source-is-correct is not page-is-correct, and a dead watcher and a shut
`<details>` each produced a correct file and a wrong page.

**The write anchor rule.** A machine write lands at a SECTION BOUNDARY, never at
a byte offset: a concurrent session once spliced a `###` block into the middle
of another page's `## Opening` sentence. Appending under a named `##` heading is
safe; inserting by offset is how that damage reproduces at scale.

**The human-decision rule.** A verb reading a transcript can report what the
transcript CLAIMS, not verify it. So a machine may update an Aim's State only
from evidence it can inspect, and may propose a human ruling as a
`### Decision Now` row.

### The title states a purpose, in sentence case

Capitalize the first word and proper nouns and nothing else; a defined term
keeps its capitals. A colon may carry a short subtitle, and that is usually
where the purpose lands: `The page template: one grammar every page kind obeys`
rather than `Page Template design`, which mixes two cases and names only a
topic. On the Index the title is the only line a reader gets before choosing, so
a title naming its subject alone makes them open the page to learn what the page
was for. Sentence case is a string test a checker can own; whether the title
states a purpose is a judgment and belongs to the Evaluation contract.

### A heading is a lookup key

The same problem one level down, and it governs this contract's own `##`
headings, every page's `###` Content divisions, and every skill's H1. Five
tests, each mechanical:

```text
① states the LAW, not the topic   `One key claims a page`, never `Page Types`
                                   a reader should learn the rule from the
                                   heading alone
② no count                        a number in a heading rots · `Seven Page
                                   Phases` said `Four` until the split
③ no date                         a heading carrying a date is a record, not
                                   a law
④ no self-reference               the heading names the SUBJECT, never this
                                   document · `…and this skill is the door for
                                   all three` is about the file
⑤ a clause after the comma        it must rule out a MISTAKE the first half
   earns its place only by         leaves open · `Write for the render, not
   ruling out a real mistake       the source` keeps it, because verifying the
                                   markdown is what people actually do ·
                                   `A heading is a lookup key, not a sentence`
                                   loses it: a lookup key already is not one
```

Test ⑤ is the one that catches machine prose. Its tell is a comma followed by a
qualifying phrase, which reads like a writer who could not choose between two
headings and shipped both, and its commonest form is the negative restatement:
say it, then say it again inverted for rhythm. Grep the tell with
`grep -n '^#\+ .*, '` and ask of each hit what mistake the clause prevents; a
heading that answers nothing loses the clause, not the heading.

An H1 says what the skill DOES for its reader, as a verb phrase:
`judge one version and name its next authority` lands where a noun phrase about
the document does not.

### Write for the render, not the source

THE FIRST BLANK LINE IN `## Opening` IS THE SPLIT. Above it is the ONE
paragraph a reader sees without clicking, joined into a single block; below it
is the `More details` drawer, behind a click. Nothing reports a blank line in
the wrong place, so the failure mode is a page whose Opening renders as one bare
question while its explanation sits unread. The visible paragraph is 4-5
sentences, about five lines on screen: target ~450 characters, HARD CEILING 520,
measured on the RENDER and enforced by `check.py`
(`OPENING_MAX_STAGE_CHARS`). Write it in PLAIN ENGLISH for a reader whose
English is weak: a shorter common word always beats a precise rare one. Its
shape is the question, what the question's own words mean, why that is hard,
what this page decides. NEVER open with a list that will grow: name examples and
say the set grows, so a fourth member never forces an edit.

`## Writing Style` is a `###` INSIDE Opening, because a top-level section
answers a reader's question about the SUBJECT while this one answers a writer's
question about the PAGE. On the main run it sat between Diagram and Content
asking the reader to skip it; inside the drawer it is one click from whoever
needs it and invisible to whoever does not. The top-level form still parses,
because pages carry it and deleting someone else's text on read would be a
silent loss.

EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT. Write
`**Name**: what this diagram shows.` directly above the fence, one line only. A
section may hold several figures, and an unlabelled one makes the reader decode
it before learning what it is; the caption goes ABOVE because an explanation
that arrives after the figure arrives too late.

CONTENT IS NUMBERED ALL THE WAY DOWN. A division is `### 3 · Content`, a group
inside it is `**3.2 · Group title**`, and a paragraph is
`#### 3.2.1 · Its heading`; an ungrouped division numbers its paragraphs
`#### 3.1 ·` straight through, so the depth of the number says whether a group
exists. Numbering is also a defect detector: it exposes a group holding exactly
one paragraph, which is the floating-group-title defect, and it gives every
paragraph a name a person can say in chat.

`More details` IS A LIST OF LABELLED PARTS, NEVER ONE BLOCK OF PROSE. Each part
starts with a bold label saying what it answers, then its sentences, with a
blank line between parts. The two halves of an Opening have two different
readers: the paragraph on stage is read straight through by someone deciding
whether to stay, while `More details` is opened by someone who already decided
and is hunting one specific thing.

A FIGURE ROW IS A LABEL AND ITS VALUE, NEVER A CLAUSE. If a row could end in a
period it is prose, and it belongs in the paragraph under the figure rather than
inside the fence. A figure earns its fence by being scannable.

The `state:` line is a row, not a paragraph. After the status word come at most
two ` · ` parts: what stands, then `open:` with a short list or a count. Keep
the whole line under 110 characters; `check.py` warns past that. A part that
could end in a period is prose: the facts belong in States and the reason in
Log, so the line only points. Good:
`🟡 PARTIAL · ruled, card grammar adopted · open: landing address, citation hop`.

The rationale's FIRST job is to define the words the question itself uses. A
sharp lead question is specific, and being specific usually means naming this
board's own things, so the sharper the question the more it leans on vocabulary
a cold reader does not have. Give each such term one line with a REAL EXAMPLE,
never a restatement: `a lifecycle-stage page carries one stage of a paper being
written, such as its Results section` lands where `a lifecycle-stage page
represents a stage` does not. Only then place the page on the board, and only
then argue the stake. Names chosen in the question bind the rest of the page and
must be used identically in Content and Law. The rationale has no required
sentence count and no required rhetorical order; use as many short sentences as
the page needs, then stop when a cold reader can say what the page asks, why it
deserves attention, and what this page owns.

Speak about the subject whenever possible. `This page defines …`,
`The hard part is …` and `It succeeds when …` are not forbidden phrases, but a
writer may not use them as a reusable scaffold. If the paragraph still fits
another page after its nouns are replaced, it is generic and must be rewritten.
Move frameworks, implementation history, evidence inventories, current status
and plans to their owning sections instead of using them to pad the Opening.

Before writing back, run a local self-check: compare the question and rationale
with the whole target page and remove any promise the page does not support;
remove any sentence whose only job is filling a category; apply the
noun-substitution test; preserve one sentence per source line, English only, and
the no-em-dash rule. This self-check improves the draft but never approves it. A
fresh reviewer judges the page after the writer's context is gone.

### Decision Now

One name is RESERVED inside States: `### Decision Now` holds the decisions a
machine proposes and the human must make, one `- [ ]` row each carrying the ask,
the options, and a recommendation. A proposal never lives only in chat: it is
written there on the owning page, the human answers by ticking, and an answered
row moves into the page's dated record.

The options take ONE LINE EACH, and each line says what choosing it commits you
to. Three labels crammed onto one line name the options and explain none, so the
reader has to reconstruct the consequences before they can choose. The
recommendation is its own line, naming the letter and why it beats the others.

```markdown
- [ ] 🗣 The ask, stated as one question
      One or two lines of context: what is true today, and what it costs.
      A · the first option, and what choosing it commits you to.
      B · the second option, and what it commits you to.
      → CC recommends B, because <the reason it beats A>.
```

A machine CLOSES a row once the human has answered it, and records the answer in
the same write: which option, who ruled, when, and the words they used. What it
may never do is close a row nobody answered, or flip a page-level human gate.
Answered means the human said it: in chat, in a comment lane, or by ticking. A
machine's own recommendation is not an answer, however confident it is.

## 🔍 How a page is judged

Evaluation asks whether the authored page satisfies its declared requirements;
it does not ask whether the reviewer personally likes the format. The
requirements stay here, in the page spec and its cited template, rather than
being copied into a second evaluation skill. The evaluator is a consumer of this
contract.

Resolve applicable requirements in this order:

1. The base section contract in this skill and `ref/page-template.md`.
2. The Page Type variant, when one exists.
3. The current Page Phase contract, when the review concerns work performed
   under DRAFT, EVIDENCE, REVISE, or CHECK.
4. The Page's own `## Writing Style`; on S Pages, also its `## Stage Contract`.
5. The local `###` division purpose and each `####` heading's immediately
   following `(job line)`, when present.

A more specific source may refine a broader one but may not silently contradict
it. When two sources disagree, report a requirement conflict and stop judging
that criterion until the owner resolves it.

Review four distinct axes:

| Axis | Question | Judge |
|---|---|---|
| Mechanics | Is the required structure present, ordered, addressable, and internally consistent? | `check.py` |
| Function | Does this section answer the reader question the contract assigns to it? | semantic reviewer |
| Evidence | Can every factual compliance claim point to visible text, a State row, or a linked artifact? | semantic reviewer |
| Readability | Can a zero-background reader understand the section without supplying a missing premise? | fresh-context reviewer |

The review units are every present `##` section, every direct `###` Content
division, and every `####` paragraph whose local job must be tested. Use exactly
four verdicts: `MEETS`, `NEEDS WORK`, `N/A`, and `NOT VERIFIABLE`. `N/A` means a
rule genuinely does not apply; `NOT VERIFIABLE` means the required evidence is
unavailable and is never a pass.

When the same section changes on several pages, the batch is an additional
readability unit. Read those sections consecutively in Board order after judging
them page by page. A sentence can be clear alone and still fail in the batch when
several pages reuse its opening stem, rhetorical sequence, or generic success
ending. The batch NEEDS WORK when prose is interchangeable after noun
substitution or when repeated scaffolds make distinct pages sound like one form
letter. Do not repair this by demanding cosmetic synonym changes; the smallest
fix is to restate each page's actual stake in its own natural order.

The report is one row per review unit:

```text
unit | applicable requirements + source | verdict | evidence | smallest fix
```

Then report requirement conflicts, mechanical findings, and one page-level
verdict. The review is read-only: it never edits prose, changes an Aim State,
ticks Decision Now, or closes a page.

Execution uses existing surfaces rather than a new skill: `check.py --strict`
supplies the deterministic mechanical findings, the page's `✅ Quality Check`
runs the complete row-by-row rubric in the current page chat, and
`haipipe-board-reviewer-agent` runs the same contract in a fresh context after
revision and adds the batch voice gate. The quick check helps the author
iterate; only the fresh reviewer tests whether the page stands on its own
without conversation context.

## 🔤 The words

Every term this family uses is defined in `ref/glossary.md`, next to the path it
names. Card, unit, mark, plan, bullet, tick, bank, stake, phase: each one sits
beside the exact path it names, so nobody has to reconstruct a term from the
section that happened to introduce it. It restates no rule; where a word has an
owning section, the entry points there rather than copying it. Load it when a
reader asks what a word means, when writing for someone new to the family, or
when you catch yourself about to coin one:
`haipipe-board/ref/writing-rules.md` forbids a phrase that is neither the
source's own wording nor defined where a reader can find it.

## 🏷 How a location is written

```text
page        QB4            #QB4
face        QB4a           a page whose id carries its parent's number
group       #group-QB      scrolls the index, opens nothing
sentence    QB8's grammar  haipipe-sentence owns everything below the section
```

Every id inside a fenced figure renders as a link, so a contract that names
pages is itself a map.

## ✅ Closing checks

This contract is correct when each of these holds, and each is testable by
reading a named file:

- `pagetypes.py --check` exits 0: no key has live pages without a contract, and
  no key the engine accepts is unowned and unused.
- The generated inventory block matches `pagetypes.py` output; a hand edit
  inside the markers is a defect.
- Every heading passes the five tests in §✍️; `grep -n '^#\+ .*, '` returns only
  clauses that state a second rule.
- No section states a rule a cited authority already owns
  (`board-form.md` §4/§8, `page-template.md`, `writing-rules.md`) except where
  this file adds what a machine may write.
- No section narrates a retirement. What a key USED to mean lives in
  `CHANGELOG.md`; this file states what is true now.
- Every path this file names resolves on disk.
- Each `##` section answers one reader question and no other section's.

## 📂 Files

```text
haipipe-page/
├── SKILL.md            this contract
├── ref/
│   └── glossary.md     every word this family uses, with the PATH it names
└── CHANGELOG.md        version history, and the only home for retired rules
```

Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 (the
section mapping and requiredness) and §8 (on-stage order) as the authority; owns
no scripts. The inventory generator is
`haipipe-board/cli/pagetypes.py`, which lives with the machinery like every
other script this contract calls. The lifecycle packet and receipt spec belong
to `page-workflows/haipipe-page-workflow/ref/page-run-contract.md`.
