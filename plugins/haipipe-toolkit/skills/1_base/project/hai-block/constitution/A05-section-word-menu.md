# A05 · The section word is the sections menu; the 📁 ball is Files

**Need.** JL wants to pick Studio, Things to Know and the other sections by clicking the section word beside the title
(Report), and to keep the round 📁 ball for Files alone.

**Now.** `focus_shell.page_shell` draws the word as `button.h1-pick` (• Report: a `::before` dot in focus.css, accent on hover) controlling `#side-menu`. `focus.js`
opens the menu under it (Files hidden there), and the ball toggles the Files pane straight away.

**Gap.** Before: the word was a plain span; every section sat behind the ball's menu at the screen's edge.

**Methods.** Reuse the one `#side-menu` and its `open()`; `showMenu(anchor)` places it under the word or beside the ball.

**Update.** Verified on 5623 b17: • Report opens Studio ... Skills; Studio opens in the pane; the ball switches the
pane to Files, and a second press closes it. workbench 230, labeling 85, paper 112, design 58 pass.

**Never again.** The tests pin `button.h1-section h1-pick` in every page's title, with no caret inside (JL 261125 16:20: the dot left of Report, "this is what I want").
