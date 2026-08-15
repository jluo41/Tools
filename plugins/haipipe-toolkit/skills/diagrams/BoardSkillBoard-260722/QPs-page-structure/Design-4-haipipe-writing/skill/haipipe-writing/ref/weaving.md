Weaving: the paragraph-flow pass
==================================

The diagnostic method for paragraph-to-paragraph arc, hinges, and rhythm.

Migrated 2026-08-01 from `haipipe-paper-revise-content/ref/`. It moved because
the method is prose craft and nothing in it is academic: a run of paragraphs has
an arc, a seam, and a rhythm whether it sits in a manuscript, a board page, or a
README. Its CALLERS stay where they are, and they keep their own recording
grammar: `haipipe-paper-revise-content` writes `%% {CC-content}:` into LaTeX,
`haipipe-writing` writes `> ✎` records via `cli/wdiff.py`.

This file carries no orchestration. When the pass runs, and what it may touch,
belong to whichever hub loaded it.
Paper-side rule sheet: `haipipe-paper-revise-content/ref/write-principles.md`

The weave step (runs inside the content pass, after paragraph, before sentence)
--------------------------------------------------------------------------------

Diagnose the section's paragraph-to-paragraph flow, then fix directly and
record each change in the host's own grammar (`%% {CC-content}:` on the paper
side, `> ✎` on the board side). No gates and no waiting: the pass is automatic.

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
- Any ids the host uses (paper banners and `Pn.Sn`, board `C.H.P.S`) are
  preserved through moves and renumbered mechanically after a split or merge.
- `plain-rules.md` applies throughout: no em-dash, one idea per sentence.
