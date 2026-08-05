---
name: haipipe-board-page-for-stage
description: >-
  The VARIANT contract for a Board's S-Family-unit stage pages, one Page per lifecycle stage of a paper or application across seed, resource, claims, venue, pitch, narrative, display, and section-edit. It resolves a Page to its own stage through the board_family and board_unit declared by stage.md and holds no per-stage rule itself. It loads haipipe-board-page for the base frame and adds the chain, managed Stage Contract, venue transfer tiers, venue-free versus venue-aligned split, and human gate semantics. Use when writing or fixing a stage Page, when its inputs or venue binding are wrong, when a paper retargets, or when a draft needs to know which venue rules bind it. Trigger: stage page, S page, S-Main, S-Venue, S-Seed, lifecycle stage, stage contract, requires, style-from, provides, venue contract, blueprint, retarget, section edit, gate, /haipipe-board-page-for-stage.
metadata:
  version: "0.4.3"
  last_updated: "2026-08-05"
  summary: "Now lives under page-types/ and composes with a separate DRAFT, PROBE, REVISE, or CHECK contract."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-stage · a stage page is the paper, one gate at a time

**LOAD `haipipe-board-page` FIRST.** It owns the base: the sections and their fixed order, the Opening split, the numbering, the `## Stage Contract` markers, the rule that an S page's Content is the stage's real product, and the evaluation contract.
This file adds only what a stage page needs and an ordinary decision page does not.
It never repeats a base rule, because a copied rule goes a night out of date while the contract moves.
After resolving this Page Type, load the current contract from `page-phases/`; this file does not imply a fixed phase order.

**The kind this variant covers**: one page per lifecycle stage, in any family.

```
kind    filename                      subject                       closes when
──────────────────────────────────────────────────────────────────────────────────
Stage   S-<Family>-<unit>-<slug>.md   ONE stage of ONE paper        its human gate passes
```

A FAMILY is a folder on the paper's board and a STAGE is a row in `stages/index.yml`. They are two axes and they do NOT line up, which is the first thing to understand about this page kind. Counted on `Paper-Personality2Opioid-MISQ2026` on 260803:

```
FAMILY        pages   declared by a stage row?
Seed            1     ✅ seed
Work            8     ✅ resource (Work/0) · claims (Work/1) · plus 6 unit pages
Venue           4     ✅ venue (Venue/0) · pitch (Venue/1) · narrative (Venue/2) · +1
Display        13     ✅ display (Display/0) · plus 12 unit pages
Main           10     ✅ section-edit, run once per unit
Appendix        7     ✅ section-edit, same stage, lettered units
Submission      4     🚫 NO STAGE ROW
Literature      5     🚫 NO STAGE ROW
Round           0     🚫 no S page at all: the family holds `QR0-round-delivery.md`, a Q page

8 stage rows · 9 families · 48 S pages · the three do not divide into each other
```

`section-edit` runs once per unit, so one stage row produces seventeen pages across two families, while `seed` produces one. Submission and Literature carry real, gated work under no stage row at all.

## ⛓ What makes a stage page different: it is CHAINED

A Q page stands alone and closes when its Aims are met. A roster page mirrors something that ships. **A stage page is a link**: it cannot start until named upstream pages have passed their gates, and something downstream cannot start until it passes its own.

Three consequences, and every rule below comes from one of them:

```
1  it has UPSTREAM         →  requires: · and the Stage Contract span is generated, not typed
2  it PRODUCES the artifact →  Content is the section, the pitch, the claims ledger itself
3  it has a HUMAN GATE      →  state: is a gate position, and no machine may flip it
```

**The chain is declared in frontmatter and materialized by a script.**

```
requires:              the upstream S pages whose gates must pass first
style-from:            the page whose prose contract this page writes under
provides:              what this page hands downstream, in one line
contract-source-hash:  sha256 of the SOURCES, never of this page

<!-- haipipe:contract:start sha256=… -->    written by stage.py · never by hand
### Required Inputs      one checkbox per requires:, with its gate state and Provides
### Writing Style        the contract inherited from style-from:
<!-- haipipe:contract:end -->               author prose goes AFTER this marker
```

`stage.py sync` replaces only what sits between the markers, and the build reports a stale hash rather than rewriting it, so drift is visible instead of possible. Hand-written contract material, including the venue block below, goes after the end marker where sync preserves it.

**Where a lifted Stage Record goes, settled.** `board-form.md` says build.py lifts an old `### Stage Record` and prints it as the contract's OPENING lines, and this variant says author prose goes AFTER the end marker. Both cannot hold, because the generated span sits directly under the heading. The ruling: **the source goes after the end marker**, where sync preserves it, and the RENDER is free to print it first. A writer follows the source rule; the build's ordering is not an instruction to authors.

**Two headings named Venue collide inside one section, and a reader hits the wrong one first.** `stage.py` generates a `### Venue` inside the managed span pointing at the PITCH page, while the hand-written `### Venue contract` after the marker names the BLUEPRINT as binding. Until the generator is renamed, the hand-written block opens by saying which page it supersedes for binding purposes.

## 🏛 ONE stage reads the venue page, and it is the venue stage

**The rule, and it is the reason this variant exists.** A venue page (`QBv<n>` on the design board) is a catalog of one desk. A paper does not read the catalog nine times. The VENUE stage reads it once, writes this paper's decision and its per-section blueprint, and every later stage reads that blueprint instead.

```
🗂 QBv<n>-<outlet>          the CATALOG · every desk, read by every paper
   what the desk buys · Venue-Structure · Submission-Rules · Authority
        │  read ONCE, by the venue stage
        ▼
📌 S-Open-Venue              this paper's DECISION · which desk, and the blueprint
   per-section budget, structure, density, H-assignments
        │  read by every stage after it
        ▼
✍️ S-Main-<n>, S-Open-Pitch…  each carries a short ### Venue contract block:
   venue · section-type · blueprint (BINDING) · pack style.md (reference only)
```

Why not let each page read `QBv` directly: nine pages re-deriving one desk drift nine ways, and the desk's rules are not per-section anyway. The blueprint is where a desk's total becomes THIS paper's per-section allocation, which is the one arithmetic no venue page can do, because it does not know how long your Results are.

**The venue block is short, and it is a pointer, not a copy.** It lives in `## Stage Contract` after the generated markers, never in Content:

```markdown
### Venue contract
venue: MISQ 2026 · section-type: theory
desk: QBv1-misq (the catalog · this page never reads it; the venue stage did)
blueprint: 0-lifecycle/S01-opening/S-Open-Venue.md (theory blueprint block)  <- BINDING
  binds:   6-7 subsections · H-assignments · the displays this section owes
  reports: ~2,900-6,000w · 0.67-0.78 citations per sentence
style: venue/playbook-utd-is · MISQ/MISQ-theory/style.md  (reference only)
override: none. MISQ publishes NO per-section length rule for theory; its only
  length rule is the 55-page total, which defers to the deliver gate, so the
  blueprint's budget is an ALLOCATION of those 55 pages and not an addition.
supersedes: the generated `### Venue` above, which points at the pitch page
```

Every row earns its place: without `desk:` a reader cannot tell which catalog was read, and without `override:` they cannot tell whether a per-section desk rule outranks the blueprint here or whether none exists. A block that shows only BINDING and reference is thinner than the rules around it and forces the next writer to re-derive both.

## 🧭 How a page finds ITS stage, and what it may take from it

**This variant holds what every stage page shares. It holds no per-stage rule at all**, and it never will: `stages/index.yml` says the phases, artifact paths, sections, done-criteria and craft of one stage live in `stages/<dir>/stage.md` and are loaded ONLY for the stage picked. So the same two-source shape as a venue page: this file is the page contract, `stage.md` is the stage contract, and this file resolves rather than copies.

**The resolver runs in the page id, and the join keys live in `stage.md`.** ⚠️ Not in `stages/index.yml`: that file carries `{key, order, dir, migrated, triggers}` and nothing else, by its own header, which says everything else about a stage lives in `stages/<dir>/stage.md`. An earlier draft of this section sent readers to the index row and a blind reader lost a step grepping the wrong file. Each `stage.md` declares `board_family` and `board_unit`, and that pair is the join:

```
stage.md       dir                        board_family        board_unit
               ▲ where the keys ACTUALLY live (read 260805, after the SNN reorg)
─────────────────────────────────────────────────────────────────────────────
seed           S01-opening/seed           Open                "Seed"   → S-Open-Seed
venue          S01-opening/venue          Open                "Venue"  → S-Open-Venue
pitch          S01-opening/pitch          Open                "Pitch"  → S-Open-Pitch
resource       S02-work/resource          Work                "R"      → S-Work-R-*
claims         S02-work/claims            Work                "C"      → S-Work-C-*
narrative      S02-work/narrative         Work                "N"      → S-Work-N-*
display        S05-display/display        Display             "0"      → S-Display-0-*
section-edit   S06-main/section-edit      Main or Appendix,   reader-order number
                                          per section_kind    or appendix letter
```

The `dir` values are relative to `skills/paper/`, where each stage now lives inside its delivery group's `SNN-` folder (the 260803 reorg); `stages/index.yml`'s `dir:` rows point at the same places. A capitalised `board_unit` such as `"Seed"` is a control-page token: `stage.py` drops the slug, so the page is `S-Open-Seed.md` with no trailing slug.

To go from a page to its rules: read `S-<Family>-<unit>` off the filename, find the row whose `board_family` and `board_unit` match, and load that `stage.md`. To go the other way, the stage spells the artifact path itself. Nothing needs to be guessed, and no page hard-codes a phase list.

**Three page shapes sit under one stage row, and only the first is what `stage.md` describes:**

```
🎯 THE STAGE PAGE     the unit the row declares · S-Work-C-claims, S-Open-Venue
                      → load its stage.md · it owns phases, gates, done-criteria

🧩 A UNIT PAGE        a page the stage produces per unit, or a sub-page under a hub ·
                      S-Main-3-theory (section-edit, once per section kind) ·
                      S-Work-R1-cms, S-Display-4c-discretion-gradient
                      → same stage.md, resolved for THIS unit: section-edit's
                        board_family and board_unit are per-unit, not per-stage

📊 A DASH PAGE        S-Main-Dash, S-Display-Dash, S-Literature-Dash
                      → NO stage row, and it is not a stage of the paper. It is a
                        rollup over one family, regenerated on every run, and it
                        holds ONLY what no single page in that family can hold.
                        S-Main-Dash states its own job: nine pages each know their
                        own state, and none can see how a section stands against
                        its venue floor while the others stand against theirs.
                        Never give a Dash page a gate, requires:, or provides:.
```

**A unit page may carry a more specific type.** An `S-Main-<n>` or `S-Appendix-<letter>` section unit declares `page-type: section` in its frontmatter and loads `haipipe-board-page-for-section` on top of this file; an `S-Display` unit page declares `page-type: display` and loads `haipipe-board-page-for-display`. The stage filename still says which family and unit the page belongs to; the `page-type:` key says which contract governs it, and the key beats the filename (base, type resolution step ③).

**A family with no stage row is a real state, not a defect.** Submission and Literature carry gated pages that no row in `index.yml` declares, and Round carries a Q page instead of an S page. Such a page has no `stage.md` to load, so it owns its own contract in its own `## Stage Contract`, and it says on the page that no stage row declares it. Do not invent a row, and do not file the page under a neighbouring stage because the folder sits next to it.

**What a page may take from its `stage.md`, and what it may not.** Same discipline as the four tiers above, one level up:

```
🟢 RESOLVE AND POINT   the phase list, the gate, the done-criteria, the artifact
                       path · named on the page, never restated in full
🔴 NEVER COPY          the stage's whole template into Content. `stage.md` ships a
                       template.md for that, and the page is the FILLED artifact
⚖️ THE STAGE OWNS      when this page may open, when it may close, and who rules ·
                       a page arguing with its stage.md is a defect in one of them
```

## 🚦 What crosses from a venue page into a draft: four tiers

Naming the source is not enough; a drafter needs to know what to DO with each row. These four tiers are the variant's core, and the third and fourth are the ones people get wrong.

```
🟢 COPY THE SHAPE        the arc · the slot patterns · the owed displays · the
                         refusals   → become the draft skeleton and its checklist

🟡 CARRY AS A TARGET     word budgets · paragraph counts · citation density
                         → measured AFTER drafting and reported, never enforced
                            these are the pack's measurements of published papers

🔴 NEVER COPY            the exemplar SENTENCES. They are evidence that the slot
                         is real, not text to reuse. Every venue page says so and
                         no stage page was ever told.

⚖️ DEFER TO DELIVER      the desk's binding rules (total page cap, reference
                         style, anonymity, disclosures) belong to the deliver
                         gate, not to a section draft
                         EXCEPT when the rule is PER-SECTION, and then it binds
                         this page: ISR caps the abstract at 300 words and
                         requires a separate 500-word contribution statement,
                         so S-Main-0 owns both
```

**A per-section desk rule outranks the blueprint's budget**, because one is published and enforced and the other is this paper's plan. A blueprint that allocates 200 words to an abstract at a desk that caps it at 150 is a planning error, and the stage page reports it rather than writing to the plan.

**The blueprint BINDS row by row, and not every row binds.** This is the contradiction a blind reader hit on 260803 and could not settle: tier 🟡 above says a word budget is "measured after drafting and never enforced", while the venue block stamps the blueprint `<- BINDING` and `S06-main/section-edit/stage.md` lists the word budget among the things that bind. Both are right about different rows, and the page was left unable to tell whether a 1,770-word shortfall was a defect or a reported deviation. The split:

```
⚖️ BINDS      the subsection count · the H-assignments · which claim each
              subsection carries · the display requests it owes
              ↳ THIS PAPER'S OWN ARCHITECTURE, decided by the venue stage

📊 REPORTS    the word floor · sentences per paragraph · citation density
              ↳ INHERITED MEASUREMENTS, copied from the pack into the
                blueprint in one step · a miss is logged with its reason,
                never treated as a failed gate

🚫 UNLESS     the desk itself publishes that number, and then it binds as a
              desk rule rather than as a blueprint row
```

A blueprint row that copies a pack measurement does not become enforceable by being copied. Where a page misses a reporting row, it says so in `## Log` with the reason; where it misses a binding row, that is a CHECK-gate failure. A deviation on a binding row needs a human ruling recorded on the page, in the `DELIBERATE DEVIATION, ruled by <who> <date>` form the sibling pages already use.

**The desk's total is the constraint the blueprint exists to divide.** Measured 260803 across sixteen venue pages: at every desk that publishes a total, the pack's per-section budgets sum to at or above it, because a pack measures published papers section by section and a published page is not a submission budget. So a stage page never adopts a per-section budget without knowing what the whole is.

## 🔀 Venue-free and venue-aligned: what a retarget rewrites

`haipipe-paper-lifecycle` draws this line and this variant enforces it on the page:

```
🆓 VENUE-FREE     seed · resource · claims
                  true about the work regardless of where it goes ·
                  a retarget does NOT rewrite them

📌 THE PIN        venue
                  reads QBv, picks the desk, writes the blueprint

🎯 VENUE-ALIGNED  pitch · narrative · display · section-edit
                  written FOR a desk · a retarget rewrites them
```

A stage page states which side it is on, because that is what tells a reader whether a venue change costs an afternoon or a month. A venue-aligned page whose `style-from:` does not resolve to a venue-pinned upstream page is misfiled, not merely incomplete.

## 🎯 Aims and States on a stage page: the `A<n>` scheme does not fit, and this says what to do

**The hole both testers named first.** The base keys an Aim id to a CONTENT PART: `### A3 · <emoji> <name>` mirrors Content division `3`, and `- A3.1 · target` hangs from it. A stage page's Content is a manuscript section numbered `§3.1 / §3.2 / §3.3`, so there is no Content part `3` for `A3.1` to hang from. Every stage page on the real board answered by using no ids at all. The measurement, 260803: `S-Main-3-theory` carries 21 un-ided Aims and zero `Done when`, and its States section is prose plus a fenced block plus ten `### Needs JL` rows. The render derives its `met/total` counter from States, so the page reports nothing about itself.

**The scheme for this kind:**

```
🎯 AIM ID       - Q-Sec<unit><Kind>-<n>   the q-consumer id S06-main/section-edit/stage.md
                                          already declares, NOT A<n>
                - P<n>                    a target belonging to no single division
   WHY          the stage owns the id pattern, and a second scheme collides with the
                probe layer · `S-Main-3` currently runs BOTH `Q-Sec3Theory-<n>` and
                `§3-Q<n>`, and the four `§3-Q<n>` entries are invisible at its own
                CHECK gate because that shape resolves to no stage

📍 STATE ROW    one per Aim id, exactly once, with the base's ⬜ 🔨 🧠 ✅ ❄️

🗣 THE HUMAN    `### Decision Now` is the base's reserved name (JL 260731) and
   ROW          `### Needs JL · tick these` is what JL approved on 260727 and what
                the whole board uses. Two rulings four days apart, neither
                superseding the other in writing. UNSETTLED: keep the local name,
                and do not renumber a board-wide convention on one page's authority.
```

**Do not force the mirror in one pass on a live manuscript page.** Reaching 1:1 on `S-Main-3` means rewriting both sections wholesale, and it would undo a JL ruling in that page's own Log (260727: a decision row carries the decision only, because a queue that carries its own reasoning stops being scannable). Add ids to new Aims, add the missing State rows, and leave the wholesale renumber to a pass that has a human in it.

## 🩺 `state:` is a gate position, and only a person moves it

The base's four values, read here as: **where is this stage in its own lifecycle?** A stage page closes when its human gate passes, so `state:` answers that and nothing else. A machine may report evidence, propose a `### Decision Now` row, and update an Aim's State from what it can inspect. It may never flip the page-level gate, and `✅ GATED <date>` is a claim about a person, so it carries the date they ruled.

The gate is also what the chain reads: `stage.py` prints each upstream page's gate state into this page's Required Inputs, so a gate flipped early silently unblocks work downstream. That is the failure this rule exists to prevent.

## 📚 Content is the artifact, and nothing else

The base already says an S page's Content is the stage's real product. The variant adds what to do with the four kinds of material that accumulate around a stage and are NOT the product:

```
Required Inputs and the venue block  →  ## Stage Contract
prose rules                          →  ## Writing Style
what is true now, flags, corrections →  ## States
what should become true              →  ## Aims
```

If `📚 Content · Main 3 §3 Theory` does not describe what a reader finds under that heading, the section is holding one of the four.

**Content numbering follows the MANUSCRIPT, not the base's `3 / 3.2 / 3.2.1`.** A division is `### §3.1 <Title>` and a paragraph is `#### P<n>. <its job>`, which is what the real pages use and what `board-form.md` §4 sanctions when it says the subsection count is the number of dotted `###` headings. The venue variant grants the same freedom for a venue's own reading index; this one grants it for the section's. Nothing checks it, so it holds only because it is written down here.

## ⚠️ Conformance debt on the real pages, stated rather than hidden

The paper board this contract was written against (`Paper-Personality2Opioid-MISQ2026`) runs its S pages on the RETIRED section vocabulary: `## Question`, `## Boundary`, `## Items to Finish`, `## Where we are`, and a direct `### Stage Record` under Content. The renderer aliases every one of them, so the pages look correct and nobody sees the drift.

Do not read that as permission. `## Boundary` was removed on 260731, `Stage Record` was folded into `## Stage Contract` on 260801, and the three renamed sections are `## Opening`, `## Aims`, `## States`. A stage page brought up to this contract renames them; a page not yet touched keeps rendering, and `check.py` reports each retired name.

**⚠️ That list is the CHEAP half, and treating it as the whole job is the trap.** Measured 260803: a session applied exactly those renames to `S-Main-3-theory` and stopped, and the checker's count fell from 32 findings to 21. Every remaining structural violation was invisible to it, because the checker cannot see any of them:

```
CHEAP · a checker sees it        four section renames · Stage Record · em-dashes
EXPENSIVE · nothing sees it      no Aim ids at all, 34 flat `- [ ]` bullets ·
                                 no `Done when` on any of them · no State row
                                 mirroring any Aim · `### Needs JL · tick these`
                                 where the reserved name is `### Decision Now` ·
                                 two competing q-consumer id schemes on one page
```

The Aim and State vocabulary is the expensive half, and it is the half the render's own `met/total` counter depends on, so a page can pass the checker and still report nothing about itself. Do the renames, then do the Aims.

## 🔀 Rules this contract does NOT own, and cannot settle alone

Found on 260803 by a reader applying this file to a live page. Each is a conflict between two live authorities, so none is fixed here; a stage page hitting one records it rather than picking a side.

```
🖼 A MANUSCRIPT SECTION HAS NO ASCII FIGURE
   the base asks every Content division to open with a /diagram-ascii figure,
   and check.py warns `division-no-figure` on §3.1, §3.2, §3.3 of a JOURNAL
   THEORY SECTION · the page must NOT satisfy it · the base/variant model lets
   a variant add a rule and gives it no way to SUPPRESS one, so this needs a
   page-kind exemption in the base, the way the roster variant got one for
   `opening-lead-not-a-question`

💬 `> CC:` IS BOTH LEGACY AND MANDATORY
   check.py calls it the legacy comment form and asks for `> Comment CC …`
   S06-main/section-edit/stage.md's Edit surgically step instructs the agent to reply
   with `> CC:` · two shipped authorities, opposite instructions, neither
   citing the other

📎 A PAPER PAGE CITES FROM THE PAPER ROOT
   dead-file-path resolves from the engine, the board, or the repo root · an S
   page at <paper>/0-lifecycle/4-main/ naturally cites `sections/…tex` and
   `displays/…/float.tex`, which exist and resolve from the PAPER root, a
   fourth base nothing declares

🔗 NOTHING OWNS CROSS-PAGE FACTUAL CONSISTENCY
   the base bounds `working on` to ONE page, correctly · but a page whose plan
   rests on a ruling the OWNING page reversed has no verb to catch it, and
   S-Main-3 is carrying exactly that today · re-read the page you attribute a
   ruling to before acting on it, and route the correction rather than fixing
   the sibling
```

## 📂 Files

```
page-types/haipipe-board-page-for-stage/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base frame is `haipipe-board-page`; the generic phase contracts are `haipipe-board-page-draft`, `haipipe-board-page-probe`, `haipipe-board-page-revise`, and `haipipe-board-page-check`; the generator for the managed span is `haipipe-board/src/stage_contract.py` driven by `cli/stage.py`; the stage roster is `paper/haipipe-paper-stage/stages/index.yml`; the catalog this contract binds to is `haipipe-board-page-for-venue`; paper and application workers add their artifact knowledge after the phase contract.
