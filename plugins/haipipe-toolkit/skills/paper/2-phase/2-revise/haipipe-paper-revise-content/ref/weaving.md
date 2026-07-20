Weaving — the paragraph-flow pass
==================================

The diagnostic method for ¶-to-¶ arc, hinges, and rhythm. Loaded by
`haipipe-paper-revise-content`, which owns the weave step; this file carries no
orchestration of its own — routing and gates belong to the hub.
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

Severity discipline:

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
