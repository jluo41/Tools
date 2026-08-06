# QBt10 · The companion folder: one brief, three shapes, and the rule that won

state: 🟡 PARTIAL · selected 260806 by JL; the record's `downstream` line is still open and one criterion is unmet
page-type: design
owner: JL
method: write the brief first, draw each candidate whole beside the others, and close on one selection record that keeps every loser and the reason it lost

## Opening

Where does a typed page keep the bytes it owns, and what names that folder?

✅ **The subject of this brief is REAL, unlike its two neighbours in this group.** All three candidate shapes existed on disk or in the engine, the winner was ruled by JL on 260806, and the engine change that followed is commit `dd7998ee`. What is RECONSTRUCTED is the brief FORM: nobody laid the three shapes side by side against a written brief before one was chosen, and no criteria were written down in advance. 🚫 Every reconstructed line below carries that marker, and the criteria in `## Aims` are the largest of them.

**What a companion folder is**: the folder a page owns, holding what that page produces. `QBt3-for-display` owns a build script and a rendered figure. `QBt5-for-value` owns two QA records and their extracts. None of that fits inside a `.md` file, so each page needs somewhere on disk, and that somewhere needs a name nobody has to keep true by hand.

**Does a design brief own a companion?**: no, and this page has none. `haipipe-board-page-for-design` declares no companion folder and owns no scripts. A candidate here IS a folder layout, so each one is drawn whole inside its own division, which is what the contract asks for: the artifact itself, never a pointer to something that scrolls away. If this page ever did own a companion, the winning rule would name it `designs/QBt10-for-design/`, and nothing on disk claims that path today. `python3 unit.py check` reports this file as a view page, which is the correct reading: a design brief SELECTS, it does not PRODUCE.

**Where candidates live on a real paper**: inside the display unit's own workspace, never in a folder belonging to the design page. On the MISQ paper, `0-lifecycle/S05-display/workspace/<unit>/candidates/` exists for all eleven units and two of them hold real files: `S-Display-1b-research-design/candidates/` carries `E-combined-design.png`, three `F-stepwise-icons.*`, `G-codex-4panel.png` and two `H-research-design.*`, and `S-Display-4c-discretion-gradient/candidates/` carries `C-enriched.pdf` and `.png`. Those letter prefixes are candidate names with no page anywhere saying what each one was trying to do or why the others lost. That gap is what this page type closes.

**Covered elsewhere**: `QBt3` and `QBt5` are the two pages this brief was decided for, and both state the winning rule in their own Openings. `QB6` owns which types exist. The winner's implementation is `topic_entry_contract.py`, not this page.

## Diagram

**The fork**: two independent choices, and the cell each candidate sits in.

```text
  🧭 TWO CHOICES, NOT ONE · what NAMES the folder · what GROUPS it

                    🏷 named by the PAGE        ✍️ named by a TYPED id
                       the folder cannot lie       a person keeps it true
  ─────────────────────────────────────────────────────────────────────
  🔭 grouped under    🏆 C  <type-plural>/       🪦 B  probes/<topic id>/
     the TYPE               <page name>/               + requires: <page id>
                            WON 260806 · JL            dropped · two names
                                                       for one thing
  ─────────────────────────────────────────────────────────────────────
  📎 sitting beside   ♻️ A  <page name>.data/     ( nobody drafted this
     the PAGE               merged · the suffix     cell, and it is the
                            still works one         worst of the four )
                            level down
  ─────────────────────────────────────────────────────────────────────
  C is A's naming ✚ B's grouping, which is why A merged and B did not
```

**The winner on disk**: the two companions this rule actually named, in this folder.

```text
  📂 QBt-page-types/                      ← the group folder
  ├── QBt3-for-display.md                 page-type: display
  ├── displays/                           🔑 the display type's level
  │   └── QBt3-for-display/               🏷 the page's filename, exactly
  │       ├── source/build.py
  │       └── out/assets/figure.txt       ← that page's one provides:
  ├── QBt5-for-value.md                   route: inward
  ├── QA-probe/                           🔑 the value type's level
  │   └── QBt5-for-value/                 🏷 the page's filename, exactly
  │       ├── 1-drift-counts.md
  │       └── 1-drift-counts.data/        ♻️ candidate A, one level down
  │           └── counts.csv              ← that record's one provides:
  ├── QBt10-for-design.md                 ← this page. No companion.
  └── unit.py
  ─────────────────────────────────────────────────────────────────────
  ⚠️ QA-probe is a ruled NAME, not the plural of value. The rule says
     <type-plural> and its second live instance does not obey it literally
```

## Content

### 1 · Candidate A · a .data suffix beside the page · ♻️ MERGED

**The artifact**: the shape as drafted, and what the group root looks like under it.

```text
  ♻️ CANDIDATE A · a suffix, sitting beside the page it belongs to

  📂 QBt-page-types/
  ├── QBt3-for-display.md
  ├── QBt3-for-display.data/         everything that page owns
  │   └── out/assets/figure.txt
  ├── QBt5-for-value.md
  ├── QBt5-for-value.data/
  │   ├── 1-drift-counts.md
  │   └── 1-drift-counts.data/       a .data nested inside a .data
  ├── QBt10-for-design.md
  └── … one more pair per page, forever, in one flat root
  ─────────────────────────────────────────────────────────────────
  fit to the brief                              🚫 criteria written after
    P1 🏷 self-naming     ✅ the name IS the page's name plus a suffix
    P2 🔭 one glob a type ❌ ten types interleave in one flat root
    P3 🔗 engine pairing  ✅ strip .data and you have the page
    P4 🚚 migration       🟡 no engine has ever globbed this shape
```

♻️ Establishes the shortest possible distance between a page and its bytes, and what that shortness costs.

**Why it was drafted this way**: a suffix cannot go stale. The folder's name is the page's name with four characters added, so a reader who can see the page can see its companion on the next line of the same listing, and a resolver derives one from the other with no lookup. It also needs no new level, so adopting it changes nobody's paths.

**What it fails**: the group root. Ten page types times one companion each puts every type's bytes in one flat listing, interleaved with the pages themselves, and there is then no way to ask "show me every display companion" without reading each page's head key first. A sweep that has to open files to find folders is not a sweep.

**Where it went**: merged, and the merge is not a consolation prize. The suffix is on disk right now doing exactly the job it is good at, one level down: `QA-probe/QBt5-for-value/1-drift-counts.data/counts.csv` is a QA RECORD's companion, not a page's. At that level there is only one kind of thing in the drawer, so P2 never applies, and P1 and P3 still pay. `unit.py`'s `atoms()` skips every file under a `*.data` parent, which is the line that makes the suffix mean evidence for a person rather than an interface for a machine.

### 2 · Candidate B · one shared probes drawer keyed by a typed id · 🪦 DROPPED

**The artifact**: the shape as it was actually running before 260806, with its pairing line.

```text
  🪦 CANDIDATE B · one shared drawer, each folder keyed by a typed id

  📂 papers/<paper>/
  └── probes/                        one drawer for all evidence
      ├── V01-drift/                 ✍️ V01-drift is typed by a person
      │   └── 1-drift-counts.md        requires: S-Value-1   ← the pairing
      └── L03-<topic>/
          └── 2-<slug>.md              requires: S-Lit-3
  ─────────────────────────────────────────────────────────────────
  the page it pairs to must therefore HAVE a stable id, so page_id()
  matched ^(S-[A-Za-z]+-\d+[a-z]?) and refused every other filename
  ─────────────────────────────────────────────────────────────────
  fit to the brief                              🚫 criteria written after
    P1 🏷 self-naming     ❌ V01-drift matches no page's filename
    P2 🔭 one glob a type 🟡 one drawer, but it serves one kind only
    P3 🔗 engine pairing  ❌ needs requires:, and a stale one is silent
    P4 🚚 migration       ✅ it IS the old shape, so nothing moves
```

🪦 Establishes what a hand-typed id costs once something downstream has to trust it.

**Why it was drafted this way**: it was not drafted, it was already running. The sweep brief of 260806 records it as the live shape, `probes/L|V<nn>-<topic>/<n>-<slug>.md`, with the digit-first filename chosen so the board's page glob would never pick a record up as a page. One drawer for all evidence is easy to find, and a record that names its page in a `requires:` line is easy to read.

**What killed it**: the id is a second name for one thing, and a second name is a thing that can disagree with the first. `V01-drift` matches no page's filename, so a reader holds two vocabularies at once, and a rename on either side leaves the other silently wrong. Worse, pairing through a typed id forced the PAGE to carry a stable id too, which is why `page_id()` required an `S-<Family>-<n>` prefix. That requirement refused every board that is not a paper. `QBt5-for-value` was refused by it, on the very board the specimens were being written for.

**Where it went**: dropped, with one read-only tail. `PROBE_DIRS = ("QA-probe", "probes")` in `topic_entry_contract.py` still globs the old name so each paper migrates on its own clock, and `requires:` still WINS where a record declares it, on the stated reason that a stale declared line should be caught rather than quietly overridden by the folder it sits in. Neither of those is a partial win for B: both are migration surface, and P4 above is why they exist. A fossil is still readable in `displays/QBt3-for-display/source/build.py`, whose docstring points at `probes/V01-drift/1-drift-counts.md`, a path that has not existed since the rename.

### 3 · Candidate C · a type level, then the page's own name · 🏆 WINNER

**The artifact**: the rule, and the two instances that live under it today.

```text
  🏆 CANDIDATE C · a level per type, then the page's own filename

  📂 <board or group>/
  ├── <page>.md                      page-type: <type>
  └── <type-plural>/                 🔑 one level, one type
      └── <page>/                    🏷 the page's filename, exactly
          └── …                      whatever pages of that type own
  ─────────────────────────────────────────────────────────────────
  live in this folder, both of them
    displays/QBt3-for-display/       the display type's level
    QA-probe/QBt5-for-value/         the value type's level
  ─────────────────────────────────────────────────────────────────
  fit to the brief                              🚫 criteria written after
    P1 🏷 self-naming     ✅ rename the page and the pairing breaks
                             loudly at the next check, not quietly
    P2 🔭 one glob a type ✅ displays/* is every display companion
    P3 🔗 engine pairing  ✅ relative.parts[-2] IS the page id
    P4 🚚 migration       🟡 both names globbed, probes not yet dropped
```

🏆 Establishes the winner, and the one thing it borrowed from each loser.

**Why it was drafted this way**: it is A's naming under B's grouping. The page's filename names the folder, so nothing is typed twice, and the type level above it gives a sweep one glob per type instead of one read per page. Neither loser could have both, because A had no level to group under and B had a name that was not the page's.

**What it bought the engine**: pairing off the path. Commit `dd7998ee` made `page_id()` fall back to a file's own stem and taught the pairing to accept the drawer name as the binding, so a record in `QA-probe/QBt5-for-value/` needs no `requires:` line at all. The S-prefix requirement went with it, and `QBt5-for-value` stopped being refused for its filename. The engine comment states the reasoning in one line worth reading before touching this: a page can only be in one folder, but it may be renamed, so a declared `requires:` should be caught rather than silently overridden.

**What it still owes**: its own wording. The rule says `<type-plural>`, and `displays` is the plural of `display`, but the value type's level is `QA-probe`, which is a name JL ruled on 260806 and not the plural of anything. Two live instances, one of which does not obey the rule literally, is a rule that has not finished being written. The Decision Now row below carries it.

### 4 · SELECTION · 260806 · JL

**The record that closes the page**: the winner, why it won, and where each loser went.

```text
  🏁 SELECTION · 260806 · JL
  ─────────────────────────────────────────────────────────────────
  winner      candidate C     <type-plural>/<page name>/
              a folder named after its page cannot go stale unnoticed,
              and the type level lets one glob find every companion
              of one type without reading a single page
  ─────────────────────────────────────────────────────────────────
  loser A     merged          the .data suffix keeps its job one
                              level down, on a RECORD's companion:
                              1-drift-counts.data/counts.csv
  ─────────────────────────────────────────────────────────────────
  loser B     dropped         a typed id is a second name for one
                              thing, and it forced the S-prefix that
                              refused every board that is not a paper
                              tail: PROBE_DIRS still globs probes
  ─────────────────────────────────────────────────────────────────
  downstream  ⬜ OPEN          the contract wants a display unit page
                              here. This winner is a RULE, and no
                              display unit renders it. See below.
  ─────────────────────────────────────────────────────────────────
  the ruling is REAL: commit 5c72c521, "One naming rule: a page's
  companion is <type-plural>/<page name>/", then dd7998ee, which
  taught the engine to pair through the folder the rule named
```

🏁 Establishes the one record that closes a design page, and the one line in it this brief cannot honestly fill.

**Why `downstream` is left open, on purpose**: the contract's `downstream` line names the display unit page the winning candidate becomes or updates, and `-for-display`'s acceptance ladder takes over from there. This brief's winner is a naming rule. Nothing renders it, so there is no display unit to hand it to. Its real consumers are a sentence in two page Openings and a constant in one engine file, and neither is a display page. Writing an invented display page path into that line would make the record pass and make it a lie, which is the one thing a selection record must not be. So the line reads `⬜ OPEN` and the Decision Now row below asks whether the type admits a rule-shaped winner at all.

**What a reader should take from an open line here**: the same thing `QBt3`'s unplaced `⬜` row and `QBt5`'s unconsumed E2 teach. A specimen whose every row is green shows a reader nothing about the rows that go wrong, and an open row is how a gap stays visible instead of going quiet.

## Aims

🚫 The four criteria below were written by reading the decision backwards, not before it. A real design brief writes them first, and the contract's whole case is that a candidate can only be judged against a stated brief. `P5` is the odd one out: it is not a criterion of the brief but a target the page itself carries, because the contract says a design page closes on the selection record.

These are page-level Aims, not `A<n>` groups, and on this Page Type they always will be. A criterion cuts across every candidate at once, so it belongs to no single Content division, and `QB4` §0.5 gives `P` to exactly that case. An `A1` group here would be read by the checker as the Aim group of `### 1`, which is a candidate, and the two names would never match.

### P · 🧾 The brief's criteria, and the record that closes them
- P1 · 🏷 The folder names its own page, with nothing typed twice.
  **Done when:** every companion in this group is its page's filename exactly, and no QA record needs a `requires:` line to be paired.
- P2 · 🔭 One glob finds every companion of one type, opening no page to do it.
  **Done when:** the type's own level lists every companion of that type and nothing that belongs to another.
- P3 · 🔗 The engine pairs a record to its page from the path alone.
  **Done when:** `topic_entry_contract.py` resolves a record that declares no `requires:`, using only the drawer it sits in.
- P4 · 🚚 The old shape stays readable while papers migrate one at a time, and then stops.
  **Done when:** every paper's drawer is `QA-probe/<page name>/` and `PROBE_DIRS` drops its second entry.
- P5 · 🏁 Every line of the SELECTION record is filled with something a person can act on.
  **Done when:** `downstream` names a real consumer, or the contract rules that a winner which is a rule has none.

## States

- 260806 CC · Written as the `for-design` specimen: a real brief with real candidates, not an essay about the type, the same way `QB4` is both the page grammar and a page obeying it. The subject is this group's own companion-folder question, chosen so the history could be checked against disk instead of invented.
- 260806 CC · P1 ✅ and P2 ✅ are met by the two live companions, `displays/QBt3-for-display/` and `QA-probe/QBt5-for-value/`. P3 ✅ is met by commit `dd7998ee`, which made `page_id()` fall back to a file's stem and let the drawer name be the binding.
- 260806 CC · P4 🔨 is not met and is not close. `PROBE_DIRS = ("QA-probe", "probes")` still carries both names on purpose so each paper migrates on its own clock, and no paper has migrated yet. The loser's tail outliving the loser is normal; it stops being normal when nobody remembers why it is there, which is what division 2 exists to prevent.
- 260806 CC · P5 ⬜ is the one thing left deliberately incomplete. The `downstream` line of the SELECTION record is open because the contract wants a display unit page there and this winner is a rule that no unit renders. Recorded as a Decision Now row rather than filled with an invented path.
- 260806 CC · This page declares no `provides:` and no `needs:`, and `python3 unit.py check` reports it as `👁 a view page, provides nothing, correct`. That is the right reading of the type: a design brief selects between candidates and produces nothing another page reads. `QBt3` is the opposite shape, an atom that provides a render; `QBt5` is a view over N atoms. Three pages, three shapes, one resolver.
- 260806 CC · The reconstruction is marked rather than hidden. The three shapes, the winner, the date, the ruler and both commits are real and were read off git and off disk. The brief form, the four criteria, and every ✅ or ❌ in a fit block were written after the fact, which is the reverse of how the contract says a brief runs, and every one of them carries 🚫.
- 260806 CC · Where the SELECTION record sits is this page's own proposal, not the contract's rule. `haipipe-board-page-for-design` says the record CLOSES the page and never says which section holds it. Written here as the last Content division, because a division is the only span Content offers and putting a dated ruling in States would turn a record into a status line. If the contract meant States, this page is the defect and not the contract.
- 260806 CC · One defect found while writing, left for the page that owns it. `displays/QBt3-for-display/source/build.py` still points its docstring at `probes/V01-drift/1-drift-counts.md`, which has not existed since the 260806 rename; its `NEED` constant is correct. That file belongs to `QBt3`, so it was reported rather than edited.
- 260806 CC · Not registered in `board.md`'s `## Pages`, whose QBt list still names two files. Registration is the board's write, not this page's, and it is worth doing quickly: while any page is unregistered the build creates a group whose token is the glyph `⚠️`, `link_faces()` puts that token in `GROUP_IDS`, and every bare `⚠️` inside every ASCII figure on the board becomes `href="#group-<span class="eu">⚠️</span>"`. Fifteen pages now carry that dead fragment, including `QB1`, `QB2`, `QB4` and `QB8`, which nobody edited. The board's own baseline was two errors. One registration write clears all fifteen, and the boundary regex in `src/body.py` that lets a bare emoji be a linkable token is the defect underneath.
- 260806 CC · This page's Aims are page-level `P` items rather than `A<n>` groups, and on this Page Type they always must be. `check_group_names()` reads `### A<n>` in Aims as the group of Content division `### <n>` and requires the two names to match; on a design page division `### 1` is a CANDIDATE and Aim 1 is a CRITERION, so the names can never match and every criterion would raise `group-name-drift`. `QB4` §0.5 already exempts `P`, so nothing needed changing in the engine, but the type contract says "Aims that ARE the brief's criteria" without saying which id shape survives that rule, and it should.
- 260806 CC · The Content headings carry no backticked paths. A backticked path token inside a `###` heading renders a chip whose href skips `tree_reroot()`, which the 260806 sweep found on `QE5` and worked around at the source rather than in the renderer. The candidate paths therefore live in each division's caption and figure, where they read the same and break nothing.

### Decision Now

- 📍 May a design brief's `downstream` line name something that is not a display unit page? **A ·** yes: a rule-shaped winner names its implementing file or contract, and `-for-display` takes over only when the winner is an artifact that renders. **B ·** no: a brief whose winner is not a display candidate is out of this type's scope and belongs on a plain Q page. Until this is ruled, the SELECTION record above cannot be completed, and P5 stays open.
- 📍 Does the rule say `<type-plural>` or `<type folder>`? Two live instances and one already disobeys the literal wording: the display type's level is `displays`, the plural, and the value type's level is `QA-probe`, a name JL ruled. **A ·** keep `<type-plural>` and rename `QA-probe` to `values/`, which breaks two engine constants and every paper mid-migration. **B ·** reword the rule to `<type folder>/<page name>/`, where each type declares its own folder name and `displays` happens to be a plural.

## Files

- `../../board/page-types/haipipe-board-page-for-design/SKILL.md`
  The contract this page is an instance of. If the two disagree, the contract wins and this page is the defect.
- `../../board/haipipe-board/src/topic_entry_contract.py`
  Where the winner is implemented: `PROBE_DIRS` carries the loser's tail, `page_id()` carries the S-prefix removal, and the pairing comment states why a declared `requires:` still beats the folder.
- `unit.py`
  The resolver. `check` reports this page as a view, and its `build_script` docstring is where the two companion levels, a page's and a record's, are written down in one place.
- `QBt3-for-display.md`
  One of the two pages this brief was decided for, and the display specimen. Its Opening states the winning rule; its `source/build.py` still carries the loser's dead path in a docstring.
- `QBt5-for-value.md`
  The other page the brief was decided for, and the page whose filename the S-prefix requirement refused.
- `QB-delivery/QB4-overall.md`
  The page frame this page sits in: the section set, their order, and the caption rule every division above obeys.
- `QB-delivery/QB6-page-types.md`
  The hub listing all ten types and owning the checker debt, including whatever rule would one day check a SELECTION record.

## Log

- 260806 · [DRAFT-CC] written as the `for-design` specimen: a real brief, three real candidate shapes, and the selection JL ruled on 260806. Both losers keep their divisions with their dispositions, which is the one hard rule of this type. The reconstruction, the criteria and every fit mark are marked 🚫; the shapes, the ruling and the two commits behind it are not.
- 260806 · [DRAFT-CC] the SELECTION record's `downstream` line left open on purpose and carried as a Decision Now row, because the contract wants a display unit page there and this winner is a naming rule that nothing renders.
