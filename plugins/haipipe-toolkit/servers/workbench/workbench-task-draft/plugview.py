"""🖼🚪 Plugview · read-only evidence/display/ and evidence/probe/ surfaces.

THE DIVISION OF LABOUR, the same one export.py drew for latex/word/bibex:

  the writers (renderer skills · the probe orchestrator)   HOW material is made
  this file                                                WHERE the tab looks, read-only

Nothing here writes MATERIAL. A display unit is written by its renderer and
accepted by a person (QPf5); a probe card is raised by its consumer and bound
by the collector (QPf9). This surface SHOWS both and writes neither, which is
each contract's own rule: "the pane shows everything · writes NOTHING".
One carve-out, ruled JL 260816 ("I want to add the rebuild button, so that we
can have a new list"): display's 🔄 recompiles each unit's DERIVED preview
(preview.tex ▶ preview.pdf, the unit README's own rebuild contract) before
re-rendering the list. intake/, recipe/, and the accepted: tick stay a
person's and are never touched — a preview is a projection, not material.

THE VIEW IS DERIVED, like every export view: `<workbench>/<stem>-view.html` is
regenerated on each open and never hand-edited. An EMPTY workbench renders the
contract's ghost scaffold instead of a blank, so an empty tab teaches what
belongs there (JL 260815).
"""
import json
import os
import re
from pathlib import Path

from live.plugview_templates import (  # noqa: F401  (moved; names kept importable here)
    _GHOST_DISPLAY, _GHOST_EVIDENCE, _PAGE, _STATE_BADGE, _STRIP_NAV)


def _esc(s):
    import html
    return html.escape(str(s or ""), quote=False)


def _readme_rows(readme):
    """`- key: value` bullets from a unit README, in file order."""
    rows = []
    if readme.is_file():
        for ln in readme.read_text(errors="replace").splitlines():
            m = re.match(r"^\s*-\s+([\w-]+):\s*(.+)$", ln)
            if m:
                rows.append((m.group(1), m.group(2)))
    return rows


def _inline_md(text):
    """The small, safe Markdown subset a probe card needs in its read-only tab.

    Card bodies are authored evidence summaries, not executable HTML.  Escape
    first, then restore only code and bold spans so a path or result can remain
    legible without allowing a card to inject markup into the Board shell.
    """
    text = _esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)


def _read(path):
    return path.read_text(errors="replace") if path.is_file() else ""


def _head_fields(text):
    """`key: value` lines above the first `##` in a legacy Probe card."""
    out = {}
    for ln in text.splitlines():
        if ln.startswith("## "):
            break
        m = re.match(r"^([a-z_-]+):\s*(.*)$", ln)
        if m:
            out.setdefault(m.group(1), m.group(2).strip())
    return out


def _proof_rows(manifest):
    """-> ([{name,kind,rows,run,source,why}], note) from proof/manifest.yaml.

    A deliberately small reader: the surface must not gain a yaml dependency,
    and the manifest is authored to a fixed shape (§🧾).
    """
    if not manifest.is_file():
        return [], "no proof/manifest.yaml"
    text = manifest.read_text(errors="replace")
    rows, cur, in_files = [], None, False
    lines = text.splitlines()
    # A folded scalar (`why: >-`) keeps its text on the following indented
    # lines. Without this the surface printed the literal `>-` (found 260817
    # by looking at the rendered tab, not at the parser).
    for i, ln in enumerate(lines):
        m = re.match(r"^(\s*)([a-z_0-9]+):\s*[>|]-?\s*$", ln)
        if m:
            pad, tail = len(m.group(1)), []
            for nxt in lines[i + 1:]:
                if nxt.strip() and len(nxt) - len(nxt.lstrip()) > pad:
                    tail.append(nxt.strip())
                else:
                    break
            lines[i] = "%s%s: %s" % (m.group(1), m.group(2), " ".join(tail))
    for ln in lines:
        if re.match(r"^files:\s*\[\s*\]\s*$", ln):
            in_files = False
            continue
        if re.match(r"^files:\s*$", ln):
            in_files = True
            continue
        if re.match(r"^(why_empty|pending|card):", ln):
            in_files = False
        if in_files and re.match(r"^\s*-\s+\w+:", ln):
            cur = {}
            rows.append(cur)
        if in_files and cur is not None:
            m = re.match(r"^\s*-?\s*([a-z_0-9]+):\s*(.*)$", ln)
            if m:
                cur[m.group(1)] = m.group(2).strip()
    note = ""
    m = re.search(r"^(why_empty|pending):\s*(.*)$", text, re.M)
    if m and not rows:
        tail = []
        for ln in text.split(m.group(0), 1)[1].splitlines():
            if re.match(r"^\s+\S", ln):
                tail.append(ln.strip())
            elif tail:
                break
        note = "%s: %s" % (m.group(1), " ".join([m.group(2)] + tail).strip(" >-"))
    return rows, note


def _missing_step(head, qx, ax, proof, pnote):
    """The FIRST step that is not done — never a claim that one exists merely
    because the folder does (§🚪)."""
    if not qx.strip():
        return "no q-executor written yet: nothing can be dispatched"
    if not head.get("target"):
        return "q-executor written, target empty: nobody has been asked yet"
    if not ax.strip():
        return "dispatched, no answer copied back into a-executor.md"
    if not proof and not pnote:
        return "answered, but proof/ is empty and says nothing about why"
    return "answered · nobody has read it and written the A-consumer"


def _embed_proof(href, path):
    """EMBED the file, never re-render it as HTML (JL 260817).

    Display frames `preview.pdf` with <object>; a proof file is framed the same
    way. This is not only a look: every proof bug so far came from PARSING —
    `15.3332***` lost its stars to the bold rule, a folded yaml scalar printed
    `>-`, and esttab's `="..."` armour needed its own splitter. An embedded file
    is the file, so there is nothing left to get wrong.
    """
    if path.suffix == ".pdf":
        return ("<object class='exhibit' data='%s' type='application/pdf'>"
                "<a href='%s'>%s</a></object>" % (href, href, _esc(path.name)))
    return ("<iframe class='exhibit' src='%s' title='%s' loading='lazy'></iframe>"
            % (href, _esc(path.name)))


def _step(icon, label, note, inner, tone=""):
    """One wall step as its OWN panel: a header strip naming it, then its body.

    JL 260817 read the previous card as "乱糟糟" — five steps ran together in
    one column with only a hairline between them, so the eye could not tell
    where the dispatched question ended and the answer began.
    """
    return ("<section class='step %s'><header class='sh'><span>%s</span>"
            "<b>%s</b><span class='sn'>%s</span></header>"
            "<div class='sb'>%s</div></section>"
            % (tone, icon, _esc(label), _esc(note), inner))


def _proof_block(rows, note, folder, rel):
    """Wall step 4: ONE PANEL PER FILE — a header bar carrying the filename and
    its facts, the framed file flush underneath, provenance folded below."""
    if not rows:
        return ("<div class='hole'>🕳 %s</div>"
                % _esc(note or "empty, and the manifest says nothing about why"))
    out = []
    for r in rows:
        nm = r.get("name", "?")
        path = folder / nm
        facts = "".join("<span class='fact'>%s</span>" % _esc(x) for x in (
            r.get("kind", "?"), "%s rows" % r.get("rows", "?"),
            "%s bytes" % r.get("bytes", "?"),
            r.get("run", "")) if x)
        body = (_embed_proof(_esc("%s/proof/%s" % (rel, nm)), path)
                if path.is_file()
                else "<div class='hole'>🕳 named in the manifest, not on disk</div>")
        out.append(
            "<figure class='pf'>"
            "<figcaption class='pfh'><span class='pfn'>%s</span>"
            "<span class='facts'>%s</span></figcaption>"
            "%s"
            "<details class='pfp'><summary>provenance</summary>"
            "<div>source: <code>%s</code></div>"
            "<div>pulled: %s</div>"
            "</details></figure>"
            % (_esc(nm), facts, body, _esc(r.get("source", "?")),
               _esc(r.get("pulled", "?"))))
        if r.get("why"):
            out.append("<div class='why'>%s</div>" % _esc(r["why"]))
    return "".join(out)


def _probe_body_html(text):
    """Render the material below a probe card's header metadata.

    The previous surface silently discarded this body, leaving a bound Probe
    looking like a question plus a file tree.  This intentionally small reader
    supports the structures used by card.md (paragraphs, headings and lists)
    while keeping the workbench read-only and dependency-free.
    """
    kept = []
    for ln in text.splitlines():
        if ln.startswith("# ") or re.match(
                r"^(?:state|question|binding)\s*:", ln, re.I):
            continue
        kept.append(ln.rstrip())
    out, para, items = [], [], []

    def flush_para():
        if para:
            out.append("<p>%s</p>" % _inline_md(" ".join(x.strip() for x in para)))
            para.clear()

    def flush_items():
        if items:
            out.append("<ul>%s</ul>" % "".join(
                "<li>%s</li>" % _inline_md(x) for x in items))
            items.clear()

    fence = None
    for ln in kept:
        s = ln.strip()
        # A ``` block is VERBATIM. Without this the inline reader ate the
        # significance stars: `15.3332***` rendered as `15.3332*`, because
        # `**` is bold everywhere else (found 260817 by reading the tab).
        if s.startswith("```"):
            if fence is None:
                flush_para()
                flush_items()
                fence = []
            else:
                out.append("<pre>%s</pre>" % _esc("\n".join(fence)))
                fence = None
            continue
        if fence is not None:
            fence.append(ln)
            continue
        if not s:
            flush_para()
            flush_items()
        elif s.startswith("##"):
            flush_para()
            flush_items()
            out.append("<h2>%s</h2>" % _inline_md(s.lstrip("#").strip()))
        elif re.match(r"^[-*]\s+", s):
            flush_para()
            items.append(re.sub(r"^[-*]\s+", "", s))
        else:
            flush_items()
            para.append(s)
    if fence:
        out.append("<pre>%s</pre>" % _esc("\n".join(fence)))
    flush_para()
    flush_items()
    return "".join(out)


def _display_state(unit, rows):
    """Compute declared/rendered/accepted from files, never from folder count."""
    row = {k.lower(): v for k, v in rows}
    inputs = unit / "intake" / "inputs"
    has_intake = (unit / "intake" / "manifest.yaml").is_file() and \
        inputs.is_dir() and any(p.is_file() for p in inputs.rglob("*"))
    has_recipe = (unit / "recipe").is_dir() and \
        any(p.is_file() for p in (unit / "recipe").rglob("*"))
    assets = unit / "assets"
    has_asset = assets.is_dir() and any(
        p.is_file() and p.name in ("table-body.tex", "figure.pdf", "figure.png", "figure.svg")
        for p in assets.rglob("*"))
    has_preview = (unit / "preview.pdf").is_file()
    accepted_text = row.get("accepted", "").strip().lower()
    accepted = accepted_text.startswith(("✅", "yes", "true", "accepted"))
    rendered = has_asset and has_preview
    if not has_intake:
        next_step = "① INTAKE missing · add an approved frozen snapshot"
    elif not has_recipe:
        next_step = "② RENDER missing · add the renderer-owned recipe"
    elif not has_asset:
        next_step = "② RENDER has not produced a winning asset"
    elif not has_preview:
        next_step = "④ BUILD missing · compile preview.pdf"
    elif not accepted:
        next_step = "⑤ ACCEPT pending · rendered candidate awaits human review"
    else:
        next_step = "complete · rendered and human-accepted"
    return {"rendered": rendered, "accepted": accepted, "next": next_step}


def _tree(root, keep=60):
    """An indented folder tree (JL 260815: "I want it to be like the folder
    structure"), derived halves marked ⚙️; capped, and the cap is said."""
    lines = []

    def walk(d, prefix):
        entries = sorted(
            (e for e in d.iterdir()
             if not e.name.startswith(".") and not e.name.endswith("-view.html")),
            key=lambda e: (e.is_file(), e.name))
        for i, e in enumerate(entries):
            if len(lines) >= keep:
                return
            last = i == len(entries) - 1
            rel = e.relative_to(root).as_posix() + ("/" if e.is_dir() else "")
            mark = "⚙️ " if re.match(
                r"(assets|candidates|versions)(/|$)|preview\.pdf$", rel) else ""
            lines.append(prefix + ("└── " if last else "├── ")
                         + mark + e.name + ("/" if e.is_dir() else ""))
            if e.is_dir():
                walk(e, prefix + ("    " if last else "│   "))

    walk(root, "")
    if len(lines) >= keep:
        lines.append("… (capped at %d entries)" % keep)
    return "\n".join(lines)


class PlugViewMixin:

    # ---- POST /_board/display ----------------------------------------
    def plug_display(self, p):
        page_src, out_dir, _, err = self._export_target(p, "display")
        if err:
            return None, err
        # 🔄 the rebuild recompiles every unit's derived preview first
        # (JL 260816): preview.tex ▶ preview.pdf in the unit's own dir, the
        # contract line each unit README already states. A unit without a
        # preview.tex is skipped whole — nothing is invented for it.
        fails = []
        env = dict(os.environ,
                   PATH="/Library/TeX/texbin:" + os.environ.get("PATH", ""))
        for unit in sorted(d for d in out_dir.iterdir() if d.is_dir()):
            if not (unit / "preview.tex").is_file():
                continue
            code, log = self._run(
                ["xelatex", "-interaction=nonstopmode", "preview.tex"],
                timeout=120, cwd=unit, env=env)
            if code != 0 or not (unit / "preview.pdf").is_file():
                fails.append(unit.name)
        cards, states = [], []
        for unit in sorted(d for d in out_dir.iterdir() if d.is_dir()):
            rows = _readme_rows(unit / "README.md")
            state = _display_state(unit, rows)
            states.append(state)
            # THE RENDER LEADS (JL 260819: "display the pdf at the very top,
            # and then show information" — clicking a unit showed him its
            # description rows first and the drawn thing below the fold).
            pdf = unit / "preview.pdf"
            if pdf.is_file():
                href = _esc(unit.name + "/preview.pdf")
                body = ("<object class='pdf' data='%s' type='application/pdf'>"
                        "<a href='%s'>preview.pdf</a></object>" % (href, href))
                body += ("<div class='%s' style='margin:7px 0'>%s</div>"
                         % ("ready" if state["accepted"] else "pending",
                            _esc(state["next"])))
            else:
                body = ("<div class='card ghost' style='margin:8px 0'>"
                        "🕳 no render yet · %s</div>" % _esc(state["next"]))
            body += "".join("<div class='mut'><b style='color:var(--fg)'>%s</b>: %s</div>"
                            % (_esc(k), _esc(v)) for k, v in rows)
            body += "<pre>%s</pre>" % _esc(_tree(unit))
            cards.append("<div class='card' id='%s'><b>%s</b>%s</div>"
                         % (_esc(unit.name), _esc(unit.name), body))
        # The NAME LIST: every unit as a chip, clicking one shifts the deck
        # there (JL 260815: "where is the name list for all the displays?").
        stem = out_dir.parent.name
        units = [d.name for d in sorted(out_dir.iterdir()) if d.is_dir()]
        # one state word for the deck, never "N declared · N rendered · N accepted" (JL 261113); each chip shows its own
        accepted, rendered = sum(s["accepted"] for s in states), sum(s["rendered"] for s in states)
        word = ("accepted" if units and accepted == len(units) else "rendered" if units and rendered == len(units)
                else "in progress" if rendered else "not rendered yet")
        summary = "<div class='summary'><span class='metric%s'>%s</span></div>" % (" ready" * (word == "accepted"), word)
        chips = ""
        if len(units) > 1:
            chips = "<div class='chips'>%s</div>" % "".join(
                "<a class='chip' href='#%s'>%s</a>"
                % (_esc(u), _esc(u[len(stem) + 1:] if u.startswith(stem + "-") else u))
                for u in units)
        footer = ("read-only · renderers write recipe/ and assets/; "
                  "a person rules intake/ and ticks accepted: (QPf5 §3) · "
                  "🔄 recompiles each unit's preview")
        if fails:
            footer += " · ⚠️ preview failed: " + ", ".join(fails)
        return self._plug_page(p, out_dir, "display", "🖼 Display",
                               cards or [_GHOST_DISPLAY], footer,
                               strip=True, head=summary + chips)

    # ---- POST /_board/probe ------------------------------------------
    def plug_probe(self, p):
        """Compatibility refusal: Page-local Probe storage is retired."""
        return None, ("Probe is retired. Specify a typed Evidence Item in "
                      "draft/, map Supporting Runs in SURVEY, and LAND one "
                      "local Result instead.")

    def _retired_plug_probe(self, p):
        """One card per FOLDER, read in WALL ORDER so the reader sees the
        crossing: head, what was asked, what came back, the proof files, and
        the stake-bearing audit copy folded away (legacy Probe boundary).

        The four counts and the `read` verdict are computed from DISK, never
        from the `state:` word — a folder count is not an answered question.
        """
        page_src, out_dir, _, err = self._export_target(p, "probe")
        if err:
            return None, err
        dirs = sorted(d for d in out_dir.iterdir()
                      if d.is_dir() and d.name.startswith("PP"))
        flat = sorted(f for f in out_dir.glob("PP*.md"))
        cards, names, tally = [], [], {"planned": 0, "commissioned": 0,
                                       "answered": 0, "read": 0}
        for d in dirs + flat:
            card = d / "card.md" if d.is_dir() else d
            if not card.is_file():
                continue
            head = _head_fields(card.read_text(errors="replace"))
            name = d.name if d.is_dir() else d.stem
            names.append(name)
            state = head.get("state", "")
            badge = _STATE_BADGE.get(state.lower(), "⬜")

            qx = _read(d / "executor" / "q-executor.md")
            ax = _read(d / "executor" / "a-executor.md")
            qc = _read(d / "consumer" / "q-consumer.md")
            proof, pnote = _proof_rows(d / "proof" / "manifest.yaml")

            # the counts, from disk
            tally["planned"] += 1
            if head.get("target"):
                tally["commissioned"] += 1
            if ax.strip() and head.get("target"):
                tally["answered"] += 1
            is_read = head.get("read", "").startswith("✅")
            tally["read"] += 1 if is_read else 0

            # DISPLAY'S SHAPE, filled with probe's material, and every
            # step in its OWN PANEL (JL 260817: "每一个 file 是不是应该分开
            # 一些？现在看着乱糟糟的").
            rows = []
            if head.get("question"):
                rows.append("<div class='q'>%s</div>" % _inline_md(head["question"]))
            rows.append("<dl class='fields'>%s</dl>" % "".join(
                "<dt>%s</dt><dd>%s</dd>" % (_esc(k), _esc(head[k]))
                for k in ("state", "route", "bank", "serves", "target")
                if head.get(k)))
            rows.append("<div class='next %s'>%s</div>"
                        % ("ok" if is_read else "owed",
                           _esc(("✅ read · " + head.get("read", "").lstrip("✅ "))
                                if is_read
                                else "🕳 " + _missing_step(head, qx, ax, proof, pnote))))
            rows.append(_step("🔢", "proof", "the files behind the answer",
                              _proof_block(proof, pnote, d / "proof", d.name),
                              tone="lead"))
            rows.append(_step("🧱", "asked", "executor/q-executor.md · the only "
                              "thing dispatched", _probe_body_html(qx)))
            if ax.strip():
                rows.append(_step("📥", "came back", "executor/a-executor.md · "
                                  "the bank's own words", _probe_body_html(ax)))
            if qc.strip():
                rows.append("<details class='step fold'><summary class='sh'>"
                            "<span>🗂</span><b>audit</b><span class='sn'>"
                            "consumer/q-consumer.md · who wanted it, and why"
                            "</span></summary><div class='sb'>%s</div></details>"
                            % _probe_body_html(qc))
            rows.append("<details class='step fold'><summary class='sh'>"
                        "<span>📂</span><b>files</b><span class='sn'>%s</span>"
                        "</summary><div class='sb'><pre>%s</pre></div></details>"
                        % (_esc(d.name), _esc(_tree(d))))
            pp, _, words = name.partition("-")
            cards.append("<div class='card' id='%s'>"
                         "<div class='chead'><span class='badge'>%s</span>"
                         "<span class='pid'>%s</span>"
                         "<span class='ptitle'>%s</span></div>%s</div>"
                         % (_esc(name), badge, _esc(pp),
                            _esc(words.replace("-", " ")), "".join(rows)))

        n = len(names)
        verdict = "ready" if n and tally["read"] == n else ""
        # one state word, never "N planned · N commissioned · N answered · N/M read" (JL 261113)
        word = ("read" if verdict else "answered" if n and tally["answered"] == n
                else "in progress" if tally["commissioned"] or tally["answered"] else "planned" if n else "nothing planned")
        summary = "<div class='summary'><span class='metric %s'>%s</span></div>" % (verdict, word)
        chips = ""
        if n > 1:
            chips = "<div class='chips'>%s</div>" % "".join(
                "<a class='chip' href='#%s'>%s</a>"
                % (_esc(x), _esc(x.split("-", 1)[0] if x.startswith("PP") else x))
                for x in names)
        return self._plug_page(p, out_dir, "probe", "🚪 Probe",
                               cards or [_GHOST_EVIDENCE],
                               "read-only · consumer/ never crosses · executor/ is "
                               "the only thing dispatched · a person ticks read:",
                               strip=True, head=summary + chips)

    # ---- shared page writer ------------------------------------------
    def _plug_page(self, p, out_dir, route, label, cards, footer, strip=False, head=""):
        """strip=True lays the cards as a horizontal deck, one unit filling
        the pane, snap-shifted right to the next (JL 260815: "shift to the
        new one to the right") — the slide deck's scroll-snap move, sideways."""
        stem = out_dir.parent.name
        btn, script = self._rebuild_ui(route, p)
        if strip and len(cards) > 1:
            nav = ("<span class='nav'><button id='prev'>◀</button>"
                   "<span class='pos' id='pos'></span>"
                   "<button id='next'>▶</button></span>")
            deck = "<div class='strip' id='strip'>%s</div>" % "".join(cards)
            script += _STRIP_NAV
        else:
            nav = ""
            deck = "".join(cards)
        body = ("%s%s<h1>%s · %s</h1>"
                "<div class='mut' style='margin:0 0 12px'>%s</div>%s%s%s"
                % (btn, nav, label, _esc(stem), _esc(footer), head, deck, script))
        view = out_dir / ("%s-view.html" % stem)
        view.write_text(_PAGE.format(title="%s · %s" % (label, stem), body=body),
                        encoding="utf-8")
        url = self._url_of(view)
        return {"url": url, "count": len(cards)}, None
