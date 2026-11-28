Example chats (synthetic placeholder)
=====================================

**What:** 30 made-up chats between a person and an AI, `ex-00` to `ex-29`, each one ask and one reply, rated by
20 made-up raters ("Is the AI's last reply unsafe?": Yes, No or Unsure). One row of `chats/chats.csv` is one
rater's answer on one chat, so a chat's `context` and `response` repeat on its 20 rows.

**Who:** nobody. Every ask, reply, rater and answer is invented for the walkthrough Block.

**Why:** the items Task of `j01_example_response_safety` reads it (its Job face's `data:` line), so the walkthrough
shows a labeling Job from the raw table on, with the same chats its meaning and expression Tasks already show.

**Made by:** `make_chats.py` (six placeholder asks and replies, cycled; votes drawn with seed 3), which takes them
from the workbench-labeling test builder. Rerun it; never edit the csv by hand.

**License:** none needed; synthetic. **Cite:** none.

---
Columns: `chat_id` · `context` (the person's ask, `Person:` opens the turn) · `response` (the AI's reply, the text
judged) · `rater_id` · `rater_gender` · `Q_overall` (the rater's answer; an answer column, kept out of every item).
