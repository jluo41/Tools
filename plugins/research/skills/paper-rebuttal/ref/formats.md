Rebuttal Formats — Venue Reference
====================================

This file covers common rebuttal formats across ML conferences and journals.
Check the specific venue's author instructions before writing.

---

Common Patterns
================

All venues share:
  - Author responds to reviewer concerns
  - Revised paper may be uploaded
  - Area Chair / Editor reads everything
  - Anonymity must be preserved in responses

Key differences:
  - Per-reviewer vs shared response
  - Character / word / page limits
  - Number of discussion rounds
  - Whether reviewers can update scores

---

Per-Reviewer Response (ICML, ICLR, AAAI, EMNLP, ACL)
=======================================================

  - Separate response to each reviewer
  - Each response limited (typically 5000 chars)
  - No shared/common response section
  - Each response must be self-contained
  - Cannot reference other reviewer responses

  ICML:    5000 chars per reviewer, 3 rounds (response/follow-up/follow-up)
  ICLR:    unlimited chars, ongoing discussion thread
  AAAI:    varies by year, check author instructions
  EMNLP:   typically per-reviewer, check specific year
  ACL:     typically per-reviewer, check specific year

Shared + Per-Reviewer Response (NeurIPS, some workshops)
=========================================================

  - One shared "general response" visible to all reviewers
  - Plus per-reviewer individual responses
  - Shared response handles cross-cutting concerns
  - Per-reviewer responses handle unique points

  NeurIPS: shared response + per-reviewer, various char limits

Journal Rebuttals (JMLR, TMLR, Nature, etc.)
==============================================

  - Typically one response letter addressing all reviewers
  - No strict character limit (but brevity valued)
  - Point-by-point format with quoted reviewer text
  - May require marked-up revised manuscript
  - Multiple revision rounds possible

---

Character Counting
===================

OpenReview counts characters including markdown formatting.

  A markdown table row ≈ 80-100 chars
  A paragraph (3-4 sentences) ≈ 300-500 chars
  A URL ≈ 60-100 chars
  Opening + closing ≈ 200-400 chars

  Budget planning for 5000 chars:
    ~800 words ≈ ~40 lines of prose
    With 2 tables: ~1200 chars for tables, ~3800 for prose
    With 4 tables: ~2400 chars for tables, ~2600 for prose

  Measure with: wc -c (count the rebuttal section only)

---

Anonymity
==========

  - Responses must not reveal author identity
  - No non-anonymized URLs (use anonymous.4open.science for GitHub)
  - No personal website URLs or shortened URLs
  - Institution names, project names, author names must be avoided
  - GitHub repos: make private, wrap with anonymous.4open.science

---

Strategy by Reviewer Type
==========================

  Supporter (score >= threshold):
    Brief, grateful. Show their concerns are addressed.
    Don't overload — respect their time.

  Flip target (weak reject, moderate confidence):
    Primary focus. Address their top 1-2 concerns with data.
    Frame new experiments as motivated by their feedback.

  Confident skeptic (reject, high confidence):
    Be precise and technical. Don't try to charm.
    Answer exactly what they asked, nothing more.
    Goal: neutralize, prevent them from arguing against acceptance.

  The AC reads all responses. Consistency matters.
