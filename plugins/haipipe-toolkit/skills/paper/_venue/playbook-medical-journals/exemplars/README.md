# Exemplars -- Diabetes Care

Real same-venue documents used to imitate STYLE (sentence shapes, section moves, CGM terminology, number formatting). The primary purpose of this playbook is style imitation; citation candidates are secondary (see `references/`).

## Exemplar source

25 Diabetes Care papers (2025-2026) are stored as PDFs in:
```
_WorkSpace/HAIToolLib/1-ExemplarLib/clinical-journals/diabetes-care/
```

## Priority exemplars (read for style extraction)

### RCTs
- `galindo-2026-diabcare-cgm-t2d-hemodialysis.pdf` -- Brief Report, crossover RCT, rtCGM vs CBG in hemodialysis T2D. Compact methods, stacked bar hero display, CGM metrics reporting.
- `bergenstal-2026-diabcare-cgm-profiles-grade-trial.pdf` -- GRADE trial CGM substudy, 4-arm comparison, extensive CGM metric tables.

### Observational / Target Trial Emulation
- `reaven-2026-diabcare-cgm-mortality-t1d-veterans.pdf` -- Large TTE (N=8,423), VHA data, CGM initiation and mortality. Full CONCLUSIONS with named subsections. Best example of discussion structure.
- `godneva-2026-diabcare-time-in-range-normoglycemia.pdf` -- Large cohort (N=7,929), normoglycemia reference ranges. Best example of CGM metric definitions and population-level reporting.
- `ajjan-2026-diabcare-gdac-cgm-hba1c-alignment.pdf` -- Prospective observational, personalized A1C concept. Best example of novel metric introduction.

### ML / AI / NLP
- `lehmann-2026-diabcare-ml-voice-hypoglycemia-detection.pdf` -- Brief Report, ML for hypoglycemia detection. Best example of ML reporting in Diabetes Care (AUROC, feature analysis, speaker-dependent vs independent).
- `zheng-2025-diabcare-nlp-cgm-data-extraction.pdf` -- Original Article, NLP pipeline for CGM data extraction. Best example of pipeline description and accuracy reporting.

### Claims / Administrative data
- `kahkoska-2025-diabcare-claims-algorithm-cgm-uptake.pdf` -- e-Letter, Medicare claims, CGM eligibility algorithm. Best example of e-Letter format (no section headings, no abstract, max 5 references).

### Cost-effectiveness
- `dupenloup-2026-diabcare-cgm-remote-monitoring-pediatric.pdf` -- Original Article, Markov model, CGM with remote monitoring in pediatric T1D. Best example of CHEERS reporting and cost-effectiveness results.

### CGM profiles
- `he-2026-diabcare-glycemic-profiles-cgm-t2d.pdf` -- e-Letter, clustering-based glycemic profiles. Best example of brief observational analysis with clustering methodology.

## How to use exemplars

1. When writing a section, find the nearest exemplar by study design and topic.
2. Read that exemplar's corresponding section to absorb sentence shapes, paragraph structure, and vocabulary.
3. Mirror the style, not the content.
4. Use the per-section style guides in `diabetes-care/diabcare-{section}/style.md` for distilled patterns with source tags.

## Status

- [x] 10 papers read and conventions extracted (June 2026).
- [x] Per-section style guides populated with exemplar sentences and source tags.
- [ ] Additional papers can be added by reading PDFs and tagging patterns in the style guides.
