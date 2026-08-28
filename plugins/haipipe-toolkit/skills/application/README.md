# Application skill family

An Application is TWO boards. One understands the data; the other designs what gets sent. It ends at accepted.

```text
🔎 InsightBoard                                    🎨 DesignBoard
Meta + Question registers → D→I→K→W  ── PageX ──▶  Brief → Principle → Design → ✅ accepted
MT00 says what EXISTS                              P warrants when promoted; cards GRANT by path
MT01-MT04 say what is ASKED of each rung           render/ plugin projects accepted divisions
```

## Ownership

| Layer | Owns | Does not own |
|---|---|---|
| Task/Discovery | execution and source evidence | Application framing |
| InsightBoard · Meta | source inventory, grain, freshness | any interpretation, any question |
| InsightBoard · Question registers | what is asked of each rung, raiser, state, the board rollup (on MT04) | any answer, any probe |
| InsightBoard · D/I/K/W | Task-backed Probe, observations → patterns → claims → counsel, Design Handoff (W only) | final message copy |
| DesignBoard · Brief | opportunity, audience, outcome, venue scope, needs raised | the answers to those needs |
| DesignBoard · Principle | because-<W>-do-<move>-within-<rail> warrants · the promoted WARRANT crossing (a direction card GRANTS evidence by path, a different act) | raw Task/Discovery inspection |
| DesignBoard · Design | PageX selection, message system, per-division acceptance | probing anything |

Folder ownership does not transfer evidence authority. A D page lives in the Application folder but follows Task source/run/staleness rules.

Six sibling skills head the family: `haipipe-application/` is the umbrella door (what an Application IS, the pairing, PageX, ends-at-ACCEPTED), `haipipe-application-workflow/` is the RUN head (five phases in two lanes named by their authority pages — Meta, Chain, Wisdom · Brief, Design — with gates G0-G5; four human gates in all, two per door — G2 handoff and G5 acceptance between phases, probe release and card release inside P1 and P4), each board has its own law door — `haipipe-insight/` (the one-dataset law, the Climb Law, the three pens, probe release + handoff signing) and `haipipe-design/` (the Reads Law, direction cards, artifact units, card release + acceptance) — and each lane additionally has its own phase machine — `haipipe-insight-workflow/` (I0-I5 named by the lane's six page types, gates GI0-GI6, the register cell as frontier unit, refining P0-P2 as I0+I1 / I2-I4 / I5) and `haipipe-design-workflow/` (D0-D4 named by the lane's artifact classes, gates GD0-GD5, the division as frontier unit, rounds with the reflect/prospect verdict and the EMIT edge, refining P3-P4 as D0 / D1-D4). An InsightBoard has two layouts, chosen once at scaffold: rung-major (groups are the four rungs, the default) and partition-major (groups are partitions, `F` template + the index-free `X-cross`; grammar in `haipipe-application/ref/partition.md`).

## Page Types

```text
application/page-types/
├── haipipe-page-for-meta/         one InsightBoard head · what data exists · NO question
├── haipipe-page-for-question/     four registers MT01-MT04 · what is asked of each rung
├── haipipe-page-for-data/         D · observed, run-bound, uninterpreted
├── haipipe-page-for-information/  I · rates and contrasts derived from named D rows
├── haipipe-page-for-knowledge/    K · a proposition with strength, rivals, boundary
├── haipipe-page-for-wisdom/       W · counsel + Design Handoff · the only bindable level
├── haipipe-page-for-brief/        one DesignBoard head · what is being built, for whom
├── haipipe-page-for-principle/    P · why this will work · the WARRANT crossing,
│                                      when promoted; cards grant evidence
└── haipipe-page-for-design/       DS · one audience × job × venue message system
```

`page-type: insight` is TASK-ONLY (the whole chain in one consumer-neutral page, `task/page-types/`). Retired 2026-08-20: `intervention` became `design`; `artifact` was absorbed into a per-division `accepted:` row. Split 2026-08-21: the Meta page's Insight Roster became the four question registers.

## Target runtime

A board's folder name says its subject: the data for an InsightBoard, the topic for a DesignBoard. PascalCase subject, literal kind, so `ls *-DesignBoard` finds them all.

```text
<application-root>/
├── InsightBoard-<Cohort>/                e.g. InsightBoard-SMSR2Full
│   ├── board.md
│   ├── 0-MT-meta/
│   │   ├── MT00-meta/                    sources · grain · freshness · limits
│   │   ├── MT01-question-data/           QD<n> · asks of 1-D-data/
│   │   ├── MT02-question-information/    QI<n> · asks of 2-I-information/
│   │   ├── MT03-question-knowledge/      QK<n> · asks of 3-K-knowledge/
│   │   └── MT04-question-wisdom/         QW<n> · asks of 4-W-wisdom/ + board rollup
│   ├── 1-D-data/D<NN>-<slug>/            observed · run-bound
│   ├── 2-I-information/I<NN>-<slug>/     derived · cites D
│   ├── 3-K-knowledge/K<NN>-<slug>/       claimed · cites I
│   └── 4-W-wisdom/W<NN>-<slug>/          counsel + handoff · cites K
└── DesignBoard-<Program>/                e.g. DesignBoard-RefillFraming
    ├── board.md
    ├── 0-BR-brief/BR00-brief/            outcome · venue scope · audience set · needs
    ├── 1-P-principle/P<NN>-<slug>/       cites W · the WARRANT crossing, promoted only
    └── 2-DS-design/DS<NN>-<slug>/        units as divisions · render/ plugin projections
```

Because the subjects are named independently, the count is free: several InsightBoards when the Application reads distinct data, several DesignBoards when it designs for distinct topics, and any DesignBoard may PageX-bind any InsightBoard.

A project using the `<Letter><NN>_<slug>` folder grammar may prefix runtime boards for ordering — `A<NN>_` InsightBoards, `B<NN>_` DesignBoards, as in `A01_InsightBoard-SMSR2Full` — a project-local prefix that never appears inside pages.

The MT group law: **nothing in MT concludes**. Meta describes, the registers ask, and neither owns `probe/` or `display/`, because a probe brings back an answer and a figure is one. Only D/I/K/W pages own `probe/`. Each Design Page owns `pagex/` bindings to exact Brief and W-handoff material, and PageX crosses boards unchanged because it binds by path.

## The Application ends at accepted

Deciding that an exact version may go is a design judgment and stays on the DesignBoard. Building it, shipping it, running the experiment, and collecting what came back are task-layer work. There is no `deploy/` folder and no round folder; the loop closes back through a source refresh reopening D pages, not through a stage on this board.

## Router

```text
/haipipe-application meta              inventory the data this board reads
/haipipe-application question          register one question on the rung register it faces
/haipipe-application chain             open or extend one D→I→K→W chain for one question
/haipipe-application brief             frame what is being built and the needs it raises
/haipipe-application design            author one audience/job/venue message system
/haipipe-application render            project an accepted division through the render/ plugin
/haipipe-application review | accept   exact-version gates, per division
/haipipe-application retarget          re-pin venue or audience, reopen dependent Design
```

## Compatibility

Legacy stage skills under `_old/` remain readers during migration. New work does not copy the descriptions/themes/claims/advice ladder, a flat `1-probes/`, a `4-deploy/`, or a `5-rounds/`. An existing page carrying `page-type: intervention` has its key renamed to `design`; one carrying `page-type: artifact` folds into its Design Page as a division. A Meta page still carrying an Insight Roster moves those rows to the four registers, keeping each question's raiser. External settled Insight Pages remain valid PageX inputs and are never moved automatically.

## Family status

Run 260828 · regenerate with `/haipipe-skillset-status` over `skills/application/` · every SKILL.md in this family read in full that session · field records counted off `designs/Project-Application-SMSDesign/applications/` and the four fieldtest rounds of 260827-28. A row whose field record is empty reads `(provisional)` whatever its static score.

**DOOR** · does every road lead somewhere

```text
| skill                | ver    | routes | resolve | stale                  | scaffold | desc shape |
|----------------------|--------|--------|---------|------------------------|----------|------------|
| haipipe-application  | 0.18.0 |   8    |  8/8    | ✗ draws `direction/`,  | ◐        | ✓          |
|                      | 260827 |        |         |   retired 260828       |          |            |
| haipipe-insight      | 0.6.0  |  14    | 14/14   | none                   | ✓        | ✓          |
| haipipe-design       | 0.6.0  |  10    | 10/10   | none                   | ✓        | ✓          |
```

Both lane doors now carry a `page types this door owns` roster (0.6.0 each); before that the folder was the only ownership signal and it holds all nine contracts flat. The umbrella's runtime tree still draws the retired `direction/` folder, which no longer exists on disk anywhere.

**MACHINE** · how much of the machine has ever run

```text
| skill                         | ver   | phases | gates | receipt owner | fired live | gazette |
|-------------------------------|-------|--------|-------|---------------|------------|---------|
| haipipe-application-workflow  | 0.8.0 |   5    |   6   |     6/6       |    2/6     |   ✓     |
| haipipe-insight-workflow      | 0.4.0 |   6    |   7   |     7/7       |    2/7     |   —     |
| haipipe-design-workflow       | 0.6.0 |   5    |   6   |     6/6       |    5/6     |   —     |
```

`fired live` counts gate ids appearing on the two live boards, not in the workflow files. Every gate names the page whose Log row is its receipt, which is the property that makes the unfired ones auditable later rather than merely unwritten.

**CONTRACT** · the eight properties · ✓ 1 · ◐ 0.5 · ✗ 0 · — not applicable

```text
| contract         | ver     | ①  | ②  | ③  | ④ | ⑤  | ⑥  | ⑦  | ⑧  | instances | tier      |
|------------------|---------|----|----|----|---|----|----|----|----|-----------|-----------|
| for-meta         | 0.3.0   | ◐  | ✓  | ✓  | — | ✓  | ✓  | ✓  | ✓  |     1     | EXERCISED |
| for-question     | 0.5.0   | ✓  | ✓  | ✓  | — | ✓  | ✓  | ✓  | ✓  |     4     | EXERCISED |
| for-data         | 0.2.0   | ◐  | ✓  | ✓  | — | ✓  | ✓  | ✓  | ✓  |     8     | EXERCISED |
| for-information  | 0.3.0   | ◐  | ✓  | ✓  | — | ✓  | ✓  | ✓  | ✓  |    80     | EXERCISED |
| for-knowledge    | 0.3.0   | ✓  | ✓  | ✓  | — | ✓  | ✓  | ✓  | ✓  |    12     | EXERCISED |
| for-wisdom       | 0.4.0   | ◐  | ✓  | ✓  | — | ✓  | ✓  | ✓  | ✓  |     7     | EXERCISED |
| for-brief        | 0.4.0   | ◐  | ✓  | ◐  | — | ✓  | ✗  | ✓  | ✓  |     1     | USED      |
| for-design       | 0.6.1   | ✓  | ✓  | ✓  | — | ✓  | ✗  | ✓  | ✓  |     1     | USED      |
| for-principle    | 0.2.1   | ✓  | ✓  | ✓  | — | ✓  | ✗  | ✓  | ✓  |     2     | USED      |
```

The whole insight lane earned ⑥ on 260828: `## Boundary` and the 🟡-final receipt duty across the four rungs, then `## Receipts` on MT00 (GI0, every partition birth) and on the registers (GI1, GI6, the register's half of the 🟡-final pair). The three remaining ⑥ failures are all design-side, and all the same defect at different addresses — a gate's receipt duty (G4/GD0 on BR00, GD1-GD5 on the DS page) stated only in the machine file, which the ruler is explicit does not count. ④ is `—` family-wide: no page type here carries a size-or-budget clause, which is correct for contracts and worth revisiting only if a board ever commissions its own runs.

**LIBRARY** · assets, and whose clock they keep

```text
| asset            | count | neutral | clock | consumed at        | oldest verify |
|------------------|-------|---------|-------|--------------------|---------------|
| venue/ packs     |   8   |   ✓     |  ✗    | D2 realize · GD3   |     none      |
```

Eight packs (sms · email · dashboard · report · push · reminder · checklist · ui-card) under one `_SCHEMA.md`, correctly written for no single consumer and read by the designer at realize and the judge at GD3. **No pack carries a verify date at all**, so the bank has no staleness floor and nothing can say whether an exemplar still reflects its venue.

**CRAFT** · none. This family owns no transform with its own scope; `check.py` belongs to the board family.

### The two knife points

**① The receipt duty is still homeless on the design side.** Each gate's receipt is defined in a workflow file and owed by a page whose contract never mentions it, so an author reading only their own contract cannot know what they owe. The insight lane closed this on 260828 across all six of its contracts; `for-brief` and `for-design` have not, and between them they carry G4/GD0 and GD1-GD5 — every receipt the design lane produces.

**② The ruler cannot see between contracts, and that is where this family's live defects are.** Three of them were live this week: seven of nine `last_updated` fields contradicted their own CHANGELOG, all nine reconciled on 260828; three skills still draw a `direction/` folder retired on 260828 (`haipipe-application`, `for-design`, `for-principle`); and until 260828 four contracts carried byte-identical copies of one chain law. None of the eight properties scores any of these, because all three are relations BETWEEN files. A ninth property — *shared law is cited, not copied; derived headers agree with their source* — would catch all three, and is the single highest-value addition to the instrument.
