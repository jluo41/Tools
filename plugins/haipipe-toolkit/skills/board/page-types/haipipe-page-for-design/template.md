<!-- TEMPLATE · ONE BRIEF = ONE DESIGN PAGE.
     Copy this file into the board group that owns the brief, rename it the way that group names
     its pages, fill every <angle-bracket> slot, and DELETE each RULE comment as you satisfy it.
     A RULE comment never ships in a filled page.

     LOAD FIRST, both of them:
       · `haipipe-page`            the BASE frame: section order, the Opening blank-line
                                         split, figure captions, Content numbering, the Aim and
                                         State vocabularies, Files groups, Decision Now.
       · this folder's SKILL.md          the CONTRACT this file serializes.
     Everything not marked below is the base's, unchanged. This template adds no section, moves
     no section, and renames nothing.

     WHAT THIS PAGE IS NOT. It does not hold anything that outlives the choice it makes:
       the winner's render, and who accepted it   -> a display unit page, `-for-display`
       a rule the winner establishes for others   -> the page that owns that rule
       which Page Types exist                     -> the board's page-type hub page
       talk about the options                     -> the meeting page, then routed here
     A design page SELECTS. It produces nothing another page reads, so it normally declares no
     `provides:` line and owns no companion folder on disk.

     NO markdown pipe tables anywhere (JL 2026-07-10): every would-be table is record lines.
     English only. No em-dashes. One sentence per source line. -->

# <Short sentence-case title: what this brief must produce, and for whom. Keep whatever prefix the page's own group uses, such as `<page id> · ` or `<subject> · `.>

state: 🔴 OPEN
page-type: design
owner: <JL | CC>
method: write the brief first, draw each candidate whole beside the others, and close on one selection record that keeps every loser and the reason it lost

<!-- RULE: `page-type: design` is REQUIRED and it is the ONLY thing that marks this page as a
     brief. No filename shape marks one, so without the key a resolver, a checker, and a cold
     reader all read the divisions as ordinary Content instead of as candidates. Keep it in the
     head block, above `owner:`. It BEATS the filename (base, type resolution step ③), which is
     what lets a brief wear a `Q<group><n>-` or `S-<Family>-<unit>-` filename without being
     resolved as a Q decision page or a stage page. -->

<!-- RULE: `state:` begins with one of the FOUR page values: 🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED ·
     ⏸️ ON HOLD. On this type they mean: 🔴 the brief is written and no candidate is drafted yet ·
     🟡 candidates are on the page and no selection is recorded, or a selection is recorded with
     an unfilled line · ✅ the SELECTION record is complete and every criterion is met or
     explicitly held · ⏸️ the brief is parked. A short readable detail may follow the emoji, such
     as `🟡 PARTIAL · selected <YYMMDD> by <who>; <what is still open>`. The evidence belongs in
     `## States`, never in the state line. -->

## Opening
<The brief's lead question, in one sentence, ending in a question mark: what has to be designed, for whom, and what has to be true of it.>
<Say what the thing being designed is, with a real example.>
<Say why the choice is hard, which on a brief is usually that two of its own criteria pull against each other.>
<Say what this page decides, which is which candidate wins.>

**Who it is for**: <the audience, named concretely: which people, which reader, which downstream consumer, and what they already know.>

**What it must do**: <the job the winning artifact has to do, stated so a candidate can fail it.>

**What bounds it**: <the constraints: length, channel, venue limit, tone, budget, what already exists that it must not contradict.>

**Where the candidates live**: <the folder holding the candidate files, or "drawn in the divisions below: these candidates are shapes, not files".>

**Covered elsewhere**: <the page that owns the winner once it renders, and the page that owns any rule the winner establishes.>

<!-- RULE: THE FIRST BLANK LINE IN `## Opening` IS THE SPLIT. The four lines above it are joined
     into the one paragraph a reader sees without clicking, capped at 520 characters on the
     render; everything below it drops into the More details drawer. So the question and the three
     sentences that explain it are CONSECUTIVE lines with no blank line between them. A brief that
     shows one bare question on stage has hidden its own audience and goal behind a click, which
     is the exact failure the split causes when the blank line is placed one line too early. -->

<!-- RULE: THE PAGE IS THE BRIEF, and the four labelled parts above are it. A candidate can only
     be judged against a stated brief, so audience, goal and constraints are written BEFORE any
     candidate is drafted. Writing them afterwards is reconstruction: it is allowed when a real
     choice already happened and is being recorded, and it is then MARKED 🚫 on every line it
     touches, including the criteria in `## Aims`. -->

<!-- RULE: the brief is prose in the Opening, never a Content division of its own. Content
     divisions are candidates and nothing else, which is what lets a reader count candidates by
     counting divisions. -->

## Diagram

**<The fork>**: <the axes the candidates differ on, and the cell each one sits in.>

```text
  <one /diagram-ascii figure, under about 80 columns, emoji on every box and row label>
  <put the candidates side by side, because side by side is the whole argument of a brief>
  <a row is a label and its value; if a row could end in a period it is prose and belongs below>
```

<!-- RULE: this section is optional on the base and effectively always earns its place here: a
     brief exists because several shapes compete, and a comparison is exactly what a figure does
     better than prose. Delete the whole section only when the candidates differ on one axis that
     a sentence already states. -->

## Content

<!-- RULE: ONE CONTENT DIVISION PER CANDIDATE, plus one final division for the SELECTION record.
     A division carries ONE candidate WHOLE: the artifact itself, the rationale for drafting it
     that way, and its fit to every criterion in `## Aims`. A division holding the artifact and no
     rationale is half a candidate, because the selection has to weigh why each one was drafted
     the way it was. A pointer to a chat message is not a candidate: chat scrolls away. -->

<!-- RULE: WHERE THE ARTIFACT LIVES, and it is never a folder named after this brief.
       · A candidate that IS a file lives with the thing it will become. On a paper that is the
         display unit's own workspace:
         `0-lifecycle/S05-display/workspace/<S-Display-unit>/candidates/<LETTER>-<slug>.<ext>`,
         which already exists for every unit and holds real files for some of them.
       · A candidate that is a wording, a layout, or a rule has no file. Draw it WHOLE inside its
         division; the drawing IS the artifact.
     Write the path on the `artifact:` record line inside the division, never in the `###`
     heading: a backticked path token in a heading renders a chip whose href skips the render's
     path rewriting, so the link lands nowhere. -->

<!-- RULE: the candidate LETTER is its stable name and the division number is only its position.
     Keep the letter identical everywhere it appears: the heading, the fit block, the SELECTION
     record, and the file prefix in `candidates/`. Renumbering divisions must never renumber a
     candidate, because the SELECTION record and the next brief both cite the letter. -->

### 1 · Candidate <A> · <one-line name of the shape> · <⬜ UNDECIDED | 🏆 WINNER | ♻️ MERGED | 🪦 DROPPED>

**<The artifact>**: <what this figure shows.>

```text
  <the candidate itself, drawn whole: the message text, the layout, the folder shape, the wording>
  <or delete this fence and embed the real file instead, on its own line: ![](<path>)>
  ─────────────────────────────────────────────────────────────────
  fit to the brief
    P1 <emoji> <criterion, in three words>   <✅ | 🟡 | ❌> <the clause that decides it>
    P2 <emoji> <criterion>                   <✅ | 🟡 | ❌> <the clause that decides it>
```

<emoji> <One or two lines saying what this candidate establishes, so a reader who jumped straight here knows what they are looking at.>

artifact: <path to the candidate file under the owning unit's `candidates/`, or "drawn above: no file">

**Why it was drafted this way**: <the reasoning behind this shape, in its own terms, written as if it might win.>

**<What it fails | What it bought>**: <for a loser, the criterion it cannot meet and what that costs; for the winner, what its shape actually bought, and what it borrowed from each loser.>

**<Where it went | What it still owes>**: <for a loser, written only after selection: `merged`, `dropped`, or `kept for A/B test`, then the reason and any tail it left behind; for the winner, the part of it that is not finished.>

<!-- RULE: the fit block names EVERY criterion id in `## Aims`, including the ones this candidate
     passes. A fit block listing only the criteria a candidate wins is an advertisement, and the
     selection cannot be checked against it. It may sit inside the candidate's figure, as rows at
     the foot of the fence, or below it as a `**Fit to the brief**:` part with one record line per
     criterion. Inside the figure is usually better, because the reader compares one candidate's
     marks against the next candidate's, and that comparison is what a figure is for. -->

<!-- RULE: the labelled parts are the SHAPE of a candidate division, not four fixed strings. Every
     division owes the artifact, the rationale, the fit, and the disposition with its reason. The
     winner's last two parts read differently from a loser's, and that is correct: a winner has no
     "where it went". Do not force a loser's wording onto it. -->

<!-- RULE: the division opens with a CAPTION LINE, then the figure or the embedded artifact, then
     the one-line intro, in that order. The caption is `**Name**: what this diagram shows.` on the
     line directly above the fence. The checker reads the first non-empty line of every division
     and reports a missing caption or a missing figure, and an embedded image or PDF counts as the
     figure. -->

### 2 · Candidate <B> · <one-line name of the shape> · <disposition>

**<The artifact>**: <what this figure shows.>

```text
  <candidate B, drawn whole, with its own fit rows at the foot of the fence>
```

<emoji> <What this candidate establishes.>

artifact: <path, or "drawn above: no file">

<the same parts as division 1, in the same order: why it was drafted this way, what it fails or bought, where it went or what it still owes>

<!-- RULE: copy this division for each further candidate, keeping the part order identical across
     all of them: a reader compares candidates by reading the same part in each division, and a
     division that reorders its parts breaks that read. Two candidates is a real brief; one
     candidate is not a brief and belongs on an ordinary page. -->

### <N+1> · SELECTION · <YYMMDD> · <who ruled>

**<The record that closes the page>**: <the winner, why it won, and where each loser went.>

```text
  🏁 SELECTION · <YYMMDD> · <who ruled>
  ─────────────────────────────────────────────────────────────────
  winner      candidate <B>   <the shape, in three or four words>
                              <why it beat the others, one or two lines>
  ─────────────────────────────────────────────────────────────────
  loser <A>   <dropped | merged | kept for A/B test>
                              <why it lost, or what it kept doing>
  ─────────────────────────────────────────────────────────────────
  loser <C>   <disposition>   <why it lost; for an A/B test, the
                              measurement that would decide it>
  ─────────────────────────────────────────────────────────────────
  downstream  <path>          <the display unit page the winner becomes
                              or updates, by path>
```

🏁 <One or two lines saying what this record settles.>

<add a labelled prose part ONLY for what the fence above cannot carry: an open `downstream` line and why it is open, the tail a dropped candidate still leaves in the code, the tradeoff the winner accepted. Delete this line when the fence says it all.>

<!-- RULE: THE SELECTION RECORD IS THE LAST CONTENT DIVISION, and this template rules that
     placement because the contract states only that the record CLOSES the page. It is a dated
     ruling with content weight, and `## States` is a snapshot of right now, so a record parked
     there would decay into a status line and lose its losers. If the contract later names a
     different home, this template is the defect and the contract wins. -->

<!-- RULE: three dispositions and no others: `dropped`, `kept for A/B test`, `merged` into the
     winner. Every loser gets one. A loser with no disposition means the brief is still open, and
     the page state is 🟡, not ✅. -->

<!-- RULE: SELECTION IS A HUMAN JUDGMENT, like display acceptance. A machine may PROPOSE a winner
     as a `### Decision Now` row and may write the record only after the human has ruled, naming
     which option, who ruled, when, and the words they used. A machine never records a selection
     nobody made. -->

<!-- RULE: `downstream` is a PATH, and it is the handoff: it names the display unit page the
     winning candidate becomes, or the existing one it updates, and `-for-display`'s acceptance
     ladder takes over from there. A winner that renders nothing has no display page; write
     `⬜ OPEN` with one clause saying why, and carry it as a `### Decision Now` row. An invented
     path makes the record pass and makes it a lie, which is the one thing this record must not
     be. -->

<!-- RULE: A LOSING DIVISION IS NEVER DELETED. After selection only its disposition changes; the
     artifact and the rationale stay exactly as they were judged. The next brief for the same
     audience starts by reading why the last losers lost, and deleting a loser deletes that. -->

## Aims

<!-- RULE: AIMS ARE THE BRIEF'S CRITERIA, one Aim per criterion, and they are page-level `P` ids
     under ONE `### P · <emoji> <name>` group. Never `### A<n>` on this Page Type. Two reasons,
     and the first is mechanical: the checker reads `### A<n>` in Aims and States as the Aim group
     of Content division `### <n>` and requires the two to carry the same name, but here division
     1 is a CANDIDATE and Aim 1 is a CRITERION, so the names can never match and every criterion
     would fire `group-name-drift`. The second is the real one: a criterion cuts across every
     candidate at once, so it belongs to no single division, which is exactly the case `P` exists
     for. A target that genuinely belongs to one candidate, such as re-rendering candidate C, is
     still written as a `P<n>` with the candidate's letter in its text. -->

<!-- RULE: the criteria are written from the brief, BEFORE the candidates are drafted, and the
     fit block in every division answers this list id by id. Add the closing criterion last: the
     SELECTION record itself is a target this page carries. -->

### P · <emoji> <The brief's criteria, and the record that closes them>
- P1 · <emoji> <the first criterion, stated so a candidate can fail it>
  **Done when:** <the observable test that decides it, naming what a reader would look at>
- P2 · <emoji> <the second criterion>
  **Done when:** <its test>
- P<n> · 🏁 <Every line of the SELECTION record is filled with something a person can act on.>
  **Done when:** <the winner, every loser's disposition, and `downstream` all name something real>

## States

<!-- RULE: States mirrors EVERY Aim id exactly ONCE, as a status row: `- <shape> P<n> · <the
     fact>`. The five shapes are ⬜ not started · 🔨 being worked on now · 🧠 waiting on a person or
     on something outside this page · ✅ met with the evidence named · ❄️ on ice on purpose. A
     narrative line that mentions `P1` inside its prose is NOT a status row: the parser reads only
     the row shape, so a page written that way reports every criterion as not started while
     reading as if the work were done. History and reasoning go to `## Log`. -->

### Decision Now

<!-- RULE: `### Decision Now` goes FIRST in States, above the `P` group, and it is where a
     machine's proposed winner waits. One `- [ ]` row per pending decision, each option on its own
     line saying what choosing it commits you to, and the recommendation on its own line. Delete
     the whole subsection when nothing waits on a person. -->

- [ ] 🗣 <The ask, stated as one question>
      <One or two lines of context: what is true today, and what it costs.>
      A · <the first option, and what choosing it commits you to.>
      B · <the second option, and what it commits you to.>
      → <CC recommends B, because the reason it beats A.>

### P · <emoji> <The brief's criteria, and the record that closes them>
- ⬜ P1 · <not started; no candidate has been measured against this criterion yet>
- ⬜ P2 · <not started>
- ⬜ P<n> · <not started; no selection has been recorded>

<!-- RULE: the States group repeats the Aims group heading word for word, so a reader comparing
     intent against fact never has to work out which group means which. -->

## Files

<!-- RULE: name the ARTIFACTS a person opens to continue this brief, each with one line saying
     what it is for. The candidate files come first, then the pages the winner hands off to.
     `<the candidates folder>` is not a way to reach anything: name the files. -->

- `<path>/candidates/<LETTER>-<slug>.<ext>`
  <Candidate <LETTER>'s artifact, as it was judged. Never edited after selection.>
- `<the display unit page, or the page the winner updates>`
  <Where the winner goes next, and who accepts its render.>
- `<page-types/haipipe-page-for-design/SKILL.md>`
  <The contract this page is an instance of. If the two disagree, the contract wins and this page is the defect.>

## Log

<!-- RULE: the brief's history belongs HERE, not in Content and not in States. When the criteria
     changed and why, when each candidate was drafted, when the selection was ruled and by whom.
     Content says what each candidate IS; the Log says how the choice got made. Never delete a
     `> USER:` line: resolve it and move it here verbatim. -->

- <YYMMDD> · <what changed>

<!-- RULE: THE MECHANICAL GATE. The page is not done until it renders clean and a person has read
     the RENDER, not the markdown:
       python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
       python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^<PAGE-ID>'
     Zero findings on this page, plus the four traps this Page Type carries that no checker sees:
       ① `page-type: design` present in the head block, or the page is resolved as the wrong type.
       ② no `### A<n>` group in Aims or States; criteria are `P<n>` under one `### P ·` group.
       ③ every candidate division opens with a caption line and a figure or an embedded artifact,
          and its fit block answers every criterion id.
       ④ every loser still has its division, with its disposition and the reason it lost.
     Register the page in the board's `board.md` roster in the same session (base, CREATE step 7):
     an unregistered page builds a group whose token is a bare emoji, and every bare emoji inside
     every figure on the board then renders as a dead link.
     On a page whose filename starts with `Q`, the checker additionally refuses `state: ✅` while
     any Aim is open, so a brief closes only when every criterion is met (✅) or explicitly held
     (❄️) with the reason on its own State row. -->
