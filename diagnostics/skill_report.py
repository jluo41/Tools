#!/usr/bin/env python3
"""Report on every skill: sizes, where it is installed, problems, and use.

    python3 diagnostics/skill_report.py                 # writes reports/skill_report_<YYMMDD_HHMM>.{md,csv}
    python3 diagnostics/skill_report.py --tag baseline  # writes reports/skill_report_baseline.{md,csv}
    python3 diagnostics/skill_report.py --html          # also runs md_to_html.py on the .md

Every run also writes the latest report as reports/skill_report.{md,csv,json,html}, and,
when reports/skill_report_baseline.* exists, a "What changed since the baseline" block.

Sizes come in three scopes, each in lines, words and tokens:
  listing  the name + description, the text every session loads
  skill    the SKILL.md file, loaded when the skill runs
  folder   every text file in the skill folder (parts, refs, scripts)
Tokens are an estimate: characters / 4 (no tokenizer is required).

Sources:
  Tools    SKILL.md files under plugins/**/skills/, skipping folders that start
           with "_" and node_modules/ (the installers' own rule); a skill's
           _parts/<name>/PART.md is counted inside its folder and listed by name
  installs ~/.claude/skills, ~/.agents/skills, and the skills/ folder of every
           plugin in ~/.claude/plugins/installed_plugins.json
  use      ~/.claude/projects/*/*.jsonl (and */<session>/subagents/*.jsonl unless
           --no-subagents): Skill tool calls (one per tool_use id) and /name
           commands typed by a person (one per message uuid)

The report names local paths, so reports/ is gitignored.
"""

import argparse
import csv
import datetime as dt
import json
import mmap
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # the fallback parser covers name, description and metadata.aliases
    yaml = None

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
HOME = Path.home()
CLAUDE_SKILLS = HOME / ".claude" / "skills"
AGENTS_SKILLS = HOME / ".agents" / "skills"
PLUGINS_JSON = HOME / ".claude" / "plugins" / "installed_plugins.json"
PROJECTS = HOME / ".claude" / "projects"
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".ps1", ".yaml", ".yml", ".json", ".toml",
                 ".js", ".ts", ".css", ".html", ".tex", ".bib", ".csv", ".r", ".R", ".do"}
LINK_RE = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKILL_CALL_RE = re.compile(rb'"type":"tool_use","id":"([^"]+)","name":"Skill","input":\{"skill":"([^"]+)"')
COMMAND_RE = re.compile(rb'"content":"<command-name>/?([^<"]+)</command-name>')
UUID_RE = re.compile(rb'"uuid":"([^"]+)"')
TS_RE = re.compile(rb'"timestamp":"(\d{4}-\d\d-\d\d)')


# ─── front matter ───────────────────────────────────────────────────────────

def split_front_matter(text):
    """Return (front matter text or None, body)."""
    if not text.startswith("---"):
        return None, text
    end = re.search(r"\n---[ \t]*(\n|$)", text[3:])
    if not end:
        return None, text
    return text[3:3 + end.start()].strip("\n"), text[3 + end.end():]


def parse_front_matter(fm):
    """Parse YAML front matter; returns (dict, error or "")."""
    if fm is None:
        return {}, "no front matter"
    if yaml is not None:
        try:
            data = yaml.safe_load(fm) or {}
            if not isinstance(data, dict):
                return {}, "front matter is not a mapping"
            return data, ""
        except yaml.YAMLError as exc:
            return {}, "front matter does not parse: " + str(exc).splitlines()[0]
    data = {}
    for key in ("name", "description"):
        m = re.search(r"(?m)^%s:\s*(.*)$" % key, fm)
        if m:
            data[key] = m.group(1).strip().strip("\"'")
    m = re.search(r"(?m)^\s+aliases:\s*\[?([^\]\n#]*)\]?", fm)
    if m:
        data["metadata"] = {"aliases": [a.strip().strip("\"'") for a in m.group(1).split(",") if a.strip()]}
    return data, ""


# ─── sizes ──────────────────────────────────────────────────────────────────

def measure(text):
    return {"lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
            "words": len(text.split()),
            "tokens": round(len(text) / 4)}


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def folder_text_files(folder):
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in ("node_modules", "__pycache__", ".git")]
        for name in files:
            p = Path(root) / name
            if p.suffix in TEXT_SUFFIXES or name in ("LICENSE",):
                yield p


def folder_size(folder):
    total = {"lines": 0, "words": 0, "tokens": 0, "files": 0}
    for p in folder_text_files(folder):
        m = measure(read_text(p))
        for k in ("lines", "words", "tokens"):
            total[k] += m[k]
        total["files"] += 1
    return total


# ─── problems ───────────────────────────────────────────────────────────────

def broken_links(folder):
    """Relative markdown links in the folder's .md files that resolve to nothing."""
    out = []
    for p in folder_text_files(folder):
        if p.suffix != ".md":
            continue
        text = read_text(p)
        in_fence = False
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith(("#", "/", "<")):
                    continue
                path = target.split("#", 1)[0]
                if not path or "{" in path or "<" in path:
                    continue
                if not (p.parent / path).exists():
                    out.append("%s:%d -> %s" % (p.relative_to(folder), n, target))
    return out


def front_matter_problems(meta, err, folder_name, kind="SKILL.md"):
    problems = []
    if err:
        return [err]
    name = meta.get("name")
    desc = meta.get("description")
    if not name:
        problems.append("no name")
    elif kind == "SKILL.md" and name != folder_name:
        problems.append("name '%s' differs from folder '%s'" % (name, folder_name))
    if not desc:
        problems.append("no description")
    elif len(str(desc)) > 1024:
        problems.append("description %d chars (> 1024)" % len(str(desc)))
    return problems


# ─── Tools skills ───────────────────────────────────────────────────────────

def tools_skills():
    """Every installable skill under plugins/**/skills/ (installer rule)."""
    rows = {}
    plugins = TOOLS / "plugins"
    for root, dirs, files in os.walk(plugins):
        dirs[:] = sorted(d for d in dirs if not d.startswith("_") and d != "node_modules")
        if "SKILL.md" in files and "/skills/" in (root + "/"):
            folder = Path(root)
            name = folder.name
            text = read_text(folder / "SKILL.md")
            fm, _ = split_front_matter(text)
            meta, err = parse_front_matter(fm)
            desc = str(meta.get("description") or "")
            listing = "%s: %s" % (meta.get("name") or name, desc)
            parts_dir = folder / "_parts"
            parts = sorted(p.name for p in parts_dir.iterdir() if (p / "PART.md").exists()) if parts_dir.is_dir() else []
            aliases = ((meta.get("metadata") or {}).get("aliases") or []) if isinstance(meta.get("metadata"), dict) else []
            if isinstance(aliases, str):
                aliases = [aliases]
            problems = front_matter_problems(meta, err, name)
            problems += ["broken link " + b for b in broken_links(folder)]
            rel = folder.relative_to(TOOLS)
            plugin = rel.parts[1] if len(rel.parts) > 1 else ""
            if name in rows:
                problems.append("duplicate name (also %s)" % rows[name]["path"])
            rows[name] = {
                "name": name, "path": str(rel), "plugin": plugin, "parts": parts,
                "aliases": [str(a) for a in aliases],
                "version": str(((meta.get("metadata") or {}) if isinstance(meta.get("metadata"), dict) else {}).get("version", "")),
                "description": desc,
                "listing": measure(listing), "skill": measure(text), "folder": folder_size(folder),
                "problems": problems,
            }
    return rows


# ─── installs ───────────────────────────────────────────────────────────────

def scan_install_dir(base, label):
    """Entries of one skills dir: name -> dict(kind, target, problems)."""
    out = {}
    if not base.exists():
        return out, "missing"
    note = ""
    if base.is_symlink():
        note = "symlink to %s" % os.path.realpath(base)
    for entry in sorted(base.iterdir()):
        name = entry.name
        if name.startswith("."):
            continue
        if name == "synced" and entry.is_dir() and not entry.is_symlink() and not (entry / "SKILL.md").exists():
            # claude.ai synced skills: managed by Claude Code, one bucket per account/org
            for bucket in sorted(p for p in entry.iterdir() if p.is_dir()):
                for sk in sorted(p for p in bucket.iterdir() if (p / "SKILL.md").exists()):
                    out.setdefault(sk.name, {"kind": "synced", "target": str(sk), "problems": [], "where": label})
            continue
        problems = []
        if entry.is_symlink():
            target = os.readlink(entry)
            real = os.path.realpath(entry)
            if not os.path.exists(real):
                kind = "dangling"
                problems.append("dangling link -> %s" % target)
            else:
                kind = "link-tools" if real.startswith(str(TOOLS)) else "link-other"
            out[name] = {"kind": kind, "target": real if os.path.exists(real) else target, "problems": problems, "where": label}
        elif entry.is_dir():
            if not (entry / "SKILL.md").exists():
                problems.append("no SKILL.md")
            else:
                meta, err = parse_front_matter(split_front_matter(read_text(entry / "SKILL.md"))[0])
                problems += front_matter_problems(meta, err, name)
            out[name] = {"kind": "copy", "target": str(entry), "problems": problems, "where": label}
        else:
            out[name] = {"kind": "file", "target": str(entry), "problems": ["not a folder"], "where": label}
    return out, note


def plugin_skills():
    out = {}
    try:
        data = json.loads(PLUGINS_JSON.read_text())
    except (OSError, ValueError):
        return out
    for key, installs in (data.get("plugins") or {}).items():
        plugin = key.split("@")[0]
        for inst in installs:
            skills_dir = Path(inst.get("installPath", "")) / "skills"
            if not skills_dir.is_dir():
                continue
            for sk in sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").exists()):
                out["%s:%s" % (plugin, sk.name)] = {"kind": "plugin", "target": str(sk), "problems": [], "where": key}
    return out


# ─── usage ──────────────────────────────────────────────────────────────────

def usage(projects=PROJECTS, since_days=30, subagents=True):
    """Count Skill tool calls and /commands across transcripts."""
    calls, cmds = {}, {}
    files = sorted(projects.glob("*/*.jsonl"))
    if subagents:
        files += sorted(projects.glob("*/*/subagents/*.jsonl"))
    for f in files:
        try:
            with open(f, "rb") as fh:
                if os.fstat(fh.fileno()).st_size == 0:
                    continue
                mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
        except (OSError, ValueError):
            continue
        # the project a transcript belongs to: ~/.claude/projects/<project>/<session>.jsonl
        proj = project_label(f.relative_to(projects).parts[0])
        with mm:
            for m in SKILL_CALL_RE.finditer(mm):
                tid = m.group(1)
                if tid in calls:
                    continue
                calls[tid] = (m.group(2).decode("utf-8", "ignore"), line_date(mm, m.start()), proj)
            for m in COMMAND_RE.finditer(mm):
                start = mm.rfind(b"\n", 0, m.start()) + 1
                end = mm.find(b"\n", m.end())
                line = mm[start:end if end != -1 else len(mm)]
                if b'"type":"user"' not in line:
                    continue
                u = UUID_RE.search(line)
                key = u.group(1) if u else ("%s:%d" % (f, m.start())).encode()
                if key in cmds:
                    continue
                ts = TS_RE.search(line)
                cmds[key] = (m.group(1).decode("utf-8", "ignore").strip(), ts.group(1).decode() if ts else "", proj)
    cutoff = (dt.date.today() - dt.timedelta(days=since_days)).isoformat()
    stats = defaultdict(lambda: {"calls": 0, "commands": 0, "recent": 0, "last": "", "projects": set()})
    for name, day, proj in calls.values():
        s = stats[name]
        s["projects"].add(proj)
        s["calls"] += 1
        s["recent"] += day >= cutoff
        s["last"] = max(s["last"], day)
    for name, day, proj in cmds.values():
        s = stats[name]
        s["projects"].add(proj)
        s["commands"] += 1
        s["recent"] += day >= cutoff
        s["last"] = max(s["last"], day)
    return stats, len(files)


def project_label(folder):
    """-Users-jl-Desktop-Tools-SPACE -> Tools-SPACE (the part after the home's Desktop/ or home)."""
    home = str(HOME).replace("/", "-")
    rest = folder[len(home):] if folder.startswith(home) else folder
    rest = rest.lstrip("-")
    return rest[len("Desktop-"):] if rest.startswith("Desktop-") else (rest or "~")


def line_date(mm, pos):
    start = mm.rfind(b"\n", 0, pos) + 1
    end = mm.find(b"\n", pos)
    m = TS_RE.search(mm[start:end if end != -1 else len(mm)])
    return m.group(1).decode() if m else ""


# ─── report ─────────────────────────────────────────────────────────────────

def merge_candidates(tools):
    """Families: a skill X and helpers X-<y> in the same parent folder."""
    fams = defaultdict(list)
    names = set(tools)
    for name, row in tools.items():
        parent = str(Path(row["path"]).parent)
        for other in names:
            if name != other and name.startswith(other + "-") and str(Path(tools[other]["path"]).parent) == parent:
                if not any(name.startswith(o + "-") and len(o) > len(other) for o in names if o != other and o in name):
                    fams[other].append(name)
    return fams


def fmt(n):
    return "{:,}".format(n)


def build(args):
    now = dt.datetime.now()
    tools = tools_skills()
    claude, claude_note = scan_install_dir(CLAUDE_SKILLS, "~/.claude/skills")
    agents, agents_note = scan_install_dir(AGENTS_SKILLS, "~/.agents/skills")
    agents_same = AGENTS_SKILLS.is_symlink() and os.path.realpath(AGENTS_SKILLS) == os.path.realpath(CLAUDE_SKILLS)
    plugins = plugin_skills()
    codex = codex_links()
    if args.no_usage:
        stats, nfiles = defaultdict(lambda: {"calls": 0, "commands": 0, "recent": 0, "last": "", "projects": set()}), 0
    else:
        stats, nfiles = usage(Path(args.projects), args.recent_days, not args.no_subagents)

    # map aliases and plugin-qualified names to their skill
    alias_of = {}
    for name, row in tools.items():
        for a in row["aliases"]:
            alias_of[a] = name

    def use_of(name):
        s = {"calls": 0, "commands": 0, "recent": 0, "last": "", "projects": set()}
        keys = [name] + [a for a, n in alias_of.items() if n == name]
        for k in keys:
            if k in stats:
                t = stats[k]
                s["calls"] += t["calls"]
                s["commands"] += t["commands"]
                s["recent"] += t["recent"]
                s["last"] = max(s["last"], t["last"])
                s["projects"] |= t["projects"]
        return s

    all_names = sorted(set(tools) | set(claude) | (set(agents) if not agents_same else set()) | set(plugins))
    rows = []
    for name in all_names:
        t = tools.get(name)
        c = claude.get(name)
        a = agents.get(name) if not agents_same else c
        p = plugins.get(name)
        installed = []
        if c:
            installed.append("claude:" + c["kind"])
        if a and not agents_same:
            installed.append("agents:" + a["kind"])
        if p:
            installed.append("plugin")
        problems = list(t["problems"]) if t else []
        for inst in (c, a if not agents_same else None, p):
            if inst:
                problems += inst["problems"]
        if t and not c:
            problems.append("in Tools, not in ~/.claude/skills (run ./install.sh --global)")
        if t and c and c["kind"] == "link-tools" and os.path.realpath(TOOLS / t["path"]) != c["target"]:
            problems.append("~/.claude/skills link points elsewhere: %s" % c["target"])
        if c and c["kind"] == "copy" and t:
            problems.append("copied folder shadows the Tools skill (replace with a link)")
        u = use_of(name.split(":")[-1] if ":" in name else name) if not p else use_of(name)
        size = t or {}
        if not t:
            src = Path((c or a or p)["target"])
            if (src / "SKILL.md").exists():
                text = read_text(src / "SKILL.md")
                meta, _ = parse_front_matter(split_front_matter(text)[0])
                size = {"listing": measure("%s: %s" % (meta.get("name") or name, meta.get("description") or "")),
                        "skill": measure(text), "folder": folder_size(src),
                        "description": str(meta.get("description") or "")}
        origin = "tools" if t else ((c or a or p)["kind"])
        rows.append({
            "name": name, "origin": origin, "path": t["path"] if t else (c or a or p)["target"],
            "version": t["version"] if t else "", "parts": ";".join(t["parts"]) if t else "",
            "installed": ",".join(installed) or "-",
            "listing_lines": size.get("listing", {}).get("lines", 0),
            "listing_words": size.get("listing", {}).get("words", 0),
            "listing_tokens": size.get("listing", {}).get("tokens", 0),
            "skill_lines": size.get("skill", {}).get("lines", 0),
            "skill_words": size.get("skill", {}).get("words", 0),
            "skill_tokens": size.get("skill", {}).get("tokens", 0),
            "folder_files": size.get("folder", {}).get("files", 0),
            "folder_lines": size.get("folder", {}).get("lines", 0),
            "folder_words": size.get("folder", {}).get("words", 0),
            "folder_tokens": size.get("folder", {}).get("tokens", 0),
            "uses": u["calls"] + u["commands"], "skill_calls": u["calls"], "commands": u["commands"],
            "uses_recent": u["recent"], "last_used": u["last"] or "-",
            "projects": len(u["projects"]), "project_names": ";".join(sorted(u["projects"])),
            "problems": " | ".join(problems),
            "area": area_of(t["path"] if t else "", origin, name),
            "what": short_what(size.get("description", "")),
        })

    # what is loaded every session: everything visible in ~/.claude/skills plus plugins
    listed = [r for r in rows if "claude:" in r["installed"] or "plugin" in r["installed"]]
    total_listing = sum(r["listing_tokens"] for r in listed)
    tools_rows = [r for r in rows if r["origin"] == "tools"]

    # recommendations
    recs = []
    retire = [r for r in rows if r["origin"] == "copy" and r["uses"] == 0
              and r["name"] not in set(args.keep)]
    if retire:
        recs.append(("Retire %d copied skill(s) not in Tools with zero uses" % len(retire),
                     "Move (never rm) to ~/.claude/skills-retired-%s/: %s"
                     % (now.strftime("%y%m%d"), ", ".join(r["name"] for r in retire))))
    else:
        recs.append(("No copied skill to retire",
                     "Every entry in ~/.claude/skills is a link into Tools, a kept skill, or managed by Claude (synced)."))
    dangling = [r for r in rows if "dangling" in r["problems"]]
    if dangling:
        recs.append(("Remove %d dangling link(s)" % len(dangling),
                     "Then rerun ./install.sh --global: " + ", ".join(r["name"] for r in dangling)))
    missing = [r for r in tools_rows if "not in ~/.claude/skills" in r["problems"]]
    if missing:
        recs.append(("Install %d Tools skill(s) not linked yet" % len(missing),
                     "./install.sh --global links: " + ", ".join(r["name"] for r in missing)))
    fams = merge_candidates(tools)
    if fams:
        lines = []
        for main in sorted(fams, key=lambda m: -len(fams[m])):
            helpers = fams[main]
            tok = sum(tools[h]["listing"]["tokens"] for h in helpers)
            used = sum(use_of(h)["calls"] + use_of(h)["commands"] for h in helpers)
            lines.append("%s + %d helper(s), %s listing tokens, %d uses: %s"
                         % (main, len(helpers), fmt(tok), used, ", ".join(sorted(helpers))))
        recs.append(("Merge %d helper families into their main skill (_parts/<name>/PART.md)" % len(fams),
                     "\n".join(lines)))
    bad = [r for r in tools_rows if r["problems"] and "not in ~/.claude/skills" not in r["problems"]]
    if bad:
        recs.append(("Fix %d Tools skill(s) with problems" % len(bad),
                     "Broken links or front matter; see the Problems table."))
    heavy = sorted((r for r in tools_rows if r["listing_tokens"] >= args.long_listing), key=lambda r: -r["listing_tokens"])
    if heavy:
        recs.append(("Shorten %d long description(s) (>= %d listing tokens)" % (len(heavy), args.long_listing),
                     ", ".join("%s (%d)" % (r["name"], r["listing_tokens"]) for r in heavy[:15])
                     + (" ..." if len(heavy) > 15 else "")))
    unused = sorted((r for r in tools_rows if r["uses"] == 0), key=lambda r: -r["listing_tokens"])
    if unused:
        recs.append(("%d Tools skill(s) never used in transcripts" % len(unused),
                     "Listing tokens they cost every session: %s. Largest: %s"
                     % (fmt(sum(r["listing_tokens"] for r in unused)),
                        ", ".join("%s (%d)" % (r["name"], r["listing_tokens"]) for r in unused[:12]))))

    summary = {
        "generated": now.strftime("%Y-%m-%d %H:%M"),
        "tools_skills": len(tools_rows),
        "tools_parts": sum(len(t["parts"]) for t in tools.values()),
        "claude_entries": len(claude),
        "claude_top": sum(1 for e in CLAUDE_SKILLS.iterdir() if not e.name.startswith(".")) if CLAUDE_SKILLS.exists() else 0,
        "claude_links": sum(1 for v in claude.values() if v["kind"].startswith("link")),
        "claude_copies": sum(1 for v in claude.values() if v["kind"] == "copy"),
        "claude_synced": sum(1 for v in claude.values() if v["kind"] == "synced"),
        "claude_dangling": sum(1 for v in claude.values() if v["kind"] == "dangling"),
        "agents_entries": len(agents), "agents_note": agents_note or ("same as ~/.claude/skills" if agents_same else ""),
        "plugin_skills": len(plugins),
        "listing_tokens_total": total_listing,
        "listing_tokens_tools": sum(r["listing_tokens"] for r in tools_rows),
        "skill_tokens_tools": sum(r["skill_tokens"] for r in tools_rows),
        "folder_tokens_tools": sum(r["folder_tokens"] for r in tools_rows),
        "transcripts": nfiles,
        "skill_calls": sum(s["calls"] for s in stats.values()),
        "commands": sum(s["commands"] for s in stats.values()),
        "problems": sum(1 for r in rows if r["problems"]),
        "codex_links": codex["links"], "codex_dangling": codex["dangling"], "codex_targets": codex["targets"],
    }
    aliases = sorted(alias_of)
    return rows, recs, summary, stats, aliases


def codex_links():
    """~/.codex/skills: how many links, how many dangle, where the dangling ones point."""
    base = HOME / ".codex" / "skills"
    out = {"links": 0, "dangling": 0, "targets": {}}
    if not base.is_dir():
        return out
    for e in base.iterdir():
        if e.is_symlink():
            out["links"] += 1
            if not os.path.exists(os.path.realpath(e)):
                out["dangling"] += 1
                root = os.readlink(e).split("/skills/")[0] if "/skills/" in os.readlink(e) else os.path.dirname(os.readlink(e))
                out["targets"][root] = out["targets"].get(root, 0) + 1
    return out


AREA_ORDER = ["Utilities", "Base", "Theme", "Package", "Plugin", "From claude.ai", "Copied in", "Other"]


def area_of(path, origin, name):
    """A reader's group: Utilities, Base · <family>, Theme · <theme>, Package · <plugin>, ..."""
    parts = Path(path).parts if path else ()
    if parts and len(parts) > 3 and parts[1] == "haipipe-toolkit":
        layer = parts[3]
        if layer == "0_utils":
            return "Utilities"
        if layer == "1_base" and len(parts) > 4:
            return "Base · " + parts[4]
        if layer == "2_theme" and len(parts) > 4:
            return "Theme · " + parts[4]
        return "Other"
    if parts and len(parts) > 1:
        return "Package · " + parts[1]
    if origin == "synced":
        return "From claude.ai (synced)"
    if origin == "plugin":
        return "Plugin · " + name.split(":")[0]
    if origin == "copy":
        return "Copied in (not from Tools)"
    return "Other"


def area_key(area):
    head = area.split(" ")[0]
    return (next((i for i, a in enumerate(AREA_ORDER) if area.startswith(a)), len(AREA_ORDER)), area)


def short_what(desc, width=110):
    """The first sentence of a description, without its Trigger list."""
    d = re.sub(r"\s+", " ", str(desc or "")).strip()
    d = re.split(r"\s*Trigger[s]?:", d)[0].strip()
    m = re.search(r"^(.+?[.!?])(\s|$)", d)
    d = m.group(1) if m else d
    return d if len(d) <= width else d[:width - 1].rstrip() + "…"


def bar(value, total, width=24):
    n = int(round(width * value / total)) if total else 0
    return "█" * n + "·" * (width - n)


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def write_md(path, rows, recs, summary, stats, aliases, args):
    """The report, grouped by topic: at a glance, what is there, use, cost, installs, problems, advice."""
    s = summary
    tools_rows = [r for r in rows if r["origin"] == "tools"]
    areas = {}
    for r in rows:
        areas.setdefault(r["area"], []).append(r)
    order = sorted(areas, key=area_key)
    tools_areas = [a for a in order if any(r["origin"] == "tools" for r in areas[a])]
    total_tok = sum(r["listing_tokens"] for r in tools_rows) or 1
    unused = [r for r in tools_rows if r["uses"] == 0]
    probs = [(r["name"], p) for r in rows for p in r["problems"].split(" | ") if p]
    L = []
    add = L.append

    add("# Skill report · %s" % s["generated"])
    add("")
    add("What is installed, what it costs every session, what is used, and what to do next. "
        "Tokens are characters / 4. Uses = Skill tool calls + typed `/name` commands in %s transcripts%s; "
        "recent = last %d days."
        % (fmt(s["transcripts"]), "" if args.no_subagents else " (sessions and their subagents)", args.recent_days))
    add("")

    # 1. at a glance
    add("## 1. At a glance")
    add("")
    add(md_table(["", "Now"], [
        ("Skills in Tools", s["tools_skills"]),
        ("Parts inside them (`_parts/*/PART.md`, not listed)", s["tools_parts"]),
        ("Areas (utilities, base families, themes, packages)", len(tools_areas)),
        ("Entries in `~/.claude/skills`", "%d (%d dangling)" % (s["claude_top"], s["claude_dangling"])),
        ("Listing tokens every session (all installed)", fmt(s["listing_tokens_total"])),
        ("Tools skills never used", "%d of %d" % (len(unused), len(tools_rows))),
        ("Skills with a problem", s["problems"]),
        ("Used in 2+ projects", sum(1 for r in tools_rows if r["projects"] >= 2)),
    ]))
    add("")
    add("**Key findings**")
    add("")
    top = sorted(tools_rows, key=lambda r: -r["uses"])[:3]
    heavy_area = max(tools_areas, key=lambda a: sum(r["listing_tokens"] for r in areas[a] if r["origin"] == "tools"))
    heavy_tok = sum(r["listing_tokens"] for r in areas[heavy_area] if r["origin"] == "tools")
    findings = [
        "Most used: %s." % ", ".join("`%s` (%d)" % (r["name"], r["uses"]) for r in top),
        "%d of %d Tools skills were never used; they cost %s listing tokens every session."
        % (len(unused), len(tools_rows), fmt(sum(r["listing_tokens"] for r in unused))),
        "The heaviest area is %s: %s listing tokens (%d%%)." % (heavy_area, fmt(heavy_tok), 100 * heavy_tok // total_tok),
        "%d skills have a problem (broken links, long descriptions, front matter); see section 6." % s["problems"],
    ]
    if s.get("codex_dangling"):
        findings.append("`~/.codex/skills`: %d of %d links dangle (they point at an old checkout)."
                        % (s["codex_dangling"], s["codex_links"]))
    for i, f in enumerate(findings, 1):
        add("%d. %s" % (i, f))
    add("")
    add("**Where the listing tokens go** (Tools skills, by area)")
    add("")
    add("```text")
    width = max(len(a) for a in tools_areas)
    peak = max(sum(r["listing_tokens"] for r in areas[a] if r["origin"] == "tools") for a in tools_areas)
    for a in sorted(tools_areas, key=lambda a: -sum(r["listing_tokens"] for r in areas[a] if r["origin"] == "tools")):
        t = sum(r["listing_tokens"] for r in areas[a] if r["origin"] == "tools")
        n = sum(1 for r in areas[a] if r["origin"] == "tools")
        add("%-*s %s %6s  %2d%%  %3d skills" % (width, a, bar(t, peak), fmt(t), 100 * t // total_tok, n))
    add("```")
    add("")

    base = getattr(args, "_baseline", None)
    if base:
        b, bnames = base
        add("**What changed since the baseline** (%s)" % b.get("generated", "?"))
        add("")
        keys = [("Skills in Tools", "tools_skills"), ("Parts inside them", "tools_parts"),
                ("Entries in `~/.claude/skills`", "claude_top"), ("Dangling links", "claude_dangling"),
                ("Listing tokens, Tools skills", "listing_tokens_tools"),
                ("Listing tokens, all installed", "listing_tokens_total"), ("Skills with a problem", "problems")]
        add(md_table(["", "Baseline", "Now", "Change"],
                     [(label, fmt(b.get(k, 0)), fmt(s.get(k, 0)), "%+d" % (s.get(k, 0) - b.get(k, 0)))
                      for label, k in keys if k in b]))
        add("")
        now_names = {r["name"] for r in tools_rows}
        gone = sorted(set(bnames) - now_names)
        new = sorted(now_names - set(bnames))
        mains = [(r["name"], p) for r in tools_rows for p in r["parts"].split(";") if p]
        # a part's CHANGELOG names the skill it was ("was the skill `X`", merge_parts.py)
        was = {}
        for r in tools_rows:
            for part in filter(None, r["parts"].split(";")):
                cl = TOOLS / r["path"] / "_parts" / part / "CHANGELOG.md"
                for old in re.findall(r"was the skill `([^`]+)`", read_text(cl)):
                    was[old] = r["name"]
        merged = {}
        for g in gone:
            hit = was.get(g) or next((m[0] for m in sorted(mains, key=lambda m: -len(m[1]))
                                      if g == m[1] or g.endswith("-" + m[1])), None)
            merged.setdefault(hit or "(moved or removed)", []).append(g)
        if gone:
            add("Left the skill list: %d. Each is now a part of its main skill, `<main>/_parts/<name>/PART.md`:" % len(gone))
            add("")
            for main, names in sorted(merged.items()):
                add("- `%s` ← %s" % (main, ", ".join(names)))
            add("")
        if new:
            add("New in the list: %s." % ", ".join("`%s`" % n for n in new))
            add("")

    # 2. what is there
    add("## 2. What is there, by area")
    add("")
    add("One row per area, then each area opens to its skills with a one-line summary of what each does.")
    add("")
    add(md_table(["Area", "Skills", "Parts", "Listing tok", "Uses", "Never used", "Last used"], [
        (a, len(areas[a]), sum(len(r["parts"].split(";")) for r in areas[a] if r["parts"]),
         fmt(sum(r["listing_tokens"] for r in areas[a])), sum(r["uses"] for r in areas[a]),
         sum(1 for r in areas[a] if r["uses"] == 0),
         max((r["last_used"] for r in areas[a] if r["last_used"] != "-"), default="-")) for a in order]))
    add("")
    for a in order:
        rs = sorted(areas[a], key=lambda r: (-r["uses"], r["name"]))
        add("<details>")
        add("<summary><strong>%s</strong> · %d skills · %s uses · %s listing tokens</summary>"
            % (a, len(rs), sum(r["uses"] for r in rs), fmt(sum(r["listing_tokens"] for r in rs))))
        add("")
        add(md_table(["Skill", "What it does", "Uses", "Projects", "Last used", "List tok", "SKILL lines", "Parts"],
                     [(r["name"], r["what"], r["uses"], r["projects"], r["last_used"], r["listing_tokens"],
                       r["skill_lines"], r["parts"].replace(";", ", ")) for r in rs]))
        add("")
        add("</details>")
        add("")

    # 3. use
    add("## 3. How they are used")
    add("")
    add("**Most used** (all time)")
    add("")
    used = sorted((r for r in rows if r["uses"]), key=lambda r: -r["uses"])[:20]
    add(md_table(["Skill", "Area", "Uses", "Recent", "Last used"],
                 [(r["name"], r["area"], r["uses"], r["uses_recent"], r["last_used"]) for r in used]))
    add("")
    add("**Never used**, by area: %d Tools skills" % len(unused))
    add("")
    add(md_table(["Area", "Never used", "Skills"], [
        (a, len(n), ", ".join(r["name"] for r in sorted(n, key=lambda r: r["name"])))
        for a in tools_areas for n in [[r for r in areas[a] if r["origin"] == "tools" and r["uses"] == 0]] if n]))
    add("")
    known = {r["name"] for r in rows} | set(aliases)
    other = sorted(((n, x["calls"] + x["commands"], x["last"]) for n, x in stats.items() if n not in known),
                   key=lambda x: -x[1])[:20]
    if other:
        add("**Names typed that no skill carries** (built-in commands, retired or old names)")
        add("")
        add(md_table(["Name", "Uses", "Last used"], other))
        add("")

    # 4. cost
    add("## 4. What they cost")
    add("")
    add("The listing (name + description) is loaded in every session; SKILL.md only when the skill runs.")
    add("")
    add("**Longest descriptions** (listing tokens)")
    add("")
    add(md_table(["Skill", "Area", "List tok", "Uses"],
                 [(r["name"], r["area"], r["listing_tokens"], r["uses"])
                  for r in sorted(tools_rows, key=lambda r: -r["listing_tokens"])[:15]]))
    add("")
    add("**Largest folders** (all text files)")
    add("")
    add(md_table(["Skill", "Area", "Files", "Lines", "Tokens"],
                 [(r["name"], r["area"], r["folder_files"], fmt(r["folder_lines"]), fmt(r["folder_tokens"]))
                  for r in sorted(tools_rows, key=lambda r: -r["folder_tokens"])[:10]]))
    add("")

    # 5. installs
    add("## 5. Where they are installed")
    add("")
    plug = {}
    for r in rows:
        if r["origin"] == "plugin":
            plug[r["area"]] = plug.get(r["area"], 0) + 1
    inst = [
        ("`~/.claude/skills`", "%d entries: %d links into Tools, %d copied folders, %d synced from claude.ai, %d dangling"
         % (s["claude_top"], s["claude_links"], s["claude_copies"], s["claude_synced"], s["claude_dangling"])),
        ("`~/.agents/skills`", "%d entries%s" % (s["agents_entries"], (" (" + s["agents_note"] + ")") if s["agents_note"] else "")),
        ("Plugins", ", ".join("%s (%d)" % (k.replace("Plugin · ", ""), v) for k, v in sorted(plug.items())) or "none"),
    ]
    if s.get("codex_links"):
        inst.append(("`~/.codex/skills`", "%d links, %d dangling%s" % (
            s["codex_links"], s["codex_dangling"],
            (": " + ", ".join("%s (%d)" % (k.replace(str(HOME), "~"), v)
                              for k, v in sorted(s["codex_targets"].items(), key=lambda kv: -kv[1])[:3]))
            if s["codex_dangling"] else "")))
    add(md_table(["Place", "What is there"], inst))
    add("")

    # 6. problems
    add("## 6. Problems")
    add("")
    kinds = [("Broken links", lambda p: p.startswith("broken link")),
             ("Descriptions over 1,024 characters", lambda p: p.startswith("description")),
             ("Front matter", lambda p: p.startswith(("no ", "name ", "front matter"))),
             ("Install", lambda p: True)]
    seen = set()
    if not probs:
        add("None.")
    for title, test in kinds:
        group = [(n, p) for n, p in probs if (n, p) not in seen and test(p)]
        if not group:
            continue
        seen.update(group)
        add("**%s** (%d)" % (title, len(group)))
        add("")
        add(md_table(["Skill", "Problem"], [(n, p.replace("broken link ", "")) for n, p in group]))
        add("")

    # 7. scope
    add("## 7. Scope: global or per project")
    add("")
    add("Today every Tools skill is linked into `~/.claude/skills`, so its listing loads in every session of "
        "every project. Grouped by how many projects used it (a project = one folder under `~/.claude/projects`):")
    add("")
    groups = [("Global: used in 2+ projects", [r for r in tools_rows if r["projects"] >= 2]),
              ("One project: install there only", [r for r in tools_rows if r["projects"] == 1]),
              ("Never used: hide or retire", [r for r in tools_rows if r["projects"] == 0])]
    peak_g = max(sum(r["listing_tokens"] for r in g) for _, g in groups) or 1
    add("```text")
    for label, g in groups:
        t = sum(r["listing_tokens"] for r in g)
        add("%-33s %s %6s tokens  %3d skills" % (label, bar(t, peak_g), fmt(t), len(g)))
    add("```")
    add("")
    add("Hiding uses the built-in front matter field `disable-model-invocation: true`: the description leaves "
        "the listing, `/name` still works, and the folder does not move. A skill that agents or other skills "
        "call through the Skill tool must stay visible (or be read by path, as parts are).")
    add("")
    for label, g in groups[:2]:
        add("<details>")
        add("<summary><strong>%s</strong> · %d skills · %s listing tokens</summary>"
            % (label, len(g), fmt(sum(r["listing_tokens"] for r in g))))
        add("")
        add(md_table(["Skill", "Area", "Projects", "Uses", "List tok"],
                     [(r["name"], r["area"], r["project_names"].replace(";", ", "), r["uses"], r["listing_tokens"])
                      for r in sorted(g, key=lambda r: (-r["projects"], -r["uses"]))]))
        add("")
        add("</details>")
        add("")

    # 8. recommendations
    add("## 8. Recommendations")
    add("")
    for i, (title, detail) in enumerate(recs, 1):
        add("> **%d. %s**" % (i, title))
        for line in detail.splitlines():
            add(">")
            add("> " + line)
        add("")

    # appendix
    add("## Appendix: every skill, every number")
    add("")
    add("<details>")
    add("<summary>Open the full table (%d rows)</summary>" % len(rows))
    add("")
    add(md_table(
        ["Skill", "Area", "Origin", "Installed", "Version", "Parts", "List tok", "SKILL lines", "SKILL tok",
         "Folder files", "Folder lines", "Folder tok", "Uses", "Recent", "Last used", "Path"],
        [(r["name"], r["area"], r["origin"], r["installed"], r["version"], r["parts"].replace(";", ", "),
          r["listing_tokens"], r["skill_lines"], r["skill_tokens"], r["folder_files"], r["folder_lines"],
          r["folder_tokens"], r["uses"], r["uses_recent"], r["last_used"], r["path"].replace(str(HOME), "~"))
         for r in sorted(rows, key=lambda r: (area_key(r["area"]), r["name"]))]))
    add("")
    add("</details>")
    add("")
    path.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tag", help="file tag instead of the timestamp (e.g. baseline, after)")
    ap.add_argument("--out", default=str(HERE / "reports"), help="output folder")
    ap.add_argument("--projects", default=str(PROJECTS), help="transcript root")
    ap.add_argument("--recent-days", type=int, default=30)
    ap.add_argument("--long-listing", type=int, default=150, help="listing tokens that count as long")
    ap.add_argument("--keep", nargs="*", default=["partner-ai-playbook", "pr-review"],
                    help="copied skills never proposed for retirement")
    ap.add_argument("--no-usage", action="store_true", help="skip the transcript scan")
    ap.add_argument("--no-subagents", action="store_true",
                    help="count only session transcripts, not */<session>/subagents/*.jsonl")
    ap.add_argument("--html", action="store_true", help="also write the .html with md_to_html.py")
    ap.add_argument("--baseline", default=str(HERE / "reports" / "skill_report_baseline"),
                    help="a tagged report (path without extension) to compare against")
    args = ap.parse_args()

    rows, recs, summary, stats, aliases = build(args)
    bpath = Path(args.baseline)
    if args.tag != bpath.name.replace("skill_report_", "") and bpath.with_suffix(".json").exists():
        bnames = [r["name"] for r in csv.DictReader(open(bpath.with_suffix(".csv"), encoding="utf-8"))
                  if r.get("origin") == "tools"] if bpath.with_suffix(".csv").exists() else []
        args._baseline = (json.loads(bpath.with_suffix(".json").read_text(encoding="utf-8")), bnames)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = args.tag or dt.datetime.now().strftime("%y%m%d_%H%M")
    md = out / ("skill_report_%s.md" % tag)
    write_md(md, rows, recs, summary, stats, aliases, args)
    with open(out / ("skill_report_%s.csv" % tag), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (out / ("skill_report_%s.json" % tag)).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("wrote %s (+ .csv, .json)" % md)
    for k in ("tools_skills", "tools_parts", "claude_top", "claude_entries", "listing_tokens_total", "listing_tokens_tools", "problems"):
        print("  %-22s %s" % (k, summary[k]))
    # the latest run also lands under one stable name: reports/skill_report.{md,csv,json,html}
    for ext in (".md", ".csv", ".json"):
        (out / ("skill_report" + ext)).write_bytes((out / ("skill_report_%s%s" % (tag, ext))).read_bytes())
    if args.html:
        for target in (md, out / "skill_report.md"):
            subprocess.run([sys.executable, str(HERE / "md_to_html.py"), str(target)], check=True)


if __name__ == "__main__":
    main()
