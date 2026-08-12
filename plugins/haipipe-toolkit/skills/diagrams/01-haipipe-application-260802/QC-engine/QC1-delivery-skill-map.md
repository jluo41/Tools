# Delivery to Engine: the skill route map
state: 🔴 OPEN
owner: JL
method: crosswalk the nine QB concerns to callable application routes without moving content authority into the Engine

## Opening
Which reusable Application, Probe, and Display routes may produce each Delivery concern QB1 through QB9, and on what authority terms?
A route is the ordered skills a builder calls for one concern, such as claims running its orchestrator plus the probe worker.
One skill family serves all nine concerns, so the map is many-to-many and easy to misread as ownership.
This page fixes the crosswalk and its rule: Delivery owns content, the Engine only maps routes.

**What a route is**: the ordered callable skills that serve one concern, such as QB4's claim ledger running `haipipe-application-claims` with `haipipe-application-probe` as its evidence door.

**Where this page sits**: QB1 through QB9 each own one Delivery concern's content and its human gate; a builder who found a concern there comes here to learn which skills produce it and on what terms.

**Covered elsewhere**: what each concern means and when it is complete stays on QB1 through QB9; the same crosswalk for the paper family lives at QC1@paper, which is this page's precedent and not an authority over application routes.

**Why it matters**: without one map, each stage skill reads as the owner of the concern it serves, and a shared worker like the probe skill would be read a different way on every page.

## Diagram
**The route map's shape**: how a concern reaches its artifact through a route, and where authority stops.

```text
📦 QB concern ── serves ──▶ 🛠 skill route ── writes ──▶ 📂 working surface
   🧑 content + gate stay here    ✍️ authority ends at its Writes

🧱 Board substrate ── carries every box above · owns none of their content
```

## Content
### 1 · 🧭 The direction and the one rule
**Two entry points, one authority**: who enters where, and which way authority flows.

```text
📦 Delivery (QB1…QB9)   owns · concern content · the human gate
⚙️ Engine (this page)   owns · the route map · the card contract
🔁 map                  reversible · a QB names its route, a card names its Serves
🚫 authority            one-directional · no route authors concern content
```
📌 This part fixes which way a reader enters the map and which way authority may never flow.

Delivery is the entry for a reader asking what the intervention needs; the Engine is the entry for a builder asking which skill to call.
The map is reversible: a QB page names its producing route by pointing here, and a Skill card names the concerns it serves.
Authority is not reversible: a concern's content and its completion gate stay on its QB page, and a route that produced a draft still hands the ruling back.
The rule is adopted unchanged from QC1@paper, where JL accepted the Delivery-first, skill-first structure on 260730.

### 2 · 🗺 The concern-to-route crosswalk
**One row per concern**: the path from a QB concern to the surface its route writes.

```text
📦 QB concern ── serves ──▶ 🛠 skill route ── writes ──▶ 📂 working surface
   🧑 gate stays here            ⚙️ authority stops here
```
📌 The table below is the forward crosswalk: nine concerns, their callable routes, and the narrow surface each route may write.

| Concern | Producing route | Working surface it writes | Round-3 engine |
|---|---|---|---|
| QB1 | `haipipe-application-seed` → `haipipe-application-venue` → `haipipe-application-pitch` | `0-lifecycle/0-seed/` · `0-lifecycle/2-venue/2-venue.md` · `0-lifecycle/2-pitch/` | candidate |
| QB2 | `haipipe-application-descriptions` + `haipipe-application-probe` | `0-lifecycle/1a-descriptions/` · `1-probes/PPNN_<topic>/` | rung candidate · probe stays |
| QB3 | `haipipe-application-themes` + `haipipe-application-probe` | `0-lifecycle/1b-themes/` | rung candidate · probe stays |
| QB4 | `haipipe-application-claims` + `haipipe-application-probe` | `0-lifecycle/1c-claims/1c-claims.md` | rung candidate · probe stays |
| QB5 | `haipipe-application-advice` + `haipipe-application-probe` | `0-lifecycle/1d-advice/` | rung candidate · probe stays |
| QB6 | `haipipe-application-display` + the shared `haipipe-display-*` layer | `0-lifecycle/4-display/` | stage candidate · display layer stays |
| QB7 | `haipipe-application-artifact` + `haipipe-application-section-edit` | `0-artifacts/<slug>-v{N}.md` · `0-sections/` | section-edit candidate · artifact stays |
| QB8 | `haipipe-application-review` → `haipipe-application-claim-audit` → `haipipe-application-deploy` | `0-artifacts/REVIEW-*` · `0-artifacts/CLAIM_AUDIT.md` | stays |
| QB9 | `haipipe-application-iterate` + `haipipe-application-round` | `1-rounds/vYYMMDD/` · fresh data backfilled into `0-lifecycle/1a-descriptions/` | stays |

Every skill name comes from the application README's Stage to Procedure and Router Rule maps.
The Writes column is the whole of a route's authority: what lands there is accepted or rejected at the QB page's gate, never by the route.
The probe worker is the only evidence door for every stage's PROBE phase, so its seat on the rung rows marks where evidence is the concern's main product, not an exclusive claim.
One route stays unplaced: `haipipe-application-narrative` (stage 3) serves no single row above, and this page records the gap rather than guessing its owner.
`haipipe-application-enter` is the door to every concern and produces content for none, so it takes no row.

### 3 · 🃏 The six-field skill card
**The card every Skill page fills**: six fields, adopted from QC1@paper.

```text
🃏 SKILL CARD

  🔔 Trigger    what invokes the skill
  🤝 Serves     the QB concerns it works for
  📥 Reads      the files and pages it consumes
  ✍️ Writes     the narrow surface it may touch
  📤 Produces   the observable output it hands off
  🧾 Evidence   the real run that proves the route
```
📌 A Skill page on this board describes itself in these six fields and nothing wider.

Two narrowing rules keep the card honest.
Writes is narrower than Serves: a skill may serve QB4 without owning a line of the claim ledger.
Evidence names a run that actually happened or states that none exists; a card without it claims a route, not a fact.

### 4 · ⚙️ What the round-3 stage engine absorbs
**Candidate against kept**: the marking rule behind the crosswalk's engine column.

```text
⚙️ round-3 stage engine · one shared DRAFT→PROBE→REVISE→CHECK runner

  🍱 candidate   every 1-lifecycle stage orchestrator (rows QB1…QB7)
  🧷 kept        probe worker · deliver verbs · display layer · iterate · round
  🗣 ruling      JL · the Decision Now row on this page
```
📌 The engine column in Part 2 is a marking, not a ruling; this part states the rule behind the marks and who fixes the set.

Every 1-lifecycle stage orchestrator drives the same four phase workers, DRAFT then PROBE then REVISE then CHECK, so those route rows differ only in the surface they write.
That shared loop is what one stage engine could absorb in this board's third work round, which is why the crosswalk marks exactly those rows candidate.
The deliver verbs, the probe worker, the shared display layer, iterate, and round are not stage orchestrators and stay outside the engine whatever the ruling.
Which candidates the engine actually absorbs is JL's ruling, raised in this page's Decision Now; until it is answered a candidate mark commits nobody.

### 5 · 🧱 The Board substrate under every route
**Serves all, owns none**: what the substrate supplies to every concern.

```text
🧱 Board substrate

  📄 supplies   page + index grammar · sentence address · lanes · render
  🤝 serves     all nine concerns · this Engine group · every future Skill card
  🚫 never      a concern of its own · an author of concern content
```
📌 This part keeps the substrate off the crosswalk: it is under every row and inside none.

`haipipe-board` and its page and sentence contracts carry every QB page, this page, and every future Skill card alike.
The substrate serves every concern without owning content, so no crosswalk row lists a Board skill as a producer.
What a concern's page must say remains that page's business; the substrate only guarantees it renders, folds, and can be addressed.

## Aims
### A1 · 🧭 The direction and the one rule
- A1.1 · The one-directional authority rule binds every row on this page.
  **Done when:** No route row grants a skill authorship of a QB concern's content, and every Writes entry stops at working folders and files.

### A2 · 🗺 The concern-to-route crosswalk
- A2.1 · Every concern QB1 through QB9 has its producing route and working surface named.
  **Done when:** Each table row names callable skills from the application README's Stage to Procedure map and the folder or file that route writes.
- A2.2 · The map is reversible from the Delivery side.
  **Done when:** Each QB page names its Engine route by pointing at this crosswalk, or the missing pointer is recorded here as open.
- A2.3 · The narrative route gains an owner or stays unplaced on purpose.
  **Done when:** A QB page claims `haipipe-application-narrative` and its row is added, or the concern pages confirm that no concern claims it.

### A3 · 🃏 The six-field skill card
- A3.1 · Future Skill pages on this board fill the card without reading the paper board.
  **Done when:** All six fields and both narrowing rules are stated here, and the first Skill card written on this board cites no other card contract.

### A4 · ⚙️ What the round-3 stage engine absorbs
- A4.1 · The engine's absorption set is ruled by JL, not assumed by the map.
  **Done when:** The Decision Now row is answered and every candidate mark in Part 2 is flipped to absorbed or kept per the ruling.

### A5 · 🧱 The Board substrate under every route
- A5.1 · The substrate's service to all nine concerns is stated without giving it content authority.
  **Done when:** Part 5 names what the substrate supplies and what it never owns, and no crosswalk row lists a Board skill as a producer.

## States
### Decision Now
- [ ] 🗣 Which routes does the round-3 stage engine absorb?
      📍 `Part 4` states the marking rule; Part 2 carries the candidate marks this ruling flips.
      🔔 `Why now` round 3 is scoped against this map, and every Skill card for a stage route waits on the set.
      `A ·` absorb only the four rung orchestrators (QB2 to QB5); seed, venue, pitch, display, and section-edit keep their own routes and their own future cards.
      ⭐ `B ·` absorb every 1-lifecycle stage orchestrator; one engine runs the shared DRAFT to PROBE to REVISE to CHECK loop, each stage keeps only its contract, and CC recommends B because the loop is already identical across those routes.
      `C ·` absorb nothing; the per-stage orchestrators stay the routes and round 3 drops the engine.
      🛑 `Blocks` closing A4.1, and any Skill card that would claim the engine as its route.
      🤖 `If nobody answers` the candidate marks stay candidates and no card claims the engine.

### A1 · 🧭 The direction and the one rule
- ✅ A1.1 · Met; every Writes entry in Part 2 stops at working folders and files, and no row claims a QB page's content or gate.

### A2 · 🗺 The concern-to-route crosswalk
- ✅ A2.1 · Met; all nine rows name skills from the application README's Stage to Procedure map with their working surfaces.
- ⬜ A2.2 · Not started; no QB page points here yet.
- 🧠 A2.3 · Waiting on the concern pages to claim or decline the narrative route.

### A3 · 🃏 The six-field skill card
- 🧠 A3.1 · Waiting; the fields and both narrowing rules are stated in Part 3, and no Skill card has been written against them yet.

### A4 · ⚙️ What the round-3 stage engine absorbs
- 🧠 A4.1 · Waiting on JL; the Decision Now row above carries the options and the default.

### A5 · 🧱 The Board substrate under every route
- ✅ A5.1 · Met; Part 5 states what the substrate supplies and what it never owns, and no row in Part 2 names a Board skill.

## Files
- `../../application/README.md`
  The Stage to Procedure and Router Rule maps every crosswalk row cites; start here when a route's skills change.
- `../01-haipipe-paper-260725/QC-engine/QC1-delivery-skill-map.md`
  The precedent QC1@paper: the six-field card and the one-directional authority rule this page adopts.

## Law
- 260730 JL · ⚖️ Delivery owns content; the Engine maps routes
      A concern's content and its human completion gate belong to its QB page, and no route becomes a second author.
      JL accepted the Delivery-first, skill-first structure on the paper board (QC1@paper, 260730), and this page adopts the rule unchanged; the rejected shape was an Engine that also carried content, which makes two sources of truth for one concern.

## Glossary
- 🛣 **Skill route**: the ordered callable skills that may serve one Delivery concern.
- 🤝 **Serves**: a skill's limited role for a concern, never ownership of its content.
- 📂 **Working surface**: the folder or file a route writes inside the intervention, as fixed by the application README's layout.
- ⚙️ **Round-3 stage engine**: the shared stage runner planned for this board's third work round, running the DRAFT to PROBE to REVISE to CHECK loop each stage orchestrator currently drives itself.
- 🧱 **Board substrate**: the generic page, index, sentence, and routing machinery from `haipipe-board` that every page on this board rides on.

## Log
260802 · Created: nine QB concerns mapped to application routes, the six-field card adopted from QC1@paper, and the engine absorption set raised as a Decision Now for JL.
