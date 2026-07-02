# Prose Quality Rules (Universal)

Rules that apply to ALL prose artifacts in the paper lifecycle: seed, claims, pitch, narrative, display captions, section prose. Any phase worker that touches prose reads this file. Venue-specific norms (word budget, tone, section arc) live in `_venue/playbook-*/style-profile.md` and override these where they conflict.

Sourced from JL feedback across multiple sessions. These are non-negotiable preferences, not suggestions.

---

## Sentence rules

- **One idea per sentence.** Don't bundle method + RQ or claim + interpretation. Split into two complete sentences even if tightly related.
- **No em-dashes.** Never use `---` or `—` anywhere. Use commas, colons, or parentheses instead.
- **Compress, don't split.** For long sentences, tighten by dropping adjectives/parentheticals/hedging. Do NOT split into many fragments. Fewer words > more sentences.
- **Short plain academic sentences.** No buzzword stacks, no parenthetical name-explosions, no italics-on-nouns. Write like a confident researcher, not a press release.
- **No AI voice.** Never use: Furthermore, Moreover, Additionally, delve, utilize, underscore, landscape, tapestry, multifaceted, crucial, pivotal, groundbreaking, innovative, cutting-edge, comprehensive, holistic, robust, novel, significant, transformative. If the sentence reads like ChatGPT wrote it, rewrite it.
- **Use verified numbers.** Prefer concrete verified numbers (e.g., "r = 0.61") over vague qualifiers ("higher", "moderate"). Strip numbers only if unverifiable.
- **Each sentence carries its own weight.** If removing a sentence wouldn't confuse the reader, the sentence doesn't belong.

## Paragraph rules

- **≤6 sentences per paragraph.** Hard ceiling. If a paragraph needs more, split it into two paragraphs with distinct jobs.
- **Each paragraph has one clear job.** The banner point (`% Para [id]`) must match what the paragraph actually does. If you can't state the job in one short phrase, the paragraph is doing too much.
- **Good transitions.** The first sentence of each paragraph should connect to the previous paragraph. The reader should never wonder "why are we talking about this now?"
- **Preview line is a scan hook.** The parenthetical preview under each paragraph heading is one short line (~80-120 chars), not a mini-abstract. Concept name + one distinguishing phrase.

## Structure rules

- **Pn.Sn markers on every sentence.** Every sentence in tex gets a `%% ---- Pn.Sn ----` marker. P restarts at P1 per file. S restarts per paragraph.
- **Outline ↔ tex must stay synced.** When the outline changes, the tex changes. When the tex changes, the outline changes. Stale sync is a defect.
- **Banner points match content.** Every `% Para [id]` banner accurately describes its paragraph. After editing, re-read the banner and update if the paragraph's job shifted.

## Comment rules

- **Preserve JL comments verbatim.** Never compress, summarize, translate, or replace `> JL:` or `%% Comments: {JL}` lines. Keep them exactly as written, even when applying the edit they request.
- **One-line CC responses.** When replying to JL inline comments, keep the response to ONE line. Multi-line response blocks make the file unreadable.
- **No elaborate tagging.** Don't add (done)/(old) tags on every comment. Focus effort on prose changes.

## POLISH phase behavior

POLISH applies these rules automatically. The agent does not stop for human review during POLISH. There is no comment-first protocol (no "Round 1 comments, wait for human, Round 2 apply"). The agent reads the prose, applies the rules below directly, and moves on. Human review of the polished prose happens in CHECK, where the human can add `> JL:` comments and restart POLISH if needed.

## What NOT to do

- **Don't explain what the code does** in comments. Well-named identifiers already do that.
- **Don't reference the current task or fix** in comments ("added for the Y flow", "handles the case from issue #123"). That belongs in the commit message.
- **Don't produce prose without understanding.** Every sentence must have a clear purpose: what does it DO for the reader and WHY. Production without understanding (知其然不知其所以然) is the root cause of bad writing.
- **Don't wholesale-rewrite silently.** Illuminate content + elicit user's taste before drafting. Loop = illuminate → elicit → draft → confirm.
- **Don't use comment-first protocol in POLISH.** POLISH applies rules directly. Human review happens in CHECK.
