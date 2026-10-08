"""b16 s21 · Run and skill: s21-paper-run-skill.excalidraw, the paper theme's skills and its Runs in one drawing.

Read from disk every build: the skills in skills/2_theme/paper (version, size, who outside calls them),
the base skills a paper borrows (found by name), the run cards of haipipe-paper-workflow/ref/run-cards.md
(button, name pattern, skill, agent, signs), and the Runs that exist in the Project paper folders, counted
by run type (names only, never their content; no Board or Section names are drawn). Two parts are typed,
since they are the proposal: each skill's job and level, and each run type's level (Block · Job · Task,
from Q01). Open points are red.

Draws with b04's studio helpers (as b17's s02-work-skills does) through b03's canvas.write, so a
person's marks survive a rebuild. What changed is written in green beside it, dated (CHANGES; JL 261007: "add the
short green comments to where we made the changes").

    python build_s21_paper_run_skill.py [out.excalidraw]
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(BLOCK.parent / "b04_skill_folder" / "studio" / "_build"))
from sketch import (GRAY, GREEN, RED, SKILLS, SPACE, TK, TOOLS, close_frame, concern, legend, mono,  # noqa: E402
                    open_frame, questions_frame, save, sticky, text)

PAPER = SKILLS / "2_theme" / "paper"
CARDS = PAPER / "haipipe-paper-workflow" / "ref" / "run-cards.md"

# ── the typed part: each paper skill's job and the level it serves (proposal, Q01) ─────────────
JOB = {"haipipe-paper": ("the door: routes a request to its owner", "all"),
       "haipipe-paper-workflow": ("Run Specs, routes, gates G0-G5", "all"),
       "workbench-paper": ("the Paper workbench (screens, run cards)", "all"),
       "haipipe-paper-ideation": ("run type: studio/s01-ideation/ (no Page)", "Block"),
       "haipipe-paper-story": ("run type: studio/sNN-story-…, Questions", "Block"),
       "haipipe-paper-venue": ("Venue Page: one journal or funder", "Block · Description › Venue ?"),
       "haipipe-paper-assemble": ("build the whole paper into delivery/", "Job · version Delivery ? (Q02)"),
       "haipipe-paper-comments": ("comments → Review Items (reviews, meetings)", "Job · reports/ (type)"),
       "haipipe-paper-section": ("Section Page: one Section", "Task")}
# the base skills a paper borrows, by what they do for it
BORROWS = [("Page workflow (every Story and Section Page)",
            ["haipipe-page-workflow", "haipipe-page-context", "haipipe-page-structure", "haipipe-page-evidence",
             "haipipe-page-writing", "haipipe-page-scratch", "haipipe-page-revise", "haipipe-page-delivery",
             "haipipe-page-check"]),
           ("Ideation (the idea pool)", ["haipipe-ideation", "haipipe-ideation-generate", "haipipe-ideation-test",
                                         "haipipe-ideation-select"]),
           ("supporting work (other themes' hard Runs)", ["haipipe-task", "haipipe-discovery"]),
           ("shared", ["haipipe-question", "haipipe-run", "haipipe-display", "excalidraw-section", "table-papers"])]
# each run card's level (proposal, Q01): Block = the Board and its Story Pages; Job = a version; Task = a Section
LEVEL = {"Generate ideas": "Block", "Test idea": "Block", "Select idea": "Block", "Idea review": "Block",
         "Story revise": "Block", "Claim review": "Block", "Write the report": "Block",
         "Review the report": "Block", "Task review": "Block", "Task runs": "Block", "Discovery runs": "Block",
         "Redraw": "Block", "Narrative review": "Job", "Build": "Job", "Check": "Job", "Cover letter": "Job",
         "Response": "Job", "Draft runs": "Task", "Evidence runs": "Task", "Delivery runs": "Task",
         "Page check": "Task"}
# the run types Q01 proposes that no card has yet
NEW = [("Block", "Add a venue", "run-venue-<venue>", "haipipe-paper-venue"),
       ("Block", "Ask a Question", "run-question-<qNN>", "haipipe-question"),
       ("Block", "Open a version", "run-version-<jNN>", "haipipe-paper"),
       ("Job", "Check the submission", "run-check-submit", "haipipe-paper-assemble")]
# which Runs on disk each card counts (a stem pattern, and the shelf it sits on)
COUNTS = {"Idea review": (r"^run-paper-idea-", "story"), "Claim review": (r"^run-paper-claim-", "story"),
          "Task review": (r"^run-paper-task-", "story"), "Narrative review": (r"^run-paper-narrative-", "story"),
          "Story revise": (r"^run-(structure|scratch|section|paragraph|revise|auto-write|evidence-embed|context)-", "story"),
          "Draft runs": (r"^run-(structure|scratch|section|paragraph|revise|auto-write|context)-", "section"),
          "Evidence runs": (r"^run-(value|citation|display|evidence-embed)-", "section"),
          "Delivery runs": (r"^run-delivery-", "section"), "Page check": (r"^run-check-", "section"),
          "Build": (r"^r\d+_compile", "delivery"), "Response": (r"^rresponse-", "round")}

CHANGES = {"skills": ["haipipe-paper-round renamed haipipe-paper-comments 1.0.0: reviews, meetings, coauthors → Review Items",
                      "its draft (was s22) sits here: haipipe-paper-comments-draft.md",
                      "Ideation and Story Pages: Block, not a j00_story Job",
                      "Ideation and Story are run types now, no Pages: studio topics + Board Questions + reports (Q04)"],
           "runs": ["Response: Job, a Page Task t32_response in the next version (was ? Q03)",
                    "a comments batch is not a Task; counted as round",
                    "a batch is a report of type comments: reports/qNN_<kind>-<MMDD>/ (haipipe-paper-comments 1.1.0)",
                    "Sections t0N_ · t2N_ in j0N_v<MMDD>_<desk>/ are counted as section (was B[ab]- only)",
                    "Run names drop <MMDD>: run-<type>-<slug>, its passes inside the one file"]}


def changed(x, y, notes, date="261007"):
    """Brief green notes of what changed, dated; returns the bottom."""
    for k, n in enumerate(notes):                       # a note starting "?" was reopened: red
        text(x, y + k * 26, n if n.startswith("?") else f"✎ {date}  {n}", 17, RED if n.startswith("?") else GREEN)
    return y + len(notes) * 26


# ── facts, read from disk ──────────────────────────────────────────────────────────────────────
def callers(name):
    """Files in the toolkit outside 2_theme/paper that name a skill (the venue bank is not read)."""
    out = subprocess.run(["grep", "-rlIw", "--exclude-dir=.git", "--exclude-dir=_legacy", "--exclude-dir=venue",
                          "--exclude=CHANGELOG.md", name, str(TK)], capture_output=True, text=True).stdout.split()
    return [o for o in out if not o.startswith(str(PAPER))]


def skill_rows():
    rows = []
    for d in sorted(p for p in PAPER.iterdir() if (p / "SKILL.md").is_file()):
        s = (d / "SKILL.md").read_text(encoding="utf-8")
        v = re.search(r'version: "?([\d.]+)', s)
        job, level = JOB.get(d.name, ("? not in the proposal", "?"))
        line = (f"{d.name:<24}{'v' + (v.group(1) if v else '?'):<9}{len(s.splitlines()):>4} lines"
                f"{len(callers(d.name)):>4} callers  {job:<44}{level}")
        rows.append(("!" if "?" in level else "") + line)
    return rows


def find_skill(name):
    return next((p for p in SKILLS.rglob(name) if (p / "SKILL.md").is_file()), None)


def borrow_rows():
    rows = []
    for group, names in BORROWS:
        rows.append(group)
        for n in names:
            p = find_skill(n)
            rows.append(f"  {n:<28}{p.parent.relative_to(SKILLS).as_posix() + '/' if p else '! not found'}")
    return rows


def not_skills():
    """What sits in 2_theme/paper but is no skill: its files and size on disk, and whether it is its own repo."""
    rows = []
    for d in sorted(p for p in PAPER.iterdir() if p.is_dir() and not (p / "SKILL.md").exists()
                    and not p.name.startswith((".", "_"))):
        files = [f for f in d.rglob("*") if f.is_file() and ".git" not in f.relative_to(d).parts]
        mb = sum(f.stat().st_size for f in files) / 2**20
        kind = "its own git repo" if (d / ".git").exists() else "in Tools"
        rows.append(("!" if mb > 10 else "") + f"{d.name + '/':<10}{len(files):>6} files {mb:>7.0f} MB  {kind}")
    return rows


def cards():
    """The run cards: (section head, button, Space, pattern, skill, agent, signs)."""
    out, head, cur = [], "", {}
    for line in CARDS.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            head = line[3:]
        elif line.startswith("🔘 BUTTON"):
            label, space, pattern = (line.split(None, 2)[2].split(" · ") + ["", "", ""])[:3]
            cur = {"head": head, "button": label.strip(), "space": space.strip(), "pattern": pattern.strip()}
        elif cur and line.startswith(("🧩 SKILL", "🤖 AGENT", "✍️ SIGNS")):
            cur[line.split()[1].lower()] = line.split(None, 2)[2].strip()
            if "signs" in cur:
                out.append(cur)
                cur = {}
    return out


def agent_exists(name):
    return any(TK.rglob(name.split()[0] + ".md"))


def paper_runs():
    """Every Run stem in a Project paper folder, with its shelf (story · section · round · delivery)."""
    seen = set()
    for paper in SPACE.glob("examples-*/*/paper*/Paper-*"):
        for d in paper.rglob("*"):
            if d.name not in ("runs", "results") or not d.is_dir() or {"_old", "_legacy"} & set(d.parts):
                continue
            rel = d.relative_to(paper).parts
            ver = re.match(r"j\d{2}_v", rel[0]) and len(rel) > 1      # the new layout: j0N_v<MMDD>_<desk>/…
            shelf = ("story" if rel[0].startswith(("A1-Story", "studio", "j00_story")) else
                     "section" if re.match(r"B[ab]-", rel[0]) or ver and re.match(r"(t[0-2]\d_|S-)", rel[1]) else
                     "round" if rel[0].startswith("Bc-") or ver and re.match(r"(comments|t3\d_|RD|CM)", rel[1]) else
                     "delivery" if "delivery" in rel[:2] else "other")
            for r in d.iterdir():
                stem = re.sub(r"\.(md|sh|yaml)$", "", r.name)
                if re.match(r"^(run-|r\d|rresponse)", stem):
                    seen.add((paper.name, rel[:-1], stem, shelf))
    return [(stem, shelf) for _, _, stem, shelf in seen], len(list(SPACE.glob("examples-*/*/paper*/Paper-*")))


def run_type(stem):
    for pat, name in [(r"^run-paper-([a-z]+)-", "run-paper-{}"), (r"^run-delivery-([a-z]+)", "run-delivery-{}"),
                      (r"^run-([a-z]+(?:-[a-z]+)?)-\d{4}", "run-{}"), (r"^run-([a-z-]+)$", "run-{}")]:
        m = re.match(pat, stem)
        if m:
            return name.format(m.group(1))
    return "rNN_ (hard)" if re.match(r"^r\d", stem) else stem


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
def draw():
    runs, n_papers = paper_runs()
    by_type = Counter((run_type(s), shelf) for s, shelf in runs)
    text(0, -170, "b16 s21 · the paper theme's skills and Runs", 44)
    legend(1300, -170)
    text(0, -105, "Read from disk: skills/2_theme/paper, the base skills it borrows, its run cards, and the Runs in "
                  "the Project paper folders. Each skill's job and level, and each run type's level, are the "
                  "proposal (Q01); red = open.", 20, GRAY)

    # 1 · skills
    fr = open_frame("1 · skills")
    r1, b1 = mono(0, 0, skill_rows(), "skills/2_theme/paper/ today: name · version · size · callers · job · "
                                      "level (proposed)", size=15)
    r2, b2 = mono(r1 + 80, 0, borrow_rows(), "the base skills a paper borrows (found by name)", size=15)
    r3, b3 = mono(0, b1 + 60, not_skills(), "in 2_theme/paper, but no skill", size=15)
    y = max(b2, b3) + 50
    sticky(0, y, 560, "A paper owns its Pages (Ideation, Story,\nVenue, Section, Round), their workflow and\n"
                      "its build. Everything else is borrowed.", "idea")
    sticky(600, y, 560, "A Section is a Page: its writing, evidence\nand delivery Runs are the Page workflow's,\n"
                        "named by haipipe-paper-section.", "idea")
    cy = y + 150
    for c in ["? venue/ (venue playbooks and journal PDFs) is its own git repo inside the skills tree the installer scans;",
              "  .gitmodules names it, but Tools does not register it. Mount it outside skills/, and register it?",
              "? haipipe-paper-venue is a Page Type for one journal; b03 proposes venues/<venue>/ (call.md, kit/)",
              "  as the Board's Description › Venue. One home for a venue (Q02)?",
              "? A user-level install, outside this SPACE, still links an older paper-edit family",
              "  (paper-edit, haipipe-paper-edit-*, haipipe-paper-minimap): retire it, or bring it into 2_theme/paper?"]:
        cy = concern(0, cy, c) + 6
    cy = changed(0, cy + 20, CHANGES["skills"])
    close_frame(fr)

    # 2 · run types, by the level they serve
    y0 = cy + 260
    fr = open_frame("2 · run types by level")
    text(0, y0, "run types: what a paper can run, by the level it serves (from run-cards.md)", 30)
    text(0, y0 + 46, "button · today's Space · Run name · skill · agent · what a person signs · Runs in the paper "
                     "folders today", 18, GRAY)
    all_cards, ty = cards(), y0 + 110
    for level in ("Block", "Job", "Task"):
        rows = []
        for c in [c for c in all_cards if LEVEL.get(c["button"], "?").startswith(level)] + \
                 [c for c in all_cards if level == "Job" and c["button"] not in LEVEL]:
            name = re.search(r"`(run-[^`]+|paper\.[a-z.]+)`", c["head"])
            pattern = c["pattern"].lstrip("^").rstrip("-") if c["pattern"] not in ("-", "") else \
                (name.group(1) if name else "-")
            pat = COUNTS.get(c["button"])
            n = sum(1 for s, shelf in runs if pat and shelf == pat[1] and re.match(pat[0], s)) if pat else None
            agent = c.get("agent", "?")
            agent += "" if "(new)" in agent or agent_exists(agent) else " (no file)"
            red = "?" in LEVEL.get(c["button"], "?") or "(new)" in agent or "(no file)" in agent
            rows.append(("!" if red else "") + f"{c['button']:<28}{c['space']:<10}{pattern[:44]:<46}"
                        f"{c.get('skill', '?'):<27}{agent[:38]:<40}{c.get('signs', '?')[:30]:<32}"
                        f"{'-' if n is None else n:>4}")
        for lv, button, pattern, skill in NEW:
            if lv == level:
                rows.append(f"!{button + ' (new)':<28}{'-':<10}{pattern:<46}{skill:<27}{'?':<40}{'?':<32}{'-':>4}")
        _, ty = mono(0, ty, rows, {"Block": "Block: the paper Board and its Story Pages",
                                   "Job": "Job: one version for one venue",
                                   "Task": "Task: one Section (a Page Task)"}[level], size=15)
        ty += 50

    # 3 · the Runs that exist, and their names
    used = [f"{t:<24}{shelf:<10}{k:>4}" for (t, shelf), k in sorted(by_type.items(), key=lambda x: -x[1])]
    used = [("!" + u) if u.startswith("rNN_") else u for u in used]
    for t in ("run-paper-idea", "run-paper-claim", "run-paper-task", "run-paper-narrative"):
        if not any(k[0] == t for k in by_type):
            used.append(f"!{t:<24}{'story':<10}{0:>4}")
    r4, b4 = mono(0, ty + 40, used, f"Runs in the {n_papers} Project paper folders today: run type · shelf · count",
                  size=15)
    names = ["Page writing    run-<kind>-<MMDD>-<slug>        structure scratch section paragraph revise ...",
             "Page evidence   run-<value|citation|display>-<MMDD>-<slug>",
             "Page delivery   run-delivery-<lane>             one fixed Run per lane, no receipt",
             "Paper judgment  run-paper-<idea|claim|task|narrative>-<MMDD>-<slug>",
             "compile         delivery/runs/rNN_compile-<slug>.sh   a hard ticket in the paper",
             "response        <Round>/runs/rresponse-NN_<batch>.md",
             "supporting      rNN_<slug> in a work or discovery Task, never renamed for the paper"]
    r5, b5 = mono(r4 + 80, ty + 40, names, "Run names today (haipipe-paper/ref/run-naming.md)", size=15)
    cy = max(b4, b5) + 40
    for c in ["? Hard rNN_ Runs sit on Story Pages today, and compile is a hard ticket in delivery/runs/:",
              "  Q01 proposes a paper holds soft Runs only. Move them to a work Task, or allow a paper its builds?",
              "? The four judgment run types (run-paper-*) have cards and buttons but no Run on disk yet."]:
        cy = concern(0, cy, c) + 6
    cy = changed(0, cy + 20, CHANGES["runs"])
    close_frame(fr)

    questions_frame(0, cy + 160, [
        ("(proposed) Q04 · Which skills and Runs make the\npaper theme? what it owns, what it borrows, and\n"
         "which run types each level offers",
         [("9 skills own the Pages, the workflow,\nthe build and the workbench", "done"),
          ("each card gets a level: Block · Job · Task\n(Q01's ladder)", "idea"),
          ("your call: venue/ out of skills/;\nhard Runs out of the paper", "open")]),
    ], width=640)


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21-paper-run-skill.excalidraw", "build_s21_paper_run_skill.py")
