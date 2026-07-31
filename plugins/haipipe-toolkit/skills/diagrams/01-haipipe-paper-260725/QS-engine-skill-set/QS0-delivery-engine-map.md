# Delivery to Engine: the skill route map
state: 🟡 PARTIAL
owner: JL
method: map every Delivery group to callable skill routes without copying content authority into the Engine

## Question
How can a reader start from one required delivery and see which skills serve it, what each may read or write, and where the route hands off?

The map must be many-to-many. A Main unit needs several skills across time, while `haipipe-paper-probe` serves Work, Literature, Value, Display, Main, and Appendix without becoming the authority for any of them. A route map that copies prose, values, or gates would create a second source of truth.

## Boundary
- ✅ Covered here
  Delivery-to-skill routing, the shared card contract, and the explicitly missing routes.
- ↪ Covered by QF through QP
  What each delivery means, its authoritative content, and its human completion gate.
- ↪ Covered by QE0
  What happened when a named route was actually executed.

## Diagram
```text
Delivery group ── serves ──▶ skill route ── runs ──▶ Execute record
      │                          │                    │
      │                          └─ reads / may write  └─ receipt or observation
      └─ owns artifact and authority
```

## Content
### The direction of the map
Delivery is the entry point for a reader who asks what the paper needs.
Engine is the entry point for a builder who asks which skill to call.
The target map is reversible: a Delivery overview will name its Engine route, and every Q-Skill page will name the Delivery groups it serves.
For now, this page is the canonical forward crosswalk; the per-page reciprocal links are intentionally listed as open work below.

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
Each Q-Skill page will gain these short sections:

```text
Trigger · Serves · Reads · May write · Produces · Hands off · Refuses · Execute evidence
```

`Serves` links Delivery groups and explains the role played for each.
`May write` is narrower than `Serves`: a skill may support Main without owning Main Content.

## Items to Finish
- [x] 🗺️ Create the Delivery × Engine crosswalk.
      It names routes without claiming their content or tests are complete.
- [ ] 🔗 Add `Engine route` and `Execute evidence` links to every Delivery overview.
      Each link must point to an existing skill page or state that the route is absent.
- [ ] 🧩 Add `Serves` and `Execute evidence` to the six existing Q-Skill pages.
      Preserve their current control-flow account while making the Delivery relationship scannable.
- [ ] 🛠 Audit Build for two possible first-class skill cards.
      `haipipe-paper-deliver` and `haipipe-paper-project` receive their own cards only if their responsibility cannot remain a leaf of an existing route.
- [ ] 🚧 Keep Present and Round explicitly route-missing.
      They become runnable only after a callable contract and bounded execution exist.

## Where we are
The crosswalk shape is now explicit.
Only Main-1 has a recorded candidate-only execution through its Build route; it is blocked at G4 and is recorded on `QE0`.
No Delivery authority moved into this page.

## Files
- `board.md`
  Declares Delivery-first reading and the Engine card contract.
- `QF-delivery-map/` through `QP-delivery-round/`
  Own the delivery-side links.
- `Q-Skill-haipipe-paper*.md`
  Existing initial skill cohort that will gain route fields.
- `QE0-execution-map.md`
  Owns actual run evidence.

## Law
Delivery owns canonical content and the human completion decision.
Engine maps callable skill routes across that content but never becomes a second authoring authority.
Every claimed route must name its Execute evidence or state that no execution exists.

## Glossary
- **Skill route**: the ordered callable skills that may serve one delivery.
- **Serves**: a skill's limited role for a Delivery group, not ownership of its content.

## Log
260730 · Created after JL accepted a Delivery-first, skill-first Engine structure and replaced the proposed Test layer with Execute.
