"""Evidence cards: read a card list, find each Run it names, and say what is missing.

A card is one topic holding many items. CITE cards come from the Project's discovery/ world (someone else's paper,
and any value or figure the paper reports); VALUE cards come from its work/ world (a number one of our Runs wrote;
kind `work` until 261020, still read as `value`). The card format is in ../SKILL.md; the sibling skills
haipipe-evidence-cite and haipipe-evidence-work say how to find each kind.

A card's topic is its Task: a needed item joins the card of the Task its proposal would be made in (`order`), so no
card is a bag of "Sources still needed" (JL 261020: "cite 1's name is very weird ... make it into different cite with
the topic").

    from cards import load, resolve, title_of, paper, facts, work_value, order, check, proposals, LABEL, COLOR
    python cards.py check   <task>/evidence/cards.yaml [--sentences <file.json>]
    python cards.py propose <task>/evidence/cards.yaml [--page <name>] [--write]
    python cards.py bib     <task>/evidence/cards.yaml --draft <draft.md> [--write]

The cards live in the Task's own evidence/ folder, beside draft/ and display/ (JL 261016): evidence/cards.yaml holds
them, evidence/proposals.md the flagged proposals. A Studio face holding `evidence:` in its yaml also works
(`--key <yaml key>`), for pages made before the folder existed.

`check` resolves every address, fact and value and prints one line per problem; with --sentences (a JSON object
{"5": "sentence text", ...}) it also checks that each anchor's words are in its sentences. Exit 1 when anything is
missing. A page builder imports the functions and draws; this file draws nothing.

`propose` turns every needed item into a flagged proposal, a line a person ticks: what to make (a Run in an existing
Task, a new Task in a Job, a new Job in a Block, or a Studio topic), where, and for what purpose, marked
"proposed by evidence". It writes proposals.md beside cards.yaml with --write and keeps every tick already
there; nothing is made until a person ticks it, and the owner of that level makes it (haipipe-discovery,
haipipe-task, haipipe-job, haipipe-studio).
"""
import json
import re
import sys
from pathlib import Path

import yaml

# VALUE, not WORK: what the item is, a number (JL 261020: "the work 1's name is not good ... more like something else")
LABEL = {'cite': 'CITE', 'value': 'VALUE'}
COLOR = {'cite': '#1971c2', 'value': '#7048e8', 'need': '#e03131'}   # external blue, internal violet, needed red
THEME = {'cite': 'discovery', 'value': 'work'}
OLD_KIND = {'work': 'value'}


def project_root(path):
    """The Project folder (the one holding project.yaml) above a file or folder."""
    path = Path(path).resolve()
    for p in [path, *path.parents]:
        if (p / 'project.yaml').is_file():
            return p
    raise ValueError(f'{path}: no project.yaml above it.')


def resolve(project, kind, address):
    """bNN.jNN[.tNN[.rNN]] in the kind's world → its folder; a full Run address → that Run's result/ folder.

    A Run is found as tNN_*/runs/rNN_*/result (Discovery, standalone Task) or jNN_*/results/tNN_*/rNN_* (a Task
    whose Results sit in its Job)."""
    parts = address.split('.')
    if not 2 <= len(parts) <= 4 or not all(re.fullmatch(r'[bjtr]\d+', p) for p in parts):
        raise ValueError(f'{address}: an address is bNN.jNN, bNN.jNN.tNN or bNN.jNN.tNN.rNN.')
    world = Path(project) / THEME[kind]
    pattern = '/'.join(f'{p}_*' for p in parts[:3])
    found = list(world.glob(pattern))
    if len(found) != 1:
        raise ValueError(f'{address}: {len(found)} folders match in {world.name}/, need one.')
    if len(parts) < 4:
        return found[0]
    task = found[0]
    runs = list(task.glob(f'runs/{parts[3]}_*/result')) + list(task.parent.glob(f'results/{task.name}/{parts[3]}_*'))
    if len(runs) != 1:
        raise ValueError(f'{address}: {len(runs)} Run results found, need one.')
    return runs[0]


def title_of(folder):
    """A Block, Job or Task's own title: the first '# ' line of its page, else its folder name in words."""
    page = Path(folder) / f'{Path(folder).name}.md'
    m = page.is_file() and re.search(r'^# (.+)$', page.read_text(encoding='utf-8'), re.M)
    return m[1].strip() if m else re.sub(r'^[bjt]\d+_', '', Path(folder).name).replace('_', ' ')


def paper(result):
    """(title, 'Calzavara et al., 2025 · EMBC') from a discovery Run's one-entry .bib."""
    bib = next(Path(result).glob('*.bib')).read_text(encoding='utf-8')
    get = lambda k: (m := re.search(r'\b' + k + r'\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', bib)) and m[1].strip()
    authors = get('author').split(' and ')
    first = authors[0].split(',')[0].strip()
    who = first + (' et al.' if len(authors) > 2 else ' and ' + authors[1].split(',')[0].strip() if len(authors) == 2 else '')
    venue = get('journal') or get('booktitle') or ''
    return re.sub(r'[{}]', '', get('title')), f"{who}, {get('year')} · {venue}"


def facts(result, ids):
    """The fact lines of a discovery Run's facts.md, `- `ID` · label: <fact> Locator: …`: a quoted sentence as
    '"…" (T06)', its closing quote followed by a stop or not ("…". Locator); a table's rows, which are not a sentence,
    as they are written, '… (T05)' (r20 Oca 2023: its counts are Table 1 and Table 3 rows)."""
    text = (Path(result) / 'facts.md').read_text(encoding='utf-8')
    out = []
    for k in ids:
        line = re.search(r'^- `' + re.escape(k) + r'` · (.*)$', text, re.M)
        if not line:
            raise ValueError(f'{Path(result).parent.name}: no fact {k}.')
        quote = re.match(r'[^:]*: "(.*)"[.;,]?\s+Locator', line[1])
        rows = re.match(r'[^:]*:\s*(.*?)\.?\s+Locator:', line[1])
        if quote:
            out.append(f'"{quote[1]}" ({k})')
        elif rows:
            out.append(f'{rows[1]} ({k})')
        else:
            raise ValueError(f'{Path(result).parent.name}: fact {k} has no quote or rows before its Locator.')
    return ' '.join(out)


def work_value(result, file, key):
    """A value from a work Run's own output: `key` (dotted) in a .json or .yaml file in its result/; `len(<key>)` counts
    the entries there (the six agents are the six keys of `metrics.b_by_model`, so a sentence's "6 AI agents" is read,
    not typed)."""
    path = Path(result) / file
    data = json.loads(path.read_text()) if path.suffix == '.json' else yaml.safe_load(path.read_text())
    count = re.fullmatch(r'len\((.+)\)', key.strip())
    for part in (count[1] if count else key).split('.'):
        data = data[int(part)] if isinstance(data, list) else data[part]
    return len(data) if count else data


def sentence_key(n):
    """A sentence id's place in reading order: `5`, `"5a"` and `"S5b"` sort as (5, ''), (5, 'a'), (5, 'b'). A sentence
    added between two others takes a letter (S2a after S2), so `for` may hold a string (JL 261020)."""
    m = re.match(r"S?(\d+)([a-z]*)$", str(n).strip())
    return (int(m.group(1)), m.group(2)) if m else (10 ** 9, str(n))


def _first(it):
    return min((sentence_key(n) for n in it.get('for') or []), default=(10 ** 9, ''))


def by_topic(cards):
    """The cards as topics: a needed item whose proposal names where it would be made sits in that place's card, a Run
    in a Task the Task's card (opened if the list has none), a new Task, Job or topic a card of its own named by it,
    whichever card it was written in; a need with no such proposal stays where it is. Items in reading order."""
    out, home = [], {}
    for c in cards:                       # one card per topic: two cards of the same Task are one
        c = dict(c, items=list(c['items']))
        key = (c['kind'], c.get('source'))
        if c.get('source') and key in home:
            home[key]['items'] += c['items']
            continue
        if c.get('source'):
            home[key] = c
        out.append(c)
    for c in list(out):
        keep = []
        for it in c['items']:
            p = it.get('propose') or {}
            to = str(p.get('in') or '')
            if not it.get('need') or not to:
                keep.append(it)
                continue
            if p.get('level', 'task') == 'run' and re.fullmatch(r'b\d+\.j\d+\.t\d+', to):
                key, new = (c['kind'], to), {'kind': c['kind'], 'source': to, 'items': []}
            else:
                name = str(p.get('name') or '').replace('_', ' ').strip()
                key = (c['kind'], f"{to}+{p.get('level', 'task')}+{name}")
                new = {'kind': c['kind'], 'title': f"{name or 'new ' + p.get('level', 'task')} · to make in {to}",
                       'items': []}
            home.setdefault(key, new)
            if home[key] is c:
                keep.append(it)
                continue
            if home[key] is new:
                out.append(new)
            home[key]['items'].append(it)
        c['items'] = keep
    return [dict(c, items=sorted(c['items'], key=_first)) for c in out if c['items']]


def order(cards):
    """[(card, 'CITE 3')] in narrative order: the cards as topics (by_topic), by the first sentence each backs, CITE
    and VALUE in one sequence, numbered within their kind."""
    count, out = {}, []
    for card in sorted(by_topic(cards), key=lambda c: min(_first(it) for it in c['items'])):
        count[card['kind']] = count.get(card['kind'], 0) + 1
        out.append((card, f"{LABEL[card['kind']]} {count[card['kind']]}"))
    return out


def check(cards, project, sentences=None):
    """Every problem with a card list, one line each: unknown kind, an address or fact that does not resolve, an item
    with neither `run` nor `need`, an anchor whose words are not in its sentences."""
    problems = []
    for card, label in order(cards):
        if card['kind'] not in LABEL:
            problems.append(f"{label}: kind {card['kind']!r} is not cite or value.")
            continue
        src = card.get('source')
        try:
            if src:
                resolve(project, card['kind'], src)
        except ValueError as e:
            problems.append(f'{label}: {e}')
            continue
        for it in card['items']:
            where = f"{label} · S{','.join(map(str, it['for']))}"
            try:
                if it.get('run'):
                    res = resolve(project, card['kind'], f"{src}.{it['run']}")
                    if card['kind'] == 'cite':
                        paper(res)
                        if it.get('fact'):
                            facts(res, it['fact'])
                    elif it.get('key'):
                        work_value(res, it['file'], it['key'])
                elif not it.get('need') and not it.get('value'):
                    problems.append(f'{where}: an item needs `run`, `value` or `need`.')
            except (ValueError, KeyError, IndexError, FileNotFoundError, StopIteration) as e:
                problems.append(f'{where}: {e}')
            for phrase in it.get('anchor', []) if sentences else []:
                if not any(phrase in sentences.get(str(n), '') for n in it['for']):
                    problems.append(f'{where}: anchor "{phrase}" is not in its sentences.')
    return problems


LEVELS = ('run', 'task', 'job', 'topic')
MAKER = {'cite': {'run': 'haipipe-discovery', 'task': 'haipipe-discovery', 'job': 'haipipe-job', 'topic': 'haipipe-studio'},
         'value': {'run': 'haipipe-task', 'task': 'haipipe-task', 'job': 'haipipe-job', 'topic': 'haipipe-studio'}}


def proposals(cards, page):
    """One flagged proposal per needed item: (id, line). An item's `propose: {level, in, name}` says what to make;
    without it, a CITE need proposes a new discovery Task in the card's `propose_in` Job, a VALUE need a new work Task."""
    out = []
    for card, label in order(cards):
        for it in card['items']:
            if not it.get('need'):
                continue
            p = {'level': 'task', 'in': card.get('propose_in') or card.get('source') or '?', **(it.get('propose') or {})}
            if p['level'] not in LEVELS:
                raise ValueError(f"{label}: propose.level is one of {', '.join(LEVELS)}.")
            sents = ','.join(f'S{n}' for n in it['for'])
            slug = re.sub(r'[^a-z0-9]+', '-', it['need'].lower()).strip('-')[:40]
            pid = f'{page}-{sents}-{slug}'
            world = THEME[card['kind']]
            name = f" `{p['name']}`" if p.get('name') else ''
            line = (f"new {world} {p['level']}{name} in `{p['in']}` · proposed by evidence ({label}, {page} {sents}) · "
                    f"for: {it['need']} · made by {MAKER[card['kind']][p['level']]}")
            out.append((pid, line))
    return out


def write_proposals(path, items):
    """proposals.md: a checkbox per proposal, ticks kept by id across rewrites."""
    path = Path(path)
    ticked = set(re.findall(r'^- \[x\] .*?<!-- (.+?) -->$', path.read_text(encoding='utf-8'), re.M)) if path.is_file() else set()
    lines = ['Evidence proposals', '==================', '',
             'Written by haipipe-evidence `cards.py propose`; a person ticks [x] what to make. Nothing is made before',
             'the tick, and the level\'s own skill makes it. Ticks survive a rewrite; a proposal whose need is gone drops out.', '']
    lines += [f"- [{'x' if pid in ticked else ' '}] {line} <!-- {pid} -->" for pid, line in items]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(ticked & {pid for pid, _ in items})


def load(path, key=None):
    """The card list from evidence/cards.yaml (`evidence:` at the top), or from a face's yaml block under `key`; a card
    written as `kind: work` before 261020 reads as `value`."""
    path = Path(path)
    if path.suffix in ('.yaml', '.yml'):
        cards = yaml.safe_load(path.read_text(encoding='utf-8'))['evidence']
    else:
        block = re.search(r'```yaml\n(.*?)\n```', path.read_text(encoding='utf-8'), re.S)[1]
        cards = yaml.safe_load(block)[key]['evidence']
    return [dict(c, kind=OLD_KIND.get(c.get('kind'), c.get('kind'))) for c in cards]


def bib(cards, project, draft_text):
    """The page's citations as one .bib, in the order the draft's `## 3 · Draft` cites them: each key's entry copied as it
    is from the one-entry .bib of the discovery Run its CITE item names, a comment above it saying which Run and how the
    entry was checked (the Run's export, or composed from the source's page and waiting for a person to adopt it). A
    cited key no CITE item names is listed as missing. (t01_introduction v0.5, 261021: the page's .bib had 2 of 10.)"""
    where = {}
    for card in cards:
        if card.get('kind') != 'cite':
            continue
        for it in card.get('items', []):
            if it.get('cite') and it.get('run'):
                where[it['cite']] = (f"{card['source']}.{it['run']}", resolve(project, 'cite', f"{card['source']}.{it['run']}"))
    m = re.search(r'(?m)^## \d+ · Draft\b', draft_text)
    text = draft_text[m.end():] if m else draft_text
    keys = list(dict.fromkeys(k.strip() for g in re.findall(r'\\cite[pt]?\{([^}]*)\}', text) for k in g.split(',') if k.strip()))
    out = ["% The page's citations, in the order the text cites them, written by haipipe-evidence cards.py bib: each",
           "% entry is copied as it is from the one-entry .bib of the discovery Run its evidence card names; the comment",
           "% above it says which Run and how that entry was checked.", ""]
    missing = []
    for key in keys:
        if key not in where:
            missing.append(key)
            continue
        addr, res = where[key]
        entry = next(Path(res).glob('*.bib')).read_text(encoding='utf-8').strip()
        rt = Path(res) / 'runtime.yaml'
        status = (re.search(r'(?m)^status: (\S+)', rt.read_text(encoding='utf-8')) or [None, '?'])[1] if rt.is_file() else '?'
        how = ("composed field by field from the source's page; waits for a person to adopt it" if status == 'blocked'
               else "the Run's export, checked when the Run was made")
        out += [f"% {key} · Run {addr} · {status} · {how}", entry, ""]
    return "\n".join(out), keys, missing


def main():
    import argparse
    ap = argparse.ArgumentParser(description='Check an evidence card list.')
    ap.add_argument('cmd', choices=['check', 'propose', 'bib'])
    ap.add_argument('cards', help='evidence/cards.yaml, or a face .md with --key')
    ap.add_argument('--key', help='a face only: the yaml key holding `evidence:`')
    ap.add_argument('--sentences', help='a JSON object {"5": "sentence text"} to check anchors against')
    ap.add_argument('--page', help='the page name proposals cite (default: the folder that holds evidence/)')
    ap.add_argument('--write', action='store_true',
                    help='propose: write proposals.md beside cards.yaml; bib: write <task>/draft/evidence/bibex/<task>.bib')
    ap.add_argument('--draft', help='bib: the draft whose `## 3 · Draft` cites the keys')
    a = ap.parse_args()
    src = Path(a.cards).resolve()
    cards = load(src, a.key)
    home = src.parent.parent if src.parent.name == 'evidence' else src.parent
    sentences = json.loads(Path(a.sentences).read_text()) if a.sentences else None
    if a.cmd == 'bib':
        text, keys, missing = bib(cards, project_root(src), Path(a.draft).read_text(encoding='utf-8'))
        out = home / 'draft' / 'evidence' / 'bibex' / f'{home.name}.bib'
        if a.write:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding='utf-8')
        print(f"{'wrote' if a.write else 'would write'} {out.name}: {len(keys) - len(missing)} of {len(keys)} cited keys"
              + (f"; no CITE item for {', '.join(missing)}" if missing else ''))
        sys.exit(1 if missing else 0)
    if a.cmd == 'propose':
        items = proposals(cards, a.page or home.name)
        for pid, line in items:
            print('- [ ]', line)
        if a.write:
            out = src.parent / ('proposals.md' if src.parent.name == 'evidence' else 'evidence-proposals.md')
            kept = write_proposals(out, items)
            print(f'wrote {out.name}: {len(items)} proposals, {kept} already ticked')
        return
    problems = check(cards, project_root(src), sentences)
    for card, label in order(cards):
        print(f"{label:8} {card.get('source') or '(needs)':16} {len(card['items'])} items")
    print('\n'.join(problems) if problems else 'every address, fact and value resolves')
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
