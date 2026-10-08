Narrative: what the story says, how it is drawn, how it is told, whether it attracts
=====================================================================================

(b16 s11, JL 261007: "for the spine and design, they should be merged with one thing, Narrative. Like how do
we want to tell the story here? Will this story attract the editor or reviewer or public.") The Board's
Audience Report › Narrative is one view, read top to bottom in four parts. It replaces the Spine and Design
views and the Board-level Section Narrative view; it writes nothing new, it gathers what the telling already
holds and adds one review.


The four parts
--------------

```text
N1  says      the telling's seed (§1 Identity, §2 Pitch, §4 Stakes) from its studio topic face, then each
              research question with its hypothesis and claim, from the Board Questions it feeds
N2  drawn     the telling's design drawing, view only, from its studio topic (the Idea Studio)
N3  told      the Sections in reading order, each with the claim it carries, from the current version
              face's ## Narrative
N4  attracts  one row per reader: what that reader looks for, where the telling answers it, and the
              verdict of the audience review
```

N1 to N3 are read from where the parts live (`../SKILL.md` § Where a Story lives on the ladder); the view never
copies them. A part with nothing behind it says so ("No telling yet", "no drawing yet").


N4 · the audience review
------------------------

```text
reader     looks for                                              answered by the telling's
editor     fit, and a contribution worth the pages, in one        Identity · Pitch
           sentence
reviewer   claims backed by evidence, honest about their limits   Research Questions · Evidence Basis
public     why it matters, and what to take away                  Stakes · Pitch
```

The review is a judging Run, `run-review-audience-<who>` (`haipipe-paper-workflow/ref/run-cards.md`, button
"Review for an audience"), done in a fresh context by an agent that wrote nothing of the telling
(`haipipe-board-reviewer-agent`). It reads the telling as that reader would, with `haipipe-journal-fit` for the
editor and `haipipe-nature-paper-review` for the reviewer, and records each verdict as a narrative Question in
`board.md ## Questions` (`group: narrative`) with its report: the verdict first, then what the reader would stop
at, then what to change. A row with no report says "No report yet: run Review for an audience".

A verdict never edits the telling. What it asks for is a Story revise (`run-revise-story-<telling>`) the person
chooses to start; a verdict a reader would raise again becomes a Board Question of its own.
