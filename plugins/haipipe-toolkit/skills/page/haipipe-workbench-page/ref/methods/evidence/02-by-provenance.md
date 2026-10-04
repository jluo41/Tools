By provenance
=============

One evidence method card. The Page workbench shows it in the shared Guide › Method,
under Evidence methods; its papers are the rows of `../../page-papers.md` whose
`group` is `by provenance`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Evidence: Where does each number come from?
move: Keep with every Evidence Item the record of what made it: which Run, which Result,
  by whom and when.
comes from: Moreau & Missier 2013, PROV-DM; Groth et al. 2010, nanopublication
reads: Run receipts · runtime.yaml
returns: an Evidence Item that names its Run, Result and receipt
test now: T2 bound
test in use: T3 fresh


What the literature says
------------------------

rationale: Provenance is described by entities, the activities that generate them and
  the agents responsible, linked by derivation [Moreau 2013]; a single statement can be
  published with its context and provenance so it can be cited and checked on its own
  [Groth 2010].
context: The W3C data model for provenance on the web [Moreau 2013]; publishing
  scientific statements as small citable units [Groth 2010].
steps: 1. Record the Run that generated the Result. 2. Record the agent that ran it. 3.
  Record the Result's path and receipt. 4. Keep the record with the item, not in the
  prose.
strengths: A reader can follow any number back to the Run that made it (ours).
limitations: The record says where a value came from, not that it is correct (ours).


Applied to AI
-------------

agent: The Run's Ticket writes its receipt; the evidence agent copies only its path into
  the item.
steps: 1. Read the Result's runtime.yaml. 2. Write the Run id and Result path into the
  item. 3. Leave the receipt where the Run wrote it.
returns: the item's Supporting Run and Local Run lines.
verify: Every item's Run and Result exist on disk (T2).
risk: An agent could copy a receipt by hand; only the Run's Ticket writes it (ours).
evidence on ai: No study tests provenance kept by agents for Pages (ours).
skill: haipipe-page-evidence
