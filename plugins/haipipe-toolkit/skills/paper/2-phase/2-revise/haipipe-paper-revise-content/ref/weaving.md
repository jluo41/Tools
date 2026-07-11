Weaving — the paragraph-flow pass (merged from haipipe-paper-revise-weaving)
==============================================================================

Merged 2026-07-07 (JL: "maybe just go into Content"). The retired standalone
skill carried its own orchestration layer (routing, approval gates, embedded
%%@ plan blocks) — that apparatus contradicted DPRC's fully-automatic REVISE
and duplicated the hub's job, so it was archived (paper/_archive/
paper-revise-weaving-skill/). What survives here is the diagnostic method.
Full rule sheet: ./write-principles.md · worked example: ./example-intro-logic-flow.txt

The weave step (runs inside the content pass, after paragraph, before sentence)
--------------------------------------------------------------------------------

Diagnose the section's paragraph-to-paragraph flow, then fix directly and
leave `%% {CC-content}: <why>` comments (DPRC-automatic — no gates, no
embedded plan blocks, no waiting).

1. **ARC** — write the section's one-line arc from the paragraph banners
   (`grep '^% Para '`): does the sequence of points tell the section's story
   in the right order? Wrong order / broken logic / a paragraph whose point
   repeats another's = 🔴 fix first.
2. **HINGES** — read each Pn→Pn+1 seam: does Pn+1's opening pick up something
   Pn put down (word, result, tension)? A seam the reader must jump = add or
   sharpen the hinge sentence; never glue with bare connectives
   (Furthermore/Moreover), use content linkage.
3. **RHYTHM** — paragraph lengths and role variety across the section: three
   report-paragraphs in a row with no interpretation beat = re-anchor or merge.

Severity discipline (from the retired skill's diagnose step — keep it):

```
🔴  broken logic, cross-paragraph redundancy, wrong order   → fix before anything else
🟡  compression / re-anchoring needed, role still valid     → fix in place
🟢  leave alone                                             → do not touch
```

Role vocabulary for arc mapping (use consistently within one section):

```
📖 opener      📌 topic/anchor    🎯 motivation/setup   📊 method-and-result
📐 stat test   💡 interpretation  🧭 mechanism          🔁 robustness
🔗 hinge       ⚠️ caveat          🔮 future-work        ✅ closer
```

Boundaries (unchanged from the content worker's contract)
-----------------------------------------------------------

- Weave fixes MOVE and RESTITCH prose; they never change what a paragraph
  claims (that is the paragraph step) and never invent numbers/citations
  (flag `{VAL:?}` / `\cite{TOADD}` instead).
- Banners and Pn.Sn ids are preserved through moves; renumber mechanically
  after splits/merges (../../REF/sentence-format.md).
- prose-quality.md rules apply throughout (no em-dash, one idea per sentence).
