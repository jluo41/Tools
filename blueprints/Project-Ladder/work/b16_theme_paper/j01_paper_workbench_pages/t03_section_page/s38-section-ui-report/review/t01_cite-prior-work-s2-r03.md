# Citation Task (t01_cite-prior-work) · stage 2 · round 3 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j03_evidence_cite/t01_cite-prior-work (Report: MindMap · Findings · Status; Work: Findings · Status; Skills; Interactions)
answers  what: yes, Aim "What did earlier work find about <the policy>?" · where: yes · here: yes, "0 of 3 keys verified" with the missing key under the bar · do: partly, the missing key has no verb (add to the bib)
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ✅ one side tab per key · 5 ⚠️ "CITE card" in the Run's line; Status 2 · Runs cuts the Run's line at "each checked for" · table ⚠️ Work has no MindMap; Work Status's Results drop Runs
tasks    find which key has no bib entry: 0 clicks · find where each key is cited: 1 click (first tab open), 1 more per key · find what the Run checked: 2 clicks (Status, Runs) but the line is cut; 3 with the pop-out
walk     29 steps · 29 ✅ · 0 ❌ · 0 ⚠️; no page errors. Mine: ⚠️ the Runs row reads only the first line of a folded says:
bar      Findings matches the citation Job's Citations tab; Status's Headline repeats Findings' tally line word for word
rubrics  Glance 9 · Place 9 · Lean 8 · Words 8 · One job 8 · Same look 8 · Phone 9 · Salience 8 · Works 8 · Modern 8 · Plain 8 · Complete 8 (shown: each key's state; one click: title, year, DOI, cited in, verified by, source card, the label; pop-out: "3 citing sentences without a source card"; missing: in the reference bib, only in citations.csv)
score    mean 8.3/10 · pass
r02      fix 1 landed (📌 Headline, state "0 of 3 keys verified", words not codes) · fix 2 landed (Tables gone, no coded headline on the Runs row) but the Run's line is now cut · fix 3 landed (the question is the Aim)
fixes    1. Move the whole folded says: onto the Runs row (it stops at "each checked for").
         2. Rename "CITE card" to "source card" in cite_tasks.py's says:.
         3. Rename the waiting line to a verb: "Add example2022two to the bib", and remove the tally repeated under Status 1 · Headline.
questions Work's Results now lack Runs (Process shows them) and Work lacks MindMap, against decision 1: keep or restore?
```
