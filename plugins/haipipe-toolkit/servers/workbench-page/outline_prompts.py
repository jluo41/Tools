"""Read-only, scope-aware prompts for the Draft Space. Never allocates a Run.

Three copy buttons, named by the Run they ask for (JL 260922: "I prefer to call
them run-structure, run-section, and run-paragraph"): `run-structure` on the
Structure card, `run-section` on each division, `run-paragraph` on each
paragraph. The copied text is short on purpose (JL: "they should be more
concise"): the door skill, the addresses, the matching Run and its next move,
any blocker, and a Feedback line. The agent reads the Outline and runtime
itself; the prompt no longer quotes the contract back at it.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from src.outline_version import latest_outline
from src.plan_shape import global_paragraph_mapping
from live.runs import local_runs

RUN_NAMES = {"structure": "run-structure", "section": "run-section",
             "paragraph": "run-paragraph"}
IDENTITY = {"structure": "rp-struct-NN", "section": "rp-sec-NN",
            "paragraph": "rp-para-NN_Pxx[-Pyy]"}
NEXT = {
    "Waiting": "resume: present the saved candidate, apply the Feedback below or ask for it.",
    "Running": "resume the unfinished Step after reconciling the saved candidate and journal.",
    "Ready": "begin the next draft → review → revise Step inside this fixed scope.",
    "Done": "closed: check the request against its frozen scope; a revisit reopens this Run "
            "in a new Version, a new goal needs its own Run.",
}


class RunPrompts:
    def __init__(self, page: Path, root: Path | None = None,
                 board_path: str = "", page_path: str = ""):
        self.page = page
        self.root = root or page.parent
        self.board_path = board_path.strip() or "current Board"
        self.page_path = page_path.strip() or self.path(page)
        self.rows = local_runs(page)
        self.plan = latest_outline(page.parent / "outline", page.stem)
        self.text = self.plan.read_text(encoding="utf-8") if self.plan else ""
        self.mapping_error = ""
        try:
            self.paragraphs = global_paragraph_mapping(self.text)
        except ValueError as exc:
            self.paragraphs = {}
            self.mapping_error = str(exc)

    def path(self, path):
        if path is None:
            return "none yet"
        try:
            return str(Path(path).relative_to(self.root))
        except ValueError:
            return str(path)

    def matches(self, row, kind, target):
        run = row["run_id"]
        if kind == "structure":
            return bool(re.fullmatch(r"rp-struct-\d{2,}", run))
        if kind == "section":
            scopes = re.findall(r"(?<![A-Za-z0-9])C\d+(?![\d.])",
                                row.get("target", "") + " " + row.get("target_scope", ""))
            return bool(re.fullmatch(r"rp-sec-\d{2,}", run) and set(scopes) == {target})
        match = re.fullmatch(r"rp-para-\d{2,}_P(\d+)(?:-P(\d+))?", run)
        if not match or target not in self.paragraphs:
            return False
        index = int(self.paragraphs[target].split(".P")[1])
        return int(match[1]) <= index <= int(match[2] or match[1])

    def excerpt(self, kind, target):
        """Only a paragraph quotes its Outline block; the others name the file."""
        if kind != "paragraph":
            return ""
        match = re.search(r"(?m)^### " + re.escape(target) + r"\b.*$", self.text)
        if not match:
            return ""
        rest = self.text[match.start():]
        offset = rest.find("\n") + 1
        end = re.search(r"(?m)^#{1,3} ", rest[offset:]) if offset else None
        return rest[:end.start() + offset].strip() if end else rest.strip()

    def prompt(self, kind, target="Page"):
        scope = target
        if kind == "paragraph" and target in self.paragraphs:
            scope += " (Page-global P%02d)" % int(self.paragraphs[target].split(".P")[1])
        matches = [row for row in self.rows if self.matches(row, kind, target)]
        active = [row for row in matches if row["status"] != "Done"]
        # Multiple open candidates are an ambiguity, never a sorting decision.
        chosen = active[0] if len(active) == 1 else None
        if not active and matches:
            chosen = max(matches, key=lambda row: int(
                re.search(r"rp-(?:struct|sec|para)-(\d+)", row["run_id"])[1]))
        board = "standalone Page" if self.board_path == "/" else self.board_path
        lines = [
            "/haipipe-page %s %s" % (RUN_NAMES[kind], scope),
            "Board: %s · Page: %s" % (board, self.page_path or self.path(self.page)),
            "Outline: " + self.path(self.plan),
        ]
        if self.mapping_error:
            lines.append("Address blocker: %s. Resolve it against the accepted Structure "
                         "before selecting or allocating a Run." % self.mapping_error)
        elif kind == "paragraph" and self.paragraphs.get(target, target) != target:
            lines.append("Legacy address: the Page-global P index is derived from reading order. "
                         "Confirm it against the accepted Structure and frozen Run target before "
                         "editing; report a conflict, never renumber the source.")
        structure_closed = any(row["run_id"] == "rp-struct-01" and row["status"] == "Done"
                               for row in self.rows)
        if kind != "structure" and not structure_closed:
            lines.append("Blocker: rp-struct-01 is not closed. Settle the Structure first; "
                         "do not allocate or start Section/Paragraph writing.")
        if len(active) > 1:
            lines.append("Run selection is ambiguous: %s · ask which Run to resume before changing anything."
                         % ", ".join(row["run_id"] for row in active))
        elif chosen:
            lines.append("Run: %s · %s · %s · %s" % (
                chosen["run_id"], chosen["status"],
                chosen.get("version") or "no version", chosen.get("step") or "no step"))
            lines.append("Next: " + NEXT.get(
                chosen["status"], "inspect the blocker and incomplete records, then report the recovery action."))
            if chosen.get("audit"):
                lines.append("Recorded blockers: " + "; ".join(chosen["audit"]))
        else:
            lines.append("Run: none yet · next canonical %s, allocated by the owner only after its "
                         "prerequisites hold." % IDENTITY[kind])
        lines.append("Rule: read the source and runtime first; touch only this scope; copying this "
                     "text starts nothing.")
        excerpt = self.excerpt(kind, target)
        if excerpt:
            lines += ["", "Selected Outline:"] + ["> " + line for line in excerpt.splitlines()]
        lines += ["", "Feedback:", ""]
        return "\n".join(lines)

    def button(self, kind, target="Page"):
        name = RUN_NAMES[kind]
        label = "Copy %s prompt" % name
        return ('<button type="button" class="run-prompt-copy" aria-label="%s" '
                'title="%s" data-run-prompt="%s">⧉ %s</button>' % (
                    html.escape(label, quote=True), html.escape(label, quote=True),
                    html.escape(self.prompt(kind, target), quote=True), name))


def assets_html():
    return r'''<style>
.run-prompt-copy{font:500 10.5px/1.2 ui-monospace,Menlo,monospace;color:var(--mut);background:transparent;border:1px solid var(--line);border-radius:4px;padding:2px 6px;margin-left:auto;cursor:pointer;white-space:nowrap}
.run-prompt-copy:hover,.run-prompt-copy:focus-visible{border-color:var(--acc);color:var(--acc);outline:none}
.structure-prompt{display:flex;justify-content:flex-end;margin:4px 0}
.run-prompt-status{font:12px system-ui;color:var(--mut);padding:2px 0;min-height:1em}
.run-prompt-status:empty{display:none}
.run-prompt-fallback{box-sizing:border-box;width:100%;min-height:9rem;font:12px/1.5 monospace}
@media(pointer:coarse){.run-prompt-copy{min-height:28px;padding:4px 8px}}
</style><div class="run-prompt-status" role="status" aria-live="polite"></div><script>
(function(){
 if(window.__draftPromptCopy)return; window.__draftPromptCopy=true;
 document.addEventListener('click',async function(event){
  var button=event.target.closest('.run-prompt-copy'); if(!button)return;
  event.preventDefault();event.stopPropagation();
  var text=button.dataset.runPrompt,ok=false;
  try{if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(text);ok=true;}}catch(e){}
  if(!ok){
   var active=document.activeElement,ta=document.createElement('textarea');ta.value=text;ta.readOnly=true;
   ta.style.cssText='position:fixed;left:-99999px;top:0';document.body.appendChild(ta);ta.select();
   try{ok=document.execCommand('copy');}catch(e){}ta.remove();if(active)active.focus({preventScroll:true});
  }
  var status=document.querySelector('.run-prompt-status');
  if(status)status.textContent=ok?'Copied '+button.textContent.replace('⧉','').trim()+'. Paste it to your agent.':'Could not copy. Use the preview below.';
  if(ok){var oldPreview=document.querySelector('.run-prompt-fallback');if(oldPreview)oldPreview.remove();}
  if(!ok){var preview=document.querySelector('.run-prompt-fallback');if(!preview){preview=document.createElement('textarea');preview.className='run-prompt-fallback';preview.readOnly=true;preview.setAttribute('aria-label','Prompt to copy manually');status.after(preview);}preview.value=text;preview.focus();preview.select();}
 });
})();
</script>'''
