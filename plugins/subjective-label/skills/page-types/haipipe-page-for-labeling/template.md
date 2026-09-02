<!-- TEMPLATE · ONE CORPUS + ONE LABEL TARGET = ONE S-Label PAGE.
     Copy this file to `<board>/<group-folder>/S-Label-<n>-<corpus>-<target>.md`, fill it, and
     DELETE each RULE comment as you satisfy it. A RULE comment never ships in a filled page.

     WHAT THIS FILE IS. The shape of a labeling Job Page, in the order its sections must run,
     with one RULE comment per rule. It states no rule that is not already in
     `haipipe-page-for-labeling/SKILL.md` (this Page Type) or in `haipipe-page`
     (the base frame). Load both before filling this in.

     WHAT A LABELING PAGE IS. One page per corpus and label target, holding one run of the
     calibration loop. It SETTLES NO METHOD: how a round works is fixed by the subjective-label
     board's QA0 through QF5, and this page records what happened, never how it is supposed to
     work. Its job is to answer two questions a folder of JSONL cannot: what does the target
     mean today, and can the labels be used yet.

     WHAT IT DOES NOT OWN. The method. The other targets on the same corpus, which get their
     own pages. The inventory of runs, which is `S-Label-Dash` and has its own specimen,
     `template-dash.md`.

     ⚠️ THE ONE THING THAT CATCHES EVERY RUN PAGE. The method pages this page obeys live on a
     DIFFERENT board: the run board holds what happened, the design board holds how the loop
     works, and they are never the same board. So every reference to a method page is a
     CROSS-BOARD reference, and cross-board references work differently in both places they
     appear. See the RULE comments at `requires:` and at Related Board Pages. Getting this
     wrong reports `dead-related-page` and `Stage Contract source not found`, and the page
     still builds, so nothing stops you.
-->

# S Label <n> · <Corpus> × <target>

<!-- RULE · title. `S Label <n> · ` first, then the subject, so the reader knows the identity
     before the phrase. Sentence case after the dot. -->

state: 🔴 OPEN
page-type: labeling
owner: <the human semantic authority>

<!-- RULE · `page-type:` is REQUIRED and it is not decoration. The 🔌 Plugin menu's
     🏗 Building entry gates on it, so a page that omits the key gets no labeling
     surface however labeling-shaped its filename is. The key beats the filename. -->
method: <one line: which loop, on what, until what>

requires: <path>, <path>
style-from: <path>
provides: <the terminal deliverable, e.g. "D*, one labeled record per item with provenance">

<!-- RULE · requires, and it has TWO cases.
     SAME BOARD: a bare page id resolves. `QA2` works; `QA2-label-region.md` does not, unless
       that file sits at the board root.
     ANOTHER BOARD: an id does NOT resolve, because ids are looked up in THIS board's pages
       only. Write the real path relative to this board's root, escaping it, for example
       `../../../../Tools/plugins/<plugin>/diagram/<board>/<group>/QA2-<slug>.md`.
     A method page is always the second case, because the design board and the run board are
     different boards. Getting it wrong prints `Stage Contract source not found: QA2` and then
     builds anyway. After filling this in, run `stage.py sync <board> S-Label-<n>` so the
     managed contract block is written; the build warns until you do. -->

## Opening

<!-- RULE · the on-stage paragraph ends at the FIRST BLANK LINE, is 4-5 sentences and at most
     520 characters, and is written for a weak English reader. Everything after the blank line
     becomes the collapsed drawer. -->

<the lead question: what does this target mean here, and are the labels usable yet?>
<what the target is, in one clause a reader outside the project can follow.>
<what makes it hard: why the authority cannot state the boundary before seeing real items.>
<what this page therefore does, and that it says which gate is still open.>

**Where this page sits**: `S-Label-Dash` lists every run, and this is one. The loop is fixed elsewhere and is never restated here.

**More details**: <why one corpus plus one target is one page, using the per-unit test; and why a round is not one.>

**Why it matters**: <the stake. A concrete measurement beats an assertion: if a keyword baseline was tried and mostly returned noise, say the counts.>

## Writing Style

<!-- RULE · four rules at most, each one this page will actually be edited against. -->

**Every quoted item is verbatim and carries its id**: a paraphrase cannot be re-judged.

**A proposal is marked as a proposal**: a machine may draft a class; only a session makes it gold.

**Numbers name the day they were measured**: a corpus can be recut.

**The method is not restated**: this page records what happened.

## Stage Contract

<!-- ⚠️ RULE · DO NOT WRITE `### Required Inputs` OR `### Venue` YOURSELF. `stage.py sync`
     generates both inside a managed block bounded by `haipipe:contract:start/end`, and it
     replaces everything between those markers. Writing your own heading of either name gives
     the page TWO of it: the generated one and yours, one above the other, and the checker
     reports nothing because both are legal headings.
     Your own contract material goes AFTER the end marker, under a heading of your own naming.
     `### Provides` is yours and sync does not touch it. -->

### The record shape · authored, outside the managed block

<!-- RULE · the record schema is INHERITED, not invented here. Point at the page that fixes it
     and show the fields. Do not add a fifth field, and do not turn a workflow state into a class. -->

**The record shape comes from <page id> unchanged.**

```text
📄 one completed annotation
├── 🏷 class_label         H | L | N
├── 🗺 diagnostic_region   H|L|N|HL|LN|HN|HLN
├── 🌡 uncertainty         project scale
└── 🧾 rationale           free text
```

**What one item is, for this target**: <the unit, and any context carried with it.>

```json
{ "item_id": "<id>", "text": "<the unit>", "context_prev": "<context, if the unit needs it>",
  "class_label": "H", "diagnostic_region": "H", "uncertainty": 1, "rationale": "<why>",
  "policy": "G_1", "labeled_by": "<authority>", "checkpoint": "round-1" }
```

<!-- RULE · if context is carried, say in one line that it is context for the judge and is
     never itself labeled. A unit that cannot be judged alone needs this said out loud. -->

### Provides

<the terminal deliverable, one sentence.>

## Diagram

**<caption>**: <what this figure shows>, measured <YYMMDD>.

<!-- RULE · every division and the Diagram open with `**Name**: what this shows.` The check
     reports `division-no-caption` when the first line of a division is not that shape. -->

```text
<the corpus and its size · the seal · the round chain with the current position marked
 · the gates · the frozen tail, each step carrying ⬜ 🔨 🧠 ✅>
```

## Content

### 1 · What <target> means now

**<caption>**: quoted from `policy/versions/G_<t>/cheatsheet.md`, <closed | PROPOSED, not closed>.

<!-- RULE · §1 QUOTES the built label. The block below is the cheatsheet's, and the seed
     cases in 1.2-1.5 come from `policy/versions/G_<t>/gallery.md`, each with its item id.
     Redrafting a rule here makes a second source of truth; the policy version wins. -->

```text
📜 G_<t> cheatsheet  ·  <closed | PROPOSED, not closed>
   🟢 HIGH   <the rule, verbatim>
   🔵 LOW    <the rule, verbatim>
   ⚪ NONE    <the rule, verbatim>
   🗺 regions <the seven tests, one line>
```

#### 1.1 · What LOW means here
<!-- RULE · REQUIRED. A reader cannot guess whether LOW is a weaker HIGH or the near miss.
     Say which, and say what follows: where LOW is the near miss, the boundary region carries
     the work and the page should expect it to be the largest. -->
(<the paragraph's job, in one line of parentheses.>)
<four or five sentences.>

#### 1.2 · Seed case · clear HIGH
(<item id>, <split>. <who proposes what, or who ruled it>.)
> <verbatim item, with the deciding words in bold>

<why it is HIGH, and the test that makes it so.>

#### 1.3 · Seed case · the boundary
<!-- RULE · on a boundary item, give the REGION and leave the class blank. Set out both
     readings so the human can rule between them, and say what the ruling then becomes. -->
(<item id>, <split>. Region HL proposed; no class proposed.)
> <verbatim item>

<reading one, and why it is defensible.>
<reading two, and why it is defensible.>
<what the human's ruling becomes, and what it must then exclude.>

#### 1.4 · Seed case · clear LOW
#### 1.5 · Seed case · clear NONE
<!-- RULE · include a NONE. A page whose examples are all interesting teaches a weak model
     that everything is interesting. -->

### 2 · Rounds

**The ledger**: one record per closed round, newest first. A round is never a division of its own.

```text
📌 <n> rounds closed · <n> items in cumulative gold · <which policy is open>
```

**round_<t>** · closed <YYMMDD> · G_<t-1> → G_<t> · <n> items (<n> challenge / <n> audit)
  🃏 card       <the gap the card targeted, and what it expected>
  🎯 actual     <what happened vs the forecast, from view/result.md>
  📜 diff       <what moved in the policy · how many prior rows flipped>
  🗺 register   <which cells settled · which are still open>
  🚦 route      <another round | freeze | HOLD>

<!-- RULE · record lines, never a markdown table. Newest first. One record indexes ONE round
     unit `rounds/round_<t>/` (ref-assets.md §3): card and forecast from the unit, actual from
     its view/result.md, route from its checkpoint. Adding a round adds five lines at the top
     and moves no heading. -->

### 3 · Gates: may we stop?

**<caption>**: read from `rounds/round_<t>/checkpoint.json` (the newest), all must pass before Freeze.

<!-- RULE · every gate row reads its value from the newest checkpoint and names it; coverage
     reads register.md. A number no checkpoint holds is not evidence. -->

```text
📊 quality     <reading vs threshold · checkpoint-<t>>   <state>
📉 stability   <streak k of K comparable checkpoints>    <state>
🗺 coverage    <register cells still open>               <state>
🚨 risk        <routed fraction · checkpoint-<t>>        <state>
```

#### 3.1 · <which gate is actually blocking, and what closes it>

### 4 · Freeze, sealed test, scorecards

**Locked until the gates pass**: this division stays empty on purpose, and the emptiness is the status.

```text
🔏 handoff  <handoff/label-v1.yaml id + checksum, or "not written">
🔒 G*       <frozen version, or "not frozen">
🧪 T*       <the seal: which split or sample, its size, read or unread>
📊 S*       <scorecards, or "no executor scored">
```

### 5 · The labeled corpus

**<caption>**: <state of completion>.

```text
📦 D*   <state>
🚨 risk queue        <state>
🎲 final audit       <state>
```

## Aims

<!-- RULE · Aims ARE the stopping gates. Do not invent a second set. Heading shape is
     `### A<n> · <emoji> <name>`; items are `- A<n>.<m> · <target>` with a `**Done when:**` line.
     A bare `### 1 · ...` heading is not read as an Aim and the page reports `no-aims`. -->

### A1 · 📜 What <target> means now
- A1.1 · The closed policy is executable by a weaker model.
  **Done when:** <the observable event>

### A2 · 🔁 Rounds
### A3 · 🛑 Gates: may we stop?
### A4 · 🔒 Freeze, sealed test, scorecards
### A5 · 🏭 The labeled corpus

## States

<!-- RULE · one row per Aim id, and the STATE EMOJI COMES FIRST: `- ⬜ A1.1 · <what is true>`.
     Writing `- A1.1 · ⬜ ...` is not matched, and the page reports `aim-without-state` and
     renders 0 of N. States are ⬜ not started · 🔨 being worked · 🧠 waiting on a person
     · ✅ met with the evidence named · ❄️ on ice. -->

### A1 · 📜 What <target> means now
- ⬜ A1.1 · <what is true now, with the evidence named>

### Decision Now

<!-- RULE · only for a question that STOPS something. If you could decide it yourself, decide it
     and write it in `## Log`. A row that blocks nothing MUST carry a default. -->

🗣 **<the question as the row's title>**
📍 Part: <the division it belongs to>
🔔 Why now: <what is waiting>
- ⭐ **<the recommended option>** <what follows if chosen>
- <the other option> <what follows if chosen>
🛑 Blocks: <what stops until this is answered>
🤖 If nobody answers: <the default, or why no default may stand in>

## Files

**The run on disk**:

```text
runs/<corpus>-<target>/                the job folder, ref-assets.md §1
├── config.yaml              schemas · thresholds · consecutive_rounds_k · executors
├── register.md              seven regions × open / covered / risky
├── corpus/manifest.json     ids · text checksum
├── policy/versions/G_<t>/   closed, immutable · + cheatsheet.md · gallery.md (§1 quotes these)
├── gold/cumulative.jsonl    human-confirmed rows only
├── rounds/round_<t>/        one ROUND UNIT per closed round: card · manifest · evidence ·
│                            prospect · events · checkpoint.json · view/ (§2 indexes these)
├── handoff/label-v1.yaml    written once at P2 Freeze (§4 shows it)
└── test/sealed/             reserved, unread
```

**The corpus**: <path, and the field the unit is read from.>

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [S-Label-Dash page](<group>/S-Label-Dash.md)
  The Dash carries this job's row and the one gate it is blocked on.

<!-- RULE · this exact row shape or the check reports `related-row-form`.
     ⚠️ ONLY PAGES ON THIS BOARD MAY APPEAR HERE. A path that leaves this board reports
     `dead-related-page`, and the rendered link additionally reports `dead-href`. The method
     pages are on the design board, so they are NOT Related Board Pages, however related they
     feel. Declare them in `board.md`'s `## Links` and cite them by name in the block below. -->

### The method · pages on ANOTHER board

The loop this run executes is settled on <the design board>, which is not this board, so those pages cannot be Related Board Pages here. They are declared in `board.md`'s `## Links` and cited by name:

- `<id>` <what it fixes for this page.>

<!-- RULE · `## Links` in board.md maps each backticked form to a real path, after which the
     form becomes a live link in this prose. One declaration per board, not one per page. -->

## Law

<!-- RULE · only rulings this PAGE made. A rule that holds for every labeling page belongs in
     the Page Type's SKILL.md, not here. -->

## Log

<YYMMDD> · <what changed>
