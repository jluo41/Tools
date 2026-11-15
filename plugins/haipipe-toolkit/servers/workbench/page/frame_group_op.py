"""The group op: add, remove, rename or reorder a group on a Studio topic, Related item, Question or result."""

from __future__ import annotations

from pathlib import Path

from live.frame_base import VANILLA, face
from live.frame_studio import _note_facts, _notes, _split_tags, studio_inventory
from live.frame_groups import (GROUP_SHELVES, _GROUP_BAD, _GROUP_RESERVED, _set_tags, _write_group_order,
                               studio_group_order)
from live.frame_report import _register, _register_set_groups, _theme_fixed
from live.frame_delivery import _delivery_set_groups, delivery_items
from live.frame_related import _related_set_groups, related_items


def _group_members(owner: Path, root: Path, kind: str) -> dict:
    """key -> (name, groups, write) for what a group bar sorts: the Studio's topics (their **Tags:** line) or
    the Block's related items (their row's group cell) or a level's Questions (their register group: line, after
    the theme's fixed groups); write(groups) returns (groups read back, error)."""
    out = {}
    if kind == "reports":
        from live import frame                # frame.themes and frame.theme_of, so a test that swaps them is read
        md, theme = face(owner), frame.themes().get(frame.theme_of(owner, root), VANILLA)
        for row in _register(md):
            qid, fixed = str(row["id"]), _theme_fixed(theme, row, owner)

            def write(new, qid=qid, fixed=fixed):
                drop = {g.casefold() for g in fixed}
                _register_set_groups(md, qid, [g for g in new if g.casefold() not in drop])
                back = next((r for r in _register(md) if str(r["id"]) == qid), {})
                return _split_tags(",".join(fixed + [str(back.get("group") or "")])), None
            out[qid] = (qid, _split_tags(",".join(fixed + [str(row.get("group") or "")])), write)
        return out
    if kind == "delivery":                    # a result's file kinds are fixed; a person's groups in result_groups.md
        for item in delivery_items(owner):
            def write(new, item=item):
                _delivery_set_groups(owner / "delivery", item["key"], [g for g in new if g not in item["fixed"]])
                back = next((i for i in delivery_items(owner) if i["key"] == item["key"]), item)
                return back["groups"], None
            out[item["key"]] = (item["title"], item["groups"], write)
        return out
    if kind == "related":
        for item in related_items(owner):
            def write(new, item=item):
                _related_set_groups(owner, item, new)
                return next((i["groups"] for i in related_items(owner) if i["key"] == item["key"]), []), None
            out[item["key"]] = (item["title"], item["groups"], write)
        return out
    for _, topic, _ in studio_inventory(owner, root):
        md = _notes(topic)

        def write(new, topic=topic, md=md):
            if md is None:
                return None, f"{topic.name} has no notes file to hold its groups."
            _set_tags(md, new)
            return _note_facts(md)["tags"], None
        out[topic.relative_to(owner).as_posix()] = (topic.name, _note_facts(md)["tags"], write)
    return out


def studio_group_op(root: Path, p: dict) -> tuple:
    """Add a row to a group, take it out, or delete the group from every row: the Studio's topics, or with
    `kind: related` the Block's related items (JL 261011: Related's groups work like the Studio's).

    A group is a tag saved on disk beside what it sorts (a topic's **Tags:** line, a related row's group
    cell), so every person and agent sees the same groups (b10 s02-D16). Returns (result, error).
    """
    root = Path(root).resolve()
    owner = (root / str(p.get("path") or "").lstrip("/")).resolve()
    if (owner != root and root not in owner.parents) or not owner.is_dir():
        return None, "No such folder under this root."
    kind = str(p.get("kind") or "studio")
    if kind not in GROUP_SHELVES:
        return None, "kind must be studio, related, reports or delivery."
    op, tag = p.get("op"), str(p.get("tag") or "").strip()
    if op not in ("add", "remove", "delete", "create", "order"):
        return None, "op must be add, remove, delete, create or order."
    bad = lambda name: not name or len(name) > 30 or _GROUP_BAD.search(name) or name.casefold() in _GROUP_RESERVED
    rule = "A group name is 1 to 30 characters, without ` , · | or *, and is not Current, All or Untagged."
    order = studio_group_order(owner, kind)
    if op == "order":                       # the buttons' new order; a name left out keeps its place at the end
        wanted = [str(n).strip() for n in (p.get("groups") or []) if isinstance(n, str)]
        if any(bad(n) for n in wanted):
            return None, rule
        keys = {n.casefold() for n in wanted}
        names = list(dict.fromkeys(wanted)) + [n for n in order if n.casefold() not in keys]
        _write_group_order(owner, names, kind)
        return {"order": names}, None
    if bad(tag):
        return None, rule
    if op == "create":
        if tag.casefold() not in {n.casefold() for n in order}:
            order.append(tag)
            _write_group_order(owner, order, kind)
        return {"order": order}, None
    members, (noun, label) = _group_members(owner, root, kind), GROUP_SHELVES[kind]
    if op == "delete":
        picked = list(members)
    elif str(p.get("topic") or "") in members:
        picked = [str(p.get("topic"))]
    else:
        return None, f"That {noun} is not in this {label}."
    key, out, changed = tag.casefold(), {}, 0
    for k in picked:
        name, tags, write = members[k]
        has = any(t.casefold() == key for t in tags)
        if op == "add" and not has:
            new = tags + [tag]
        elif op != "add" and has:
            new = [t for t in tags if t.casefold() != key]
        else:
            if op != "delete":                      # nothing to change; report its groups as they are
                out[k] = tags
            continue
        after, err = write(new)
        if err:
            return None, err
        if op != "add" and any(t.casefold() == key for t in after):
            return None, (f"{name}: that group is its subfolder, related/{tag}/; it changes only when the file "
                          "moves." if kind == "related" else
                          f"{name}: {tag} is fixed by the theme (s05-D06); it cannot be taken out here."
                          if kind == "reports" else
                          f"{name}: {tag} is its file kind; it cannot be taken out." if kind == "delivery" else
                          f"{name}: that group comes from a **Type:** line; change it in the notes.")
        out[k] = after
        changed += 1
    if op == "delete" and any(n.casefold() == key for n in order):
        _write_group_order(owner, [n for n in order if n.casefold() != key], kind)
    return {"changed": changed, "topics": out}, None
