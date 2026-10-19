haipipe-delivery · Changelog
============================

**[0.5.0] · 2026-10-19 · A round: render and read back (b32 s41-D21, D23)**

`scripts/word_round.py`, made shared from b21_event_cgm's `delivery/word_versions.py`: numbered versions, `render`
(each version's pages as pictures in `render/<name>-v<N>/`), `push`, and `pull`, the read back: OneDrive's changed
copy as the next version, rendered, its new comments listed, a `back` row in delivery.md. New section: A round;
`ref/page-delivery.md` no longer says render is Design-only (JL 2026-10-19: "after the delivery, we will also have
the render").

**[0.4.0] · 2026-10-16 · A Page's Delivery Runs fold in (s41-D11)**

The skill haipipe-draft-delivery is now `ref/page-delivery.md` (its changelog: `ref/history/haipipe-draft-delivery-CHANGELOG.md`).
Run names are unchanged (run-delivery-webpage, -latex, -word). New section: A Page's Delivery Runs; its triggers
join the description (JL 2026-10-16).

**[0.3.0] · 2026-10-14 · One item per deliverable, its versions inside; decks preview**

A deliverable is one item: its lanes (web/, word/, latex/; slide/ and render/) and its versions (`-v<N>`) fold
in, a row of versions over the picked one's preview (b10 s03-D10; JL 261014: "all of them should one Delivery
Item, and within it, we can see different versions"). A deck is drawn slide by slide from its package (JL
261014: "could we do the preview of the slide as well?"). New section: Items and versions.

**[0.2.4] · 2026-10-14 · Delivery folds inside the Studio too**

The Studio's third folding part, under Related: every result of the Block's `delivery/`, as Delivery's
own cards, each opened on its preview; the top row's Delivery stays the full view (b10 s03-D09; JL 261014:
"a new item after the Related to name it as the delivery ... show all the delivery and preview them here").

**[0.2.3] · 2026-10-11 · Its twin has a skill**

The boundary names `haipipe-related`, new, which owns `related/` (what came in), as this skill owns `delivery/` (b10 s04-D09).

**[0.2.2] · 2026-10-11 · From a Job or Task, Delivery opens the Block's**

The top row's Delivery opened from a Job or Task shows the Block's Delivery with a source row
(Block · jNN · tNN) and the open source picked, as Studio does (b10 s03-D06; JL 261011: "apply
it to all the workbench").

**[0.2.1] · 2026-10-11 · Related folds inside Studio**

The top row stays `Guide · Studio | Block · Job · Task | Delivery`; Related (what came in, the
twin of Delivery) folds inside the Studio under its topic cards (b10 s04-D05; JL 261011).

**[0.2.0] · 2026-10-11 · One row per send, no dNN**

A delivery folder keeps its source's name (`delivery/jNN_<job>/`); the dNN card is dropped (b10
s03-D05; JL: "could this be still the today's version or to make it like dNN_j01_vXXXX?"). Each
send is one row of `delivery/delivery.md` (date · for · from · status), the twin of the Block's
`related/related.md` (what came in, b10 s04).

**[0.1.0] · 2026-10-10 · A skill for the Block's Delivery**

New, beside haipipe-studio and haipipe-report (JL 261010: "should we have a skill named
/haipipe-delivery? ... just as we have the /haipipe-studio"). It holds the Block-only Delivery
rule once (b10 s02-D14, s09-D05), which haipipe-block, haipipe-report, haipipe-cowork and
haipipe-draft-delivery each carried as a copy; they now point here. The dNN card per send is
written as a proposal (b10 s03 Open 1), not applied.
