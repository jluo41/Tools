# QBt18 · page-type OPENING · establish the paper before Narrative orders it

state: ✅ SETTLED · contract, resolver, Board, and fresh-context validation complete
page-type: opening
owner: JL
method: test whether one control page can replace duplicated Seed, Venue, and Pitch reads without migrating runtime pages

## Opening
What paper is this, for whom, and what may Narrative safely assume before it begins ordering claims?

Opening answers that question once per paper.
It combines a venue-free paper identity with a venue-aligned position and finishes with a bounded Narrative handoff.

**Covered here**: the seven fixed roles of Opening and its compatibility boundary.

**Covered elsewhere**: the reusable venue catalog stays in `QBv`; Narrative architecture stays on `QBt15`; Section execution stays on `QBt6`.

## Writing Style
Plain English for a reader who has never opened the paper.
One sentence per line, and no em dashes.

## Content
### 1 · Identity · one paper, one research question
**Stable identity**: retargeting changes the desk, not the paper's empirical identity.

```text
working title ─▶ paper identity ─▶ primary research question
```

Opening states the working title, paper identity, and primary research question.
These survive a venue retarget.

### 2 · Stakes · the problem, reader, and why now
**Stakes test**: the problem must matter to a named reader now.

```text
problem + reader + timing ─▶ stakes
```

Opening says what is at stake before it tries to sell the answer.
The reader is concrete enough to test the venue choice.

### 3 · Source Pages · existing work the paper can read
**Page inventory**: sources cross the boundary as Pages rather than copied evidence.

```text
Board A Page ─┐
Board B Page ─┴─ PageX ─▶ Opening
```

Opening inventories existing Board Pages through PageX.
It references their evidence, displays, and citations through the Page boundary instead of copying them.

### 4 · Establishment · what is known and where the line stops
**Establishment boundary**: every proposition carries a confidence state and source.

```text
established | provisional | absent ─▶ headline + hard limit
```

Every important establishment is marked established, provisional, or absent.
The headline finding and hard limit are visible together.

### 5 · Venue Position · the selected desk and audience
**Venue position**: shared catalog knowledge becomes one paper-specific choice.

```text
QBv catalog ─▶ selected desk + audience + fit
```

Opening records the selected venue, audience, and fit.
Reusable venue knowledge remains in the QBv catalog rather than being copied into this page.

### 6 · Editor Promise · why this desk should care
**Promise ceiling**: venue framing may narrow the promise but cannot cross the limit.

```text
contribution + payoff ≤ hard limit
```

The promise states the contribution and payoff without exceeding the hard limit.
This division rewrites when the venue changes.

### 7 · Narrative Handoff · the bounded packet downstream may assume

**Opening output**: Narrative receives one bounded packet, not three legacy control pages.

```text
identity · primary claim · PageX support · hard limit
venue · promise · open tensions
```

Narrative begins from this packet rather than rereading legacy Seed, Venue, and Pitch pages.

## Aims
### A1 · 🪪 Identity · one paper, one research question
- A1.1 · Opening states one paper identity and one primary research question.
  **Done when:** both survive a venue retarget unchanged.

### A2 · 🎯 Stakes · the problem, reader, and why now
- A2.1 · The problem matters to a named reader now.
  **Done when:** problem, reader, and timing are explicit.

### A3 · 🔎 Source Pages · existing work the paper can read
- A3.1 · Existing work arrives as PageX references rather than copied evidence.
  **Done when:** each establishment names a source Page or an explicit gap.

### A4 · 📏 Establishment · what is known and where the line stops
- A4.1 · The headline claim and hard limit are visible together.
  **Done when:** every proposition is established, provisional, or absent.

### A5 · 🏛 Venue Position · the selected desk and audience
- A5.1 · Opening selects one desk and audience without copying the venue catalog.
  **Done when:** the paper-specific position points back to QBv knowledge.

### A6 · 📣 Editor Promise · why this desk should care
- A6.1 · The promise gives the desk a payoff without exceeding the hard limit.
  **Done when:** contribution, reader payoff, and boundary agree.

### A7 · 📤 Narrative Handoff · the bounded packet downstream may assume
- A7.1 · Narrative can begin from one bounded packet.
  **Done when:** legacy Seed, Venue, Pitch, and Claims are compatibility inputs only.
- A7.2 · A new agent builds all seven roles and stops at the handoff.
  **Done when:** the required fresh-context validation passes.

## States
### A1 · 🪪 Identity · one paper, one research question
- ✅ A1.1 · The v0.1.0 contract separates stable identity from venue alignment.

### A2 · 🎯 Stakes · the problem, reader, and why now
- ✅ A2.1 · Problem, reader, and timing are required in Division 2.

### A3 · 🔎 Source Pages · existing work the paper can read
- ✅ A3.1 · PageX references source work and explicit gaps route outward.

### A4 · 📏 Establishment · what is known and where the line stops
- ✅ A4.1 · Establishment state, headline claim, and hard limit are required together.

### A5 · 🏛 Venue Position · the selected desk and audience
- ✅ A5.1 · The selected position reads rather than duplicates the QBv catalog.

### A6 · 📣 Editor Promise · why this desk should care
- ✅ A6.1 · The editor promise is bounded by the hard limit.

### A7 · 📤 Narrative Handoff · the bounded packet downstream may assume
- ✅ A7.1 · Legacy pages remain read-only compatibility inputs.
- ✅ A7.2 · Fresh agent built all seven roles and stopped before accepting the handoff.

## Files
- `../../paper/page-types/haipipe-page-for-opening/SKILL.md`
  The v0.1.0 Opening contract.
- `4-QBt-page-types/QBt15-for-narrative/QBt15-for-narrative.md`
  The downstream Narrative specimen and decision record.

## Log
260817 · JL · approved Opening, Narrative, and Section as the Paper control structure
260817 · JL · kept PageX and Probe parallel for this design round
260817 · Codex · added the Opening contract, resolver entry, and Board specimen
260817 · fresh agent · passed the fixed Opening and preserved every evidence and human gate
