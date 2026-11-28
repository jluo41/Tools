# A01 · Every article has a report, and the report is seen

> "and for each time, we should have a report, to explain what is the need, what current things do, and why current settings doesn't support it. ..." (JL 261118, chat)
> "and for this information, how do we save it in the disk folder, and how to present them in the UI?" (JL 261118, chat)

## 1. Need
Each time feedback becomes a rule, JL wants to read why: what he needed, what existed, why it fell short,
what was changed, and why it will not come back. He wants it on disk in a known place and visible in the
workbench, not only in a chat.

## 2. Now
`hai-studio/CONSTITUTION.md` A01 to A04 keep his words, Rule, Why, Class, Cases, Check, Run. The
"why it fell short" is one line (Why); methods weighed and the reason the fix holds are not written
anywhere. The file is read only in an editor; no workbench page shows it.

## 3. Gap
- `hai-stack/SKILL.md` article template had no Report field and no report step.
- `scripts/constitution.py --check` checked Run lines only, so an article with no reasons passed.
- `workbench/home/space_home.py` had no section that reads CONSTITUTION.md.

## 4. Methods
1. A longer Why inside the article: keeps one file, but the constitution turns into a wall; rejected.
2. A report file per article, linked from it, required by `--check`, listed on Home: chosen. The article
   stays short; the report holds the reasoning; the checker refuses a missing one.
3. Reports only in chat replies: lost after the session; rejected.

## 5. Update
- `skills/0_utils/hai-stack/ref/report.md`: the six parts and where the file goes
- `skills/0_utils/hai-stack/SKILL.md`: Report field, step 10, report-back shape
- `skills/0_utils/hai-stack/scripts/constitution.py`: `--check` ❗ on a missing report
- `servers/workbench/page/parts_and_map/space_constitution.py`: Home › 📜 Constitution
- `servers/workbench/home/space_home.py`: adds the section

Cases: ✅ this article · ✅ hai-studio A01 to A04 (reports written by their owner session; `--check` exit 0).

## 6. Never again
- The writer: step 10 makes the report part of every /hai-stack run, and Status may say solved only once it
  exists.
- The check: `constitution.py --check` exits 1 for any article without its report file, so
  `/hai-stack sweep` shows it as ❗.
- The reader: Home › 📜 Constitution lists every article in every SPACE, so a missing or open one is seen.
- Still open: nothing checks that a report's six parts are filled with real evidence; a reviewer reads it.
