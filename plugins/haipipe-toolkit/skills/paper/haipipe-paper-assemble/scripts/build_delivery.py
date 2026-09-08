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
  .venv/bin/python delivery/build.py send RD02       copy the current build into that Round's sent/
  .venv/bin/python delivery/build.py release RD01    copy the current build into that Round's released/

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
#   [evidence] draft_includes_unready = true   a DRAFT prints every page that has a body fragment, tagged
#                                              "[DRAFT PAGE · reason]"; readiness accounting is unchanged
#   [source]   preamble = "preamble.tex"       a paper-owned preamble file beside paper-build.toml, inlined
#                                              into the generated master (packages, column types, unicode maps)
#   [paper]    venue_profile = "jama-internal-medicine"  title-page center block, JAMA section boundaries,
#                                              and the page's own \section*{Key Points}/\section*{Abstract} kept
DRAFT_INCLUDES_UNREADY = bool(CFG.get("evidence", {}).get("draft_includes_unready", False))
VENUE_PROFILE = str(CFG["paper"].get("venue_profile", "")).lower()
JAMA = VENUE_PROFILE == "jama-internal-medicine"
PREAMBLE_FILE = rel(CFG["source"]["preamble"]) if CFG.get("source", {}).get("preamble") else None

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
    missing_prev = [u.name for u in units if not (u / "preview.pdf").exists()]
    if missing_prev: reasons.append(f"display preview.pdf missing: {', '.join(missing_prev)}")
    return {"id": pid, "dir": d, "fragment": frag, "units": units, "ready": not reasons, "reasons": reasons,
            "sha256": sha(frag) if frag.exists() else None, "outline": outline}


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
    floats = []
    for lab in dict.fromkeys(re.findall(r"\\ref\{([^}]+)\}", t)):
        hit = labels.get(lab)
        if hit:
            name = copy_unit(hit[1])
            # behavior A · md2tex already embeds a cited display as a real float
            # INSIDE the fragment, so re-inputting the unit's float/ after it printed
            # every display twice: Figure 1 = Figure 2, Table 1 = Table 4 (260908).
            if DEDUPE_EMBEDDED_FLOATS and f"displays/{name}/" in t: continue
            if name not in floats: floats.append(name)
        else:
            unresolved.append({"page": p["id"], "ref": lab})
    return floats

# ── bibliography ─────────────────────────────────────────────────────────────
def merge_bib(pages):
    seen, out = set(), []
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
                if key not in seen:
                    seen.add(key); out.append(txt[start:j+1])
    BIB.write_text(f"% merged by {ENGINE_TAG} from every page's outline/evidence/bibex/*.bib · do not edit\n\n" + "\n\n".join(out) + "\n", encoding="utf-8")
    return len(out)

# ── master ───────────────────────────────────────────────────────────────────
def write_master(main, appx, status, ready_n, total_n):
    title = CFG["paper"].get("title", CFG["paper"]["id"])
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    paper_preamble = ("% paper-owned preamble · " + PREAMBLE_FILE.name + "\n" + PREAMBLE_FILE.read_text(encoding="utf-8")) \
        if PREAMBLE_FILE and PREAMBLE_FILE.exists() else "% no paper preamble declared"
    if JAMA:   # the JAMA Word renderer parses a title-page center block, not \maketitle
        title_block = ("\\begin{document}\n\n\\begin{center}\n{\\Large\\bfseries " + title + "}\n\n\\vspace{1em}\n\n"
                       "[Authors blinded for review]\n\n\\vspace{0.5em}\n\\end{center}")
    else:
        title_block = "\\title{" + title + "}\n\\author{}\n\\date{}\n\\begin{document}\n\\maketitle"
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
\providecommand{{\displayroot}}{{displays/}}
{paper_preamble}
\onehalfspacing
\setlength{{\parindent}}{{0.25in}}
\setlength{{\parskip}}{{0.35em}}
\graphicspath{{{{./}}}}
\pagestyle{{fancy}}\fancyhf{{}}
\fancyhead[L]{{\small {status} · {ready_n}/{total_n} section pages ready · built {stamp}}}
\fancyfoot[C]{{\thepage}}
{title_block}
\thispagestyle{{fancy}}

"""
    body = []
    for p, floats in main:
        if p.get("included", p["ready"]) and not p["ready"]:
            note = "; ".join(p["reasons"]).replace("_", r"\_").replace("<", r"$<$").replace(">", r"$>$")
            body.append(r"\noindent\textcolor{red!70!black}{\small\textit{[DRAFT PAGE · " + note + "]}}")
        if p.get("included", p["ready"]) and p["id"].endswith("-Abstract"):
            body.append(rf"\input{{sections/{p['id']}}}"); body.append(""); continue
        if p.get("included", p["ready"]):
            if JAMA:   # the JAMA Word renderer splits the body on these four headings
                kind = p["id"].rsplit("-Main-", 1)[-1].replace("-", " ")
                frag_txt = (SEC / f"{p['id']}.tex").read_text(encoding="utf-8", errors="replace")
                if kind in ("Introduction", "Methods", "Results", "Discussion") and not re.search(rf"\\section\{{{kind}\}}", frag_txt):
                    body.append(rf"\section{{{kind}}}")
            body.append(rf"\input{{sections/{p['id']}}}")
            body += [rf"\input{{displays/{f}/float}}" for f in floats]
        else:
            _, title = page_heading(p)
            body.append(rf"\section{{{tex_text(title)}}}" + "\n" +
                        r"\noindent\textit{[Not yet compiled into this build: " +
                        "; ".join(p["reasons"]).replace("_", r"\_").replace("<", r"$<$").replace(">", r"$>$") + "]}")
        body.append("")
    tail = ["\\section*{Acknowledgments}", "\\noindent\\textit{[Acknowledgments, funding and disclosures are written at submission; this build is a draft.]}", "",
            "\\clearpage", "\\bibliographystyle{apalike}", "\\bibliography{reference}", "", "\\clearpage", "\\appendix", ""]
    if JAMA:   # JAMA supplements number their floats eTable 1… / eFigure 1…, restarting after the references
        tail += ["\\setcounter{table}{0}\\renewcommand{\\tablename}{eTable}\\renewcommand{\\thetable}{\\arabic{table}}",
                 "\\setcounter{figure}{0}\\renewcommand{\\figurename}{eFigure}\\renewcommand{\\thefigure}{\\arabic{figure}}", ""]
    for p, floats in appx:
        if p.get("included", p["ready"]) and not p["ready"]:
            note = "; ".join(p["reasons"]).replace("_", r"\_").replace("<", r"$<$").replace(">", r"$>$")
            tail.append(r"\noindent\textcolor{red!70!black}{\small\textit{[DRAFT PAGE · " + note + "]}}")
        if p.get("included", p["ready"]):
            tail.append(rf"\input{{appendices/{p['id']}}}")
            tail += [rf"\input{{displays/{f}/float}}" for f in floats]
        else:
            _, title = page_heading(p)
            tail.append(rf"\section{{{tex_text(title)}}}" + "\n" +
                        r"\noindent\textit{[Not yet compiled into this build: " +
                        "; ".join(p["reasons"]).replace("_", r"\_").replace("<", r"$<$").replace(">", r"$>$") + "]}")
        tail.append("")
    MASTER.write_text(head + "\n".join(body) + "\n" + "\n".join(tail) + "\n\\end{document}\n", encoding="utf-8")

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
    for readme in sorted(ROOT.glob("B*/*/outline/evidence/display/*/README.md")):
        unit = readme.parent.name
        d = declared_number(unit)
        if d: claimed.setdefault(d, []).append(unit)
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
def build():
    main_ids, appx_ids, order_source = read_order()
    G_MAIN, G_APP = rel(CFG["pages"]["main"]), rel(CFG["pages"]["appendix"])
    if LATEX.exists(): shutil.rmtree(LATEX)
    for d in (SEC, APP, DISP): d.mkdir(parents=True, exist_ok=True)
    main = [inspect(i, G_MAIN) for i in main_ids]
    appx = [inspect(i, G_APP) for i in appx_ids]
    pages = main + appx
    labels = label_index(pages); unresolved = []
    for p in pages:   # 0.6.1: a DRAFT may print an unready page's fragment when the paper opts in
        p["included"] = p["ready"] or (DRAFT_INCLUDES_UNREADY and p["fragment"].exists())
    main_f = [(p, place_fragment(p, SEC, labels, unresolved) if p["included"] else []) for p in main]
    appx_f = [(p, place_fragment(p, APP, labels, unresolved) if p["included"] else []) for p in appx]
    nbib = merge_bib(pages)
    ready = [p for p in pages if p["ready"]]
    status = build_readiness(pages, unresolved)["status"]
    write_master(main_f, appx_f, status, len(ready), len(pages))
    register = display_register(main_f, appx_f)
    # compile
    rc = subprocess.run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-quiet", MASTER.name],
                        cwd=LATEX, capture_output=True, text=True)
    pdf = LATEX / "master.pdf"; main_pdf = rel(OUT["main_pdf"])
    if pdf.exists(): shutil.copy2(pdf, main_pdf)
    for junk in LATEX.glob("master.*"):
        if junk.suffix not in {".tex", ".pdf", ".bbl", ".log"}: junk.unlink()
    # word
    docx_rc, docx_err = None, None
    if DOCX_ENGINE.exists():
        env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(HERE / "paper-build.toml"))
        r = subprocess.run([sys.executable, str(DOCX_ENGINE)], cwd=HERE, env=env, capture_output=True, text=True)
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
        "pages": [{"id": p["id"], "ready": p["ready"], "reasons": p["reasons"], "fragment_sha256": p["sha256"],
                   "outline": p["outline"],
                   "fragment": str(p["fragment"].relative_to(ROOT)) if p["fragment"].exists() else None} for p in pages],
        "submission_readiness": submission_readiness,
        "unresolved_refs": unresolved, "bib_entries": nbib, "displays": register,
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

def freeze(kind: str, rd: str):
    rounds = list(ROOT.glob(f"B*-*-Round/{rd}-*"))
    if len(rounds) != 1: sys.exit(f"expected one Round folder for {rd}, found {len(rounds)}")
    dst = rounds[0] / kind; dst.mkdir(exist_ok=True)
    for key in ("main_pdf", "main_docx", "manifest"):
        src = rel(OUT[key])
        if src.exists(): shutil.copy2(src, dst / src.name); print(f"  → {dst.relative_to(ROOT)}/{src.name}")
    print(f"{kind}/ frozen for {rounds[0].name} · hash {sha(rel(OUT['manifest']))}")

def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or a[0] == "build": build()
    elif a[0] in {"send", "release"} and len(a) == 2: freeze("sent" if a[0] == "send" else "released", a[1])
    else: sys.exit(__doc__)

if __name__ == "__main__":
    main()
