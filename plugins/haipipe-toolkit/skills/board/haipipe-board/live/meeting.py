"""🗣 Meeting · a page's own kept record of a conversation (QPf14).

STANDALONE, AS DECLARED (JL 260818): the roster's `meeting/` row already named
this shape — `<page>/meeting/<YYMMDD-HHMM>/` holding `digest.md` and
`transcript.md` — before this file existed, and the design round that added
`task/` beside it (QPf13) confirmed the shape rather than pointing it at the
separate `Meeting-<n>` PAGE TYPE (`haipipe-page-for-meeting`). The two solve
different problems: a `Meeting-<n>` page is a whole board page recording a
conversation that OWES a decision to some other page (routing, ruling, its
own Aims); this plugin is a page's own attachment, a person's notes from a
meeting that bears on THIS argument, with nothing to route anywhere.

  A PERSON WRITES IT           unlike chat/'s unruled "when does a live
                               session get kept", a meeting record is typed
                               by someone who was in the room — there is no
                               automatic-keep question here to leave open
  NO STORE, NO RANK            unlike pagex/task, a meeting is not read in
                               a person's chosen order; it is read by WHEN IT
                               HAPPENED, so the folder name (`<YYMMDD-HHMM>`)
                               is the only index and newest sorts first
  READ-ONLY VIEW, WRITABLE PEN the view lists what exists and writes
                               nothing but itself (plugview.py's own rule for
                               display/probe); `meeting-entry` is the one
                               door that lands new material, and it only ever
                               ADDS a folder, never edits or removes one —
                               a meeting is a record, not a list a person
                               curates afterward
"""
import re
import time
from pathlib import Path

from live.export import _VIEW, _esc

_STAMP = re.compile(r"^\d{6}-\d{4}")


class MeetingMixin:

    # ---- shared ground -------------------------------------------------
    def _meeting_dir(self, p):
        page_src, out_dir, board, err = self._export_target(p, "meeting")
        if err:
            return None, None, None, err
        return page_src, out_dir, board, None

    # ---- POST /_board/meeting-entry · the pen -----------------------------
    def meeting_entry(self, p):
        """{digest, transcript?, cast?}: a person's own record. The stamp is
        the SERVER clock, never the client's, so two people in different time
        zones land on the same board's own idea of "now" (the rule every
        other timestamped write in this engine already follows)."""
        page_src, out_dir, board, err = self._meeting_dir(p)
        if err:
            return None, err
        digest = (p.get("digest") or "").strip()
        if not digest:
            return None, "a meeting needs at least a digest: what it decided"
        transcript = (p.get("transcript") or "").strip()
        cast = (p.get("cast") or "").strip()
        stamp = time.strftime("%y%m%d-%H%M")
        folder = out_dir / stamp
        n = 1
        while folder.exists():
            n += 1
            folder = out_dir / ("%s-%d" % (stamp, n))
        folder.mkdir(parents=True)
        head = "# Meeting · %s\n" % stamp
        if cast:
            head += "cast: %s\n" % cast
        (folder / "digest.md").write_text(head + "\n" + digest + "\n",
                                          encoding="utf-8")
        if transcript:
            (folder / "transcript.md").write_text(transcript + "\n",
                                                   encoding="utf-8")
        url = self._meeting_render(page_src, out_dir)
        return {"ok": True, "folder": folder.name, "url": url}, None

    # ---- POST /_board/meeting · the view -----------------------------------
    def meeting_view(self, p):
        page_src, out_dir, board, err = self._meeting_dir(p)
        if err:
            return None, err
        url = self._meeting_render(page_src, out_dir)
        return {"ok": True, "url": url}, None

    def _meeting_render(self, page_src, out_dir):
        stem = page_src.stem
        kept = sorted((d for d in out_dir.iterdir()
                      if d.is_dir() and _STAMP.match(d.name)),
                     reverse=True)
        cards = []
        for d in kept:
            digest = d / "digest.md"
            transcript = d / "transcript.md"
            text = digest.read_text(encoding="utf-8", errors="replace") \
                if digest.is_file() else ""
            cast = ""
            body = []
            for ln in text.splitlines():
                m = re.match(r"^cast:\s*(.*)$", ln)
                if m:
                    cast = m.group(1).strip()
                    continue
                if ln.startswith("# "):
                    continue
                body.append(ln)
            digest_html = "".join(
                "<p>%s</p>" % _esc(x) for x in body if x.strip())
            when = "%s-%s-%s %s:%s" % (d.name[0:2], d.name[2:4], d.name[4:6],
                                       d.name[7:9], d.name[9:11])
            meta = "<span class='mut'>%s</span>" % _esc(when)
            if cast:
                meta += "<span class='mut'> · %s</span>" % _esc(cast)
            tl = ("<div class='mut'><a href='%s' target='_blank'>"
                 "transcript.md</a></div>"
                 % _esc(self._url_of(transcript))) if transcript.is_file() else ""
            cards.append(
                "<div class='card'><b>%s</b><br>%s%s%s</div>"
                % (_esc(d.name), meta, digest_html or
                   "<p class='mut'>no digest text</p>", tl))

        form = (
            "<div class='card'><b>＋ keep this meeting</b>"
            "<div class='pick'>"
            "<input id='mcast' placeholder='who was there (optional)'>"
            "<textarea id='mdigest' rows='4' placeholder="
            "'what it decided — the reading path, in your own words'>"
            "</textarea>"
            "<textarea id='mtranscript' rows='6' placeholder="
            "'raw exchange (optional, reference only)'></textarea>"
            "<button id='keepmeeting'>keep</button></div></div>")

        head = ("<div class='bar'><b>🗣 %s</b><span class='mut'>· %d meeting%s "
                "kept</span></div>"
                % (_esc(stem), len(kept), "" if len(kept) == 1 else "s"))

        script = """<script>
document.getElementById('keepmeeting').onclick = function () {
  var body = {digest: document.getElementById('mdigest').value,
              transcript: document.getElementById('mtranscript').value,
              cast: document.getElementById('mcast').value};
  fetch('/_board/meeting-entry', {method: 'POST',
    headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (!j.ok) { alert('\\u26a0 ' + (j.err || 'meeting-entry')); return; }
      location.reload();
    })
    .catch(function (e) { alert('\\u26a0 ' + e); });
};
</script>"""
        css = ("<style>"
               "body{padding:12px 16px}"
               "button{cursor:pointer;border:1px solid var(--line);"
               "background:var(--card);color:var(--fg);border-radius:6px;"
               "padding:6px 12px;font:500 12.5px -apple-system,sans-serif}"
               "input,textarea{border:1px solid var(--line);border-radius:6px;"
               "padding:6px 8px;background:var(--bg);color:var(--fg);"
               "font:13px -apple-system,sans-serif;width:100%;box-sizing:border-box}"
               ".bar{margin:0 0 12px}"
               ".bar b{font:600 15px ui-monospace,Menlo,monospace}"
               ".card{border:1px solid var(--line);border-radius:10px;"
               "padding:12px 16px;margin:0 0 12px;background:var(--card)}"
               ".card b{font:600 13px ui-monospace,Menlo,monospace}"
               ".pick{display:flex;flex-direction:column;gap:8px;margin-top:8px}"
               "</style>")
        # The form goes FIRST, since keeping a fresh record is the reason
        # anyone opens this tab; kept meetings read newest-first beneath it.
        view = out_dir / (stem + "-view.html")
        view.write_text(_VIEW.format(title=_esc(stem + " · meeting"),
                                     body=css + head + form
                                     + "".join(cards) + script),
                        encoding="utf-8")
        return self._url_of(view)
