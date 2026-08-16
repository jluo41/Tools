# PP03-skill-census
question: How many skills does the board family ship under plugins/haipipe-toolkit/skills/board, and which are they?
state: bound
binding: → tasks/F01_skill_inventory/01_board_skill_count/QA/1-board-skill-count.md
stake: the family's own size is quoted in reviews and rosters; a wrong count makes every such claim soft.

## Q-executor
Count the skills under /Users/floydluo/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/board, where one skill is one folder containing a SKILL.md file. List every skill name, grouped by subdirectory.
Deliverable: QA digest with the full list. Accepted: an exact count with the list.

## bank binding
route: task · bank: new → answered · target: the binding line above

## A-executor
24 skills: 5 at the board root (board, board-routing, page, plugin, sentence), 10 under page-plugins/, 4 under page-types/, 5 under page-workflows/.
