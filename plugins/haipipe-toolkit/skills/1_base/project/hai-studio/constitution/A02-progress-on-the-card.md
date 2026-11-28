# A02 · Progress is seen on the card, without opening the drawing

> "What I mean is the hai-studio things, so that we want to make it work as we expected so when we reading the studio, we know the progress/" (JL 261118)
> "current the studio is not valid" (JL 261118, when the progress sat only inside Design B)

## 1. Need
On the workbench's Studio row, the s01 card alone should tell JL how far the setup is, without Open Draw.

## 2. Now
`five_parts.card()` (scripts/five_parts.py, `def card`) renders only elements within 1350 x 820 of the
canvas origin: Idea and Now. Progress was drawn in Design B (x around 1400+). `/wb` screenshot (261118
16:00) showed the card with Idea and Now, and no step states.

## 3. Gap
`five_parts.now()` drew only `spec["what"]["parts"]`, decided and open; there was no field a builder could
fill with live steps, so progress could only go into Design, outside the card's crop.

## 4. Methods
1. Widen the card crop: every card shrinks and becomes unreadable at card size; rejected.
2. An optional `spec["progress"]` drawn at the top of Now: inside the crop, opt-in, other topics unchanged. Chosen.
3. Put the steps into the face's Open list: Now shows only three open lines; rejected.

## 5. Update
- `scripts/five_parts.py`: `now()` draws `spec["progress"]` when given
- `s01-how-livesync-works/build_s01_how_livesync_works.py`: passes the live steps as progress

Cases: ✅ five_parts.now (every five-part topic can use it) · ✅ b01_livesync s01 · ⬜ draw.py topics (no Now part).
Run: `grep` for `spec.get("progress")` in five_parts.py and "setup progress, live" in the s01 canvas; ✅ (261118). The card PNG showed 10 steps with marks.

## 6. Never again
The writer (`five_parts.now`) now has the field, so any builder can put progress on the card. Open risk: a
topic that tracks work but never sets `spec["progress"]` still hides it; the Run line covers s01 only, not a
glob over every topic (asked by WorkBench-Project-UI, 261118; not yet done).
