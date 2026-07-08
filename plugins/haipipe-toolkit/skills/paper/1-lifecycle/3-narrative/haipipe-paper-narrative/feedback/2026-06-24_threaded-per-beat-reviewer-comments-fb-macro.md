---
status: fixed
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: haipipe-paper narrative stage on Paper-Personality2Opioid-MISQ2026; user asked to record an external reviewer's (Ritu Agarwal) feedback in the narrative so progress is tracked. First attempt added a single summary footer line; user corrected that it should be threaded onto each beat.
fixed_in: "haipipe-paper-narrative v1.5.0"
regressed: ""
---
The narrative should support EXTERNAL reviewer comments threaded onto the beat each one concerns, like comments on a post. The user's words: "It is more like the post, and people leave the comments" and "you should have the macro for user, and then we can put the user name, and then put the user's feedback, and how we solved it."

Distilled ask:
- A single summary footer line that lists all reviewer comments is NOT what is wanted. Each reviewer comment should sit UNDER the specific beat it is about (post + comments model), next to the existing internal interrogation comment.
- Provide a dedicated macro carrying four things: reviewer NAME, a STATUS, their FEEDBACK (verbatim), and HOW WE SOLVED IT. Implemented this session as:
  `\fb{reviewer name}{status}{their feedback, verbatim}{how we addressed it}`
  rendered in a distinct color (maroon) so it reads apart from the gray internal `\rev` interrogation comment.
- Status vocabulary used: [done | part | open]. This lets the narrative double as a progress tracker for an external review pass.
- Keep the reviewer's quoted feedback verbatim (their words); only the "how we solved it" text is authored by us (and must follow the short-plain-sentence rule, see the sibling file 2026-06-24_fb-reviewer-comments-use-simple-short-sentences.md).
- A comment with no single home beat (e.g. "see comments in Overleaf") can stay in the footer ledger; everything else threads onto a beat.

How to apply (narrative stage):
1. Add a reviewer-comment macro to the narrative template preamble, parallel to the existing `\rev` interrogation macro: `\fb{name}{status}{feedback}{resolution}`, distinct color.
2. When an external review (a co-author, advisor, or referee) comes in, attach each comment to the beat it concerns via `\fb`, with status + how-addressed; do not collapse them into one footer paragraph.
3. Keep a slim footer pointer that says the threaded reviewer lines exist + carries any comment that has no single beat.
4. This is for EXTERNAL named-reviewer feedback; it is distinct from the internal subagent interrogation (`\rev`) covered by 2026-06-22_narrative-points-need-subagent-reviewed-inclusion-comments.md (sibling, related, different topic).

Why:
- A footer summary forces the reader to map a comment back to the beat it is about. Threading the comment onto its beat (with name + verbatim feedback + resolution + status) makes a review pass trackable at the point where the change must happen.

Where it touches:
- haipipe-paper-narrative: template preamble (add `\fb` macro) + the narrative authoring step (thread external reviewer comments per beat, keep a slim footer pointer).

Fix: v1.5.0 (2026-06-24). ref/narrative-template.tex now defines \fb{name}{status}{feedback}{resolution} (maroon cFb) after \rev, with a doc-comment, a worked example under the first Intro beat, and an "External review (<name>, <date>)" footer line for no-beat comments. SKILL.md gained an "External Reviewer Comments (\fb, threaded per beat)" section, a Rules entry, and an Output part-4 mention. Template recompiles clean.
