## 0.6.2 — 2026-08-31

- **Phase law location named** (workflow-phases restructure, JL 260831): each
  journey phase's own law now ships as `workflow-phases/haipipe-paper-<phase>`;
  one pointer line added above the six-phase table. Gates, names, groups
  unchanged.

## 0.6.1 — 2026-08-31

- **The appendix token is `SA`, Section-Appendix** (JL 260831: "The AM is not
  correct, it should be SA"): a desk group's pages are `S<D><NN>` main
  sections, `SA<NN>` appendix sections, `RD<NN>` rounds. The Round ledger
  grammar (`SA-PP<n>` rows) already said so; the page ids now agree. MISQ
  renamed AM01-AM06 → SA01-SA06 the same day; boards still on `A<D>` are
  grandfathered until their own rename.

## 0.6.0 — 2026-08-28

- **Six phases: the Collection page folded into the Roadmap** (JL 260828: the
  two were plan and result of the same campaign, one-to-one; the lap-L1 field
  test showed every Collection edit forcing a mirrored Roadmap edit). P2
  Roadmap (route) now carries plan AND intake; Narrative, Section, Round
  renumber P3/P4/P5. The establish loop is P1↔P2.
- **Gate numbers unchanged**: G2 (plan → dispatch) and G3 (lap → Seed) both
  read the Roadmap now — its plan face and its lap face — and both leave
  their receipt Log rows there. Three pens become two: the Roadmap plans and
  registers; the Seed alone flips.
- Group mapping: P0–P2 in A1-SD-story (three pages), P3 in A2-NA-narrative,
  P4–P5 in the desks' B groups. Boards with a separate SD03-collection page
  are grandfathered; the gazette gains the 0.6.0 renumber rows.

## 0.5.0 — 2026-08-24

- **Seven phases, named by their authority pages** (JL 260824: "phase 和 page
  名字起得一模一样"): Ideation (ideate) → Seed (establish) → Roadmap (route) →
  Collection (collect) → Narrative (tell) → Section (realize) → Round
  (respond). The old verbs survive as parenthesized aliases (JL: keep the
  word in the phase's parentheses); the naming law forbids any future phase
  from taking a name its authority page does not carry.
- **Roadmap and Collection promoted to full journey phases** (JL 260824,
  overruling the engine-inside-P1 design): P1↔P2↔P3 is the establish loop —
  Seed states gaps, Roadmap plans and a person releases, Collection collects
  and the settle is written back on the Seed; the loop's only exit is G4.
- **Gates renumbered G0-G7** with the old G1-G4 gazetted in-file; new G1
  (skeleton stands), G2 (every gap has a released row or waiver), G3 (lap
  done-when + settle on the Seed).
- **Group mapping**: P0-P3 → A1-SD-story, P4 → A2-NA-narrative, P5-P6 → one
  B group per desk holding sections AND rounds; old layouts grandfathered.

## 0.4.0 — 2026-08-24

- **Ideation-first story order** (JL 260824, with ideation 0.4.0): P0's
  authority page is A1-SD-story/SD00-ideation, the seed sits at SD01, and G0's
  receipt reads: SD01-seed exists and its §5 first row binds SD00-ideation
  back. The separate A0 group is abolished.

## 0.3.0 — 2026-08-24

- **P0 renamed IDEATE** (JL 260824, with ideation 0.3.0: the P0 act is
  thinking up ideas — "想 idea 的过程,然后才是 seed"): the journey reads
  Ideate → Establish → Tell → Realize → Respond; authority page `ideation`
  at `0-paperboard/A0-ID-ideation/`; G0 is `Ideate → Establish`.

## 0.2.0 — 2026-08-23

- **P0's home moves with explore 0.2.0** (JL 260823: the nursery belongs in
  the paper's own board, before the seed): the phase table reads
  `explore (paperboard/A0)` and notes the repo is minted WITH that page; the
  standing IdeaBoard is retired unshipped.
- **G0's receipt becomes same-board**: SD00-seed exists in this board's
  A1-SD-story with §5's first row binding the Explore Page back; an idea
  graduating into a DIFFERENT paper additionally requires that new repo to
  exist as a submodule.

## 0.1.0 — 2026-08-23

- **Created as the thin five-phase machine** over the six Page Types (JL
  260823): owns gates G0-G4 and phase receipts only; explicitly NOT a revival
  of the deleted S01-S10 stage lane, which owned content contracts and
  tooling. Gates are grep-able assertions over existing pages; phase is read,
  not stored, per telling from P2 on; advancement is never scheduled (ARIS
  external-cadence rule). Terminology law: journey phase ≠ Page phase.