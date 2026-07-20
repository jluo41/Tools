---
status: fixed
created: 2026-06-22
context: haipipe-paper narrative stage on Paper-Personality-Opioid-MedJournal; after adding self-authored "Why (job)" lines to each narrative point, the user found them limp ("软绵无力") and the per-section content too thin
fixed_in: "haipipe-paper-narrative v1.3.0"
---
"感觉每个部分说的太少了，不过可以之后再更新这个 skill 的 writing style。这个 why 有点软绵无力，感觉需要 call subagent 去 review 每个 items，看看要不要放到这里，然后把 comments 用小字加进去。我们就这样做吧。"

Distilled ask:
- The per-point inclusion justification ("why this beat is here / must it be here") must NOT be weakly self-authored by the drafting agent. Self-authored "why" lines come out limp and circular. Instead, CALL A SUBAGENT to review each narrative item independently: for each point decide keep / move / demote-to-Supplement / cut against the paper's spine, primary claim, and target venue. The reviewer's judgment replaces the limp self-authored why.
- Render the reviewer's verdict + comment in SMALL FONT (\footnotesize / \small) attached to each point, so the narrative carries an independent editorial judgment per beat, visibly subordinate to the beat itself.
- Per-section narrative CONTENT is currently too thin. The fix is a richer narrative writing style, but that is DEFERRED: update the narrative skill's writing-style guidance later, not in the current pass.

How to apply (narrative stage):
1. Keep the per-point structure: name + description + [readiness color].
2. Dispatch a subagent (ONE reviewer that sees all points, so it can also judge flow / redundancy / gaps) to return, per item: verdict {keep | move→where | demote→Supplement | cut} + one sharp venue-aware comment. The drafting agent does not self-author these.
3. The drafting agent integrates the returned comments in small font + recompiles (compile-every-stage stays with the main agent, not the subagent; the subagent does not edit files).
4. Defer thin-content expansion to a later narrative-skill writing-style update.

Why:
- A drafting agent justifying its own inclusions produces soft, circular "why" lines. An independent reviewer judging each beat's necessity (keep/move/demote/cut) is sharper and catches beats that do not earn their place.
- Small font keeps the editorial comment visibly subordinate to the beat.

Where it touches:
- haipipe-paper-narrative: add a "review each point's inclusion via subagent, render comments in small font" step; the drafting agent does not self-author necessity justifications.
- narrative skill writing-style guidance: per-section content is too thin (DEFERRED enhancement, not this pass).

Fix:
