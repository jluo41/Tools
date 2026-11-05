"""Evidence cards: read a card list, find each Run it names, and say what is missing.

A card is one topic holding many items. CITE cards come from the Project's discovery/ world (someone else's paper,
and any value or figure the paper reports); VALUE cards come from its work/ world (a number one of our Runs wrote;
kind `work` until 261020, still read as `value`). The card format is in ../SKILL.md; the sibling skills
haipipe-evidence-cite and haipipe-evidence-work say how to find each kind.

A card's topic is its Task: a needed item joins the card of the Task its proposal would be made in (`order`), so no
card is a bag of "Sources still needed" (JL 261020: "cite 1's name is very weird ... make it into different cite with
the topic").

    from cards import load, resolve, title_of, paper, facts, work_value, order, check, proposals, LABEL, COLOR
    from cards import catalog, item_status, find_value, bind_proposals, adopt_bindings, lineage, tokens, same, agrees
    python cards.py check   <task>/evidence/cards.yaml [--sentences <file.json>]
    python cards.py propose <task>/evidence/cards.yaml [--page <name>] [--write]
    python cards.py propose <task>/evidence/cards.yaml --catalog <run>/result/values.yaml --source <task address>
                            --sentences <file.json> [--write] [--adopt]     bind a catalog's values (0.9.0)
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

VALUE bindings (0.9.0, JL 261103): an item may name a value of a catalog (a Run's result/values.yaml) by its id,
`value: RQ1-t01-002`, with `anchor:` words (a display's item: `display:` and `printed:`). `item_status` gives a bound
item its status, match, differs, missing, no anchor, owed or pending, at the printed precision with exact half-up
rounding; `check` reports a differs as a problem. `propose --catalog` finds each catalog value in the page's sentences
and adds a "bind VALUE <id> to S<n>" line to proposals.md; a person ticks it once and `--adopt` writes it as an item,
fixed from then on. `lineage` reads a value's checks: the work Run's values.csv `source` column through its Block's
src/inputs.yaml (`runs:` address, path, label; `typed:` stand-ins are screen reads).
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


def board_of(near):
    """The paper Board (the folder holding board.md) at or above `near`, else None."""
    for p in [Path(near).resolve(), *Path(near).resolve().parents] if near else []:
        if (p / 'board.md').is_file():
            return p
    return None


def resolve(project, kind, address, near=None):
    """bNN.jNN[.tNN[.rNN]] in the kind's world → its folder; a full Run address → that Run's result/ folder.

    jNN.tNN[.rNN] is a Task of the paper Board's own evidence Job (j01_evidence_display, j02_evidence_value; 261031),
    found in the Board that holds `near` (the cards file or its Task), since every paper Board has its own j01.
    A Run is found as tNN_*/runs/rNN_*/result (Discovery, standalone Task) or jNN_*/results/tNN_*/rNN_* (a Task
    whose Results sit in its Job)."""
    parts = address.split('.')
    if not 2 <= len(parts) <= 4 or not all(re.fullmatch(r'[bjtr]\d+', p) for p in parts):
        raise ValueError(f'{address}: an address is bNN.jNN, bNN.jNN.tNN, bNN.jNN.tNN.rNN or a paper Board\'s jNN.tNN[.rNN].')
    take = 3
    if parts[0].startswith('j'):
        world = board_of(near)
        if world is None:
            raise ValueError(f'{address}: a jNN.tNN address names a paper Board\'s evidence Task; no board.md above {near}.')
        take = 2
    else:
        world = Path(project) / THEME[kind]
    pattern = '/'.join(f'{p}_*' for p in parts[:take])
    found = list(world.glob(pattern))
    if len(found) != 1:
        raise ValueError(f'{address}: {len(found)} folders match in {world.name}/, need one.')
    if len(parts) <= take:
        return found[0]
    task = found[0]
    runs = list(task.glob(f'runs/{parts[take]}_*/result')) + list(task.parent.glob(f'results/{task.name}/{parts[take]}_*'))
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


def check(cards, project, sentences=None, near=None):
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
                resolve(project, card['kind'], src, near)
        except ValueError as e:
            problems.append(f'{label}: {e}')
            continue
        for it in card['items']:
            where = f"{label} · " + (it['display'] if it.get('display') else
                                     ','.join(f'S{n}' if re.fullmatch(r'\d+[a-z]*', str(n)) else str(n) for n in it.get('for') or []) or 'S')
            row = None
            try:
                if it.get('run'):
                    res = resolve(project, card['kind'], f"{src}.{it['run']}", near)
                    if card['kind'] == 'cite':
                        paper(res)
                        if it.get('fact'):
                            facts(res, it['fact'])
                    elif is_value_id(it.get('value')):
                        row = catalog_value(res, it['value'])
                    elif it.get('key'):
                        row = {'value': work_value(res, it['file'], it['key'])}
                elif not it.get('need') and not it.get('value'):
                    problems.append(f'{where}: an item needs `run`, `value` or `need`.')
            except (ValueError, KeyError, IndexError, FileNotFoundError, StopIteration) as e:
                problems.append(f'{where}: {e}')
            if not sentences or it.get('display'):
                continue
            text = ' '.join(sentences.get(str(n), '') for n in it.get('for') or [])
            for phrase in it.get('anchor', []):
                if phrase not in text:
                    problems.append(f'{where}: anchor "{phrase}" is not in its sentences.')
            if row is not None and card['kind'] == 'value':
                for printed, st, _ in item_status(it, row, text):
                    if st == 'differs':
                        problems.append(f'{where}: "{printed}" differs from its value {row.get("shown", row["value"])}.')
    return problems


# ── VALUE bindings (0.9.0, JL 261103): an item bound to a value of a catalog, its status, its lineage ──────────────
# A catalog is a Run's result/values.yaml, `values: {<key>: {id, value, shown, what, scale?, p?, checks, ...}}` (the
# paper's j02_evidence_value writes one per value Task; any work Run may). An item names a value by its id,
# `value: RQ1-t01-002` (a `value:` that is not an id stays what it was, a value stated in words), or by `file` + `key`.
ID = re.compile(r'^[A-Za-z][A-Za-z0-9]*-t\d+-\d{3}$')
STATUSES = ('match', 'differs', 'missing', 'no anchor', 'owed', 'pending')


def is_value_id(v):
    return isinstance(v, str) and bool(ID.match(v.strip()))


def catalog(path):
    """{id: row} of a catalog file (a Run's result/values.yaml); each row keeps its key as `key`."""
    data = yaml.safe_load(Path(path).read_text(encoding='utf-8')) or {}
    return {r['id']: dict(r, key=k) for k, r in (data.get('values') or {}).items() if isinstance(r, dict) and r.get('id')}


def catalog_value(result, value_id):
    rows = catalog(Path(result) / 'values.yaml')
    if value_id not in rows:
        raise ValueError(f'{Path(result).parent.name}: no value {value_id} in values.yaml.')
    return rows[value_id]


CITES = re.compile(r'\\(?:cite[pt]?\*?|ref|eqref|label)(?:\[[^\]]*\])*\{[^}]*\}')
TOKEN = re.compile(r'(?<![\w.])(?:[<>]\s*)?[−–-]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)')
NUMBER = re.compile(r'-?(?:\d[\d,]*(?:\.\d+)?|\.\d+)')


def tokens(sentence):
    """(printed, number, decimals, the 8 characters before it, the verbatim words) per number of a sentence; a range
    6.1-16.0 gives two; citation keys are not read."""
    s = CITES.sub(lambda m: ' ' * len(m.group(0)), sentence).replace('−', '-').replace('–', '-')
    out = []
    for m in TOKEN.finditer(s):
        raw = m.group(0)
        lt = raw.lstrip().startswith(('<', '>'))
        body = raw.lstrip('<> ')
        start = m.end() - len(body)
        if body.startswith('-') and start > 0 and s[start - 1].isdigit():
            body, start = body[1:], start + 1                 # the hyphen of a range, not a minus
        try:
            x = float(body.replace(',', ''))
        except ValueError:
            continue
        dec = len(body.split('.')[1]) if '.' in body else 0
        verbatim = sentence[m.start():m.end()].strip() if lt else sentence[start:m.end()]
        out.append((('<' if lt else '') + body, x, dec, s[max(0, m.start() - 8):m.start()], verbatim))
    return out


def same(x, dec, v, scale=1):
    """The value v (or v x scale), rounded half up to the printed decimals, is the printed number x."""
    from decimal import ROUND_HALF_UP, Decimal
    for w in {v, v * scale}:
        if dec >= 6 and abs(x - w) <= 1e-6 * max(1.0, abs(w)):
            return True
        if dec < 6 and float(Decimal(repr(float(w))).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP)) == x:
            return True
    return False


def agrees(printed, value, scale=1):
    """The printed words against the value: `< .001` is a bound; the first number is compared at its printed precision
    (exact half-up rounding); None when the words hold no number."""
    words = str(printed).replace('−', '-').replace('–', '-')
    bound = re.search(r'<\s*(\d*\.?\d+)', words)
    if bound and isinstance(value, (int, float)):
        return value < float(bound[1])
    m = NUMBER.search(words)
    if not m or not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    token = m[0].replace(',', '')
    return same(float(token), len(token.split('.')[1]) if '.' in token else 0, value, scale)


def item_status(it, row, text, scale=None):
    """[(printed, status, note)] for a VALUE item against its value row and the text it is bound to: owed (a need),
    no anchor (no words to check), missing (the words left the text), match or differs (the number at its printed
    precision), pending (the row says it waits for a Run; the note says what it would be)."""
    if it.get('need'):
        return [(' / '.join(it.get('anchor') or []), 'owed', it['need'])]
    scale = scale if scale is not None else (row or {}).get('scale', 1)
    out = []
    for printed in (it.get('printed') if it.get('display') else it.get('anchor')) or [None]:
        if printed is None:
            st = 'no anchor'
        elif printed not in text:
            st = 'missing'
        else:
            ok = agrees(printed, row.get('value'), scale)
            st = 'match' if ok else ('differs' if ok is False else 'no anchor')
        note = ''
        if row.get('pending') and st in ('match', 'differs'):
            st, note = 'pending', f"{row['pending']} (as printed it would be: {st})"
        out.append((printed or '', st, note))
    return out


def find_value(row, sentences, loose=False):
    """[(sentence id, verbatim words)] where a catalog value is printed. Guards: a P value (`p: true`) only after "P ="
    or "P <"; a whole number under 10 never; fewer than two significant digits and fewer than two decimals only when
    `loose`; one hit per sentence."""
    v, scale, is_p = row.get('value'), row.get('scale', 1), bool(row.get('p'))
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return []
    out = []
    for sid, text in sentences.items():
        for printed, x, dec, before, verb in tokens(text):
            if is_p != bool(re.search(r'\b[Pp]\s*[=<>]?\s*$', before.rstrip())):
                continue
            if not is_p and dec == 0 and abs(x) < 10:
                continue
            sig = len(printed.lstrip('<-0.').replace(',', '').replace('.', ''))
            if not is_p and not loose and sig < 2 and dec < 2:
                continue
            if (is_p and v < float(printed[1:])) if printed.startswith('<') else same(x, dec, v, scale):
                out.append((sid, verb))
                break
    return out


def bind_proposals(rows, sentences, page, source, run, cards, found=None):
    """The proposed bindings of a page, on the "Proposing what to make" path: [(id, line, (source, item))], one per
    catalog value printed in a sentence that no item binds yet. `found` may give the hits ({id: [(sid, words)]}, a
    caller's own finder); else find_value. A person ticks the line; adopt_bindings writes the ticked ones as items."""
    bound = {(str(it.get('value')), str(n)) for c in cards for it in c.get('items') or [] for n in it.get('for') or []}
    bound |= {(str(it.get('value')), str(it['display'])) for c in cards for it in c.get('items') or [] if it.get('display')}
    out = []
    for vid, row in rows.items():
        for sid, words in (found or {}).get(vid, None) or (find_value(row, sentences) if found is None else []):
            if (vid, str(sid)) in bound:
                continue
            disp = sid if str(sid).startswith('display:') else None
            item = ({'run': run, 'for': [], 'display': disp[8:], 'value': vid, 'printed': [words]} if disp else
                    {'run': run, 'for': [sid], 'value': vid, 'anchor': [words]})
            where = disp[8:] if disp else f'S{sid}' if re.fullmatch(r'\d+[a-z]*', str(sid)) else str(sid)
            pid = f"bind-{vid}-{re.sub(r'[^A-Za-z0-9]+', '-', where).strip('-')}"
            line = (f"bind VALUE {vid} ({row.get('shown', row.get('value'))}) to {page} {where} \"{words}\" · proposed by "
                    f"evidence (value search) · for: {row.get('what', row.get('key', ''))} · from {source}.{run}")
            out.append((pid, line, (source, item)))
    return out


def ticked(path):
    path = Path(path)
    return set(re.findall(r'^- \[x\] .*?<!-- (.+?) -->$', path.read_text(encoding='utf-8'), re.M)) if path.is_file() else set()


def adopt_bindings(cards_path, proposals, only=None):
    """Write the ticked binding proposals (or the ids in `only`) into cards.yaml as VALUE items of the card of their
    source; returns how many. A binding once written is fixed: no search rewrites it."""
    cards_path = Path(cards_path)
    take = ticked(cards_path.parent / 'proposals.md') if only is None else set(only)
    chosen = [(src, it) for pid, _, (src, it) in proposals if pid in take]
    if not chosen:
        return 0
    text = cards_path.read_text(encoding='utf-8') if cards_path.is_file() else 'evidence: []\n'
    head = ''.join(ln + '\n' for ln in text.splitlines() if ln.startswith('#')) if text.startswith('#') else ''
    doc = yaml.safe_load(text) or {'evidence': []}
    ev = doc.setdefault('evidence', []) or []
    doc['evidence'] = ev
    for src, it in chosen:
        card = next((c for c in ev if c.get('kind') == 'value' and c.get('source') == src), None)
        if card is None:
            card = {'kind': 'value', 'source': src, 'items': []}
            ev.append(card)
        card['items'].append(it)
    cards_path.parent.mkdir(parents=True, exist_ok=True)
    cards_path.write_text(head + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120), encoding='utf-8')
    return len(chosen)


def lineage(run_dir, file, where=None, project=None):
    """The Runs behind a value a work Run returned: the `source` cell of its row in `file` (a .csv; `where` picks the
    row by {column: value}), read through the work Block's `src/inputs.yaml`: a key of its `runs:` (address, path from
    work/, label), `typed:"<file>"` (a typed stand-in, a screen read, labelled by `typed:`), or a bNN.jNN.tNN.rNN
    address. Returns (checks, has_source): each check {address, folder, name[, typed: True]}; has_source is None when
    the file is not a .csv, False when its row has no `source`."""
    import csv
    run_dir = Path(run_dir)
    path = run_dir / 'result' / file
    if path.suffix != '.csv' or not path.is_file():
        return [], None
    with path.open(newline='', encoding='utf-8') as f:
        rows = [r for r in csv.DictReader(f)
                if all(str(r.get(c, '')).strip() in [str(x) for x in (w if isinstance(w, list) else [w])] for c, w in (where or {}).items())]
    if not rows or 'source' not in rows[0]:
        return [], False
    src = ' ; '.join(str(r.get('source') or '') for r in rows)
    block = next((p for p in run_dir.parents if re.match(r'b\d+_', p.name)), None)
    inputs = block / 'src' / 'inputs.yaml' if block else None
    keys = (yaml.safe_load(inputs.read_text(encoding='utf-8')) or {}) if inputs and inputs.is_file() else {}
    project = Path(project) if project else project_root(run_dir)
    out, seen = [], set()
    for token in re.split(r'[;,]\s*|\s+', src):
        name = token.split(':')[0].strip('"()')
        hit = None
        if name in (keys.get('runs') or {}):
            info = keys['runs'][name]
            hit = {'address': info.get('address', name), 'folder': project / 'work' / info['path'] if info.get('path') else None,
                   'name': info.get('label', info.get('says', name))}
        elif name == 'typed' and ':' in token and block is not None:
            rel = token.split(':', 1)[1].strip('"')
            lab = next((v.get('label') for v in (keys.get('typed') or {}).values() if v.get('path') == rel), None)
            hit = {'address': 'typed ' + Path(rel).name, 'folder': block / rel, 'name': lab or 'typed stand-in ' + Path(rel).name,
                   'typed': True}
        else:
            m = re.search(r'\bb(\d+)\.j(\d+)\.t(\d+)\.r(\d+)\b', token)
            if m:
                b, j, t, r = m.groups()
                found = sorted(project.glob(f'work/b{b}_*/j{j}_*/t{t}_*/runs/r{r}_*'))
                hit = {'address': m.group(0), 'folder': found[0] if len(found) == 1 else None,
                       'name': title_of(found[0].parent.parent) if len(found) == 1 else 'not found in work/'}
        if hit and hit['address'] not in seen:
            seen.add(hit['address'])
            out.append(hit)
    return out, bool(src.strip(' ;'))


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
    ap.add_argument('--catalog', help='propose: a Run\'s result/values.yaml whose values to bind to the --sentences')
    ap.add_argument('--source', help='propose --catalog: the catalog Run\'s Task address (bNN.jNN.tNN, or a paper Board\'s jNN.tNN)')
    ap.add_argument('--run', default='r01', help='propose --catalog: the catalog Run, rNN (default r01)')
    ap.add_argument('--adopt', action='store_true', help='propose --catalog: write the ticked bindings into cards.yaml')
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
        binds = []
        if a.catalog:
            if not (a.source and sentences):
                ap.error('propose --catalog needs --source and --sentences')
            binds = bind_proposals(catalog(a.catalog), sentences, a.page or home.name, a.source, a.run, cards)
            if a.adopt:
                n = adopt_bindings(src, binds)
                print(f'adopted {n} ticked bindings into {src.name}')
                cards = load(src, a.key)
                binds = bind_proposals(catalog(a.catalog), sentences, a.page or home.name, a.source, a.run, cards)
        items += [(pid, line) for pid, line, _ in binds]
        for pid, line in items:
            print('- [ ]', line)
        if a.write:
            out = src.parent / ('proposals.md' if src.parent.name == 'evidence' else 'evidence-proposals.md')
            kept = write_proposals(out, items)
            print(f'wrote {out.name}: {len(items)} proposals, {kept} already ticked')
        return
    problems = check(cards, project_root(src), sentences, near=src)
    for card, label in order(cards):
        print(f"{label:8} {card.get('source') or '(needs)':16} {len(card['items'])} items")
    print('\n'.join(problems) if problems else 'every address, fact and value resolves')
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
