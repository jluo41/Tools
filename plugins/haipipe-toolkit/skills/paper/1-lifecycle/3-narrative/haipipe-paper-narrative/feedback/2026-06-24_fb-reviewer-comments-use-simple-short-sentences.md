---
status: fixed
created: 2026-06-24
fixed_in: "haipipe-paper-narrative v1.5.0"
context: haipipe-paper narrative stage on Paper-Personality2Opioid-MISQ2026; after adding per-beat reviewer-comment lines (the new \fb{name}{status}{feedback}{resolution} macro carrying Ritu Agarwal's 0622 comments), the "how we solved it" resolution text came out as long run-on sentences with semicolons and parentheticals
---
"the sentence you used is really long and hard to read, could you use the simple sentence style to explain or describe?"

Distilled ask:
- The "how we addressed it" text in per-beat reviewer comments (and narrative comment text generally) must be written in SHORT, PLAIN sentences. No long run-on sentences chained by semicolons, no stacked parentheticals.
- Pattern: one idea per sentence; 2-4 short sentences beat one long compound one. Lead with the action taken, then the open item.
- Before/after (resolution text for a \fb comment):
  - BEFORE (rejected): "re-weighted the spine + this contribution beat so the main story is the message-derived LLM signal predicting physician behavior; opioids are the application, not the headline."
  - AFTER (wanted): "Reframed the spine and this beat. The main story is now the LLM signal predicting physician behavior. Opioids are just the application."

How to apply (narrative stage, and any comment text the skill writes):
1. When authoring the \fb resolution (or any \rev / footer comment), use short declarative sentences. One idea each.
2. Drop adjectives, hedging, and parentheticals; compress rather than nest. Split a compound sentence into two short ones rather than joining with ";".
3. Keep the reviewer's quoted feedback verbatim (it is their words); only the resolution prose follows the short-sentence style.
4. This is the same readability discipline already required for the pitch (ref/pitch-readability.md) and for chat replies; carry it into narrative comment text.

Why:
- Long compound resolution lines are hard to scan, especially in \footnotesize. The comment thread exists to track progress at a glance; short sentences make the status and the action readable in one pass.

Where it touches:
- haipipe-paper-narrative: the per-beat comment authoring step (\fb resolutions, \rev comments, footer ledger lines) should follow the short-plain-sentence rule. Relates to the existing readability rules in pitch and the workspace style memories (compress-not-split, one-idea-per-sentence, no-ai-voice).

Fix: v1.5.0 (2026-06-24). Added a "Comment text is short and plain" rule to SKILL.md Rules (covers \rev, \fb resolutions, footer; quoted \fb feedback stays verbatim). Added a COMMENT STYLE note to ref/narrative-template.tex. The Output section part-4 description now states all comment text uses short plain sentences, one idea each.
