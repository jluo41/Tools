# dashboard: the venue a reader operates instead of reads
state: 🔴 OPEN
owner: JL
method: state what the channel gates, rewards, and refuses from the pack's two files against the schema, and record what it cannot answer as GAP rows rather than filling them

## Opening

A dashboard is the venue a reader operates instead of reads: they filter, drill down, and act on live numbers.
So what does its pack know: what does the channel gate, reward, and require of claims settlement, display, and data contracts?
The pack is two short files, and they fire every lifecycle stage at the full settlement bar.
This page states what those files rule, what desk-rejects a dashboard, and what the schema demands that the pack cannot answer.

**Where this page sits**: it is one venue pack in `QBv`, one page per channel, and this page owns only what is true of `venue/venue-dashboard/`.
Its shape follows QBv1@paper, the MISQ desk page on the paper board, with the desk voice adapted from a journal to a channel.

**Why this venue matters**: in the schema's stage table only dashboard and report fire all six stages at the full bar, so pinning this venue is the largest commitment an intervention can make, and the pack's thinness is a cost worth recording before anyone pins it.

**What the pack cannot answer**: an exemplars folder, audience tone rows, a section list for section-edit, and a data-contract shape.
The first three are schema demands and the fourth the pack raises itself; each is a GAP row in §4, never a guess.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from the board**: the page grammar, the section order, and the sentence rules come from `haipipe-board/ref/page-template.md` and `ref/writing-rules.md` and are not restated here.

**Say what the channel refuses, not what it prefers**: a preference does not gate a spec.

✅ `a KPI card missing current, trend, target is refused`  ❌ `dashboards value clarity`

**A pack fact carries its file**: every rule on this page names `README.md`, `style-profile.md`, or `_SCHEMA.md` inline, and what no file says is a GAP row, never a guess.

## Diagram

**The heaviest venue in the pack**: every stage fires, and every number must be earned.

```text
  🚦 GATES    seed · pitch · claims · narrative · display · section-edit
              all six required · claims_settlement: full
              [venue-dashboard/README.md stages block]

  🏆 REWARDS  drill-down arc   L1 summary KPIs → L2 detail → L3 actions
              display map      metric-card · line-chart · bar-chart ·
                               table · action-list
              per unit         type · claim · Job · C-id · data source

  ❌ REFUSES  a panel without a claim and a data source
              a KPI card missing current · trend · target
              a metric with no evidence that it matters
              an unspecified drill-down path · no refresh cadence

  🕳 GAPS     exemplars/ · audience tone rows · section list ·
              data-contract shape

  📊 2 files on disk · README.md 58 lines · style-profile.md 41 lines
```

## Content

### 1 · What the channel gates: all six stages, and a full settlement bar

**Nothing is skipped**: the stage row only report shares exactly.

```text
  🚦 STAGES     seed req · pitch req · claims req ·
                narrative req · display req · section-edit req
                [venue-dashboard/README.md stages block]

  ⚖️ BAR        claims_settlement: full
                primary claims supported by JUDGED answers ·
                load-bearing GAPs settled   [_SCHEMA.md]

  👥 ROW MATES  venue-report all req, full ·
                venue-ui-card the same except section-edit optional
                [_SCHEMA.md stage summary]
```

🚦 Establishes the gate: pinning venue-dashboard fires every lifecycle stage and sets the claims CHECK gate to full, the schema's highest bar.

The stages block in `venue-dashboard/README.md` marks all six lifecycle stages required, so at pin time the STATUS.md `stages_skipped` row is written empty [_SCHEMA.md, stage requirements block].
The settlement bar is full: primary claims supported by judged answers, and load-bearing GAPs settled before artifact work [_SCHEMA.md, claims settlement].
The README says why in one sentence: "you can't show a metric on a dashboard without evidence that the metric matters" [venue-dashboard/README.md, Claims mapping].
A GAP in the claims ledger therefore triggers a probe plan rather than a caveat, which is the whole difference between this bar and medium.
In the schema's summary table only venue-report shares this row exactly, and venue-ui-card matches it except that section-edit is optional [_SCHEMA.md, stage requirements summary].

#### 1.1 · Why full, in the channel's own terms
(the number faces the reader live, so a caveat has nowhere to hang)
An SMS or an email can soften a weak claim inside a sentence.
A KPI card shows a current value, a trend, and a target, and nothing else [style-profile.md, drafting rule 4], so a claim behind a card is either settled or the card is wrong in front of a provider.
That is why the bar is full here while the prose channels run light or medium [_SCHEMA.md, available venues].

### 2 · What the channel rewards: a drill-down arc rendered as a display map

**Three levels, five widget types, five fields per unit**: the reward structure of the channel.

```text
  🪜 ARC       L1 summary KPIs     the headline answer
               L2 detail panels    the supporting evidence
               L3 action items     what to do about it
               [README.md → Narrative]

  🧩 TYPES     metric-card · line-chart · bar-chart · table · action-list

  🏷 PER UNIT  type · claim · Job ("show current vs target") ·
               evidence anchor C-id · data source (task or endpoint)
               [README.md → Display]

  ✍️ COPY      panel titles · KPI labels · action-list phrasing ·
               drill-down captions   [README.md → Section-edit]

  📤 DRAFT     dashboard spec: panel layouts · widget specs ·
               data bindings · interaction rules   [README.md → Draft]
```

🏆 Establishes what a dashboard intervention actually produces: not prose but a spec whose every unit carries its claim, its job, and its data source.

The narrative stage fires here, but its arc is spatial rather than rhetorical: level 1 answers the headline question in summary KPIs, level 2 backs it with detail panels, level 3 says what to do about it [README.md, Narrative mapping].
The display stage writes the display map: each panel or widget gets a type, a claim, a per-unit Job such as "show current vs target", an evidence anchor (C-id), and a data source, a task or an endpoint [README.md, Display mapping].
The per-unit Job is the absorbed minimap concern, in the README's own words.
Section-edit settles the copy to final wording: panel titles, KPI labels, action-list phrasing, drill-down captions [README.md, Section-edit mapping].
Draft produces a dashboard spec document with panel layouts, widget specs, data bindings, and interaction rules, written by haipipe-application-artifact reading this profile, and a wireframe render goes through /haipipe-task when one is needed [README.md, Draft mapping].

#### 2.1 · The voice example is a wireframe, not prose
(the one exemplar the pack carries is embedded in its style profile)
The style profile's only voice example is a three-card KPI row drawn in ASCII: each card shows a current value, a trend arrow with its delta, and a target or threshold, and beneath each card sit its claim id and its source task [style-profile.md, voice example].
That single figure is doing the work an exemplars folder would do, and §4 records the folder's absence as GAP-1.
The drafting rules generalize it: an ASCII wireframe for every panel with a dimensions hint, interaction notes naming drill-down targets and filter scope, and axis labels, legend, and data granularity for every chart [style-profile.md, drafting rules].

### 3 · What refuses a dashboard: the self-review checklist is the desk

**Five checkbox rows plus one upstream rule**: each is a rejection, not a preference.

```text
  ❌ REFUSED ON SIGHT   [style-profile.md checklist · README.md → Claims]
     a panel with no claim or no data source
     a KPI card missing current · trend · target
     a drill-down with no specified path
     a panel with no refresh cadence
     a spec with no adopted_A / declined_A frontmatter
     a metric with no evidence that the metric matters
```

❌ Establishes the refusal list: this channel has no editor, so it publishes its rejection reasons as five checkboxes, and the sixth refusal fires upstream at the claims gate.

The desk is the self-review checklist at the bottom of the style profile: every panel has a claim and a data source, every KPI card has current, trend, and target, drill-down paths are specified, refresh cadence is noted, and the frontmatter carries `adopted_A` and `declined_A`, the advice entries the artifact adopted and declined [style-profile.md, self-review checklist].
The sixth refusal never reaches the spec at all: a metric with no evidence that it matters is stopped at the claims gate, because the full bar turns that missing evidence into a probe plan instead of a caveat [README.md, Claims mapping].
What the checklist cannot catch is a dashboard that passes every row and still answers no question its provider has; that failure belongs to seed and claims, which are venue-free and already exist before this venue is pinned [_SCHEMA.md, stage requirements block].

### 4 · What the pack cannot answer: four GAP rows

**Three schema demands and one self-raised**: recorded here instead of invented.

```text
  🕳 GAP-1  exemplars/           demanded by the _SCHEMA.md pack shape ·
                                 absent on disk
  🕳 GAP-2  audience tone rows   _SCHEMA.md: those rows ARE the audience
                                 axis · style-profile.md has none
  🕳 GAP-3  section list         _SCHEMA.md → Section-edit demands a list
                                 plus per-section jobs · README.md names
                                 copy surfaces only
  🕳 GAP-4  data-contract shape  the pack demands a source and a cadence
                                 per panel · nothing says what carries them
```

🕳 Establishes the pack's debts: what a pinned dashboard intervention will find missing, written down so nobody finds it mid-stage.

GAP-1: the schema's uniform pack shape carries an `exemplars/` folder of real artifacts to pattern-match, and venue-dashboard has none; the folder on disk holds exactly `README.md` and `style-profile.md` [_SCHEMA.md, pack shape].
GAP-2: the schema says the style profile's tone-by-audience rows ARE the audience axis, and this style profile has no such rows; the README names the audience as "typically clinician/provider or executive" and nothing says how a dashboard sounds to either [_SCHEMA.md, audience; venue-dashboard/README.md, constraints].
GAP-3: the schema's section-edit mapping demands a section list with per-section jobs for a sectioned venue; the README names four copy surfaces and its narrative arc implies three levels, but no section list is declared anywhere [_SCHEMA.md, lifecycle mappings; README.md, Section-edit mapping].
GAP-4: the pack demands real-time or near-real-time refresh, a data source per panel, and data bindings in the spec, yet neither file says what shape that data contract takes or where it lives [README.md, constraints and Draft mapping; style-profile.md, drafting rule 2].
None of these is filled on this page: each waits on the Decision Now row in States, which puts the fill timing to JL.

## Aims

### Decision Now
- [ ] 🗣 When do the pack's four GAPs get filled?
      📍 `Part` §4
      🔔 `Why now` this page records the debts, and the first pinned dashboard intervention inherits whichever remain
      ⭐ `A ·` fill on first pin: the first intervention that pins venue-dashboard writes the exemplar, the tone rows, the section list, and the data-contract shape from its own artifact, so the pack grows from real work at the cost of that team paying mid-lifecycle; recommended because a GAP filled from a real artifact beats one invented ahead of it
      `B ·` fill now: write all four into the pack from the schema and the style profile's one wireframe, so the first pin lands on a complete pack at the cost of four documents written with no real dashboard behind them
      🛑 `Blocks` nothing this page can see; the pack's two files name no pinned intervention
      🤖 `If nobody answers` A takes effect


### A1 · 🚦 What the channel gates
- ⬜ A1.1 · The full settlement bar is applied by the claims CHECK gate rather than remembered.
  **Done when:** a dashboard intervention's claims gate names the judged answer behind every load-bearing claim before artifact work starts.
  **Now:** Not started. The bar is declared in the README and defined in the schema, and this page has seen no dashboard run apply it.


### A2 · 🏆 What the channel rewards
- ⬜ A2.1 · Every display-map unit carries its five fields.
  **Done when:** a dashboard display map has no unit missing type, claim, Job, C-id, or data source.
  **Now:** Not started. The five fields are listed in the README's Display mapping, and the pack's only worked example carries two of them (claim, source) per card.


### A3 · ❌ What refuses a dashboard
- ⬜ A3.1 · The self-review checklist runs as a gate, not as decoration in the spec.
  **Done when:** a dashboard spec draft records a verdict per checklist row instead of shipping unticked boxes.
  **Now:** Not started. The checklist exists as five unticked boxes in `style-profile.md` and nothing runs it.


### A4 · 🕳 What the pack cannot answer
- 🧠 A4.1 · Each GAP row is filled in the pack or explicitly declined.
  **Done when:** every GAP row in §4 points at a pack file that answers it, or at the dated ruling that declined it.
  **Now:** Waiting on the Decision Now row above; until it is answered the four GAPs stay recorded and unfilled.


## Files

- `../../../../application/venue/venue-dashboard/README.md`
  The hub: the constraints, the stages block, the full settlement bar, and the five lifecycle mappings; change what the channel gates here.
- `../../../../application/venue/venue-dashboard/style-profile.md`
  The voice wireframe, the five drafting rules, and the checklist that is this channel's desk; change what refuses a spec here.
- `../../../../application/venue/_SCHEMA.md`
  The uniform pack shape every venue obeys, the settlement-bar definitions, and the stage summary row this page reads against; a GAP in §4 is measured against this file.

## Glossary

- 🏷 **Per-unit Job**: the one line a display unit owes, such as "show current vs target"; the README calls it the absorbed minimap concern.
- ⚖️ **Settlement bar**: how much of the claims campaign must settle before artifact work, on the schema's light, medium, full scale; this venue sits at full.
- 📌 **Pin**: haipipe-application-venue writing one venue into an intervention's STATUS.md, after which every downstream stage reads this pack by path.

## Log

260802 · Opened with the QBv venue-pack pages, from `venue/venue-dashboard/` at two files (README.md, style-profile.md). The stages block, the full bar, the drill-down arc, the display map, and the checklist were recorded from the pack against `_SCHEMA.md`, and four unanswered demands were recorded as GAP rows in §4 with the fill timing put to JL in Decision Now. Shape adapted from QBv1@paper.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0