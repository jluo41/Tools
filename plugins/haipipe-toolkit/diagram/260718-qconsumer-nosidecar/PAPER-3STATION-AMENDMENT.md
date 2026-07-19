Cross-family note — the answer's THREE STATIONS (paper side, 2026-07-18)
=======================================================================

FROM: the paper-family session (JL co-design). TO: whoever resumes the application-family `qconsumer-nosidecar` work.

WHY THIS NOTE: your D2 dropped the stage-doc `Answer:` field ("the stage-doc Q-consumer holds only the QUESTION + a POINTER; the ANSWER lives in the probe file's a-consumer"). JL has since ruled the OTHER way for consistency: the answer is SELF-CONTAINED in the stage doc too. The shared **probe constitution has been amended** to document a THREE-station model — so paper and application must both follow it.

WHAT CHANGED (constitution `skills/probe/haipipe-probe/SKILL.md`, v9.0.0 → 9.1.0):
- New section **"The answer's three stations"**. An answer lands in three places, each a more integrated FORM of the same fact, each ANCHORED to the one before:
  - **① probe file** — `a-consumer:`, bound to the `target:` QA file (evidence / provenance). [you already have this]
  - **② Q-consumer `Answer:`** in the stage doc, carrying a `[source: PPnn]` anchor — the answer recorded next to its question, so the stage doc is a self-contained Q&A + review checkpoint. [you DROPPED this — re-add it]
  - **③ stage content** — the answer woven into the sentence(s) that cite `[Q<n>]`, citation discharged. [REVISE]
- The old line "the stage doc keeps only the human question + the pointer / never copied back" is REPLACED: station ② IS a copy-back, but ANCHORED (never a free-typed number; the `[source:]` anchor points at ①, which points at the QA file). That handles the fabrication worry without deleting the field.

ACTION FOR APPLICATION:
- Re-add station ② to the application stage-doc Q-consumer: an `Answer:` field carrying `[source: PPnn]`, filled at PROBE beside the probe-file a-consumer.
- Your NO-SIDECAR decision (D6) is compatible and NOT reversed — sidecars stay retired; ② is a single anchored `Answer:` line in the Q-consumer, not a `_VALUES_`/`_CITATION_` doc. The harvest still lands inline; it just ALSO surfaces in the stage doc's `Answer:`.
- Field labels: paper currently uses `Description` / `Reason` / `Answer`; application uses `Ask` / `Why`. Harmonize to one set in a joint pass (open — token full-vs-abbrev also still open: paper `Q-Narrative-1` vs application `Q-Narr-1`).

PAPER SIDE STATUS: constitution amended; paper templates already carry the anchored `Answer:` (resource/claims/venue/pitch had `[source: PPnn]`; seed normalized); charter `TEMPLATES.md` C5 points at the constitution's three-station section.
