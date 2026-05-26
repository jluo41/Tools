============================================================
 UTD24 IS Venues — discover-stage filter list
============================================================

Purpose: a tiny data file consumed by discover-stage skills
(/research-lit, /idea-creator, /novelty-check) when invoked
with the `— venues: utd24-is` directive. NOT a SKILL.md.

The full UTD24 list is 24 business journals; this file holds
only the **3 IS-track journals**. Writing-stage workflow
already exists in `_workflows/is-paper-workflow/SKILL.md`,
which references the per-venue playbooks below.

------------------------------------------------------------
 Venue list
------------------------------------------------------------

| Key   | Full name                       | Society | Playbook                 | S2 venue strings (any-of match)                   |
| ----- | ------------------------------- | ------- | ------------------------ | ------------------------------------------------- |
| misq  | MIS Quarterly                   | AIS     | 13_venue/misq-playbook/  | "MIS Quarterly", "MISQ", "Mis Quarterly"          |
| isr   | Information Systems Research    | INFORMS | 13_venue/isr-playbook/   | "Information Systems Research", "Inf. Syst. Res." |
| ms-is | Management Science (IS section) | INFORMS | 13_venue/ms-is-playbook/ | "Management Science", "Manag. Sci."               |

> Note on `ms-is`: Management Science is multi-discipline.
> The S2 venue string filter cannot distinguish IS-section
> papers from OM/Marketing/Finance papers. Discover-stage
> skills should accept all MS hits and rely on topic
> keywords (IS, IT, digital, platform, mobile, healthcare-IT)
> for downstream filtering.

------------------------------------------------------------
 Fit summary (used by /idea-creator for ranking)
------------------------------------------------------------

(verbatim from is-paper-workflow Stage 1, kept in sync)

  Signal                                          Lean MISQ  Lean ISR  Lean MS-IS
  ----------------------------------------------- ---------  --------  ----------
  Theory-forward, pluralistic method                 ✓
  Tight hypothetico-deductive, survey/experiment                 ✓
  Causal identification, economics framing                                 ✓
  Design science, IT artifact evaluation              ✓
  Computational methods, large-scale data                        ✓          ✓
  Behavioral theory, organizational IS                ✓          ✓
  Markets, platforms, economic mechanisms                                    ✓

------------------------------------------------------------
 How discover-stage skills should consume this file
------------------------------------------------------------

When `— venues: utd24-is` appears in arguments:

  1. Read this file. Extract the union of S2 venue strings
     across all 3 rows.

  2. /research-lit:
     • Pass venue strings to semantic_scholar_fetch.py via
       `--venue "MIS Quarterly,Information Systems Research,Management Science"`.
     • In the final landscape table, add a "UTD24-IS hit?"
       column (✓ if venue in list, blank otherwise).
     • De-prioritize non-UTD24-IS papers in synthesis unless
       they are foundational/canonical.

  3. /idea-creator:
     • In Phase 2 brainstorm prompt, add a constraint:
       "Each idea must plausibly fit ONE of MISQ / ISR / MS-IS
        per the fit summary above. Annotate each idea with
        target venue + which signal-row it satisfies."
     • In Phase 3 ranking, add a "venue-fit" sub-score (0-3).

  4. /novelty-check:
     • Restrict S2 prior-art search to the venue list first.
     • If <5 prior-art hits, expand to web/arXiv broadly.

------------------------------------------------------------
 Maintenance
------------------------------------------------------------

  • Adding a venue: append a row + S2 strings.
  • Adding a venue group (e.g. utd24-marketing, utd24-om):
    add a sibling file `utd24-marketing-venues.md`. The
    discover-skill directive becomes `— venues: utd24-marketing`.
  • Keep the fit summary table in sync with
    `_workflows/is-paper-workflow/SKILL.md` Stage 1.

============================================================
