# Delivery to Engine: the skill route map
state: 🟡 PARTIAL
owner: JL
method: map every Delivery group to callable skill routes without copying content authority into the Engine

## Opening
How can a reader start from one required delivery and see which routes serve it, what each may read or write, and where the route hands off?

The map must be many-to-many. A Main unit needs several routes across time, while the PROBE phase serves Work, Literature, Value, Display, Main, and Appendix without becoming the authority for any of them. Since 260805 the paper family registers exactly ONE skill, `haipipe-paper`; a route is now a stage key, a phase, or an `fn/` verb inside that one door, not a separate skill. Paper, Probe, and Display routes all stand on Board's common page, sentence, and routing substrate. A route map that copies prose, values, gates, or Board contracts would create a second source of truth.

Scope: This page covers Delivery-to-route mapping, the shared card contract, the Board substrate, and the explicitly missing routes. QB1 through QB10 cover What each delivery means, its authoritative content, and its human completion gate. `QC5` owns the Paper Board's section, paragraph, sentence, and evidence requirements; it does not export those manuscript semantics to generic Boards. QF1 covers What happened when a named route was actually executed.

## Diagram
```text
                         Board substrate
           Board-Folder/Webpage · page/index grammar · sentence address
                         comments · routing · render
                                  ▲
Delivery group ── serves ──▶ Paper / Probe / Display route ──▶ Execute record
      │                          │                                  │
      │                          └─ reads / may write                └─ receipt or observation
      └─ owns artifact and authority

Paper Board dialect: section purpose · paragraph job and progression ·
sentence claim/evidence/attachment requirements. It is carried by QC3/QC5,
not by the generic Board substrate.
```

## Content
### The direction of the map
Delivery is the entry point for a reader who asks what the paper needs.
Engine is the entry point for a builder who asks which route to invoke.
The target map is reversible: a Delivery page will name its Engine route, and the Skill page will name the Delivery pages it serves.
For now, this page is the canonical forward crosswalk; the per-page reciprocal links are intentionally listed as open work below.

A route is no longer a skill name. Thin-paper phases 2 and 3 (260805 and 260806) folded `haipipe-paper-enter`, `-lifecycle`, `-stage`, the draft/probe/revise/check workers, the folder/conform/build verbs, and round/rebuttal into `paper/haipipe-paper`; the retired folders sit in `paper/_old/`. What a route names today is one of four things: a stage key in `paper/haipipe-paper/stages/index.yml`, a phase contract under `board/page-phases/`, an `fn/` verb procedure in the door's own folder, or a separately registered worker skill the stage `commissions:` (the four Display renderers).

### The Board substrate and the Paper writing dialect
`haipipe-board` is not an eleventh delivery route and it does not decide a manuscript's truth. It supplies the generic object on which every route works: a source page and generated webpage, five on-stage page sections plus Files and the folded ones, index/group order, sentence addresses, lanes, anchored routing, and rendering.

This Paper Board supplies the next layer: what a paper section must accomplish for a reader, what job and progression a paragraph must have, and how a sentence's claim, citation, value, display, or owed question is made inspectable. The Board skills are NOT mirrored on this board: their mirror pages live on the Boardform design board's `7-QCskill-engine-skill/`, and this board's `7-QCskill-engine-skill/` carries exactly one page, `Skill-0-haipipe-paper.md`. `QC3` and `QC5` remain the authority for the Paper-specific overlay.

| Concern | Board substrate owns | This Paper Board owns |
|---|---|---|
| Page and index | Q/S shell, section boundaries, group order, render and write-back | which Paper stage or delivery occupies the page and what its Content means |
| Section and paragraph | generic headings, paragraph address and fold behavior | reader purpose, paragraph job, claim-to-evidence progression, venue/stage constraints |
| Sentence and evidence | one addressable source line, lanes, evidence-card surface | claim role, citation/value/display/owed semantics, local and sibling review |
| Route | routing an input to its owner without ticking it | whether the input changes a Paper argument, delivery, or human gate |

### Delivery × Engine routes
One record per delivery: the callable route, then its state.

- **Opening** → `/haipipe-paper seed | venue | pitch`; stage data under `paper/S01-opening/`.
  Live. Three stage keys, each with its own `stage.md`; venue pins before the venue-aligned stages run.
- **Work** → `/haipipe-paper resource | claims | narrative`; stage data under `paper/S02-work/`.
  Live. Venue-free; `claims` declares `craft: [citation, values]` and is the only home of a claim's status.
- **Literature** → the PROBE phase filling an evidence page; page data under `paper/S03-literature/`.
  Live. No stage key of its own: the page is Page Type `for-literature`, and PROBE writes its `E<n>` divisions.
- **Value** → the PROBE phase filling an evidence page; page data under `paper/S04-value/`.
  Live. Same shape as Literature, Page Type `for-value`; the structured binding check remains open.
- **Display** → `/haipipe-paper display`; stage data under `paper/S05-display/`.
  Live. The stage's `commissions:` names the four renderers, which stay separately registered skills.
- **Main** → `/haipipe-paper section-edit <section>`; stage data under `paper/S06-main/`.
  Live, `runs: per-unit`. Main-1 is still the only recorded candidate execution (`QF1`).
- **Appendix** → no stage key; `paper/S07-appendix/` holds no stage data.
  Route missing. The delivery is defined on `QB7` and nothing callable has been built for it.
- **Present** → no stage key; `paper/S08-present/` holds no stage data.
  Route missing, deliberately. `QB8` owns the delivery definition.
- **Build** → the door's `fn/` verbs: `folder`, `conform`, `compile`, `diffpdf`, `project`, `to-overleaf`, `to-word`.
  Live. Since 260806 these are procedures inside the one skill, not skills; tooling sits under `paper/haipipe-paper/scripts/`.
- **Round** → `/haipipe-paper round <n|new>` and `rebuttal`; stage data under `paper/S10-round/`.
  Live since 260806, `runs: per-unit`, one unit per dated round. Callable, but no execution recorded yet.

### Required fields on every skill card
The one Skill page on this board, `Skill-0-haipipe-paper`, will gain these short sections:

```text
Trigger · Serves · Reads · May write · Produces · Hands off · Refuses · Execute evidence
```

`Serves` links Delivery groups and explains the role played for each.
`May write` is narrower than `Serves`: a route may support Main without owning Main Content.
Because the door now serves every delivery, `Serves` on that one card is a list of ROUTES and the deliveries each one carries, not a single relationship.
The Board substrate cards live on the Boardform board and are not restated here; nothing on that board may be read as authority to author Paper content.

## Aims
- [x] 🗺️ Create the Delivery × Engine crosswalk.
      It names routes without claiming their content or tests are complete.
- [ ] 🔗 Add `Engine route` and `Execute evidence` links to every Delivery overview.
      Each link must point to a route record above, or state that the route is absent.
- [ ] 🧩 Add `Serves` and `Execute evidence` to `Skill-0-haipipe-paper`.
      Preserve its current control-flow account while making the ten Delivery relationships scannable from one card.
- [ ] 🧱 Add reciprocal links from the Boardform board's substrate pages to the Paper-specific QC3/QC5 overlay.
      A reader must be able to move from generic Board grammar to the Paper requirements without treating either as a duplicate contract.
- [x] 🛠 Audit Build for first-class skill cards.
      Settled by the 260806 collapse: `project` is `fn/project.md` and the `deliver` umbrella is retired to `paper/_old/`, so neither earns a card.
- [ ] 🚧 Keep Present explicitly route-missing.
      It becomes runnable only after a callable contract and bounded execution exist. Round left this state on 260806 and now has a stage key.

## States
The crosswalk shape is now explicit, including the distinction between three delivery-serving lanes (Paper, Probe, Display) and the Board substrate they share.
The route column did NOT survive the 260805-260806 collapse to one registered skill: its ten rows named retired skills (`-lifecycle`, `-stage`, `-draft`, `-probe`, `-revise`) and were rewritten in the 260806 sweep. Every row now resolves to a stage key, a phase, or an `fn/` verb inside `paper/haipipe-paper`.
Eight of the ten deliveries are callable. Appendix and Present are the two with no route, and Round left that state on 260806.
Only Main-1 has a recorded candidate-only execution through its Build route; it is blocked at G4 and is recorded on `QF1`.
No Delivery authority moved into this page.

## Files
- `board.md`
  Declares Delivery-first reading and the Engine card contract.
- `2-QB-delivery/`
  Own the delivery-side links.
- `7-QCskill-engine-skill/Skill-0-haipipe-paper/Skill-0-haipipe-paper.md`
  The one Skill page on this board; it will gain the route fields.
- `paper/haipipe-paper/stages/index.yml`
  The roster every stage route resolves against.
- `8-QF-execute/QF1-execution-map/QF1-execution-map.md`
  Owns actual run evidence.

## Law

- Delivery owns canonical content and the human completion decision.
  Engine maps callable skill routes across that content but never becomes a second authoring authority.
  Every claimed route must name its Execute evidence or state that no execution exists.
- Board owns generic working-record mechanics, not manuscript semantics. This Paper Board owns the Paper dialect above that substrate; section, paragraph, sentence, and evidence requirements belong to QC3/QC5 and must not be copied into the generic Board skill.

## Glossary
- **Skill route**: the ordered callable steps that may serve one delivery. Since 260806 a step is a stage key, a phase contract, an `fn/` verb, or a commissioned worker skill, not one skill per step.
- **Serves**: a route's limited role for a Delivery group, not ownership of its content.

## Log
- 260806 2222 · [REVISE-CC] swept to the 260806 architecture; the ten routes now name stage keys, phases, and `fn/` verbs inside the one registered skill, and the false `Skill-6`-`Skill-10` Board mirror roster is corrected to this board's single `Skill-0-haipipe-paper` page.
260801 · Consolidated the route map into QC Engine; Delivery now lives as QB1–QB10 rather than ten separate groups.
260801 · Added the Board substrate as a first-class Engine participant and located the Paper-specific writing dialect in QC3/QC5 rather than the generic Board contracts.
260730 · Created after JL accepted a Delivery-first, skill-first Engine structure and replaced the proposed Test layer with Execute.
