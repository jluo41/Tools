# A venue pack: what one is, what it owes, and who is allowed to write it

state: 🟡 PARTIAL · the four artifact kinds and the one-writer law are ruled; three pack-shape breaches are open in Aims
owner: JL
method: define the pack as a read-only knowledge unit, name the four files it owes, and separate the venue DECISION from the venue KNOWLEDGE so this group does not re-open QB1

## Opening

The paper system already knows which journal it is writing for. So what is a journal, to this system?

A venue pack is that unit. It is one folder under `paper/venue/` holding what one outlet family rewards, what its editor desk-rejects, and how long its Introduction is allowed to be. Seven of them exist. Fourteen outlets sit inside them. Roughly a dozen skills read them and not one skill owns them.

**Where this group sits, and what it does NOT re-open**: `QB1` ruled on 260729 that the venue DECISION lives inside Opening, alongside seed and pitch, and that filing it as its own Delivery concern read backwards.
That ruling stands and this group does not touch it. QBv is not an eleventh Delivery concern; it is the KNOWLEDGE catalog that Opening reads when it makes the decision, and that four other concerns read afterwards.
One sentence separates them: **QB1 owns which venue this paper targets; QBv owns what that venue knows.**

**Why the knowledge needs its own group**: a pack does not feed one stage. Every `playbook-*/README.md` carries four `-> stage` maps, and they land on four different Delivery concerns.
Rewards land on QB4 Value, the display conventions land on QB5 Display, the section arcs land on QB6 Main, and the language style lands on QB11a.
A body of knowledge that cuts across five concerns cannot be filed under any one of them without going missing from the other four.

**What was actually wrong when this page was opened**: `paper/venue/` is a git submodule, and on this checkout it was **empty**.
The 2a-venue stage contract declares `packs: ../../../../venue/`; on a fresh clone without `--recursive` that path resolves to a directory with nothing in it, and the stage reads zero packs without saying so.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never re-argue where the venue DECISION lives**: `QB1` settled that on 260729 and this page cites it rather than reasoning about it.
A sentence about *when in the lifecycle a venue is picked* belongs on QB1. A sentence about *what the pack for that venue must contain* belongs here.

**Never transcribe a pack's numbers onto this board**: a word budget copied here is a second copy that can only disagree with the pack.
Point at the file; state the rule the file must satisfy.

✅ `every outlet owes a taste.md with a one-sentence test`  ❌ `npj DM Introductions run 600-1500 words`

**Say pack and outlet as two words**: a pack is a family folder, an outlet is one journal inside it, and they own different files. Collapsing them is how `playbook-pnas` came to have an outlet folder with no `taste.md`.

## Diagram

**One pack, four artifact kinds**: and the wall between reading it and writing it.

```text
  📦 ONE PACK ── playbook-<family>/
  ┌──────────────────────────────────────────────────────────┐
  │ 📄 README.md          rewards · fit · 4 stage maps       │  ← family level
  │ 🗣 style-profile.md    the language to imitate            │
  │                                                          │
  │ 🏛 <outlet>/                                             │  ← outlet level
  │    👁 taste.md         desk-accept · desk-reject          │
  │                       + the one-sentence test            │
  │    📐 <abbr>-<section>/style.md   quantified norms       │
  │                      /template.md  the skeleton          │
  │    📚 examples/       exemplar PDFs + INDEX.md           │
  └──────────────────────────────────────────────────────────┘
                              │ READ
        ┌─────────────────────┼──────────────────────┐
        ▼                     ▼                      ▼
   🎯 QB1 Opening        📊 QB4 · QB5           ✍️ QB6 · QB11a
   which venue           what counts as         how a section
   (the DECISION)        a claim / a float      must read

  🚫 no skill WRITES a pack ── the packs are their own repo
     git@github.com:jluo41/Venue-Paper.git @ fe25a88
  ⚠️ and on a clone without --recursive that folder is EMPTY,
     which the venue stage reads as "no packs" and never says
```

## Content

### 1 · What a pack owes, file by file

**Four artifact kinds, split across two levels**: the family answers *why this outlet group*, the outlet answers *what this journal accepts*.

```text
  FAMILY LEVEL ── answers "why this group of journals"
  ├─ README.md         what it rewards · when to pick it
  │                    + 4 maps: ->Claims ->Display ->Minimap ->Write/Edit
  └─ style-profile.md  the distilled language to imitate

  OUTLET LEVEL ── answers "what will this desk accept"
  ├─ taste.md                       ✅ yes / ❌ no / 🎯 one-sentence test
  ├─ <abbr>-<section>/style.md      word budget · ¶ counts · arc
  │                   /template.md  the section skeleton
  └─ examples/                      published exemplars + INDEX.md

  📊 today: 7 families · 14 outlets · 503 files
```

📦 Establishes the pack as a two-level unit, so a missing file is a missing answer rather than a missing folder.

#### 1.1 · The section abbreviation is not the outlet folder name, and the lifecycle already knows
(so the pack shape has a reader-side resolver, and that is where the rule for it lives)
The outlet folder is `npj-digital-medicine` and its section folders are `npjdm-introduction`; `jama-netopen` uses `jno-`, `jama-im` uses `jamaim-`, `diabetes-care` uses `diabcare-`, and `MISQ` uses `MISQ-`.
`stages/section-kinds.yml` measured this on 260720 and ruled the consequence: reach the path by GLOB (`*-<kind>`), never by concatenation, which happens to work for MISQ and fails on six other outlets.

### 2 · Who reads a pack, and who may write one

**Roughly a dozen readers, zero writers**: the packs are a separate repository, and every skill in this plugin holds read access only.

```text
  📥 READERS (paper family alone)
     2a-venue  ── packs:  the only DECLARED dependency
     2b-pitch · 3-narrative · 4-display · 5-section-edit
     draft · revise · revise-results
     paper-folder · paper-enter · lifecycle
     ── plus the whole application family, on its own venue/ tree

  ✍️ WRITERS
     (none in this plugin)

  📜 the 2a-venue contract says it outright:
     "This stage is the READER that turns a pack into a pinned
      contract; it NEVER edits a pack."
```

🔒 Establishes the one-writer law's real shape: the writer is outside this repo, so every skill here is a reader by construction.

#### 2.1 · Read-only is a submodule fact, not a convention
(so the failure mode is not a bad edit, it is an absent folder)
`paper/venue` is a gitlink to `jluo41/Venue-Paper`, pinned at `fe25a88`.
Nothing in this plugin can drift a pack, because nothing here can commit into one. What it can do is read a pack that was never checked out.

### 3 · Where the shape actually varies

**A pack shape is only a contract if a deviation is visible**: two files sit at different levels depending on the pack, and one outlet has no exemplars at all.

```text
  🔀 taste.md sits at TWO different levels
     OUTLET level  jama ×3 · nature ×5 · utd-is ×4 · diabetes-care
                   ── 13 outlets
     FAMILY level  playbook-pnas · playbook-grant · playbook-patent
                   ── the three single-outlet / non-journal packs
     ── the split is defensible, and it is written down nowhere

  🔀 examples/ splits the same way
     FAMILY level  playbook-pnas/examples/   35 files
     OUTLET level  everyone else

  ⚠️ playbook-jama-portfolio/jama-netopen/   examples/ absent
     ── its 3 exemplars are filed under jama-flagship/examples/
        and named in its own taste.md: correct knowledge,
        wrong shape, and an inflated count on the sibling

  ✅ playbook-grant · playbook-patent   no outlet tree at all
     ── agency and jurisdiction deltas are README tables, and
        `stages/section-kinds.yml` declares both packs
        blueprint-only BY DESIGN, in a file the venue and
        section-edit stages both read

  💥 nothing FAILS on any of these ── a reader gets silence
```

⚠️ Establishes the gap between the shape the README describes and the shape the packs actually have.

## Aims

### A1 · 📦 What a pack owes, file by file
- A1.1 · The pack shape is checkable against the resolver the lifecycle already has, so the two cannot drift.
  **Done when:** a kind folder added to or removed from any outlet fails a check until `section-kinds.yml`'s outlet map agrees.

### A2 · 🔒 Who reads a pack, and who may write one
- A2.1 · An uninitialized `paper/venue/` fails loudly instead of reading as zero packs.
  **Done when:** the 2a-venue stage distinguishes "no pack matches" from "the submodule is not checked out", and says which.

### A3 · ⚠️ Where the shape actually varies
- A3.1 · The two placement levels for `taste.md` and `examples/` are declared, with the rule that decides which a pack uses.
  **Done when:** a reader resolving taste for an unfamiliar pack knows which level to look at without listing both.
- A3.2 · An exemplar is filed under the outlet it exemplifies.
  **Done when:** listing any outlet folder gives that outlet's true exemplar count, with no cross-pointing needed.
- A3.3 · The blueprint-only declaration and the packs' own contents cannot disagree.
  **Done when:** adding a per-section pack to grant or patent fails until `section-kinds.yml` stops calling it blueprint-only.

## States

### A1 · 📦 What a pack owes, file by file
- ⬜ A1.1 · Not started, and narrower than first written. `stages/section-kinds.yml` already carries the glob rule and an outlet-to-kinds map measured on disk; what is missing is anything that fails when a pack changes and that map does not.

### A2 · 🔒 Who reads a pack, and who may write one
- ⬜ A2.1 · Not started, and hit today. `paper/venue/` was empty on this checkout until it was initialized on 260802; the stage contract's `packs:` path resolved to an empty directory with no error.

### A3 · ⚠️ Where the shape actually varies
- ⬜ A3.1 · Not started. Thirteen outlets carry `taste.md` at outlet level; `pnas`, `grant`, and `patent` carry it at family level, and no file says which rule applies.
- ⬜ A3.2 · Not started. Three JNO exemplars sit under `jama-flagship/examples/`, which both empties one outlet's count and inflates the other's.
- ✅ A3.3 · Resolved on inspection, and replaced. `section-kinds.yml` already declares grant and patent blueprint-only by design, and both venue and section-edit read it; what remains unguarded is the two declarations staying in step.

## Files

- `../../paper/venue/README.md` · the pack index and the family table
- `../../paper/1-lifecycle/haipipe-paper-stage/stages/2a-venue/stage.md` · the only contract that declares `packs:`
- `QB-delivery/QB1-opening.md` · owns the venue DECISION, which this group does not re-open
- `../../application/venue/_SCHEMA.md` · the application family's parallel venue tree, same idea, different outlets
- `sync-exemplars.py` · regenerates each outlet page's `📚 Exemplars` block from the packs, and fails on a count this board states and the folder does not

## Law

A venue pack is READ and never written by this plugin: it is a separate repository, pinned as a submodule, and the paper stages are readers by construction.
A pack answers at two levels, family and outlet, and a file missing from either level is a missing answer, not a missing folder.
This group holds what a venue knows; `QB1` holds which venue this paper picked, and neither may restate the other.

## Glossary

- **Pack**: one `playbook-<family>/` folder, the unit that answers why this group of outlets and what it rewards.
- **Outlet**: one journal inside a pack, the unit that answers what this particular desk accepts.
- **Taste**: the outlet-level desk-accept / desk-reject signals plus the one-sentence test a paper must pass to be worth submitting.
- **Pin**: the venue decision recorded on the paper's own `S-Venue-0` page, owned by QB1, never by a pack.

## Log

260802 · Corrected against `stages/section-kinds.yml`, found while answering how a Content division becomes an S-Main page. That file already carries the glob rule for the section abbreviation, an outlet-to-kinds map measured on disk, the `theory-model` alias, and the blueprint-only declaration for grant and patent. Four claims on this group that something was undeclared were wrong, and the Aims they carried are replaced by drift guards.
260802 · Every outlet page now lists its exemplars, generated by `sync-exemplars.py` rather than typed. Writing the generator immediately disproved thirteen counts this board had stated: they came from `ls | wc -l`, which counts `INDEX.md` and `*_RESULTS.md` as papers. The real total is 236 papers, and the script now fails on any count a page states that the folder does not.
260802 · Opened with the QBv group. Split the venue KNOWLEDGE from the venue DECISION so this group could exist without re-opening the 260729 QB1 ruling, and recorded the empty-submodule failure found while checking the packs.
