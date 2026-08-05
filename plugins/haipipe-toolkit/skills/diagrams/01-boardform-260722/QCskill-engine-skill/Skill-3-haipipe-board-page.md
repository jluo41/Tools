# haipipe-board-page · v0.20.1
state: 🟡 in flux · door test passed 260802, scope bound unmeasured
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-page` is the spec one Board Page is measured against and the door for CREATE, WORK ON, and RUN.
CREATE scaffolds one persistent Page.
WORK ON performs a known repair.
RUN follows bounded DRAFT, PROBE, REVISE, and CHECK routes until CLOSE or HOLD.
Load it when the unit is one Page; load `haipipe-board` when the Board itself is the subject.
This skill owns the Page contract and lifecycle receipt, while the Board skill owns rendering, checking, Workflow execution, and audit code.

**Where the line with `haipipe-board` runs**: both are doors, and the unit of work is what separates them.
Ask for a board and `haipipe-board` renders it, serves it and checks it.
Ask for a page and this skill decides what that page must contain, then calls those same scripts.
So the renderer, the write-back server, `check.py` and `ref/page-template.md` all live over there, and this skill cites the template rather than forking it.

**What the 260802 measurement showed**: the test removed every hint, giving three fresh agents one sentence each with no path, no skill name and no example page.
All three opened this skill unaided, at tool calls #5, #6 and #5, including the one phrased "can you clean up QF5-sentence-run for me", whose words match no trigger in the description.
They drove three pages from 15, 13 and 10 findings to zero.
The same run exposed what nobody had questioned: from that one instruction they wrote to 15 files, 1 file and 2 files, so the verb said where to start and never where to stop.
`0.10.0` wrote that bound in as steps 7 and 8, and no second run has measured it.

**What RUN adds**: an automatic run begins with an explicit raw-material packet and records one receipt per attempted Phase.
The producer writes, a mechanical worker rebuilds and identifies the exact source and render version, and a fresh reviewer performs CHECK.
The durable `_runs/page/` bundle and `pageflow.py` make illegal routes, self-approval, changed-after-check, missing human evidence, and exhausted limits visible.

**Covered elsewhere**: `haipipe-board-sentence` owns everything below a section, such as a comment lane attached to one sentence.
`haipipe-board-routing` is a consumer rather than a neighbour: it loads this contract to decide which page and which section an input belongs in.
`haipipe-board-page-for-skill` owns the Skill and Agent mirror kinds, and it is the variant this page itself is written to.

## Diagram
<!-- haipipe:skill:tree:start c2c826fa70d66d44 board/haipipe-board-page -->

**What `haipipe-board-page` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-board-page/
  ref/
    page-run-contract.md   195 ln  Page RUN contract
  CHANGELOG.md             292 ln  haipipe-board-page · Changelog
  SKILL.md                 468 ln  /haipipe-board-page · the page, as a contract you can load
```

<!-- haipipe:skill:tree:end -->

**How the Page contract is reached**: two direct verbs, one bounded lifecycle verb, and a pure spec load share the same door.

```text
WORKFLOW  three verbs and one spec load, from the same door

  ── loaded as a SPEC ──────────────────────────────────────────
  an agent with NO board open needs to know what a page is:
  routing picking a section · a variant author in another family
  (haipipe-paper-stage was the first; retired 260805, the stage
  variant now lives at page-types/for-stage) · the chat drawer, one day
        │  it READS the contract and writes nothing
        ▼
  the seven sections, in their fixed order, and what each one owes
  🧭 Opening  🖼 Diagram  📚 Content  🎯 Aims  📍 States  📎 Files  🗃 folds

  ── invoked as a VERB ─────────────────────────────────────────
  CREATE                 WORK ON                 RUN
  scaffold Page          perform known repair   route unknown next work
       │                       │                       │
       └──────────┬────────────┘                       ▼
                  ▼                         producer · builder · reviewer
        haipipe-board engine                     ↺ until CLOSE | HOLD
        build.py · check.py                 receipt → pageflow.py audit

  ── the bound, added at 0.10.0 because it was measured missing ──
  steps 7 and 8: ONE page is the deliverable. A write outside it is
  allowed only when the page cannot be made correct without it, and
  it must be named in the report. A sibling's CONTENT is never
  rewritten. Three fresh agents given the same instruction wrote to
  15 files, 1 file and 2 files: the verb said where to start and
  never where to stop.
```

## Content
<!-- haipipe:skill:body:start c2c826fa70d66d44 board/haipipe-board-page -->

**haipipe-board-page** · `0.20.1` · last shipped 2026-08-05

- folder   `board/haipipe-board-page/`
- tools    not declared
- summary  One resolution table covers ALL types: filename prefix, then the register's REQUIRED route: line, then the REQUIRED page-type: frontmatter key, then the stage and Q filenames; exactly one key matches or the page is defective.

### SKILL.md




`haipipe-board` is the door you walk through to RUN a board.
This skill is the door for ONE PAGE, and the spec that page is measured against. Say `create a new page on <topic>`, `working on <page>`, or `run <page>`; load it with no board open and it is a pure contract.
QC1b §1 on the design board states the test it passes: a consumer needs these rules with no board open.
Those consumers exist today: the routing verb deciding "which page, which section", the chat drawer priming a per-page session, and the variant authors in other families.

**The boundary, and it is a hard one:**

**Who owns what**: this skill holds the spec, `haipipe-board` holds the machinery.

```
haipipe-board-page               haipipe-board
─────────────────────            ──────────────────────────────
what a page IS                   rendering it (src/page_question.py)
the section contract             serving and write-back (cli/serve.py)
where a write may land           the checker (cli/check.py)
the base/variant model           the template file itself (ref/page-template.md)
```

This skill never CONTAINS the renderer, the server or the checker. It calls them, because a reader asking for one page should not have to know which script does what, and owning one page end to end is not the same as owning the machinery.
The authoritative template stays `haipipe-board/ref/page-template.md`; this contract cites it and must never fork it.


- 1 · 🧬 Page Types, one base
      A Page's TYPE comes from one machine-readable key on the page: a filename prefix, a declared register marker, or a frontmatter `page-type:` line.
      The type decides how the Page closes, what its Content holds, and which typed records it fills through the base frame's declared extension points.
      Everything else is the shared base (the model on the design board's QB4, JL 260729).
      The implementation may still call this field `kind`; the contract term is Page Type.
      **Type resolution**: one table for ALL types. Resolve ① to ⑤ in order and stop at the first key that matches.
      ```
      step  machine-readable key                            Page Type             contract
      ─────────────────────────────────────────────────────────────────────────────────────
      ①     filename Skill-<n>- or Agent-<n>-               Skill / Agent mirror  for-skill
            filename Meeting-<n>-                           Meeting               for-meeting
            filename QBv<n>-                                QBv venue             for-venue
      ②     `### Q-consumer register` + `route: outward`    Literature topic      for-literature
            `### Q-consumer register` + `route: inward`     Value topic           for-value
      ③     frontmatter `page-type: display`                Display unit          for-display
            frontmatter `page-type: slide`                  Slide deck            for-slide
            frontmatter `page-type: design`                 Design brief          for-design
            frontmatter `page-type: section`                Section unit          for-section
      ④     filename S-<Family>-<unit>-<slug>               Stage                 for-stage
      ⑤     filename Q<group><n>[<face>]-<slug>             Q decision            base only
      ```
      EXACTLY ONE step may claim a page, or the page is defective: a page no key matches, or one carrying two keys that disagree, is fixed on the page, never in the resolver.
      Step ② needs the register's `route:` line because the marker alone cannot tell the two topic routes apart; the line is REQUIRED, and `haipipe-board/ref/topic-entry-contract.md` declares it.
      Step ③'s `page-type:` line is REQUIRED on those four types' pages, and it BEATS the filename.
      That order settles the two real collisions: `S-Display-4c` wears a stage filename and is a display unit, so `page-type: display` resolves it at ③ before ④ can claim it; `QA4` wears a Q filename and is a slide deck, so `page-type: slide` resolves it before ⑤.
      Each type's contract states how it closes; the base's own type, the Q decision page, closes when every Aim is met or explicitly held, and mirror and Meeting pages are NEVER counted in a board's settled totals.
      `src/common.py` globs four filename prefixes, `Q`, `S`, `Agent` and `Meeting`, and that glob decides only what counts as a page at all; a `Skill-` page starts with the letter S, so it rides the `S` glob.
      Membership is the glob's whole job. The table above, not the glob, decides which type a page is.
      `Meeting-<n>` is generated by `cli/meetingpage.py`, and its contract is `haipipe-board-page-for-meeting`: talk is recorded there, ruled elsewhere.
      A Page Type used by one consumer family is a VARIANT of the base: it defines Content and may populate fixed extension points in Aims, States, and Stage Contract, but it never redefines, adds, removes, or reorders those frame sections.
      A variant ships WHERE THE BOARD FAMILY MAINTAINS IT (JL 260803).
      The ten Page Type variants maintained here live under `page-types/`; family-specific stage data, such as the paper door's `stages/` and craft files, remains in its own family.
      The earlier wording was "ships under its CONSUMER, never here", which broke when the venue variant landed because its consumer is the paper family and its maintainer is this one.
      This skill owns the BASE those variants extend.
      TEN Page Type variants ship under `page-types/`, and one of them must be loaded before you write the Page it governs:
      ```
      Skill-<n> · Agent-<n>   →  haipipe-board-page-for-skill      a page that mirrors a
                                                                   shipped unit and decides nothing
      QBv<n>                  →  haipipe-board-page-for-venue      a page per place a paper
                                                                   is submitted to
      S-<Family>-<unit>       →  haipipe-board-page-for-stage      a page per lifecycle stage
                                                                   of one paper or application
      topic, outward route    →  haipipe-board-page-for-literature a Q-consumer register asking
                                                                   what is already KNOWN
      topic, inward route     →  haipipe-board-page-for-value      a Q-consumer register asking
                                                                   what this project must PRODUCE
      display unit            →  haipipe-board-page-for-display    a unit a person must ACCEPT:
                                                                   figure, table, diagram
      section unit            →  haipipe-board-page-for-section    one reader-ordered unit, bound
                                                                   to its venue allocation
      Meeting-<n>             →  haipipe-board-page-for-meeting    talk recorded here, ruled
                                                                   elsewhere · NEVER counted
      slide deck              →  haipipe-board-page-for-slide      one division per slide, each
                                                                   embedding the deck LIVE via
                                                                   ?preview=N
      design brief            →  haipipe-board-page-for-design     one division per candidate,
                                                                   closes on a SELECTION record
      ```
      The last seven were admitted 260805 (JL, ruled on the design board's QB6; `-for-slide` on the Page-for-Slide branch).
      `-for-section` loads `-for-stage` the way the topic types load the topic core.
      It adds the section kind, the venue contract block, and the landing surface where citation, value, and display bindings reach prose.
      A section reads the venue BLUEPRINT, never the QBv catalog.
      `-for-meeting` closed a gap this section itself used to record: `Meeting-<n>` pages had a generator and no contract.
      Its one owned rule is that a spoken decision is not ruled until routed to the owning page.
      The two topic types resolve by the `### Q-consumer register` marker plus the register's REQUIRED `route:` line, the same marker `src/topic_entry_contract.py` already trusts.
      Their filenames look like stage-page filenames, which is why a filename cannot resolve them.
      Both LOAD `haipipe-board/ref/topic-entry-contract.md` for the anatomy and add only their route's translation layer.
      A display page is mirror-shaped but closes on human ACCEPTANCE of a render, not on a unit shipping.
      That is why it does not load `-for-skill`.
      A slide page shares that acceptance model at deck grain: one division per slide.
      Each division embeds the ONE deck file live, via html-ppt's `?preview=N` single-slide mode.
      The same file opened bare is the presentation.
      JL ruled the embed must be the html itself, and the boardform board's QA4 is the proving page (260805).
      A design page is the brief itself: its Opening states audience, goal, and constraints, and each Content division carries one CANDIDATE artifact.
      It closes on a SELECTION record naming the winner and each loser's disposition.
      It sits UPSTREAM of `-for-display`: design selects the candidate, display accepts its render.
      Load the matching one before writing or fixing any Page of those types.
      `haipipe-board-page-for-stage` names the ONE stage that reads a `QBv` Page and the four tiers deciding what crosses from that catalog into a draft.
      The first two listed types also do NOT take the `create a new page` steps below: they are GENERATED by `haipipe-board/cli/skillpage.py new`, which writes the Page from its own stub and registers it in `board.md` itself, so copying `ref/page-template.md` and registering by hand produces a Page with no managed spans that the checker then reports as broken forever.
      `haipipe-board-page-for-skill` exists because a mirror page DECIDES NOTHING, so this skill's Opening shape, which ends in `what this page decides`, leaves it with no question to ask; five skill and agent pages filled that empty slot with the same rhetorical question on 260802.

- 2 · 🎭 Four Page Phases, independent of Page Type
      A Page persists while the authority acting on it changes.
      The current phase is not another Page Type and is not inferred from the edit operation.
      ```text
      phase       authority                                     load
      ─────────────────────────────────────────────────────────────────────────────
      DRAFT       define or reopen purpose, Aims, promised shape page-phases/haipipe-board-page-draft
      PROBE       resolve a consequential unknown across the evidence wall
                                                               page-phases/haipipe-board-page-probe
      REVISE      improve the current promise while purpose and Aims stay fixed
                                                               page-phases/haipipe-board-page-revise
      CHECK       judge one version and route its next authority page-phases/haipipe-board-page-check
      ```
      Resolve one invocation in this order:
      ```text
      base Page contract
        → matching Page Type, when one exists
        → current Page Phase
        → family craft: the stage's declared craft files (and for probe, the family door's probe tooling), when paper or application adds artifact knowledge
      ```
      The four phases form a routing grammar, not a conveyor belt.
      Each may repeat, PROBE may be skipped when no consequential unknown exists, and CHECK may route to REVISE, PROBE, or DRAFT.
      Returning to DRAFT because purpose or Aims changed starts a new round on the same Page.
      Use the authority test when the visible operation is ambiguous:
      ```text
      purpose or Aims change                 → DRAFT
      an unanswered consequential fact moves → PROBE
      the same purpose and Aims are improved  → REVISE
      a concrete version is judged            → CHECK
      ```
      Adding, deleting, moving, and rewriting may be DRAFT or REVISE.
      The reason for the change decides.
      `RUN` is the router verb now that the automatic loop has a concrete contract.
      It is deliberately not called `ADVANCE`: a Page can repeat a phase, branch, HOLD, or return to DRAFT in a new round.
      The shared packet, receipt, version, role-separation, and stop rules live in `ref/page-run-contract.md`.

- 3 · 📑 The sections, in their fixed on-stage order
      **The sections in order**: what each owes a reader, and how much a machine may write into it.
      The AUTHORITY is `haipipe-board/ref/board-form.md` §4, which fixes the ON-STAGE order as five, `Opening → Diagram → Content → Aims → States`, with Files after them and the folds last. This skill adds no section to that list; the table below names the same run plus what a machine may write into each. `ref/page-template.md` carries more `##` headings than this because it also seeds the optional and folded ones.
      ```
      #   section            owes the reader                      phase authority
      ──────────────────────────────────────────────────────────────────────────────────
      1   Opening            the lead question + why it matters   DRAFT defines · REVISE clarifies
      2   Diagram            the figure; ids in it are links      DRAFT/REVISE, within Page Type rules
      3   Content            the substance, ### divisions         DRAFT defines · REVISE realizes
      4   Aims               durable Content-linked targets       DRAFT; changing intent starts a round
      5   States             one factual current State per Aim    any phase, from inspectable evidence
      6   Files              action map + scoped Page context      DRAFT/REVISE maintain
      7   folds              Discussion · Law · Lesson · Glossary · Log  the phase owning the record
      ```
      Each section answers ONE reader question, and the same five rows define every section's contract (JL 260801, ruled on the design board's QB4 §0): **conveys**, the reader question it answers · **holds**, the elements it must contain · **source**, how the author writes it · **rules**, what binds a write · **omit**, when it may be absent.
      **One reader question per section**: the question it answers, and when it may be left out.
      ```
      section            conveys · the reader question                omit
      ──────────────────────────────────────────────────────────────────────
      🧭 Opening          what is this page, why should I care?        never
      🖼 Diagram          can I see the whole subject at once?         when no figure helps: delete
      📚 Content          what does this page actually establish?      Q may · S never
      🎯 Aims             what should become true, and for which Content division? never
      📍 States           what is true now for each Aim, what waits?   never
      📎 Files            which few files or Page fragments continue this work? allowed, advised against
      🗃 folds            what was ruled, learned, changed, if needed  each optional
      ```
      A sentence answering another section's question is MISPLACED, and the protocol names its home: substance found in Opening moves to Content, Required Inputs and Venue move to Stage Contract, prose rules move to Writing Style, intended outcomes move to Aims, current facts move to States, and temporary next steps become an Aim's optional Plan.
      The full five rows per section live in the design board's `QB4` Content divisions; the authoritative source form stays `haipipe-board/ref/page-template.md`.
      An Aims or States group is `### A<n> · <emoji> <name>`, taking the NUMBER, NAME and EMOJI of the Content part it answers, so the three sections line up by eye as well as by id (JL 260802; it was `C<n>` until then, which made a reader translate one letter to see that `A3.1` belonged under it, and `C<n>` still resolves). `P` is for a target belonging to no single part. Ordinary Files groups are a MENU of actions, taken as they apply: ⚙️ Engines what RUNS the subject · 📋 Contracts what CARRIES a rule to other pages · 🧪 Checks what CATCHES a page breaking one · 📥 Input files what the work READS · 📤 Output files what a BUILD writes. Their names state an ACTION, never a subject, because a subject-named group rots the moment its subject leaves the page.
      `### 🔗 Related Board Pages` is the one fixed Files group. It is a selective context map between Pages, not a file dependency graph and not configuration inheritance. The fixed group name gives the checker a parser boundary; each row begins with the action-like relation that ordinary Files groups put in their heading:
      ```markdown
      ### 🔗 Related Board Pages · what this Page READS BY SCOPE
      - `reads · PROBE` · [QB7 §3](QB-research/QB7-literature.md)
        Read the evidence boundary before resolving this Page's consequential unknown.
      ```
      The four relations are `reads`, `constrained by`, `continues`, and `contrasts`. The phase is `DRAFT`, `PROBE`, `REVISE`, `CHECK`, or `ALL`. The target is a Board-root-relative Page source. Its visible id must match that Page. Scope is `page` or one direct Content division such as `§3` or `§3.2`; a division read automatically carries the target Page's identity, Opening, and matching Aims/States group so the fragment does not arrive without its promise and current state. When one packet selects several divisions from the same target Page, identity and Opening are emitted once rather than repeated per row.
      Read the current Page whole first. Then run `python3 <board-skill>/cli/pagecontext.py <current-page.md> --phase <PHASE>` and load only the returned packet. The reader follows one hop: it never traverses Related Board Pages declared by a target Page. Cycles are therefore harmless, context stays bounded, and a phase sees only rows written for it or for `ALL`. `check.py` rejects a malformed row, a path outside the Board, a dead Page, a mismatched Page id, or a missing scope before an agent can silently work without that context.
      An Aim is not a task. Write `- A3.1 · target` for a result owned by Content part 3, under the group `### A3`, and `P1` only for a target that genuinely crosses parts. One division may have zero, one, or many Aims. Each Aim has a testable `Done when` and may carry a temporary `Plan`; changing Plan does not change the Aim.
      The section labels are deliberately both plural: `Aims` contains Aim records and `States` contains their State records. States mirrors every Aim id exactly once: `⬜` not started, `🔨` being worked on now, `🧠` waiting on a person or something outside this page, `✅` met with the evidence named, or `❄️` on ice, held on purpose. Each says its meaning by SHAPE (JL 260802); the old `🟡` `🟠` `⏸️` still parse. This is the AIM vocabulary and NOT the page `state:` line, which keeps its own ✅ 🟡 🔴 ⏸️ set and is checked apart. The section is a snapshot, so the reason for a transition belongs in Log. The strict one-to-one relationship is Aim to current State row, never Content division to Aim.

- 4 · 🚪 Three verbs, and this skill is the door for all three
      Say any of these and this skill runs it. You never call the engine yourself.
      ```
      📄 CREATE     /haipipe-board-page create a new page on <topic>   [on <board>]
      🔧 WORK ON    /haipipe-board-page working on <page>              or just the path
      🔁 RUN        /haipipe-board-page run <page> [from <phase>]
      ```
      `haipipe-board` owns the machinery and this skill owns the contract, which is why the boundary above says this skill never renders, serves or checks: it does not CONTAIN that code. It does CALL it. A page is one unit of work, and a reader asking for one page should not have to know which script does what.

- 4.1 · 📄 create a new page on a topic
      1. Resolve the board folder, and the group the page belongs to. Ask ONLY if the group is genuinely ambiguous.
      2. Pick the id (`Q<group><n>-<slug>`, or `S-<Family>-<unit>-<slug>` for a lifecycle stage) and copy `haipipe-board/ref/page-template.md` to it. Never retype the shape from memory: the template's guide sentences ARE the contract.
      3. Write the title so it states the page's PURPOSE, in sentence case.
      4. Write the Opening: the visible paragraph above the first blank line, everything else below it.
      5. Write Content as numbered parts, each opening with a caption, a `/diagram-ascii` figure and a short intro.
      6. Write Aims, their States, and Files. When another Page supplies necessary context, add only the exact Related Board Pages row and scope the current phase needs.
      7. Register the page in the board's `board.md` roster.
      8. Build, check, and read the RENDER. Report the page's finding count, not the fact that you finished.

- 4.2 · 🔧 working on an existing page
      Scope is the one thing this verb got wrong when it was measured. On 260802 three fresh agents were each given one sentence and nothing else, and all three found this skill unaided and drove their page to zero findings. They then disagreed completely about how far to reach: one wrote to a single file, its own page; another wrote to fifteen, including four shipped `SKILL.md` files, four `CHANGELOG.md` files, six sibling pages and the shared `board.md`. Neither was wrong on the merits, and the wide one was fixing citations a renumbering really had broken. The skill simply never said where to stop, so steps 7 and 8 below now do.
      1. Read the whole target file first, including Content, Aims, States, Files and the settled folds. If Files declares Related Board Pages, resolve the current phase with `cli/pagecontext.py` and read that one-hop packet before changing prose.
      2. Run the checker on it and work its list. Every finding names the rule it breaks and the part it is in, so nothing has to be read to know what to do.
      3. Fix the MECHANICAL findings first, in bulk: dead `## Files` paths, a part with no figure, a figure with no caption, a group name that drifted. None needs judgment.
      4. Then read for what no checker reaches: the weak-English axis, whether each part still answers one question, whether the Opening's visible paragraph says anything the title did not.
      5. If a fix reveals a rule nobody wrote down, write it in three places: the owning page, `haipipe-board/ref/page-template.md`, and this file. A repair that stops at one page will be needed again next week.
      6. Build, check, read the render, and report the before and after counts.
      7. ONE page is the deliverable. Step 5 sends you to other files on purpose, and this step bounds it: a write outside the target page is allowed only when the page CANNOT be made correct without it, and every such write is named in the report, with the reason, file by file.
      8. Never rewrite a sibling page's content. Repointing a citation your own renumbering broke is repair; rewriting the page that citation lands in is a second job, and it belongs to that page's own turn.

- 4.3 · 🔁 run one Page lifecycle
      RUN is the automatic, bounded loop. Use it when the process itself must be
      exercised and audited, rather than when one known edit is enough.
      1. Read `ref/page-run-contract.md` and assemble its raw-material packet. Resolve
         the Page Type from the filename. For a new Page, CREATE and register it first,
         then start at DRAFT. For an existing Page with no known next authority, start
         at CHECK. Before each phase dispatch, materialize that phase's Related Board
         Pages packet with `cli/pagecontext.py`; an invalid row or missing scope is a
         named HOLD, never omitted context.
      2. Invoke `haipipe-board/ref/page-lifecycle.workflow.js` with the packet. The
         workflow dispatches a phase-scoped producer for DRAFT, PROBE, or REVISE, a
         mechanical builder/version snapshot, and a fresh read-only reviewer for
         CHECK.
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
      The engine the direct verbs call, so nobody has to remember it:
      ```bash
      python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
      python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^<PAGE>'
      python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --summary
      ```
      `watch.py` rebuilds on any `.md` save, so step "build" is usually already done; a change to `.py`, `.css` or `.js` is not watched and needs the build run once.

- 5 · ✍️ What CREATE and WORK ON write to
      Load this skill and `haipipe-board/ref/writing-rules.md` directly before writing.
      Do not copy their requirements into an assignment prompt: a copied checklist becomes a second prose authority and drifts.
      For an existing page, read the entire target file before changing any section, including Content, Aims, States, Files, and settled folds.
      A CHANGE IS FINISHED WHEN IT IS ON THE RENDERED PAGE, and nobody is asked for permission on the way (JL 260801: "don't wait me to say go next time, just go ahead and don't stop until the content is updated in the Page").
      The unit of work is a visible page, not an edit.
      Carry every change all the way through: write the source, propagate the rule to `haipipe-board/ref/page-template.md` and to this file so a new page inherits it, run `check.py`, then confirm the RENDER rather than the markdown.
      Stopping mid-way to ask for a go leaves the change half-applied, which is strictly worse than either finishing or not starting: a renamed label with a dozen sentences still naming the old one, or a rule written on one page and in no template.
      Verify on the artifact a reader opens, because source-is-correct is not page-is-correct: a dead watcher and a shut `<details>` each produced a correct file and a wrong page.
      The page's own source is what keeps a rewritten Opening from promising something the rest of the page does not establish.
      The title is a phrase in SENTENCE CASE that says what the page is FOR (JL 260801, ruled on the design board's QB4 §8). Capitalize the first word and proper nouns and nothing else; a defined term keeps its capitals. A colon may carry a short subtitle, and that is usually where the purpose lands: `The page template: one grammar every page kind obeys` rather than `Page Template design`, which mixes two cases and names only a topic. On the Index the title is the only line a reader gets before choosing, so a title naming its subject alone makes them open the page to learn what the page was for. Sentence case is a string test a checker can own; whether the title states a purpose is a judgment and belongs to the Evaluation contract below.
      An Opening keeps one fixed physical shape: one real question paragraph, then one plain rationale paragraph.
      THE FIRST BLANK LINE IN `## Opening` IS THE SPLIT (JL 260801, ruled on QB4 §1). Above it is the ONE paragraph a reader sees without clicking, joined into a single block; below it is the `More details` drawer, behind a click. Nothing reports a blank line in the wrong place, so the failure mode is a page whose Opening renders as one bare question while its explanation sits unread. The visible paragraph is 4-5 sentences, about five lines on screen: target ~450 characters, HARD CEILING 520, measured on the RENDER. 520 is what `check.py` enforces (`OPENING_MAX_STAGE_CHARS`); ~450 is the comfortable length, not the limit. Write it in PLAIN ENGLISH for a reader whose English is weak: a shorter common word always beats a precise rare one. Its shape is the question, what the question's own words mean, why that is hard, what this page decides. NEVER open with a list that will grow: name examples and say the set grows, so a fourth member never forces an edit; the roster lives in the Content division that owns it.
      EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT (JL 260801, ruled on QB4 §2). Write `**Name**: what this diagram shows.` directly above the fence, one line only. A section may hold several figures, and an unlabelled one makes the reader decode it before learning what it is; the caption goes ABOVE because an explanation that arrives after the figure arrives too late.
      CONTENT IS NUMBERED ALL THE WAY DOWN (JL 260801, ruled on QB4 §1). A division is `### 3 · Content`, a group inside it is `**3.2 · Group title**`, and a paragraph is `#### 3.2.1 · Its heading`; an ungrouped division numbers its paragraphs `#### 3.1 ·` straight through, so the depth of the number says whether a group exists. This is the same rule the board applies one level up with `§6` against `§6.1`. Numbering is also a defect detector: it exposes a group holding exactly one paragraph, which is the floating-group-title defect, and it gives every paragraph a name a person can say in chat.
      `More details` IS A LIST OF LABELLED PARTS, NEVER ONE BLOCK OF PROSE (JL 260801, ruled on QB4 §1). Each part starts with a bold label saying what it answers, then its sentences, with a blank line between parts. The two halves of an Opening have two different readers: the paragraph on stage is read straight through by someone deciding whether to stay, while `More details` is opened by someone who already decided and is hunting one specific thing, so they scan for a label instead of reading from the top.
      A FIGURE ROW IS A LABEL AND ITS VALUE, NEVER A CLAUSE (JL 260801, ruled on QB4 §2). If a row could end in a period it is prose, and it belongs in the paragraph under the figure rather than inside the fence. A figure earns its fence by being scannable; a wall of clauses in a box is slower to read than the same clauses outside it.
      The rationale's FIRST job is to define the words the question itself uses (JL 260801, ruled on QB4 §1). A sharp lead question is specific, and being specific usually means naming this board's own things, so the sharper the question the more it leans on vocabulary a cold reader does not have. Give each such term one line with a REAL EXAMPLE, never a restatement: `a lifecycle-stage page carries one stage of a paper being written, such as its Results section` lands where `a lifecycle-stage page represents a stage` does not. A restatement passes the author's own eye as an explanation, because the author already knows what the word means. Only then place the page on the board (the bearing rule), and only then argue the stake: a reader who cannot parse the question cannot be told where the page sits or why it matters. Names chosen in the question bind the rest of the page and must be used identically in Content and Law.
      The rationale has no required sentence count and no required rhetorical order.
      Use as many short sentences as the page needs, then stop when a cold reader can say what the page asks, why that question deserves attention, and what this page owns.
      Difficulty, failure, downstream effect, and a success consequence are diagnostic prompts for missing stakes, not four slots to fill and not one sentence each.
      Speak about the subject whenever possible.
      `This page defines ...`, `The hard part is ...`, and `It succeeds when ...` are not forbidden phrases, but a writer may not use them as a reusable scaffold.
      If the paragraph still fits another page after its nouns are replaced, it is generic and must be rewritten.
      Move frameworks, implementation history, evidence inventories, current status, and plans to their owning sections instead of using them to pad the Opening.
      Before writing back, run a local self-check:
      1. Compare the question and rationale with the whole target page; remove any promise the page does not support.
      2. Remove any sentence whose only job is filling a category such as difficulty, downstream, or success.
      3. Apply the noun-substitution test; wording that could introduce a sibling page is not page-specific enough.
      4. Preserve one sentence per source line, English only, and the no-em-dash rule.
      This self-check improves the draft but never approves it.
      A fresh reviewer judges the page after the writer's context is gone.

- 6 · ✅ Evaluation contract
      Evaluation asks whether the authored page satisfies its declared requirements; it does not ask whether the reviewer personally likes the format.
      The requirements stay here, in the page spec and its cited template, rather than being copied into a second evaluation skill.
      The evaluator is a consumer of this contract.
      Resolve applicable requirements in this order:
      1. The base section contract in this skill and `ref/page-template.md`.
      2. The Page Type variant, when one exists.
      3. The current Page Phase contract, when the review concerns work performed under DRAFT, PROBE, REVISE, or CHECK.
      4. The Page's own `## Writing Style`; on S Pages, also its `## Stage Contract`.
      5. The local `###` division purpose and each `####` heading's immediately following `(job line)`, when present.
      A more specific source may refine a broader one but may not silently contradict it.
      When two sources disagree, report a requirement conflict and stop judging that criterion until the owner resolves it.
      Review four distinct axes:
      | Axis | Question | Judge |
      |---|---|---|
      | Mechanics | Is the required structure present, ordered, addressable, and internally consistent? | `check.py` |
      | Function | Does this section answer the reader question the contract assigns to it? | semantic reviewer |
      | Evidence | Can every factual compliance claim point to visible text, a State row, or a linked artifact? | semantic reviewer |
      | Readability | Can a zero-background reader understand the section without supplying a missing premise? | fresh-context reviewer |
      The review units are every present `##` section, every direct `###` Content division, and every `####` paragraph whose local job must be tested.
      Use exactly four verdicts: `MEETS`, `NEEDS WORK`, `N/A`, and `NOT VERIFIABLE`.
      `N/A` means a rule genuinely does not apply; `NOT VERIFIABLE` means the required evidence is unavailable and is never a pass.
      When the same section changes on several pages, the batch is an additional readability unit.
      Read those sections consecutively in Board order after judging them page by page.
      A sentence can be clear alone and still fail in the batch when several pages reuse its opening stem, rhetorical sequence, or generic success ending.
      The batch NEEDS WORK when prose is interchangeable after noun substitution or when repeated scaffolds make distinct pages sound like one form letter.
      Do not repair this by demanding cosmetic synonym changes; the smallest fix is to restate each page's actual stake in its own natural order.
      The report is one row per review unit:
      **The evaluation row**: one row per reviewed unit, so a failed criterion points straight at its repair.
      ```text
      unit | applicable requirements + source | verdict | evidence | smallest fix
      ```
      Then report requirement conflicts, mechanical findings, and one page-level verdict.
      The review is read-only: it never edits prose, changes an Aim State, ticks Decision Now, or closes a page.
      Execution uses existing surfaces rather than a new skill:
      - `check.py --strict` supplies the deterministic mechanical findings.
      - The page's `✅ Quality Check` runs the complete row-by-row rubric quickly in the current page chat.
      - `haipipe-board-reviewer-agent` runs the same contract in a fresh context after revision and adds the batch voice gate when several pages changed.
      The quick check helps the author iterate; only the fresh reviewer tests whether the page stands on its own without conversation context.
      There is NO `## Boundary` section (JL 260731, said twice). It was added by CC on 260723 and never ruled in. What a page covers is the Opening's job; point at a neighbouring page from the prose that needs it, as a `**Covered elsewhere**:` part in the Opening's drawer.
      The same ruling renamed three sections: `## Question` -> `## Opening`, `## Items to Finish` -> `## Aims`, `## Where we are` -> `## States`. `src/common.py` still ALIASES every old name, so a page on the old vocabulary keeps rendering correctly. Do not read that as permission. This skill claimed the removal was finished on 260731; on 260802 the board still had 26 `## Boundary` sections and 45 of 55 pages on the old names, because a forgiving renderer means nobody ever sees the drift. `check.py` now reports every retired name as `retired-section`, which is the only reason this paragraph can be trusted.
      One name is RESERVED inside States (JL 260731): `### Decision Now` holds the decisions a machine proposes and the human must make, one `- [ ]` row each carrying the ask, the options, and a recommendation.
      One exception is UNSETTLED and admitted: the paper board's S pages use `### Needs JL · tick these`, which JL approved four days before this reservation, and neither ruling supersedes the other in writing; keep each board's local name until JL rules once for both (the conflict is recorded in `page-types/haipipe-board-page-for-stage`).
      A proposal never lives only in chat: it is written there on the owning page, the human answers by ticking, and an answered row moves into the page's dated record.
      The options take ONE LINE EACH, and each line says what choosing it commits you to (JL 260731: "I want the decision A, B, C, to be in a new line and explain each options, not all the options in one line").
      Three labels crammed onto one line name the options and explain none, so the reader has to reconstruct the consequences before they can choose.
      The recommendation is its own line, naming the letter and why it beats the others.
      **A Decision Now row**: the shape a page uses to put one choice in front of a human.
      ```markdown
      - [ ] 🗣 The ask, stated as one question
            One or two lines of context: what is true today, and what it costs.
            A · the first option, and what choosing it commits you to.
            B · the second option, and what it commits you to.
            → CC recommends B, because <the reason it beats A>.
      ```
      **The write anchor rule (QC1b §4, from a real casualty).**
      A machine write lands at a SECTION BOUNDARY, never at a byte offset: on 260730 a concurrent session spliced a `###` block into the middle of another page's `## Opening` sentence.
      Appending under a named `## ` heading is safe; inserting by offset is how that damage reproduces at scale.
      **The human-decision rule (QC1b §5).**
      A verb reading a transcript can report what the transcript CLAIMS, not verify it.
      So a machine may update an Aim's State only from evidence it can inspect, and may propose a human ruling as a `### Decision Now` row.
      **Closing a row (JL 260802, amending the never-tick rule).**
      A machine CLOSES a `### Decision Now` row once the human has answered it, and records the answer in the same write: which option, who ruled, when, and the words they used.
      What it may never do is close a row nobody answered, or flip a page-level human gate.
      The old rule left every answered row open, so a page showed decisions as pending that had been made hours earlier and acted on, which is the same drift the board exists to prevent.
      Answered means the human said it: in chat, in a comment lane, or by ticking. A machine's own recommendation is not an answer, however confident it is.

- 7 · 🏷 Addressing
      **How a location is addressed**: what each level of the board is called, and how it is written.
      ```
      page        QB4            #QB4
      face        QB4a           a page whose id carries its parent's number
      group       #group-QB      scrolls the index, opens nothing
      sentence    QB8's grammar  haipipe-board-sentence owns everything below the section
      ```
      Every id inside a fenced figure renders as a link (haipipe-board 0.53.0), so a contract that names pages is itself a map.

- 8 · 📂 Files
      **This skill's own files**: what ships in the folder, and what each part is for.
      ```
      haipipe-board-page/
      ├── SKILL.md            this contract
      ├── CHANGELOG.md        version history
      └── ref/
          └── page-run-contract.md
      ```
      Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 (the section mapping and requiredness) and §8 (on-stage order) as the authority; owns no scripts.
      `ref/page-run-contract.md` is the shared lifecycle packet and receipt spec; executable workflow and audit machinery remain under `haipipe-board`.
      The named next step (QC1b §1): `live/chat.py`'s four hand-rolled rule strings (`CHAT_RULES`, `FULL_RULES`, `BOARD_CHAT_RULES`, `BOARD_FULL_RULES`) become this contract's consumers instead of restating it, which kills the copies, one of which has already rotted once.
### The other files

1 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
ref/page-run-contract.md     195 ln  Page RUN contract
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🧪 The door test passes on evidence rather than on argument
      Three fresh agents were given one sentence each, with no path, no skill name and no example page, and all three opened this door unaided at tool calls #5, #6 and #5.
      One of them was phrased "can you clean up QF5-sentence-run for me", whose words match no trigger in the skill's description, and it opened the door anyway.
      The same run drove three pages from 15, 13 and 10 findings to zero and took the board from 210 findings to 171.
- [ ] 🛑 The scope bound holds on a second measured run
      The same three agents wrote to 15 files, 1 file and 2 files from the same instruction, so what failed was never discovery, it was where to stop.
      0.10.0 added that bound as steps 7 and 8, and nobody has re-run the measurement since, so the fix is reasoning until a second run produces a tighter spread.
- [ ] 🧹 `live/chat.py` loads this spec instead of restating it
      Four rule strings there teach an agent the page and board contracts in Python prose, and `QB8d` already caught one describing a page shape that no longer existed.
      This is `A6.1` on `QC1b`, and it is the family's one real defect: the fix costs one function and adds no version surface.
- [ ] 🧩 A page can name the unit that supports it
      `QB8a · Evidence Card` should be able to say `supported by haipipe-board-sentence · Evidence Card` without duplicating the board-level roster.
      The syntax is unruled and no page carries one, which is `A7.1` on `QC1b`.

## States
This is the most proven unit in the family and also the one changing fastest: 23 releases to 0.20.1, and the only one whose door test was measured rather than assumed.
Its health is `🟡 in flux` because 0.10.0 shipped a bound that has not been re-measured, not because anything about it is unsettled.
It is also the base that variant doors extend, so the ten `page-types/` variants, the stage and display types among them, depend on this contract staying one file.

- 260802 CC · 🧪 The measurement, and the thing it accidentally proved instead
  The 260731 fan-out could not test the door: its brief pasted the path to `SKILL.md` and named `QB4` as the worked example, so all five agents read the contract as a plain file and not one of them invoked it.
  The real test removed every hint, and what it proved was the trigger surface; what it disproved was the scope, which had never been questioned.
  A test that only confirms what you expected has told you less than one that fails somewhere you were not looking.
- 260802 CC · 📄 The base and variant split makes this spec's second consumer real
  `haipipe-paper-stage` ships the S page kind under the paper family, which JL's base and variant model reads as the first variant door working as intended rather than as a leak.
  So this unit is not written only for routing: variant authors in other families resolve the same base contract, which is why a rule may never be forked into a variant.

## Log
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); haipipe-paper-stage no longer cited as live, the stage variant is page-types/for-stage and the release count reads 23 to 0.20.1.
260804 · Updated the authored mirror for the third Page verb: CREATE, WORK ON, and bounded RUN now appear together, including the producer, builder, reviewer, version receipt, and audit boundary.
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the spec load, the two verbs and the 0.10.0 scope bound, four real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in flux. The measured door test recorded as met, and its scope failure recorded as the one Aim it left open
260731 1115 · page generated from `board/haipipe-board-page/` by `skillpage.py new`

<!-- haipipe:skill:log:start c2c826fa70d66d44 board/haipipe-board-page -->

Converted from the skill's own `CHANGELOG.md`: 23 releases.

260805 · `0.20.1`
      Resolve-order slot reworded for thin-paper phase 2: the last slot is
      "family craft: the stage's declared craft files (and for probe, the family
      door's probe tooling)". Family-specific stage data (the paper door's stages/
      and craft files) stays in its own family; `haipipe-paper-stage` is retired.
260805 · `0.20.0`
      **One resolution table, every type machine-resolvable** (review fix). The stale
      "Six Page Types" table, written when six types existed, is replaced by a single
      resolution table covering ALL types, resolved in a fixed order: ① filename
      prefix (`Skill-`/`Agent-` → for-skill, `Meeting-` → for-meeting, `QBv` →
      for-venue), ② the register's REQUIRED `route: outward | inward` line
      (for-literature / for-value, declared in `haipipe-board/ref/topic-entry-contract.md`),
      ③ the REQUIRED frontmatter `page-type: display | slide | design | section`,
      ④ the `S-<Family>-<unit>` stage filename, ⑤ the Q filename. Exactly one key
      matches or the page is defective. A `page-type:` key beats the filename, which
      settles the S-Display-4c stage/display double match and the QA4 Q-file slide
      page.
      - Four stale self-contradictions fixed: the six-type heading and table; "the
        three Page Type variants maintained here" (ten); the "five implemented types
        need only four prefixes" sentence (the glob decides membership only, the
        table decides type); the claim that Meeting "has no contract in any skill"
        (it has for-meeting).
      - The admissions paragraph is split into short sentences; "ride the stage
        shape" now reads "look like stage-page filenames".
260805 · `0.19.0`
      **for-design admitted** (JL, ruled A on the design board's QB6; his definition,
      260805: "we want to design some messages, say message A, B, C for one group of
      people; the Content divisions ARE the different messages"). One page per design
      BRIEF, its Opening stating audience, goal, and constraints; one Content division
      per CANDIDATE, each carrying the artifact itself, its rationale, and its fit to
      the brief's criteria; Aims are the criteria. Closes on a SELECTION record naming
      the winner, why, and each loser's disposition (dropped · kept for A/B test ·
      merged). Sits upstream of for-display: design selects the candidate, display
      accepts its render. A losing division is never silently deleted, because the
      rationale for NOT choosing is part of the design record.
260805 · `0.18.0`
      **for-slide admitted** (JL, on the Page-for-Slide branch). One page per deck, one
      division per slide, each carrying its outline plus the PNG export of the built
      slide; the live html-ppt deck stays a linked artifact because the board strips JS.
      The slide binding (division · source · render · acceptance) is its typed record.
260805 · `0.17.0`
      **Two more Page Types admitted** (JL, same day, thought against the paper skill board and the MISQ board together).
      - `for-section`: loads `for-stage`, adds the section kind, the venue contract block (blueprint BINDING, style reference, override stated), and the landing surface for the three record types. Reverses the for-main rejection: Main is one family's region, section is a cross-family shape.
      - `for-meeting`: the routing rule for spoken decisions; Meeting pages stop being contract-less.
      - The types table's Meeting row now states the real closing rule.
260805 · `0.16.0`
      **Three Page Types admitted** (JL, QB6 Decision Now: D, plus display standing alone).
      - `page-types/haipipe-board-page-for-literature` and `-for-value`: two types over ONE loaded topic core (`ref/topic-entry-contract.md`), each adding only its route's translation layer. They resolve by the register marker plus route direction, not by filename.
      - `page-types/haipipe-board-page-for-display`: mirror-shaped, but its unit is produced by the project and closes on human acceptance of a specific render.
      - The Six Page Types section now lists six variants and says why the last three were admitted.
260805 · `0.15.1`
      **Nine review findings applied** (fresh-context cold read, verdict REVISE; JL: "go ahead to update it").
      - The Decision Now reservation now admits the unsettled S-page exception (`### Needs JL · tick these`) instead of stating the rule as settled while a variant contradicted it.
      - The "A CHANGE IS FINISHED" paragraph split to one sentence per line; the QC1b consumer chain split at its double colon.
      - The boundary figure names `cli/serve.py` and `cli/check.py` with their dir, as it already did for `src/`.
260804 · `0.15.0`
      - Adds `### 🔗 Related Board Pages` as the fixed, typed Files group for bounded
        cross-Page context rather than configuration inheritance or dependency
        inference.
      - Defines relation + Page Phase + Page id + scope + Board-relative path rows.
        Scope is either one whole Page or one direct Content division; a division
        brings its Page identity, Opening, and matching Aims/States group.
      - Requires agents and Page RUN to resolve the current phase through
        `cli/pagecontext.py`, one hop only. Broken paths, mismatched Page ids, missing
        scopes, and malformed rows stop as mechanical findings instead of silently
        dropping context.
      - Emits Page identity and Opening once when one phase selects several scopes on
        the same target, after the first fresh-context trial exposed the repetition.
260804 · `0.14.0`
      - Adds the concrete `RUN` verb for one bounded, non-linear Page lifecycle. It is
        not named `ADVANCE` because phases may repeat, branch, HOLD, or begin a new
        DRAFT round.
      - Adds `ref/page-run-contract.md`, the common raw-material packet, phase receipt,
        version identity, role-separation, durable audit bundle, legal-route, stop,
        and fault-test contract shared by all four Page Phases.
      - Requires the producer, mechanical builder, and judge to have distinct actor
        identities and verifies that each version is exactly its two declared
        lowercase SHA-256 digests.
      - Makes the CLI independently rehash the current source and rendered Page, so
        agreement among receipt fields cannot substitute for artifact identity.
      - Audits the preserved packet against the run and enforces receipt-to-receipt
        version continuity, start-phase identity, gate identity, and declared bounds.
      - Wires RUN to the Board-owned Workflow and deterministic lifecycle auditor.
260804 · `0.13.0`
      - Adopts QB9's lifecycle vocabulary without adding an `ADVANCE` verb: one persistent Page combines a stable Page Type with a current DRAFT, PROBE, REVISE, or CHECK phase.
      - Adds the load order `base → matching Page Type → current Page Phase → family worker` and routes phases by authority rather than add, delete, move, or rewrite operations.
      - Moves the three `for-*` variants under `page-types/` and names the four direct phase contracts under `page-phases/`.
      - Defines returning to DRAFT after purpose or Aims change as a new round on the same Page.
      - Changes the section write table from generic machine permissions to phase authority, including the correction that changing Aim intent is DRAFT rather than REVISE.
260803 · `0.12.0`
      **Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.
      - **"The seven sections" is gone.** It was an invented count, cited as settled by four files, and it disagreed with its own authority and with the template: `ref/board-form.md` §4 fixes the ON-STAGE order at FIVE, and `ref/page-template.md` carries 13 `##` headings. Every statement now points at the authority instead of restating a number.
      - The kind table went from three kinds to **six**, with the note that `src/common.py` globs four prefixes because a `Skill-` page rides the `S` glob.
      - Both variants are named, with which page kind each governs, so a `QBv` author is routed. Only `haipipe-board-page-for-skill` was named before.
      - The variant location rule is MAINTAINER-based, matching the door.
      - The Opening budget says target ~450, hard ceiling 520, which is what `check.py` enforces. It had said "under ~450", a limit nothing checked.
260802 · `0.11.1`
      - Routes the two skill and agent page kinds away from this skill's own `create a new page` steps. They are GENERATED by `haipipe-board/cli/skillpage.py new`, which writes the page from its own stub and registers it in `board.md` itself; copying `ref/page-template.md` and registering by hand produces a page with no managed spans that the checker reports as broken forever.
      - Found by a blind door test that followed this contract literally and hit the contradiction: two create procedures existed and nothing said which applied.
260802 · `0.11.0`
      - Names `haipipe-board-page-for-skill` as the variant for the Skill and Agent mirror
        kinds, and says to load it before writing or fixing any `Skill-<n>` or `Agent-<n>`
        page. It is the one variant that ships BESIDE this skill rather than under a
        consumer family, because for those two kinds the consumer IS the board family.
      - Records why that variant had to exist rather than a tighter rule here. This skill
        already carries the noun-substitution test, so the rule was on the books when five
        skill and agent pages came out of one template on 260802. The cause is upstream of the test:
        this skill's Opening shape ends in `what this page decides`, and a mirror page
        decides nothing, so a writer obliged to ask a question can only manufacture a
        rhetorical one. The empty slot was the defect, not the writers.
260802 · `0.10.0`
      - `working on an existing page` gains steps 7 and 8: ONE page is the deliverable,
        a write outside it is allowed only when the page cannot be made correct without
        it and must be named in the report, and a sibling page's CONTENT is never
        rewritten. Step 5 sends an agent to other files on purpose; nothing bounded it.
      - The verb now states the measurement that produced the rule. Three fresh agents
        were each given one sentence and nothing else on 260802. All three found this
        skill unaided (at tool calls #5, #6, #5) and drove their page to zero findings,
        including the one whose wording matches no trigger in the description. They then
        disagreed completely about reach: 1 file versus 15, the wide one touching four
        shipped `SKILL.md`, four `CHANGELOG.md`, six sibling pages and `board.md`.
        Neither was wrong on the merits, which is exactly why the bound had to be written
        rather than left to judgment.
260802 · `0.9.0`
      - A machine now CLOSES a `### Decision Now` row once the person has answered it,
        recording which option, who ruled, when, and the words they used (JL 260802:
        "I think you should close it automatically, please go ahead and do it").
        It still may not close a row nobody answered, and may not flip a page-level
        human gate; a machine's own recommendation is never an answer. Before this a
        row answered in chat and acted on within the hour still rendered as pending,
        so the page reported work as waiting that had already shipped.
260802 · `0.8.1`
      - Repointed every design-board citation after `QC1b`'s 260802 Content rebuild: the door test
        moved from `QC6 §7` to `QC1b §1`, the anchored-write rule from `QC6 §9` to `QC1b §4`, and the
        human-decision rule from `QC6 §10` to `QC1b §5`.
      - Corrected the named next step. The rule strings it must replace are not in `cli/serve.py` and
        there are not one of them: they moved to `live/chat.py` in the `QC2c` live-layer split, and
        there are four (`CHAT_RULES`, `FULL_RULES`, `BOARD_CHAT_RULES`, `BOARD_FULL_RULES`).
260801 · `0.5.1`
      - Clarified the base/variant boundary: a consumer variant defines Content and
        may fill typed records through declared Aims, States, and Stage Contract
        extension points, but it never redefines the shared frame sections.
260801 · `0.5.0`
      - Keeps requirements in the page spec instead of copying them into a separate
        evaluation skill.
      - Resolves base, variant, page-local, Stage Contract, division, and paragraph-job
        requirements before judging.
      - Defines four axes (mechanics, function, evidence, readability), four verdicts,
        and one evidence-bearing report row per section or Content unit.
      - Assigns execution to the existing `check.py`, `✅ Quality Check`, and fresh
        Board reviewer surfaces.
260801 · `0.4.1`
      - Canonicalized the paired section labels as `Aims / States`: both are plural
        collections, while one Aim still maps to one current State record.
      - Kept singular `State` as a legacy input alias alongside `Where we are` and
        `Now`.
260801 · `0.4.0`
      - The page contract now separates durable intent from present fact. `## Aims` holds stable Content-linked targets (`A3.1`, with `P1` for page-level targets), a testable `Done when`, and an optional temporary `Plan`. `## State` mirrors every Aim exactly once with ⬜, 🟡, 🟠, ✅, or ⏸️. State transitions go to Log; Decision Now remains the human-only checkbox edge. A Content division may have zero, one, or many Aims, while every Aim must have one current State row.
      - The fixed sequence is `Opening → Diagram → Content → Aims → State → Files`. The contract no longer teaches the retired generated Structure row or checkbox-based page completion. Historical `Items to Finish`, `Done when`, `Where we are`, and `Now` remain parser aliases, not canonical authoring guidance.
260801 · `0.3.0`
      - The five-row section contract (JL 260801, ruled as option A on the design board's
        QB4 Decision Now): every section answers ONE reader question, and the same five
        rows define each section's contract — conveys · holds · source · rules · omit.
        The seven-sections table gains the reader-question ladder plus the
        misplaced-sentence rule (substance in Opening → Content, contract material in
        Content → Stage Contract, settled flags → Where we are, open work → Items to
        Finish). Long form stays on the board's QB4a-QB4g faces; the compact form now
        lives here and in `ref/q-template.md`'s How-to-use comment, where a writer
        actually meets it.
260731 · `0.2.0`
      - Decision Now: the one RESERVED subsection name inside `## Where we are` (JL, same
        day: "don't make the decision here ... Always go to the corresponding Q's Where we
        are's subsection of Decision Now"). It lists the decisions a machine proposes and
        the human must make, one `- [ ]` row each with the ask, the options, and a
        recommendation; the human answers by ticking; an answered row moves into the
        page's dated record. The 260729 contextual-naming rule stands for every other
        subsection; this is its single exception.
      - The tick rule now names the landing spot: a machine PROPOSES a tick as a Decision
        Now row, never in chat alone.
      - The board pages `QB4e` (the Where-we-are face) and `QC6` on the design board carry
        the first two live subsections.
260731 · `0.1.0`
      - First cut, created on JL's order ("make the haipipe-board thinner, and have other
        skills, like haipipe-board-page ... please creating them now") from the roster the
        design board had already settled: QC6 §8's shape is one door, two SPECS, two VERBS,
        and this is the page SPEC the routing and digest verbs LOAD.
      - Contract-first: no code moved. It owns what a page IS (the three kinds over one
        base, the seven sections in their fixed order, the write anchors), and it cites
        `haipipe-board/ref/q-template.md` as the authority rather than forking it.
      - Carries the two machine-write rules with their provenance: writes land at a
        SECTION BOUNDARY, never a byte offset (QC6 §9, after a concurrent session spliced
        a heading into the middle of another page's Question sentence on 260730), and a
        transcript-reading verb may propose a tick but never tick or flip `state:`
        (QC6 §10, because reporting a claim is not verifying it).
      - Names its own next step from QC6 §7: `serve.py`'s `CHAT_RULES` becomes a consumer
        of this contract instead of a hand-rolled copy, which has already rotted once
        (QB5d caught it describing a page shape that no longer existed).

<!-- haipipe:skill:log:end -->
