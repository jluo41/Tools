---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: section-edit
order: "5"
title: Section Edit
one_line: "Write ONE section as real, venue-quality prose."
board_family: "Main or Appendix, according to section_kind"
board_unit: "reader-order section number or appendix letter"

phases: [draft, probe, revise, check]

# The phase list above runs once PER SECTION, not once for the paper. Display
# qualifies by the same independent-gate rule, but its contract migration is separate.
# `$2` is the unit, not the paper dir.
gates: [check]             # THE HUMAN GATES THIS STAGE OPENS, declared like `phases:`.
                           # Default is ONE, at CHECK. DRAFT/PROBE/REVISE run unattended.
                           # This is safe only because PROBE cannot spend: see probe_depth.
probe_depth: 0             # THE CEILING on what PROBE may dispatch, on the bank's own ladder
                           # (task/haipipe-task/fn/qa.md:102-107), which maps 1:1 onto the
                           # consumer's `bank:` verdict:
                           #   0 READ        reuse  results already answer it   free, nothing runs
                           #   1 NEW RUN     run    old script, new config      costs
                           #   2 NEW SCRIPT  code   must write new code         costs
                           #   3 NEW FOLDER  new    open a new task-folder      costs most
                           # Rule: dispatch when depth(bank) <= probe_depth, else DEFER.
                           # At 0 the stage can only HARVEST, so a run of it is free and needs
                           # no gate. Raise it per invocation with `probe --depth N`.
runs: per-unit
unit: section
units_from: 0-lifecycle/2-venue/S-Venue-2-narrative.md
             # FALLBACK, for papers that predate the narrative stage: if that file is
             # absent, the unit list is the folders already scaffolded under
             # 0-lifecycle/4-main/ (excluding z-structure/, which is the
             # architecture doc, not a manuscript section). Say which source you used.

# ⚠️ ARGUMENT ORDER CHANGES on cutover — the section is no longer positional 1:
#      old: /haipipe-paper-section-edit <section> <phase> [paper-path]
#      new: /haipipe-paper-stage section-edit <section> <phase> [paper-path]
#    Stage name is always positional 1 under the router; the section slides to 2.
argument_hint: "<section> [draft|probe|revise|check] [paper-path]"

needs_paper: true
venue_aligned: true       # rewritten on retarget to another journal

artifact: 0-lifecycle/4-main/S-{board_family}-{board_unit}-{board_slug}.md
                          # PER SECTION — one folder per unit. `{section}` is the unit's folder;
                          # the FILENAME is resolved by haipipe-board/stage.py from this unit's
                          # family, unit and slug (QC2), never spelled by this stage. `board_family`
                          # and `board_unit` are per-unit here, not per-stage: a unit's kind decides
                          # Main vs Appendix and its reader order decides the number or letter.
probes: 1-probes/PPNN_<topic>/
output: sections/*.tex   # GENERATED from the .md by sync; NEVER hand-authored
template: <resolved per (venue, section_kind)>
          # PRINCIPLE (JL 2026-07-20): every (venue, kind) has its OWN template, summarized from
          # that outlet's exemplars — a MISQ introduction ≠ a Nature introduction in SHAPE. So the
          # skeleton is NOT fixed here. The venue stage resolved it into S-Venue-0-venue.md's Section
          # Styles table (the `template:` path for this section's kind). Read THAT and copy it.
          #   venue has a pack template for this kind  -> use it (authoritative)
          #   pack exists but no template.md for this kind, OR a pack-less venue (grant/patent/
          #     NEJM…)                                  -> fall back to ./template.md (generic)
          # The generic ./template.md below is the FALLBACK, not the default — its own header
          # says so. Never hand-spell a pack path; the venue stage owns resolution.
fallback_template: template.md     # generic scaffold — placeholder grammar, the
                          # mandatory Q-consumer block and its fill rules all live inline
                          # as <tpl: …> guidance. There is no separate format spec.

read_order:               # optional DRAFT craft order; dependencies live on the Board page
  venue:         0-lifecycle/2-venue/S-Venue-0-venue.md                        # blueprint + writing principles
  narrative:     0-lifecycle/2-venue/S-Venue-2-narrative.md                  # the story beats
  claims:        0-lifecycle/1-work/S-Work-1-claims.md                      # what this section must support
  existing_tex:  sections/{NN}_{section}.tex                           # only if prose already exists

venue_contract: 0-lifecycle/2-venue/S-Venue-0-venue.md
venue_read_first:         # DRAFT opens these BEFORE writing a sentence
  - "Structural Blueprint, THIS section's block — BINDING: subsections, ¶ per subsection,
     sentences per ¶, citation density, word budget, display limits"
  - "Writing Principles — advisory"
section_kind: <one of the closed set in ../section-kinds.yml>
                                   # THIS section's kind: abstract · introduction · theory ·
                                   # related-work · methods · results · discussion · appendix ·
                                   # letter · significance. Which kinds EXIST is per-outlet —
                                   # section-kinds.yml records that, measured, per journal.

venue_style_pack: |                # READ IT, do not resolve it.
  The VENUE stage already resolved every section style path and wrote them into
  S-Venue-0-venue.md's `Section Styles` table, one record line per kind. Read the row for this
  section's `section_kind:` and use the path it gives.
  · row is a path            -> that IS the deep-dive pack; REFERENCE ONLY, never binding
  · row reads blueprint-only -> this outlet has no guide for this kind; the S-Venue-0-venue.md
                                Structural Blueprint block alone is sufficient to draft
  · table or row is MISSING  -> the venue stage has not been run (or is stale): say so and
                                stop; do NOT glob the venue dir yourself
  ⛔ Never find(1) the venue directory, never glob a pack path, never spell a per-journal
     slug. Six outlets use slugs no consumer can derive (jno · diabcare · npjdm · natcomm ·
     MS-IS · MS-Marketing); that knowledge lives in ONE place, upstream.
venue_fallback: "venue/ packs directly, only when S-Venue-0-venue.md is absent"

exit_when: "writing exposes missing evidence -> 1-claims"

sections:                 # the .md's four parts, top to bottom
  - Title + venue header
  - Structure overview
  - Paragraph blocks
  - Q-consumer                          # the mandatory last block

prose_rule: |
  The .md holds REAL prose — complete academic sentences the user can read as a paper, one
  sentence per line, blank line between (these become the Pn.Sn markers, which live only in
  tex). \citep{key} ONLY for a key that already greps in the paper's .bib; an unverified number
  is {VAL:? <what>} [Q-<Stage>-<n>]; a citation slot with no key is \cite{TOADD} [Q-<Stage>-<n>].
  Placeholder and bracket sit SIDE BY SIDE, never fused — a placeholder with no bracket is a
  hole no question will ever fill. Never invent a key or a number to avoid a placeholder.
  The .bib is human-only; the agent learns a key by grepping it after the human adds it.

formatting:
  headings: "## for subsections · ### for paragraphs · ## per Q-consumer entry"
  line_breaks: "one sentence per line, blank line between; never prefix a sentence with S1./S2."
  preview: "one short line per paragraph (~80-120 chars) — a scan hook, not a mini-abstract"
  latex: "citation commands are the ONLY LaTeX allowed in the .md; no %% markers"
  tables: "bullet lines, never markdown tables, anywhere in the Q-consumer block"
  template_residue: "grep -c '<tpl' {section}.md must print 0"

displays: file-only       # JL ruling: this stage FILES a display request, it never CREATES one
display_request: 0-lifecycle/3-display/_DISPLAY_REQUEST.md   # a DR row goes here; the units
                          # themselves come from displays/ and 0-lifecycle/3-display/
display_split: |          # BINDING, owned by ../4-display/stage.md (`display_split:`) — read it there.
  A DR row filed from here names BOTH halves of the unit, because they have different owners:
    `bank deliverable:`     the numbers — source_data.csv + provenance, produced by the TASK
                            layer (haipipe-task-for-display); a paper stage never authors them.
    `consumer deliverable:` the framing — which rows/columns the argument needs — plus venue
                            formatting and \label/\ref wiring; rendered FROM that source_data.csv.
  A DR naming only one half is incomplete. Hand-typing numbers into a unit's .tex is a DEFECT:
  it is how a display silently drifts out of agreement with the prose it supports.
display_gate: "the section's display axis cannot pass CHECK until the DR row is `done` and the
               unit is linked"

q_id_pattern: "## Q-Section-<n> · <title>"   # unified across all 8 stages: the heading id
                                            # and the inline anchor are THE SAME TOKEN
q_anchor: "[Q-Section-<n>] beside the {VAL:?} or \\cite{TOADD} it will fill; the entry's
           Reason names the §<N> P<x>.S<y> sentence(s) that raised it — the back-link"
closed_when: "PROBE writes the Answer + the target: QA-file path; CHECK's human
              verifies and the agent THEN places the real \\citep{}/value, retiring the
              placeholder and its bracket together"

done_criteria:
  - "grep -c '<tpl' {section}.md = 0; structure overview matches the paragraph blocks"
  - "every paragraph carries heading + one-line preview + real prose sentences"
  - "no bare {VAL:?} or \\cite{TOADD} — each sits beside its [Q-<Stage>-<n>]; a TOADD that
     survives into compiled tex fails CHECK"
  - "the Q-consumer block is the .md's LAST content, in the unified
     `## Q-Section-<n>` + Description/Reason/Answer shape, followed by Settled Flags and the
     user-owned notes section"
  - "every display need is a DR row that came back `done` with its unit linked"
  - "6-axis CHECK gate PASSes: structure · citation · values · display · venue · proof"
  - "newest [REVISE] carries a `workers:` line and sections/*.tex is synced from the .md"
  - "_LOG entry records the current state"
  - "check-probe-cards.sh <paper_root> --stage section-edit exits 0"

upstream: [narrative, display]
downstream: [round]
handoff: "on CHECK confirm, append the gate row to THIS section's S page ## Log; the stage is not
          finished until every unit from units_from has passed -> round"
---

Section Edit — the craft
========================

Three lanes sweep the draft mechanically: citation, values, display. They find missing TOKENS.
What no lane can find is a missing ARGUMENT — and that is the only reason this stage needs
judgement at all.

The two lenses no lane has
--------------------------

🧩 **Unearned move.** This paragraph makes a step the reader has not been given the ground for.
Every sentence is true, the key is real, the number checks out — and the reader still cannot get
from the previous paragraph to this one. Read each paragraph asking one question: what must the
reader already believe for this to land, and did an earlier sentence give it to them? Fix it by
ADDING the missing ground or DROPPING the step. Never by softening the verb — hedging hides the
gap instead of closing it, and the gap survives into review.

📛 **Norm conflict.** The section-type norm and the venue blueprint disagree here. The blueprint
is BINDING and the playbook is reference, so the blueprint wins on numbers. But record WHY in the
_LOG: a conflict that keeps recurring in the same section is evidence the section is mapped to
the wrong type, and that is a structure problem, not a prose one.

The other two things worth raising are lane OUTPUT, not judgement — an owed number the values
lane already marked `{VAL:?}`, an owed source the citation lane already marked `\cite{TOADD}`.
Raise them only when the lane handed them back UNOWNED, and the only decision left is whether
the number is worth going to get.

The .md and the .tex are not peers
----------------------------------

The `.md` is the paper. The `.tex` is a build product. Prose authored into tex sits outside the
record the user actually reviews, and sync will either overwrite it or silently keep it — both
are failures. Pure LaTeX mechanics (labels, floats, `\input`) do live in tex, and sync preserves
them untouched.

File a display; never draw one
------------------------------

A section that needs a figure or a table writes a DR row into the display stage's inbox and
stops there. This stage has no renderer and never writes to `displays/`. The display stage owns
whether the evidence can carry the picture; section-edit owns only whether the prose needs one.

What DRAFT prose IS — and is NOT
--------------------------------

DRAFT settles **WHAT** each sentence says, in real sentences. REVISE settles **HOW** it sounds.

The `.md` holds REAL paper prose — complete academic sentences the user can read as a paper, not
telegraphic notes and not a skeleton (JL ruling 2026-07-09; this superseded an earlier "lean plan"
model that produced outlines nobody could evaluate as writing).

DRAFT prose is:

```text
NOT verified        that is PROBE — {VAL:?} and \cite{TOADD} stay until traced
NOT venue-polished  that is REVISE — humanizer, sentence economy, weave
NOT LaTeX           that is sync-to-tex, after REVISE
```

Three placeholder forms, and nothing guessed
--------------------------------------------

```text
{VAL:? <what>} [Q-Section-<n>]   a number PROBE must trace to a source, + the question that owes it
\citep{key} / \citet{key}        a REAL citation — the key must ALREADY EXIST in the .bib
\cite{TOADD} [Q-Section-<n>]     a citation slot with no suitable .bib key yet, + its question
```

The placeholder and its anchor bracket are **two markers side by side, never fused**. The bracket
names the question that owes the answer; without it the placeholder is a defect — a hole no
question will ever fill. (JL ruling 2026-07-10; a legacy `[CITE:]` in an old draft reads as
`\cite{TOADD}`.)

- `\citep{key}` — grep the `.bib` FIRST. Writing a key that does not grep is inventing a citation.
- `grep -c TOADD` counts open slots. A `TOADD` surviving into compiled tex FAILS CHECK.
- `{VAL:?}` — the `<what the number is>` text is exactly what PROBE traces.

Citation commands are the ONLY LaTeX allowed in the `.md`; they sync to tex verbatim. No other
markup, no `%%` markers, no agent monologue.

Edit surgically
---------------

Change the specific lines under discussion. A full-file rewrite of a `.md` carrying `> USER:`
comments is forbidden — the rewrite is how threads get silently dropped. The agent never deletes,
rewords, or relocates a `> USER:` comment; it replies underneath with `> CC:`. Only the user
declares a thread resolved, and a resolved thread MOVES to `_LOG` verbatim. Each phase starts from
a clean file.

Backward-fill, once, at scaffold
--------------------------------

When the section ALREADY has prose in `sections/*.tex`, the `.md` is filled FROM it — once:

```text
1  read the tex
2  extract the paragraph structure (% Para [id] banners, or %% ---- Pn.Sn ---- markers)
3  per paragraph: write the heading + preview, then copy the sentences as prose lines —
   one per line, blank-line separated, markers stripped
4  preserve every existing > USER: comment EXACTLY where it was
5  present the populated .md for review
```

This is the ONLY time text flows tex → `.md`. From then on the `.md` is the source and tex is
sync output; a second backward-fill would overwrite authored prose with a build product.
