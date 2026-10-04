By bound value
==============

One evidence method card. The Page workbench shows it in the shared Guide › Method,
under Evidence methods; its papers are the rows of `../../page-papers.md` whose
`group` is `by bound value`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Evidence: Where does each number come from?
move: Every number, citation and figure on the Page is bound to the Result that holds it
  and rewritten from it, never typed in.
comes from: Knuth 1984, literate programming; Gentleman & Temple Lang 2007, dynamic
  documents
reads: the plan's Evidence Items · Run Results
returns: each sentence's value, citation or display line, from its Result
test now: T2 bound · T3 fresh
test in use: T3 fresh


What the literature says
------------------------

rationale: A program and its explanation can be written as one source for people to read
  [Knuth 1984]; a document whose figures and tables are recomputed from the code and
  data it carries keeps its results and its text together [Gentleman 2007].
context: Programming as literature [Knuth 1984]; statistical analysis and reproducible
  research [Gentleman 2007].
steps: 1. Name each Evidence Item in the plan with what it needs. 2. Bind it to one
  Result. 3. Rewrite the value line from the Result. 4. Flag the Page when the Result is
  newer than its reading.
strengths: A value on the Page cannot drift from its Result unnoticed: the freshness
  check names the stale one (ours).
limitations: A bound value is only as right as its Run; binding checks where the value
  came from, not whether the Run was right (ours).


Applied to AI
-------------

agent: An evidence agent lands each Evidence Item: it validates the Result and binds it;
  it never writes prose.
steps: 1. Read the item's need. 2. Find or commission the Run. 3. Bind its Result. 4.
  Embed the value line under its sentence.
returns: draft/<stem>-evidence-items.md and the Page's value, citation and display
  lines.
verify: Every value names its Result (T2) and no Result is newer than results-read (T3).
risk: A model asked for a number may produce a plausible one; a value that names no
  Result is refused (ours).
evidence on ai: No study tests agent-bound values on Pages (ours).
skill: haipipe-page-evidence
