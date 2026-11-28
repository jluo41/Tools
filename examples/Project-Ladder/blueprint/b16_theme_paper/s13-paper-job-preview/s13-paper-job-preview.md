s13 · Block Job UI Preview: Paper
=================================

**Tags:** `Levels`

**For:** a Paper or Grant Job worked on inside its Block, using the same navigation, bands and folds as Work

**Delivery type:** ui

**UI preview:** Job · paper

**Covers:** Writing Version, Display Evidence, Value Evidence, Citation Evidence, Submission and Review Job; each Job's Main and selected Task

**Topic:** What stays common when a Job builds a manuscript, prepares evidence, answers comments or submits a grant? Keep Work's Job topic → Job → Main or Task topic → Task. Main carries Overview, Tasks and Findings; the Job type supplies their content. A selected Task keeps its workflow controls and Runs.

**Source:** [Work Job preview](../../b17_theme_work/s11-work-job-preview/s11-work-job-preview.md), [Paper example](../../../paper/Paper-Example/board.md), [proposed specification](../delivery/page-spec/job-ui-design.md).

**Feeds:** shared `servers/workbench/page/job_task_views/focus_jobs.py` and the Paper content adapters in `servers/workbench-paper/`.

## Page

The live views open `paper/Paper-Example` in its Block's Jobs section. The job-rows and job-main views share j11 and differ only in the highlighted part. Evidence, Submission and Review each open their existing Job. These show the current server output, including the older content defaults.

## Effect

`delivery/ui/paper-job-main.html` is the reviewed interaction proposal. Paper and Grant select the two writing contexts; the Job topics reach all six Job types. Example text and feedback remain local to the preview. This is not a new reader or a writer of study records.

The Overview merge is a proposal alongside b17's choices. Its final form follows the shared Work decision; it is not an independent Paper convention.

## Decided

- Reuse Work's four horizontal navigation rows; hide the Task row on Main and remember the selected Task within its topic.
- Paper and Grant share the same Job types. Their target requirements and authored sections differ.
- Semantic groups are Evidence, Writing, Submission and Review. A lower numbered group does not mean obsolete.
- Main uses Overview, Tasks and populated Findings. A selected Task retains its own steps, output, Runs and inline questions.
- Idea Job design belongs to [s14](../s11-idea-job-preview/s11-idea-job-preview.md); source Idea Jobs retain their identity when a Paper is created.

## Open

- Adapt the six Job Main contents to the shared renderer, including the missing Review dispatch.
- Preserve scoped Task view controls when embedded; switching a step must stay inside the selected Task.
- Add canonical Grant and Idea examples through their scaffold writers, then verify actual pages.
- Keep the current `job-views.md` matrix truthful until the renderer changes. The proposed matrix is in `job-ui-design.md`.

## Files

- `s13-paper-job-preview.html`: Studio's live Page views and proposed Effect entry.
- `delivery/ui/paper-job-main.html`: interactive Paper and Grant Main/Task proposal.
- `../delivery/page-spec/job-ui-design.md`: content mapping, reader boundaries, implementation order and acceptance.
- The existing drawing, image, slides data and original builder remain historical material; they have not been rebuilt for this proposal.

## Historical source

The previous face is retained below as historical content. Its old folder, Space and comments-batch conventions do not override the current Paper ladder or the proposal above.

> s12 · Job level
> ===============
>
> **Tags:** `Levels`
>
> **Stage:** shaping
>
> **For:** a deck, and a paper version's tab, its Spaces as full screens with what is on disk, for the people who build the workbench
>
> **Delivery type:** ui
>
> **Topic:** a paper version's tab on the shared frame: one version for one venue, its telling, its Sections
> and its build; its Spaces as full screens, "on disk" under each, two pop-outs, then Guide › Method
> opened from the Job tab (JL 261007).
>
> **Source:** the screens are drawn by `../_build/paper_ui.py`, shared by s11 · s12 · s13; the Guide's
> steps and method cards are read from `servers/workbench-paper/guide/method.md` and its `methods/`
> (and the Page Task's `guide.yaml` at Task level) at build time. Placeholders only.
>
> **Feeds:** `../reports/` Q01 (and the open marks of q02, q03).
>
>
> Files
> -----
>
> ```text
> s13-paper-job-preview/
> ├── s13-paper-job-preview.md           this notes file
> ├── build_s13_paper_job_preview.py     the builder; marks are kept on rebuild
> ├── s13-paper-job-preview.excalidraw   the drawing: today → proposed, one row per Space (screen · on disk · why), Guide › Method, open notes
> └── s13-paper-job-preview.png          its preview
> ```
>
> Rebuild: `python build_s13_paper_job_preview.py`, then
> `python ../../../../../plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/render_png.py s13-paper-job-preview.excalidraw s13-paper-job-preview.png 0.4`.
>
>
> Decided and drawn (261007, green ✎ in the drawing)
> --------------------------------------------------
>
> 1. A version is `jNN_v<MMDD>_<desk>/`, dated by its send; its face carries venue · deadline · tells
>    (a studio topic, `studio/sNN-story-<telling>/`) · from · answers, its `## Narrative` (the old §8, the
>    build's order) and its `## Questions`. It holds `studio/` · `reports/` · `runs/`, its Tasks and `delivery/`.
> 2. Its Tasks: `t00_abstract` · `t0N_` Main · `t2N_` Appendix (A = t21) · `t3N_` letters (t31 cover
>    letter, t32 response).
> 3. Audience Report: Questions (the register, then the standing J1–J5) · Draft-Main · Draft-Appendix
>    (Question │ Work │ Report, the rendered draft beside the Section's drawing) · Comments (Review Items
>    citing R1.1 · E1.2) · Cover letter (paragraph │ the question it answers │ its text).
> 4. Comments are a report of type comments, `reports/qNN_<kind>-<MMDD>/` in the version that answers
>    them (hai-paper-comments 1.1.0); never a Task.
> 5. Delivery: item cards (Manuscript · Letters · Checks · Sent), no third row.
> 6. A revision is a new version, starting as a copy of the last one's authored files.
>
> Live: `servers/workbench-paper/paper_theme.py` (`version_spaces`) draws all of this on TestToLearn's
> j01 and j02.
>
>
> Open
> ----
>
> 1. Agree its **For:** line and **Delivery type:** (ui), proposed by the agent 261030?
>
> See the drawing's red notes (open ?).
>
> (write here, or mark the drawing in red)
