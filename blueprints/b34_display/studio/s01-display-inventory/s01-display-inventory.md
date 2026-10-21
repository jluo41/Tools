s01 · Displays as they are: 260 units against six wants
=======================================================

**Stage:** explore

**Topic:** What a display is today, measured on disk on 261016, so JL can decide what display should be. A display
unit is one folder holding one figure or table (`Display<N>-<slug>/`, or any folder whose README has an `accepted:`
line). We walked WellDoc-SPACE, DrFirst-SPACE, Physician-SPACE, REACH-SPACE and Knowledge-SPACE (not `.git`, `.venv`,
`node_modules` or each SPACE's `Tools` link) and found 335 units: 263 named `Display<N>-...` (the "about 260"
of the b34 face), 67 older ones whose name has a section prefix before `Display<N>`, and 5 with another name. We then
scored the six wants from the b34 face (`board.md`, Topic) against the 335 rows. A home is where a unit lives:
a Page Result payload (`results/<run>/payload/<unit>/`), the old display lane (`evidence/display/`, `display/`,
`displays/`), or a delivery copy (`delivery/latex/displays/`).

**Feeds:** `board.md` (the six wants and the Close of b34); no report yet (`reports/` is empty).


Files
-----

```text
s01-display-inventory/
├── s01-display-inventory.md        this face
├── build_s01_display_inventory.py  walks the SPACEs and writes the table
└── inventory.csv                   335 rows, one per unit, relative paths only
```

- `inventory.csv` (this folder): one row per unit; columns below. 👀 Check: the `home`, `kind`, `accepted` columns.
- Columns: space, path, home, archived, kind, has_readme, has_recipe, name_form, has_intake, has_assets,
  has_float_tex, has_preview, names_data_source, has_serves_line, accepted, accepted_value, delivery_copy_of,
  has_delivery_copy, same_name_elsewhere_in_paper, cited_by_page_files, cited_same_paper, cited_in_page_body,
  names_built_on, cited_example.
- How it was made: `build_s01_display_inventory.py` beside this face (about 3 minutes; rerun it to refresh the table). `kind` is read from the
  README `kind:` line, else from `float.tex` (table or includegraphics), else from the assets. 2 rows stay `unknown`.


Findings
--------

**The population.** 335 units.

```text
by SPACE      Physician 208 · DrFirst 102 · WellDoc 24 · REACH 1 · Knowledge 0
by home       old display lane 146 · delivery copy 96 · Page Result payload 93
by kind       table 193 · figure 139 · diagram 1 · unknown 2   (no illustration, no tex)
archived      107 sit under _archive/, _old/ or a legacy folder (87 of them in the old lane)
home x SPACE  DrFirst 32/50/20 · Physician 100/40/68 · WellDoc 14/6/4 · REACH 0/0/1   (lane/delivery/payload)
```

Of the 93 payload units, 23 (Physician 22, REACH 1) live under a work Run (`work/.../runs/<run>/result/units/.../payload/`),
not under a paper Page. So a fourth address already exists.

**The six wants, scored.** Counts are over all 335 rows unless said. "Source units" are the 239 that are not delivery copies.

1. **Reproducible from recipe and data: partly met, 131 of 335.** A unit counts when it has both a `recipe/` folder
   and an `intake/` folder (88 old lane, 43 payload, 0 delivery copies). 165 have a recipe or a legacy `source/`
   folder. 170 have no recipe at all: they are a carried asset (a PDF or `table-body.tex`) with a README saying so.
   Examples: met, `Physician-SPACE/_WorkSpace/paper-preview/Paper-AgreeablePrescriptionDiscretion-260928/Bb-MISQ-Appendix/S-MISQ-Appendix-B-Validation/results/re-display-01_model-performance/payload/Display1-model-performance`;
   absent, `DrFirst-SPACE/examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026/j01_v0429_mansci/t26_regression-robustness/results/run-display-0930-main-effects/payload/Display1-table-main-effects-260516`
   (README: "carried submitted asset, not accepted").

2. **Names the evidence it is built on: mostly absent, 57 of 335 name any data, 0 say `built_on`.** 29 have an
   `intake/manifest.yaml` with an origin (all Physician), 28 have a README `source:` line (all DrFirst), 278 name
   nothing. `built_on` (the field that would point to evidence cards) is in zero units; the field is new. By home,
   payload units do best (42 of 93 name a source), the old lane 15 of 146, delivery copies 0 of 96.
   Example: `Physician-SPACE/examples-3-nlp/Project-LLMRec-Physician/work/b01_physician_ground_truth/j03_physician_directory_pages/t04_virtual_site_three_platforms/runs/r46_package_frozen_report_displays/result/units/E55-DISPLAY-release-summary/payload/t04_virtual_site_three_platforms-Display1-release-summary`
   (manifest names its origin).

3. **One home vs duplicates: absent as a rule, 134 source units have a delivery copy.** All 96 delivery copies have a
   source twin (same name, same paper), so delivery is already only a copy, but 134 sources are matched to them (some
   sources have several copies) and 105 of the 239 source units have none yet. Worse, the source itself is split: of
   165 distinct (paper, unit name) pairs among source units, 52 exist in two or more source homes (for example the
   old lane and a payload folder, or a live paper and its `_old/` or `paper-preview/` twin), and 62 names have 2+
   source copies. Example: `DrFirst-SPACE/.../Paper-PhyTraitNudging-IS/delivery/latex/displays/S-ISR-Appendix-C-Balance-and-Selection/Display1-balance-pvalues`
   copies `.../Bb-ISR-Appendix/S-ISR-Appendix-C-Balance-and-Selection/draft/evidence/display/Display1-balance-pvalues`.

4. **A person's acceptance recorded: nearly absent, 3 rows, 1 display.** 3 READMEs carry `accepted: ✅`, and they are
   the same unit three times: `Display1-hero-concept` ("JL 260907 · in chat: OK, 这很好", in the paper-preview copy, the
   live paper's `_archive/legacy-outline-evidence/` copy, and an `_old/` copy). 93 units have an open `accepted: ⬜`
   line (44 say only "review"; 24 say JL ticks after the values are checked against a Run receipt), and 239 have no
   `accepted:` line at all, including all 102 DrFirst units and all 96 delivery copies. The only
   `accepted: ✅` unit also sits in archive or `_old/` folders, so no live display is accepted today.

5. **Linked from the sentence that cites it: partly met, by name only.** 320 of 335 units are named somewhere in
   their own paper (plans, logs, Page text); 204 are named in a Page face or draft (not a log, outline table or
   README). That is a text mention, not a box on the sentence and not a card. 103 READMEs have a `serves:` line
   (the section that prints it), the only backlink the unit itself carries. Example: the plan table
   `DrFirst-SPACE/.../Paper-SuitableMessageForRx-JAMANO/Ba-JAMANO-Main/S-JAMANO-Main-3-Results/outline/S-JAMANO-Main-3-Results-evidence-items.md`
   lists Display1 to Display5 as `DISPLAY` items, each with the claim sentence it supports.

6. **A missing display flagged as a proposal: partly present, never as a proposal.** 15 `*-evidence-items.md`
   tables (WellDoc 11, DrFirst 4) hold 43 `DISPLAY` item rows. 24 carry `✅ preview.pdf` and an empty `⬜`
   acceptance mark; the 19 WellDoc rows name a unit (`unit Display1-...`), but only 6 of the 43 rows point at a unit
   folder that exists under that exact name. So a planned display is visible in plain tables, and some are not built,
   but nothing says "proposed by evidence" and nothing can be ticked to create it. Only 4 unit READMEs use the word "proposed" (a candidate render waiting), 8 say "Open needs".
   Example: `WellDoc-SPACE/examples-3-pred/Proj21-CGM-Pred/paper/Paper-CGMtoHbA1c/Bb-DC-Appendix/S-DC-Appendix-C-Supplementary-Figures/draft/S-DC-Appendix-C-Supplementary-Figures-evidence-items.md`
   (E01 and E02 `DISPLAY` rows name units `Display1-tir-...` and `Display2-bootstrap-...`).

```text
want                          met    partly   absent     count
1 reproducible                         🔶                 131 / 335 (recipe + intake)
2 names its data                                ⬜         57 / 335 (0 built_on)
3 one home                                      ⬜         134 sources copied; 52 names in 2+ homes
4 person accepted                               ⬜         1 display, archived
5 linked from sentence               🔶                    204 / 335 by name
6 missing = proposal                 🔶                    43 planned rows, 0 flagged proposed
```

**Not covered, said plainly.** "Names its data" read only manifests and README `source:` lines; a recipe script that
reads a CSV by path would not count. "Linked" is a text search for the unit name, so a slug mentioned in a log
counts as less than a box. 107 of the 335 rows are archived or `_old/` copies (96 delivery copies overlap that
count partly); the same counts over the 147 live,
non-delivery units are: recipe + intake 71, names a source 51, `accepted: ⬜` 65, 0 accepted, named in a Page 88.
Knowledge-SPACE has no display units at all.


Decided
-------

(none yet: a decision is one line, s01-D01 · <what was decided> (<who> <date>))


Open
----

1. Should the 3 homes collapse to one? 96 delivery copies are fine as copies; the old lane (146) and the work-Run
   payloads (93) both hold sources. Which is the single home: `display/` in the Task, or the Page Result payload?
2. What counts as a display's data source: a manifest origin, a README `source:` line, or only `built_on` evidence
   cards? Today 57 of 335 name one, so the strict rule makes 278 units "unsourced" on day one.
3. Do the 170 carried assets with no recipe (old PDFs and `table-body.tex` from submitted papers) have to be rebuilt,
   or are they allowed as "carried, accepted by JL" units, since they are what was already sent?
4. Acceptance: no live display has a ✅. Does JL tick each of the 147 live units, tick per paper at CHECK, or accept
   the ones a paper already submitted in one pass?
5. Do the 107 archived and `_old/` units stay in the count, or leave the display inventory (87 are old-lane
   copies, and the only 3 accepted rows are all in them)?
6. The 43 planned `DISPLAY` rows in the evidence-items tables: should they be read as proposals (a missing unit
   flagged for JL to tick), replacing those tables, or should the evidence skill's `proposals.md` own them?

(write here, or mark the drawing in red)
