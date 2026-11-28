# 🔤 Sentence ids and renumbering

- **Lowercase s** · `be94d2606`
  - Every writer writes `s1`, `C1.P2.s3`; an older `S1` reads as the same sentence everywhere.
  - JL: "make them to be small s for all"
- **One id once per Draft** · `be94d2606`, `1e8be4f06`
  - Renumber goes by position when a Draft restarts at s1 in every paragraph; the health check fails a repeat.
- **Ranges follow their paragraph** · 11-15
  - Headings and Structure Overview ranges ("→ s21 to s26") are rebuilt from the sentences the paragraph holds.
  - An Abstract's title keeps s0.
- **A converter, not yet run on any paper** · `page.py sentence-case <draft> --records --dry-run`
