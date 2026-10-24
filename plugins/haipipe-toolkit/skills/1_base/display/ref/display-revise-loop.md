# Display Revise Loop

Owner: the `display/` family. Every display a reader will see (a paper's main text and appendix, a
report, a deck built from units) goes through this loop before its `accepted:` can be ticked. It is
a must, the way a draft is a loop: a display matters as much as the sentences around it.

Why (JL, 261022): a journal paper's first displays were rendered and shipped with no review. They
were black and white, their captions described instead of answered, and a unit folder named
`agreement-between-agents` held an odds-ratio table. JL asked "what question does this display
answer? why is it not in colour? what does each display represent?", then "display should also have
a loop, like the draft is a loop". The procedure below is what fixed that set: round 1 scored 5.5 to
6.5/10, round 2 fixed the colour clashes, a table's panel structure, an unfair denominator (a
same-unit panel was added), a redundant figure panel (it became the odds-ratio plot the table no
longer repeats) and a structural floor.

## The loop

```text
make ─▶ blind review r01 ─▶ pass? ── yes ─▶ ✅ the person may tick accepted:
            ▲                 │
            │                 no, and fewer than 4 rounds
            │                 ▼
            └── review rNN ◀─ revise (the maker fixes, re-renders, never scores itself)

after r04 with no pass ─▶ 🙋 stop; hand the person the open problems
```

1. **Make.** The renderer builds each unit by the output contract, with a `question:` in its README,
   the paper's one colour scheme, and a folder name that says what the unit is (the rules below).
2. **Blind review.** A FRESH agent, one that never saw the making, reviews the round. It reads only
   each unit's `preview.pdf` and `assets/figure.png` (when the unit has one): no `recipe/`, no
   README, no `intake/`, no paper text. Give it the brief below, verbatim.
3. **Record.** Save the reviewer's text for each unit as `<unit>/review/rNN.md` (the record below)
   and update the README `review:` line.
4. **Revise.** The maker fixes what the review names, re-renders and recompiles `preview.pdf`. Each
   fix goes where it lives: a caption, legend, label or folder-name change is the caller's (they are
   caller-owned); a picture change goes to the code that draws the picture. In a paper that code is
   a Run of the paper's work Block, and the unit only frames its `result/` (haipipe-paper-evidence,
   rule 3): fix that Run's script and rerun the Run, never patch the copy in the unit. The maker
   never scores its own work and never edits a review record.
5. **Review again** with ANOTHER fresh reviewer (not the round before's), and repeat until the pass
   rule holds or round 4 ends.

A unit changed after it passed (a new intake, a new caption, a new render) needs a new round: its
pass was for the picture that is no longer there.

## The pass rule

```text
pass  =  overall >= 8/10  and  question, readability, honesty, journal-ready each >= 7/10
```

- Every display the reader sees must pass; one failing display keeps the set open.
- **Stop after 4 rounds.** If round 4 does not pass, stop looping and hand the person the
  remaining problems (each unit's latest `review/rNN.md`, its scores, and what the maker could not
  fix). The person rules: a changed design, a cut, or a hand fix. A round after that ruling
  continues the numbering (r05, ...) and counts 4 more.
- **Stop earlier only when nothing is left the maker may change.** If every open problem needs what
  the maker may not touch (new numbers beyond the frozen intake, a definition only the author knows,
  a ruling between two designs), another round would re-score the same problems: hand over the same
  way, and say which problems block which score. A problem the maker can fix is never a reason to
  stop.
- **`accepted:` waits for a pass.** `accepted:` is the person's decision, and it can not be recorded
  on a unit whose latest round does not pass. A pass is not acceptance either: it only lets the person
  decide.

## The question rule

- Each display answers ONE question, written as a question a reader would ask, in the README:
  `question: Do the names the agent gives match the specialty the patient asked for?`
- The question and the answer live in the unit, not in the printed caption: README `question:` and
  the takeaways (`display.yaml` `takeaways:`, numbered). The text that cites the display gives the
  finding; the caption only lets a reader read the picture (the caption rule below).
- Each panel title is a short neutral label (A. Adjusted odds ratio; B. Agents vs search engine),
  never a variable name, and never a question or a finding.
- A display that answers two questions is two displays, or one question with two panels.

## The caption rule

A caption is short (JL 261023: "do not make it too long"; JAMA Network Open legends run 20 to 75
words). It has two parts, and nothing else:

- **Title**: a descriptive phrase of 10 to 15 words in the venue's style. It says what is shown,
  not what was found.
- **Legend**: at most 75 words for a figure, 120 for a table's footnotes. It defines what is drawn:
  every symbol, error bar, line, colour, scale, the groups compared and every abbreviation. One
  clause may say what a marker's fill means or what an axis value of 1 means.
- **Never in a caption**: the study design, the sample build, model details beyond "adjusted for"
  one clause, sample sizes already printed in the picture, findings, takeaways, caveats and
  "associations, not causal" (those belong to Methods, Results and Limitations).
- Count the words before every review round; an over-length caption is a journal-ready finding.
  Venue limits win when the venue states them (haipipe-paper-venue).

## The colour rule

- **One colour scheme for the whole paper (or report).** It is one small file the recipes read
  (`colour-scheme.yaml`: a thing, its hex code, what it means); a recipe never types its own hex
  codes. A paper keeps it once per version (haipipe-paper-evidence says where).
- **The same thing gets the same colour in every display**, and **a colour never means two things**:
  the colour of one source or company is not reused for an outcome category, and an outcome's colour
  is not reused for a group.
- **Tick labels and axis text are black.** Colour marks data, never text.
- Colour is expected, not optional: a black-and-white figure is a review finding. The key contrast
  still survives grayscale (position, shape, weight or a direct label carry it too), so colour is
  never the only channel.

## The naming rule

The unit folder name says what the reader sees and which question it answers:
`Display<n>-<paper label>-<question id>-<answer in words>`, for example
`Display2-figure1-rq1-names-match-request`. A name that tells the method or the hoped-for theme
(`agreement-between-agents` over an odds-ratio table) is a defect. Rename the folder when the
display's job changes, and sweep every place that cites the old name in the same pass.

## The reviewer brief (paste into a fresh agent)

Make a review packet first: a new empty folder outside the project, one subfolder per unit named as
the unit, holding only a copy of its `preview.pdf` and `assets/figure.png` (when it has one). Give
the reviewer the packet path, so it can not wander into recipes or the paper. Fill `{units}` with one
line per display, in reading order: its number in the paper, its folder name and its packet path.
Fill `{venue}` with the journal or the reader (for example "a general medical journal").

```text
You are a blind reviewer of the displays (figures and tables) of one paper for {venue}.
You never saw how they were made. Read ONLY the files listed below: each display's
preview.pdf and, when present, figure.png. Do not open scripts, READMEs, data, or any
other file, and do not search the disk.

Displays, in the order a reader meets them:
{units}

For EACH display, in order:
1. Before reading its caption, look at the picture and write the question it seems to
   answer, in your own words (one line).
2. Now read the caption. Write the 10-second takeaway a busy reader would leave with.
   Say whether it matches your question in step 1.
3. List concrete problems, each as: element · where · what is wrong. (For example:
   "legend · top right of panel B · covers the last two bars".) Cover colour (one
   scheme? the same thing the same colour? a colour meaning two things? text in colour?),
   labels, scales, denominators, confidence intervals, panel structure, caption length
   (a title of 10 to 15 words; a figure legend of at most 75 words that only defines what
   is drawn), and anything a journal would send back.
4. Score each from 0 to 10 on one line, exactly in this form:
   scores: question N · readability N · honesty N · journal-ready N · overall N
   question = it answers one clear question, and the caption says which;
   readability = a reader gets it in 10 seconds without the text;
   honesty = scales, denominators, intervals and comparisons are fair, and no
   structural artefact (a floor, a ceiling, a forced zero) is shown as a finding;
   journal-ready = it could go to {venue} as it is.
5. Name the 1 to 3 changes that would raise the overall score most, each concrete
   enough to code (what to change, where, to what).

Then a CROSS-DISPLAY verdict:
- Do the displays tell one story in order, with no gap a reader would trip on?
- Does any display repeat another (name both, and say which to cut or change)?
- Is the colour consistent across displays (the same thing the same colour, no colour
  with two meanings)?

Format: one "### <folder name>" block per display (steps 1 to 5), then
"### Cross-display verdict". Be specific and blunt; do not praise.
```

## The review record

Each round is kept in each unit as `review/rNN.md` (r01, r02, ...; the unit's own count of rounds).
The reviewer's words are copied verbatim, never edited or summarised:

```text
# <unit folder name> · review r02

round: r02
date: 2026-10-22                         from the clock
reviewer: fresh agent, never saw the making; read only preview.pdf and figure.png
result: pass                             pass | open, by the pass rule, from the scores line

<the reviewer's "### <folder name>" block for this unit, verbatim, including its
 scores: question N · readability N · honesty N · journal-ready N · overall N line>

<the reviewer's "### Cross-display verdict", verbatim>
```

The README carries one line for the latest round:

```text
question: <the one question this display answers>?
review: r02 · 8.5/10 · pass              latest round · overall · pass | open
```

A checker reads the `scores:` line of the latest `review/rNN.md` and applies the pass rule itself;
the `result:` and `review:` words are for a person scanning the folder.

## Who does what

```text
maker (renderer or its caller)   makes, revises, re-renders, writes review/rNN.md from the
                                 reviewer's text and the README review: line; never scores
fresh reviewer (one per round)   reads only the packet; writes the review; never edits
person                           rules after round 4; ticks accepted: after a pass
```
