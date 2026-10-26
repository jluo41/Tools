#!/usr/bin/env python3
"""Merge small helper skills into their main skill as _parts/<name>/PART.md.

    python3 diagnostics/merge_parts.py --spec task-pipeline --dry-run
    python3 diagnostics/merge_parts.py --spec task-pipeline
    python3 diagnostics/merge_parts.py --main <dir> --helper <dir>=<part> [--helper ...] \
        [--style command|path] [--words <part>="<words>"]

For each helper of a main skill:
  1. git mv <helper>/ -> <main>/_parts/<part>/ and SKILL.md -> PART.md, so git
     sees renames. The installers skip folders that start with "_", so the part
     is no longer listed as a skill; only its main skill is.
  2. PART.md front matter: name: <part>, part-of: <main>; its allowed-tools go
     into the main skill's allowed-tools; "invoked directly" phrases are retired.
  3. Every text file in the repo (except --protect paths, which are only
     reported) gets its references rewritten:
       paths      ../<helper>/ref/x.md -> resolved and re-relativized to the part,
                  <helper>/SKILL.md -> .../_parts/<part>/PART.md; files that moved
                  have their own relative links re-based
       Skill()    Skill("<helper>", args="v") -> Skill("<main>", args="<words> v")
       companions [.., <helper>, ..] -> [.., <main>, ..] (deduplicated; a skill
                  never lists itself)
       commands   /<helper> -> /<main> <words>   (style "command")
                  /<helper> -> <main>/_parts/<part>  (style "path")
       names      <helper> -> <main> <words>  or  <main>/_parts/<part>
  4. One CHANGELOG entry and one version bump per affected skill or part, keyed
     by --marker so a rerun never adds a second one (minor bump for a main skill,
     patch for everything else; a change to CHANGELOG.md alone bumps nothing).
  5. Prints what is left for a person: brace and placeholder forms
     (<main>-{a,b}, <main>-<layer>), short forms (-<part>), protected-path hits.

The main skill's routing prose (its own Skill() dispatch, its description) is
judgment work and is left to a person; the script prints the parts' trigger
lines to fold in.
"""

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TODAY = dt.date.today().isoformat()
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".ps1", ".yaml", ".yml", ".json", ".toml",
                 ".js", ".ts", ".css", ".html", ".tex", ".excalidraw", ".csv", ".do", ".r", ".R"}
TASK = "plugins/haipipe-toolkit/skills/1_base/task"
DISPLAY = "plugins/haipipe-toolkit/skills/1_base/display"
THEME = "plugins/haipipe-toolkit/skills/2_theme"
BASE = "plugins/haipipe-toolkit/skills/1_base"

SPECS = {
    # 261025: the task family's pipeline umbrellas and two fit/agent companions.
    "task-pipeline": [
        {"main": TASK + "/2_nn/haipipe-nn", "style": "command",
         "helpers": {TASK + "/2_nn/haipipe-nn-" + p: p for p in ("algo", "tuner", "instance", "modelset")}},
        {"main": TASK + "/3_end/haipipe-end", "style": "command",
         "helpers": {TASK + "/3_end/haipipe-end-" + p: p for p in (
             "meta", "trig", "post", "src2input", "input2src", "endpointset",
             "develop-local", "develop-sagemaker", "develop-databricks",
             "deploy-local", "deploy-sagemaker", "deploy-databricks", "deploy-mlflow")},
         "words": {p: p.replace("-", " ") for p in (
             "develop-local", "develop-sagemaker", "develop-databricks",
             "deploy-local", "deploy-sagemaker", "deploy-databricks", "deploy-mlflow")}},
        {"main": TASK + "/1_data/haipipe-data", "style": "command",
         "helpers": {TASK + "/1_data/haipipe-data-" + p: p for p in (
             "raw", "source", "record", "case", "aidata", "external", "remote")}},
        {"main": TASK + "/5_fit/haipipe-task-for-fit", "style": "path",
         "helpers": {TASK + "/5_fit/haipipe-task-for-fit/haipipe-task-gpu": "gpu",
                     TASK + "/5_fit/haipipe-task-for-fit/haipipe-task-gpu-training": "gpu-training"}},
        {"main": TASK + "/9_agent/haipipe-task-for-agent", "style": "path",
         "helpers": {TASK + "/9_agent/haipipe-task-llm-engine": "llm-engine"}},
    ],    # 261026 (third pass, JL: "别人的代码 ... 直接把它放到 part 里面去"): every copied outside skill
    # still listed becomes a part of the door that uses it; html-ppt stays (its own plugin, served).
    "originals": [
        {"main": BASE + "/ideation/haipipe-ideation", "style": "command",
         "helpers": {BASE + "/ideation/1_generate/idea-creator": "idea-creator",
                     BASE + "/ideation/2_test/novelty-check": "aris-novelty-check"},
         "no_bare": ("idea-creator", "novelty-check")},
        {"main": BASE + "/search/haipipe-search", "style": "command",
         "helpers": {BASE + "/search/1_search/" + n: n for n in ("arxiv", "semantic-scholar", "openalex")},
         "no_bare": ("arxiv", "semantic-scholar", "openalex")},
        {"main": THEME + "/discovery/haipipe-discovery", "style": "command",
         "helpers": {THEME + "/discovery/2_review/" + n: n for n in ("academic-researcher", "comm-lit-review", "research-lit")},
         "no_bare": ("academic-researcher", "comm-lit-review", "research-lit")},
    ],
    # 261026 (second pass): helpers no server, agent or test names, and that were never used;
    # copied outside skills (generic names) get no bare-name rewriting.
    "base-more": [
        {"main": BASE + "/ideation/haipipe-ideation", "style": "command",
         "helpers": {BASE + "/ideation/haipipe-ideation-generate": "generate",
                     BASE + "/ideation/haipipe-ideation-test": "test",
                     BASE + "/ideation/haipipe-ideation-select": "select",
                     BASE + "/ideation/haipipe-idea-pressure-test": "pressure-test",
                     BASE + "/ideation/haipipe-novelty-check": "novelty-check",
                     BASE + "/ideation/haipipe-journal-fit": "journal-fit",
                     BASE + "/ideation/haipipe-nature-paper-review": "nature-paper-review",
                     BASE + "/ideation/1_generate/framing-research-questions": "framing-research-questions",
                     BASE + "/ideation/2_test/kill-argument": "kill-argument",
                     BASE + "/ideation/2_test/paper-reviewer": "paper-reviewer"},
         "no_bare": ("framing-research-questions", "kill-argument", "paper-reviewer")},
        {"main": BASE + "/search/haipipe-search", "style": "command",
         "helpers": {BASE + "/search/1_search/" + n: n for n in
                     ("alphaxiv", "deepxiv", "exa-search", "gemini-search", "paper-analyzer")},
         "no_bare": ("alphaxiv", "deepxiv", "exa-search", "gemini-search", "paper-analyzer")},
        {"main": BASE + "/evidence/haipipe-evidence", "style": "command",
         "helpers": {BASE + "/evidence/haipipe-evidence-cite": "cite",
                     BASE + "/evidence/haipipe-evidence-work": "work"}},
        {"main": "plugins/inlab-human/skills/inlab-human", "style": "command",
         "helpers": {"plugins/inlab-human/skills/inlab-human-" + n: n for n in ("bundle", "console", "report", "review")}},
        {"main": BASE + "/draft/haipipe-draft-review", "style": "command",
         "helpers": {BASE + "/draft/haipipe-draft-review/1_style/writing-dna-skill": "writing-dna-skill",
                     BASE + "/draft/haipipe-draft-review/2_evaluate/humanizer": "humanizer",
                     BASE + "/draft/haipipe-draft-review/2_evaluate/academic-humanizer": "academic-humanizer"},
         "no_bare": ("writing-dna-skill", "humanizer", "academic-humanizer")},
        {"main": DISPLAY + "/haipipe-display", "style": "command",
         "helpers": {DISPLAY + "/" + n: n for n in ("figure-to-svg", "html-to-svg", "icon-to-svg")},
         "no_bare": ("figure-to-svg", "html-to-svg", "icon-to-svg")},
    ],
    # 261026: the theme helpers no workbench server, test or run card names (the rest wait for
    # the servers to find parts: host_paths.skill_dir skips "_" folders).
    "theme-free": [
        {"main": THEME + "/insight/haipipe-insight", "style": "command",
         "helpers": {THEME + "/insight/haipipe-insight-bind": "bind"}},
        {"main": THEME + "/paper/haipipe-paper", "style": "command",
         "helpers": {THEME + "/paper/haipipe-paper-related": "related"}},
    ],
    # 261026: the display door and its five renderers.
    "display": [
        {"main": DISPLAY + "/haipipe-display", "style": "command",
         "helpers": {DISPLAY + "/haipipe-display-" + p: p for p in ("table", "figure", "diagram", "illustration", "tex")}},
    ],
}

# Never read: upstream sources and this folder (its SPECS name the helpers).
SKIP = ["references/", "diagnostics/", ".git/"]
# Paths another session owns in this checkout: report hits, never edit.
PROTECT = [
    "blueprints/",
    "plugins/haipipe-toolkit/servers/",
    "plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/",
    "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/",
    "plugins/haipipe-toolkit/skills/1_base/excalidraw/",
    "install.ps1", ".gitignore",
]

CODE_SUFFIXES = {".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".sh", ".ps1"}
PATH_TOKEN = re.compile(r"(?<![\w.~/@+-])((?:\.{1,2}/|\.?[\w~][\w.~@+-]*/)(?:[\w.~@+-]+/)*[\w.~@+-]*)")
DIRECT_PHRASES = [
    (re.compile(r";?\s*[Dd]irect invocation works[^.\"]*\."), "."),
    (re.compile(r"; can also be invoked directly\."), ", which reads this file as a part (not a separate skill)."),
    (re.compile(r"\s*[Cc]an also be invoked directly\."), ""),
]


class Family:
    def __init__(self, spec):
        self.main = (REPO / spec["main"]).resolve()
        self.name = self.main.name
        self.style = spec.get("style", "command")
        self.helpers = {}
        for rel, part in spec["helpers"].items():
            d = (REPO / rel).resolve()
            self.helpers[d.name] = {"old": d, "part": part, "new": self.main / "_parts" / part,
                                    "words": spec.get("words", {}).get(part, part),
                                    "bare": d.name not in spec.get("no_bare", ())}

    def bare(self, helper):
        h = self.helpers[helper]
        return ("%s %s" % (self.name, h["words"])) if self.style == "command" else ("%s/_parts/%s" % (self.name, h["part"]))

    def slash(self, helper):
        return ("/" + self.bare(helper)) if self.style == "command" else self.bare(helper)


def load_families(args):
    if args.spec:
        specs = SPECS[args.spec]
    else:
        helpers = {}
        for h in args.helper:
            d, _, part = h.partition("=")
            helpers[d] = part or Path(d).name.replace(Path(args.main).name + "-", "")
        words = dict(w.split("=", 1) for w in args.words)
        specs = [{"main": args.main, "style": args.style, "helpers": helpers, "words": words}]
    fams = [Family(s) for s in specs]
    for f in fams:
        if not (f.main / "SKILL.md").exists():
            sys.exit("main skill has no SKILL.md: %s" % f.main)
    return fams


# ─── locations ──────────────────────────────────────────────────────────────

def moved_map(fams):
    """old helper dir -> new part dir (absolute, longest first)."""
    m = {}
    for f in fams:
        for h in f.helpers.values():
            m[str(h["old"])] = str(h["new"])
    return dict(sorted(m.items(), key=lambda kv: -len(kv[0])))


def new_location(path, moves):
    """Where an old absolute path lives after the moves (SKILL.md of a helper -> PART.md)."""
    p = str(path)
    for old, new in moves.items():
        if p == old:
            return new
        if p.startswith(old + "/"):
            rest = p[len(old) + 1:]
            if rest == "SKILL.md":
                rest = "PART.md"
            return new + "/" + rest
    return p


def owner_dir(path, marker=("SKILL.md",)):
    d = Path(path).parent
    while str(d).startswith(str(REPO)) and d != REPO:
        if any((d / m).exists() for m in marker):
            return d
        d = d.parent
    return None


def is_protected(rel):
    return any(rel == p.rstrip("/") or rel.startswith(p) for p in PROTECT)


def repo_files():
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.splitlines()
    for rel in out:
        if any(rel.startswith(s) for s in SKIP):
            continue
        p = REPO / rel
        if p.suffix in TEXT_SUFFIXES and p.is_file() and not p.is_symlink():
            yield rel


# ─── rewriting ──────────────────────────────────────────────────────────────

class Rewriter:
    def __init__(self, fams):
        self.fams = fams
        self.moves = moved_map(fams)
        self.helper_fam = {h: f for f in fams for h in f.helpers}
        names = sorted(self.helper_fam, key=len, reverse=True)
        alt = "|".join(re.escape(n) for n in names)
        self.skill_call = re.compile(r'Skill\(\s*"(%s)"\s*(?:,\s*(?:args\s*=\s*)?"([^"]*)")?\s*\)' % alt)
        self.companions = re.compile(r"(companions:\s*\[)([^\]]*)(\])", re.S)
        self.slash = re.compile(r"(?<![\w.~/-])/(%s)(?![\w-])" % alt)
        self.bare = re.compile(r"(?<![\w/-])(%s)(?![\w-])" % alt)

    def resolve(self, token, bases):
        """First base where token resolves to an existing path in the old tree."""
        clean = token.rstrip("/")
        for base in bases:
            if base is None:
                continue
            p = os.path.normpath(os.path.join(str(base), clean))
            if os.path.exists(p):
                return base, p
        return None, None

    def rewrite_path(self, token, old_file, new_file):
        if token.endswith(".") and not token.endswith(".."):  # a sentence's full stop
            return self.rewrite_path(token[:-1], old_file, new_file) + "."
        segs = token.rstrip("/").split("/")
        names_in = [s for s in segs if s in self.helper_fam]
        old_dir = Path(old_file).parent
        new_dir = Path(new_file).parent
        moved = str(old_file) != str(new_file)
        if not names_in and not (moved and token.startswith(("../", "./"))):
            return token
        old_owner = owner_dir(old_file)
        bases = [old_dir, old_owner, REPO]
        base, target = self.resolve(token, bases)
        trail = "/" if token.endswith("/") else ""
        if target is not None:
            new_target = new_location(target, self.moves)
            if base == old_dir:
                new_base = new_dir
            elif base == old_owner:
                new_base = Path(new_location(old_owner, self.moves))
            else:
                new_base = REPO
            if new_target == target and str(new_base) == str(base):
                return token
            rel = os.path.relpath(new_target, str(new_base))
            if token.startswith("./") and not rel.startswith("."):
                rel = "./" + rel
            return rel + trail
        if not names_in or getattr(self, "_code", False):
            return token
        if not all(self.helper_fam[n].helpers[n]["bare"] for n in names_in):
            return token  # a generic name (blader/humanizer is a repository, not our folder)
        # textual fallback: a partial path (1_data/haipipe-data-source/SKILL.md, a tree label)
        out = []
        i = 0
        while i < len(segs):
            s = segs[i]
            if s in self.helper_fam:
                f = self.helper_fam[s]
                h = f.helpers[s]
                if out and out[-1] == h["old"].parent.name:
                    out.append(os.path.relpath(str(h["new"]), str(h["old"].parent)))
                else:
                    out.append("%s/_parts/%s" % (f.name, h["part"]))
                if i + 1 < len(segs) and segs[i + 1] == "SKILL.md":
                    out.append("PART.md")
                    i += 1
            else:
                out.append(s)
            i += 1
        return "/".join(out) + trail

    def rewrite(self, text, old_file, new_file, self_name):
        """Rewrite one file. Code and data files (CODE_SUFFIXES) get only paths that resolve
        on disk: a name there may be an identifier (an owner: field, a folder built in code)."""
        code = Path(new_file).suffix in CODE_SUFFIXES
        self._code = code
        hold = []

        def stash(s):
            hold.append(s)
            return "\x00%d\x00" % (len(hold) - 1)

        # 1. paths (stashed so later steps leave them alone)
        def path_sub(m):
            tok = m.group(1)
            new = self.rewrite_path(tok, old_file, new_file)
            return stash(new) if new != tok or any(s in self.helper_fam for s in tok.split("/")) else tok
        text = PATH_TOKEN.sub(path_sub, text)

        if code:
            return re.sub(r"\x00(\d+)\x00", lambda m: hold[int(m.group(1))], text)

        # 2. Skill("helper", args="...")
        def call_sub(m):
            f = self.helper_fam[m.group(1)]
            h = f.helpers[m.group(1)]
            if f.style == "path":
                return "Read `%s/_parts/%s/PART.md`" % (f.name, h["part"])
            args = (h["words"] + " " + (m.group(2) or "")).strip()
            return stash('Skill("%s", args="%s")' % (f.name, args))
        text = self.skill_call.sub(call_sub, text)

        # 3. companions lists
        def comp_sub(m):
            items = [i.strip() for i in m.group(2).replace("\n", " ").split(",") if i.strip()]
            if not any(i in self.helper_fam for i in items):
                return m.group(0)
            out = []
            for i in items:
                i = self.helper_fam[i].name if i in self.helper_fam else i
                if i != self_name and i not in out:
                    out.append(i)
            body = ", ".join(out)
            if len(m.group(1)) + len(body) > 100 and "\n" in m.group(2):
                lines, cur = [], ""
                for i in out:
                    nxt = (cur + ", " + i) if cur else i
                    if len(nxt) > 80 and cur:
                        lines.append(cur + ",")
                        cur = i
                    else:
                        cur = nxt
                lines.append(cur)
                body = "\n  ".join(lines)
            return stash(m.group(1) + body + m.group(3))
        text = self.companions.sub(comp_sub, text)

        # 4. /helper commands, 5. bare names
        text = self.slash.sub(lambda m: stash(self.helper_fam[m.group(1)].slash(m.group(1))), text)
        text = self.bare.sub(lambda m: stash(self.helper_fam[m.group(1)].bare(m.group(1)))
                             if self.helper_fam[m.group(1)].helpers[m.group(1)]["bare"] else m.group(0), text)

        # 6. brace and placeholder forms: ../<main>-{a,b}/x, /<main>-<stage>, <main>-{a,b}
        for f in self.fams:
            if f.style != "command":
                continue
            var = r"(\{[^}\s]*\}|<[\w-]+>)"
            def brace_path(m, f=f):
                base = os.path.normpath(os.path.join(str(Path(old_file).parent), m.group(1) or "."))
                if base != str(f.main.parent):
                    return m.group(0)
                rel = os.path.relpath(str(f.main / "_parts"), str(Path(new_file).parent))
                return "%s/%s/" % (rel, m.group(2))
            text = re.sub(r"(?<![\w/.-])((?:\.\.?/)+)%s-%s/" % (re.escape(f.name), var), brace_path, text)
            text = re.sub(r"(?<![\w.~/-])/%s-%s" % (re.escape(f.name), var),
                          lambda m, f=f: "/%s %s" % (f.name, m.group(1)), text)
            text = re.sub(r"(?<![\w/(\"-])%s-(\{[^}\s]*\})" % re.escape(f.name),
                          lambda m, f=f: "%s %s" % (f.name, m.group(1)), text)
            # a shared part prefix with a wildcard: /<main>-deploy-* , <main>-deploy-{local,mlflow}
            prefixes = sorted({h["part"].split("-")[0] for h in f.helpers.values() if "-" in h["part"]})
            if prefixes:
                text = re.sub(r"(?<![\w-])(/?)%s-(%s)-(\{[^}\s]*\}|\*|<[\w-]+>)"
                              % (re.escape(f.name), "|".join(map(re.escape, prefixes))),
                              lambda m, f=f: "%s%s %s %s" % (m.group(1), f.name, m.group(2),
                                                             "<target>" if m.group(3) == "*" else m.group(3)), text)

        # 7. short forms (-deploy-local) inside a family's own folder
        fam = next((f for f in self.fams if str(new_file).startswith(str(f.main.parent) + "/")), None)
        if fam is not None and fam.style == "command":
            parts = {h["part"]: hn for hn, h in fam.helpers.items()}
            rx = re.compile(r"(?<![\w/.\-])-(%s)(?![\w-])" % "|".join(sorted(map(re.escape, parts), key=len, reverse=True)))
            text = "\n".join(line if "haistep" in line else rx.sub(lambda m: fam.bare(parts[m.group(1)]), line)
                             for line in text.split("\n"))
        return re.sub(r"\x00(\d+)\x00", lambda m: hold[int(m.group(1))], text)


# ─── front matter ───────────────────────────────────────────────────────────

FM = re.compile(r"\A---\n(.*?)\n---[ \t]*\n", re.S)


def tools_of(text):
    m = FM.match(text)
    if not m:
        return []
    t = re.search(r"(?m)^allowed-tools:\s*(.+)$", m.group(1))
    return [x.strip() for x in t.group(1).split(",") if x.strip()] if t else []


def part_front_matter(text, fam, helper):
    """SKILL.md front matter -> PART.md front matter."""
    m = FM.match(text)
    if not m:
        return text
    fm = m.group(1)
    h = fam.helpers[helper]
    fm = re.sub(r"(?m)^name:\s*.*$", "name: %s\npart-of: %s" % (h["part"], fam.name), fm, count=1)
    fm = re.sub(r"(?m)^allowed-tools:.*\n?", "", fm)
    for rx, rep in DIRECT_PHRASES:
        fm = rx.sub(rep, fm)
    body = text[m.end():]
    for rx, rep in DIRECT_PHRASES:
        body = rx.sub(rep, body)
    return "---\n" + fm + "\n---\n" + body


def merge_tools(text, extra):
    m = FM.match(text)
    if not m or not extra:
        return text
    fm = m.group(1)
    have = tools_of(text)
    union = have + [t for t in extra if t not in have]
    if union == have:
        return text
    if re.search(r"(?m)^allowed-tools:", fm):
        fm = re.sub(r"(?m)^allowed-tools:.*$", "allowed-tools: " + ", ".join(union), fm, count=1)
    else:
        fm += "\nallowed-tools: " + ", ".join(union)
    return "---\n" + fm + "\n---\n" + text[m.end():]


def bump(text, minor):
    m = FM.match(text)
    if not m:
        return text, None
    fm = m.group(1)
    v = re.search(r'(?m)^(\s*version:\s*)"?(\d+)\.(\d+)\.(\d+)"?', fm)
    new = None
    if not v:  # an unversioned skill starts at 0.1.0
        if re.search(r"(?m)^metadata:\s*$", fm):
            fm = re.sub(r"(?m)^metadata:\s*$", 'metadata:\n  version: "0.0.0"', fm, count=1)
        else:
            fm += '\nmetadata:\n  version: "0.0.0"\n  last_updated: ""'
        v = re.search(r'(?m)^(\s*version:\s*)"?(\d+)\.(\d+)\.(\d+)"?', fm)
        minor = True
    if v:
        a, b, c = int(v.group(2)), int(v.group(3)), int(v.group(4))
        new = "%d.%d.0" % (a, b + 1) if minor else "%d.%d.%d" % (a, b, c + 1)
        fm = fm[:v.start()] + '%s"%s"' % (v.group(1), new) + fm[v.end():]
        fm = re.sub(r'(?m)^(\s*last_updated:\s*).*$', lambda x: '%s"%s"' % (x.group(1), TODAY), fm, count=1)
    return "---\n" + fm + "\n---\n" + text[m.end():], new


def add_changelog(folder, title, version, note, marker):
    cl = Path(folder) / "CHANGELOG.md"
    entry = "## [%s] — %s\n\n%s (%s)\n\n" % (version or "unversioned", TODAY, note, marker)
    if cl.exists():
        text = cl.read_text(encoding="utf-8")
        if marker in text:
            return False
        i = text.find("\n## ")
        text = (text + "\n\n" + entry) if i < 0 else (text[:i + 1] + entry + text[i + 1:])
    else:
        text = ("%s — Changelog\n%s\n\nSkill-scoped changelog (never loaded at invocation; read on demand).\n"
                "Versions match the front matter `version:`.\nNewest first.\n\n\n%s" % (title, "=" * (len(title) + 12), entry))
    cl.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
    return True


# ─── main ───────────────────────────────────────────────────────────────────

def git(*a):
    subprocess.run(["git"] + list(a), cwd=REPO, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", choices=sorted(SPECS), help="a named merge from SPECS")
    ap.add_argument("--main", help="main skill folder (repo-relative)")
    ap.add_argument("--helper", action="append", default=[], help="<dir>[=<part>]")
    ap.add_argument("--style", choices=["command", "path"], default="command")
    ap.add_argument("--words", action="append", default=[], help='<part>="<command words>"')
    ap.add_argument("--marker", default="merge-parts " + dt.date.today().strftime("%y%m%d"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.spec and not (args.main and args.helper):
        ap.error("give --spec, or --main with --helper")
    fams = load_families(args)
    rw = Rewriter(fams)
    moves = rw.moves

    missing = [h["old"] for f in fams for h in f.helpers.values() if not (h["old"] / "SKILL.md").exists()]
    if missing:
        sys.exit("already merged or missing: %s" % ", ".join(map(str, missing)))

    # 1. compute every rewrite against the old tree
    planned, protected_hits = {}, []
    names_rx = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(n) for n in rw.helper_fam))
    for rel in repo_files():
        old = REPO / rel
        text = old.read_text(encoding="utf-8", errors="surrogateescape")
        if is_protected(rel):
            for n, line in enumerate(text.splitlines(), 1):
                if names_rx.search(line):
                    protected_hits.append("%s:%d" % (rel, n))
            continue
        new = Path(new_location(old, moves))
        # the new owner does not exist yet for moved files; a part's skill is its main
        self_name = next((f.name for f in fams if str(new).startswith(str(f.main) + "/")), None)
        self_name = self_name or (owner_dir(old).name if owner_dir(old) else None)
        out = text
        for f in fams:
            for hname, h in f.helpers.items():
                if old == h["old"] / "SKILL.md":
                    out = part_front_matter(out, f, hname)
        out = rw.rewrite(out, old, new, self_name)
        if out != text or str(old) != str(new):
            planned[str(old)] = (str(new), out, out != text)

    changed = sorted(os.path.relpath(o, REPO) for o, (_, _, c) in planned.items() if c)
    print("families: %d, helpers: %d, files rewritten: %d" % (len(fams), len(rw.helper_fam), len(changed)))
    for f in fams:
        print("  %s <- %s" % (f.name, ", ".join(h["part"] for h in f.helpers.values())))
    if args.dry_run:
        for c in changed:
            print("  ~ " + c)
        report_leftovers(fams, protected_hits,
                         {os.path.relpath(n, REPO): t for _, (n, t, _) in planned.items()})
        return

    # 2. move with git, then write the rewritten text at the new places
    tools_extra = {f.name: [] for f in fams}
    for f in fams:
        (f.main / "_parts").mkdir(exist_ok=True)
        for hname, h in f.helpers.items():
            tools_extra[f.name] += [t for t in tools_of((h["old"] / "SKILL.md").read_text(encoding="utf-8"))
                                    if t not in tools_extra[f.name]]
            git("mv", str(h["old"]), str(h["new"]))
            git("mv", str(h["new"] / "SKILL.md"), str(h["new"] / "PART.md"))
    for old, (new, out, _) in planned.items():
        Path(new).write_text(out, encoding="utf-8", errors="surrogateescape")

    # 3. main skills: allowed-tools union
    for f in fams:
        p = f.main / "SKILL.md"
        p.write_text(merge_tools(p.read_text(encoding="utf-8"), tools_extra[f.name]), encoding="utf-8")

    # 4. one CHANGELOG entry and one bump per affected skill or part
    owners = {}
    for old, (new, _, c) in planned.items():
        if not c or Path(new).name == "CHANGELOG.md":
            continue
        d = owner_dir(new, ("SKILL.md", "PART.md"))
        if d:
            owners[str(d)] = d
    for f in fams:
        owners[str(f.main)] = f.main
        for h in f.helpers.values():
            owners[str(h["new"])] = h["new"]
    mains = {str(f.main): f for f in fams}
    parts = {str(h["new"]): (f, hn, h) for f in fams for hn, h in f.helpers.items()}
    for key, d in sorted(owners.items()):
        md = d / ("PART.md" if (d / "PART.md").exists() else "SKILL.md")
        text = md.read_text(encoding="utf-8")
        cl = d / "CHANGELOG.md"
        if cl.exists() and args.marker in cl.read_text(encoding="utf-8"):
            continue
        text, version = bump(text, minor=key in mains)
        md.write_text(text, encoding="utf-8")
        if key in mains:
            f = mains[key]
            note = ("Merged %d helper skill(s) into `_parts/`: %s. /%s reads `_parts/<name>/PART.md` instead of "
                    "calling a separate skill; allowed-tools gained the parts' tools. Old commands map as "
                    "`/%s` -> `%s`."
                    % (len(f.helpers), ", ".join("`%s` -> `_parts/%s`" % (n, h["part"]) for n, h in f.helpers.items()),
                       f.name, next(iter(f.helpers)), f.slash(next(iter(f.helpers)))))
        elif key in parts:
            f, hn, h = parts[key]
            note = ("Became a part of `%s`: `%s/_parts/%s/PART.md` (was the skill `%s`); front matter, "
                    "commands and links updated." % (f.name, f.name, h["part"], hn))
        else:
            note = ("Links, commands and companions repointed at the helper skills merged into %s "
                    "(now `_parts/<name>/PART.md`)." % ", ".join("`%s`" % f.name for f in fams))
        title = d.name if key not in parts else "%s %s" % (parts[key][0].name, parts[key][2]["part"])
        add_changelog(d, title, version, note, args.marker)
        print("  bumped %-60s %s" % (os.path.relpath(d, REPO), version))
    report_leftovers(fams, protected_hits, marker=args.marker)


def report_leftovers(fams, protected_hits, texts=None, marker=None):
    """Print what still names a helper, a brace or placeholder form, or a short form.

    texts: rel path -> planned text (dry run); otherwise files are read from disk."""
    pats = []
    for f in fams:
        pats.append(r"%s-([a-z0-9]+-)?[{<\[*]" % re.escape(f.name))
        pats.append(r'Skill\(\s*"%s ' % re.escape(f.name))  # a multi-line Skill() the rewrite split
        pats += [r"(?<![\w-])%s(?![\w-])" % re.escape(n) for n in f.helpers]
    rx = re.compile("|".join(pats))
    short = re.compile(r"(?<![\w/.-])-(%s)\b" % "|".join(sorted({re.escape(h["part"]) for f in fams
                                                                  for h in f.helpers.values()}, key=len, reverse=True)))
    hits, shorts = [], []
    fam_dirs = tuple(str(f.main.parent) for f in fams)
    texts = dict(texts or {})
    for rel in repo_files():
        if is_protected(rel) or rel in texts:
            continue
        if texts and os.path.relpath(new_location(REPO / rel, moved_map(fams)), REPO) in texts:
            continue
        texts[rel] = (REPO / rel).read_text(encoding="utf-8", errors="ignore")
    for rel, text in sorted(texts.items()):
        for n, line in enumerate(text.splitlines(), 1):
            if marker and marker in line:
                continue  # the CHANGELOG entry that records the rename
            if rx.search(line):
                hits.append("%s:%d: %s" % (rel, n, line.strip()[:140]))
            if str(REPO / rel).startswith(fam_dirs) and short.search(line):
                shorts.append("%s:%d: %s" % (rel, n, line.strip()[:140]))
    print("\nleft for a person (helper names, brace or placeholder forms): %d" % len(hits))
    for h in hits:
        print("  " + h)
    print("\nshort forms (-<part>) in the families' folders, check each: %d" % len(shorts))
    for h in shorts:
        print("  " + h)
    print("\nprotected paths that name a helper (tell their owner): %d" % len(protected_hits))
    for h in protected_hits[:200]:
        print("  " + h)


if __name__ == "__main__":
    main()
