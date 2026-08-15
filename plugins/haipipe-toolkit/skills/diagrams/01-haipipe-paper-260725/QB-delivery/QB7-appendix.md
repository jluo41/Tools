# Delivery Appendix: lettered units that each stand up to being checked alone

state: ✅ RULED · the source-region rule is ruled; splitting the MISQ leaves is held as paper work
owner: JL
method: give every appendix unit an authoritative source region, human gate, wrapper order, and projected target set

## Opening

How do appendix prose, prompt templates, and tables stay source-complete?

An appendix unit is one lettered payload, such as Appendix B holding the validation evidence. A wrapper is a generated file whose only job is ordered `\input` wiring. A leaf is the prose or template inside it. The danger is a leaf with no source region, which compiles fine and can never be reviewed.

**Where this page sits**: QB6 Main owns the reader-facing argument, and QB9 Build owns manifest coverage and the candidate checks.
This concern owns the appendix inventory and what each lettered unit must carry before it may be generated.

**Why the appendix is where source-completeness fails first**: nobody reads it end to end, so a hole survives.
A prompt template pasted straight into a `.tex` file has no page behind it, and the paper cannot say who approved that wording or what it replaced.

**What the gate actually tests**: not whether the appendix compiles, but whether every leaf resolves to a region a person gated.
That is why the MISQ appendix is blocked today rather than shipped.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../BoardSkillBoard-260722/QPs-page-structure/QPs1-overall/QPs1-overall.md` and are not restated here.

**This page DESIGNS; the paper board SHOWS**: `### 2` states what a paper must carry for this concern, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

**Keep wrapper and leaf apart in every sentence**: a wrapper carries wiring and a leaf carries content.
The whole Law turns on that split, so a sentence that says "the appendix file" has already lost it.

## Diagram

**Source to appendix**: what a person authors, and what the build generates.

```text
  ✍️ 0-lifecycle/5-appendix/          🤖 appendices/
  ─────────────────────────           ─────────────
  🗂 S-Appendix-0-control  inventory
  📄 S-Appendix-A  prompts     ━━━━▶  A.tex   leaf, from a gated region
  📄 S-Appendix-B  validation  ━━━━▶  B.tex
  📄 S-Appendix-C … F          ━━━━▶  …
                               ━━━━▶  driver  wrapper: \input ONLY

  🚪 the gate: every LEAF has a unique non-empty selector,
     and its owning source page is GATED
  ⚠️ MISQ today: G0 maps all targets · G1 refuses every unit
```

## Content

### 1 · The delivery contract

**What Appendix owes**: a gated source region behind every leaf that ships.

```text
  📥 CONSUMES                📤 PROJECTS TO           🚪 GATE
  accepted claims       ━━▶  appendices/*.tex   ━━▶  every leaf has a
  values                     pure wrappers            unique non-empty
  validation artifacts       prose leaves             selector, and its
                                                      source page is GATED
```

📜 Establishes what an appendix unit must have before it may be generated.

| Field | Contract |
|---|---|
| Lifecycle | Appendix units after the main argument establishes what verification payload is needed. |
| Authority | `0-lifecycle/5-appendix/` source pages and unit gates. |
| Projects to | `appendices/*.tex`, including pure wrappers and prose leaves. |
| Skills | Section-edit and `haipipe-paper-project`. |
| Consumes | Accepted claims, values, and validation artifacts. |
| Gate | Every leaf has a unique non-empty selector and its owning source page is GATED. |
| Open gaps | The MISQ A-F source is centralized and OPEN; prompt/table leaf divisions remain incomplete. |

#### 1.1 · A wrapper holds wiring and nothing else
(the moment a wrapper carries content, that content has no page behind it)
A wrapper's only job is ordered `\input`, so it can be regenerated freely and nobody loses anything.
Every prose or template leaf must point at an explicit authoritative source region, because a leaf without one cannot be reviewed and cannot be re-approved after an edit.

### 2 · What we want on the paper board

**The group we are designing**: a control page plus one page per lettered unit.

```text
  🎯 WHAT WE WANT a paper to carry for this concern
  ### Delivery · Appendix
        🗂 S-Appendix-0-control.md    the INVENTORY: which units exist
        📄 S-Appendix-A-prompts.md     ┐
        📄 S-Appendix-B-validation.md  │ one page per lettered unit,
        📄 S-Appendix-C-variables.md   │ each individually checkable
        📄 S-Appendix-D-iv.md          │
        📄 S-Appendix-E-robustness.md  │
        📄 S-Appendix-F-bigfive.md     ┘

  ⚡ this concern owns NO STAGE ── `../../paper/haipipe-paper-stage/stages/index.yml` has no `appendix` key
  🔑 the control page is a FAMILY control page, which no stage writes
  🔤 units are LETTERED, so a unit added late renumbers nothing
```

🎯 Establishes what a paper board must show for this concern, and why the unit count is the paper's rather than the template's.

#### 2.1 · Lettering is what makes a unit insertable
(Main numbers its sections; Appendix letters its units, and the difference is not cosmetic)
An appendix grows when a reviewer asks for one more piece of evidence, often late.
Letters mean a new unit lands as G without renumbering anything that cites A through F, which is exactly the failure a numbered scheme would create at the worst moment.

#### 2.2 · The control page is the inventory, and no stage writes it
(`S-Appendix-0-control.md` is a family control page, the same kind as `S-Main-Dash`)
`../../paper/haipipe-paper-stage/stages/index.yml` declares no appendix stage, so the lettered pages are authored through section-edit and the control page is authored by hand.
It answers one question a reader cannot get from the units themselves: which units this paper has, and which of them are gated.

#### 2.3 · Where the MISQ paper stands against this
(the group is built as designed, and every unit is refused at the gate)
All seven pages exist under `Delivery · Appendix`.
G0 maps every appendix target and G1 correctly refuses all of them, because the A-F source is centralized and still OPEN, and the prompt and table leaves have not been split into their own regions.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · Every shipped leaf resolves to a gated source region.
  **Done when:** no `appendices/*.tex` leaf reaches a candidate without a unique non-empty selector pointing at a GATED page.

### A2 · 🎯 What we want on the paper board
- A2.1 · A paper board shows this concern as a control page plus one page per lettered unit.
  **Done when:** `Delivery · Appendix` lists an inventory page and one page per unit, and no unit is described only inside another unit's page.
- A2.2 · The MISQ prompt and table leaves are split into their own source regions.
  **Done when:** every MISQ appendix leaf has its own selector and G1 stops refusing the units.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · Ruled and carried in the Law: a wrapper holds wiring only, and every leaf needs an explicit authoritative source region.

### A2 · 🎯 What we want on the paper board
- ✅ A2.1 · Built as designed on the MISQ paper: a control page plus six lettered units under `Delivery · Appendix`.
- ❄️ A2.2 · Held while we work the design board. G0 maps all targets and G1 refuses every unit, and splitting the A-F source is paper work that thaws when we turn to the paper.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `board.md` · the `## Pages` order and the Board Map row for this concern
- `QB9-build.md` · owns manifest coverage and the gates that refuse an ungated leaf

📥 **Input files** · what the work reads

- `../../paper/S06-main/section-edit/stage.md` · the per-unit stage that authors an appendix page

## Law

- An appendix wrapper contains wiring only; every prose or template leaf must have an explicit authoritative source region.
  Appendix units are lettered rather than numbered, so a unit added late renumbers nothing that cites the others.

## Glossary

- **Wrapper**: a generated file whose only job is ordered `\input` wiring.
- **Leaf**: the prose or template inside a unit, which must resolve to a gated source region.

## Log

260802 · State moved from 🟡 to ✅. Every Aim is met or explicitly held, which is what ✅ means on a Q page; `partial-with-nothing-open` caught the mismatch.
260802 · Migrated to the QB4 page contract and given `### 2 · What we want on the paper board`. Two facts came out of it: this concern owns NO stage, so its pages are authored through section-edit and its control page by hand, and the units are LETTERED so a unit added late renumbers nothing.
260730 · MISQ manifest validated 20 outputs plus 8 explicit unreachable targets; Appendix remains G1-blocked.
