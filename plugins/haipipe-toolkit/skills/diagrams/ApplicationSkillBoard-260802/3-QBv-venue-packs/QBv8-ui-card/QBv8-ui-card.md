# ui-card: the venue embedded in someone else's screen

state: 🔴 OPEN
owner: JL
method: state what the ui-card pack gates, rewards, and refuses, and record what it cannot answer as GAP items for JL to rule on

## Opening
A ui-card is the one venue in this tree that never owns its screen: a focused, interactive element embedded in an existing app, such as a refill alert inside a patient portal.
The pack fires every lifecycle stage and sets the claims bar to full, the schema's strictest level.
Yet its rules stop at the card's own border; the host outside it is never named.
So what does this channel gate, reward, and refuse, and what does the pack still not know?

**Where this page sits**: it is one venue target in `QBv-venue-packs`, one page per venue pack, and it owns only what is true of `venue/venue-ui-card/`.
Its nearest confusable sibling is the dashboard pack's page: a dashboard is the standalone data-rich surface a clinician navigates to, while a ui-card interrupts a screen its reader already had open.

**Why this venue matters to this repo**: the pack's own two voice examples are a patient refill alert and a clinician panel-risk card, so the pack is already written in this repo's clinical vocabulary.

**What the pack cannot answer**: three GAPs and one internal clash, listed in §5; the first two wait on the Decision Now rows in States.

## Writing Style
How this page must be written; read it before editing, and edit to it.

**Inherited from the board grammar**: the section order and the sentence rules come from the board's page template and are not restated here.

**Say what the channel refuses, not what it prefers**: a preference does not fail a card, a checklist line does.

✅ `core content behind a scroll is not a ui-card`  ❌ `ui-cards value brevity`

**Every rule carries its file**: a constraint is cited to `README.md` or `style-profile.md` inline, because the two files disagree at least once (§5.4) and an uncited rule cannot be traced to either.

**A GAP is recorded, never filled**: when `_SCHEMA.md` demands what the pack lacks, this page names the absence and routes the ruling to `### Decision Now`, and it never writes the missing answer itself.

## Diagram

**The pack at a glance**: what the channel gates, rewards, refuses, and cannot answer.

```text
  🖥 SURFACE   one screen in a host app · tap, dismiss, act · refreshed on data change

  🚦 GATES     seed → claims → pitch → narrative → display · section-edit optional
  ⚖️ BAR       claims_settlement: full · every UI element ── one claim

  🏆 REWARDS   header hook → body evidence → one specific action
  ❌ REFUSES   scrolling core content · a third button · "Learn More" ·
               a live number with no data source · a standalone screen

  🕳 GAPS      exemplars/ absent · host unnamed · compliance unrecorded
  ⚡ CLASH     wireframe: README "may include" ── style-profile "required"
```

## Content

### 1 · What the channel gates: every stage fires, and the claims bar is full

**The ui-card row of the schema table**: which stages fire and how deep claims must settle.

```text
  🚦 STAGES   seed ✅ · claims ✅ · pitch ✅ · narrative ✅ · display ✅ ·
              section-edit 🔀 optional
  ⚖️ BAR      claims_settlement: full
  🔗 TRACE    every UI element ── one claim in the ledger
  🏋️ PEERS    only dashboard and report also carry the full bar
```

📌 Establishes ui-card as one of the schema's three heaviest venues: the card is small, and the evidence bill behind it is not.

Only three of the eight venues demand the full bar, and ui-card is one of them beside dashboard and report [`_SCHEMA.md`, stage requirements summary].
Full means primary claims supported by judged answers, with load-bearing GAPs settled before artifact work [`_SCHEMA.md`, claims settlement].
The pack's own claims mapping is one line and it is the strictest trace rule in this tree: each UI element must trace to a claim [`venue-ui-card/README.md`, → Claims].
Narrative is required and hierarchical: the header carries the hook or alert, the body the detail or evidence, the action the what-to-do [`venue-ui-card/README.md`, → Narrative].
Display is required and produces the widget map: header type, body elements (gauge, list, chart), action button, and data sources, with one Job sentence per widget on a multi-widget card [`venue-ui-card/README.md`, → Display].
Section-edit is the only stage the venue lets go: a multi-widget card gets a per-widget review pass, and a simple header-plus-body-plus-button card skips it [`venue-ui-card/README.md`, → Section-edit].
The schema's venue template block does not apply here, because it replaces the stages a venue skips, and this venue skips none of narrative, display, or section-edit [`_SCHEMA.md`, venue template].

### 2 · What the channel requires: the physical contract

**Seven rules before the message is judged**: every one checkable on the ASCII wireframe.

```text
  📏 SIZE         one screen · no scroll for core content
  🧭 HIERARCHY    header hook → body detail → action CTA
  🔘 BUTTONS      max 2 · primary left · secondary right
  👆 INTERACTION  tap or click for detail · dismiss · act
  🔌 DATA         every live element ── a named data source
  🔄 UPDATE       persistent · refreshed on data change
  🏠 CONTEXT      embedded in an existing app · never standalone
```

📌 Establishes the contract as physics, not style: a card that breaks any row here fails before anyone reads its words.

Four of the rows are the README's constraints block verbatim: size, interaction, context, and update [`venue-ui-card/README.md`, constraints].
The other three are drafting rules: the header-body-action hierarchy, the two-button ceiling with primary on the left, and the live-data rule that every number or list names its source [`style-profile.md`, drafting rules 2-4].
Rule 5 adds that production rendering comes later, so the draft artifact is a spec plus a wireframe rather than a rendered component [`style-profile.md`, drafting rule 5].
The wireframe itself is the one rule the pack states twice and differently, which §5.4 records as the pack's internal clash.

### 3 · Who reads the card: four audiences, one skeleton

**Venue fixes structure, audience fixes voice**: the pairing table, whole.

```text
  🧑 patient      warm · simple · large tap targets
  🧑‍⚕️ clinician    data-dense · inline C-id · actionable
  🎨 designer     annotated wireframe · component names
  💻 dev          interface spec · data binding · events
```

📌 Establishes that one card is four artifacts depending on its reader, while the header-body-action skeleton never moves.

The schema folds the audience axis into the pack itself: the venue decides what the output looks like, the audience decides how it sounds, and there is no separate audience directory [`_SCHEMA.md`, audience].
The pack demonstrates the two ends it cares most about: a patient-facing alert card that explains one refill in plain words behind two buttons, and a clinician-facing insight card whose body is live counts and a patient list [`style-profile.md`, voice examples].
The clinician row cites its claim inline by C-id, as the insight card does, which is the visible end of the element-to-claim trace §1 demands [`style-profile.md`, audience pairing and voice examples].
The designer and dev rows read the spec rather than the card: they receive the annotated wireframe with component names, or the interface spec with data binding and events [`style-profile.md`, audience pairing].

### 4 · What desk-rejects a ui-card

**Every refusal is a line in the pack**: six checklist checks plus two constraint edges.

```text
  ❌ core content behind a scroll         checklist 1 · constraint size
  ❌ a header that grabs nothing          checklist 2
  ❌ a body too thin to act on            checklist 3
  ❌ "Learn More" as the CTA              checklist 4 · the one named string
  ❌ a live element with no data source   checklist 5 · drafting rule 4
  ❌ missing adopted_A / declined_A       checklist 6
  ❌ a third action button                drafting rule 3
  ❌ a card built as its own screen       constraint context
```

📌 Establishes the desk-reject list as eight named checks, all of them testable on the wireframe before production rendering exists.

The pack names exactly one forbidden string, and it is a CTA: "Learn More" is the checklist's own example of an action that is not specific [`style-profile.md`, self-review checklist].
The frontmatter check refuses a card on provenance rather than content: a card that never records which 1d-advice entries it adopted or declined fails review whatever its message says [`style-profile.md`, checklist line 6].
The refusals come from two files but read as one voice: the README's constraints set the card's edges, and the style profile's checklist is what makes each edge a check instead of a taste.
Nothing in either file refuses a card for what the host would refuse it for, and that silence is §5's second and third GAP.

### 5 · What the pack does not know, and where it disagrees with itself

**The GAP ledger**: recorded absences, never filled by invention.

```text
  🕳 GAP-1   exemplars/      demanded by _SCHEMA.md · absent from the pack
  🕳 GAP-2   the host        "an existing app" · never named · no real-estate
                             grant · no component rules · no approval path
  🕳 GAP-3   compliance      no data-handling or host-approval rule recorded
  ⚡ CLASH    the wireframe   README "may include" ── style-profile "required"
```

📌 Establishes what this page refuses to invent: each row is an absence with a route, and the first two wait on the Decision Now rows in States.

#### 5.1 · GAP-1: the exemplars folder the schema promises
(the pack ships two files where the schema draws three parts)
`_SCHEMA.md` draws every venue pack as `README.md`, `style-profile.md`, and `exemplars/`, "real artifacts to pattern-match" [`_SCHEMA.md`, pack shape].
venue-ui-card ships the first two and no `exemplars/` at all, so a draft here pattern-matches two ASCII voice examples and nothing that ever shipped inside a product.
Whether to fill the folder or waive it for this venue is the first Decision Now row.

#### 5.2 · GAP-2: the host that is never named
(the defining constraint points at a product the pack knows nothing about)
The constraint that makes this venue itself is "embedded in an existing app (not standalone)" [`venue-ui-card/README.md`, constraints].
The pack stops there: no host product is named, no real-estate grant is recorded, and no host's component, interaction, or approval rules are carried anywhere.
A draft can therefore satisfy every rule in §2 and still be unplaceable, because the pack's rules end at the card's own border.
Where that host knowledge should live, in this pack or in each intervention's venue pin, is the second Decision Now row.

#### 5.3 · GAP-3: compliance, unrecorded
(nothing says what a clinical host demands of a card full of live patient data)
Neither pack file carries a compliance line, a data-handling rule, or an approval requirement for the live elements a card displays.
The clinician voice example fills its body with per-patient risk counts and a patient list [`style-profile.md`, voice examples], and the pack is silent on what showing that inside a host product requires.
This page records the silence; it does not guess the answer.

#### 5.4 · The clash: one wireframe, two rules
(the pack's two files disagree about the same artifact)
The README's draft mapping says the UI spec "may include an ASCII wireframe" [`venue-ui-card/README.md`, → Draft], while the style profile's drafting rule 5 says the ASCII wireframe is required in draft [`style-profile.md`, drafting rules].
A checker following one file passes what the other fails.
The clash blocks nothing, because a drafter loses nothing by drawing the wireframe either way, so it is recorded here and reconciling the two files is A5.2's target rather than this page's edit.

## Aims

### Decision Now
- [ ] 🗣 Does venue-ui-card get the exemplars/ folder the schema promises?
      📍 `Part 5.1` the GAP it settles
      🔔 `Why now` `_SCHEMA.md` declares exemplars/ in every pack and this pack has none, so drafts pattern-match two ASCII wireframes and nothing real.
      ⭐ `A ·` fill it: collect de-identified or synthetic in-product card artifacts into `exemplars/`, which commits someone to sourcing and scrubbing them; recommended because a full-settlement venue with the thinnest style evidence in the tree is backwards.
      `B ·` waive it: declare the two style-profile wireframes sufficient for this venue and record the exception in `_SCHEMA.md`, which commits the schema to its first per-venue exemption.
      🛑 `Blocks` no current work; the first real ui-card draft that needs a pattern to imitate will hit it.
      🤖 `If nobody answers` B in effect: drafts already run on the style profile alone.
- [ ] 🗣 Where does host-product knowledge live: in this pack, or in each intervention's venue pin?
      📍 `Part 5.2` and `Part 5.3`, the two GAPs it settles
      🔔 `Why now` the venue's defining constraint points at a host, and the pack records nothing about any host: no real estate, no component rules, no compliance, no approval path.
      `A ·` grow the pack a host-constraints section per known host product, which commits the pack to tracking products it does not own.
      ⭐ `B ·` keep the pack host-generic and make the venue pin record the host's rules per intervention, which commits the pin step to one more required field; recommended because hosts change per intervention and the pack should stay knowledge that is true for all of them.
      🛑 `Blocks` any deployment-ready card spec: a draft can pass every pack rule and still not fit its host.
      🤖 `If nobody answers` the pack stays as it is and nobody records the host rules, so the blind spot in §5.2 persists.


### A1 · 🚦 What the channel gates
- ⬜ A1.1 · The stage block and the full bar bind at pin time instead of being recalled.
  **Done when:** an intervention pinned to venue-ui-card shows the stages_skipped row in its STATUS.md and its claims CHECK gate names `claims_settlement: full`.
  **Now:** Not started; the stage block is prose in the pack README, and no pin has been checked against it from this page.


### A2 · 📏 What the channel requires
- ⬜ A2.1 · Every ui-card draft ships the wireframe and names a data source per live element.
  **Done when:** a draft is returned as incomplete without both, citing §2's contract.
  **Now:** Not started; the contract is six checklist lines and five drafting rules in `style-profile.md`, recorded here as §2.


### A3 · 🧑‍⚕️ Who reads the card
- ⬜ A3.1 · The audience row is chosen before the voice is written.
  **Done when:** a card draft states patient, clinician, designer, or dev, and its tone matches that pairing row.
  **Now:** Not started; the pairing table has four rows and nothing on this page shows one being picked.


### A4 · ❌ What desk-rejects a ui-card
- ⬜ A4.1 · The refusal list runs as a review check, not as taste.
  **Done when:** a review pass on a real card cites the checklist or rule line behind every finding.
  **Now:** Not started.


### A5 · 🕳 What the pack does not know
- 🧠 A5.1 · The three GAPs carry rulings instead of silence.
  **Done when:** exemplars/, the host question, and the compliance question each have a JL ruling recorded on this page or a filled pack section behind them.
  **Now:** Waiting on JL; both Decision Now rows above are open.
- ⬜ A5.2 · The wireframe clash is reconciled in the pack.
  **Done when:** `README.md` and `style-profile.md` state the same wireframe rule, and the Log names which file moved.
  **Now:** Not started; §5.4 records the clash and both pack files still disagree.


## Files

- `../../../../application/venue/venue-ui-card/README.md`
  Edit here to change what the channel gates: the constraints, the stage block, the full settlement bar, and the lifecycle mappings.
- `../../../../application/venue/venue-ui-card/style-profile.md`
  Edit here to change how a card sounds: the voice examples, the drafting rules, the audience pairing, and the self-review checklist.
- `../../../../application/venue/_SCHEMA.md`
  The pack contract every venue answers to, and the line that makes GAP-1 a gap.

## Glossary

- 🏠 **Host product**: the existing app a ui-card is embedded in; the pack's whole record of it is the phrase "an existing app (not standalone)".
- 🔖 **C-id**: the claim ledger id a clinician-facing element cites inline; it is the visible end of the element-to-claim trace.
- 📇 **adopted_A / declined_A**: the frontmatter fields recording which 1d-advice entries the card adopted or declined; the self-review checklist fails a card without them.
- 🗞 **Desk-reject**: borrowed from the outlet pages (QBv1@paper); here it means a card the pack's own checklist refuses before any reader weighs its message.

## Log

260802 · Opened from `venue/venue-ui-card/` and `venue/_SCHEMA.md` with the shape adapted from QBv1@paper; recorded three GAPs (exemplars/ absent, host unnamed, compliance unrecorded) and one internal clash (the wireframe rule), and raised two Decision Now rows for JL.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0