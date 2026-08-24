Harvest — no sidecar (haipipe-application-evidence, ⑤ INTERPRET)
=============================================================

Application harvest FOLDS INTO the probe ENTRY. There are no sidecar docs and no
harvest lanes — `1-probes/` is the only consumer-side source of truth (`_LOG` aside).

When a QA answer carries a number, a citation, or a display unit the intervention needs:

- Write it in the entry's `### a-executor` — the COPY of the answering QA file's answer —
  in plain words, WITH its anchor inline:

    ### a-executor
    young-male arm click 6.2% vs 3.1% pooled   [→ tasks/…/QA/2-rates.md]

- The anchor is the entry's own `target:` — the answering QA file, already verified
  `answered` + non-superseded by the checker. That IS the fabrication anchor: the
  number's source is one hop away, on disk, checked. No second transcription, no
  per-lane grep, no separate doc.
- Each Q-consumer this entry serves then writes its OWN a-consumer in its stage doc
  (station ②), anchored `[source: PP<NN>]` back to this copy.
- If a question needs a display unit that does not exist yet, REROUTE it to the display
  stage (a request row); do not invent an artifact here.

Rationale: ./CHANGELOG.md. `probe` keeps the
optional harvest-lane fields for other families (`../../../../../probe/haipipe-probe/SKILL.md`);
the application family does not use them.
