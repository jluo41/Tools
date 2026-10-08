Requirement: what a Section is written to, and what it is judged by
=====================================================================

(b16 s13, JL 261007: "for the requirements, we can add the draft evaluation rubric here as well, so we can
understand the rubric here as well.") A Section's Description › Requirement is its own tab. It shows four things
in this order, each read from its one home and copied from none, so a fix in one place shows everywhere.


The four parts
--------------

```text
part   what                                              read from                                       written by
V      the venue's rules for this section kind           draft/records/<stem>-requirement.md, the        haipipe-page cli/requirement.py
       (length, order, required moves, format)           generated V block, from the bound venue's         (it replaces only V)
                                                         division (structure-source · structure-division)
W      the Page's own writing rules                      the same file, the authored W<n> records          a person or a writing Run;
       (Rule · Applies · Source)                                                                             kept verbatim on regeneration
R      the rubric the draft is judged by: Mechanics ·    1_base/writing/haipipe-writing/ref/               the writing skill (base-v1)
       Function · Evidence · Readability                 evaluation-rubric.md
SUB    the submission rows for this section kind         haipipe-paper/ref/submission-readiness.md        haipipe-paper (G4)
       (SUB-INTRO-*, SUB-METHOD-*, SUB-RESULT-*,         (the rows whose Owner names this kind's
       SUB-DISC-*), judged at submission                  Page CHECK)
```

The venue's own call (`venues/<venue>/call.md`, haipipe-paper-venue) feeds V through the bound division; it is
not shown twice. `SUB-COVER-*` and `SUB-WHOLE-*` belong to the version's build, not to a Section.


How it is used
--------------

1. **Before writing** (CONTEXT, OUTLINE): V and W say what the Section must obey; a structure that breaks a V rule
   names the deviation on its Narrative row, where the target decision lives.
2. **While writing** (CONTENT): every W rule applies to every paragraph it names; the writing Run reads them, it
   does not restate them in the draft.
3. **When judged** (Page CHECK): the four rubric axes are the questions the check asks of the built Section, each
   finding located in the prose; the rubric gives no numeric score.
4. **At submission** (G4): the Section's SUB rows are checked on its current built version and recorded with the
   version's Check (Delivery › checks); a failing hard row keeps the build DRAFT.

The workbench reads the SUB rows straight from `submission-readiness.md` (`paper_theme._sub_rows`), so this file
and that table never drift.
