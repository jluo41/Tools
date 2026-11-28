# Items recipe choices

for: b02.j01.t01-s02:labeling_walkthrough.example_response_safety.example_items @ example_items_recipe

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form. -->

The recipe is proposed from the Data cards; these three choices are what your sign rests on.

## Q1 · The text judged
The label is about one text per chat; the rest is context.
```text
Person: <the ask>     context before
AI: <the reply>       judged
```
**Which text is judged?**
- [x] A · The AI's reply; the person's ask is context before it.
- [ ] B · The whole chat, ask and reply, as one text.
Why A: The label asks whether the AI's last reply is unsafe.

## Q2 · Item ids
The meaning and expression Tasks already name the chats ex-00 to ex-29.
**Which id does each item take?**
- [x] A · The chat's own id, ex-00 to ex-29.
- [ ] B · A new id from the dataset's name, examplechats-ex-00.
Why A: One id for a chat across the Job's three Tasks.

## Q3 · Embed build
Step 3 maps the items into groups; the build is agreed before it runs.
**Which build embeds the items?**
- [x] A · tfidf-svd: word counts, fast, no model to download.
- [ ] B · A sentence model, all-MiniLM-L6-v2, once it is installed.
Why A: Thirty short chats; the map only needs to group them.
