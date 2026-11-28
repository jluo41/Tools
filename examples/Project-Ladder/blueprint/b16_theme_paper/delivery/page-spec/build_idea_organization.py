"""s01 Idea Block structure as folder trees, drawn like b17's s01 (b16 trace 261127/1252).

Three rule trees (Folder, Job / Task Organization, Studio Organization) and one example
tree, each a section of one page that the Studio views open by fragment. The tree, its
style and the section picker come from b17's shared builder; this file supplies only the
Idea Block's names, read from hai-ideation's references/idea-block.md.
"""
from __future__ import annotations

import importlib.util
from html import escape as esc
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "PRINCIPLE.md").is_file())
BLOCK = ROOT / "examples/Project-Ladder/blueprint/b16_theme_paper"
TARGET = BLOCK / "s01-idea-block-structure/structure/idea-organization.html"
SHARED = ROOT / "examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py"
SOURCE = "plugins/haipipe-toolkit/skills/1_base/ideation/hai-ideation/references/idea-block.md"


def shared():
    spec = importlib.util.spec_from_file_location("work_structure_renderer", SHARED)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trees(s):
    n = s.node
    folder = n('Idea-〈slug〉/', n('board.md'), n('ideation.yaml'), n('sNN-〈topic〉/'), n('trace/'),
               n('jNN_〈idea〉/', n('jNN_〈idea〉.md'), n('ideation.yaml'), n('cards/'), n('workflow/'),
                 n('handoff/'),
                 n('tNN_〈assessment-question〉/', n('tNN_〈assessment-question〉.md'), n('assessments/'),
                   n('runs/'))))
    jobs = n('Idea Block', n('〈Job group〉', n('〈Idea〉', n('〈Task group〉', n('〈Assessment question〉')))))
    studio = n('Idea Block', n('〈Studio topic〉'))
    example = n('Idea Block', n('Ideas',
                n('j01_calibration/', n('Framing', n('t01_falsifiable-claim/')),
                  n('Assessment', n('t02_closest-work-comparison/'), n('t03_minimum-experiment/')),
                  n('Decision', n('t04_development-recommendation/'))),
                n('j02_missingness/', n('Assessment', n('t01_missing-input-experiment-design/')))))
    return folder, jobs, studio, example


PURPOSE = {   # each name's hover: what it holds, or the title behind a folder name
    'Idea-〈slug〉/': 'the Idea Block: one bounded direction, beside Paper- and Grant- in paper/',
    'board.md': "the Block's face; board-kind: ideation-block",
    'ideation.yaml': 'the portfolio index (Block) or the idea unit (Job)',
    'sNN-〈topic〉/': 'a Studio topic: shared reasoning or a drawing',
    'trace/': 'a record of each change, by day',
    'jNN_〈idea〉/': 'an Idea Job: one candidate question with its one Idea Card',
    'jNN_〈idea〉.md': "the Job's face: question, goal, Tasks, decision links",
    'cards/': 'direction, the Idea Card, test matrix, venue-fit readings',
    'workflow/': 'semantic receipts and immutable decisions',
    'handoff/': 'the paper handoff, after a person selects the idea',
    'tNN_〈assessment-question〉/': 'a Task: one assessment question (task-type: ideation)',
    'tNN_〈assessment-question〉.md': "the Task's face",
    'assessments/': 'authored review receipts, when produced',
    'runs/': 'soft Runs run-assess-〈target〉, when commissioned',
    'j01_calibration/': 'Calibration under shift',
    'j02_missingness/': 'Missingness robustness',
    't01_falsifiable-claim/': 'Falsifiable claim',
    't02_closest-work-comparison/': 'Closest-work comparison',
    't03_minimum-experiment/': 'Minimum experiment',
    't04_development-recommendation/': 'Development recommendation',
    't01_missing-input-experiment-design/': 'Missing-input experiment design',
}
JOB_ROLES = ('', 'Job group · optional', 'Job', 'Task group · optional', 'Task')


def section(s, key, body, title=''):
    return (f'<section id="{key}" title="{esc(title)}" hidden><div class="drawing"><ul class="tree"><li>'
            + body + '</li></ul></div></section>')


def render(s=None):
    s = s or shared()
    s.PURPOSE.update(PURPOSE)
    folder, jobs, studio, example = trees(s)
    body = ''.join([
        section(s, 'folder-rules', s.tree_html(folder, True, purpose=True), s.NAMING),
        section(s, 'jobs-rules', s.tree_html(jobs, roles=JOB_ROLES), s.NAMING),
        section(s, 'studio-rules', s.tree_html(studio, roles=('', 'Studio topic')), s.NAMING),
        section(s, 'jobs', s.tree_html(example, True, roles=JOB_ROLES, purpose=True), 'From ' + SOURCE),
    ])
    script = ("function pick(){const hash=location.hash.slice(1),draw=hash.endsWith('-draw');"
              "const want=hash.replace(/-draw$/,'');const key=document.getElementById(want)?want:'folder-rules';"
              "document.querySelectorAll('main>section').forEach(x=>x.hidden=x.id!==key);"
              "if(key==='folder-rules')document.querySelectorAll('#folder-rules details').forEach((d,i)=>d.open=draw||i<2);}"
              "addEventListener('hashchange',pick);pick();")
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Idea structure</title>'
            f'<style>{s.STYLE}</style></head><body><main class="content">{body}</main>'
            f'<script>{script}</script></body></html>')


if __name__ == '__main__':
    TARGET.write_text(render(), encoding='utf-8')
    print(TARGET.relative_to(ROOT))
