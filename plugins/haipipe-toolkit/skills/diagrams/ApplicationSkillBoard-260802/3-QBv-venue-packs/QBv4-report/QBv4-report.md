# Report: the venue closest to a paper, without a journal desk

state: 🔴 OPEN
owner: JL
method: state what the pack gates, rewards, and requires in its own numbers, and record what it lacks as GAP items for JL to rule on

## Opening

What does the report venue pack know: what does this channel gate, reward, and require of narrative, sections, and settlement?
A venue pack is the knowledge a pinned venue hands every downstream stage; `venue-report/` holds it for the formal stakeholder report.
Report fires all six lifecycle stages at full claim settlement, a profile only dashboard shares.
It has no journal desk: the reader is the desk, and this page names what that reader bounces.

**A venue pack**: knowledge, not a skill; it is consulted by path after `haipipe-application-venue` pins one venue in STATUS.md, and every downstream stage reads the pinned pack [_SCHEMA.md].
On disk this pack is two files, `README.md` and `style-profile.md`.

**Where this page sits**: it is one venue target in `QBv`, one page per channel; this page owns only what is true of `application/venue/venue-report/`, and the other seven channels in `_SCHEMA.md`'s table belong to their own pages.

**The shape it adapts**: QBv1@paper wrote the first page of this kind for MISQ's desk; this page keeps that voice and swaps the journal desk for the stakeholder who accepts or bounces the report.

**Why this venue matters**: the reader is often an exec or a clinical stakeholder deciding whether to fund or ship, so a report that reads as a descriptive dashboard instead of a business case loses the decision it was written to win.

**What the pack cannot answer**: two holes, recorded in §5 and put to JL in States › Decision Now rather than patched with plausible prose.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited**: the page grammar, the section order, and the sentence rules come from the board's page contract (`haipipe-board-page` and `page-template.md`) and are not restated here.

**A number may be stated, but never claimed**: a word cap or a section count appears only with its source named inline (a `README.md` or `style-profile.md` block), and never as this page's own claim.

**Say what fails the report, not what it prefers**: a preference does not bounce a draft.

✅ `an uncited factual statement fails the self-review`  ❌ `reports value citations`

**A hole is recorded, never filled**: where the schema demands an answer the pack lacks, this page writes a GAP item and a Decision Now row instead of inventing the answer.

## Diagram

**The report pack at a glance**: what it gates, who it is for, and where it is thin.

```text
  📋 THE PACK    venue-report/ ── README.md + style-profile.md · no exemplars/
  🚦 GATES       all six stages required · claims_settlement: full
  🏛 AUDIENCES   regulator · executive · partner ── arc, citations, cap per reader
  🧱 SECTIONS    01-subgroup-profile → 02-exploration → 03-findings
                 → 04-messages → 05-performance → 06-gate-check
  ❌ BOUNCES     uncited statement · contested K/W as settled · no captioned
                 display on a data claim · over the audience cap
  🕳 GAPS        exemplars/ absent · the two length tables disagree
```

## Content

### 1 · What the channel gates, and what it pays back

**Every stage fires, and the claims bar is full**: the price of this channel, and the room it buys.

```text
  🚦 STAGES     seed · pitch · claims · narrative · display · section-edit
                ── all six required, no skip row   [README.md]
  ⚖️ BAR        claims_settlement: full ── judged answers ·
                load-bearing GAPs settled   [_SCHEMA.md]
  👯 PEERS      venue-dashboard ── the only other skip-free, full-bar profile
  🎁 PAYBACK    sections · tables · figures · KPI callouts · full citations
```

🚦 Establishes the price of this channel as the full settlement bar, and its payback as room the light channels do not have.

The stages block requires all six lifecycle stages, the only skip-free profile in the family beside venue-dashboard [venue-report/README.md, Stage requirements; _SCHEMA.md, Stage requirements summary].
`claims_settlement: full` sets the bar the claims CHECK gate applies before artifact work: primary claims supported by judged answers, and load-bearing GAPs settled [_SCHEMA.md, Claims settlement].
The README restates it for this venue: every finding and recommendation must trace to a supported claim, and GAPs trigger probes [venue-report/README.md, Claims mapping].
What the channel pays back for that price is room: narrative, display, and section-edit all fire, so a report carries the tables, figures, KPI callouts, and citations that a light channel has no slot for [README.md, Constraints and Display mapping].
An SMS leans on one claim at the light bar; a report leans on the whole ledger [_SCHEMA.md, Available venues].

#### 1.1 · What full costs relative to medium
(the one word in the stages block that resizes the evidence campaign)
At medium, a load-bearing GAP may ride into drafting with an open campaign row; at full it must be settled first [_SCHEMA.md, Claims settlement].
Pinning report therefore converts every load-bearing GAP in the 1c ledger from a to-do into a blocker, and the evidence campaign is sized to that at pin time.

### 2 · The audience decides the arc, the citations, and the length

**One venue, three readers**: the same pack drafts three different documents.

```text
  🏛 REGULATOR   methodology → findings → limitations → recommendations
                 footnotes · ≤ 1,500 words · formal, comprehensive
  💼 EXECUTIVE   bottom line → evidence → ask
                 endnotes · ≤ 600 words · direct, outcome-oriented
  🤝 PARTNER     context → joint findings → next steps
                 inline citations · ≤ 800 words · collaborative tone
  📏 README      600-2,000 words, audience-dependent ── disagrees, see §5
```

🏛 Establishes the audience as the axis that rewrites the report: three arcs, three citation forms, three caps, one pack.

Venue and audience are orthogonal but coupled, and both live in this pack: the venue fixes what the output looks like, the audience fixes how it sounds [_SCHEMA.md, Audience].
The narrative arc is chosen by reader: methodology-first for a regulator, bottom-line-first for an executive, context-first for a partner [venue-report/README.md, Narrative mapping; style-profile.md, drafting rule 1].
Every factual statement cites a K/W entry, and the citation form tracks the audience: footnotes for a regulator, endnotes for an executive, inline parentheticals for a partner [style-profile.md, drafting rule 2].
The caps are per audience: regulator at or under 1,500 words, executive 600, partner 800 [style-profile.md, drafting rule 5].
A limitations section is mandatory for the regulator, and only for the regulator [style-profile.md, drafting rule 4].

#### 2.1 · The executive report is a business case
(gap → lever → credibility → ask, compressed to three beats)
The executive arc is bottom line → evidence → ask [venue-report/README.md, Narrative mapping].
The section spine in §3 originated in the C-group report work [README.md, Section-edit mapping], where a report argues an investment case: the gap, the lever the intervention pulls, the credibility behind it, and the ask.
The pack's stored executive voice example runs that case in four sentences: it opens on the effect with its interval, prices the annual impact, closes on a dated expansion ask, and parenthesizes the claim ids it leans on [style-profile.md, Voice examples].
The arc has no methodology beat; at 600 words the method's credibility rides in the cited claims, not in the body.

#### 2.2 · The regulator report is the strictest, and the spine does not fit it as-is
(the one audience whose arc demands a section the default spine lacks)
The regulator footnote carries the whole evidence chain in one line: the claim id and its statement, the probe it rests on, the sample size, and the cohort window [style-profile.md, Voice examples].
The regulator arc demands a limitations section, and the default six-section spine names no slot for one; the nearest is `06-gate-check`, whose job is settlement and caveats before shipping rather than a reader-facing limitations statement.
So audience=regulator is the case the README's "adjust per intervention in 3-narrative" exists for [venue-report/README.md, Section-edit mapping].

### 3 · Sections and displays: a DIKW spine, edited one section at a time

**The sectioned venue**: the same section-by-section machinery a paper runs, on a spine the intervention may reshape.

```text
  🧱 SPINE      01-subgroup-profile  who the cohort is        D
                02-exploration       what was tried           D/I
                03-findings          what the evidence shows  I/K
                04-messages          what we recommend        K/W
                05-performance       how it performed         I/K
                06-gate-check        settlement + caveats     gate
  🖼 DISPLAYS   tables: summary stats · comparisons ── figures: forest
                plots · trend charts ── KPI callouts
  ✍️ EDIT UNIT  per-section DPRC · paragraph jobs in each section's outline
  📦 ASSEMBLY   0-sections/ → haipipe-application-artifact → full citations
```

🧱 Establishes the report as the venue where section-edit earns its keep, walking the DIKW ladder in reader order.

"This is the venue closest to an academic paper" is the README's own sentence, and section-edit is where it earns it: per-section DPRC on the declared sections, with paragraph-level job assignments in each section's outline [venue-report/README.md, Section-edit mapping].
The default spine walks the DIKW ladder in reader order: cohort (D), exploration (D/I), findings (I/K), messages (K/W), performance (I/K), then a gate-check before shipping [README.md, sections block].
It is a default and not a contract: the README says adjust per intervention in 3-narrative, and §2.2 names the audience that forces the adjustment.
Tables and figures with captions are a constraint, not a nicety, and the display map names summary-stat and comparison tables, forest plots, trend charts, and KPI callouts [README.md, Constraints and Display mapping].
The draft is assembled from `0-sections/` by `haipipe-application-artifact`, following the narrative arc, with full citations [README.md, Draft mapping].

### 4 · What bounces a report

**No journal desk, but a desk all the same**: the refusals are written in the pack's own self-review checklist.

```text
  ❌ BOUNCED AT SELF-REVIEW   [style-profile.md, checklist]
     an uncited factual statement
     a contested or superseded K/W cited as settled
     a data claim with no captioned table or figure
     over the audience's word budget
     a regulator report with no limitations section
     structure off the audience template
     missing adopted_A / declined_A frontmatter
  🚧 BOUNCED BEFORE DRAFTING
     an unsettled load-bearing GAP ── the full bar of §1
```

❌ Establishes the reader as this venue's desk: the checklist is what they would refuse, run before they see it.

A paper venue names desk-reject signals; this pack encodes them as a self-review checklist a draft runs before its gate [style-profile.md, Self-review checklist].
The heaviest row is evidential: no contested or superseded K/W cited as settled evidence, which is the sentence-level face of §1's full settlement bar.
An uncited factual statement fails outright, since every one must cite a K/W entry in the audience's format [style-profile.md, drafting rule 2].
The `adopted_A / declined_A` frontmatter row ties the artifact back to 1d-advice: a report declares which advice entries it adopted and which it declined, so a declined entry stays visible instead of silently vanishing [style-profile.md, checklist].
And upstream of all of it, the claims gate bounces the draft before it exists when a load-bearing GAP is unsettled [_SCHEMA.md, Claims settlement].

### 5 · What the pack lacks, and where it contradicts itself

**Two recorded holes, neither filled here**: the schema is the ruler, and inventing the missing answers is the one thing this page refuses to do.

```text
  🕳 GAP-1   exemplars/ ── demanded by _SCHEMA.md, absent on disk
             → Draft's "style from exemplars/" has nothing to read
  🕳 GAP-2   the length tables disagree
             README   600-2,000 words, audience-dependent
             style    regulator ≤ 1,500 · executive ≤ 600 · partner ≤ 800
             ── no audience row reaches 2,000
  🗣 BOTH    put to JL in States › Decision Now
```

🕳 Establishes what a consumer of this pack must not trust yet, and routes both holes to a human.

The schema declares every venue profile a uniform pack of three parts: `README.md`, `style-profile.md`, and `exemplars/` holding real artifacts to pattern-match [_SCHEMA.md, opening block].
On disk `venue-report/` is two files with no `exemplars/` folder, so the Draft mapping's "format constraints + style from exemplars/" resolves to nothing for this venue [directory listing 260802; _SCHEMA.md, Lifecycle mappings].
The two length tables disagree: the README constraint says 600 to 2,000 words, audience-dependent, while the style profile caps every audience at or under 1,500 [venue-report/README.md, Constraints; style-profile.md, drafting rule 5].
No audience row reaches 2,000, and the executive cap of 600 sits at the README's floor, so which table binds a drafting gate is a real ruling and not a typo fix.
Both holes go to JL as Decision Now rows, and this page holds them open.

## Aims

### A1 · 🚦 What the channel gates, and what it pays back
- A1.1 · The full settlement bar is applied by the claims gate before report artifact work, rather than recalled by a human.
  **Done when:** a report round shows the gate refusing a draft over an unsettled load-bearing GAP, or passing one with the judged answers named.

### A2 · 🏛 The audience decides the arc, the citations, and the length
- A2.1 · The audience is pinned beside the venue before narrative work, since it decides the arc, the citation form, and the cap.
  **Done when:** a report intervention's STATUS.md records the audience with the venue pin, and its 3-narrative names the matching arc.

### A3 · 🧱 Sections and displays: a DIKW spine, edited one section at a time
- A3.1 · The spine is adjusted per intervention instead of copied, with the regulator case handled.
  **Done when:** a regulator-audience report shows a limitations section in its declared sections, or records why the default spine stood.

### A4 · ❌ What bounces a report
- A4.1 · The self-review checklist runs as a check with verdicts, not as advice.
  **Done when:** a report draft carries the checklist with each row's verdict, before its gate.

### A5 · 🕳 What the pack lacks, and where it contradicts itself
- A5.1 · `exemplars/` exists and the Draft mapping's "style from exemplars/" has something to read.
  **Done when:** the folder holds at least one real report artifact and the README names it.
- A5.2 · One length table binds.
  **Done when:** `README.md` and `style-profile.md` state the same per-audience caps, or one names the other as authoritative.

## States

### Decision Now

- [ ] 🗣 Where do report exemplars come from, or does this venue get a pass on the schema's `exemplars/`?
      📍 `Part` §5 · GAP-1
      🔔 `Why now` `_SCHEMA.md` makes `exemplars/` part of every uniform pack, and this pack's own Draft mapping reads style from a folder that does not exist.
      ⭐ `A ·` harvest real C-group reports into `exemplars/`, filling the folder with the artifacts the section spine came from; CC recommends A because the spine's origin is the closest thing to a house exemplar this venue has.
      `B ·` write one synthetic exemplar report, which fills the slot fast but pattern-matches prose nobody shipped.
      `C ·` amend `_SCHEMA.md` to mark `exemplars/` optional for report, which makes the disk honest and the pack thinner.
      🛑 `Blocks` A5.1
      🤖 `If nobody answers` nothing is added: the gap stays recorded here and A5.1 stays waiting.

- [ ] 🗣 Which length table binds a report draft, the README's range or the style profile's per-audience caps?
      📍 `Part` §5 · GAP-2
      🔔 `Why now` the two tables disagree today, and a drafting gate cannot apply both: a 2,000-word report passes one table and fails every row of the other.
      ⭐ `A ·` the per-audience caps bind and the README range becomes descriptive; CC recommends A because a per-audience cap is what the self-review checklist actually runs.
      `B ·` the README range binds and the caps become suggestions, which frees long reports and blunts the checklist's length row.
      🛑 `Blocks` A5.2
      🤖 `If nobody answers` drafts follow the stricter table, since a draft under the caps satisfies both.

### A1 · 🚦 What the channel gates, and what it pays back
- ⬜ A1.1 · Not started. The bar is prose in `_SCHEMA.md` and this page cites no run of the claims gate applying it.

### A2 · 🏛 The audience decides the arc, the citations, and the length
- ⬜ A2.1 · Not started. The pairing block couples tone to audience, and no pin recording an audience is cited here.

### A3 · 🧱 Sections and displays: a DIKW spine, edited one section at a time
- ⬜ A3.1 · Not started. The README says adjust per intervention, and no adjusted spine is cited here.

### A4 · ❌ What bounces a report
- ⬜ A4.1 · Not started. The checklist is a fenced block in `style-profile.md` and nothing runs it as a check.

### A5 · 🕳 What the pack lacks, and where it contradicts itself
- 🧠 A5.1 · Waiting on the first Decision Now row: the source of exemplars is JL's call.
- 🧠 A5.2 · Waiting on the second Decision Now row: which length table binds is JL's call.

## Files

- `../../application/venue/venue-report/README.md`
  The hub: the stage gates, the constraints, the six-section spine, and the lifecycle mappings; edit here when the venue's demands change.
- `../../application/venue/venue-report/style-profile.md`
  The voice examples, the per-audience drafting rules, and the self-review checklist; edit here when an audience row changes.
- `../../application/venue/_SCHEMA.md`
  What every pack must declare and the settlement ladder; the ruler §5's gaps are measured against.

## Glossary

- 📦 **Venue pack**: the knowledge folder (`README.md`, `style-profile.md`, `exemplars/`) a pinned venue hands every downstream stage; consulted by path, never invoked as a skill.
- ⚖️ **Settlement bar**: the depth the claims gate demands before artifact work, one of light, medium, or full, set per venue by `claims_settlement:`.
- 🧠 **K/W entry**: an evidence cell at the knowledge or wisdom rung of the intervention's D-I-K-W ladder; a report's factual sentences cite these.

## Log

260802 · Opened from `application/venue/venue-report/` (two files on disk) read against `venue/_SCHEMA.md`, adapting the outlet-page shape of QBv1@paper with the journal desk swapped for the stakeholder reader; two holes recorded (no `exemplars/`, disagreeing length tables) and both put to JL as Decision Now rows.
