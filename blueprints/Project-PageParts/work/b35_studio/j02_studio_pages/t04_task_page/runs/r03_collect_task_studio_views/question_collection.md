# Task Studio views

for: b35.j02.t04-s19

Proposals for the Studio section of a Task page. Every preview is t02_block_page, the real Task page, with its s11, s12 and s13.

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form.
     The previews are written by a script from the live page's HTML (its look and CSS kept). -->

## Q1 · View list

The view-button-list sits under the title. Today a Task's Studio has one button per Tag; t02_block_page has one, Block UI, over three cards. A Task holds at most three sNN.

**Which buttons sit under the title of a Task's Studio?**

- [x] A · One button per Tag (today): Block UI opens the three cards.
  [preview](q1-a.html)
- [ ] B · One button per sNN: each opens that topic whole, face and drawing.
  [preview](q1-b.html)
- [ ] C · Topics · Drawings: the cards, then every sNN drawing large in one column.
  [preview](q1-c.html)

Why A: Same bar on Block, Job and Task; the Tag names the group.

## Q2 · Tag view

With the A pick, each Tag button opens one view of the Task's own sNN. Today it holds cards: name, one line, buttons, a small picture on the right.

**What does a Tag view, such as Block UI, hold?**

- [x] A · Cards (today): name, one line, buttons, small picture on the right.
  [preview](q2-a.html)
- [ ] B · Big rows: each sNN's drawing full width under its name and buttons.
  [preview](q2-b.html)
- [ ] C · Cards, each with its first Open line under its buttons.
  [preview](q2-c.html)

Why A: Same card as the Block and Job; a click shows the picture large.

## Q3 · One sNN

The face's Open point: when a Task holds one sNN only, should Studio open straight on it? The previews show t02_block_page as if it held s11 only.

**When a Task holds one sNN only, what does Studio show?**

- [ ] A · Its card, the same as when the Task holds three.
  [preview](q3-a.html)
- [ ] B · The sNN opened whole: buttons, its Topic, Rules and Open, then its drawing.
  [preview](q3-b.html)
- [x] C · Its drawing first, full width, with the card's name and buttons under it.
  [preview](q3-c.html)

Why C: One topic, so its real drawing is the page; its buttons stay.

## Q4 · Clicks

Today a card's name opens its face and its picture opens its drawing, both in a pop-out over the page (JL 261029).

**What does a click on a card's name or picture do?**

- [x] A · A pop-out over the page: the name its face, the picture its drawing.
  [preview](q4-a.html)
- [ ] B · The card unfolds in place: its drawing and face open under it.
  [preview](q4-b.html)
- [ ] C · A new tab: the Excalidraw drawing, ready to edit.
  [preview](q4-c.html)

Why A: The reader stays on the Task page; one close brings them back.
