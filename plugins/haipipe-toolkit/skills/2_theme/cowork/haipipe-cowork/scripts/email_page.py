"""A cowork email draft as a page to copy from: delivery/<date>-<what>/<...>-draft.md -> <...>-draft.html.

The draft is written by hand and is the one place its words live:

    # <title>                         the page's heading
    status: draft
    How: <how to send it>             shown under the heading
    To: ... / Cc: ... / Subject: ...  each in a box with a Copy button
    Attach: a.png; b.pdf              the files, all in the draft's folder (refused if one is missing)
    ---
    the body: paragraphs split by a blank line; "1. " numbered items and "- " bullets; a line that is
    not an item continues the one above it; an item indented under another is nested one level; the
    last paragraph is the sign-off and keeps its lines

Each box copies as rich text and plain text, so Outlook keeps the paragraphs, the numbers and the
bullets. Numbers and bullets are written as text, not <ol>/<ul>, so a plain paste keeps them too
(the shape b12_epic_streaming's first reply to PACE used, JL 261009: "I want the format like this").

    python email_page.py <draft.md>      writes <draft>.html beside it
"""
import html
import re
import sys
from pathlib import Path

ITEM = re.compile(r"^(\s*)(\d+\.|-) (.*)$")


def parts(draft):
    """(title, head, blocks): the heading, the header lines {To, Cc, Subject, Attach, How, ...}, and the
    body as blocks: ("p", text), ("item", level, marker, text) or ("sign", [lines])."""
    text = Path(draft).read_text(encoding="utf-8")
    top, _, rest = text.partition("\n---\n")
    title = next((l[2:].strip() for l in top.splitlines() if l.startswith("# ")), Path(draft).stem)
    head = {k.strip(): v.strip() for k, sep, v in (l.partition(": ") for l in top.splitlines()
                                                   if not l.startswith("#")) if sep and " " not in k.strip()}
    paras = re.split(r"\n\s*\n", rest.strip())
    blocks = []
    for k, para in enumerate(paras):
        lines = para.splitlines()
        if k == len(paras) - 1:
            blocks.append(("sign", [l.strip() for l in lines]))
            continue
        cur = None
        for line in lines:
            m = ITEM.match(line)
            if m:
                cur = ["item", 0 if len(m.group(1)) < 2 else 1, "•" if m.group(2) == "-" else m.group(2), m.group(3).strip()]
                blocks.append(cur)
            elif cur is None:
                cur = ["p", line.strip()]
                blocks.append(cur)
            else:
                cur[-1] = (cur[-1] + " " + line.strip()).strip()
        if blocks and blocks[-1][0] == "item":
            blocks[-1].append("last")                     # a list's last item keeps the paragraph gap
    return title, head, [tuple(b) for b in blocks]


def body_html(blocks):
    e = html.escape
    out = []
    for b in blocks:
        if b[0] == "p":
            out.append(f'<p style="margin:0 0 11pt 0">{e(b[1])}</p>')
        elif b[0] == "item":
            _, level, marker, words, *last = b
            left, gap = (24 if level == 0 else 48), (11 if last else 4)
            out.append(f'<p style="margin:0 0 {gap}pt {left}pt;text-indent:-18pt">{e(marker)}&nbsp;&nbsp;{e(words)}</p>')
        else:
            out.append('<p style="margin:0 0 11pt 0">' + "<br>".join(e(r) for r in b[1]) + "</p>")
    return "".join(out)


def page(draft, made_by="this folder's build.py"):
    """The email as a page: each part in a box with a Copy button."""
    title, head, blocks = parts(draft)
    e = html.escape
    def field(label, key, value):
        return (f'<div class="row"><div class="label">{label}</div><div class="box" id="{key}">{e(value)}</div>'
                f'<button onclick="copyBox(\'{key}\', this)">Copy</button></div>')
    files = [f.strip() for f in head.get("Attach", "").split(";") if f.strip()]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<style>
  :root {{ --ink:#1e1e1e; --muted:#666; --line:#d0d0d0; --bg:#ffffff; --panel:#f6f6f6; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 -apple-system, "Segoe UI", Arial, sans-serif; }}
  main {{ max-width:860px; margin:0 auto; padding:24px 16px 48px; }}
  h1 {{ font-size:20px; margin:0 0 4px; }}
  .note {{ color:var(--muted); font-size:13px; margin:0 0 20px; }}
  .row {{ display:grid; grid-template-columns:72px 1fr auto; gap:10px; align-items:start; margin:0 0 10px; }}
  .label {{ font-weight:600; padding-top:7px; }}
  .box {{ border:1px solid var(--line); border-radius:6px; padding:6px 10px; background:var(--panel); word-break:break-word; }}
  button {{ font:inherit; font-size:13px; padding:6px 14px; border:1px solid var(--ink); border-radius:6px;
           background:#fff; color:var(--ink); cursor:pointer; min-width:84px; }}
  button.done {{ background:var(--ink); color:#fff; }}
  #body {{ background:#fff; padding:14px 16px; font-family:Aptos, Calibri, Arial, sans-serif; font-size:11pt; color:#000; }}
  ul.files {{ margin:6px 0 0; padding-left:20px; }}
  @media (max-width:560px) {{ .row {{ grid-template-columns:1fr; }} .label {{ padding-top:0; }} }}
</style></head><body><main>
<h1>{e(title)}</h1>
<p class="note">How: {e(head.get("How", ""))} Made by {e(made_by)} from {e(Path(draft).name)}: to change a word, edit
that file and rerun it. Paste each part with its Copy button, then attach the files below from this folder.</p>
{field("To", "to", head.get("To", ""))}
{field("Cc", "cc", head.get("Cc", ""))}
{field("Subject", "subject", head.get("Subject", ""))}
<div class="row"><div class="label">Body</div>
<div class="box" id="body">{body_html(blocks)}</div>
<button onclick="copyBox('body', this)">Copy</button></div>
<div class="row"><div class="label">Attach</div><div class="box"><ul class="files">
{"".join(f"<li>{e(f)}</li>" for f in files) or "<li>nothing</li>"}
</ul></div><div></div></div>
</main>
<script>
function copyBox(id, btn) {{
  const el = document.getElementById(id), range = document.createRange(), sel = window.getSelection();
  range.selectNodeContents(el); sel.removeAllRanges(); sel.addRange(range);
  let ok = false;
  try {{ ok = document.execCommand("copy"); }} catch (err) {{ ok = false; }}
  if (ok) sel.removeAllRanges();
  btn.textContent = ok ? "Copied" : "Now press Cmd+C";
  btn.classList.toggle("done", ok);
  setTimeout(() => {{ btn.textContent = "Copy"; btn.classList.remove("done"); }}, 2000);
}}
</script></body></html>
"""


def write(draft, made_by="this folder's build.py") -> Path:
    """Write <draft>.html beside the draft; refuse when an Attach: file is not in the draft's folder."""
    draft = Path(draft)
    _, head, _ = parts(draft)
    absent = [f.strip() for f in head.get("Attach", "").split(";") if f.strip() and not (draft.parent / f.strip()).exists()]
    if absent:
        sys.exit(f"not written: the draft's Attach: line names files not in {draft.parent.name}/: " + ", ".join(absent))
    out = draft.with_suffix(".html")
    out.write_text(page(draft, made_by), encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(write(sys.argv[1], "haipipe-cowork scripts/email_page.py"))
