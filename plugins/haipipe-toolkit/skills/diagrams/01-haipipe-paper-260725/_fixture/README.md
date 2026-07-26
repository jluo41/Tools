# _fixture — a real slice of the MISQ paper, so the design board can SHOW its rules

Not a paper and never rendered as one. It exists so the `QC` faces carry LIVE
examples: the board declares `dialect: paper` with `paper-root: _fixture`, and
every marker in a QC example resolves against the files here.

**Every key, number, probe entry and display asset here is copied VERBATIM from
`examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026`.**
That matters: an example built on made-up keys and made-up coefficients
demonstrates the syntax and proves nothing about the resolver, and a reader
cannot tell a real state from a staged one. Here the reference the panel prints
is the reference that paper will print, and the numbers the chips check are the
numbers that paper cites.

NO PROSE LIVES HERE (JL 260726). The example sentences are written in the QC
pages' own `## Content`; this folder holds only what a marker RESOLVES AGAINST.
The split is the rule: prose on the page, evidence in the fixture. Two of QC0's
six sentences are written rather than lifted, and `QC0`'s own `### Where each
sentence comes from` marks which and why.

To make a new state showable, copy in the REAL entry that already produces it:
a bibtex entry out of that paper's bibliography, a probe entry out of its
`1-probes/`, a display folder out of its `0-displays/`. Never write one. That is
the same human-only boundary `QC1` states, and it is why a chip's colour here
can be trusted to mean what it means on the paper.

    misq-slice.bib     6 real entries, for the keys the examples cite
                       `stock2005testing` is ABSENT here exactly as it is there,
                       so the broken-citation example is a real defect
    misq.bst           the paper's own style, so refs.py renders real references
    1-probes/PP01_seed-feasibility/
      QX1_novelty.md                 real, state `read`, which is why the
                                     paragraph's \cite{TOADD} chip is `owed`
                                     rather than `ready`
    1-probes/PP03_results-values/
      QX1_opioid-reg-estimates.md    real, answered, real coefficients
      QX5_binary-exposure-flags.md   real, answered, real odds ratio
    displays/display02-discretion-gradient/     real figure + its real waiting
                                               candidate  -> ready
    displays/display05-descriptives/            real table                -> ok

It is a FROZEN snapshot and is meant to drift from the paper. It is a fixture,
not a mirror: its job is to hold still so a change in the resolver shows up as a
change on the design board.

Two deliberate omissions. `source/source_data.csv` is not copied, so the figure
reads `ready` rather than the `stale` the live paper currently shows; staleness
is a property of that paper today, not of this design. And no raw CMS data is
here or ever will be: every number in these probe entries is an aggregated
regression output, which is the only kind that may leave the secure server.

Folders starting with `_` are skipped by face discovery, so nothing here becomes
a board page.
