#!/usr/bin/env python3
"""Report on every skill: sizes, where it is installed, problems, and use.

    python3 diagnostics/skill_report.py                 # writes reports/skill_report_<YYMMDD_HHMM>.{md,csv}
    python3 diagnostics/skill_report.py --tag baseline  # writes reports/skill_report_baseline.{md,csv}
    python3 diagnostics/skill_report.py --html          # also runs md_to_html.py on the .md

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
        with mm:
            for m in SKILL_CALL_RE.finditer(mm):
                tid = m.group(1)
                if tid in calls:
                    continue
                calls[tid] = (m.group(2).decode("utf-8", "ignore"), line_date(mm, m.start()))
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
                cmds[key] = (m.group(1).decode("utf-8", "ignore").strip(), ts.group(1).decode() if ts else "")
    cutoff = (dt.date.today() - dt.timedelta(days=since_days)).isoformat()
    stats = defaultdict(lambda: {"calls": 0, "commands": 0, "recent": 0, "last": ""})
    for name, day in calls.values():
        s = stats[name]
        s["calls"] += 1
        s["recent"] += day >= cutoff
        s["last"] = max(s["last"], day)
    for name, day in cmds.values():
        s = stats[name]
        s["commands"] += 1
        s["recent"] += day >= cutoff
        s["last"] = max(s["last"], day)
    return stats, len(files)


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
    if args.no_usage:
        stats, nfiles = defaultdict(lambda: {"calls": 0, "commands": 0, "recent": 0, "last": ""}), 0
    else:
        stats, nfiles = usage(Path(args.projects), args.recent_days, not args.no_subagents)

    # map aliases and plugin-qualified names to their skill
    alias_of = {}
    for name, row in tools.items():
        for a in row["aliases"]:
            alias_of[a] = name

    def use_of(name):
        s = {"calls": 0, "commands": 0, "recent": 0, "last": ""}
        keys = [name] + [a for a, n in alias_of.items() if n == name]
        for k in keys:
            if k in stats:
                t = stats[k]
                s["calls"] += t["calls"]
                s["commands"] += t["commands"]
                s["recent"] += t["recent"]
                s["last"] = max(s["last"], t["last"])
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
                        "skill": measure(text), "folder": folder_size(src)}
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
            "problems": " | ".join(problems),
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
    }
    aliases = sorted(alias_of)
    return rows, recs, summary, stats, aliases


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def write_md(path, rows, recs, summary, stats, aliases, args):
    s = summary
    L = []
    L.append("# Skill report %s" % s["generated"])
    L.append("")
    L.append("Tools: `%s`. Tokens are characters / 4. Uses count Skill tool calls and typed `/name` "
             "commands in %d transcripts (`~/.claude/projects/*/*.jsonl`%s); recent = last %d days."
             % (TOOLS, s["transcripts"], "" if args.no_subagents else " and their `subagents/*.jsonl`",
                args.recent_days))
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append(md_table(["Measure", "Value"], [
        ("Tools skills (installable SKILL.md)", s["tools_skills"]),
        ("Parts inside Tools skills (_parts/*/PART.md)", s["tools_parts"]),
        ("Entries in ~/.claude/skills", "%d top-level; %d skills (%d links, %d copies, %d synced, %d dangling)"
         % (s["claude_top"], s["claude_entries"], s["claude_links"], s["claude_copies"], s["claude_synced"], s["claude_dangling"])),
        ("Entries in ~/.agents/skills", "%d %s" % (s["agents_entries"], ("(" + s["agents_note"] + ")") if s["agents_note"] else "")),
        ("Plugin skills", s["plugin_skills"]),
        ("Listing tokens, everything installed", fmt(s["listing_tokens_total"])),
        ("Listing tokens, Tools skills", fmt(s["listing_tokens_tools"])),
        ("SKILL.md tokens, Tools skills", fmt(s["skill_tokens_tools"])),
        ("Folder tokens, Tools skills", fmt(s["folder_tokens_tools"])),
        ("Skill tool calls / commands counted", "%s / %s" % (fmt(s["skill_calls"]), fmt(s["commands"]))),
        ("Skills with a problem", s["problems"]),
    ]))
    L.append("")
    L.append("## Recommendations")
    L.append("")
    for i, (title, detail) in enumerate(recs, 1):
        L.append("> **%d. %s**" % (i, title))
        for line in detail.splitlines():
            L.append(">")
            L.append("> " + line)
        L.append("")
    L.append("## Skills")
    L.append("")
    L.append(md_table(
        ["Skill", "Origin", "Installed", "Version", "Parts", "List tok", "SKILL lines", "SKILL tok",
         "Folder files", "Folder lines", "Folder tok", "Uses", "Recent", "Last used", "Path"],
        [(r["name"], r["origin"], r["installed"], r["version"], r["parts"].replace(";", ", "), r["listing_tokens"],
          r["skill_lines"], r["skill_tokens"], r["folder_files"], r["folder_lines"], r["folder_tokens"],
          r["uses"], r["uses_recent"], r["last_used"], r["path"].replace(str(HOME), "~"))
         for r in sorted(rows, key=lambda r: (r["origin"] != "tools", r["name"]))]))
    L.append("")
    L.append("## Problems")
    L.append("")
    probs = [(r["name"], p) for r in rows for p in r["problems"].split(" | ") if p]
    L.append(md_table(["Skill", "Problem"], probs) if probs else "None.")
    L.append("")
    L.append("## Uses not matched to a skill")
    L.append("")
    L.append("Built-in commands and names no installed skill carries (old names, plugin commands).")
    L.append("")
    known = {r["name"] for r in rows} | set(aliases)
    other = sorted(((n, s["calls"] + s["commands"], s["last"]) for n, s in stats.items() if n not in known),
                   key=lambda x: -x[1])[:40]
    L.append(md_table(["Name", "Uses", "Last used"], other) if other else "None.")
    L.append("")
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
    args = ap.parse_args()

    rows, recs, summary, stats, aliases = build(args)

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
    if args.html:
        subprocess.run([sys.executable, str(HERE / "md_to_html.py"), str(md)], check=True)


if __name__ == "__main__":
    main()
