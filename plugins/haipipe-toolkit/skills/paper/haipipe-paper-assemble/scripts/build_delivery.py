#!/usr/bin/env python3
r"""build_delivery.py · the canonical delivery engine of haipipe-paper-assemble.

One engine for every paper (260908, after three fixes were found paper-locally
and would otherwise be re-invented by each copy). The pages own the words: the
engine reads each Section Page's body fragment <page>/delivery/latex/<page>.tex
in the Story's compile order (the `haipipe:compile-order` block), copies
fragments, display floats and bibliographies into delivery/latex/, generates
master.tex, compiles it, converts Word, writes delivery/display-register.md and
one build-manifest.json. Nothing here is a source of record.

How a paper calls it — its delivery/build.py is a thin wrapper (see
ref/build.py.wrapper) that sets HAIPIPE_PAPER_BUILD_CONFIG to its own
paper-build.toml and execs this file, so a fix here reaches every paper:

  .venv/bin/python delivery/build.py                 build (DRAFT unless every page is ready)
  .venv/bin/python delivery/build.py send RD02       copy every declared output into that Round's sent/
  .venv/bin/python delivery/build.py release RD01    copy every declared output into that Round's released/

Three behaviors this engine guarantees, each with a tooth in tests/:
  A  a display cited by a fragment is printed ONCE (md2tex already embeds it as
     a float; the master never re-inputs it)               DEDUPE_EMBEDDED_FLOATS
  B  a not-ready page keeps its number: a real \section{<its own title>} from
     the page's H1, never an unnumbered "[NOT READY]"       page_heading()
  C  delivery/display-register.md counts what the MASTER prints, in \input
     order, and compares with what each unit's README declares  display_register()
"""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys, tomllib
from datetime import datetime
from pathlib import Path

# ── where am I · which paper ────────────────────────────────────────────────
# A wrapper execs this file inside its own module and pre-sets __engine_dir__;
# a direct call resolves everything from this file and the environment.
ENGINE_DIR = Path(globals().get("__engine_dir__") or Path(__file__).resolve().parent)
DOCX_ENGINE = ENGINE_DIR / "latex_room_to_docx.py"
def _engine_version():
    skill = ENGINE_DIR.parent / "SKILL.md"
    if skill.exists():
        m = re.search(r'^\s*version:\s*"([^"]+)"', skill.read_text(encoding="utf-8"), re.M)
        if m: return m.group(1)
    return "?"
ENGINE_VERSION = _engine_version()
ENGINE_TAG = f"haipipe-paper-assemble {ENGINE_VERSION} · scripts/build_delivery.py"
_cfg_env = os.environ.get("HAIPIPE_PAPER_BUILD_CONFIG")
CONFIG_PATH = Path(_cfg_env).expanduser().resolve() if _cfg_env else Path(__file__).resolve().with_name("paper-build.toml")
if not CONFIG_PATH.exists():
    sys.exit(f"paper-build.toml not found: {CONFIG_PATH} (set HAIPIPE_PAPER_BUILD_CONFIG or run through delivery/build.py)")
HERE = CONFIG_PATH.parent                              # <paper>/delivery/
ROOT = HERE.parent                                     # the paper
CFG = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
DEDUPE_EMBEDDED_FLOATS = True   # behavior A · tests flip this to prove the register catches the double print

def rel(p): return (HERE / p).resolve()
LATEX = rel(CFG["source"]["room"])
SEC = LATEX / CFG["source"]["sections"]
APP = LATEX / CFG["source"].get("appendices", "appendices")
DISP = LATEX / CFG["source"]["displays"]
BIB = LATEX / CFG["source"]["bibliography"]
MASTER = LATEX / CFG["source"]["master"]
OUT = CFG["outputs"]
# 0.6.1 · paper-level switches, all opt-in through paper-build.toml (JL 260908, Paper-AgreeableOpioid-Jama):
#   [evidence] draft_includes_unready = true   a DRAFT prints every page that has a body fragment; the page's
#                                              not-ready reasons stay in build-manifest.json and the display
#                                              register, never inside the reader's PDF/DOCX (JL 260908)
#   [source]   preamble = "preamble.tex"       a paper-owned preamble file beside paper-build.toml, inlined
#                                              into the generated master (packages, column types, unicode maps)
#   [paper]    venue_profile = "jama-internal-medicine"  title-page center block, JAMA section boundaries,
#                                              and the page's own \section*{Key Points}/\section*{Abstract} kept
DRAFT_INCLUDES_UNREADY = bool(CFG.get("evidence", {}).get("draft_includes_unready", False))
VENUE_PROFILE = str(CFG["paper"].get("venue_profile", "")).lower()
JAMA = VENUE_PROFILE == "jama-internal-medicine"
PREAMBLE_FILE = rel(CFG["source"]["preamble"]) if CFG.get("source", {}).get("preamble") else None

# ── venue profile · presentation only, never claims (0.7.0) ──────────────────
# profiles/<name>.toml carries the desk's typography; [profile] in paper-build.toml
# may override single keys. The [latex] table drives write_master(); the flat keys
# drive scripts/latex_room_to_docx.py. Shipped: jama-internal-medicine, misq.
def load_profile(name: str) -> dict:
    prof = {}
    if name:
        path = ENGINE_DIR.parent / "profiles" / f"{name}.toml"
        if not path.exists(): sys.exit(f"venue profile not found: {path}")
        prof = tomllib.loads(path.read_text(encoding="utf-8"))
    inline = CFG.get("profile", {})
    if isinstance(inline, dict): prof.update(inline)
    return prof
PROFILE = load_profile(VENUE_PROFILE)
_L = PROFILE.get("latex", {}) if isinstance(PROFILE.get("latex"), dict) else {}
LATEX_SPACING = str(_L.get("spacing", "onehalf"))            # single · onehalf · double
LATEX_BIBSTYLE = str(_L.get("bibstyle", "apalike"))
LATEX_DISPLAYS = str(_L.get("displays", "inline"))            # inline · end (endfloat: every float after the text)
LATEX_APPENDIX_NEWPAGE = bool(_L.get("appendix_newpage", False))
LATEX_TITLE_PAGE = str(_L.get("title_page", "inline"))        # inline · separate (blind title page alone)
LATEX_ABSTRACT_PAGE = bool(_L.get("abstract_page", False))    # abstract (+ keywords) alone on its page
LATEX_RUNNING_HEAD = bool(_L.get("running_head", True))       # False: header carries only the DRAFT word while drafting

# ── document-wide placement state (0.7.0) ────────────────────────────────────
# A display prints ONCE in the whole document, not once per fragment: a page
# that \ref's a float another page embeds must not re-input it.
EMBEDDED_UNITS: set = set()      # units some included fragment embeds as a real float
PLACED_FLOATS: set = set()       # units the master already \input after a fragment
BUILD_WARNINGS: list = []        # document-level warnings (bib collisions, …)

def reset_placement():
    EMBEDDED_UNITS.clear(); PLACED_FLOATS.clear(); BUILD_WARNINGS.clear()

def prescan_embedded(pages):
    """record every unit any INCLUDED fragment embeds, before any fragment is placed."""
    for p in pages:
        if p.get("included", p["ready"]) and p["fragment"].exists():
            raw = p["fragment"].read_text(encoding="utf-8", errors="replace")
            EMBEDDED_UNITS.update(re.findall(r"displays?/([^/}]+)/", raw))   # raw page path (display/) or final room path (displays/)

# ── order ─────────────────────────────────────────────────────────────────────
ORDER_BLOCK = re.compile(r"<!--\s*haipipe:compile-order:start\s*-->(.*?)<!--\s*haipipe:compile-order:end\s*-->", re.S)
OUTLINE_VERSION = re.compile(r"-outline-v([0-9]+(?:\.[0-9]+)*)\.md$")

def outline_key(path: Path):
    match = OUTLINE_VERSION.search(path.name)
    return tuple(int(part) for part in match.group(1).split(".")) if match else ()

def latest_outline(group: Path, pid: str):
    candidates = list((group / pid / "outline").glob(f"{pid}-outline-v*.md"))
    superseded = set()
    for plan in candidates:
        header = re.split(r"(?m)^##\s", plan.read_text(encoding="utf-8"), maxsplit=1)[0]
        superseded.update(re.findall(r"(?m)^supersedes:[ \t]*(v[0-9]+(?:\.[0-9]+)*)[ \t]*$", header))
    current = [plan for plan in candidates
               if "v" + ".".join(map(str, outline_key(plan))) not in superseded]
    if candidates and not current:
        raise RuntimeError(f"ambiguous outline lineage for {pid}: no current revision")
    return max(current, key=outline_key) if current else None

def read_order():
    """(main ids, appendix ids, source) from the Story's compile-order block."""
    src = rel(CFG["pages"]["order"]); text = src.read_text(encoding="utf-8")
    main, appx = [], []
    blocks = list(ORDER_BLOCK.finditer(text))
    starts = re.findall(r"<!--\s*haipipe:compile-order:start\s*-->", text)
    ends = re.findall(r"<!--\s*haipipe:compile-order:end\s*-->", text)
    if len(blocks) != 1 or len(starts) != 1 or len(ends) != 1:
        raise RuntimeError(
            f"{src.relative_to(ROOT)} must contain exactly one haipipe:compile-order block"
        )
    blk = blocks[0]
    lane = None
    seen_lanes, seen_ids = set(), set()
    for line in blk.group(1).splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s in ("main:", "appendix:"):
            lane = s[:-1]
            if lane in seen_lanes:
                raise RuntimeError(f"duplicate compile-order lane: {lane}")
            seen_lanes.add(lane)
            continue
        m = re.match(r"-\s*(S-[A-Za-z0-9-]+)\s*$", s)
        if not m or lane is None:
            raise RuntimeError(f"invalid compile-order entry: {s}")
        pid = m.group(1)
        if pid in seen_ids:
            raise RuntimeError(f"duplicate compile-order Section: {pid}")
        seen_ids.add(pid)
        (main if lane == "main" else appx).append(pid)
    if not main:
        raise RuntimeError(
            f"{src.relative_to(ROOT)} compile-order block must declare main Sections"
        )
    source = f"compile-order block · {src.relative_to(ROOT)}"
    return main, appx, source

def sha(p: Path): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def purge_retired_delivery_receipts(value):
    """Remove deprecated delivery-QA keys before carrying a prior manifest forward."""
    retired = {"buildqa", "qareport", "deliveryqa", "deliveryquality",
               "deliveryqualityassurance"}
    if isinstance(value, dict):
        for key in list(value):
            normalized = re.sub(r"[-_ ]", "", str(key)).lower()
            if normalized in retired:
                del value[key]
            else:
                purge_retired_delivery_receipts(value[key])
    elif isinstance(value, list):
        for item in value:
            purge_retired_delivery_receipts(item)

# ── one page ──────────────────────────────────────────────────────────────────
def inspect(pid: str, group: Path):
    d = group / pid
    frag = d / "delivery" / "latex" / f"{pid}.tex"
    pdfs = [d / "delivery" / "latex" / f"{pid}-complete.pdf", d / "delivery" / "latex" / f"{pid}.pdf"]
    units = sorted((d / "outline" / "evidence" / "display").glob("*/")) if (d / "outline" / "evidence" / "display").exists() else []
    reasons = []
    if not d.exists(): reasons.append("page folder missing")
    plan = latest_outline(group, pid)
    outline = None
    if plan is not None:
        plan_text = plan.read_text(encoding="utf-8", errors="replace")
        header = re.split(r"(?m)^##\s", plan_text, maxsplit=1)[0]
        approvals = re.findall(r"(?m)^approved:[ \t]*(.*)$", header)
        declarations = re.findall(r"(?m)^outline-version:[ \t]*(.*)$", header)
        version = "v" + ".".join(str(part) for part in outline_key(plan))
        outline = {
            "path": str(plan.relative_to(ROOT)), "version": version,
            "approval": approvals[0].strip() if len(approvals) == 1 else None,
            "sha256": hashlib.sha256(plan.read_bytes()).hexdigest(),
        }
        if declarations and (len(declarations) != 1 or declarations[0].strip() != version):
            reasons.append(f"outline version does not match {plan.name}")
    if plan is None or not outline_key(plan) or outline_key(plan)[0] < 1:
        reasons.append("outline not approved (no v1.x)")
    elif not outline["approval"] or not outline["approval"].startswith("✅"):
        reasons.append(f"outline not approved (latest {plan.name} has no unambiguous approval)")
    if not frag.exists(): reasons.append("no body fragment delivery/latex/<page>.tex")
    if not any(p.exists() for p in pdfs): reasons.append("no page PDF")
    # 0.6.2 (JL 260908, Paper-MISQ-Board): a display unit gates the page only if
    # the page CITES it and the unit is LIVE. An uncited folder, or a unit folded
    # into another (state 🟣) or retired, is dead weight, not a gate; before this
    # rule S-Display-3a-funnel (folded, cited by nothing) blocked a fully written
    # §4 on a missing preview.pdf.
    frag_text = frag.read_text(encoding="utf-8", errors="replace") if frag.exists() else ""
    md_path = d / f"{pid}.md"
    md_text = md_path.read_text(encoding="utf-8", errors="replace") if md_path.exists() else ""
    cited, folded, uncited = [], [], []
    for u in units:
        state = unit_state(u)
        if state != "live":
            folded.append(f"{u.name} ({state})"); continue
        if unit_is_cited(u, frag_text, md_text): cited.append(u)
        else: uncited.append(u.name)
    missing_prev = [u.name for u in cited if not (u / "preview.pdf").exists()]
    if missing_prev: reasons.append(f"display preview.pdf missing for cited unit: {', '.join(missing_prev)}")
    warnings = []
    if folded: warnings.append(f"display units not gating (folded/retired): {', '.join(folded)}")
    if uncited: warnings.append(f"display units not gating (cited by nothing): {', '.join(uncited)}")
    # a fragment is DERIVED from the page .md by the LaTeX lane; when the .md is
    # newer the fragment silently prints yesterday's words. Reported, not a
    # blocker: mtimes are unreliable after a clone or a bulk rename sweep.
    if frag.exists() and md_path.exists() and md_path.stat().st_mtime > frag.stat().st_mtime + 1:
        warnings.append("fragment may be stale: the page .md is newer than delivery/latex/<page>.tex; rerun the LaTeX lane")
    return {"id": pid, "dir": d, "fragment": frag, "units": units, "cited_units": cited,
            "ready": not reasons, "reasons": reasons, "warnings": warnings,
            "sha256": sha(frag) if frag.exists() else None, "outline": outline}


def unit_state(u: Path) -> str:
    """'live' unless the unit's own records say it is folded (state 🟣) or retired."""
    for f in [u / "README.md", *sorted(u.glob("*.md"))]:
        if not f.exists(): continue
        t = f.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?m)^state:\s*🟣", t): return "folded"
        m = re.search(r"(?ms)^## Placement\s*\n(.*?)(?=^## |\Z)", t)
        if m and re.search(r"\b(retired|folded into|no standalone display)\b", m.group(1), re.I): return "retired"
    return "live"


def unit_is_cited(u: Path, frag_text: str, md_text: str) -> bool:
    """the page names the unit in its fragment or its .md, or \\ref's one of the unit's labels."""
    if u.name in frag_text or u.name in md_text: return True
    ft = u / "float.tex"
    if ft.exists():
        for lab in re.findall(r"\\label\{([^}]+)\}", ft.read_text(encoding="utf-8", errors="replace")):
            if re.search(r"\\ref\{" + re.escape(lab) + r"\}", frag_text): return True
    return False


def build_readiness(pages, unresolved=(), latex_rc=None, docx_rc=None):
    """Report mechanical checks without treating them as the human G4 gate.

    This adapter does not yet validate current Page CHECK/evidence bindings or
    an exact-build human submission decision. It must keep that gap visible;
    adding a config flag or finding all PDFs does not close it.
    """
    blockers = [
        "G4 unverified: current Page CHECK closure, accepted evidence bindings, "
        "and exact-build human submission approval are not validated by this adapter"
    ]
    if not pages:
        blockers.append("no Sections admitted")
    elif any(not page["ready"] for page in pages):
        blockers.append("one or more Section milestones are not ready")
    if unresolved:
        blockers.append("unresolved references remain")
    if latex_rc != 0:
        blockers.append("LaTeX rendering failed or has not been verified")
    if docx_rc != 0:
        blockers.append("Word rendering failed or has not been verified")
    return {"status": "DRAFT", "blockers": blockers}

# ── displays ─────────────────────────────────────────────────────────────────
def all_units(pages):
    for p in pages:
        for u in p["units"]:
            yield p["id"], u

def label_index(pages):
    idx = {}
    for pid, u in all_units(pages):
        ft = u / "float.tex"
        if ft.exists():
            for lab in re.findall(r"\\label\{([^}]+)\}", ft.read_text(encoding="utf-8", errors="replace")):
                idx.setdefault(lab, (pid, u))
    return idx

def copy_unit(u: Path) -> str:
    """copy one display unit into latex/displays/<unit>/ · returns the unit name"""
    dst = DISP / u.name; dst.mkdir(parents=True, exist_ok=True)
    fig = u / "assets" / "figure.pdf"
    if not fig.exists(): fig = u / "figure.pdf"                  # flat unit layout (0.6.1)
    if not fig.exists(): fig = u / "preview.pdf"
    if fig.exists(): shutil.copy2(fig, dst / "figure.pdf")
    tbs = list((u / "assets").glob("table-body*.tex")) if (u / "assets").exists() else []
    tbs += list(u.glob("table-body*.tex"))                       # flat unit layout (0.6.1)
    for tb in tbs:
        shutil.copy2(tb, dst / tb.name)
    ft = u / "float.tex"
    if ft.exists():
        t = ft.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"(\\includegraphics(?:\[[^\]]*\])?)\{[^}]*\}", rf"\1{{displays/{u.name}/figure.pdf}}", t)
        t = re.sub(r"\\input\{[^}]*?(table-body[^}/]*)\}", rf"\\input{{displays/{u.name}/\1}}", t)
        (dst / "float.tex").write_text(t, encoding="utf-8")
    return u.name

def place_fragment(p, dest_dir: Path, labels, unresolved):
    """copy the fragment, retarget its \\input paths, return the list of floats to \\input after it"""
    t = p["fragment"].read_text(encoding="utf-8", errors="replace")
    def fix_input(m):
        path = m.group(1)
        mm = re.search(r"display/([^/]+)/(?:assets/)?([^/}]+?)(?:\.tex)?$", path)   # assets/ or flat; .tex optional
        if mm:
            unit, name = mm.groups()
            src = p["dir"] / "outline/evidence/display" / unit
            if src.exists(): copy_unit(src)
            return rf"\input{{displays/{unit}/{name}}}"
        return m.group(0)
    t = re.sub(r"\\input\{([^}]+)\}", fix_input, t)
    def fix_graphic(m):
        mm = re.search(r"display/([^/]+)/(?:assets/)?([^/}]+)$", m.group(2))
        if mm:
            unit, name = mm.groups()
            src = p["dir"] / "outline/evidence/display" / unit
            if src.exists(): copy_unit(src)
            return rf"\includegraphics{m.group(1) or ''}{{displays/{unit}/figure.pdf}}"
        return m.group(0)
    t = re.sub(r"\\includegraphics(\[[^\]]*\])?\{([^}]+)\}", fix_graphic, t)
    if p["id"].endswith("-Abstract") and not JAMA:
        # the generic Word engine wants a real abstract environment; the JAMA renderer instead
        # parses the page's own \section*{Key Points} and \section*{Abstract} headings (0.6.1)
        body = re.sub(r"^%.*\n", "", t, flags=re.M)                       # generator comments
        body = re.sub(r"\\section\*?\{Abstract\}\s*", "", body)        # the heading
        lines = [l for l in body.strip().splitlines()]
        if lines and not lines[0].startswith("\\") and len(lines[0].split()) <= 12:
            lines = lines[1:]                                             # stray title line from md2tex
        t = "\\begin{abstract}\n" + "\n".join(lines).strip() + "\n\\end{abstract}\n"
    (dest_dir / f"{p['id']}.tex").write_text(t, encoding="utf-8")
    EMBEDDED_UNITS.update(re.findall(r"displays/([^/}]+)/", t))
    floats = []
    for lab in dict.fromkeys(re.findall(r"\\ref\{([^}]+)\}", t)):
        hit = labels.get(lab)
        if hit:
            name = copy_unit(hit[1])
            # behavior A · md2tex already embeds a cited display as a real float
            # INSIDE the fragment, so re-inputting the unit's float/ after it printed
            # every display twice: Figure 1 = Figure 2, Table 1 = Table 4 (260908).
            # 0.7.0: once in the whole DOCUMENT, so a cross-page \ref never re-inputs
            # a float another page embeds, whichever page comes first.
            if DEDUPE_EMBEDDED_FLOATS and (name in EMBEDDED_UNITS or name in PLACED_FLOATS): continue
            if name not in floats:
                floats.append(name); PLACED_FLOATS.add(name)
        else:
            unresolved.append({"page": p["id"], "ref": lab})
    return floats

# ── bibliography ─────────────────────────────────────────────────────────────
def merge_bib(pages):
    seen, out, bodies = set(), [], {}
    for p in pages:
        # Page contract: the canonical evidence lane is the only bibliography source.
        lane = p["dir"] / "outline/evidence/bibex"
        for b in sorted(lane.glob("*.bib")) if lane else []:
            txt = b.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", txt):
                key = m.group(1)
                start = m.start(); depth = 0; i = txt.index("{", start)
                for j in range(i, len(txt)):
                    if txt[j] == "{": depth += 1
                    elif txt[j] == "}":
                        depth -= 1
                        if depth == 0: break
                body = txt[start:j+1]
                norm = re.sub(r"\s+", " ", body).strip()
                if key not in seen:
                    seen.add(key); out.append(body); bodies[key] = (norm, p["id"])
                elif bodies[key][0] != norm:
                    # same key, different entry: the first page's version is printed, the
                    # other page's citation data silently disappears unless someone is told
                    BUILD_WARNINGS.append(f"bib key {key} differs between {bodies[key][1]} and {p['id']}; {bodies[key][1]}'s entry kept")
    BIB.write_text(f"% merged by {ENGINE_TAG} from every page's outline/evidence/bibex/*.bib · do not edit\n\n" + "\n\n".join(out) + "\n", encoding="utf-8")
    return len(out)

# ── master ───────────────────────────────────────────────────────────────────
def write_master(main, appx, status, ready_n, total_n):
    title = CFG["paper"].get("title", CFG["paper"]["id"])
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    # the reader's document carries only the status word, for every profile (0.7.0; JL 260908
    # "the delivered pdf or word must be clean"); counts and the build time live in build-manifest.json
    header = status
    spacing_cmd = {"single": "\\singlespacing", "double": "\\doublespacing"}.get(LATEX_SPACING, "\\onehalfspacing")
    endfloat = "\\usepackage[nolists,tablesfirst,nomarkers]{endfloat}" if LATEX_DISPLAYS == "end" else "% displays inline at first reference"
    paper_preamble = ("% paper-owned preamble · " + PREAMBLE_FILE.name + "\n" + PREAMBLE_FILE.read_text(encoding="utf-8")) \
        if PREAMBLE_FILE and PREAMBLE_FILE.exists() else "% no paper preamble declared"
    if JAMA:   # the JAMA Word renderer parses a title-page center block, not \maketitle
        title_block = ("\\begin{document}\n\n\\begin{center}\n{\\Large\\bfseries " + title + "}\n\n\\vspace{1em}\n\n"
                       "[Authors blinded for review]\n\n\\vspace{0.5em}\n\\end{center}")
    else:
        title_block = "\\title{" + title + "}\n\\author{}\n\\date{}\n\\begin{document}\n\\maketitle"
        if LATEX_TITLE_PAGE == "separate":       # blind copy: the title alone on page 1
            title_block += "\n\\thispagestyle{empty}\n\\clearpage"
    head = rf"""% GENERATED by {ENGINE_TAG} on {stamp}
% The pages own the words. Edit a Section Page, then rebuild; never edit this file.
\documentclass[12pt]{{article}}
\usepackage[letterpaper,margin=1in]{{geometry}}
\usepackage{{fontspec}}
\IfFontExistsTF{{TeX Gyre Termes}}{{\setmainfont{{TeX Gyre Termes}}}}{{\IfFontExistsTF{{Times New Roman}}{{\setmainfont{{Times New Roman}}}}{{}}}}
\usepackage{{microtype}}
\usepackage[authoryear,round]{{natbib}}
\usepackage{{graphicx,booktabs,tabularx,multirow,amsmath,amssymb,setspace,caption,float,xcolor}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{fancyhdr}}
{endfloat}
\providecommand{{\displayroot}}{{displays/}}
{paper_preamble}
{spacing_cmd}
\setlength{{\parindent}}{{0.25in}}
\setlength{{\parskip}}{{0.35em}}
\graphicspath{{{{./}}}}
\pagestyle{{fancy}}\fancyhf{{}}
\fancyhead[L]{{\small {header}}}
\fancyfoot[C]{{\thepage}}
{title_block}
\thispagestyle{{fancy}}

"""
    body = []
    for p, floats in main:
        if p.get("included", p["ready"]) and p["id"].endswith("-Abstract"):
            body.append(rf"\input{{sections/{p['id']}}}")
            if LATEX_ABSTRACT_PAGE: body.append(r"\clearpage")   # abstract (+ keywords) alone on its page
            body.append(""); continue
        if p.get("included", p["ready"]):
            if JAMA:   # the JAMA Word renderer splits the body on these four headings
                kind = p["id"].rsplit("-Main-", 1)[-1].replace("-", " ")
                frag_txt = (SEC / f"{p['id']}.tex").read_text(encoding="utf-8", errors="replace")
                if kind in ("Introduction", "Methods", "Results", "Discussion") and not re.search(rf"\\section\{{{kind}\}}", frag_txt):
                    body.append(rf"\section{{{kind}}}")
            body.append(rf"\input{{sections/{p['id']}}}")
            body += [rf"\input{{displays/{f}/float}}" for f in floats]
        else:
            body.append(_stub(p))
        body.append("")
    tail = ["\\section*{Acknowledgments}", "\\noindent\\textit{[Acknowledgments, funding and disclosures are written at submission; this build is a draft.]}", "",
            "\\clearpage", "\\bibliographystyle{" + LATEX_BIBSTYLE + "}", "\\bibliography{reference}", "", "\\clearpage", "\\appendix", ""]
    if JAMA:   # JAMA supplements number their floats eTable 1… / eFigure 1…, restarting after the references
        tail += ["\\setcounter{table}{0}\\renewcommand{\\tablename}{eTable}\\renewcommand{\\thetable}{\\arabic{table}}",
                 "\\setcounter{figure}{0}\\renewcommand{\\figurename}{eFigure}\\renewcommand{\\thefigure}{\\arabic{figure}}", ""]
    for p, floats in appx:
        if LATEX_APPENDIX_NEWPAGE: tail.append(r"\clearpage")      # each lettered appendix on a new page
        if p.get("included", p["ready"]):
            tail.append(rf"\input{{appendices/{p['id']}}}")
            tail += [rf"\input{{displays/{f}/float}}" for f in floats]
        else:
            tail.append(_stub(p))
        tail.append("")
    MASTER.write_text(head + "\n".join(body) + "\n" + "\n".join(tail) + "\n\\end{document}\n", encoding="utf-8")

def _stub(p) -> str:
    """a not-ready page: its own numbered heading plus ONE neutral line. The reasons
    are build scaffolding and live in build-manifest.json and the display register,
    never in the reader's PDF/DOCX (JL 260908: "the delivered pdf or word must be clean")."""
    _, title = page_heading(p)
    return rf"\section{{{tex_text(title)}}}" + "\n" + r"\noindent\textit{[This section is not yet compiled into this build.]}"

# ── the page's own heading ───────────────────────────────────────────────────
# Every Section Page's H1 declares the number and title the paper intends:
#   "# S-MISQ-Main-Empirical-Strategy · §4 Empirical Strategy and Data"
#   "# S-MISQ-Appendix-Prompts · Appendix A · Agreeableness Prompt Specification"
# Nothing read it, so a NOT-READY page printed "[NOT READY] <page-id>" as an
# UNNUMBERED heading and every section after it slid one number down: Results
# printed as §4 while its own page says §5.
def page_heading(p):
    """(declared number, title) from the Section Page's H1; ('', id) if unreadable."""
    md = p["dir"] / f"{p['id']}.md"
    if not md.exists(): return "", p["id"]
    parts = [x.strip() for x in md.read_text(encoding="utf-8", errors="replace").splitlines()[0].lstrip("# ").split("·")]
    if len(parts) < 2: return "", p["id"]
    m = re.match(r"^§(\d+)\s+(.*)$", parts[1])
    if m: return m.group(1), m.group(2)
    m = re.match(r"^Appendix\s+([A-Z])$", parts[1])
    if m: return m.group(1), (parts[2] if len(parts) > 2 else parts[1])
    return "", parts[1]

def tex_text(value):
    return value.replace("\\", "").replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")

# ── display register ─────────────────────────────────────────────────────────
# Nothing else in this pipeline knows a display's paper-level number. The unit id
# digits (1a, 2a, 4al2) are a human memory aid, `\ref` only proves a label
# RESOLVES, and the printed number is whatever LaTeX counts at compile time — so
# it silently moves whenever a page's readiness changes. This register is the
# missing map: it counts what the master actually prints and compares that with
# what each unit CLAIMS in its README `## Placement`.
FLOAT_ENV = re.compile(r"\\begin\{(figure|table)\*?\}(.*?)\\end\{\1\*?\}", re.S)
PLACEMENT_NUM = re.compile(r"\b(Table|Figure)\s+([A-Z]?\d+)\b")
LABEL_CMD = re.compile(r"\\label\{([^}]+)\}")

def declared_number(unit):
    """the paper-level number a unit claims, read from its README ## Placement."""
    hits = list(ROOT.glob(f"B*/*/outline/evidence/display/{unit}/README.md"))
    if not hits: return None
    block = re.search(r"^## Placement\s*(.*?)(?=^## |\Z)",
                      hits[0].read_text(encoding="utf-8", errors="replace"), re.S | re.M)
    if not block or re.search(r"\bretired\b", block.group(1), re.I): return None
    m = PLACEMENT_NUM.search(block.group(1))
    return f"{m.group(1)} {m.group(2)}" if m else None

def label_to_unit():
    """which unit declares each label, read from the float.tex files this build copied."""
    out = {}
    for float_tex in sorted(DISP.glob("*/float.tex")):
        for lab in LABEL_CMD.findall(float_tex.read_text(encoding="utf-8", errors="replace")):
            out.setdefault(lab, float_tex.parent.name)
    return out

def display_register(main, appx):
    units, counters, rows = label_to_unit(), {"figure": 0, "table": 0}, []
    # Count from the FINAL master in \\input order, not from the fragments. Counting
    # fragments measured what a page CONTAINS, never what the document PRINTS, so it
    # stayed blind to a float the master \\input a second time -- the exact bug this
    # register exists to catch (proved by removing the dedupe and re-running).
    owner = {f"sections/{q['id']}": q["id"] for q, _ in main}
    owner.update({f"appendices/{q['id']}": q["id"] for q, _ in appx})
    for m in re.finditer(r"\\input\{([^}]+)\}", MASTER.read_text(encoding="utf-8", errors="replace")):
        target = LATEX / (m.group(1) + ".tex")
        if not target.exists(): continue
        for kind, body in FLOAT_ENV.findall(target.read_text(encoding="utf-8", errors="replace")):
            counters[kind] += 1
            hit = LABEL_CMD.search(body)
            lab = hit.group(1) if hit else ""
            unit = units.get(lab, "")
            rows.append({"printed": f"{kind.title()} {counters[kind]}", "kind": kind,
                         "label": lab, "unit": unit,
                         "page": owner.get(m.group(1), m.group(1)),
                         "declared": declared_number(unit) if unit else None})
    # sections: the twin of the display problem, same root cause and same tooth
    secs, n, letter = [], 0, 0
    for p_, _ in main:
        if p_["id"].endswith("-Abstract"): continue
        n += 1
        dec, title = page_heading(p_)
        secs.append({"printed": f"§{n}", "declared": f"§{dec}" if dec else None,
                     "title": title, "page": p_["id"], "ready": p_["ready"]})
    for p_, _ in appx:
        dec, title = page_heading(p_)
        letter += 1
        printed = f"Appendix {chr(64 + letter)}"
        secs.append({"printed": printed, "declared": f"Appendix {dec}" if dec else None,
                     "title": title, "page": p_["id"], "ready": p_["ready"]})
    findings, seen_label, claimed = [], {}, {}
    for r in secs:
        if r["declared"] and r["declared"] != r["printed"]:
            findings.append(f"{r['page']}: page H1 says {r['declared']}, prints {r['printed']}")
    for r in rows:
        if r["declared"] and r["declared"] != r["printed"]:
            findings.append(f"{r['unit'] or r['label']}: claims {r['declared']}, prints {r['printed']}")
        if r["unit"] and not r["declared"]:
            findings.append(f"{r['unit']}: prints {r['printed']} but its README declares no number")
        if r["label"] and r["label"] in seen_label:
            findings.append(f"label {r['label']} printed twice: {seen_label[r['label']]} and {r['printed']}")
        seen_label.setdefault(r["label"], r["printed"])
    # every unit ON DISK, not only the ones this build copied: a collision on a
    # NOT-READY page is exactly the one that detonates later, when it compiles.
    homes = {}
    for readme in sorted(ROOT.glob("B*/*/outline/evidence/display/*/README.md")):
        unit = readme.parent.name
        homes.setdefault(unit, []).append(readme.parents[4].name)
        d = declared_number(unit)
        if d: claimed.setdefault(d, []).append(unit)
    for unit, pages_ in sorted(homes.items()):
        if len(pages_) > 1:   # declared_number() reads the first README it finds; two homes make that a guess
            findings.append(f"unit {unit} exists on {len(pages_)} pages: {', '.join(pages_)}")
    for number, owners in sorted(claimed.items()):
        if len(owners) > 1:
            findings.append(f"{number} claimed by {len(owners)} units: {', '.join(owners)}")
    lines = [f"# Display register · GENERATED by {ENGINE_TAG}, never hand-edited", "",
             f"Built {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
             f"{counters['figure']} figure(s) + {counters['table']} table(s) printed.",
             "A number here is provisional while any page is NOT READY: a page that starts",
             "compiling inserts its floats and renumbers everything after it.", "", "```text"]
    lines.append(f"{'PRINTED':<10} {'DECLARED':<10} {'LABEL':<34} {'UNIT':<44} PAGE")
    for r in rows:
        flag = "" if (r["declared"] or "") in ("", r["printed"]) else "  ⛔"
        lines.append(f"{r['printed']:<10} {(r['declared'] or '—'):<10} {r['label']:<34} {r['unit'] or '—':<44} {r['page']}{flag}")
    lines += ["```", "", "## Sections", "", "```text"]
    lines.append(f"{'PRINTED':<12} {'DECLARED':<12} {'READY':<6} {'TITLE':<44} PAGE")
    for r in secs:
        flag = "" if (r["declared"] or r["printed"]) == r["printed"] else "  ⛔"
        lines.append(f"{r['printed']:<12} {(r['declared'] or '—'):<12} "
                     f"{('yes' if r['ready'] else 'no'):<6} {r['title'][:44]:<44} {r['page']}{flag}")
    lines += ["```", ""]
    lines.append("## Findings")
    lines += [f"- {f}" for f in findings] if findings else ["- none"]
    (HERE / "display-register.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"figures": counters["figure"], "tables": counters["table"],
            "rows": rows, "sections": secs, "findings": findings}

# ── build ────────────────────────────────────────────────────────────────────
class _Missing:
    """stands in for a CompletedProcess when the tool itself is not installed."""
    def __init__(self, tool): self.returncode, self.stdout, self.stderr = 127, "", f"{tool} not found on PATH; install it or run on a machine that has it"

def _run(cmd, **kw):
    try: return subprocess.run(cmd, **kw)
    except FileNotFoundError: return _Missing(cmd[0])

def build():
    reset_placement()
    main_ids, appx_ids, order_source = read_order()
    G_MAIN = rel(CFG["pages"]["main"])
    G_APP = rel(CFG["pages"]["appendix"]) if CFG["pages"].get("appendix") else None   # 0.7.0: appendix group optional
    if appx_ids and G_APP is None:
        raise RuntimeError("the compile-order block lists appendix Sections but paper-build.toml [pages] declares no appendix group")
    if LATEX.exists(): shutil.rmtree(LATEX)
    for d in (SEC, APP, DISP): d.mkdir(parents=True, exist_ok=True)
    main = [inspect(i, G_MAIN) for i in main_ids]
    appx = [inspect(i, G_APP) for i in appx_ids] if G_APP else []
    pages = main + appx
    labels = label_index(pages); unresolved = []
    for p in pages:   # 0.6.1: a DRAFT may print an unready page's fragment when the paper opts in
        p["included"] = p["ready"] or (DRAFT_INCLUDES_UNREADY and p["fragment"].exists())
    prescan_embedded(pages)
    main_f = [(p, place_fragment(p, SEC, labels, unresolved) if p["included"] else []) for p in main]
    appx_f = [(p, place_fragment(p, APP, labels, unresolved) if p["included"] else []) for p in appx]
    nbib = merge_bib(pages)
    ready = [p for p in pages if p["ready"]]
    status = build_readiness(pages, unresolved)["status"]
    write_master(main_f, appx_f, status, len(ready), len(pages))
    register = display_register(main_f, appx_f)
    # compile
    rc = _run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-quiet", MASTER.name],
              cwd=LATEX, capture_output=True, text=True)
    pdf = LATEX / "master.pdf"; main_pdf = rel(OUT["main_pdf"])
    if pdf.exists(): shutil.copy2(pdf, main_pdf)
    for junk in LATEX.glob("master.*"):
        if junk.suffix not in {".tex", ".pdf", ".bbl", ".log"}: junk.unlink()
    # word
    docx_rc, docx_err = None, None
    if DOCX_ENGINE.exists():
        env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(HERE / "paper-build.toml"))
        r = _run([sys.executable, str(DOCX_ENGINE)], cwd=HERE, env=env, capture_output=True, text=True)
        docx_rc, docx_err = r.returncode, (r.stderr or r.stdout)[-1500:]
    manifest_path = HERE / OUT["manifest"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    except (OSError, json.JSONDecodeError):
        manifest = {}
    purge_retired_delivery_receipts(manifest)
    submission_readiness = build_readiness(pages, unresolved, rc.returncode, docx_rc)
    status = submission_readiness["status"]
    manifest.update({
        "built": datetime.now().isoformat(timespec="seconds"), "engine": ENGINE_TAG,
        "status": status, "order": {"main": main_ids, "appendix": appx_ids}, "order_source": order_source,
        "pages": [{"id": p["id"], "ready": p["ready"], "reasons": p["reasons"], "warnings": p.get("warnings", []), "fragment_sha256": p["sha256"],
                   "outline": p["outline"],
                   "fragment": str(p["fragment"].relative_to(ROOT)) if p["fragment"].exists() else None} for p in pages],
        "submission_readiness": submission_readiness,
        "unresolved_refs": unresolved, "bib_entries": nbib, "displays": register, "warnings": list(BUILD_WARNINGS),
        "venue_profile": VENUE_PROFILE or None,
        "latex_profile": {"spacing": LATEX_SPACING, "bibstyle": LATEX_BIBSTYLE, "displays": LATEX_DISPLAYS,
                          "appendix_newpage": LATEX_APPENDIX_NEWPAGE, "title_page": LATEX_TITLE_PAGE,
                          "abstract_page": LATEX_ABSTRACT_PAGE, "running_head": LATEX_RUNNING_HEAD},
        "outputs": {"pdf": OUT["main_pdf"] if main_pdf.exists() else None,
                    "docx": OUT["main_docx"] if rel(OUT["main_docx"]).exists() else None},
    })
    manifest["readiness"] = {
        "ready": len(ready),
        "total": len(pages),
        "not_ready": [{"id": p["id"], "reasons": p["reasons"]} for p in pages if not p["ready"]],
    }
    manifest["render"] = {
        "latexmk_rc": rc.returncode,
        "latexmk_tail": (rc.stdout + rc.stderr)[-1200:] if rc.returncode else "",
        "docx_rc": docx_rc,
        "docx_tail": docx_err,
    }
    if isinstance(manifest.get("build"), dict):
        manifest["build"].update({"status": status, "page_readiness": manifest["readiness"], "render": manifest["render"]})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"{status} · {len(ready)}/{len(pages)} pages ready · bib {nbib} entries · unresolved refs {len(unresolved)}")
    print(f"order: {order_source} · {len(main_ids)} main + {len(appx_ids)} appendix")
    for blocker in submission_readiness["blockers"]:
        print(f"  G4: {blocker}")
    print(f"displays: {register['figures']} figure + {register['tables']} table · "
          f"{len(register['findings'])} numbering finding(s) · delivery/display-register.md")
    print(f"pdf: {'✅ ' + OUT['main_pdf'] if main_pdf.exists() else '❌ latexmk rc=' + str(rc.returncode)}")
    print(f"docx: {'✅ ' + OUT['main_docx'] if rel(OUT['main_docx']).exists() else '❌ rc=' + str(docx_rc)}")
    for p in pages:
        if not p["ready"]: print(f"  ⬜ {p['id']}: {'; '.join(p['reasons'])}")
    for p in pages:
        for w in p.get("warnings", []): print(f"  ⚠ {p['id']}: {w}")
    for w in BUILD_WARNINGS: print(f"  ⚠ document: {w}")

def freeze(kind: str, rd: str):
    """Cut one immutable Round snapshot from the current generated delivery.

    The Round contract is output-config driven: every declared output must be
    present, and the derived display register travels with the manifest. A
    partially populated destination is never repaired in place; a new Round
    (or an explicit human migration) is required.
    """
    if kind not in {"sent", "released"}:
        sys.exit(f"invalid freeze target {kind!r}; expected sent or released")
    rounds = list(ROOT.glob(f"B*-*-Round/{rd}-*"))
    if len(rounds) != 1:
        sys.exit(f"expected one Round folder for {rd}, found {len(rounds)}")

    dst = rounds[0] / kind
    if dst.exists():
        leftovers = [p for p in dst.iterdir() if p.name != ".gitkeep"]
        if leftovers:
            names = ", ".join(sorted(p.name for p in leftovers))
            sys.exit(f"{dst.relative_to(ROOT)} is immutable and already contains: {names}")
    dst.mkdir(parents=True, exist_ok=True)

    sources = []
    missing = []
    targets = set()
    for key, configured in OUT.items():
        src = rel(configured)
        if not src.exists():
            missing.append(f"{key}: {configured}")
            continue
        target_name = src.name
        if target_name in targets:
            sys.exit(f"freeze output name collision: {target_name}")
        targets.add(target_name)
        sources.append((key, src))

    register = HERE / "display-register.md"
    if not register.exists():
        missing.append(f"display-register: {register.relative_to(ROOT)}")
    elif register.name in targets:
        sys.exit(f"freeze output name collision: {register.name}")
    else:
        sources.append(("display-register", register))

    if missing:
        sys.exit("cannot freeze an incomplete build; missing: " + "; ".join(missing))

    for key, src in sources:
        target = dst / src.name
        if src.is_dir():
            shutil.copytree(src, target)
        else:
            shutil.copy2(src, target)
        print(f"  → {dst.relative_to(ROOT)}/{target.name} ({key})")
    print(f"{kind}/ frozen for {rounds[0].name} · hash {sha(dst / Path(OUT['manifest']).name)}")

def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or a[0] == "build": build()
    elif a[0] in {"send", "release"} and len(a) == 2: freeze("sent" if a[0] == "send" else "released", a[1])
    else: sys.exit(__doc__)

if __name__ == "__main__":
    main()
