# A04 · Design is drawn as pictures, never as small tables and long stickies

> "this is not vidid, should update this this again>" (JL 261118, a screenshot of s01's whole canvas)

## 1. Need
Opened in Excalidraw, s01's Design should catch the eye in seconds: the path of a note as pictures, the
state as a big number.

## 2. Now
JL's screenshot (261118): Design A was four small tables (`data_table`), B ten stickies whose words ran
past their edges ("QR ready on Desktop, scan it"), C long sticky lines. `excalidraw-studio/SKILL.md` rule ⑨
("vivid, never a wall of text") exists, and `check.py` passed: it fails only a frame with no picture and
over 600 words.

## 3. Gap
- `check.py` ⑨ counts words, so small tables and stickies pass while reading as a form.
- The sticky text width estimate (`quick_draw.WIDE` 0.62) is narrower than the font Excalidraw draws, so
  lines that fit in the builder overflow on screen.
- The `sketch_<topic>.py` stub `new_topic.py` writes starts A from `data_table`, steering every topic to tables.

## 4. Methods
1. Tighten check.py ⑨ to need icons and a big number in Design: right in spirit, but it touches every topic
   in every SPACE (about 4,000 builder files counted, many through the Tools link); left open.
2. Redraw s01 with pictures (computer, lock, database with its live count, cloud, laptop, phone), a 8/10
   scoreboard and stickies of at most 14 characters a line; add the rule and a Run line. Chosen now.
3. Only shorten the sticky words: fixes overflow, not vividness; rejected.

## 5. Update
- `s01-how-livesync-works/sketch_how_livesync_works.py`: icons lit by live state, scoreboard, short stickies

Cases: ✅ b01_livesync s01 A, B, C · ⬜ other five-part topics with a table-only Design, not audited.
Run: check.py passes and the s01 canvas has 20 or more ellipse and line shapes; ✅ (261118). Rendered PNG
showed the icons, "29,461" and "8/10".

## 6. Never again
The rule binds every agent through the constitution line in SKILL.md. Open risk, the main one: the writer
(`new_topic.py`'s stub) and the checker (`check.py` ⑨) are unchanged, so a new topic can still be drawn as
tables and pass; the Run line checks s01 only. Method 1 is the fix that would close it.


## 261119 · Reopened: it came back on s04

> "have you check the constintution that we want to make the vivid diagram??? /haistack to related skills to update the workflow." · "why you missed this again??" (JL 261119)

1. **Need**: the same as above, on every Studio topic, also when an agent only adds one node to an old drawing.
2. **Now**: on 261119 an agent added Sudip's plan 3 and email to b11 j02 s04-upload-path as boxes and text. It
   opened the topic's own `sketch_path.py` and never this constitution: the pointer sat only in
   `haipipe-studio/SKILL.md`, which a quick edit does not reload; the builder said nothing; the icons were private
   to s01's sketch, so drawing pictures meant copying code.
3. **Gap**: the open risk named above (writer and checker unchanged) is exactly what happened. Rules a reader must
   remember are lost on the next quick edit; only a rule the build itself says out loud holds.
4. **Methods**: (a) failing check.py ⑨ for every topic: still too wide (thousands of builders); (b) a warning in
   `five_parts.build`, printed on every rebuild of every five-part topic, plus the shared icons and a picture-first
   stub: chosen; (c) a memory note only: rejected, it is the same "remember to read" that failed.
5. **Update**: `scripts/icons.py` (new, the s01 icons plus server, shield, gate, cross, big_number,
   picture_count); `scripts/five_parts.py` `build()` prints `❗ A04 <topic>: Design has N picture shapes`;
   `templates/sketch.py.tmpl` A starts from icons; `excalidraw/SKILL.md` and `excalidraw-studio/SKILL.md` point
   here first; s04 A and B redrawn as pictures (phone, Cloudflare cloud and shield, the gateway as a gate, the
   Function App as a server, storage as a cylinder, a red cross and a big "2" failed deploys).
6. **Never again**: an agent that skips this file still runs the builder, and the builder now says ❗ A04 with the
   file to read. Every older table-only topic is a case that prints the warning on its next rebuild and is fixed then.
   Run line: s01 and s04 hold 20+ picture shapes, the warning, the stub and both door lines exist.
