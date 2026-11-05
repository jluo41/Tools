# Word build speed

for: b16.j02-s22:theme_paper.word_lane_speed @ word_lane_speed

Word was stuck, not slow. On a working Word a whole build took 40 to 80 seconds. Builds now take turns in Word. One choice left.

## Q1 · Draft mode

Paper-AgreeablePrescriptionDiscretion: 28 minutes on the stuck Word, 40 to 80 seconds now (three runs), 13 of 14 displays opening their page. So skipping page tops would save seconds. For the PDF alone, `build.py --pdf-only` takes seconds.

```text
stuck Word     28 min    displays after their paragraphs
working Word   40-80 s   displays at page tops
```

**Do you still want a Word draft without page tops?**

- [x] A · No; every Word copy keeps displays at page tops.
  [preview](tops-a.html)
- [ ] B · Yes; drafts skip page tops, final copies keep them.
  [preview](tops-b.html)

Why A: About a minute is short enough, and nothing is lost.
