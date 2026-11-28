---
name: word-track-change
description: "A co-author Word round with tracked changes: pulls their newest .docx, adds ours as tracked changes with theirs kept, renders the PDF in Word and pushes it back on the person's word. Use to send edits back in Word. Trigger: track changes in Word, co-author Word file, /word-track-change."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-11-11"
---

# /word-track-change · our changes, tracked, on the co-authors' own Word file

Co-authors edit a shared .docx in OneDrive with Track Changes on and leave comments. We answer on that same
file: every change we make is a tracked change by one author they can accept or reject, a comment is left only
when no edit can answer it, and nothing they wrote is lost. Built first for an MIS Quarterly Round 2 (2026-11-10).

```text
OneDrive .docx ─▶ ① pull ─▶ vN ─▶ ② read ─▶ ③ decide (edits.yaml) ─▶ ④ try ─▶ ⑤ build
 ─▶ ⑥ render in Word ─▶ ⑦ check + look ─▶ ⑧ import vN+1 ─▶ ⑨ push (person's word) ─▶ OneDrive
```

## Tools

| Step | Command |
|---|---|
| ① pull, ⑧ import, ⑨ push | `hai-delivery/scripts/word_round.py --word-dir <lane>/word --name <Name> --onedrive <docx> pull \| import <file> \| push <N>` |
| ② ④ ⑤ ⑥ ⑦ | `scripts/wordtc.py read \| try \| build \| render \| check \| diff` (this skill) |
| the XML work | `hai-draw/gallery/draft/ref/track_changes.py` `write_tracked` (smallest deletion and insertion per edit) |

## Steps

1. **Pull.** `word_round.py pull` saves OneDrive's file as the next version `vN` in the lane's `word/` and lists new comments. Always build on the newest pulled version, never on our own older export.
2. **Read.** `wordtc.py read vN.docx --changes`: comments and tracked changes per author, with their words. Their inserted words are theirs: note them before you plan any change.
3. **Decide.** Write `edits.yaml` in the round's Task (`scripts/edits.yaml`), one entry per change:
   ```yaml
   edits:
   - id: <section>:<P>.<S>          # where it is
     find: <their exact words, accepted view, unique in the file>
     new: <what they become>        # "" deletes; omit to only comment
     comment: <a note>              # optional; alone = a point on their sentence, no rewrite
     why: <the comment or review that asked for it>
   ```
   - Only changes a person or a blind check accepted go in (hai-paper-draft § Co-authors' patterns).
   - **Fix, don't comment** (JL 261113: "for the comments here, why you don't fix them?"; "only leave the comments when you must have to"; hai-paper must-check M-C11). What a comment asks, and a slip or a contradiction in a co-author's sentence, becomes a `new:` tracked change on their sentence, their own marks kept; `comment:` alone only when no edit can answer it (a question for the author, a choice only they can make), with the reason.
   - `find` is the accepted text: strip review markup (comment anchors, inline author tags) first.
   - A sentence whose math or symbols the export lost is left alone; fix the exporter, not the words.
4. **Try.** `wordtc.py try vN.docx edits.yaml` tests each edit alone. Fix every ✗ (not found, not unique: lengthen `find`) before building.
5. **Build.** `wordtc.py build vN.docx edits.yaml <out>-tracked.docx --author "<Name>"`, or the round Task's own `build_tracked.py` that calls `write_tracked`. The output is generated: change `edits.yaml`, then rebuild; never edit the .docx.
6. **Render in Word.** `wordtc.py render <out>-tracked.docx` drives Microsoft Word through AppleScript (Word saves only inside its sandbox container; the script copies in and out) and falls back to LibreOffice, which paginates differently. Page counts are Word's.
7. **Check and look.** `wordtc.py check vN.docx <out>-tracked.docx --author "<Name>"` must say `others kept: yes` and the same comment count plus ours. Then render two or three pages to PNG (`pdftoppm -f N -l N -r 70 -png`) and look at the strike-through and underline yourself.
8. **Import.** `word_round.py import <out>-tracked.docx` makes it version `vN+1` in `word/`.
9. **Push only on the person's word.** `word_round.py push N+1` copies it to OneDrive; it refuses when OneDrive holds edits no version has (pull first) or when a comment someone left would be lost. Only a person writes `sent` in `delivery.md`.
   - **Working copy for the person (optional).** When the person asks to review it in OneDrive first, the build writes `<out>-tracked.docx` beside the co-authors' file in the current round folder (theirs is never replaced) and keeps a copy as `sent.docx`; a rerun never overwrites the OneDrive copy unless forced. `wordtc.py diff sent.docx <onedrive copy>` lists what the person changed: paragraphs, comments, tracked changes added, accepted or rejected. When the person says it is okay, it becomes the next round folder's file.

## Rules

- One author for all our marks (the person's name as co-authors know it). Never impersonate a co-author.
- Their tracked changes stay unresolved: we never accept or reject their marks for them.
- No process text in the file (counts, scores, "blind reader"): those live in the Task's records.
- A round is a review Job (`jNN_review_coauthor_v<MMDD>/`), its Tasks: sentence review, readability check, tracked Word (and structure, when they ask for it); never `reports/`.
