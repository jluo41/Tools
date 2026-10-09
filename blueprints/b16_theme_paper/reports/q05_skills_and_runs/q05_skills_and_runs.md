# Which skills and Runs make the paper theme?
state: 🟡 DRAFT · g04 run 2026-10-07, phases 1-6; two calls left to JL (venue/ out of skills/, one home for a venue)
answers: Q05
answer-status: partial
results-read: 2026-10-07T22:45-04:00

## Opening

The paper theme is nine skills under `skills/2_theme/paper/` and the base skills it borrows. On the
ladder, each level's Spaces offer buttons, and each button makes one Run, named `run-<type>-<target>`.
This report says which skill owns each Run, where the skills fall short today, and how their folders
change to close the gap.

**Where this Page sits:** [Q05 · Which skills and Runs make the paper theme?](../../board.md).

**Why it matters:** a button whose Run no card owns copies a prompt that no skill answers. The workbench
can't say who runs it, or what a person signs.

## Content

### 1 · Answer

Drawn in `studio/s21-paper-run-skill/` (seven frames; the notes file holds the counts and the plan).

| level | Runs its buttons make | with a run card or the frame, before g04 | after g04 (261007) |
|---|---|---|---|
| Block (the paper Board) | 23 | 12 | 21 (left: Open a grant, Build reference.bib, both still "?" in s11) |
| Job (one version) | 22 | 11 | 22 |
| Task (one Section) | 19 | 19 | 19 |

- **Ownership:** a Section's Runs are the Page workflow's, already carded; the Board's and the version's
  are the paper skills', and before g04 half had no card; now every Job button and all but two Block buttons do.
- **Run names:** every Run is `run-<type>-<target>`; two buttons that make one Run share it. Only another
  theme's supporting Run keeps its hard `rNN_` name.
- **Skill folders:** shaped like the design theme's skill, with one ladder contract (`haipipe-paper/ref/paper-ladder.md`)
  and one scaffold for every level (`haipipe-paper/scripts/paper_ladder.py`). Each file's change and its
  reason are in s21's "skill folders: before → after" frame.
- **Order:** contract → cards → Board skills → version skills → Section skill → old names out. The goal
  `goals/g04-paper-skills.md` runs it.

### 2 · Evidence

JL 261007: "focus on show what are the skills and runs we have in the paper set"; "the current skill is
not that powerful enough … make a plan"; "a before after plan of the skill folders and what to change and
why"; "unify the run to be run-xxx-xxx". The counts are read on every build from the s11, s12 and s13
builders, the paper and Page `run-cards.md`, the paper workbench (`paper_theme.py`) and the shared frame.

### 3 · Limits

- The Board's and the version's Run names are real now (their cards' patterns); a Board or version Run is a
  `haipipe-run` folder, a Section's stays a Page engine ticket file, so the two shapes differ by level.
- Two calls stay with JL: whether `venue/` (its own repo, 821 MB) moves out of `skills/`, and whether the
  assemble skill's `profiles/` move into `venues/<venue>/kit/` (Q02).
- The old paper-edit family installed at user level is outside this plan.

### 4 · Done (2026-10-07, goal g04)

- **Phase 1 · contract:** `haipipe-paper/ref/paper-ladder.md` (was paper-structure.md); `scripts/paper_ladder.py`
  (board · version · next · spaces · task · run · rollback; `run` makes a `haipipe-run` folder with its run.yaml);
  `scripts/carry_over/` for the three one-time moves; `version_paper.py` retired (its `comments` is
  `haipipe-paper-comments/scripts/review_items.py add`). Family test `tests/test_paper_ladder.py`.
- **Phase 2 · cards:** `haipipe-paper-workflow/ref/run-cards.md` by `<Level> › <Space>`, one card per button; gates
  G0-G2 at the Board, G3-G5 in a version; `workbench-paper/ref/workbench-table.md` by level (check PASS);
  `servers/workbench-paper/paper_theme.py` reads every button from the cards (`_run_cards`), no typed labels;
  `workbench-paper` SKILL.md is the theme on the frame, the old page's text is `ref/old-page.md`, and
  `ref/space-mapping.md` is retired. "Add a review" is "Add comments".
- **Phase 3 · Board:** `haipipe-paper-story` (a telling as a studio topic, `ref/narrative.md`), `-ideation`
  (`studio/s01-ideation/`), `-venue` (`venues/<venue>/`, `ref/call-template.md`).
- **Phase 4 · version:** `review_items.py route · reply`; `build.py send|release` into a comments report; the
  cover letter from the `t31_` Task; the Send card; J1-J5 in the workflow skill.
- **Phase 5 · Section:** `haipipe-paper-section` (the Narrative row, `ref/requirement.md`, a Section's own
  `studio/` and `reports/`); `create_section_sessions.py` reads `tNN_` Sections.
- **Phase 6 · old names:** 0 old names left as current in the nine skills; each touched skill has its version and
  CHANGELOG line.
- **Checks:** paper 8/8 · workbench-paper + _host 86/86 · assemble 66 pass, 2 known Word-conversion failures ·
  `table-workbench --check --cards` PASS.

### 5 · Next

- JL's two calls: move `venue/` (its own 821 MB repo) out of `skills/`, and one home for a venue (the shared Venue
  Page or the Board's `venues/<venue>/call.md`, Q02).
- s11's two proposed buttons, Open a grant and Build reference.bib, get cards once s11 decides them.

## Questions this raises

- Should a Section's Requirement rubric live in `haipipe-paper-section` or in the Page's own skills?
