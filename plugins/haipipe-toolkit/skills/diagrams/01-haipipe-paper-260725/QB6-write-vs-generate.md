# What does a stage write, and what is only generated from it?
state: 🟡 PARTIAL
owner: JL
method: one direction, no exceptions; then say what the rule means for the stages whose output is not prose

## Question
A stage produces a page on the board and, downstream, the manuscript carries LaTeX that says the same things. Which of those two is the paper? The answer has to be one of them, because the moment both are writable there are two manuscripts, only one of them is being reviewed, and the human editing either one cannot tell which they are looking at. That is the oldest failure in this system and it is not a subtle one: whichever copy somebody edits, the other is silently wrong from that instant.

The rule is that the `.md` is the paper and the `.tex` is a build product, generated in one direction and never read back. Prose authored into a `.tex` sits outside the record a human reviews, so sync will either overwrite it or silently keep it, and both of those are defects. Section-edit's own contract already warns that a second backward fill would overwrite authored prose with a build product.

Two things keep it from being settled. The generator's input is a path that no longer exists on the one paper using it, so the rule is true and unexecutable at the same time. And "the `.md` is the paper" is exact only for section-edit: the pitch stage's real output has been a `.tex`, and display's output is a rendered asset plus a float file. For those two the rule needs a second sentence that nobody has written.

## Boundary
- ✅ Covered here
  What a stage authors, what is generated from it, the direction, and the stages whose output is not prose.
- ↪ Covered elsewhere
  What the page is called is `QB4`; what a re-run does to it is `QB5`; the sentence-level shape the extractor relies on is `QC0`; rendering into Word and HTML is `QD7`.

## Diagram
```
   ➡️ ONE DIRECTION, AND ONLY ONE

      S page  ## Content        THE PAPER: authored, reviewed, gated
           │
           │  sync              ✅  .md ──▶ .tex
           ▼                    ⛔  .tex ──▶ .md    NEVER
      sections/*.tex            A BUILD PRODUCT

   ── why it is not negotiable ──────────────────────────────────────
      two writable copies of one prose is the oldest failure here.
      Whichever one a human edits, the other is silently wrong, and
      the human cannot tell which one they are reading.

   ── what sync reads, once the shape contract holds ────────────────
      ### §6.1 <Title>   ──▶  a subsection
      #### P1. <job>     ──▶  a paragraph BREAK; the heading is
                              scaffolding, not prose
      (job line)         ──▶  DROPPED: it describes the paragraph,
                              it is not IN it
      > any lane         ──▶  DROPPED: apparatus, never manuscript
      plain sentences    ──▶  the prose, as authored, one per line

      ⚖️ extraction is MECHANICAL, not interpretive. That is the whole
         design: an interpretive extractor is a second author.

   ── the open edge: artifacts that are not prose ───────────────────
      5-section-edit   .md ──▶ .tex                ✅ exact here
      2b-pitch         output has BEEN a .tex      ⚠️ restate
      4-display        a rendered asset + a float  ⚠️ restate
      "the .md is the paper" needs a SECOND SENTENCE for these two,
      and until it has one the rule quietly does not cover them.

   ── the rule IS a contract field, and only one stage has it ───────
      5-section-edit    output: sections/*.tex
                        # GENERATED from the .md by sync;
                        #   NEVER hand-authored
      ✅ that comment IS this face's Law, declared where a machine
         reads it. It is also the ONLY `output:` in the eight, so the
         law is enforced for the one stage that already obeyed it.
      📍 `sections/` is UNNUMBERED now (QA6's delete test), so a
         generated file ships and its source does not. The direction
         and the delete test agree, which is why both survive.

   ── the state it is in right now ──────────────────────────────────
      the rule    stated in the section-edit contract, with the reason,
                  and declared as `output:`
      the input   a path that no longer exists on the one paper using it
      ⚠️ true and unexecutable at the same time.
```

## Content
### Two copies is the failure, not the format
Nothing here is against LaTeX. The rule is about how many places a sentence can be authored, and the answer has to be one. A `.tex` that is generated is a projection and is safe to delete and rebuild; a `.tex` that somebody typed into is a second manuscript wearing the same name.

That is also why the extractor must be mechanical. An extractor that interprets, that decides what a heading probably meant or smooths a sentence on the way out, is writing prose nobody reviewed, and the output stops being a projection.

### The case that will actually happen
A coauthor edits the Word file or the `.tex` directly. It is not a hypothetical: it is the normal way collaborators work, and the rule as written has nothing to say about it. Either the change is backported into the S page, or the manuscript has crossed into a new authoritative mode and the S page is no longer the paper. Silence is the one answer that is certainly wrong, because silence means both files stay writable and nobody is told which one won.

### Where this rule stops being exact
Section-edit produces prose and the rule fits it perfectly. Pitch has produced a `.tex` as its real output. Display produces a rendered asset plus a float file, and the asset is not authored at all: it is computed. So "the artifact is the `.md`" is a rule about prose stages that has been stated as though it were about every stage.

## Items to Finish
- [x] 📜 One direction only: md to tex
      Stated in the section-edit contract, with the reason.
- [ ] 🧠 Rule what sync reads
      The page's `## Content`, with the extraction rule written into the contract so two implementations cannot disagree.
- [ ] 🔧 Repoint the generator's input
      It reads a path that no longer exists on the one paper using it, so the rule cannot currently be executed.
- [ ] 📐 Restate the rule for non-prose artifacts
      Pitch and display produce things that are not sections. Say what "the artifact" means for each.
- [ ] 🔁 Rule the external edit
      A coauthor edits the `.tex` or the Word file. Backport into the S page, or declare the manuscript has crossed into a new authoritative mode. Silence is the only certainly wrong answer.
- [ ] 🧪 Round-trip one section
      Generate a section's tex from its page and diff against the shipped file. Differences are either rule bugs or drift the tex accumulated. A parity test, not permission to make TeX a second source.

## Where we are
The rule holds, is stated with its reason, and is respected in practice on the MISQ paper. It is also unexecutable: the generator's declared input path does not exist on that paper, so nothing has actually round-tripped.

The prose case is exact. The two non-prose stages are covered by a sentence that was written about prose, which is a gap rather than a decision.

## Files
- `stages/5-section-edit/stage.md`
  Carries the law, the reason, and the dead input path.
- `stages/4-display/stage.md`
  The stage whose artifact is an asset plus a float file.
- `stages/2b-pitch/stage.md`
  The stage whose real output has been a `.tex`.

## Law
The `.md` is the paper. The `.tex` is a build product, generated from it in one direction, and nothing reads back. A compiled artifact may never become the source of a claim, because at that moment two manuscripts exist and only one of them is reviewed.

Extraction is mechanical, not interpretive. An extractor that decides what a heading meant is a second author.

## Log
260726 · Carried from `_archive/QB9-artifact-and-tex.md` and retitled to the fork it actually turns on: what a stage AUTHORS versus what is merely generated. The format-projection half moved out to `QD7`, where Word and HTML already live.
260726 · Aligned against `QA6`, which had moved well past this group. `output: sections/*.tex` in the section-edit contract IS this face's Law declared where a machine reads it, and it is the only `output:` in the eight. `sections/` is unnumbered under the delete test, so the generation direction and the delete test agree.
