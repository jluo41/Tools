# Execute: delivery routes on a real paper
state: 🟡 PARTIAL
owner: JL
method: record bounded runs from a named Delivery target through a named Engine route, with an artifact, evidence, and an owning reopen path

## Opening
How should the Board distinguish a delivery design from an actual execution that produced, checked, or blocked a concrete artifact?

An execution is more than a unit test. It runs a route on a fixture or real paper under explicit non-write limits, observes what happened, and links failure back to the Delivery or Engine page that owns the repair. It must not turn a receipt into permission to overwrite submission files.

Scope: This page covers Execute-record shape, execution modes, and the first MISQ candidate record. QB1 through QB10 cover The desired delivery, canonical content, and human completion gate. QC1 covers The reusable skill route that an execution invokes. QB9 covers The Build deliverable and its promotion law.

## Diagram
```text
Delivery target + Engine route + named fixture
                    │
                    ▼
             bounded execution
                    │
      artifact / candidate / observation
                    │
       gate + receipt + non-write check
                    │
      pass → next allowed handoff
      fail → reopen owning Delivery or Engine page
```

## Content
### Execute is not a second authoring layer
Delivery pages remain the only content authority.
Engine pages remain reusable route definitions.
Execute records what occurred when a route was run, including a block that prevents the run from reaching the next handoff.

### Three kinds of execution evidence
| Mode | What it proves | Example |
|---|---|---|
| Mechanical | Declared paths, contracts, and static closure obey the route | manifest validation or a contract checker |
| Candidate | A bounded route makes an isolated artifact without touching submission authority | Main-1 → `3-dist/tex/<run-id>/` |
| Fresh agent | A clean-context agent finds the entry, follows the route, and stops at the right boundary | `QF3` stage acceptance run |

### First recorded execution: MISQ Main-1 Build route
| Field | Record |
|---|---|
| Delivery target | Main → Build, `main-1` introduction projection |
| Engine route | stage authority → `haipipe-paper-project` generate/check/compile boundary |
| Fixture | Paper-Personality2Opioid-MISQ2026, candidate-only run |
| Artifact | content-addressed candidate under `3-dist/tex/f53ccf5c5fc965bbc0c74f478e9015ac8ded949e91e7bc35a667c54cc38ffa98/` |
| Evidence | G0 exact coverage, G1 gate, G2 isolation, and G3 pre-render marker checks passed |
| Block | G4 refuses the baseline missing `displays/S-Display-4a-main-regression/float.tex` |
| Non-write boundary | No submission file changed and G5 was not run |
| Reopen path | Repair the owning Display projection, then rerun isolated G4 from QB9 |

## Items to Finish
- [x] 🧾 Define Execute as a bounded real or fixture run.
      Tests, gates, receipts, compiles, and fresh-agent observations are evidence within Execute.
- [x] 🔒 Record the Main-1 candidate-only execution without promotion.
      G0-G3 pass; G4 is blocked by an existing Display dependency; G5 remains unrun.
- [ ] 🔗 Link every Delivery overview to the relevant Execute record or explicit absence.
      A missing run must remain visible rather than being inferred from an Engine design.
- [ ] 🧪 Add a fresh-agent execution for a complete route.
      `QF3` remains the behavioral acceptance owner and must observe process as well as output.
- [ ] 🔁 Define the Round execution record after Round has a callable route.
      The record must connect reviewer input, chosen action, diff, compile, and resubmission.

## Where we are
Execute now names the Board's third layer.
The Main-1 candidate is the first recorded execution and remains deliberately blocked before promotion.
Present and Round have delivery definitions but no runnable Execute record yet.

## Files
- `QB-delivery/QB9-build.md`
  Owns the Build delivery contract and G5 promotion law.
- `QC-engine/QC1-delivery-skill-map.md`
  Owns the Delivery × Engine route map.
- `2-src/projection-receipts/`
  Holds immutable records of the MISQ candidate run.
- `3-dist/tex/f53ccf5c5fc965bbc0c74f478e9015ac8ded949e91e7bc35a667c54cc38ffa98/`
  Holds the candidate artifact.

## Law
An execution must name its Delivery target, Engine route, fixture, observable evidence, non-write boundary, and failure-to-reopen path.
Passing an execution permits only its declared next handoff; it never implies promotion.

## Glossary
- **Execute**: a bounded run that records what actually happened when a Delivery route was invoked.
- **Non-write boundary**: files or authorities the run is prohibited from changing.

## Log
260801 · Renamed into QF Execute after the Paper Skill-Board consolidated its groups.
260730 · Created after JL replaced the proposed Test layer with Execute and accepted the Delivery-first, skill-first Engine design.
