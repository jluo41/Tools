# Co-author Word

How we work on a Word file that co-authors share in OneDrive (word-track-change, hai-delivery
`scripts/word_round.py`). Each topic below is one rule or tool, with its requests.

## 🤝 Topic: Co-author Word ▸ sync while co-authors are active

A co-author may be typing in the shared .docx while we prepare our tracked changes. Today `word_round.py push`
copies our whole file over theirs: its checks (edits we never pulled, comments we would lose) see only what OneDrive
has synced to this Mac, and anything typed between the check and the copy is overwritten. A Word session open on the
file gets a new file under it and may fork a conflict copy.

Two ways of working, picked by whether co-authors are active:

| Co-authors | Where we work | How our changes land |
| --- | --- | --- |
| active (the file changed in the last hour, or the person says so) | in the shared file itself, opened in Word on this Mac | each edit made live as a tracked change; a paragraph whose words changed since the pull is skipped and listed |
| quiet | here: pull, `edits.yaml`, build, check, render | `word_round.py push` on the person's word, after a fresh pull |

Both start from a pull: it is how we read their newest text, comments and tracked changes and plan `edits.yaml`.
The live way re-reads each paragraph just before its edit, so a pull an hour old is still safe.

Questions:

1. Does AppleScript find-and-replace with Track Changes on record the smallest change, as `write_tracked` does, or
   one large replace?
2. Does Word on the Mac co-author when it opens the file from its OneDrive location (AutoSave on), and not from a
   local copy?
3. How fast is it: a round is 20 to 60 edits, a few seconds each in Word, so a few minutes. Is that acceptable?
4. How does the script tell "active": the OneDrive file's change time, the people listed in Word, or only the
   person's word?
5. Should `push` refuse while co-authors are active and point to the live way?

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-16 | "for the remote word, people are actively working on one word first, how could we sync and update it and not disturb others?" | JL directly | topic opened; proposed a live in-Word edit step (`wordtc.py live`) beside today's beside-copy route |
| 11-16 | "maybe some time, we just need to work on the word files with the coauthers when the coauthors are active, and if not, we just work here" | JL directly | the two ways written as the table above; first trial on a test .docx in OneDrive, not built yet |

## 📊 Topic: Word build ▸ tables read as the PDF prints them

The paper's own Word build (hai-paper-assemble) must print a table as its LaTeX does. Rule and parts:
`hai-paper-assemble/ref/word-lane.md` § Table cells read as the PDF prints them.

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-18 | "how do you think the display of the word? it think it should be better?" (ED Table 5: data rows bold, "A N-α", panel title centred and plain, italic names upright) | JL via ScalingGlucose-Board | header only when 3 or fewer rows above the first `\midrule`; cell exponents raised; `\textbf`, `\textit` and `{l}` spans kept; `latex_table.py` and `docx_table.py` split out; `tests/test_table_cells.py` |

## 🔍 Topic: Word round ▸ is the co-authors' Word the same as the build

A Word file comes back from the co-authors; is it the same paper as the build, sentence by sentence, and are its
reference numbers still in the order first cited? Rule and command: `hai-paper-assemble/ref/word-lane.md`
§ Is the co-authors' Word file the same as the build (`scripts/word_compare.py`).

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | "is the co-authors' Word file the same as the build?" asked by JL 4 times in one session; `word_round.py pull` reports comments and versions, not sentence equality, and nothing compared a .docx with the LaTeX PDF (Report topic 2) | AgreeableJama-Board Report | `scripts/word_compare.py` adopted from the peer's word_vs_word.py, word_vs_pdf.py, pdf_vs_word.py; equations read, NFKC on both sides, superscripts found by pieces; `tests/test_word_compare.py` (7) |
| 11-22 | the co-authors' Round 2 file numbers one reference 16 though it is first cited after 17 and 18; AMA requires order of first citation (Report topic 4) | AgreeableJama-Board Report | `word_compare.py --citations`; `word_round.py pull` prints it on every file that comes back; on Round 2 it prints "16 is first cited after 17, 18" |
| 11-22 | "never cited in the main text ...: 23" for both files, though Methods cites 23 right after "(eAppendix 4 in Supplement 1)"; on the supplement 30 numbers "never cited" and 3 out of order | AgreeableJama-Board Report | cause: the R² filter read "1)" as a one-letter base; now a power only touches a one-letter word; the gap line says "not found ... by this tool"; a supplement is not checked for order; `tests/test_word_compare.py` (9) |

State: fixed (both). Open: `--reverse` stays rough (pdftotext glues captions and cells to their neighbours).

## 🗂 Topic: Word round ▸ one folder layout per round

A co-author round is one folder, the same shape every round: the working Word files at the top, `previous/`,
`track/`, `clean/`, `submission/`, each with one `last-update-YYYY-MM-DD HH.MM.txt` marker. Rule and steps:
`hai-delivery/ref/round-folder.md` (`scripts/word_round_folder.py`).

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | rounds had loose, inconsistent files (Round1 "-draft.docx", Round2 "v4-tracked", Round3-v1112 holding v1114, Round4 three same-named files at top); JL designed the layout step by step, rejecting a changes/ log folder ("useless"), a separate diff/ folder and the name final/ | Pp-AgreeableRx-Discrention Report (topic 1) | `open-round` (last round's files into previous/, Track Changes on at the top), `submit` (portal uploads numbered by slot, then frozen), `round-status`; markers in every subfolder; `tests/test_word_round_folder.py` |
| 11-22 | "JL agreed the layout below is the one to keep; please confirm the ref says it exactly" | Pp-AgreeableRx-Discrention Report | ref/round-folder.md tree rewritten to the agreed layout: track/ diff PDFs against previous/, clean/ rebuilt each settle, submission/ slots 1 to 3 (later perhaps 4 latex.zip) |

State: fixed. Checked on scratch copies of the OneDrive Round3-v1112 and Round4-v1121 (Round5-v1123 opened,
submitted, a second submit refused). Open: the portal document itself (the peer's Block-local `portal_doc.py`)
is not lifted into a skill yet.

## 🧹 Topic: Word round ▸ settle a round

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | "this is what we want to have": refuse while open in Word, copy to track/, list every change with its author (Track Changes off too), sync each to its source, rebuild clean/, check word for word | Pp-AgreeableRx-Discrention Report (topic 2) | `settle <N\|all>` in that order; untracked edits found by words against the newest track/ copy; settle writes no source itself, it lists where each change goes |
| 11-22 | "when I say settle, you ask me how to deal with the changes in the working file" | Pp-AgreeableRx-Discrention, addendum | with no `--working`, settle asks and stops; `keep` (next settle starts from the track/ copy), `accept` (clean Word, refused while a marked insertion is not in the drafts), `each` (`--pick 1,3-5`, `scripts/word_marks.py`) |
| 11-22 | "for the clean and submission, they must be updated" | Pp-AgreeableRx-Discrention | after the rebuild, clean/ is refreshed for every file whose build changed and `--config` refreshes submission/; submission/ follows the newest build until Submit, and the new `submitted` freezes it; test `test_settle_refreshes_every_rebuilt_clean_file_and_submission` |
| 11-22 | working file 3 kept old portal values after a portal rebuild; the hand replacement then showed as four "untracked [?] say who made it" changes; a portal-only change took two reruns, hand copies and hand markers (Report 22:55, topics 1 and 2) | Pp-AgreeableRx-Discrention Report | new verb `refresh <round> N --clean N=… --config …`; settle's baseline is `track/.placed-<n>.docx`, the clean Word last placed; markers only by the tool; on scratch Round4-v1121 the 5 untracked lines became "no changes since then" |

State: fixed. Checked on the scratch Round5-v1123: a sentence typed with Track Changes off was listed as
untracked, keep left the file, and the next settle listed nothing twice. Open: writing the revise cards into
each source is still the session's step (settle prints the list and where each change goes).

## ✅ Topic: Word round ▸ the layout is checked by code

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | "why this doesn't follow the structure we want? It is so weird": push wrote a flat Round3-v1122 (no numbers, a PDF at the top, no subfolders) | JL via Pp-AgreeableRx-Discrention | `push` refuses any target in a RoundN-vMMDD/; `round-status` "❗ old layout"; SKILL.md "A round" leads with the round verbs |
| 11-22 | "should we make the code to do this check? should we have the check.py in the skill?" | JL via Pp-AgreeableRx-Discrention | `scripts/check_round.py` (`word_round.py check`, `--all`): six rules, exit code = ❗ count; every round verb ends with it |
| 11-22 | "I think you should have the folder like the submission, or track, or clean, or previous, you didn't find it?"; "why it is not followed? should we have the code to do this check?" (GlucoseScalingLaw/v1118 flat; `publish()` copied anywhere; open-round could not make a first round) | JL via ScalingGlucose-Board-v2 | `adopt-round` (`round_adopt.py`): a flat folder moved into RoundN-vMMDD, nothing deleted; `[publish]` copies only into a round's `clean/` (`delivery_publish.py`) |
| 11-22 | "With version": one name form `N-<Name>-vMMDD-<kind>.docx` | JL via Pp-AgreeableRx-Discrention | regex unchanged; check_round prints the rename for any other name |

State: fixed. Read-only on the live rounds: MISQ Round4-v1121 all ✅; AgreeableJama Round2-v1120 and LLMRec Round3-v1122 ❗ names only (rename given); LLMRec Round1, Round2 ❗ flat. Guards: `tests/test_word_round_folder.py` (20), `hai-paper-assemble/tests/test_delivery_publish.py`. Open: no paper_check row "shared folder in round shape" yet; the check runs from the round verbs and by hand.

## 🧽 Topic: Co-author Word ▸ a co-author edits the clean copy

```text
BEFORE                                       AFTER
clean/1-<Name>-v1120-manuscript.docx         clean/1-<Name>-v1120-manuscript-clean.docx
check: nothing looks inside clean/           ❗ 7 "a co-author edited the clean copy" + take-clean 1
merge by hand with cp                        take-clean: both to track/, his copy on top, clean/ rebuilt
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-23 | a co-author left 29 insertions, 18 deletions, 3 comments in clean/'s copy, named like the working file; the pull saw none; merged by hand with cp (topic 1) | AgreeableJama-Board Report | clean/ names end `-clean` (`clean-names` moves an older round); check rule 7; `take-clean`; `changes()` no longer lists an in-paragraph insertion twice |
| 11-23 | the hand refill rewrote previous/'s marker (topic 2) | AgreeableJama-Board Report | `marker()` refuses previous/ once it has one |

Check: live Round2-v1120 read only: ❗ 7 with the renames; scratch copy: `clean-names` makes it ✅; the co-author's
01.29 copy put back into clean/, `take-clean 1` moved his 29 + 18 + 3 marks to the top. State: fixed. Guard:
`tests/test_round_clean.py` (6).

## 📁 Topic: Co-author Word ▸ the first round of a new paper folder

```text
BEFORE                                      AFTER
adopt-round Paper-FairGlucose               refused: not a round folder, pass --into
  ─▶ Paper-FairGlucose renamed Round1-v1123   adopt-round Paper-X --into Paper-X
  ─▶ the paper folder vanished                ─▶ Paper-X/Round1-v1123/, Paper-X stays
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-23 | adopt-round renamed the new paper folder itself to Round1-v1123; the dry run "Paper-FairGlucose ─▶ Round1-v1123" read like "inside"; `round-status` refused by word_round_folder.py | Paper-FairGlucose-preprint Report | `adopt-round --into <paper-dir>`; without it only a RoundN-vMMDD or vMMDD folder is renamed; dry run prints full paths; `round-status` alias of `status` |

Check: scratch Paper-FairGlucose: plain adopt-round refused; `--into` made `Paper-FairGlucose/Round1-v1123`, check all
✅, the paper folder holds only the round; a second round beside it leaves Round1 in place. State: fixed. Guard:
`tests/test_round_clean.py` (adopt into a paper folder, round-status).

## 📦 Topic: Co-author Word ▸ submission/ reads the portal config as the portal does

```text
BEFORE                                         AFTER
from = "npj/npjDM-X-*-source.zip"              same line
build.py portal ✅   submit ❗ "not built"      build.py portal ✅   submit ✅ newest zip
dated name typed into the toml, goes stale     one config for portal/ and submission/
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-23 | `submit` took `from` as a literal path; the npj zip carries the build day, so the glob stopped it with "not built" | Paper-FairGlucose-preprint Report | `portal_files()` in word_round_folder.py: glob, newest by time, all matches with `all = true` (numbered -1, -2) |

Check: the real j12_writing_v1121_npjdm config read only: the glob resolves to npjDM-FairGlucose-261123-source.zip.
State: fixed. Guard: `tests/test_round_clean.py::test_submit_reads_a_portal_glob_as_the_portal_does`.
