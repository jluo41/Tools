Harvest — no sidecar (haipipe-application-probe, ⑤ INTERPRET)
=============================================================

2026-07-18: application harvest FOLDS INTO the probe SECTION. There are NO
`_VALUES_` / `_CITATION_` / `_DISPLAY_` / `_DESCRIPTIONS/` sidecar docs, and no
`values:` / `sources:` / `displays:` lanes.

When a QA answer carries a number, a citation, or a display unit the intervention needs:

- Write it in the section's `a-consumer:`, in plain words, WITH its anchor inline:
    a-consumer: |
      young-male arm click 6.2% vs 3.1% pooled   [→ tasks/…/QA/2-rates.md]
- The anchor is the section's own `target:` — the answering QA file, already verified
  `answered` + non-superseded by the checker (PASS 1 R19/R20). That IS the fabrication
  anchor: the number's source is one hop away, on disk, checked. No second transcription,
  no per-lane grep, no separate doc.
- If a question needs a display unit that does not exist yet, REROUTE it to the display
  stage (a request row); do not invent an artifact here.

Rationale + the retired lane machinery: ./CHANGELOG.md. The constitution keeps the
optional harvest-lane fields for other families (`../../../../probe/haipipe-probe/SKILL.md`);
the application family does not use them.
