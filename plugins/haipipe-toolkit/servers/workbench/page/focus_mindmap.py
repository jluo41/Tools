"""The focus page's MindMap of a page's own parts, and the focus-part documents."""
from __future__ import annotations

import re
from pathlib import Path

from live import frame, task_questions
from live import focus_base
from live.focus_base import (band_title, document, face_parts, first_sentence, inside, job_short, kids, one_line,
    page_level, page_module, part, read_face, report_path)
from live.focus_styles_bands import FIT_MAP, FRAMED_SCROLL, map_html
from live.focus_runs import run_document, run_goal
from live.focus_interactions import interaction_items, standard_interactions
from live.focus_reports import first_answer
from live.focus_tree import PARTS, family_words, task_families, work_root
from live.focus_delivery import delivery_html
from live.focus_themes import draft_branches, is_draft


def part_document(folder: Path, root: Path, key: str) -> str:
    """One of a row's parts alone, for its pop-out: its mind map, its Work (Jobs, Tasks, Runs), or its delivery."""
    from live import project_page as PP
    if key == "interactions" and folder.is_dir() and inside(folder, root):   # the Interaction button's list (JL 261031)
        items = interaction_items(folder, root)
        body = standard_interactions(items, folder, root, in_pop=True) or '<p class="mut">No interactions here.</p>'
        return document(f"{folder.name} · Interaction", '<main class="focus-page"><h1>' + frame.esc(folder.name)
                        + '<span class="h1-section">Interaction</span></h1><section class="focus-card">'
                        + f'<div class="focus-content">{body}</div></section></main>')
    if key == "run" and folder.is_dir() and inside(folder, root) and folder.parent.name == "runs":
        return run_document(folder, root)
    if key in ("find-data", "find-values", "find-display", "find-fn") and folder.is_dir() and inside(folder, root):
        return PP.find_part_document(folder, root, key)
    if not folder.is_dir() or not inside(folder, root) or key not in dict(PARTS):
        return ""
    if key == "map":
        body = parts_mindmap(folder, root) if page_level(folder) in ("Block", "Job", "Task") else PP.mindmap_view(folder, root)
    elif key == "work":
        start = work_root(folder)
        if start is None:
            return ""
        mm_ = frame.mindmap_module()
        import mmbuild
        body = mm_.draw(mmbuild.from_work(start), "", editable=False, base=start,     # a result's chip pops it out
                        url_of=lambda q: frame.reader(q, root) if inside(q, root) else "")
    else:
        body = delivery_html(folder, root) or '<p class="mut">No delivery yet: nothing agreed has been handed over.</p>'
    if key in ("map", "work"):                           # the bare map, as an sNN's Mind map pop-out shows it
        return document(f"{folder.name} · {dict(PARTS)[key]}", body)
    return document(f"{folder.name} · {dict(PARTS)[key]}", '<main class="focus-page"><h1>' + frame.esc(folder.name)
                    + f'<span class="h1-section">{frame.esc(dict(PARTS)[key])}</span></h1><section class="focus-card">'
                    + f'<div class="focus-content">{body}</div></section></main>')


# ── end HOOK ─────────────────────────────────────────────────────────────────────────────────────────────────────


ANSWER_PILL = {"agreed": "✅ answer agreed", "proposed": "🙋 answer: your call", "draft": "🔶 answer not final",
               "": "⬜ no answer yet"}                     # first_answer's stage, said so a reader need not ask


LADDER_NAME = re.compile(r'<span class=(pm-role|pm-id)([^>]*)>([jtsr]\d+)([_-][^<]*)</span>')


def parts_mindmap(folder: Path, root: Path) -> str:
    """A Block's, a Job's or a Task's own mind map (JL 261029: "WE SHOULD HAVE THE MINIMAP AS WELL"): its Questions, each
    with how far its answer has got, its Jobs with their Tasks, its topics. A Job's Tasks and a Task's Runs each show
    what they must find out, never the Run tree with its marks, which Status shows (JL 261106, decided on the lean)."""
    mm_ = frame.mindmap_module()
    import mmbuild, mmtree
    level, branches = page_level(folder), []
    rows, _ = focus_base.owned_register(read_face(folder, root), root, 'Questions', 'questions')
    if rows:
        points = []
        for i, row in enumerate(rows):
            path = report_path(row, folder, root)
            stage, line = first_answer(path, str(row.get("id") or "")) if path else ("", "")
            asked = task_questions.words(row.get("question")) or task_questions.words(row.get("title"))
            # the question itself, and on a Block its ↗ opens the report; the answer's words stay there and on Findings
            # (JL 261103: "what does this mean?" of "To find out" and "draft"; too many words)
            words = f"[{asked}]({frame.reader(path, root)})" if path and level == "Block" else asked
            points.append(mmbuild.built(f"{folder}/q{i}", f"[{ANSWER_PILL.get(stage, ANSWER_PILL[''])}] {words}", [],
                                        [line] if line and level != "Block" else []))
        branches.append(mmbuild.built(f"{folder}/find", "Questions", points))

    # Each sNN hangs on the rung its **At:** names, beside the Jobs, never under a "Studio" node (JL 261029: "each sNN
    # should be just below bNN"); a Block's own topics sit in their groups, its leaves its open questions.
    block = {"Block": folder, "Job": folder.parent, "Task": folder.parent.parent}.get(level, folder)
    shelf = [t for t, _ in frame._studio_topics(block) if t.is_dir() and frame._notes(t) is not None]   # with a face,
    drawn = {}                                                            # as is_topic(); a bare folder took b11 down

    def rung(f):
        return ".".join(p.name.split("_")[0] for p in [f.parent, f][2 - len(f.relative_to(block).parts):]) if f != block else ""

    def topic_nodes(at):
        out = []
        for t in shelf:
            facts = frame._note_facts(frame._notes(t))
            if facts["at"] != at:
                continue
            face = frame._notes(t).read_text(encoding="utf-8", errors="ignore")
            asks = re.findall(r"(?m)^\d+\.\s+(.+)$", part(face_parts(face), "open"))
            # one short line, shown whole: the topic's own question, its title (JL 261030: "make this to be short and
            # fully presented"); its open questions are no leaves here ("should we delete this? no one will read this")
            first = face.splitlines()[0] if face.strip() else ""
            title = first.split(" · ", 1)[1].strip() if " · " in first else ""
            words = re.sub(r"[\[\]]", "", title or first_sentence(facts["topic"]))
            # its box: why, what it delivers, what is still open ("the short paragraphs", JL 261030), as one plain
            # paragraph, the way the draft Task's map shows a sentence (b32 s42; JL 261031)
            plain = lambda s: re.sub(r"\s*\(JL [^)]*\)", "", s).strip().rstrip(".")
            whole = lambda s, n=160: (lambda t: t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…")(" ".join(s.split()))
            gives = re.search(r"(?m)^\*\*For:\*\*\s*(.+)$", face)
            said = ([one_line(plain(first_sentence(facts["topic"])), 160)] if facts["topic"] else []) \
                + ([f"Delivers {one_line(plain(gives.group(1)), 160)}"] if gives else []) \
                + ([f"Still open: {whole(plain(asks[0]))}"] if asks else [])     # a question whole, never cut at its colon
            # each piece one sentence, its own mark kept: "Still open: Is it the right level?" never "level?." (261031)
            said = [s[:1].upper() + s[1:] + ("" if s[-1:] in ".?!" else ".") for s in said if s]
            note = [" ".join(said)] if said else []
            if (t / f"{t.name}.excalidraw").is_file():           # its quick drawing (quick_draw.py), opened from its label
                drawn[t.name] = frame._draw_url(t / f"{t.name}.excalidraw", root, edit=True)
            if at and level == "Block":                          # a Job's drawing in the Block's map: its name only;
                note, words = [], "the Job as one drawing"        # its Job's node already says what it is (JL 261103)
            out.append(((facts["tags"][:1] or [""])[0], mmbuild.built(str(t), f"[{t.name}] {words}", [], note)))
        return out

    def grouped(at):
        """The rung's topics; a Block's in one node per group (studio/_groups.txt order) when it has two or more."""
        nodes = topic_nodes(at)
        names = list(dict.fromkeys(g for g, _ in nodes))
        if at or len(names) < 2:
            return [n for _, n in nodes]
        order = frame.studio_group_order(block)
        names.sort(key=lambda g: (order.index(g) if g in order else len(order), g == ""))
        return [mmbuild.built(f"{block}/group/{g or 'untagged'}", g or 'Untagged',
                              [n for x, n in nodes if x == g]) for g in names]

    def short(f, label_len):
        """A Job's or Task's own title, whole (as a topic's line, JL 261030: "short and fully presented"); else its goal."""
        face = f / f"{f.name}.md"
        first = face.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0] if face.is_file() else ""
        return (first.split(" · ", 1)[1].strip() if " · " in first else one_line(read_face(f, root)["goal"], label_len)) \
            or f.name.split("_", 1)[-1].replace("_", " ")     # its label shows only "j61", so it always has words

    def task_node(t, label_len):
        """A Task: its name, then what it must find out (its goal) as its first leaf, then its topics; a Block's map
        shows names only (261103). A child's note is not drawn, so the goal is a leaf (JL 261106, on the lean)."""
        title, goal = short(t, label_len), one_line(read_face(t, root)["goal"], 200)
        finds = [mmbuild.built(f"{t}/goal", f"[finds out] {goal}")] if goal and goal != title and level != "Block" else []
        return mmbuild.built(str(t), f"[{t.name}] {title}", finds + grouped(rung(t)))
    branches += grouped(rung(folder))
    if level == "Block" and kids(folder):
        def family_nodes(j):                              # same-shaped Tasks as one node each family (JL 261103)
            out = []
            for key, members, values in task_families(kids(j)):
                if key is None:
                    out.append(task_node(members[0], 70))
                else:
                    name, words = family_words(key, members, values)
                    out.append(mmbuild.built(f"{j}/family/{key}", f"{name}: {words}"))
            return out
        # a face's `bands:` groups the Jobs as a Block's topics group, in the same cards, so 15 Jobs read as 5 lines of
        # work (JL 261104: "一眼就能看出来这东西是干啥的"; b35 with 6 cards is the height to match)
        face_text = frame.face(folder).read_text(encoding="utf-8", errors="ignore") if frame.face(folder) else ""
        bands_line = re.search(r"(?m)^bands:\s*(.+)$", face_text)
        named = dict(re.findall(r"\bj(\d)N\s+([^·\n]+)", bands_line.group(1))) if bands_line else {}
        jobs = kids(folder)
        if named and all(re.match(r"j\d\d_", j.name) and j.name[1] in named for j in jobs):
            for b, title in named.items():
                js = [j for j in jobs if j.name[:2] == f"j{b}"]
                if js:
                    branches.append(mmbuild.built(f"{folder}/band/{b}", band_title(title),
                                                  [mmbuild.built(str(j), f"[{j.name}] {job_short(j, js, root)}", grouped(rung(j)) + family_nodes(j)) for j in js]))
        else:
            branches += [mmbuild.built(str(j), f"[{j.name}] {short(j, 80)}", grouped(rung(j)) + family_nodes(j))
                         for j in jobs]
    if level == "Job" and kids(folder):
        for key, members, values in task_families(kids(folder)):
            if key is None:
                branches.append(task_node(members[0], 80))
            else:
                name, words = family_words(key, members, values)
                branches.append(mmbuild.built(f"{folder}/family/{key}", f"{name}: {words}",
                                              [task_node(t, 80) for t in members]))
    if level == "Task" and is_draft(folder):          # HOOK: a Section's map is its paper content, only (JL 261031:
        branches = draft_branches(folder, root)       # "I think the mindmap here should be the paper content")
        drawn = {}
    if level == "Task" and frame.runs_of(folder) and not is_draft(folder):   # each Run and what it must find out
        branches.append(mmbuild.built(f"{folder}/runs", "Runs", [
            mmbuild.built(f"{folder}/{r.name}", f"[{r.name}] {one_line(run_goal(r), 120)}", [])
            for r in sorted(d for d in (folder / "runs").glob("*") if d.is_dir() and not d.name.startswith((".", "_")))]))
    if not branches and level in ("Block", "Job", "Task"):   # a page the shared map cannot read (a cowork Job, no Tasks):
        mod, prefix = page_module(frame.theme_of(folder, root), folder, root)   # its theme's own branches (261108)
        fn = getattr(mod, prefix + "map_branches", None) if mod is not None else None
        try:
            own = list(fn(folder, root, level) or []) if fn else []
        except Exception:
            own = []
        for k, (label, leaves) in enumerate(own):
            branches.append(mmbuild.built(f"{folder}/own/{k}", str(label),
                                          [mmbuild.built(f"{folder}/own/{k}/{i}", str(leaf), []) for i, leaf in enumerate(leaves)]))
    if not branches:
        return '<p class="mut">Nothing to map yet.</p>'
    rootnode = mmbuild.built(".", folder.name, branches)
    rootnode.id = "root"
    tree = mmtree.MindMap({"mindmap": "1", "title": folder.name, "built": "focus-page"}, rootnode)
    html = map_html(mm_.draw(tree, "", editable=False), folder, root)
    for name, url in drawn.items():                          # the label itself opens the drawing (JL 261029: "this should be in the label")
        html = re.sub(rf'<span class=(pm-role|pm-id)[^>]*>{re.escape(name)}</span>',
                      lambda m: f'<a class="{m.group(1)} pm-open pm-draw" data-pop="{frame.esc(name)}" href="{frame.esc(url)}" '
                                f'title="{frame.esc(name)}: open its quick drawing">✎ drawing</a>', html)   # words, no "✎ s01" (round 3)
    # a label is its kind and number in words ("Task 1"), its full folder name on hover: the long names ran past their
    # card and said the title twice (JL 261104), and "j01", "t01" read as ids (round 3)
    html = LADDER_NAME.sub(lambda m: f'<span class={m.group(1)}{m.group(2)} title="{m.group(3)}{m.group(4)}">{ladder_words(m.group(3))}</span>', html)
    if level == "Block":                                     # a question wraps beside its pill, its ↗ never past the box
        find = frame.esc("@" + frame.rel(folder, root) + "/find")
        html = html.replace(f'<div class=pm-para data-p="{find}">', f'<div class="pm-para pm-questions" data-p="{find}">')
    # the map fits its box: columns that shrink, leaves that wrap in theirs, and at phone width each card's leaves
    # under it; the box is as tall as the opened map, so Open all hides nothing (round 3: leaves cut at 1440 and 390)
    top = ""                                                 # a theme's own picture above its map (a Question Book's
    if level in ("Block", "Job"):                            # questions as a network, JL 261109)
        mod, prefix = page_module(frame.theme_of(folder, root), folder, root)
        fn = getattr(mod, prefix + "map_top", None) if mod is not None else None
        try:
            top = fn(folder, root, level) if fn else ""
        except Exception:
            top = ""
    return top + ('<style>' + FIT_MAP + '.focus-map.fit-map .pm-questions .pm-leaves li{display:flex;align-items:baseline}'
            '.focus-map.fit-map .pm-questions .pm-role{flex:none}'
            '.focus-map .pm-id{overflow-wrap:anywhere}.focus-map .pm-detail{max-width:380px}.focus-map .pm-detail,'
            '.focus-map .pm-detail *{white-space:normal}</style><div class="focus-map fit-map">' + html + '</div>')


def ladder_words(name: str) -> str:
    """'t01' -> 'Task 1', 'j02' -> 'Job 2', 'r03' -> 'Run 3', 's01' -> 'Topic 1': a map's label in words."""
    kind = {"j": "Job", "t": "Task", "r": "Run", "s": "Topic"}.get(name[:1], "")
    return f"{kind} {int(name[1:])}" if kind and name[1:].isdigit() else name


def mindmap_document(path, root, compact=False):
    if not inside(path, root) or not path.is_file() or not path.name.endswith(".mindmap.md"):
        return ""
    body = frame.mindmap_module().fragment(path, frame.rel(path, root), editable=False,
                                         url_of=lambda p: frame._file_url(p, root) if inside(p, root) else "")
    body = re.sub(r"<span class=pm-id>\d+(?:\.\d+)+</span>", "", body)   # a node's number is no word (round 2: "3.2" tags)
    if compact:                              # framed in a side tab: it fits the frame, as a page's own map (round 3)
        # ... but it never wraps a name: a map wider than its frame slides sideways (JL 261109: "why I don't have
        # the left right scroll here?", a leaf "SkinConductance" and "TimezoneOffset" cut in two)
        return document(path.name, f'<style>{FIT_MAP}.focus-map.framed{{border:0;padding:2px 4px}}{FRAMED_SCROLL}</style>'
                                   f'<div class="focus-map fit-map framed">{body}</div>')
    return document(path.name, body)
