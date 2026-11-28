# A02 · No "JL 26xxxx" tags on a page

> "do not add the things like this in the UI, totally avoid this" (JL 261113)

## 1. Need
A page shows the work, not who asked for its design or when.

## 2. Now
Code comments carry "JL 2611xx" tags by design. The 261118 scan found tags shown on pages: Studio topic
subtitles taken from faces ("(JL 261030)", "(JL 261029, meeting …)") on Physician 5599 and the Tools test hosts,
and commit messages on the Timeline ("env.sh secrets blanked (JL 261103)").

## 3. Gap
- Faces and topic descriptions are written by agents that copy the tag habit from code comments.
- The page shows a face's line as-is, so the tag passes through; no check read the result.

## 4. Methods
1. Strip tags at render time: hides them, but also edits content a person wrote (a commit message); rejected.
2. Scan what pages show, then fix the writer (the face or the skill that writes it): chosen.
3. Ban tags in faces by a face checker: worth adding per theme once the scan shows which faces.

## 5. Update
- `hai-ui/scripts/page_words.py`: flags every visible `JL 2xxxxx`
Cases: ⬜ Studio subtitles from faces · ✅ Timeline commit messages (content as written, allowed) · ⬜ others.

## 6. Never again
- `/hai-stack sweep` rescans; a new tag on any page turns this article ❗.
- Still open: telling content a person wrote from text an agent wrote needs a look; the scan lists, a
  person or reviewer decides.
