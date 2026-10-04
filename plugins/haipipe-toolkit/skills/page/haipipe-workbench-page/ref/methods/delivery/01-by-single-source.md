By single source
================

One delivery method card. The Page workbench shows it in the shared Guide › Method,
under Delivery methods; its papers are the rows of `../../page-papers.md` whose
`group` is `by single source`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Delivery: How does it reach the reader, checked?
move: Keep one source, the Page's Markdown, and build every delivery from it: web page,
  LaTeX and Word; a fix goes in the source, never in a built file.
comes from: MacFarlane n.d., Pandoc; Allaire et al. 2022, Quarto
reads: the Page's Markdown · its bound values
returns: delivery/ web page, LaTeX and Word
test now: T5 builds
test in use: T5 builds


What the literature says
------------------------

rationale: One markup source can be converted to HTML, LaTeX and Word [MacFarlane n.d.],
  and a scientific publishing system built on that conversion keeps one source for every
  format [Allaire 2022].
context: Document conversion and open scientific publishing [MacFarlane n.d.; Allaire
  2022].
steps: 1. Write the Page once. 2. Build each format from it. 3. Change the source to fix
  a fault and rebuild.
strengths: Every format says the same thing because none is edited apart from the source
  (ours).
limitations: A format's own needs (a journal's LaTeX class, a Word template) still need
  their own settings (ours).


Applied to AI
-------------

agent: A writing agent rebuilds the deliveries; it never edits a built file.
steps: 1. Build. 2. Read the build log. 3. Route a fault back to the Page's source.
returns: delivery/<lane>/ files and their build log.
verify: The one source builds every lane without hand edits (T5).
risk: A quick fix in a built file is lost at the next build and hides the fault (ours).
evidence on ai: No study tests agent-run single-source builds (ours).
skill: haipipe-page-delivery
