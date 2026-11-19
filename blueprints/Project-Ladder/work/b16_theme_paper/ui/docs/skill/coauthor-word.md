# Co-author Word

How we work on a Word file that co-authors share in OneDrive (word-track-change, haipipe-delivery
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

The paper's own Word build (haipipe-paper-assemble) must print a table as its LaTeX does. Rule and parts:
`haipipe-paper-assemble/ref/word-lane.md` § Table cells read as the PDF prints them.

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-18 | "how do you think the display of the word? it think it should be better?" (ED Table 5: data rows bold, "A N-α", panel title centred and plain, italic names upright) | JL via ScalingGlucose-Board | header only when 3 or fewer rows above the first `\midrule`; cell exponents raised; `\textbf`, `\textit` and `{l}` spans kept; `latex_table.py` and `docx_table.py` split out; `tests/test_table_cells.py` |
