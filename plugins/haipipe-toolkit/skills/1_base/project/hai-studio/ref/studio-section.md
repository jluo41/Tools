# The Studio section of a page

Part of hai-studio's topic contract (`ref/topic-contract.md`). What the workbench shows for a level's topics and
what it reads to show it. Only two things here are written by hand: a topic's `**Tags:**` line and
`_studio_groups.txt`.

## Where a topic opens

A topic has no page of its own. Every link to it (the left rail's sNN, an old `?path=…/sNN-<topic>&layout=focus`
link) opens its card in its level's Studio section, under its group, outlined (`focus_page.py` `topic_home`; the
server sends an old link on with a 302). The card's name and line open the face, its picture the slide; Slide, Draw,
Mind map, Work and Delivery pop out over the page. A builder's page in `delivery/` wears the workbench frame, its
path ending at that card. A Job or Task finds a topic in its own folder first, else wherever it lives in the Block.

## Groups

A topic's groups are its `**Tags:**` line. The Studio row edits them: `+ Group` names one, dragging a card onto a
group adds the tag, × on a card's group takes it out, × beside a group deletes the tag from every topic.
`_studio_groups.txt` keeps the Block's groups in button order, empty ones included; dragging a group sideways
rewrites it. Both are plain text: edit them by hand when that is quicker. Which group is current is the person's own
choice and stays in the browser.

A blueprint Block groups its topics by the shared Studio bands instead (`ref/topic-numbering.md`).

Related, folded under the topics, has the same bar: an item's groups are its subfolder (`meetings/` → meetings) and
the names in its row's `group` cell of `related/related.md`; `related/_groups.txt` keeps their order.
`hai-related` owns that folder.

## Runs, Timeline, Folder

Each reads what is on disk; nothing is written for it.

1. **Runs**, folded under Delivery: every hard Run (`runs/rNN_*`) of every Task under the Block, Job → Task, each
   with its own mark and finish day, and no count or tally. Read from the Runs' receipts.
2. **Timeline**, folded under Runs: what moved when, on one axis down the page, the oldest day at the top, at three
   levels (Days · Topics · Everything). It reads a decision's date in its brackets, a round's `pNN-<MMDD>` and a
   drawing's green `✎ <YYMMDD>` notes. A decision with no date is left off, so date every decision.
3. **Folder**, folded under Timeline: the Block's own folder as one tree. A folder says what it is for (a shared
   name's fixed line, a Run's card, else its face's title); a file opens in the pop-out.

## A topic's life on the row

`**Stage:**` runs explore → shaping → agreed → closed and is moved by a person; each round may move it.

## Inside a topic: top, left, right

Every view of a topic reads the same way: the kinds of thing are buttons on top, the parts of the picked one are
tabs on the left, one part is on the right.

```text
several items in a view          a left tab per item
one folder item                  one fold per file on the right
one Markdown file, 2+ sections   a left tab per `##` section, named by the heading; the page makes them
one file with one section, a drawing, a deck     full width
```

The text before a file's first section is the first tab, named by the file's title, when it says more than the
title. A Page Face (it has an Opening section) is shown as a Page, never split. Nothing is copied: do not cut a
file into part files to get left tabs.
