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
                                                     on the ladder (b16 Q05) the name is a comments report of
                                                     the version, reports/qNN_<kind>-<MMDD>/ (`send q02`, or
                                                     its full stem): the send freezes into its sent/
  .venv/bin/python delivery/build.py check           (or --dry-run) find every Section's folder and fragment
                                                     through [pages]; writes nothing, exit 1 if one is missing

Three behaviors this engine guarantees, each with a tooth in tests/:
  A  a display cited by a fragment is printed ONCE (md2tex already embeds it as
     a float; the master never re-inputs it)               DEDUPE_EMBEDDED_FLOATS
  B  a not-ready page keeps its number: a real \section{<its own title>} from
     the page's H1, never an unnumbered "[NOT READY]"       page_heading()
  C  delivery/display-register.md counts what the MASTER prints, in \input
     order, and compares with what each unit's README declares  display_register()
"""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, time, tomllib
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

def validate_build_config(config, delivery):
    """Reject unsafe generated paths before any build side effect."""
    delivery = Path(delivery).resolve()
    required = {
        "paper": ("id",), "pages": ("main", "order"),
        "source": ("room", "master", "sections", "displays", "bibliography"),
        "outputs": ("main_pdf", "main_docx", "manifest"),
    }
    for table, keys in required.items():
        if not isinstance(config.get(table), dict):
            raise ValueError(f"paper-build.toml requires [{table}]; see ref/paper-build.toml.example")
        for key in keys:
            value = config[table].get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"paper-build.toml requires a nonempty [{table}] {key}")
    if delivery.name != "delivery":
        raise ValueError("paper-build.toml must live in <paper>/delivery/")

    def child(base, value, label):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} must be a nonempty relative path")
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"{label} must stay inside {base}; absolute paths and '..' are not allowed")
        resolved = (base / path).resolve()
        if resolved == base or not resolved.is_relative_to(base):
            raise ValueError(f"{label} escapes its generated directory: {value}")
        return resolved

    if config["source"]["room"] != "latex":
        raise ValueError('[source] room must be "latex" (generated delivery/latex/); move source groups to [pages]')
    room = child(delivery, "latex", "[source] room")
    if (delivery / "latex").is_symlink():
        raise ValueError("generated delivery/latex must not be a symlink")
    for key in ("master", "sections", "appendices", "displays", "bibliography"):
        if key in config["source"]:
            child(room, config["source"][key], f"[source] {key}")

    inputs = [(delivery / config["pages"][key]).resolve()
              for key in ("main", "appendix", "order") if config["pages"].get(key)]
    # 0.10.0 (b16 g03): on the ladder a version Job holds its Sections and its own delivery/, so a
    # [pages] group may be the folder that holds delivery/ ("..": j01_v1_<desk>/). A page is found there
    # by its id (S-…), never delivery/ itself, so the generated room cannot overwrite it.
    holder = delivery.parent
    inputs = [x for x in inputs if x != holder]
    for key in ("preamble", "head", "opening", "supplement_head", "supplement_opening", "store"):
        if config["source"].get(key):
            inputs.append((delivery / config["source"][key]).resolve())
    for source in inputs:
        if source == delivery or source == room or source.is_relative_to(room) or room.is_relative_to(source):
            raise ValueError(f"generated room overlaps a source input: {source}")
    for key, value in config["outputs"].items():
        if value == "":
            continue   # an empty optional output is switched off (0.8.4: section_snapshots = "")
        target = child(delivery, value, f"[outputs] {key}")
        if target in {delivery / "paper-build.toml", delivery / "build.py"}:
            raise ValueError(f"[outputs] {key} would overwrite build configuration/code")
        if any(target == source or target.is_relative_to(source) or source.is_relative_to(target) for source in inputs):
            raise ValueError(f"[outputs] {key} overlaps a source input")
    child(delivery, "display-register.md", "display register")

# ── where am I · which paper ────────────────────────────────────────────────
# A wrapper execs this file inside its own module and pre-sets __engine_dir__;
# a direct call resolves everything from this file and the environment.
ENGINE_DIR = Path(globals().get("__engine_dir__") or Path(__file__).resolve().parent)
DOCX_ENGINE = ENGINE_DIR / "latex_room_to_docx.py"
COVER_LETTER = ENGINE_DIR / "cover_letter.py"            # 0.9.0: run-delivery-coverletter
# the Page workbench's renderer: a PDF drawn from the .docx package itself, so a reader can see the Word output
DOCX2PDF = next(p for p in ENGINE_DIR.parents if p.name == "skills").parent / "servers" / "workbench" / "task-page" / "exporters" / "docx2pdf.py"
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
# the paper: delivery/'s folder, or on the ladder (0.10.0, b16 g03) the Board above the version Job that
# holds it (Paper-<Slug>/j01_v1_<desk>/delivery/); VERSION is the folder holding delivery/ either way
VERSION = HERE.parent
ROOT = next((q for q in (VERSION, VERSION.parent) if (q / "board.md").is_file()), VERSION)
# where Section Pages sit: today's B<x>-<desk>-<part>/ groups, or the version Job itself
PAGE_HOMES = ("B*",) if VERSION == ROOT else ("B*", VERSION.relative_to(ROOT).as_posix())
CFG = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
validate_build_config(CFG, HERE)
DEDUPE_EMBEDDED_FLOATS = True   # behavior A · tests flip this to prove the register catches the double print

def rel(p): return (HERE / p).resolve()


def unrooted(text):
    """A tool's printed output with the SPACE root (the folder with env.sh) cut off its paths, so the manifest
    holds no /Users/... path (JL 260927; the Word lane prints every file it writes)."""
    root = next((q for q in [HERE.resolve(), *HERE.resolve().parents] if (q / "env.sh").is_file()), None)
    return text.replace(f"{root}/", "") if text and root else text
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
# 0.9.1 · a paper that owns its LaTeX, all opt-in (JL 260929, Paper-FairGlucose-preprint: npj + arXiv):
#   [source]   head = "<file>"            the paper's own preamble, \documentclass and \title included,
#                                         inlined in place of the engine's package head and title block
#                                         (a desk class, arxiv.sty); the files beside it are copied into
#                                         the room so its \usepackage/\input resolve and the room stays
#                                         self-contained for arXiv
#   [source]   opening = "<file>"         what follows \begin{document} (default \maketitle)
#   [source]   supplement_head / supplement_opening   the same pair, for a separate supplement
#   [source]   store = "<dir>"            a paper-level display store a fragment reads by path
#                                         (displays/Figure/x.pdf): each file is copied into the room
#                                         and warned, since a display belongs in a DISPLAY Result
#   [evidence] draft_citations = true     a DRAFT merges a Page's draft-bibliography/<page>.bib (the
#                                         unverified keys a `delivery: draft` Page cites) when it has no
#                                         selected-bibliography; every such Page is a G4 blocker
def _source_file(key):
    value = CFG.get("source", {}).get(key)
    return rel(value) if value else None
HEAD_FILE = _source_file("head")
OPENING_FILE = _source_file("opening")
SUPP_HEAD_FILE = _source_file("supplement_head")
SUPP_OPENING_FILE = _source_file("supplement_opening")
STORE = _source_file("store")
DRAFT_CITATIONS = bool(CFG.get("evidence", {}).get("draft_citations", False))

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
LATEX_ACKNOWLEDGMENTS = bool(_L.get("acknowledgments", True))  # false = a blind copy prints no Acknowledgments section (0.8.4)
LATEX_RUNNING_HEAD = bool(_L.get("running_head", True))       # False: header carries only the DRAFT word while drafting
# 0.8.2 · "per-appendix": floats restart in each lettered appendix (Table B1, C1 …); the Word lane reads the same key
APPENDIX_PER_LETTER = str(PROFILE.get("appendix_float_numbering", "continuous")).lower() == "per-appendix"
# 0.9.1 · `pdflatex` for a paper whose head loads no fontspec (arXiv builds with pdflatex);
# appendices = "supplement": master.tex is the main article, supplement.tex the appendices
# alone, combined.tex both (the one-file arXiv copy); main_pdf, supplement_pdf, combined_pdf
LATEX_ENGINE = str(_L.get("engine", "xelatex")).lower()
SUPPLEMENT_SPLIT = str(PROFILE.get("appendices", "")).lower() == "supplement"

# ── document-wide placement state (0.7.0) ────────────────────────────────────
# A display prints ONCE in the whole document, not once per fragment: a page
# that \ref's a float another page embeds must not re-input it.
EMBEDDED_UNITS: set = set()      # units some included fragment embeds as a real float
PLACED_FLOATS: set = set()       # units the master already \input after a fragment
BUILD_WARNINGS: list = []        # document-level warnings (bib collisions, …)
DRAFT_CITED: list = []           # 0.9.1: Pages whose citations came from their unverified draft Bib
STORE_READS: dict = {}           # 0.9.1: page id -> store paths its fragment read

def reset_placement():
    EMBEDDED_UNITS.clear(); PLACED_FLOATS.clear(); BUILD_WARNINGS.clear()
    DRAFT_CITED.clear(); STORE_READS.clear()

def prescan_embedded(pages):
    """record every unit any INCLUDED fragment embeds, before any fragment is placed."""
    for p in pages:
        if p.get("included", p["ready"]) and p["fragment"].exists():
            raw = p["fragment"].read_text(encoding="utf-8", errors="replace")
            refs = re.findall(
                r"\\(?:input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}", raw
            )
            for ref in refs:
                found = page_unit_reference(p, ref)
                if found:
                    EMBEDDED_UNITS.add(f"{p['id']}/{found[0].name}")

# ── order ─────────────────────────────────────────────────────────────────────
ORDER_BLOCK = re.compile(r"<!--\s*haipipe:compile-order:start\s*-->(.*?)<!--\s*haipipe:compile-order:end\s*-->", re.S)
OUTLINE_VERSION = re.compile(r"-(?:outline|draft)-v([0-9]+(?:\.[0-9]+)*)\.md$")


def plan_home(page_dir: Path) -> Path:
    """A Page's plan folder: `draft/` (Page 0.118), else the older `outline/`."""
    draft = page_dir / "draft"
    return draft if draft.is_dir() else page_dir / "outline"

def outline_key(path: Path):
    match = OUTLINE_VERSION.search(path.name)
    return tuple(int(part) for part in match.group(1).split(".")) if match else ()

def latest_outline(group: Path, pid: str):
    home = plan_home(group / pid)
    candidates = [*home.glob(f"{pid}-outline-v*.md"), *home.glob(f"{pid}-draft-v*.md")]
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
        m = re.match(r"-\s*(S-[A-Za-z0-9-]+|t\d{2}_[a-z0-9-]+)\s*$", s)   # S-<desk>-… or a version's tNN_<title>
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



def _yaml_scalar(value: str) -> str:
    """Read the simple scalar fields used by Page Result envelopes."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value.split("#", 1)[0].strip()


def _result_field(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.*?)\s*$", text)
    return _yaml_scalar(match.group(1)) if match else ""


def _result_text(text: str) -> str:
    """0.8.2: a result.yaml written in JSON form (valid YAML) is read like the YAML form.
    The field readers below match `key: value` lines, so a JSON Result was invisible:
    its unit was never placed and its page-relative \\input broke the master (AgreeableRx 260928)."""
    s = text.lstrip()
    if not s.startswith("{"):
        return text
    try:
        d = json.loads(s)
    except ValueError:
        return text
    lines = [f"{k}: {d[k]}" for k in ("item", "type", "status", "run") if isinstance(d.get(k), str)]
    payload = d.get("payload") if isinstance(d.get("payload"), dict) else {}
    if isinstance(payload.get("unit"), str):
        lines += ["payload:", f"  unit: {payload['unit']}"]
    return "\n".join(lines) + "\n"


def _page_result_display_unit(page_dir: Path, manifest: Path, text: str):
    """Resolve a typed Page DISPLAY Result's payload.unit within results/."""
    item = _result_field(text, "item")
    kind = _result_field(text, "type").upper()
    if kind != "DISPLAY" and not re.search(r"-DISPLAY-", item, re.I):
        return None

    payload = re.search(
        r"(?ms)^payload:[ \t]*\n((?:^[ \t]+[^\n]*(?:\n|$))*)", text
    )
    if not payload:
        return None
    unit_match = re.search(r"(?m)^[ \t]{2}unit:[ \t]*(.*?)\s*$", payload.group(1))
    if not unit_match:
        return None
    raw = _yaml_scalar(unit_match.group(1))
    if not raw:
        return None

    result_root = page_dir / "results"
    raw_path = Path(raw)
    candidates = []
    placeholder = "<resolved-result>/"
    if raw.startswith(placeholder):
        candidates.append(manifest.parent / raw[len(placeholder):])
    if raw_path.is_absolute():
        candidates.append(raw_path)
    else:
        candidates.extend((page_dir / raw_path, manifest.parent / raw_path))
        if raw_path.parts and raw_path.parts[0] not in ("results", "payload"):
            candidates.append(manifest.parent / "payload" / raw_path)

    try:
        resolved_root = result_root.resolve()
    except OSError:
        return None
    for candidate in candidates:
        if candidate.is_symlink():
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(resolved_root)
        except (OSError, ValueError):
            continue
        if resolved.is_dir():
            return resolved
    return None


def page_display_units(page_dir: Path):
    """Return current Result units; read the retired Outline lane only during migration."""
    result_root = page_dir / "results"
    current = {}
    saw_display_result = False
    if result_root.is_dir() and not result_root.is_symlink():
        for manifest in sorted(result_root.rglob("result.yaml")):
            if manifest.is_symlink():
                continue
            try:
                manifest.resolve().relative_to(result_root.resolve())
                text = manifest.read_text(encoding="utf-8", errors="replace")
                text = _result_text(text)
            except (OSError, ValueError):
                continue
            item = _result_field(text, "item")
            kind = _result_field(text, "type").upper()
            if kind != "DISPLAY" and not re.search(r"-DISPLAY-", item, re.I):
                continue
            saw_display_result = True
            # Sorted Result paths mirror the Page Evidence reader: a later
            # attempt for the same stable Evidence Item replaces the older one.
            key = item or manifest.parent.name
            current[key] = (
                _page_result_display_unit(page_dir, manifest, text),
                manifest,
            )
    if saw_display_result:
        unresolved = [
            (item, manifest)
            for item, (unit, manifest) in current.items()
            if unit is None
        ]
        if unresolved:
            details = "; ".join(
                f"{item} ({manifest.relative_to(page_dir)})"
                for item, manifest in unresolved
            )
            raise RuntimeError(
                "Could not resolve payload.unit for current Page DISPLAY Result(s): "
                f"{details}. Expected a unit directory contained under results/. "
                "Refusing to omit these displays from the assembled paper."
            )
        return sorted(
            {unit for unit, _manifest in current.values()},
            key=lambda p: p.as_posix(),
        )

    legacy = plan_home(page_dir) / "evidence" / "display"
    return sorted((p for p in legacy.glob("*/") if p.is_dir()), key=lambda p: p.name) if legacy.is_dir() else []


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
    pdfs = [d / "delivery" / "latex" / f"{pid}.pdf"]      # the Page export's compiled wrapper
    units = page_display_units(d)
    reasons = []
    if not d.exists(): reasons.append("page folder missing")
    plan = latest_outline(group, pid)
    outline = None
    if plan is not None:
        plan_text = plan.read_text(encoding="utf-8", errors="replace")
        header = re.split(r"(?m)^##\s", plan_text, maxsplit=1)[0]
        approvals = re.findall(r"(?m)^approved:[ \t]*(.*)$", header)
        declarations = re.findall(r"(?m)^(?:outline|draft)-version:[ \t]*(.*)$", header)
        version = "v" + ".".join(str(part) for part in outline_key(plan))
        outline = {
            "path": str(plan.relative_to(ROOT)), "version": version,
            "approval": approvals[0].strip() if len(approvals) == 1 else None,
        }   # 0.8.4 (JL 260928): no content hashes; a version is its number, staleness is mtime
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
    missing_tex_asset = []
    for u in cited:
        ft = u / "float.tex"
        if not ft.exists():
            continue
        raw_float = ft.read_text(encoding="utf-8", errors="replace")
        if (re.search(r"\\input\{(?:\./)?recipe/", raw_float)
                and not (u / "assets" / "figure.pdf").exists()):
            missing_tex_asset.append(u.name)
    if missing_tex_asset:
        reasons.append(
            "standalone TeX display asset missing at assets/figure.pdf for cited unit: "
            + ", ".join(missing_tex_asset)
        )
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
            "outline": outline}


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
    if DRAFT_CITED:
        blockers.append("citations are unverified: %d Section(s) cite from their draft Bib (%s)"
                        % (len(DRAFT_CITED), ", ".join(DRAFT_CITED)))
    if STORE_READS:
        blockers.append("displays read from the paper store, not DISPLAY Results: %s"
                        % ", ".join("%s (%d)" % (k, len(v)) for k, v in STORE_READS.items()))
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


def page_unit_reference(p, raw_path: str):
    """Resolve a unit reference embedded by Page LaTeX or a legacy fragment."""
    parts = [part for part in raw_path.replace("\\", "/").split("/")
             if part not in ("", ".")]
    units = {u.name: u for u in p.get("units", [])}
    for i, part in enumerate(parts):
        unit_i = None
        if parts[i:i + 3] in (["outline", "evidence", "display"], ["draft", "evidence", "display"]):
            unit_i = i + 3
        elif part == "results" and i + 3 < len(parts) and parts[i + 2] == "payload":
            unit_i = i + 3
        elif part == "display":
            unit_i = i + 1
        elif part == "displays":
            unit_i = i + 2 if i + 1 < len(parts) and parts[i + 1] == p["id"] else i + 1
        if unit_i is not None and unit_i < len(parts) and parts[unit_i] in units:
            return units[parts[unit_i]], parts[unit_i + 1:]
    return None

def unit_page(u: Path) -> str:
    """the Section Page owning a Result unit or its retired migration folder."""
    return u.parents[3].name

def unit_key(u: Path) -> str:
    """'<page-id>/<unit>' · 0.7.5: Display<n>-<slug> is unique only inside its page (JL 260908)"""
    return f"{unit_page(u)}/{u.name}"

def copy_unit(u: Path) -> str:
    """copy one display unit into latex/displays/<page-id>/<unit>/ · returns '<page-id>/<unit>'"""
    key = unit_key(u)
    dst = DISP / unit_page(u) / u.name; dst.mkdir(parents=True, exist_ok=True)
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
        # The Paper master has no renderer-specific TeX preamble. Project a
        # TeX-native unit through its standalone PDF asset instead of importing
        # recipe source that may require undeclared packages or macros.
        t = re.sub(
            r"\\input\{(?:\./)?recipe/[^}]+\}",
            rf"\\includegraphics{{displays/{key}/figure.pdf}}", t
        )
        t = re.sub(r"(\\includegraphics(?:\[[^\]]*\])?)\{[^}]*\}", rf"\1{{displays/{key}/figure.pdf}}", t)
        t = re.sub(r"\\input\{[^}]*?(table-body[^}/]*)\}", rf"\\input{{displays/{key}/\1}}", t)
        (dst / "float.tex").write_text(t, encoding="utf-8")
    return key

_GRAPHIC_EXT = ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps")


def from_master(p, path: str, exts=("", ".tex")):
    """A target written relative to the Page's own delivery/latex/, rewritten to resolve
    from the master's folder (latexmk runs in LATEX); None when it does not resolve from
    the Page, so an engine-written or already-master-relative path is left alone."""
    if not path or path.startswith(("/", "\\", "~")) or re.match(r"^[A-Za-z]:", path) or "\\" in path.strip("\\"):
        return None
    target = os.path.normpath(os.path.join(p["fragment"].parent, path))
    if not any(os.path.isfile(target + ext) for ext in exts):
        return from_store(p, path, exts)
    if "_archive" in Path(path).parts:
        BUILD_WARNINGS.append(f"{p['id']}: the fragment reads {path}, a retired _archive lane; bind it to a current Result")
    return os.path.relpath(target, os.path.normpath(LATEX)).replace(os.sep, "/")


_STORE_REF = re.compile(r"\\(?:input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}")


def from_store(p, path: str, exts=("", ".tex")):
    """0.9.1 · `[source] store`: a fragment path inside the paper's display store
    (`displays/Figure/x.pdf`) is copied into the room at that same path and left as
    written; a stored .tex it reaches is followed, because a table may \\input another.
    None when no store is declared or the path is not in it."""
    if STORE is None:
        return None
    parts = Path(path).parts
    if not parts or parts[0] != STORE.name or ".." in parts:
        return None
    src = next((STORE.parent / (path + ext) for ext in exts if (STORE.parent / (path + ext)).is_file()), None)
    if src is None or not src.resolve().is_relative_to(STORE.resolve()):
        return None
    dst = LATEX / src.relative_to(STORE.parent)
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if src.suffix == ".tex":
            text = re.sub(r"(?m)(?<!\\)%.*$", "", src.read_text(encoding="utf-8", errors="replace"))
            for m in _STORE_REF.finditer(text):
                from_store(p, m.group(1), _GRAPHIC_EXT + (".tex",))
    reads = STORE_READS.setdefault(p["id"], [])
    if path not in reads:
        reads.append(path)
    return path


def place_fragment(p, dest_dir: Path, labels, unresolved):
    """copy the fragment, retarget its \\input paths, return the list of floats to \\input after it"""
    t = p["fragment"].read_text(encoding="utf-8", errors="replace")
    def fix_input(m):
        path = m.group(1)
        found = page_unit_reference(p, path)
        if found:
            src, tail = found
            key = copy_unit(src)
            tail = list(tail)
            if tail and tail[0] == "assets":
                tail = tail[1:]
            target = "/".join(tail) if tail else "float"
            if target.endswith(".tex"):
                target = target[:-4]
            return rf"\input{{displays/{key}/{target}}}"
        moved = from_master(p, path)            # any other page-relative \input: resolve it from the master
        return rf"\input{{{moved}}}" if moved else m.group(0)
    t = re.sub(r"\\input\{([^}]+)\}", fix_input, t)
    def fix_graphic(m):
        found = page_unit_reference(p, m.group(2))
        if found:
            src, _tail = found
            key = copy_unit(src)
            return rf"\includegraphics{m.group(1) or ''}{{displays/{key}/figure.pdf}}"
        moved = from_master(p, m.group(2), _GRAPHIC_EXT)
        return rf"\includegraphics{m.group(1) or ''}{{{moved}}}" if moved else m.group(0)
    t = re.sub(r"\\includegraphics(\[[^\]]*\])?\{([^}]+)\}", fix_graphic, t)
    # JL 260915: an Abstract page that already opens its own abstract environment is kept as written,
    # so a block the desk prints right after the abstract (Diabetes Care's Article Highlights) can share the page
    if is_abstract(p) and not JAMA and "\\begin{abstract}" not in t:
        # the generic Word engine wants a real abstract environment; the JAMA renderer instead
        # parses the page's own \section*{Key Points} and \section*{Abstract} headings (0.6.1)
        body = re.sub(r"^%.*\n", "", t, flags=re.M)                       # generator comments
        body = re.sub(r"\\section\*?\{Abstract\}\s*", "", body)        # the heading
        lines = [l for l in body.strip().splitlines()]
        if lines and not lines[0].startswith("\\") and len(lines[0].split()) <= 12:
            lines = lines[1:]                                             # stray title line from md2tex
        t = "\\begin{abstract}\n" + "\n".join(lines).strip() + "\n\\end{abstract}\n"
    (dest_dir / f"{p['id']}.tex").write_text(t, encoding="utf-8")
    EMBEDDED_UNITS.update(f"{pg}/{u}" for pg, u in re.findall(r"displays/([^/}]+)/([^/}]+)/", t))
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
def page_bib(p):
    """The Bib a Page's own LaTeX delivery cites: the export freezes it from the Page's
    selected, verified CITE Results at `delivery/latex/selected-bibliography/<page>.bib`."""
    return p["dir"] / "delivery" / "latex" / "selected-bibliography" / f"{p['id']}.bib"


def page_draft_bib(p):
    """0.9.1 · the unverified Bib a `delivery: draft` Page's export writes beside its verified one."""
    return p["dir"] / "delivery" / "latex" / "draft-bibliography" / f"{p['id']}.bib"


def citing_bib(p):
    """The Bib this build merges for a Page: its verified `page_bib`, else, when the paper
    opts in with `[evidence] draft_citations`, its draft Bib (a G4 blocker, never silent)."""
    verified = page_bib(p)
    if verified.is_file() or not DRAFT_CITATIONS or not page_draft_bib(p).is_file():
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
        fragment = p["dir"] / "delivery" / "latex" / f"{p['id']}.tex"
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
            fragment = p["dir"] / "delivery" / "latex" / f"{p['id']}.tex"
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

# ── master ───────────────────────────────────────────────────────────────────
def _inputs(pairs, folder):
    """\\input lines for one lane, a not-ready page as its numbered stub."""
    out = []
    for p, floats in pairs:
        if p.get("included", p["ready"]):
            out.append(rf"\input{{{folder}/{p['id']}}}")
            out += [rf"\input{{displays/{f}/float}}" for f in floats]
        else:
            out.append(_stub(p))
    return out


def write_paper_owned(main, appx):
    """0.9.1 · `[source] head`: the paper owns its preamble and title; the engine owns the order.

    The head and the files beside it (a .sty, the shared preamble it \\inputs) are copied into
    the room. With `appendices = "supplement"` the appendices leave master.tex: supplement.tex
    prints them alone, each on a new page, with its own reference list, and combined.tex
    prints the whole paper as one file (the arXiv copy)."""
    for f in sorted(HEAD_FILE.parent.iterdir()):
        if f.is_file() and f.suffix in {".sty", ".cls", ".clo", ".cfg", ".bst", ".tex"} \
                and not (LATEX / f.name).exists():
            shutil.copy2(f, LATEX / f.name)
    gen = (f"% GENERATED by {ENGINE_TAG}\n"
           "% The pages own the words. Edit a Section Page, then rebuild; never edit this file.\n")
    head = HEAD_FILE.read_text(encoding="utf-8").rstrip() + "\n"
    opening = OPENING_FILE.read_text(encoding="utf-8").rstrip() if OPENING_FILE else "\\maketitle"
    bib = "\\bibliographystyle{%s}\n\\bibliography{reference}\n" % LATEX_BIBSTYLE

    def doc(preamble, start, body):
        return gen + preamble + "\n\\begin{document}\n" + start + "\n\n" + body + "\n\\end{document}\n"

    main_body = "\n".join(_inputs(main, "sections"))
    appx_inputs = _inputs(appx, "appendices")
    sep = "\n\\clearpage\n" if LATEX_APPENDIX_NEWPAGE else "\n"
    combined = main_body + "\n\n" + bib
    if appx_inputs:
        combined += "\n\\clearpage\n\\appendix\n" + sep.join(appx_inputs) + "\n"
    for stale in ("supplement.tex", "combined.tex"):
        (LATEX / stale).unlink(missing_ok=True)
    if SUPPLEMENT_SPLIT and appx_inputs:
        MASTER.write_text(doc(head, opening, main_body + "\n\n" + bib), encoding="utf-8")
        supp_head = head + (SUPP_HEAD_FILE.read_text(encoding="utf-8").rstrip() + "\n" if SUPP_HEAD_FILE else "")
        supp_open = SUPP_OPENING_FILE.read_text(encoding="utf-8").rstrip() if SUPP_OPENING_FILE else opening
        (LATEX / "supplement.tex").write_text(
            doc(supp_head, supp_open, "\n\\clearpage\n".join(appx_inputs) + "\n\n\\clearpage\n" + bib),
            encoding="utf-8")
        (LATEX / "combined.tex").write_text(doc(head, opening, combined), encoding="utf-8")
    else:
        MASTER.write_text(doc(head, opening, combined), encoding="utf-8")


def write_master(main, appx, status, ready_n, total_n):
    if HEAD_FILE:
        return write_paper_owned(main, appx)
    # The Abstract PAGE is the title's authority; paper-build.toml is the fallback.
    # Both carried a title and they drifted (JL 260908), so the pages win here for
    # the same reason they win for every other word in the document.
    title = declared_title([p for p, _ in main]) or CFG["paper"].get("title", CFG["paper"]["id"])
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
% a verbatim block (a published prompt) is single-spaced, framed, and wraps inside the margin (0.8.4)
\usepackage{{fvextra}}
\RecustomVerbatimEnvironment{{verbatim}}{{Verbatim}}{{breaklines,breaksymbolleft={{}},breakindent=2ex,fontsize=\small,baselinestretch=1,frame=single,framesep=6pt}}
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
        if p.get("included", p["ready"]) and is_abstract(p):
            body.append(rf"\input{{sections/{p['id']}}}")
            if LATEX_ABSTRACT_PAGE: body.append(r"\clearpage")   # abstract (+ keywords) alone on its page
            body.append(""); continue
        if p.get("included", p["ready"]):
            if JAMA:   # the JAMA Word renderer splits the body on these four headings
                kind = re.sub(r"^(\d+|[A-Z])-", "", p["id"].rsplit("-Main-", 1)[-1]).replace("-", " ")   # 0.7.5: drop the page index
                frag_txt = (SEC / f"{p['id']}.tex").read_text(encoding="utf-8", errors="replace")
                if kind in ("Introduction", "Methods", "Results", "Discussion") and not re.search(rf"\\section\{{{kind}\}}", frag_txt):
                    body.append(rf"\section{{{kind}}}")
            body.append(rf"\input{{sections/{p['id']}}}")
            body += [rf"\input{{displays/{f}/float}}" for f in floats]
        else:
            body.append(_stub(p))
        body.append("")
    # 0.8.4 (JL 260928): the draft line below is process text in the deliverable; a blind copy (MISQ) carries
    # no acknowledgments at all, since funding and thanks would unblind it; they go in the separate title-page file.
    tail = (["\\section*{Acknowledgments}", "\\noindent\\textit{[Acknowledgments, funding and disclosures are written at submission; this build is a draft.]}", ""]
            if LATEX_ACKNOWLEDGMENTS else [])
    tail += ["\\clearpage", "\\bibliographystyle{" + LATEX_BIBSTYLE + "}", "\\bibliography{reference}", "", "\\clearpage", "\\appendix", ""]
    if JAMA:   # JAMA supplements number their floats eTable 1… / eFigure 1…, restarting after the references
        tail += ["\\setcounter{table}{0}\\renewcommand{\\tablename}{eTable}\\renewcommand{\\thetable}{\\arabic{table}}",
                 "\\setcounter{figure}{0}\\renewcommand{\\figurename}{eFigure}\\renewcommand{\\thefigure}{\\arabic{figure}}", ""]
    elif APPENDIX_PER_LETTER:   # 0.8.2: Table B1, B2 … restart in every lettered appendix (MISQ convention)
        tail += ["\\counterwithin*{table}{section}\\renewcommand{\\thetable}{\\thesection\\arabic{table}}",
                 "\\counterwithin*{figure}{section}\\renewcommand{\\thefigure}{\\thesection\\arabic{figure}}", ""]
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

PAGE_INDEX = re.compile(r"^S-.+?-(?:Main|Appendix)-(\d+|[A-Z])-")

def page_index(pid: str) -> str:
    """the index a page id carries: S-<desk>-Main-<N>-<Title> → 'N', S-<desk>-Appendix-<L>-<Title> → 'L', else ''
    (0.7.5, JL 260908: the page folder carries the section index; unnumbered pages keep title only)"""
    m = PAGE_INDEX.match(pid)
    if m:
        return m.group(1)
    t = re.match(r"^t(\d{2})_", pid)                   # a version's Task (JL 261007): t0N → N, t2N → its letter
    if not t:
        return ""
    n = int(t.group(1))
    return "" if n == 0 else str(n) if n < 20 else chr(ord("A") + n - 21) if 21 <= n < 30 else ""

def is_abstract(p) -> bool:
    """the Abstract is an unnumbered page whose H1 title is Abstract (or a legacy id ending -Abstract)"""
    return p["id"].endswith("-Abstract") or page_heading(p)[1].strip().lower() == "abstract"

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
    """the paper-level number a unit claims, read from its README ## Placement. `unit` is '<page-id>/<unit>' (0.7.5)."""
    page, _, name = unit.partition("/")
    hits = [h for g in PAGE_HOMES for h in ROOT.glob(f"{g}/{page}/results/*/payload/{name}/README.md")] if name else []
    if not hits and name:
        # Read the retired Outline lane only for papers that have not migrated
        # their DISPLAY Results yet.
        hits = [hit for home in ("draft", "outline") for g in PAGE_HOMES
                for hit in ROOT.glob(f"{g}/{page}/{home}/evidence/display/{name}/README.md")]
    if not hits: return None
    block = re.search(r"^## Placement\s*(.*?)(?=^## |\Z)",
                      hits[0].read_text(encoding="utf-8", errors="replace"), re.S | re.M)
    if not block or re.search(r"\bretired\b", block.group(1), re.I): return None
    m = PLACEMENT_NUM.search(block.group(1))
    return f"{m.group(1)} {m.group(2)}" if m else None

def label_to_unit():
    """which unit declares each label, read from the float.tex files this build copied."""
    out = {}
    for float_tex in sorted(DISP.glob("*/*/float.tex")):
        for lab in LABEL_CMD.findall(float_tex.read_text(encoding="utf-8", errors="replace")):
            out.setdefault(lab, f"{float_tex.parents[1].name}/{float_tex.parent.name}")
    return out

CITE_CMD = re.compile(r"\\cite[a-zA-Z]*\{([^}]*)\}")

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

def declared_title(pages):
    """The title the ABSTRACT PAGE declares under `### Title`, if it declares one.

    paper-build.toml also carries `[paper] title`, so the title had two sources of
    truth and they drifted: the PDF and the .docx printed "Physician Personality
    and Opioid Prescribing" while the page said "Physician Agreeableness and
    Opioid Prescribing" (JL 260908).
    """
    for p in pages:
        if not is_abstract(p):
            continue
        md = p["dir"] / f"{p['id']}.md"
        if not md.exists():
            continue
        m = re.search(r"^###\s+Title\s*$(.*?)(?=^#{2,4}\s)", md.read_text(encoding="utf-8", errors="replace"),
                      re.S | re.M)
        if m:
            for line in m.group(1).splitlines():
                if line.strip() and not line.lstrip().startswith(("<!--", ">", "(")):
                    return line.strip()
    return None


def venue_findings(pages, page_count=None):
    """Check the manuscript against the numbers the VENUE PACK measured.

    haipipe-paper-venue's store carried a measured MISQ pack (abstract 120-160
    words, never past ~185, 4-7 sentences of unstructured prose, 40-50 pages)
    while profiles/misq.toml was written from general knowledge; nothing in the
    build read it, so a 168-word 11-sentence abstract passed every gate
    (JL 260908). Any profile that declares these keys now gets the same check.
    """
    out = []
    band = PROFILE.get("abstract_words")
    hard = PROFILE.get("abstract_words_max")
    sent_band = PROFILE.get("abstract_sentences")
    pages_band = PROFILE.get("main_pages")
    pack = PROFILE.get("venue_pack", "the venue profile")
    abstract = next((p for p in pages if is_abstract(p)), None)
    if abstract and (band or hard or sent_band):
        frag = LATEX / f"sections/{abstract['id']}.tex"
        if frag.exists():
            raw = frag.read_text(encoding="utf-8", errors="replace")
            # The keywords line must go BEFORE commands are stripped: stripping turns
            # \textbf{Keywords:} into nothing and leaves the 18 bare keyword words,
            # which counted a 168-word abstract as 186.
            raw = re.split(r"\\smallskip|\\noindent\s*\\textbf\{\s*Keywords", raw)[0]
            body = re.sub(r"\\[a-zA-Z]+\*?(\{[^}]*\})?", " ", raw)
            words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", body))
            sents = len([x for x in re.split(r"(?<=[.!?])\s+", body)
                         if len(re.findall(r"[A-Za-z][A-Za-z'-]*", x)) >= 4])
            if hard and words > hard:
                out.append(f"abstract is {words} words; {pack} local writing ceiling is {hard} (pack guidance; verify official rules against the current Venue contract)")
            elif band and not (band[0] <= words <= band[1]):
                out.append(f"abstract is {words} words; {pack} target is {band[0]}-{band[1]} (pack guidance)")
            if sent_band and not (sent_band[0] <= sents <= sent_band[1]):
                out.append(f"abstract is {sents} sentences; {pack} target is {sent_band[0]}-{sent_band[1]}")
    if pages_band and page_count and not (pages_band[0] <= page_count <= pages_band[1]):
        out.append(f"main document is {page_count} pages; {pack} expects {pages_band[0]}-{pages_band[1]}")
    return out


def display_register(main, appx, extra_findings=()):
    units, counters, rows = label_to_unit(), {"figure": 0, "table": 0}, []
    cited = set()
    # Count from the FINAL master in \\input order, not from the fragments. Counting
    # fragments measured what a page CONTAINS, never what the document PRINTS, so it
    # stayed blind to a float the master \\input a second time -- the exact bug this
    # register exists to catch (proved by removing the dedupe and re-running).
    owner = {f"sections/{q['id']}": q["id"] for q, _ in main}
    owner.update({f"appendices/{q['id']}": q["id"] for q, _ in appx})
    for m in re.finditer(r"\\input\{([^}]+)\}", MASTER.read_text(encoding="utf-8", errors="replace")):
        target = LATEX / (m.group(1) + ".tex")
        if not target.exists(): continue
        target_text = target.read_text(encoding="utf-8", errors="replace")
        for group in CITE_CMD.findall(target_text):
            cited.update(k.strip() for k in group.split(",") if k.strip())
        for kind, body in FLOAT_ENV.findall(target_text):
            counters[kind] += 1
            hit = LABEL_CMD.search(body)
            lab = hit.group(1) if hit else ""
            unit = units.get(lab, "")
            rows.append({"printed": f"{kind.title()} {counters[kind]}", "kind": kind,
                         "label": lab, "unit": unit,
                         "page": owner.get(m.group(1), m.group(1)),
                         "declared": declared_number(unit) if unit else None})
    # sections: what LaTeX NUMBERS is every unstarred \section{...} in \input order; a page whose
    # fragment (or stub) prints only \section*{...} (Key Points, an abstract) gets no number.
    # 0.7.5: the declared value is the H1's §N / Appendix L; the page id carries the same index.
    def _numbered_count(p_, rel):
        """how many sections LaTeX will NUMBER for this page: every unstarred \\section{ in its placed
        file; a not-included page is a stub in master.tex with exactly one. 0.7.6: counting, not a
        flag, because a fragment whose inner divisions use \\section (md2tex mapped ### that way)
        shifts every later section number, and the register must print what the reader sees."""
        if not p_.get("included", p_["ready"]): return 1
        f = LATEX / (rel + ".tex")
        return len(re.findall(r"\\section\{", f.read_text(encoding="utf-8", errors="replace"))) if f.exists() else 0
    secs, n, letter, overnumbered = [], 0, 0, []
    for p_, _ in main:
        dec, title = page_heading(p_)
        k = _numbered_count(p_, f"sections/{p_['id']}")
        printed = f"§{n + 1}" if k else None
        if k > 1: overnumbered.append((p_["id"], k))
        n += k
        secs.append({"printed": printed, "declared": f"§{dec}" if dec and dec.isdigit() else None,
                     "index": page_index(p_["id"]), "title": title, "page": p_["id"], "ready": p_["ready"]})
    for p_, _ in appx:
        dec, title = page_heading(p_)
        k = _numbered_count(p_, f"appendices/{p_['id']}")
        printed = f"Appendix {chr(64 + letter + 1)}" if k else None
        if k > 1: overnumbered.append((p_["id"], k))
        letter += k
        secs.append({"printed": printed, "declared": f"Appendix {dec}" if dec and dec.isalpha() else None,
                     "index": page_index(p_["id"]), "title": title, "page": p_["id"], "ready": p_["ready"]})
    findings, seen_label, claimed = [], {}, {}
    for pid_, k in overnumbered:
        findings.append(f"{pid_}: its fragment prints {k} numbered sections; inner divisions should be \\subsection so the page is one §")
    for r in secs:
        if r["declared"] and r["printed"] and r["declared"] != r["printed"]:
            findings.append(f"{r['page']}: page H1 says {r['declared']}, prints {r['printed']}")
    for r in rows:
        if r["declared"] and r["declared"] != r["printed"]:
            findings.append(f"{r['unit'] or r['label']}: claims {r['declared']}, prints {r['printed']}")
        if r["unit"] and not r["declared"]:
            findings.append(f"{r['unit']}: prints {r['printed']} but its README declares no number")
        if r["label"] and r["label"] in seen_label:
            findings.append(f"label {r['label']} printed twice: {seen_label[r['label']]} and {r['printed']}")
        seen_label.setdefault(r["label"], r["printed"])
    # Check units on disk, including Pages not yet ready. Page IDs are stable
    # identities; legacy embedded indices never determine current reading order.
    ladder = [VERSION.relative_to(ROOT).as_posix() + "/"] if VERSION != ROOT else []   # 0.10.0: the version's Sections
    for page_dir in sorted(q for pat in ["B*-*-Main/*/"] + ladder for q in ROOT.glob(pat)
                           if q.is_dir() and not q.name.startswith(("_", "."))) + \
                    sorted(q for q in ROOT.glob("B*-*-Appendix/*/") if q.is_dir() and not q.name.startswith(("_", "."))):
        page = page_dir.name
        if not (page.startswith("S-") or re.match(r"^t[0-2]\d_", page)): continue
        disp = plan_home(page_dir) / "evidence" / "display"
        for unit_dir in sorted(u for u in disp.glob("*/") if u.is_dir()) if disp.exists() else []:
            unit = unit_dir.name; key = f"{page}/{unit}"
            if not re.fullmatch(r"Display\d+-[A-Za-z0-9][A-Za-z0-9-]*", unit):
                findings.append(f"legacy unit name {key}: rename to Display<n>-<slug> (the Page owns the unit independently of printed order)")
            if not (unit_dir / "README.md").exists():
                findings.append(f"{key} has no README.md, so it can declare no number")
                continue
            d = declared_number(key)
            if d: claimed.setdefault(d, []).append(key)
    for number, owners in sorted(claimed.items()):
        if len(owners) > 1:
            findings.append(f"{number} claimed by {len(owners)} units: {', '.join(owners)}")
    # 0.7.7 tooth: one work under two keys. Both cited = the reference list PRINTS it twice
    # (a finding). Only one cited = the spare entry is still staged and the next author can
    # pick the wrong key, so it is a warning rather than a finding.
    dup_both, dup_staged = duplicate_bib_works(cited)
    for keys in dup_both:
        findings.append(f"one work cited under {len(keys)} keys, so the reference list prints it twice: {', '.join(keys)}")
    for keys in dup_staged:
        BUILD_WARNINGS.append(f"bib: one work staged under {len(keys)} keys ({', '.join(keys)}); only one is cited, drop the spare before someone cites it")
    lines = [f"# Display register · GENERATED by {ENGINE_TAG}, never hand-edited", "",
             f"Built {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
             f"{counters['figure']} figure(s) + {counters['table']} table(s) printed.",
             "A number here is provisional while any page is NOT READY: a page that starts",
             "compiling inserts its floats and renumbers everything after it.", "", "```text"]
    lines.append(f"{'PRINTED':<10} {'DECLARED':<10} {'LABEL':<34} {'UNIT (page/Display<n>-slug)':<64} PAGE")
    for r in rows:
        flag = "" if (r["declared"] or "") in ("", r["printed"]) else "  ⛔"
        lines.append(f"{r['printed']:<10} {(r['declared'] or '—'):<10} {r['label']:<34} {r['unit'] or '—':<64} {r['page']}{flag}")
    lines += ["```", "", "## Sections", "", "```text"]
    lines.append(f"{'PRINTED':<12} {'DECLARED':<12} {'READY':<6} {'TITLE':<44} PAGE")
    for r in secs:
        flag = "" if (r["declared"] or r["printed"] or "") == (r["printed"] or r["declared"] or "") else "  ⛔"
        lines.append(f"{(r['printed'] or '(unnumbered)'):<12} {(r['declared'] or '—'):<12} "
                     f"{('yes' if r['ready'] else 'no'):<6} {r['title'][:44]:<44} {r['page']}{flag}")
    lines += ["```", ""]
    findings.extend(extra_findings)
    # Computed HERE, not by the caller: build() used to assemble these two and pass
    # them in, so every other entry point (the test harness included) silently ran
    # without them (found 260908 when both new teeth reported nothing under pytest).
    all_pages = [q for q, _ in main] + [q for q, _ in appx]
    page_title, cfg_title = declared_title(all_pages), CFG["paper"].get("title")
    if page_title and cfg_title and page_title != cfg_title:
        findings.append(f"title drift: the Abstract page says {page_title!r}, paper-build.toml says "
                        f"{cfg_title!r}; the page is printed")
    findings.extend(venue_findings(all_pages))
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
    # Recheck immediately before mutation, including symlinks changed since load.
    validate_build_config(CFG, HERE)
    reset_placement()
    main_ids, appx_ids, order_source = read_order()
    G_MAIN = rel(CFG["pages"]["main"])
    G_APP = rel(CFG["pages"]["appendix"]) if CFG["pages"].get("appendix") else None   # 0.7.0: appendix group optional
    if appx_ids and G_APP is None:
        raise RuntimeError("the compile-order block lists appendix Sections but paper-build.toml [pages] declares no appendix group")
    main = [inspect(i, G_MAIN) for i in main_ids]
    appx = [inspect(i, G_APP) for i in appx_ids] if G_APP else []
    pages = main + appx
    for p in pages:   # 0.6.1: a DRAFT may print an unready page's fragment when the paper opts in
        p["included"] = p["ready"] or (DRAFT_INCLUDES_UNREADY and p["fragment"].exists())
    require_page_bibs(pages)  # refuse before the last good delivery/latex/ is removed
    if LATEX.exists(): shutil.rmtree(LATEX)
    for d in (SEC, APP, DISP): d.mkdir(parents=True, exist_ok=True)
    labels = label_index(pages); unresolved = []
    prescan_embedded(pages)
    main_f = [(p, place_fragment(p, SEC, labels, unresolved) if p["included"] else []) for p in main]
    appx_f = [(p, place_fragment(p, APP, labels, unresolved) if p["included"] else []) for p in appx]
    nbib = merge_bib(pages)
    ready = [p for p in pages if p["ready"]]
    status = build_readiness(pages, unresolved)["status"]
    write_master(main_f, appx_f, status, len(ready), len(pages))
    register = display_register(main_f, appx_f)
    # compile · master.tex, and (0.9.1) supplement.tex / combined.tex when the paper declares them
    documents = [(MASTER, "main_pdf")] + [
        (LATEX / f"{name}.tex", key) for name, key in (("supplement", "supplement_pdf"), ("combined", "combined_pdf"))
        if (LATEX / f"{name}.tex").exists() and OUT.get(key)]
    rc, printed = None, {}
    for tex, key in documents:
        r = _run(["latexmk", "-pdf" if LATEX_ENGINE == "pdflatex" else "-xelatex", "-interaction=nonstopmode",
                  "-halt-on-error", "-quiet", tex.name], cwd=LATEX, capture_output=True, text=True)
        if rc is None or (rc.returncode == 0 and r.returncode != 0):
            rc = r   # the first failure is the one the manifest reports
        if (LATEX / f"{tex.stem}.pdf").exists():
            shutil.copy2(LATEX / f"{tex.stem}.pdf", rel(OUT[key]))
        log = LATEX / f"{tex.stem}.log"
        if log.exists():
            m = re.search(r"Output written on \S+ \((\d+) pages?", log.read_text(errors="replace"))
            printed[key] = int(m.group(1)) if m else None
        for junk in LATEX.glob(f"{tex.stem}.*"):
            if junk.suffix not in {".tex", ".pdf", ".bbl", ".log"}: junk.unlink()
    main_pdf = rel(OUT["main_pdf"])
    # word
    docx_rc, docx_err = None, None
    if DOCX_ENGINE.exists():
        env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(HERE / "paper-build.toml"))
        r = _run([sys.executable, str(DOCX_ENGINE)], cwd=HERE, env=env, capture_output=True, text=True)
        docx_rc, docx_err = r.returncode, unrooted((r.stderr or r.stdout)[-1500:])
    # JL 260929 "for the word, why we cannot preview it": each .docx gets its PDF twin beside it,
    # <stem>.pdf, drawn from the package the Word lane just wrote; the Paper Workbench's Word Preview shows it
    twins = {}
    if DOCX2PDF.exists():
        for key in ("main_docx", "supplement_docx"):
            docx = rel(OUT[key]) if OUT.get(key) else None
            if docx is not None and docx.suffix == ".docx" and docx.is_file():
                twin = docx.with_suffix(".pdf")
                r = _run([sys.executable, str(DOCX2PDF), str(docx), "-o", str(twin)], cwd=HERE,
                         capture_output=True, text=True, timeout=300)
                twins[key] = str(twin.relative_to(HERE)) if getattr(r, "returncode", 1) == 0 and twin.is_file() else None
    # 0.9.0 (JL 260929): the submission cover letter, words from the Round page, facts from this build
    cover = None
    if COVER_LETTER.exists() and isinstance(CFG.get("coverletter"), dict):
        import importlib.util
        spec = importlib.util.spec_from_file_location("haipipe_cover_letter", COVER_LETTER)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        cover = mod.build_cover_letter(CFG, PROFILE, ROOT, HERE, OUT,
                                       title=declared_title(main) or CFG["paper"].get("title", CFG["paper"]["id"]),
                                       main_pdf=main_pdf, tables=register["tables"], figures=register["figures"], run=_run)
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
        "pages": [{"id": p["id"], "ready": p["ready"], "reasons": p["reasons"], "warnings": p.get("warnings", []),
                   "outline": p["outline"],
                   "fragment": str(p["fragment"].relative_to(ROOT)) if p["fragment"].exists() else None} for p in pages],
        "submission_readiness": submission_readiness,
        "unresolved_refs": unresolved, "bib_entries": nbib, "displays": register, "warnings": list(BUILD_WARNINGS),
        "venue_profile": VENUE_PROFILE or None,
        "latex_profile": {"spacing": LATEX_SPACING, "bibstyle": LATEX_BIBSTYLE, "displays": LATEX_DISPLAYS,
                          "appendix_newpage": LATEX_APPENDIX_NEWPAGE, "title_page": LATEX_TITLE_PAGE,
                          "abstract_page": LATEX_ABSTRACT_PAGE, "running_head": LATEX_RUNNING_HEAD},
        "outputs": {"pdf": OUT["main_pdf"] if main_pdf.exists() else None,
                    "docx": OUT["main_docx"] if rel(OUT["main_docx"]).exists() else None,
                    "docx_pdf": twins.get("main_docx"), "supplement_docx_pdf": twins.get("supplement_docx")},
    })
    for key in ("supplement_pdf", "combined_pdf"):   # 0.9.1: the paper-owned documents and their length
        if key in printed:
            manifest["outputs"][key.replace("_pdf", "")] = OUT[key] if rel(OUT[key]).exists() else None
    manifest["pages_printed"] = printed
    manifest["draft_citations"] = list(DRAFT_CITED)
    manifest["store_reads"] = {k: list(v) for k, v in STORE_READS.items()}
    if cover is not None:
        manifest["cover_letter"] = cover
    else:
        manifest.pop("cover_letter", None)
    manifest["readiness"] = {
        "ready": len(ready),
        "total": len(pages),
        "not_ready": [{"id": p["id"], "reasons": p["reasons"]} for p in pages if not p["ready"]],
    }
    manifest["render"] = {
        "latexmk_rc": rc.returncode,
        "latexmk_tail": unrooted((rc.stdout + rc.stderr)[-1200:]) if rc.returncode else "",
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
    for key, n in printed.items():   # 0.9.1: every document this build compiled, with its length
        print(f"  {'✅' if rel(OUT[key]).exists() else '❌'} {OUT[key]} · {n} pages")
    print(f"docx: {'✅ ' + OUT['main_docx'] if rel(OUT['main_docx']).exists() else '❌ rc=' + str(docx_rc)}")
    if cover is not None:
        todo = [f"{c['check']}: {c['detail']}" for c in cover["checks"] if not c["ok"]]
        print(f"cover letter: {'✅' if cover['outputs']['pdf'] else '❌'} {cover['outputs']['pdf'] or 'latexmk rc=' + str(cover['latexmk_rc'])}"
              f" · {'ready' if cover['ready'] else 'not ready'} · words from {cover['from']}")
        for t in todo: print(f"  ✉ {t}")
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
    rounds = list(ROOT.glob(f"B*-*-Round/{rd}-*")) + (list(VERSION.glob(f"{rd}-*")) if VERSION != ROOT else [])
    if VERSION != ROOT:                     # on the ladder: a comments report of this version (b16 Q05)
        rounds += [p for p in VERSION.glob("reports/q[0-9][0-9]_*") if p.is_dir()
                   and (p.name == rd or p.name.startswith(rd + "_"))]
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
    no_supplement = str(PROFILE.get("appendices", "")).lower() == "main"
    for key, configured in OUT.items():
        if configured in ("", None):
            continue      # 0.9.0: an output switched off (e.g. section_snapshots = "") is not part of a Round
        if no_supplement and key.startswith("supplement_"):
            continue      # 0.9.0: appendices inside the manuscript (MISQ) produce no supplement file
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
    try:   # 0.9.0: say so when a letter that is not ready travels with the Round
        cover = json.loads((HERE / OUT["manifest"]).read_text(encoding="utf-8")).get("cover_letter")
    except (OSError, ValueError, KeyError):
        cover = None
    if cover and not cover.get("ready"):
        print("  ⚠ the cover letter is not ready: " + "; ".join(c["check"] for c in cover.get("checks", []) if not c["ok"]))

    for key, src in sources:
        target = dst / src.name
        if src.is_dir():
            shutil.copytree(src, target)
        else:
            shutil.copy2(src, target)
        print(f"  → {dst.relative_to(ROOT)}/{target.name} ({key})")
    print(f"{kind}/ frozen for {rounds[0].name}")

def lock_path() -> Path:
    """The build lock of this delivery/: one per folder, outside the repository."""
    digest = hashlib.sha1(str(HERE.resolve()).encode("utf-8")).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / f"haipipe-paper-build-{digest}.lock"


@contextmanager
def delivery_lock(wait: float = 600):
    """One build at a time per delivery/ (Paper-AgreeableRxDiscretion 260928: two builds ran
    in one delivery/ and one regenerated latex/ under the other, which then failed with 79
    undefined citations). An OS lock, released when the process ends even on a crash, on a
    file in the system temp folder named by this delivery/ path, so the paper repo gets no
    lock file; a second build says who holds it, waits up to `wait` seconds, then stops."""
    path = lock_path()
    handle = open(path, "a+", encoding="utf-8")
    try:
        import fcntl
        def lock(): fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        def unlock(): fcntl.flock(handle, fcntl.LOCK_UN)
    except ImportError:                                   # Windows
        import msvcrt
        def lock(): handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        def unlock(): handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    start, told = time.monotonic(), False
    while True:
        try:
            lock()
            break
        except OSError:
            handle.seek(0)
            holder = handle.read().strip() or "another build"
            if time.monotonic() - start >= wait:
                handle.close()
                sys.exit(f"delivery/ is busy: {holder} holds its build lock; try again when it finishes")
            if not told:
                print(f"waiting: {holder} holds the delivery/ build lock")
                told = True
            time.sleep(2)
    handle.seek(0); handle.truncate()
    handle.write(f"build pid {os.getpid()} started {datetime.now():%Y-%m-%d %H:%M:%S}\n"); handle.flush()
    try:
        yield
    finally:
        handle.seek(0); handle.truncate(); handle.flush()
        unlock()
        handle.close()


def check():
    """0.10.0 · a dry run: every compile-order Section's folder and body fragment, found through
    [pages]; writes nothing. Returns the number missing (a folder, or a fragment of a page that
    must print)."""
    main_ids, appx_ids, source = read_order()
    g_main = rel(CFG["pages"]["main"])
    g_app = rel(CFG["pages"]["appendix"]) if CFG["pages"].get("appendix") else None
    print(f"order: {source}")
    missing = 0
    for lane, ids, group in (("main", main_ids, g_main), ("appendix", appx_ids, g_app)):
        for pid in ids:
            d = group / pid if group else None
            frag = d / "delivery" / "latex" / f"{pid}.tex" if d else None
            state = ("no [pages] group" if d is None else "page folder missing" if not d.is_dir()
                     else "fragment" if frag.is_file() else "no fragment")
            missing += state in ("no [pages] group", "page folder missing")
            print(f"  {lane:8} {pid:48} {state}")
    print(f"{len(main_ids) + len(appx_ids)} Sections · {missing} not found")
    return missing


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if a and a[0] in {"check", "--dry-run"}:
        sys.exit(1 if check() else 0)
    if not a or a[0] == "build":
        with delivery_lock(): build()
    elif a[0] in {"send", "release"} and len(a) == 2:
        with delivery_lock(): freeze("sent" if a[0] == "send" else "released", a[1])
    else: sys.exit(__doc__)

if __name__ == "__main__":
    main()
