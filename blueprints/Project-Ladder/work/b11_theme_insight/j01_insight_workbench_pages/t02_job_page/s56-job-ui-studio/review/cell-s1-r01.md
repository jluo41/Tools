# s56 Job UI: Studio · cell review · stage 1 · r01

Scores: A 8.1 not yet (Salience 6) · B 8.3 not yet (One job 5).

Does each letter belong?
- A This Job: belongs as the Job's own topics, but its button is a scope, not a group. Studio's view-button-list is one button per group (the topics' Tags), Other last.
- B Board: redundant. The page-at-each-level table says a Job's Studio shows its own topics and its Tasks', and the Board's Studio already shows s01 and s05. This answers the open question: a Job's own topics (and its Tasks'), not the Board's.
- Missing: the Tasks' topics, rolled up with where they live (s02 · t10).

Further improvements beyond the rubric fixes:
1. Group buttons by Tag (for example Readings, Cuts), not by scope. Why: matches every other Studio in b15 and b16, and the base rule.
2. Helpers at the bottom after a dashed rule: Ask the agent with a Copy prompt button, then the mind map button. Why: the topic is the content; the prompt is a tool.
3. An empty-state row ("no topic yet, start one") as the Task Studio has. Why: most Jobs will have no own topic, and the page then still says what Studio is for.
4. Each row carries where it lives ("s02 · j03"). Why: haipipe-ui Rows on rolled-up items; the reader sees the same sNN on the Board page.
5. Fix the default caption builder ("the topics of the This Job group"). Why: the fallback text in view_rows reads as broken English on every group without a CAPTION entry.
