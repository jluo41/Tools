# A co-author round as one folder

JL 261122 (Pp-AgreeableRx-Discrention, MISQ paper): one folder per round, the same shape every round. The working
Word files sit at the top; four subfolders say where every other copy came from. Script:
`scripts/word_round_folder.py` (also reached as `word_round.py open-round | settle | refresh | submit | submitted | round-status`).
JL agreed this layout (Pp-AgreeableRx 261122, 22:55); it is the one to keep.
Live example: the OneDrive folder `PhyTrait-Opioid-Discretion-MISQ2026/Round4-v1121`.

```text
RoundN-vMMDD/
├─ 1-<Name>-vMMDD-manuscript.docx     working Word files ONLY, Track Changes on (w:trackRevisions):
├─ 2-<Name>-vMMDD-cover-letter.docx   what co-authors open and edit
├─ 3-<Name>-vMMDD-portal.docx         the portal's fields as a document
├─ previous/    the earlier version of each file, each keeps its own vMMDD; written once, by open-round
├─ track/       the diff PDFs against previous/ (when built), and a marked copy saved before any clean or replace:
│               <n>-<Name>-v<ver>-<kind>-tracked-YYYY-MM-DD HH.MM.docx
├─ clean/       per file: the LaTeX PDF and the LaTeX-made Word, no marks; rebuilt each settle (and by refresh)
└─ submission/  portal uploads only, numbered by slot (1 manuscript pdf, 2 cover-letter pdf,
                3 research-transparency pdf; later perhaps 4 latex.zip); refreshed until Submit, frozen by `submitted`
```

## Rules

1. One number per document, the same in every folder (1 manuscript, 2 cover letter, 3 portal). One name form
   everywhere, `N-<Name>-vMMDD-<kind>.docx` (JL 261122: "With version"), so a file carries its version when it is
   downloaded or emailed; `check_round.py` gives the rename for any other name.
2. No PDF at the top. `round-status` marks one with ❗.
3. Every subfolder has one marker, `last-update-YYYY-MM-DD HH.MM.txt` (a dot: SharePoint refuses a colon), listing
   its files with their times. The tool that rewrites a folder rewrites its marker; markers are never written by
   hand (a hand `rm` of the old marker also trips the shell's safety block).
4. Never accept marks mid-round without the track/ copy first.
5. previous/ is written once, by open-round. submission/ always equals the newest build until the person presses
   Submit (`submit`, and every settle or refresh given `--config`, refresh it); `submitted` then freezes it. Nothing else writes
   them. After a settle's rebuild, clean/ is refreshed for every file whose build changed, not only the settled one
   (JL 261122: "for the clean and submission, they must be updated").
6. An old round is re-laid out only by moving files within the same SharePoint library (a copy loses its history).
7. Names JL rejected: `changes/` (a log nobody reads), `diff/` (the diffs are in track/), `final/` (clean/ is not
   frozen; submission/ is).

## The steps

```text
open-round <rounds-dir> [--date MMDD] [--file N=<built.docx>]
    the last round's working files ─▶ previous/; the new working files at the top, Track Changes on
settle <round-dir> <N|all> [--rebuild CMD] [--clean N=<docx>[,<pdf>]]... [--config <paper-build.toml>] [--draft N=<docx>] [--working …]
refresh <round-dir> <N|all> [--clean N=<docx>[,<pdf>]]... [--version MMDD] [--config <paper-build.toml>]
    a working file nobody changed ─▶ track/ (old copy); clean/ placed; the clean Word at the top, Track Changes on
submit <round-dir> --config <paper-build.toml>
    each [[portal.upload]] ─▶ submission/<slot number>-<Name>-vMMDD-<kind>.pdf (the newest build)
submitted <round-dir>
    the person pressed Submit: submission/ is frozen
round-status <round-dir>
adopt-round <flat-dir> --name <Name> --date MMDD [--round N] --file N=<file>:<kind>... [--dry-run]
    a flat folder ─▶ RoundN-vMMDD/ by moving: the named files to the top, their PDFs and a copy as built to clean/,
    marked copies ("tracked") to track/, everything else to previous/ as it came; nothing deleted
check <round-dir> | check <rounds-dir> --all      (word_round.py check, scripts/check_round.py; --all before or after)
    one ✅ or ❗ per rule, exit code = the ❗ count; every verb above ends with it
```

## The check

`scripts/check_round.py` (JL 261122: "should we make the code to do this check? should we have the check.py in
the skill?"). Rules: 1 the top holds only working Word files in the one name form (with the rename when not);
2 all four subfolders; 3 each subfolder with files has one marker that lists them; 4 Track Changes on; 5 each
working file has its clean Word and PDF, submission/ only numbered slots; 6 previous/ keeps older versions, a
submitted submission/ is unchanged since Submit. `push` never writes into a round; the paper build's `[publish]`
copies only into a round's `clean/`, with numbered names.

## How to settle

JL 261122: "this is what we want to have", and "when I say settle, you ask me how to deal with the changes in the
working file". One command, always in this order:

1. **Refuse while the file is open**: Word's `~$` lock file beside it, or `lsof` finds it open. AutoSave writes over
   any outside change (the Table C3 loss of 261121).
2. **The marked copy**: the working file as it is into track/. If nothing changed since the newest marked copy, that
   copy stays the one copy.
3. **The change list**: every tracked insertion, deletion and comment with its author (wordtc.py's reader), plus the
   words that differ from the last synced point, so an edit typed with Track Changes off is caught too. The last
   synced point is the clean Word last placed at the top (`track/.placed-<n>.docx`, written by `accept` and
   `refresh`, removed when a later marked copy is saved), else the newest track/ copy (by the stamp in its name),
   else clean/, else previous/, so a change is never listed twice and a replacement is never listed as untracked. Each change goes to its source as a revise card: file 1 to the Section drafts, file 2 to
   t31_cover-letter, file 3 to portal-values.yaml. A comment that is a question, or an untracked change, is marked
   🙋 for the person. settle writes no source itself.
4. **Rebuild**: `--rebuild "<the paper's build>"`, then `--clean N=<docx>,<pdf>` places the build in clean/.
5. **Check**: `--draft N=<docx>`: the draft's Word and clean/ hold the same words.
6. **The question**: with no `--working`, settle asks and stops. The answers:
   - `keep`: the working file stays as it is, marks and comments included; the next settle starts from this track/
     copy.
   - `accept`: the working file becomes the clean Word (no marks, comments closed, Track Changes still on). Refused
     when a marked insertion's words are not yet in the drafts, so nothing is lost.
   - `each`: every mark and comment numbered; `--pick 1,3-5` accepts those (an insertion kept, a deletion dropped,
     a comment closed) and keeps the rest.

`--dry-run` writes nothing and says what each step would do.

## How to refresh

Pp-AgreeableRx 261122: the portal was rebuilt (one portal-values.yaml field), and working file 3 still held the old
values; the hand fix (save to track/, copy clean/3 over it, track_on.py, markers by hand) then made settle list the
replacement as four untracked changes. `refresh <round> 3 --clean 3=<portal.docx>,<portal.pdf> --config
<paper-build.toml>` is the one command:

1. **Refuse while the file is open** in Word, as settle.
2. **Refuse an edited file**: any mark, comment, or word changed since the last synced point; `settle N` deals with
   those first.
3. **Place clean/** from `--clean`; the old working file is saved to track/; the clean Word becomes the working file
   (named with `--version`), Track Changes on; settle's baseline becomes that clean Word.
4. **submission/** is refreshed from the newest build when `--config` is given (unless frozen).
5. Every marker is rewritten by the tool. A working file that already holds clean/'s words (a copy made by hand)
   changes nothing: refresh only records it as the baseline.

