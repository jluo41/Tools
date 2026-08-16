# 1-board-skill-census
state: answered
started: 260816
question: How many skills does the board family ship under plugins/haipipe-toolkit/skills/board, and which are they?

## Answer
24 skills, counted as folders holding a SKILL.md, in four tiers (260816):

- 5 base: haipipe-board · haipipe-board-routing · haipipe-page · haipipe-plugin · haipipe-sentence
- 10 plugin variants (page-plugins/): haipipe-plugin- bibex · chat · display · draw · folder · latex · probe · skill · slide · word
- 4 page types (page-types/): haipipe-page-for- design · meeting · skill · stage
- 5 workflow phases (page-workflows/): haipipe-page-workflow · haipipe-page- draft · probe · revise · check

Method: `find skills/board -name SKILL.md`, one skill per folder; agents/ holds agent definitions, not skills, and is not counted.
NOTE: this QA file is a SPECIMEN, answered by the session demonstrating the probe loop, not by the task or discovery bank; it lives in the page's own _fixture/ because this repo has no bank tree.
