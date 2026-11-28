"""Guard the authored Idea/Grant examples and their shared Studio bindings.

These are content examples, not evidence of scientific Test, Select or submission.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse
from importlib import import_module

import yaml

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())
PAPER = ROOT / 'examples/Project-Ladder/paper'
BLUEPRINT = ROOT / 'examples/Project-Ladder/blueprint/b16_theme_paper'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def problems():
    errors = []
    scripts = ROOT / 'plugins/haipipe-toolkit/skills/1_base'
    sys.path.insert(0, str(scripts / 'ideation/hai-ideation/scripts'))
    from check_idea_block import check_block
    checker = load('example_job_records', scripts / 'project/hai-job/scripts/new_job.py')
    draft_src = scripts / 'draft/hai-draft/src'
    spec = importlib.util.spec_from_file_location('example_draft_source', draft_src / '__init__.py',
                                               submodule_search_locations=[str(draft_src)])
    package = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = package
    spec.loader.exec_module(package)
    read_draft = import_module('example_draft_source.page_structure').read_draft
    for name, kind in (('Idea-Example', 'ideation-block'), ('Grant-Example', 'grant-board')):
        block = PAPER / name
        face = block / 'board.md'
        if not face.is_file() or f'board-kind: {kind}' not in face.read_text():
            errors.append(f'{name}: real Block face/kind missing')
            continue
        if 'demonstration' not in face.read_text().lower():
            errors.append(f'{name}: demonstration boundary missing')
        for job in sorted(block.glob('j[0-9]*_*/')):
            errors.extend(f'{name}/{job.name}: {e}' for e in checker.check(job))
            for task in sorted(job.glob('t[0-9]*_*/')):
                text = (task / f'{task.name}.md').read_text()
                expected = 'ideation' if name == 'Idea-Example' else 'draft'
                if f'task-type: {expected}\n' not in text or '## Content\n' not in text:
                    errors.append(f'{task.name}: authored Task type/content missing')
                if any(task.glob('runs/*/result/runtime.yaml')):
                    errors.append(f'{task.name}: example must not claim scientific execution')
                if expected == 'draft':
                    drafts = list((task / 'draft').glob('*-draft-v*.md'))
                    if len(drafts) != 1:
                        errors.append(f'{task.name}: one readable example Draft source required')
                    else:
                        source = drafts[0].read_text()
                        parsed = read_draft(source)
                        if not parsed['paras'] or not all(p['ids'] and p['words'] for p in parsed['paras']):
                            errors.append(f'{task.name}: Draft reader cannot find authored sentences')
                        if 'approved: ⬜' not in source:
                            errors.append(f'{task.name}: example must not claim human approval')
        for path in block.rglob('*.md'):
            for raw in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                url = urlparse(raw)
                if url.scheme or not url.path or url.path.startswith('/_board/'):
                    continue
                target = (ROOT / url.path.lstrip('/') if url.path.startswith('/')
                          else path.parent / unquote(url.path))
                if not target.is_file():
                    errors.append(f'{path.relative_to(ROOT)}: broken link {raw}')
                elif re.match(r'[jt]\d+_', target.parent.name) and target.stem == target.parent.name:
                    errors.append(f'{path.relative_to(ROOT)}: Job/Task link must select inside its Block')
        if not list(block.glob('s[0-9][0-9]-*/studio-views.json')):
            errors.append(f'{name}: no actual Studio content')
    idea = PAPER / 'Idea-Example'
    errors.extend(f'Idea-Example: {f.code}: {f.message}' for f in check_block(idea, gate='generate'))
    if (idea / 'ideation.yaml').is_file():
        index = yaml.safe_load((idea / 'ideation.yaml').read_text())
        if len(index.get('ideas', [])) < 2:
            errors.append('Idea-Example: portfolio must demonstrate distinct candidate Jobs')
        for row in index.get('ideas', []):
            job = idea / row['job']
            for card_path in (job / 'cards').glob('i*.yaml'):
                card = yaml.safe_load(card_path.read_text())
                if card.get('state') != 'open' or card.get('decision_ref'):
                    errors.append(f'{card_path.name}: no human selection was commissioned')
                if any(c.get('evidence') or c.get('novelty_check', {}).get('status') != 'unverified'
                       for c in card.get('core_claims', [])):
                    errors.append(f'{card_path.name}: demonstration hypotheses claim verified evidence')
    grant = PAPER / 'Grant-Example'
    if (grant / 'board.md').is_file():
        face = (grant / 'board.md').read_text()
        for band in ('j0N Story', 'j1N Evidence', 'j2N Display', 'j3N Writing', 'j4N Presentation'):
            if band not in face:
                errors.append(f'Grant-Example: missing {band} group')
        for job in grant.glob('j[0-9]*_*/'):
            if re.match(r'j\d+_(submission|review)', job.name):
                errors.append(f'{job.name}: Review/Submission belongs inside Writing')
        for job in grant.glob('j[0-9]*_writing_*/'):
            face = (job / f'{job.name}.md').read_text()
            if 't2N Review' not in face or 't3N Submission' not in face:
                errors.append(f'{job.name}: Writing groups missing')
            if not list(job.glob('t2[0-9]_*')) or not list(job.glob('t3[0-9]_*')):
                errors.append(f'{job.name}: Review/Submission examples missing')
    return errors


if __name__ == '__main__':
    found = problems()
    for error in found:
        print('FAIL:', error)
    print(f'Idea/Grant examples: {len(found)} problems')
    raise SystemExit(bool(found))
