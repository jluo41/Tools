"""Draw the Grant Block structure proposal with the shared Studio kit.

Read hai-studio/CONSTITUTION.md before editing. This is a design drawing,
not an example of an implemented Grant-specific renderer. The canvas writer
preserves the person's additions, edits and deletions across rebuilds.

Run here or from an installed topic:
    python build_s02_grant_block_structure.py [--repo-root <Tools checkout>]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
STEM = 's02-grant-block-structure'
INK, BLUE, PALE = '#15324b', '#6088a6', '#edf4f9'
AMBER, GREEN, GREY = '#b7791f', '#24795b', '#607486'


def repository(given: Path | None) -> Path:
    candidates = [given] if given else [*Path(__file__).resolve().parents, Path.cwd()]
    for p in candidates:
        if p and (p / 'PRINCIPLE.md').is_file() and (p / 'plugins/haipipe-toolkit').is_dir():
            return p.resolve()
    raise SystemExit('Pass --repo-root <Tools checkout> when building outside the repository.')


def draw(root: Path, out: Path) -> None:
    scripts = root / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'
    sys.path.insert(0, str(scripts))
    import quick_draw as q
    import icons
    import canvas
    from render_png import render

    els = [q._el('frame', 'grant_structure', 0, 0, 2560, 1440,
                 stroke=BLUE, name='Grant Block Structure')]

    def text(eid, x, y, words, size=32, color=INK, align='left'):
        block = q.text(eid, x, y, words, size, color, align)
        for e in block:
            e['fontFamily'] = 6
        els.extend(block)

    def box(eid, x, y, w, h, fill=PALE, stroke=BLUE, radius=True):
        els.append(q._el('rectangle', eid, x, y, w, h, stroke, fill,
                         roundness={'type': 3} if radius else None))

    def arrow(eid, points, label='', at=None, color=BLUE):
        els.extend(q.arrow(eid, points, color, width=3))
        if label and at:
            text(eid + '_label', *at, label, 30, color, 'center')

    def picture(eid, fn, x, y, scale=.7, color=BLUE, fill=PALE):
        for e in fn(eid, 0, 0, state='off'):
            old_fill = e.get('backgroundColor')
            if e.get('strokeColor') == old_fill and old_fill not in ('transparent', '#ffffff'):
                e['strokeColor'] = fill
            else:
                e['strokeColor'] = color
            if old_fill not in ('transparent', '#ffffff'):
                e['backgroundColor'] = fill
            e['x'], e['y'] = x + e['x'] * scale, y + e['y'] * scale
            e['width'] *= scale
            e['height'] *= scale
            if e.get('points'):
                e['points'] = [[a * scale, b * scale] for a, b in e['points']]
            els.append(e)

    text('title', 75, 45, 'Grant Block Structure', 60)
    text('thesis', 80, 130, 'Named groups, typed work, distinct application versions', 34)
    text('hierarchy', 1350, 136, 'Job group → Job Name → Task group → Task Name', 30, GREY)

    def group(eid, x, y, w, h, name):
        box(eid, x, y, w, h, '#f8fbfd')
        text(eid + '_name', x + 34, y + 25, name, 44)

    def job(eid, x, y, words, size=34):
        picture(eid + '_record', icons.document, x, y - 4, .36)
        text(eid, x + 70, y + 6, words, size)

    def task(eid, x, y, group_name, output, split=190, size=30):
        text(eid + '_group', x, y, group_name, size, BLUE)
        arrow(eid + '_to_name', [(x + split - 48, y + 18),
                                (x + split - 12, y + 18)])
        text(eid + '_name', x + split, y, output, size, GREEN)

    # The root branches to Job groups. Contract annotations distinguish types;
    # document icons distinguish named Job instances inside those groups.
    group('story_group', 80, 220, 650, 475, 'Story')
    text('story_type', 115, 302, 'Job Type: to define', 28, GREY)
    job('research_case', 115, 346, 'Research case', 36)
    text('story_task_type', 115, 412, 'Task Type: draft for prose', 28, GREY)
    task('aims', 115, 472, 'Aims', 'Specific aims')
    task('rationale', 115, 538, 'Rationale', 'Significance')
    task('approach', 115, 604, 'Approach', 'Research plan')

    group('evidence_group', 80, 780, 650, 475, 'Evidence')
    text('evidence_type', 115, 862, 'Job Type: to define', 28, GREY)
    job('preliminary_evidence', 115, 906, 'Preliminary evidence', 34)
    text('evidence_task_type', 115, 972, 'Task Types: reconcile owners', 28, AMBER)
    task('values', 115, 1032, 'Values', 'Pilot measurements', size=28)
    task('citations', 115, 1098, 'Citations', 'Closest-work check', size=28)
    task('checks', 115, 1164, 'Checks', 'Source provenance', size=28)

    group('display_group', 900, 220, 730, 475, 'Display')
    text('display_type', 935, 302, 'Job Type: display (legacy reader)', 28, GREY)
    job('display_roles', 935, 346, 'Main · Appendix · Explore', 34)
    text('display_task_type', 935, 412, 'Task Type: final-asset contract?', 28, '#b7791f')
    task('figures', 935, 492, 'Figures', 'Study design', split=190, size=32)
    task('tables', 935, 580, 'Tables', 'Feasibility summary', split=190, size=30)

    group('writing_group', 1800, 220, 690, 655, 'Writing')
    text('writing_type', 1835, 302, 'Job Type: Writing Version', 28, GREY)
    job('full_application', 1835, 346, 'Full application', 36)
    text('other_versions', 1835, 410, 'Letter of intent · Revision', 30)
    text('writing_task_type', 1835, 468, 'Task Type: draft for prose', 28, GREY)
    task('application', 1835, 530, 'Application', 'Research strategy', split=215, size=28)
    task('attachments', 1835, 600, 'Attachments', 'Budget justification', split=215, size=28)
    task('review', 1835, 670, 'Review', 'Reviewer response', split=215, size=28)
    task('submission', 1835, 740, 'Submission', 'Upload package', split=215, size=28)
    text('submission_type', 1835, 810, 'Packaging Task Type?', 28, '#b7791f')

    group('presentation_group', 900, 955, 730, 300, 'Presentation')
    text('presentation_type', 935, 1034, 'Job Type: to define', 28, GREY)
    job('presentation_formats', 935, 1083, 'Slides · Video · Poster', 34)
    text('presentation_task_type', 935, 1148, 'Task Types: draft script · production?', 28, GREY)
    task('content', 935, 1202, 'Content', 'Research pitch', split=190, size=30)

    box('grant_block', 1010, 755, 480, 110, '#fff3bf')
    text('grant_block_name', 1080, 779, 'Grant Block', 48)
    arrow('owns_story', [(1010, 810), (800, 810), (800, 470), (730, 470)])
    arrow('owns_evidence', [(800, 810), (800, 1015), (730, 1015)])
    arrow('owns_display', [(1250, 755), (1250, 695)])
    arrow('owns_writing', [(1490, 810), (1710, 810), (1710, 550), (1800, 550)])
    arrow('owns_presentation', [(1250, 865), (1250, 955)])

    # Named Studio discussions are illustrative; they are not scaffolded records.
    text('studio_heading', 82, 1294, 'Studio groups → topics', 30, GREY)
    text('studio_research', 480, 1294, 'Research design → Aims and rationale', 30)
    text('studio_communication', 1560, 1294, 'Communication → Application narrative', 30)
    text('studio_views', 82, 1375, 'Views: Structure · Draw · Examples · Skills', 32)
    text('group_note', 1360, 1378, 'Groups organize; types define the work', 30, GREY)
    for e in els[1:]:
        e['frameId'] = 'grant_structure'
    out.mkdir(parents=True, exist_ok=True)
    canvas.write(out / (STEM + '.excalidraw'), els,
                 'hai-studio: Grant Block structure proposal', palette=False)
    render(out / (STEM + '.excalidraw'), out / (STEM + '.png'), .6)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', type=Path)
    ap.add_argument('--out-dir', type=Path, default=Path(__file__).resolve().parent)
    a = ap.parse_args()
    draw(repository(a.repo_root), a.out_dir)


if __name__ == '__main__':
    main()
