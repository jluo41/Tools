"""delivery_bib.py: the paper's one bibliography, merged from each Page's Bib (merge_bib, latex_safe_entry, uncap_entry, duplicate_bib_works).
build_delivery.py runs this file inside its own namespace (_load_part), so BIB, BUILD_WARNINGS and the config come from there."""
from __future__ import annotations

import re


# ── bibliography ─────────────────────────────────────────────────────────────
def page_bib(p):
    """The Bib a Page's own LaTeX delivery cites: the export freezes it from the Page's
    selected, verified CITE Results at `delivery/latex/selected-bibliography/<page>.bib`."""
    return page_latex(p["dir"]) / "selected-bibliography" / f"{p['id']}.bib"


def page_draft_bib(p):
    """0.9.1 · the unverified Bib a `delivery: draft` Page's export writes beside its verified one."""
    return page_latex(p["dir"]) / "draft-bibliography" / f"{p['id']}.bib"


def citing_bib(p):
    """The Bib this build merges for a Page: its verified `page_bib`, else, when the paper
    opts in with `[evidence] draft_citations`, its draft Bib (a G4 blocker, never silent)."""
    # A Page's draft Bib holds its verified entries plus the unverified ones (workbench export
    # _draft_bibliography), so with draft_citations on it wins whenever it exists; taking the verified Bib
    # alone printed every unverified key as (?) (MISQ, 261022: 25 in the assembled draft).
    verified = page_bib(p)
    if not DRAFT_CITATIONS or not page_draft_bib(p).is_file():
        return verified
    return page_draft_bib(p)


def _missing_bib(p):
    return (f"{p['id']}: cited Page has no delivery/latex/selected-bibliography/{p['id']}.bib; "
            "regenerate its Page delivery from accepted CITE Results")


def require_page_bibs(pages):
    """Each printed Page that cites must carry its derived Bib (`page_bib`)."""
    for p in pages:
        if not p.get("included", p.get("ready", True)):
            continue
        fragment = page_latex(p["dir"]) / f"{p['id']}.tex"
        if (not citing_bib(p).is_file() and fragment.is_file()
                and re.search(r"\\cite\w*\*?(?:\[[^\]]*\])*\{", fragment.read_text(encoding="utf-8"))):
            raise RuntimeError(_missing_bib(p))


_URL_FIELDS = {"url", "doi", "eprint", "howpublished"}


_ACRONYM = re.compile(r"(?<![\w\\-])([\w-]*[A-Z][\w-]*[A-Z][\w-]*)(?![\w-])")


def protect_title_acronyms(title: str) -> str:
    """Brace every title word with two or more capitals (LLMs, CDC, GPT-4, BMJ) that is not
    already braced, so a style that lowercases titles (apalike) keeps it: the reference list
    printed "Online Reviews with llms" (0.8.4, Results CHECK 260928). Braced text is left alone."""
    out, depth, seg = [], 0, []
    for ch in title:
        if ch == "{":
            if depth == 0:
                out.append(_ACRONYM.sub(r"{\1}", "".join(seg))); seg = []
            depth += 1; out.append(ch)
        elif ch == "}" and depth:
            depth -= 1; out.append(ch)
        elif depth:
            out.append(ch)
        else:
            seg.append(ch)
    out.append(_ACRONYM.sub(r"{\1}", "".join(seg)))
    return "".join(out)


def latex_safe_entry(entry: str):
    r"""One Bib entry with every `&` LaTeX can typeset: `&amp;` (an HTML entity a Discovery
    Bib copied from a web page), a doubled `\\&`, or a bare `&` becomes `\&`; inside a
    url/doi field `&amp;` becomes a plain `&`. Returns (entry, what was fixed or "")."""
    out, fixed, i = [], set(), 0
    for m in re.finditer(r"(\w+)\s*=\s*\{", entry):
        if m.start() < i:
            continue
        start = m.end(); depth, j = 1, m.end()
        while j < len(entry) and depth:
            depth += {"{": 1, "}": -1}.get(entry[j], 0)
            j += 1
        value = entry[start:j - 1]
        if m.group(1).lower() in _URL_FIELDS:
            new = value.replace("&amp;", "&")
        else:
            new = re.sub(r"(?<!\\)&", r"\\&", value.replace("&amp;", "&").replace("\\\\&", "&"))
        if new != value:
            fixed.add("&amp;" if "&amp;" in value else "&")
        if m.group(1).lower() == "title":
            new = protect_title_acronyms(new)   # presentation, not a source defect: no warning
        out.append(entry[i:start] + new)
        i = j - 1
    out.append(entry[i:])
    return "".join(out), " and ".join(sorted(fixed))



def uncap_entry(body: str):
    """A title or author typed in capitals in the source record (Crossref returns some old papers so: "THE TREATMENT
    OF TIES IN RANKING PROBLEMS", "KENDALL, M. G.") printed in capitals in the references (JL 261023: "make it as ready
    as possible"). An all-capitals title becomes sentence case and an all-capitals surname gets an initial capital;
    the field is changed only when it has no lowercase letter at all. Returns (body, what changed)."""
    changed = []
    def field(name, fix):
        nonlocal body
        m = re.search(r"(\b" + name + r"\s*=\s*\{)((?:[^{}]|\{[^{}]*\})*)(\})", body, re.I)
        if not m:
            return
        value = m.group(2)
        letters = [c for c in re.sub(r"\band\b", "", value) if c.isalpha()]   # an author list's "and" is lowercase
        if len(letters) < 4 or any(c.islower() for c in letters):
            return
        body = body[:m.start(2)] + fix(value) + body[m.end(2):]
        changed.append(name)
    def sentence(v):
        v = v.lower()
        return re.sub(r"(^\W*\w|[:.?!]\s+\w)", lambda m: m.group(0).upper(), v)
    field("title", sentence)
    field("author", lambda v: re.sub(r"[A-Za-z][A-Za-z'-]+", lambda m: m.group(0) if m.group(0) == "and" else
                                     "-".join(w.capitalize() for w in m.group(0).split("-")), v))
    return body, changed

def merge_bib(pages):
    seen, out, bodies = set(), [], {}
    for p in pages:
        if not p.get("included", p.get("ready", True)):
            continue  # DRAFT stubs do not print the excluded Page's citations.
        # Merge the same derived bibliography used by this Page's LaTeX delivery.
        # Citation authority remains its accepted CITE Results. Never read the
        # retired Outline/flat bibex lanes or substitute a paper-wide seed Bib.
        b = citing_bib(p)
        if b.is_file() and b == page_draft_bib(p):
            DRAFT_CITED.append(p["id"])
        if not b.is_file():
            fragment = page_latex(p["dir"]) / f"{p['id']}.tex"
            if fragment.is_file() and re.search(r"\\cite\w*\*?(?:\[[^\]]*\])*\{", fragment.read_text(encoding="utf-8")):
                raise RuntimeError(_missing_bib(p))
        for b in [b] if b.is_file() else []:
            txt = b.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", txt):
                key = m.group(1)
                start = m.start(); depth = 0; i = txt.index("{", start)
                for j in range(i, len(txt)):
                    if txt[j] == "{": depth += 1
                    elif txt[j] == "}":
                        depth -= 1
                        if depth == 0: break
                body, fixed = latex_safe_entry(txt[start:j+1])
                body, uncapped = uncap_entry(body)
                if re.search(r"(?i)\bdoi\s*=", body):   # a DOI and a URL print the same link twice (JL 261104, the MISQ references)
                    body = re.sub(r"(?i),?\s*url\s*=\s*\{[^{}]*\}", "", body)
                if uncapped:
                    BUILD_WARNINGS.append(f"bib key {key} ({p['id']}): {' and '.join(uncapped)} in capitals, printed in normal case")
                if fixed:
                    BUILD_WARNINGS.append(f"bib key {key} ({p['id']}): {fixed} written as LaTeX; fix the source Bib")
                norm = re.sub(r"\s+", " ", body).strip()
                if key not in seen:
                    seen.add(key); out.append(body); bodies[key] = (norm, p["id"])
                elif bodies[key][0] != norm:
                    # same key, different entry: the first page's version is printed, the
                    # other page's citation data silently disappears unless someone is told
                    BUILD_WARNINGS.append(f"bib key {key} differs between {bodies[key][1]} and {p['id']}; {bodies[key][1]}'s entry kept")
    unverified = (f"% UNVERIFIED draft-bibliography/<page>.bib merged for: {', '.join(DRAFT_CITED)}\n"
                  if DRAFT_CITED else "")
    BIB.write_text(f"% merged by {ENGINE_TAG} from each Page's delivery/latex/selected-bibliography/<page>.bib · do not edit\n"
                   + unverified + "\n" + "\n\n".join(out) + "\n", encoding="utf-8")
    return len(out)


def bib_entries(text):
    """(key, body) for every top-level @entry, brace-balanced so a nested {M}edicare is safe."""
    out = []
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", text):
        i = text.index("{", m.start()); depth = 0
        for j in range(i, len(text)):
            if text[j] == "{": depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0: break
        out.append((m.group(1), text[m.start():j + 1]))
    return out

def duplicate_bib_works(cited):
    """Two DIFFERENT keys for ONE work, which prints that work twice in the reference list.

    merge_bib()'s tooth above only sees a key COLLISION. Two pages that spell the same
    paper differently collide on nothing, so both reach \bibitem and apalike prints the
    same article as (2018a) and (2018b) with two entries in the list -- exactly what
    Buchmueller_2018 vs buchmueller2018pdmp did to §1 and §2 (JL 260908).

    Identity uses BOTH signals and UNIONS them, never one or the other: the hand-written
    entry usually carries no `doi` while its Crossref twin does, so a doi-first rule put
    dowell2016cdc and Dowell_2016 in different buckets and found nothing. Signals are the
    DOI and (first author's surname + 28 letters of the title, braces and case stripped so
    `{CDC} guideline` matches `CDC Guideline`). Returns (both_cited, staged_only) groups.
    """
    if not BIB.exists(): return [], []
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for key, body in bib_entries(BIB.read_text(encoding="utf-8", errors="replace")):
        me = ("key", key); find(me)
        doi = re.search(r"\b(?:doi|DOI)\s*=\s*[{\"]\s*([^}\"]+)", body)
        if doi: union(me, ("doi", doi.group(1).strip().rstrip(".").lower()))
        au = re.search(r"author\s*=\s*[{\"]([^,}\"]+)", body)
        ti = re.search(r"title\s*=\s*[{\"](.{0,60})", body, re.S)
        surname = re.sub(r"[^a-z-]", "", (au.group(1) if au else "?").lower())
        head = re.sub(r"[^a-z0-9]", "", (ti.group(1) if ti else "").lower())[:28]
        if surname and head: union(me, ("at", surname, head))
    groups = {}
    for node in list(parent):
        if node[0] == "key": groups.setdefault(find(node), []).append(node[1])
    both, staged = [], []
    for _root, keys in sorted(groups.items(), key=lambda kv: sorted(kv[1])):
        if len(keys) < 2: continue
        keys = sorted(keys)
        (both if len([k for k in keys if k in cited]) > 1 else staged).append(keys)
    return both, staged
