#!/usr/bin/env python3
"""paper-check-reference: mechanical audit of LaTeX cross-references.

Scans the root .tex and all transitively \\input{}-ed files for:
  - \\label{} definitions
  - \\ref / \\autoref / \\cref / \\eqref / \\nameref / \\hyperref consumers
  - \\cite / \\citep / \\citet / ... citations
  - \\input{} / \\include{} includes
  - \\phantomsection\\label position relative to \\section*

Produces a markdown audit report with 🔴 broken / 🟡 positional / 🟡 orphan items.

Usage:
    python3 check_refs.py <paper-dir-or-root-tex> [-o output.md]
"""
from __future__ import annotations
import argparse
import re
from collections import defaultdict
from pathlib import Path

COMMENT_RE = re.compile(r'(?<!\\)%.*$', re.MULTILINE)
LABEL_RE = re.compile(r'\\label\s*\{([^}]+)\}')
REF_RE = re.compile(r'\\(?:ref|autoref|cref|Cref|eqref|nameref)\b\*?\s*\{([^}]+)\}')
HYPERREF_RE = re.compile(r'\\hyperref\s*\[([^\]]+)\]')
CITE_RE = re.compile(
    r'\\(?:cite|citep|citet|citealp|citealt|citeauthor|citeyear|citeyearpar|nocite)\b\*?'
    r'\s*(?:\[[^\]]*\])?\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}'
)
INPUT_RE = re.compile(r'\\input\s*\{([^}]+)\}')
INCLUDE_RE = re.compile(r'\\include\s*\{([^}]+)\}')
SECTION_RE = re.compile(r'\\(?:section|subsection|subsubsection)\*?\s*\{([^}]*)\}')
PHANTOM_RE = re.compile(r'\\phantomsection')
BIBITEM_RE = re.compile(r'^\s*@\w+\s*\{\s*([^,\s]+)', re.MULTILINE)


def strip_comments(s: str) -> str:
    return COMMENT_RE.sub('', s)


def find_root_tex(path: Path) -> Path:
    if path.is_file():
        return path
    for c in sorted(path.glob('*.tex')):
        try:
            txt = c.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        if r'\documentclass' in txt:
            return c
    raise SystemExit(f'No root .tex with \\documentclass found in {path}')


def resolve_input(target: str, paper_dir: Path):
    target = target.strip()
    p = (paper_dir / target)
    if p.is_file():
        return p.resolve()
    p_tex = paper_dir / (target + '.tex')
    if p_tex.is_file():
        return p_tex.resolve()
    return None


def scan_tex_files(root_tex: Path, paper_dir: Path):
    seen, seen_set, queue = [], set(), [root_tex.resolve()]
    while queue:
        f = queue.pop(0)
        if f in seen_set:
            continue
        seen.append(f)
        seen_set.add(f)
        try:
            raw = f.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        content = strip_comments(raw)
        for rx in (INPUT_RE, INCLUDE_RE):
            for m in rx.finditer(content):
                sub = resolve_input(m.group(1), paper_dir)
                if sub and sub not in seen_set:
                    queue.append(sub)
    return seen


def relpath(f: Path, paper_dir: Path) -> str:
    try:
        return str(f.relative_to(paper_dir))
    except ValueError:
        return str(f)


def extract_markers(f: Path, paper_dir: Path):
    try:
        raw = f.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return
    rel = relpath(f, paper_dir)
    for i, line in enumerate(raw.split('\n'), 1):
        no_c = strip_comments(line)
        for m in LABEL_RE.finditer(no_c):
            yield ('label', m.group(1), rel, i)
        for m in REF_RE.finditer(no_c):
            yield ('ref', m.group(1), rel, i)
        for m in HYPERREF_RE.finditer(no_c):
            yield ('ref', m.group(1), rel, i)
        for m in CITE_RE.finditer(no_c):
            for k in m.group(1).split(','):
                k = k.strip()
                if k:
                    yield ('cite', k, rel, i)
        for rx in (INPUT_RE, INCLUDE_RE):
            for m in rx.finditer(no_c):
                yield ('input', m.group(1), rel, i)


def check_phantom_position(f: Path, paper_dir: Path):
    try:
        raw = f.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return []
    rel = relpath(f, paper_dir)
    lines = raw.split('\n')
    issues = []
    for i, line in enumerate(lines):
        no_c = strip_comments(line)
        if PHANTOM_RE.search(no_c) and LABEL_RE.search(no_c):
            label = LABEL_RE.search(no_c).group(1)
            prev_idx = i - 1
            while prev_idx >= 0 and not strip_comments(lines[prev_idx]).strip():
                prev_idx -= 1
            next_idx = i + 1
            while next_idx < len(lines) and not strip_comments(lines[next_idx]).strip():
                next_idx += 1
            prev = strip_comments(lines[prev_idx]) if prev_idx >= 0 else ''
            nxt = strip_comments(lines[next_idx]) if next_idx < len(lines) else ''
            prev_is_section = bool(SECTION_RE.search(prev))
            next_is_section = bool(SECTION_RE.search(nxt))
            if prev_is_section and not next_is_section:
                issues.append({
                    'label': label,
                    'file': rel,
                    'phantom_line': i + 1,
                    'section_line': prev_idx + 1,
                    'section_text': prev.strip()[:80],
                })
    return issues


def check_unlabeled_si(f: Path, paper_dir: Path):
    try:
        raw = f.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return []
    rel = relpath(f, paper_dir)
    lines = raw.split('\n')
    issues = []
    for i, line in enumerate(lines):
        no_c = strip_comments(line)
        m = SECTION_RE.search(no_c)
        if not m:
            continue
        title = m.group(1)
        if not any(k in title for k in ('SI', 'Supplementary', 'Appendix')):
            continue
        win = lines[max(0, i - 2):min(len(lines), i + 4)]
        has = any(PHANTOM_RE.search(strip_comments(w)) and LABEL_RE.search(strip_comments(w)) for w in win)
        if not has:
            issues.append({'file': rel, 'line': i + 1, 'section_text': title[:80]})
    return issues


def load_bib(bib_files):
    keys = set()
    for b in bib_files:
        try:
            txt = b.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        for m in BIBITEM_RE.finditer(txt):
            keys.add(m.group(1))
    return keys


def pick_output_path(paper_dir: Path, override):
    if override:
        return Path(override).resolve()
    feedback = paper_dir / '1-rounds'
    if feedback.is_dir():
        version_dirs = sorted([d for d in feedback.iterdir() if d.is_dir() and d.name.startswith('v')])
        if version_dirs:
            return version_dirs[-1] / 'reference-audit.md'
    return paper_dir / 'reference-audit.md'


def build_report(root_tex, paper_dir, tex_files, bib_files,
                 labels, refs, cites, input_locations,
                 phantom_issues, unlabeled_si, bib_keys,
                 broken_refs, orphan_labels, broken_cites, dead_bib, broken_inputs):
    out = []
    out.append('# Reference Audit\n')
    out.append(f'**Paper root:** `{relpath(root_tex, paper_dir)}`  ')
    out.append(f'**Scanned:** {len(tex_files)} `.tex` files; {len(bib_files)} `.bib` files; '
               f'{sum(len(v) for v in labels.values())} labels; '
               f'{sum(len(v) for v in refs.values())} refs; '
               f'{sum(len(v) for v in cites.values())} citations; '
               f'{len(input_locations)} \\input{{}} calls.\n')

    out.append('## Summary\n')
    out.append('| Severity | Category | Count |')
    out.append('|---|---|---:|')
    out.append(f'| 🔴 | Broken refs (\\ref / \\hyperref with no matching \\label) | {len(broken_refs)} |')
    out.append(f'| 🔴 | Broken inputs (\\input{{}} file not found on disk) | {len(broken_inputs)} |')
    out.append(f'| 🔴 | Broken citations (\\cite key not in any .bib) | '
               f'{len(broken_cites) if bib_keys else "n/a (no .bib found)"} |')
    out.append(f'| 🟡 | Phantom-after-section (\\phantomsection\\label{{}} placed AFTER heading) | {len(phantom_issues)} |')
    out.append(f'| 🟡 | Unlabeled SI / Appendix sections | {len(unlabeled_si)} |')
    out.append(f'| 🟡 | Orphan labels (defined but never \\ref-ed) | {len(orphan_labels)} |')
    out.append(f'| 🟢 | Dead bib entries (in .bib but never \\cite-ed) | {len(dead_bib)} |')
    out.append('')

    def section(title, items):
        if not items:
            return
        out.append(f'\n## {title}\n')
        for line in items:
            out.append(line)

    section(f'🔴 Broken refs ({len(broken_refs)})',
            [f'- **`{n}`** used at:' + ''.join(f'\n    - `{f}:{l}`' for f, l in locs)
             for n, locs in broken_refs])

    section(f'🔴 Broken inputs ({len(broken_inputs)})',
            [f'- `\\input{{{t}}}` at `{f}:{l}` — file not found' for t, f, l in broken_inputs])

    if bib_keys:
        section(f'🔴 Broken citations ({len(broken_cites)})',
                [f'- **`{n}`** used at:' + ''.join(f'\n    - `{f}:{l}`' for f, l in locs)
                 for n, locs in broken_cites])

    if phantom_issues:
        out.append(f'\n## 🟡 `\\phantomsection\\label{{}}` placed AFTER `\\section*{{}}` ({len(phantom_issues)})\n')
        out.append('**Fix:** move the `\\phantomsection\\label{...}` line to ABOVE the `\\section*{...}` line, '
                   'so `\\hyperref` clicks land on the heading text.\n')
        for it in phantom_issues:
            out.append(f'- `{it["file"]}:{it["section_line"]}-{it["phantom_line"]}` — label `{it["label"]}`')
            out.append(f'    - heading: `{it["section_text"]}`')

    if unlabeled_si:
        out.append(f'\n## 🟡 Unlabeled SI / Appendix sections ({len(unlabeled_si)})\n')
        out.append('**Fix:** add `\\phantomsection\\label{...}` immediately above the `\\section*{}` so future '
                   'cross-refs have an anchor.\n')
        for it in unlabeled_si:
            out.append(f'- `{it["file"]}:{it["line"]}` — `\\section*{{{it["section_text"]}}}`')

    if orphan_labels:
        out.append(f'\n## 🟡 Orphan labels ({len(orphan_labels)})\n')
        out.append('Defined but never `\\ref`-ed or `\\hyperref`-ed. Remove or wire up a cross-ref.\n')
        for n, locs in orphan_labels:
            out.append(f'- **`{n}`** defined at `{locs[0][0]}:{locs[0][1]}`')

    if dead_bib:
        out.append(f'\n## 🟢 Dead bib entries ({len(dead_bib)})\n')
        out.append('In one or more `.bib` files but never `\\cite`-ed. Cleanup is optional.\n')
        out.append(f'<details><summary>Show all {len(dead_bib)}</summary>\n')
        for k in dead_bib:
            out.append(f'- `{k}`')
        out.append('\n</details>')

    return '\n'.join(out) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Audit LaTeX paper cross-references.')
    ap.add_argument('paper_root', help='Paper directory or root .tex file.')
    ap.add_argument('-o', '--output', default=None, help='Output report path (.md). '
                    'Defaults to <paper-dir>/1-rounds/v<latest>/reference-audit.md.')
    args = ap.parse_args(argv)

    root_arg = Path(args.paper_root).resolve()
    if root_arg.is_file():
        root_tex = root_arg
        paper_dir = root_tex.parent
    else:
        paper_dir = root_arg
        root_tex = find_root_tex(paper_dir)

    tex_files = scan_tex_files(root_tex, paper_dir)
    bib_files = sorted(paper_dir.glob('*.bib'))
    bib_keys = load_bib(bib_files)

    labels = defaultdict(list)
    refs = defaultdict(list)
    cites = defaultdict(list)
    input_locations = []
    for f in tex_files:
        for kind, name, rel, line in extract_markers(f, paper_dir):
            if kind == 'label':
                labels[name].append((rel, line))
            elif kind == 'ref':
                refs[name].append((rel, line))
            elif kind == 'cite':
                cites[name].append((rel, line))
            elif kind == 'input':
                input_locations.append((name, rel, line))

    phantom_issues = []
    unlabeled_si = []
    for f in tex_files:
        phantom_issues.extend(check_phantom_position(f, paper_dir))
        unlabeled_si.extend(check_unlabeled_si(f, paper_dir))

    broken_refs = [(n, locs) for n, locs in sorted(refs.items()) if n not in labels]
    orphan_labels = [(n, locs) for n, locs in sorted(labels.items()) if n not in refs]
    broken_cites = [(n, locs) for n, locs in sorted(cites.items()) if bib_keys and n not in bib_keys]
    dead_bib = sorted(bib_keys - set(cites.keys())) if bib_keys else []
    broken_inputs = []
    for target, f, l in input_locations:
        if resolve_input(target, paper_dir) is None:
            broken_inputs.append((target, f, l))

    report = build_report(root_tex, paper_dir, tex_files, bib_files,
                          labels, refs, cites, input_locations,
                          phantom_issues, unlabeled_si, bib_keys,
                          broken_refs, orphan_labels, broken_cites, dead_bib, broken_inputs)

    output_path = pick_output_path(paper_dir, args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')

    # Brief stdout summary
    print(f'Report -> {output_path}')
    print(f'🔴 broken refs:     {len(broken_refs)}')
    print(f'🔴 broken inputs:   {len(broken_inputs)}')
    print(f'🔴 broken cites:    {len(broken_cites) if bib_keys else "n/a"}')
    print(f'🟡 phantom-after:   {len(phantom_issues)}')
    print(f'🟡 unlabeled SI:    {len(unlabeled_si)}')
    print(f'🟡 orphan labels:   {len(orphan_labels)}')
    print(f'🟢 dead bib:        {len(dead_bib)}')


if __name__ == '__main__':
    main()
