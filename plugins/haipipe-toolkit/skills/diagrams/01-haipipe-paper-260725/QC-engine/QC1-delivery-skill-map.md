# Delivery to Engine: the skill route map
state: 🟡 PARTIAL
owner: JL
method: map every Delivery group to callable skill routes without copying content authority into the Engine

## Opening
How can a reader start from one required delivery and see which skills serve it, what each may read or write, and where the route hands off?

The map must be many-to-many. A Main unit needs several skills across time, while `haipipe-paper-probe` serves Work, Literature, Value, Display, Main, and Appendix without becoming the authority for any of them. Paper, Probe, and Display routes all stand on Board's common page, index, sentence, and routing substrate. A route map that copies prose, values, gates, or Board contracts would create a second source of truth.

Scope: This page covers Delivery-to-skill routing, the shared card contract, the Board substrate, and the explicitly missing routes. QB1 through QB10 cover What each delivery means, its authoritative content, and its human completion gate. `QC5` owns the Paper Board's section, paragraph, sentence, and evidence requirements; it does not export those manuscript semantics to generic Boards. QF1 covers What happened when a named route was actually executed.

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
Engine is the entry point for a builder who asks which skill to call.
The target map is reversible: a Delivery page will name its Engine route, and every Skill page will name the Delivery pages it serves.
For now, this page is the canonical forward crosswalk; the per-page reciprocal links are intentionally listed as open work below.

### The Board substrate and the Paper writing dialect
`haipipe-board` is not an eleventh delivery route and it does not decide a manuscript's truth. It supplies the generic object on which every route works: a source page and generated webpage, seven page sections, index/group order, sentence addresses, lanes, anchored routing, and rendering.

This Paper Board supplies the next layer: what a paper section must accomplish for a reader, what job and progression a paragraph must have, and how a sentence's claim, citation, value, display, or owed question is made inspectable. The Board skills are therefore mirrored here as `Skill-6` through `Skill-10`, while `QC3` and `QC5` remain the authority for the Paper-specific overlay.

| Concern | Board substrate owns | This Paper Board owns |
|---|---|---|
| Page and index | Q/S shell, section boundaries, group order, render and write-back | which Paper stage or delivery occupies the page and what its Content means |
| Section and paragraph | generic headings, paragraph address and fold behavior | reader purpose, paragraph job, claim-to-evidence progression, venue/stage constraints |
| Sentence and evidence | one addressable source line, lanes, evidence-card surface | claim role, citation/value/display/owed semantics, local and sibling review |
| Route | routing an input to its owner without ticking it | whether the input changes a Paper argument, delivery, or human gate |

### Initial Delivery × Engine routes
| Delivery | Initial route | Current route state |
|---|---|---|
| Opening | `haipipe-paper` → lifecycle → stage → draft / revise | existing skill cohort |
| Work | stage → draft → paper-probe → `haipipe-probe` | existing skill cohort |
| Literature | draft → paper-probe → revise → format adapter | existing skills; adapter detail remains Delivery-owned |
| Value | paper-probe → revise → projection adapter | existing skills; structured binding check remains open |
| Display | stage → shared Display layer → project when shipped | Paper and Display keep separate authority |
| Main | stage → draft / probe / revise → project | Main-1 is the first executed candidate route |
| Appendix | stage → draft / probe / revise → project | G1-blocked until source divisions are gated |
| Present | accepted content → Present adapter | no callable Paper route yet |
| Build | deliver → project → conform / compile / Word leaves | project has an independent safety boundary to audit |
| Round | revise → diff → compile → ship | no callable Round route yet |

### Required fields on every skill card
Each Skill page will gain these short sections:

```text
Trigger · Serves · Reads · May write · Produces · Hands off · Refuses · Execute evidence
```

`Serves` links Delivery groups and explains the role played for each.
`May write` is narrower than `Serves`: a skill may support Main without owning Main Content.
For the five Board cards, `Serves` is the shared substrate and `May write` remains the Board contract's own narrow, anchored operation; their cards must never be read as authority to author Paper content.

## Aims
- [x] 🗺️ Create the Delivery × Engine crosswalk.
      It names routes without claiming their content or tests are complete.
- [ ] 🔗 Add `Engine route` and `Execute evidence` links to every Delivery overview.
      Each link must point to an existing skill page or state that the route is absent.
- [ ] 🧩 Add `Serves` and `Execute evidence` to the six existing Skill pages.
      Preserve their current control-flow account while making the Delivery relationship scannable.
- [ ] 🧱 Add reciprocal links from the Board substrate cards to the Paper-specific QC3/QC5 overlay.
      A reader must be able to move from generic Board grammar to the Paper requirements without treating either as a duplicate contract.
- [ ] 🛠 Audit Build for two possible first-class skill cards.
      `haipipe-paper-deliver` and `haipipe-paper-project` receive their own cards only if their responsibility cannot remain a leaf of an existing route.
- [ ] 🚧 Keep Present and Round explicitly route-missing.
      They become runnable only after a callable contract and bounded execution exist.

## States
The crosswalk shape is now explicit, including the distinction between three delivery-serving lanes (Paper, Probe, Display) and the Board substrate they share.
Only Main-1 has a recorded candidate-only execution through its Build route; it is blocked at G4 and is recorded on `QF1`.
No Delivery authority moved into this page.

## Files
- `board.md`
  Declares Delivery-first reading and the Engine card contract.
- `QB-delivery/`
  Own the delivery-side links.
- `Skill-0*.md`
  Existing initial skill cohort that will gain route fields.
- `QF-execute/QF1-execution-map.md`
  Owns actual run evidence.

## Law

- Delivery owns canonical content and the human completion decision.
  Engine maps callable skill routes across that content but never becomes a second authoring authority.
  Every claimed route must name its Execute evidence or state that no execution exists.
- Board owns generic working-record mechanics, not manuscript semantics. This Paper Board owns the Paper dialect above that substrate; section, paragraph, sentence, and evidence requirements belong to QC3/QC5 and must not be copied into the generic Board skill.

## Glossary
- **Skill route**: the ordered callable skills that may serve one delivery.
- **Serves**: a skill's limited role for a Delivery group, not ownership of its content.

## Log
260801 · Consolidated the route map into QC Engine; Delivery now lives as QB1–QB10 rather than ten separate groups.
260801 · Added the Board substrate as a first-class Engine participant and located the Paper-specific writing dialect in QC3/QC5 rather than the generic Board contracts.
260730 · Created after JL accepted a Delivery-first, skill-first Engine structure and replaced the proposed Test layer with Execute.
