---
status: open
created: 2026-06-24
context: display stage; after rendering a figure/table, we kept finding render defects (zero-width CI, overflow, ugly layout, conceptual muddle) only by eyeballing the PDF
updated: 2026-06-24
occurrences: 2
fixed_in: ""
---
The display stage needs a REVIEW LOOP on the COMPILED / rendered figures and tables, not just on the plan. Two parts JL asked for:

1. A REVIEW AGENT for compiled displays (builder != judge). After a figure/table is rendered, an independent agent READS the compiled asset/preview PDF and judges: does it render correctly (no overflow, no overlap, no zero-width CI, labels legible), does it convey its claim in five seconds, does it match the narrative beat + venue conventions, and is it not ugly? Returns a verdict + concrete fixes. This is the visual analog of the per-display self-check (which judged the PLAN); this one judges the RENDER. (Today this was done ad-hoc by the main agent reading the PDF; formalize it as an agent so it is independent and repeatable.)

2. An ASCII PREVIEW + comment elicitation step. After rendering, show each figure/table as a /diagram-ascii preview in chat so JL can review and comment WITHOUT opening the PDF, then capture JL's comments as `%% {JL}:` lines in 0-lifecycle/4-display.tex (per the comment-location convention). The ASCII preview is the fast human-in-the-loop; the review agent is the automated QA. Run both before the display stage gate.

How to apply (haipipe-paper-display revision): add a "review rendered displays" step to the stage that (a) dispatches a compiled-display review agent over each main/supplement unit and (b) renders an ASCII preview of each and asks JL for comments. Gate stage-close on both. Likely needs a new registered agent (e.g. display-render-reviewer-agent) that can read PDFs. Related: [[feedback_narrative_points_subagent_review_smallfont]] (拷打-every-unit), [[feedback_display_comments_in_lifecycle_4display]] (comment location), [[feedback_communicate_via_diagram_ascii]] (ASCII previews).

## Recurrences
- 2026-06-24 (digest, Display-for-Opioid-JAMA): "figure 2 is so urgly, please use modern python code to rerun it ... and for the table 2, it is overflowed, please think about how to fix it as well."; "how did you generated the Figure 2??? why it is grey and white, could you make it more modern?"; "关于 Figure 2: 为什么我们图下面也有那么多字？为什么我们有两个 block（一个蓝色一个灰色），它的意义是什么？"; "you see the interaction term overstacked, how could we rearrage it?"
