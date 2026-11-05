# Word build speed · answers

received: 2026-11-04 13:57

for: b16.j02-s22:theme_paper.word_lane_speed @ word_lane_speed

Word was stuck, not slow. On a working Word a whole build took 40 to 80 seconds. Builds now take turns in Word. One choice left.

## Q1 · Draft mode

Paper-AgreeablePrescriptionDiscretion: 28 minutes on the stuck Word, 40 to 80 seconds now (three runs), 13 of 14 displays opening their page. So skipping page tops would save seconds. For the PDF alone, `build.py --pdf-only` takes seconds.

```text
stuck Word     28 min    displays after their paragraphs
working Word   40-80 s   displays at page tops
```

**Do you still want a Word draft without page tops?**

- [ ] A · No; every Word copy keeps displays at page tops.
  [preview](tops-a.html)
- [x] B · Yes; drafts skip page tops, final copies keep them.
  [preview](tops-b.html)

Why A: About a minute is short enough, and nothing is lost.

Answer: B, changed from my pick A. Where the note below says otherwise, the note wins.

> note: JL in the chat: "don't use 1, we can use method B, as long as the table is at the top of that page, that should be okay"

## The pasted text

```text
haipipe-interaction answers · r01_collect_word_lane_speed · Word build speed · 2026-11-04
form: /blueprints/Project-Ladder/work/b16_theme_paper/j02_word_lane_speed/runs/r01_collect_word_lane_speed/r01_collect_word_lane_speed.html
built: 2026-11-04 11:45:58.736927
Q1 · Draft mode: B · Yes; drafts skip page tops, final copies keep them. (changed from A)
   note: JL in the chat: "don't use 1, we can use method B, as long as the table is at the top of that page, that should be okay"
```
