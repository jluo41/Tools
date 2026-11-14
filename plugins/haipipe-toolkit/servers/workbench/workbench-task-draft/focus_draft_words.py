"""The draft Task page's words: its section names, state words, asks, verbs, captions and prompts."""
from __future__ import annotations

import re

# Write and Revise are one view, Draft: the sentence board, each sentence with its cards, comments and scores (JL 261113:
# "merge the Revise and Write into one View, just call it Draft"); the files keep the two steps (ds.STEPS, DRAFT)
WORK = (("plan", "1 · Plan"), ("draft", "2 · Draft"), ("evidence", "3 · Evidence"), ("display", "4 · Display"))
DRAFT = ("2 · Write", "5 · Revise")


STATE_WORD = {"done": "done", "next": "next", "sign": "sign", "asked": "asked", "send": "send", "optional": "optional",
              "pass": "pass {k}", "todo": "later", "early": "before the sign"}


WAITS = ("sign", "asked", "send", "pass", "early")            # a word the person acts on, shown in the warn colour


# what a step waits for, as the Interactions rows read (JL 261102: "make it the same style as the interactions"):
# its name, then what it waits for, then the button
# what the person does is the row's button (Sign the plan); how, its hover (r02: "✅ on approved: in the draft" read as an
# instruction line)
ASKS = {"1 · Plan": {"sign": ("Plan", "waits for your sign")},
        "3 · Evidence": {"asked": ("Evidence asks", "waits for you: tick each ask, and settle each open point")},
        "4 · Display": {"sign": ("Displays", "waits for you: write <code>accepted:</code> in each display's README")},
        "5 · Revise": {"pass": ("Revise cards", "waits for you: accept or reject each card")},
        "2 · Draft": {"pass": ("Revise cards", "waits for you: accept or reject each card")},
        "Delivery": {"send": ("Built files", "waits for you: check them, then mark the send in <code>delivery.md</code>")}}


# the verb on a step's waiting row, and how it is done (its hover)
SIGN = {"1 · Plan": ("Sign the plan", "Read the plan, then type ✅ on approved: in the draft; no skill signs."),
        "5 · Revise": ("Open the cards", "Accept or reject each card."), "2 · Draft": ("Open the cards", "Accept or reject each card."), "3 · Evidence": ("Open the draft", "Tick each ask.")}


# the button on each prompt: the step's own verb, so the row says what the copy is for
VERBS = {"plan": "Copy prompt: plan", "write": "Copy prompt: write", "evidence": "Copy prompt: find evidence",
         "display": "Copy prompt: make the displays", "revise": "Copy prompt: revise", "studio": "Copy prompt: talk and sketch",
         "delivery-build": "Copy prompt: build", "delivery-render": "Copy prompt: render the pages",
         "delivery-send": "Copy prompt: check", "delivery-back": "Copy prompt: read back"}


# the Task's Runs each step makes, by the start of their names (haipipe-draft's Run families)
RUN_PREFIX = {"1 · Plan": ("run-structure", "run-context", "run-scratch"),
              "2 · Write": ("run-section", "run-write", "run-paragraph"),
              "3 · Evidence": ("run-value", "run-citation", "run-evidence"),
              "4 · Display": ("run-display",),
              "5 · Revise": ("run-revise", "run-paragraph", "run-section"),
              "2 · Draft": ("run-section", "run-write", "run-paragraph", "run-revise"),
              "Delivery": ("run-delivery", "run-check")}


CAPTIONS = {"plan": "The plan: its paragraphs and their points, before the sentences.",
            "write": "The text, and your own sentences typed beside it.",
            "evidence": "The text beside the evidence for each sentence, and what is still open.",
            "display": "The Tables and Figures the text calls, each beside its sentence.",
            "revise": "The text beside its review cards: accept or reject each change.",
            "draft": "Each sentence with its cards, comments and scores: accept, reject or edit it in place.",
            "runs": "Every Run of this Task.",
            "pdf": "The Section as the LaTeX build prints it.", "web": "The Section as a web page.",
            "word": "The Word file, through the PDF the build writes beside it.",
            "files": "Every built file, the sends, the Runs, and the prompts that build them.",
            "paper": "The whole paper, as the LaTeX build prints it.", "supplement": "The supplement, through its PDF twin.",
            "mindmap": "The content as a map: each part, then what it holds.",
            "text": "Each sentence beside its evidence, its changes and the review's notes.",
            "status": "Where each step stands, and what waits for you.",
            # the Interactions views say what they hold, no instruction (r03: "…; each opens the same form its Work row opens")
            "all": "Everything asked at this page or below.", "waiting": "What waits for your answer.",
            "answered": "What you have answered."}


PROMPT = re.compile(r'<details class=run-prompt-box open><summary>(.*?) <button type=button class="run-copy work-act" '
                    r'data-copy="([^"]*)"(?: data-tail="([^"]*)")?>Copy prompt</button></summary>.*?'
                    r'data-key="([^"]*)"', re.S)


INPUT = re.compile(r"<h4>Input</h4>(<table.*?</table>)", re.S)


# the folds draft_steps writes by hand (an example, an Evidence card, the open points, a display, the canvas, the
# Scratch editor), each with no fold inside: on this page each is a section under its heading
FOLD = re.compile(r'<details class="topic work-task(?: items-step)?"(?: open)?><summary>(.*?)</summary>(.*?)</details>', re.S)


LAZY = re.compile(r'<iframe class=st-frame title="([^"]*)" data-src="([^"]*)"[^>]*></iframe>')


# the common workbench width, the title at the same x as every page (JL 261031, b10-s33-D06: paper pages use the
# common width, no verb after the section word); only the draft's own rules stay here
WIDE = """<style>.section-views{flex-wrap:wrap}.section-views a{white-space:nowrap}
.pm-role:empty::before{content:"no role";color:var(--muted);font-size:11px}
.rv-split.wr-split{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.wr-split .rv-right iframe,.fd-sec iframe.space-frame{display:block;width:100%}
</style>"""
