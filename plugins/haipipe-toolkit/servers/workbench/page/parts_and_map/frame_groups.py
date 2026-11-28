"""The group bar: group emoji, tags, the group file and order, the bar itself, and the Studio's topic cards."""

from __future__ import annotations

import json
import re
from pathlib import Path

from live.frame_base import _block_above, _e, _rel, _yaml_scalar, level_of, short_name
from live.frame_studio import _note_facts, _notes, _sessions, _studio_topics, _topic_row, studio_inventory


_GROUP_BAD = re.compile(r"[`,·|*\n\r\t]")
# A group's emoji comes from its name (JL 261010): the first word of the table found in the name, else a
# fixed pick from the palette, so a new group gets one at once and everyone sees the same. The browser
# reads this same table from the nav's data-studio-emoji to give a group made there its emoji.
GROUP_EMOJI = {
    "current": "🎯", "guide": "🧭", "level": "🪜", "server": "🖥️", "structure": "🏗️", "ui": "🎨",
    "design": "🎨", "workflow": "🔁", "flow": "🔁", "run": "⚙️", "skill": "🛠️", "tool": "🛠️",
    "data": "📊", "model": "🧠", "paper": "📄", "report": "📑", "question": "❓", "idea": "💡",
    "draft": "✏️", "review": "🔍", "test": "🧪", "bug": "🐞", "issue": "🐞", "todo": "📌", "plan": "🗺️",
    "people": "👥", "meeting": "🗓️", "email": "✉️", "delivery": "📦", "method": "🧮", "evidence": "🔎",
    "slide": "🖼️", "chat": "💬", "agent": "🤖", "code": "💻", "focus": "🎯", "archive": "🗄️",
    "当前": "🎯", "指南": "🧭", "层级": "🪜", "服务": "🖥️", "结构": "🏗️", "界面": "🎨", "设计": "🎨",
    "流程": "🔁", "技能": "🛠️", "数据": "📊", "模型": "🧠", "论文": "📄", "报告": "📑", "问题": "❓",
    "想法": "💡", "草稿": "✏️", "测试": "🧪", "计划": "🗺️", "会议": "🗓️", "交付": "📦", "方法": "🧮",
}
GROUP_PALETTE = ("🔷", "🟣", "🟢", "🟠", "🧩", "🔖", "🌱", "📌", "💠", "🪐", "🍀", "🔸")


def group_emoji(label: str) -> str:
    """Pick a group's emoji from its name; the browser's emojiFor() follows the same steps."""
    low = label.lower()
    tokens = [t for t in re.split(r"[ _/&+-]+", low) if t]
    for word, emoji in GROUP_EMOJI.items():
        if word.isascii():
            if any(t == word or (t.endswith("s") and t[:-1] == word) for t in tokens):
                return emoji
        elif word in low:
            return emoji
    return GROUP_PALETTE[sum(ord(c) for c in label) % len(GROUP_PALETTE)]
_GROUP_RESERVED = {"current", "all", "untagged"}


def _set_tags(md: Path, tags: list) -> None:
    """Write a topic's **Tags:** line, placed above **Topic:**; drop it when no tag is left."""
    text = md.read_text(encoding="utf-8")
    line = "**Tags:** " + " · ".join(f"`{t}`" for t in tags) if tags else ""
    found = re.search(r"(?m)^\*\*Tags:\*\*[^\n]*(?:\n|\Z)", text)
    if found:
        end = found.end()
        if not line and re.match(r"[ \t]*\n", text[end:]):
            end += re.match(r"[ \t]*\n", text[end:]).end()
        text = text[:found.start()] + (line + "\n" if line else "") + text[end:]
    elif line:
        topic = re.search(r"(?m)^\*\*Topic:\*\*", text)
        under = re.search(r"(?m)^[=-]{3,}[ \t]*\n", text)
        if topic:
            text = text[:topic.start()] + line + "\n\n" + text[topic.start():]
        elif under:
            text = text[:under.end()] + "\n" + line + "\n" + text[under.end():]
        else:
            text = line + "\n\n" + text
    md.write_text(text, encoding="utf-8")


GROUP_FILE = "_groups.txt"      # studio/_groups.txt, related/_groups.txt: a bar's groups in button order (b10 s02-D17)
# What a group bar sorts: kind -> (its rows are called, its view's name). One bar, one script, one op for both.
GROUP_SHELVES = {"studio": ("topic", "Studio"), "related": ("item", "Related"), "reports": ("question", "Report"),
                 "delivery": ("result", "Delivery")}


def group_file(owner: Path, shelf: str = "studio") -> Path:
    """Where a bar's group order lives: <shelf>/_groups.txt; with no studio/ folder (sNN beside the Jobs, JL 261030)
    the Studio's order is the level's own _studio_groups.txt."""
    if shelf == "studio" and not (owner / "studio").is_dir():
        return owner / "_studio_groups.txt"
    return owner / shelf / GROUP_FILE


def studio_group_order(owner: Path, shelf: str = "studio") -> list:
    """The group names in the level's group file (group_file), in order; [] when the file is missing."""
    f = group_file(owner, shelf)
    if not f.is_file():
        return []
    names, seen = [], set()
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        name = line.strip()
        if name and not name.startswith("#") and name.casefold() not in seen:
            seen.add(name.casefold())
            names.append(name)
    return names


def _write_group_order(owner: Path, names: list, shelf: str = "studio") -> None:
    what = {"studio": "topics are the ones whose **Tags:** line names it",
            "related": "items are the related/related.md rows whose group cell names it",
            "reports": "Questions are the register rows whose group: line names it",
            "delivery": "results are the delivery/result_groups.md rows whose group cell names it"}[shelf]
    f = group_file(owner, shelf)
    f.parent.mkdir(exist_ok=True)
    f.write_text(
        f"# {shelf.title()} groups of this level, in button order. The workbench writes this file when a group is\n"
        f"# made, moved or deleted; a group's {what}.\n"
        + "".join(n + "\n" for n in names), encoding="utf-8")


def group_list(owner: Path, root: Path, kind: str, tag_lists: list, listing: str, picker: str = "",
               add: str = "", starting: tuple = (), fixed: tuple = ()) -> str:
    """A list under its group bar, the Studio's topics, Related's items or a Report's Questions (b10 s02-D16,
    D17; Related and Report JL 261011): Current first (kept in the browser), then each group with its count, in
    <kind>/_groups.txt order, then `starting` (a theme's groups, shown even empty), then the rest, Untagged,
    + Group. No group picked shows every row (no All button, JL 261010). `tag_lists` holds each row's groups;
    the page script drives the bar. A group in `fixed` (the theme's, read off the Question) and one in `starting`
    (the theme's suggested ones) each take their own colour, a Block's own stays white (b10 s05-D16, JL 261012:
    "for each group ... the fixed groups (or the suggested default group labels) ... give them different colors")."""
    noun, label = GROUP_SHELVES[kind]
    counts, untagged = {}, 0
    for tags in tag_lists:
        untagged += not tags
        for tag in tags:
            key = tag.casefold()
            name, count = counts.get(key, (tag, 0))
            counts[key] = (name, count + 1)
    options = [("__current__", "Current", 0)]
    for name in studio_group_order(owner, kind) + list(fixed) + list(starting):   # saved order, then the theme's; empty kept
        if any(key == name.casefold() for key, _, _ in options):
            continue
        name, count = counts.pop(name.casefold(), (name, 0))
        options.append((name.casefold(), name, count))
    if kind == "reports":                                  # a name the Studio uses too keeps the Studio's order (s05-D08)
        for name in studio_group_order(owner if level_of(owner) == "Block" else (_block_above(owner) or owner)):
            if name.casefold() in counts:
                name, count = counts.pop(name.casefold())
                options.append((name.casefold(), name, count))
    options += [(key, name, count) for key, (name, count) in sorted(counts.items())]
    if untagged:
        options.append(("__untagged__", "Untagged", untagged))

    def icon(key: str, name: str) -> str:
        return "" if key == "__untagged__" else f'<span class=grp-emoji aria-hidden=true>{group_emoji(name)}</span>'

    fixed_keys = {g.casefold() for g in fixed}
    suggested = {g.casefold() for g in starting} - fixed_keys

    def group_button(key: str, name: str, count: int) -> str:
        cls, why = ("tab grp-fixed", ' title="Fixed by the theme: it comes from the Question itself"') \
            if key in fixed_keys else ("tab grp-suggested", ' title="Suggested by the theme: shown even when empty"') \
            if key in suggested else ("tab", "")
        button = (f'<button type=button class="{cls}"{why} data-studio-label="{_e(name)}" '
                  f'data-studio-tag="{_e(key)}" aria-pressed="false">{icon(key, name)}{_e(name)} <span class=tag-count>{count}</span></button>')
        if key in ("__current__", "__untagged__") or key in fixed_keys:    # a fixed group cannot be deleted
            return button
        # a group is a tag: × deletes it from every row, the rows stay (b10 s02-D16)
        return (f'<span class=grp>{button}<button type=button class=grp-x data-studio-delete="{_e(key)}" '
                f'title="Delete group {_e(name)}" aria-label="Delete group {_e(name)}">×</button></span>')

    buttons = "".join(group_button(*option) + ("<span class=bar></span>" if option[0] == "__current__" else "")
                      for option in options)
    new_group = (f'<button type=button class=grp-new title="Make a new group, then drag {noun}s onto it">+ Group</button>'
                 '<span class=grp-form hidden><input type=text maxlength=30 placeholder="Group name" '
                 'aria-label="New group name"><button type=button class=grp-ok>Add</button>'
                 '<button type=button class=grp-cancel>Cancel</button></span>')
    table = json.dumps({"words": GROUP_EMOJI, "palette": GROUP_PALETTE}, ensure_ascii=False)
    filters = (f'<nav class="row studio-filters" aria-label="{label} {noun} groups" data-studio-emoji="{_e(table)}">'
               f'{buttons}{new_group}</nav>')
    where = {"studio": "each topic's notes", "related": "the group column of related/related.md",
             "reports": "each Question's group: line in the face's ## Questions",
             "delivery": "delivery/result_groups.md"}[kind]
    kinds = " ".join(w for w, on in (("<span class=\"grp-key grp-fixed\">gray</span>: fixed by the theme;", fixed_keys),
                                      ("<span class=\"grp-key grp-suggested\">amber</span>: suggested by the theme, "
                                       "shown even when empty;", suggested)) if on)
    help_ = (f'<p class="mut studio-help">Every {noun} shows until you pick a group; pick it again to see them all. '
             f'Drag a{"n" if noun[0] in "aeiou" else ""} {noun} by ⋮⋮ onto a group; drag a group sideways to move it. '
             f'Groups are saved in {_e(where)}; Current is saved in this browser.'
             + (f' {kinds} white: added here.' if kinds else '') + '</p>')
    empty = '<p class="mut studio-empty" hidden>This group is empty.</p>'
    status = '<p class="mut studio-status" role=status aria-live=polite></p>'
    marks = "" if kind == "studio" else f' data-group-kind={kind} data-group-noun={noun}'
    return (f'<div class=studio-topics data-studio-owner="{_e(_rel(owner, root))}"{marks}>{filters}'
            f'{picker}{help_}{status}{empty}{listing}{add}</div>')


def studio_cards(folder: Path, root: Path) -> str:
    """The Studio's topic rows under their group bar (group_list); sNN is a topic, never a group."""
    folder, root = folder.resolve(), root.resolve()
    topics = studio_inventory(folder, root)
    own = [(t, d) for source, t, d in topics if source == folder]
    last = max([int(m.group(1)) for t, _ in own for m in [re.match(r"s(\d+)", t.name)] if m] or [0])
    add = f'<p class="mut add">+ Add topic → studio/s{last + 1:02d}-&lt;topic&gt;/</p>'
    rows = "".join(_topic_row(t, d, root, source, shared=folder) for source, t, d in topics)
    sources = dict.fromkeys(source for source, _, _ in topics)
    picker = ""
    if len(sources) > 1:
        choices = ''.join(f'<option value="{_e(source.relative_to(folder).as_posix() if source != folder else "")}">'
                          f'{_e(short_name(source.name) if source != folder else "Block")}</option>' for source in sources)
        picker = ('<label class=studio-source>Source <select aria-label="Studio source" data-studio-source-filter>'
                  '<option value="__all__">All sources</option>' + choices + '</select></label>')
    return group_list(folder, root, "studio", [_note_facts(_notes(t))["tags"] for _, t, _ in topics],
                      rows or '<p class=mut>No studio topics yet.</p>', picker, add)


def studio_sessions(folder: Path, root: Path) -> list:
    """One Runs-panel row per topic that has sessions: its soft Run `run-draw-<sNN>`, its passes, and
    the older `chat/` sessions kept until they move into passes (JL 261007: the card read as a
    stray session; it is a pass of the topic's Run)."""
    rows = []
    for topic, _ in _studio_topics(folder):
        sessions = _sessions(topic, folder)
        if not sessions:
            continue
        sid = topic.name.split("-", 1)[0]
        run = folder / "runs" / f"run-draw-{sid}"
        older = sum(1 for s in sessions if s["path"].parent.name == "chat")
        passes = len(sessions) - older
        what = " · ".join(x for x in (f"{passes} pass{'es' if passes != 1 else ''}" if passes else "",
                                      f"{older} older chat/ session{'s' if older != 1 else ''}" if older else "") if x)
        card = run / "run.yaml"                 # its own status (waiting, held …); "done" only when it has no card
        status = _yaml_scalar(card.read_text(encoding="utf-8", errors="ignore"), "status") if card.is_file() else ""
        rows.append({"run_id": f"run-draw-{sid}", "status": status or "done", "target": topic.name,
                     "_display": f"run-draw-{sid}", "_of": f"studio topic {topic.name} · {what}",
                     "result": _rel(run if run.is_dir() else sessions[0]["path"].parent, root),
                     "result_path": str(run / "passes" if run.is_dir() else sessions[0]["path"].parent)})
    return rows
