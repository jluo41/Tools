---
status: fixed
created: 2026-06-22
context: whole lifecycle flow (every stage skill seed/pitch/claims/narrative/display/minimap + haipipe-paper-enter console); felt during the seed re-walk on Paper-Personality-Opioid-MedJournal, where the agent rewrote 0-seed.tex wholesale without first teaching the user the content or drawing out their judgment
fixed_in: "paper ref/stage-illuminate.md + all stage skills v2.0.0"
---
I think the problem here is you didn't ask and explain and illuminate the users about this paper, paper need to internalize the content and give their tastes. do you understand? this part is not included in this stage, this should be in every stage of the haipipe-paper's lifecycle and this should be very very important.

Distilled ask:
- Producing the stage artifact is not enough. Before/while drafting, the agent must EXPLAIN and ILLUMINATE the stage content to the user (what this stage says about the paper, why, the trade-offs), and ASK for the user's judgment, so the user INTERNALIZES the content and can inject their own TASTE. The paper is the user's; the agent is drafting on their behalf, not deciding for them.
- This is a participatory / Socratic requirement, NOT just a confirm-to-advance gate. The agent currently jumps straight to producing the artifact (e.g. rewrote 0-seed.tex in one shot) and then asks "confirm to advance?". That skips the middle: educating the user and eliciting their preferences DURING the stage.
- It applies to EVERY stage (seed, pitch, claims, narrative, display, minimap), not just one. The user marked it "very very important."

Why this matters:
- A paper carries the author's taste and voice. If the agent silently fills each stage with its own choices, the user never owns the content, cannot defend it, and the paper reads as generated rather than authored.
- Internalization is the point of the lifecycle, not just artifact completeness. The user needs to UNDERSTAND each stage's content well enough to push back on it.

Relation to existing items (this generalizes + sharpens them):
- [enter-should-show-what-paper-is-about]: that asks the ENTER console to educate the user about the paper once. THIS asks every STAGE skill to educate + elicit taste, every time.
- [stage-advance-needs-user-confirm]: that adds a confirm-BEFORE-ADVANCE gate (a stage is over only when the user says so). THIS adds an explain-and-elicit step BEFORE/DURING drafting, upstream of that gate. Confirm-to-advance answers "are we done?"; this answers "do you understand and agree with what we are about to write?".
- Together the per-stage loop becomes: illuminate -> elicit user taste -> draft with that taste -> present done-criteria -> confirm to advance.

Proposed solution -- an "Illuminate + Elicit" step at the front of every stage skill:
1. Before writing the stage artifact, the stage skill PRESENTS the current state and the key choices in plain language: "Here is what the <stage> currently says / could say, here are the 2-3 decisions that carry taste (framing, emphasis, scope, ordering), here is my recommendation and why."
2. It ASKS the user for their take on those taste-bearing choices (chat text, not a wholesale rewrite). Only after the user weighs in does it draft, folding in their preference.
3. For a re-walk of an already-drafted stage, it must surface what is ALREADY there and ask "keep / change / reframe?" per taste-bearing element, rather than silently overwriting.
4. Add this as a shared convention, e.g. ref/stage-illuminate.md (a short "teach-then-elicit-then-draft" protocol), referenced by every stage skill's workflow as Step 0.
5. The autonomy policy (ref/delivery-need.md): drafting taste-bearing stage content is a PAUSE-to-elicit action, not an autonomous one. Mechanical formatting can stay autonomous; choices that shape the paper's argument or voice must be illuminated and offered to the user first.

Where it touches:
- new ref/stage-illuminate.md (teach-then-elicit-then-draft protocol + a short "taste-bearing decisions" prompt list per stage).
- each stage skill (seed/pitch/claims/narrative/display/minimap): add Step 0 "Illuminate + Elicit" before the produce step; for re-walks, diff-and-ask rather than overwrite.
- haipipe-paper-enter / haipipe-paper-lifecycle: state in their copilot policy that stage drafting is gated on an illuminate+elicit exchange, not just on the final advance-confirm.

Fix:
