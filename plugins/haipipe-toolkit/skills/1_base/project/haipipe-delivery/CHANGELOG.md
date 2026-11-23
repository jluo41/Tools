haipipe-delivery · Changelog
============================

## 0.11.0 · 2026-11-22 · check_round.py and adopt-round

- JL 261122 ("should we make the code to do this check? should we have the check.py in the skill?"), from Pp-AgreeableRx-Discrention and ScalingGlucose-Board-v2 the same night: new `scripts/check_round.py` (`word_round.py check <round>`, or `<rounds-dir> --all`), six rules, one ✅ or ❗ line each, exit code = the ❗ count; open-round, adopt-round, settle, refresh, submit and submitted end with it. Read-only on the live rounds: MISQ Round4-v1121 all ✅; AgreeableJama Round2-v1120 and LLMRec Round3-v1122 ❗ only on names (the rename given); LLMRec Round1, Round2 ❗ flat.
- One name form (JL: "With version"): `N-<Name>-vMMDD-<kind>.docx`; the regex is unchanged and the check prints the rename.
- New verb `adopt-round` (`scripts/round_adopt.py`): a flat folder becomes RoundN-vMMDD by moving, never deleting. On scratch copies of GlucoseScalingLaw/v1118 and LLMRec Round2-v1028 the check then passes except "clean/ lacks 2 .pdf" (never built). open-round's "make the first round by hand" now names adopt-round.
- tests/test_word_round_folder.py: 2 more (20).

## 0.10.1 · 2026-11-22 · push never writes into a round folder

- Pp-AgreeableRx Report 261122 (JL: "why this doesn't follow the structure we want? It is so weird"): a new session followed the SKILL's push-first workflow and wrote a flat `Round3-v1122/` (an unnumbered .docx, a PDF at the top, no subfolders). `word_round.py push` now refuses a target inside any `RoundN-vMMDD/` and names open-round and refresh; `round-status` prints "❗ old layout" for a round with none of previous/ track/ clean/ submission/; SKILL.md "A round" leads with the round folder, and the single-file lane comes second. tests/test_word_round_folder.py (2 more).

## 0.10.0 · 2026-11-22 · refresh: an unedited working file becomes the clean build

- Pp-AgreeableRx Report 261122 22:55, topic 1: working file 3 (portal) still held old values after a portal rebuild; the hand fix (save to track/, copy clean/3 over it, track_on.py, markers by hand) made `settle 3` list the replacement as four untracked changes, because its baseline was the newest track/ copy, the old file. New verb `refresh <round> <N|all> --clean N=… [--version] [--config]`: refuses an open or edited file; places clean/, saves the old file to track/, makes the clean Word the working file with Track Changes on, refreshes submission/ with `--config`, writes every marker. `track/.placed-<n>.docx` (written by refresh and by settle's accept, removed by a later marked copy) is settle's baseline. A working file already holding clean/'s words is only recorded. On a scratch copy of Round4-v1121: refresh 3 recorded the hand copy and `settle 3 --dry-run` said "no changes since then" (it listed 5 untracked before); a changed portal build then replaced file 3 as v1122 in one command.
- Pp-AgreeableRx 261122 (after verifying refresh on Round4-v1121): settle's dry run named the baseline `track/.placed-3.docx` as the marked copy it would write; now "marked copy: none needed" and "since: the clean Word placed at the top".
- Topic 2: a portal-only change is now `refresh 3 --clean 3=… --config …`; markers are never written by hand.
- ref/round-folder.md: the tree says the JL-agreed layout exactly (track/ diff PDFs against previous/, clean/ rebuilt each settle, submission/ slots 1 to 3), a "How to refresh" section, the baseline rule. tests/test_word_round_folder.py: 4 more (16).

## 0.9.1 · 2026-11-22 · clean/ and submission/ follow the newest build

- Pp-AgreeableRx-Discrention 261122 (JL: "for the clean and submission, they must be updated"): after a settle's rebuild, clean/ is refreshed for every file whose build changed (`--clean N=...` for each), not only the settled one, and `--config <paper-build.toml>` refreshes submission/ too; both markers are rewritten. submission/ equals the newest build until the person presses Submit; the new `submitted` verb freezes it (`submit` no longer does). tests: 12.

## 0.9.0 · 2026-11-22 · a co-author round as one folder, and settle

- Pp-AgreeableRx-Discrention Report 261122 (topics 1 and 2; JL: "this is what we want to have", "when I say settle, you ask me how to deal with the changes in the working file"): `RoundN-vMMDD/` holds the working Word files at the top (numbered 1, 2, 3, Track Changes on) and `previous/`, `track/`, `clean/`, `submission/`, each with one `last-update-YYYY-MM-DD HH.MM.txt` marker. New `scripts/word_round_folder.py` (`open-round`, `settle`, `submit`, `status`; `word_round.py` passes the verbs on) and `scripts/word_marks.py` (number the marks, accept the picked ones). `ref/round-folder.md`.
- settle: refuses while Word holds the file; copies it marked into track/; lists every tracked change and comment with its author, plus untracked edits found by comparing words with the newest track/ copy; rebuilds into clean/; checks the draft against clean/; then asks keep, accept or each. accept is refused while a marked insertion's words are not in the drafts.
- Run on scratch copies of the OneDrive Round3-v1112 and Round4-v1121: open-round made Round5-v1123 with previous/ and Track Changes on in all three (Round4's cover letter had it off); a sentence typed with Track Changes off was listed as untracked; keep left the file and the next settle started from the track/ copy with no change listed twice; submit numbered the 3 portal uploads by slot and refused a second submit.
- tests/test_word_round_folder.py: 11 tests.

## 0.8.1 · 2026-11-04 · models, data and websites

- A work Block's Findings ends with 📦 Delivery, tabs Models · Data · Website; lanes `model/`, `data/`, `web/` (JL 261104).

## 0.8.0 · 2026-11-04 · a live page in Delivery

- A deliverable with `url:` shows as a closed card in Delivery, its page working in a frame when opened (JL 261104): `frame._live_pages`, `focus_page.live_pages_html`; new section Live pages. Findings gets 🌐 Service, one side tab per site (`service:`, `focus_page.service_section`).

## 0.7.1 · 2026-11-01 · b16 review 261101: current paper names

- The opening says the Block owns the one `delivery/`, a level's output under `<Block>/delivery/<its address>/`, as the code (`delivery_dir`) does; so does the description.
- Studio wording: one sNN numbering per Block, topics beside the Jobs (haipipe-studio 0.28.1), no `studio/` folder.
- Metadata last_updated follows the 0.7.0 entry before this bump.

## [0.7.0] — 2026-10-30

New `ref/gallery.md`, the delivery gallery (JL 261030: "we might also have a sNN for the gallery of the deliveries"):
every kind of `delivery/` on the machine (Word + PDF, LaTeX + PDF, web page, deck, skill, ...), how many, whose, and the
newest real one each. Rendered from b35-s04's `delivery/skill/gallery.md`, which haipipe-studio `gallery_scan.py` writes.

## [0.6.2] — 2026-10-29

Only the clean, agreed version lands in `delivery/`, after rounds in a Studio topic (b35 s01-D11).

## [0.6.1] — 2026-10-29

The Studio is one per Block again (b35 s01-D05); only `delivery/` stays at every level.

## [0.6.0] · 2026-10-28 · Delivery at every level

- JL 261028: a Project, Block, Job and Task may each hold its own `delivery/`; a page shows its own plus its children's
  (the workbench focus page's Delivery section). SKILL.md's opening and description say so; a Block's existing
  `delivery/` stays where it is. haipipe-project 0.18.0 drops `delivery` from its Block-only list.

**[0.5.1] · 2026-10-23 · A SharePoint copy is still its version (Paper-Example-Jama, Round1-v1023)**

`scripts/word_round.py`: `held()` also matches a copy whose document, comments and footnotes equal a version's
(`same_words()`), since SharePoint adds its own properties to every .docx it stores and `push` then took its own
copy for someone's edits; `rel()` prints a path outside the SPACE as it is (OneDrive's real folder behind the
`_WorkSpace/CoWork-JHU` symlink crashed `push` after the copy, before its `draft` row).

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


## [0.5.2] — 2026-10-26

Shorter description (1201 -> 419 characters): what it does, when to use it, its trigger words; aliases and old command names kept (diagnostics/descriptions/261026.yaml). (describe 261026)
