#!/usr/bin/env python3
"""Read-only check of Design entry contracts against owning links and actual examples.

Run with the SPACE Python environment. This checks its explicit entry-point scope, not every reference
or a running service. --structure also runs the existing structure builder's freshness check.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

DESIGN = Path('plugins/haipipe-toolkit/skills/3_theme/design')
BLUEPRINT = Path('examples/Project-Ladder/blueprint/b12_theme_design')
SKILLS = ('hai-design', 'hai-design-method', 'hai-design-goal',
          'hai-design-unit', 'hai-design-workflow', 'hai-design-delivery', 'workbench-design')
EXTRA = ('hai-design/ref/design-ladder.md', 'workbench-design/CONSTITUTION.md',
         'workbench-design/ref/topics.md')
TASK_TYPES = {'t00': 'design-reason', 't99': 'design-whole', 'design': 'design-item'}
HISTORY = re.compile(r'\blegacy\b|\bhistorical\b|\bolder (?:board|block|layout|page|names|tabbed)\b|'
                     r'\bsix[- ]spaces?\b|\bprevious (?:layout|version|page)\b', re.I)
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\s]+)\)')


def prose_errors(text: str) -> list[str]:
    errors = []
    for i, line in enumerate(text.splitlines(), 1):
        if HISTORY.search(line):
            errors.append(f'{i}: superseded instruction in the current contract')
        if re.search(r'\bJL\s+\d{6}\b', line):
            errors.append(f'{i}: conversation provenance belongs in Trace')
        if re.search(r'<[A-Za-z][^<>]*>', line):
            errors.append(f'{i}: variable names must use 〈brackets〉')
    if len(text.splitlines()) >= 700:
        errors.append('human-readable file must remain under 700 lines')
    return errors


def field(text: str, name: str) -> str:
    match = re.search(r'^' + re.escape(name) + r':\s*([^\n]*)', text, re.M)
    return match.group(1).strip().strip('"\'') if match else ''


def check_documents(root: Path) -> list[str]:
    errors = []
    paths = [DESIGN / name / 'SKILL.md' for name in SKILLS] + [DESIGN / name for name in EXTRA]
    for rel in paths:
        path = root / rel
        if not path.is_file():
            errors.append(f'{rel}: missing contract')
            continue
        text = path.read_text()
        errors.extend(f'{rel}:{msg}' for msg in prose_errors(text))
        if path.name == 'SKILL.md':
            if field(text, 'name') != path.parent.name:
                errors.append(f'{rel}: skill identity does not match its folder')
            versions = re.findall(r'^\s{2}version:\s*["\']?([\d.]+)', text, re.M)
            if len(versions) != 1:
                errors.append(f'{rel}: metadata must declare one version')
            for declared in re.findall(r'(?:keeps|stays at|starts at)[^\n]*?`(\d+\.\d+\.\d+)`', text):
                if versions and declared != versions[0]:
                    errors.append(f'{rel}: version prose contradicts metadata')
        for href in LINK.findall(text):
            if re.match(r'^[a-z]+:|^#|^//', href, re.I):
                continue
            target = (path.parent / href.split('#')[0]).resolve()
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f'{rel}: unresolved owning/source link {href}')
    goal = (root / DESIGN / 'hai-design-goal/SKILL.md').read_text()
    schema = re.search(r'```yaml\s*\ngoals:\n(.*?)```', goal, re.S)
    if not schema or not re.search(r'^\s+name:', schema.group(1), re.M):
        errors.append('hai-design-goal: goal schema must name the slug required by the Job scaffold')
    ladder = (root / DESIGN / 'hai-design/ref/design-ladder.md').read_text()
    for role in TASK_TYPES.values():
        if f'`{role}`' not in ladder:
            errors.append(f'design-ladder: document actual Task type {role}')
    return errors


def check_examples(root: Path) -> list[str]:
    errors = []
    examples = root / 'examples/Project-Ladder/design'
    for kind in ('Design-Example', 'DesignMethodBook-Example'):
        block = examples / kind
        if not (block / 'board.md').is_file():
            errors.append(f'{kind}: missing Block face')
            continue
        book = kind.startswith('DesignMethodBook')
        expected = 'design-method-book' if book else 'design-board'
        if field((block / 'board.md').read_text(), 'board-kind') != expected:
            errors.append(f'{kind}: Block kind differs from its contract')
        jobs = sorted(block.glob('j[0-9][0-9]_*'))
        if not jobs:
            errors.append(f'{kind}: no real Jobs to check')
        seen = set()
        for job in jobs:
            face = job / f'{job.name}.md'
            if not face.is_file():
                errors.append(f'{job}: missing Job face')
                continue
            text = face.read_text()
            if not field(text, 'method'):
                errors.append(f'{face}: method identity is required')
            tasks = sorted(job.glob('t[0-9][0-9]_*'))
            if book:
                if tasks:
                    errors.append(f'{job}: Method Book has no execution Task layer')
                if not list(job.glob('m[0-9]*.md')):
                    errors.append(f'{job}: signed-version source files missing')
                continue
            if not all(field(text, name) for name in ('goal', 'inputs')):
                errors.append(f'{face}: Board Job pins are incomplete')
            for task in tasks:
                face = task / f'{task.name}.md'
                if not face.is_file():
                    errors.append(f'{task}: missing Task face')
                    continue
                role = task.name[:3] if task.name[:3] in ('t00', 't99') else 'design'
                declared = field(face.read_text(), 'task-type')
                if declared != TASK_TYPES[role]:
                    errors.append(f'{face}: expected task-type {TASK_TYPES[role]}, found {declared!r}')
                seen.add(declared)
        if not book and seen != set(TASK_TYPES.values()):
            errors.append(f'{kind}: examples do not cover the declared Task roles')
    return errors


def check_studios(root: Path) -> list[str]:
    errors = []
    for topic, example in (('s01-design', 'Design-Example'), ('s02-workbench-ui', 'DesignMethodBook-Example')):
        path = root / BLUEPRINT / topic / 'studio-views.json'
        try:
            views = json.loads(path.read_text())['views']
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f'{path}: {exc}')
            continue
        if [v.get('name') for v in views] != ['Structure', 'Draw', 'Skills']:
            errors.append(f'{topic}: Block Structure views differ from the approved contract')
        by_name = {v.get('name'): v.get('items', []) for v in views}
        live = [i.get('block') for i in by_name.get('Structure', []) if 'block' in i]
        if live != [f'examples/Project-Ladder/design/{example}']:
            errors.append(f'{topic}: Structure must embed its real Block')
        skills = by_name.get('Skills', [])
        if not skills:
            errors.append(f'{topic}: no owning skills')
        for view in views:
            for item in view.get('items', []):
                rel = item.get('path') or item.get('block') or ''
                target = (root / rel).resolve()
                if not rel or not target.is_relative_to(root) or not target.exists():
                    errors.append(f'{topic}: unresolved source {rel}')
                if 'block' in item and not (target / 'board.md').is_file():
                    errors.append(f'{topic}: embedded example is not a Block')
        for item in skills:
            if not item.get('path', '').endswith('/SKILL.md'):
                errors.append(f'{topic}: Skills must open owning entry files')
    source = root / BLUEPRINT / 'delivery/structure/build_organization.py'
    tree = ast.parse(source.read_text())
    if not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == '_studio_types' for n in ast.walk(tree)):
        errors.append(f'{source}: read Bands through the shared Work adapter')
    for topic in ('s11-design-job-preview', 's12-methodbook-job-preview'):
        face = root / BLUEPRINT / topic / f'{topic}.html'
        text = face.read_text()
        if '/_board/workbench?path=examples%2FProject-Ladder%2Fdesign%2F' not in text:
            errors.append(f'{topic}: live preview must select a real Design Block')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, help='repository root (defaults to this checkout)')
    parser.add_argument('--structure', action='store_true', help='also check generated page freshness')
    args = parser.parse_args()
    root = (args.root or next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())).resolve()
    errors = check_documents(root) + check_examples(root) + check_studios(root)
    for error in errors:
        print('FAIL', error)
    if args.structure:
        result = subprocess.run([sys.executable, str(root / BLUEPRINT / 'delivery/structure/build_organization.py'), '--check'], cwd=root)
        if result.returncode:
            errors.append('structure freshness check failed')
    if errors:
        print(f'Design contract check failed: {len(errors)} finding(s).')
        return 1
    print('Design current contracts, owning links, real Task roles and Studio bindings pass.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
