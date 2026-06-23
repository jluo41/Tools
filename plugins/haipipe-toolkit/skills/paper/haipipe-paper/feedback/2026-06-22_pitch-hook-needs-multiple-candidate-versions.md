---
status: open
created: 2026-06-22
context: pitch stage (haipipe-paper-pitch) while walking Paper-LLMPhysicianRanking; generated 1-pitch.tex did not follow the updated template
fixed_in: ""
---

Reporter (JL): obviously, the pitch doesn't follow the skill I updated. For the hook section, we should have different versions of the hook, why don't we have it. [follow-up] These hooks should all stay displayed; there is no need to hide them.

What happened: the generated `0-lifecycle/1-pitch/1-pitch.tex` Hook section contained a SINGLE hook (one sentence). The skill requires drafting MULTIPLE candidate hooks (one per narrative method) and laying them out for comparison before committing.

Two concrete divergences from the template:
1. HOOK = MULTIPLE CANDIDATES. `ref/pitch-readability.md` ("A good hook: narrative methods" -> "Choosing", lines ~70-71) says: "When unsure, draft the hook in two or three methods and compare before committing" and "During selection, lay the candidates out as \subsection* blocks under the Hook section (one per method, the chosen one marked '(selected)'), compile, and compare in the PDF; collapse to the selected hook once it is locked." The generated pitch did none of this; it committed to one hook with no alternatives to compare.
2. BANNER/CUE BLOCKS DROPPED + hook too short. The SKILL.md template (Step 2) puts a `% === % Para [pitch.x] ... % Cue: ... % ===` banner before each section; the generated pitch omitted them. The hook was also 1 sentence, but the cue requires 2-4 (grab -> deepen -> bridge).

Root cause (real skill inconsistency, not only operator error): the SKILL.md INLINE template Hook block (lines ~113-119) shows only a single `%% ---- P2.S1 ----` example sentence. That inline template is what the generator follows, and it directly contradicts the multi-candidate selection workflow in ref/pitch-readability.md. The two should agree.

3. KEEP ALL CANDIDATES, DO NOT COLLAPSE (JL follow-up). `ref/pitch-readability.md` line ~71 currently ends the selection workflow with "collapse to the selected hook once it is locked," and principle 6 says "commit to ONE move." JL wants the OPPOSITE for the artifact: keep every hook candidate displayed permanently, mark a recommended lead, and never hide the alternates. The collapse step contradicts this and should be removed.

Fix: make the multi-hook-candidate workflow first-class in the SKILL.md template itself, not buried in the readability ref. In the Step 2 inline template, replace the single-sentence Hook block with a layout that lays out 2-3+ candidates as `\subsection*` blocks (one per narrative method) and KEEPS THEM ALL displayed, marking a recommended lead (not "selected", which implies hiding the rest). Remove the "collapse to the selected hook once it is locked" instruction from pitch-readability.md "Choosing"; reword principle 6 so "commit to one move" applies PER candidate, not to the final artifact (the final pitch keeps all candidate hooks visible for the author to choose at write time). Add a pitch done-gate item: "Hook section shows >=2 candidate methods, all retained, with a recommended lead." (Applied this layout by hand to Paper-LLMPhysicianRanking 1-pitch.tex as the interim fix: 5 candidates A-E, all kept, A marked recommended lead.)
