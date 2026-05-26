cc-session-summary
==================

Export and summarize a Claude Code session into a single, self-contained file.

---

Quick Reference
---------------

```
/cc-session-summary  [output_folder]
```

- output_folder is OPTIONAL — if omitted, Claude auto-detects the best folder
  based on which project directories were most active in the session.

Example (explicit folder):

```
/cc-session-summary  examples/ProjC-Model-WeightPredict/workspace
```

Example (auto-detect folder):

```
/cc-session-summary
```

---

What It Does
------------

1. 🔍  Finds the current session JSONL file automatically

2. 📥  Extracts all real user messages (filters tool results + system injections)
       Converts all timestamps to local time

3. 📂  Detects the best save folder by scanning which project directories
       were most active during the session

4. 🏷️  Generates a descriptive filename:
       cc_{YYMMDD}_h{HH}_{emoji}_{topic-slug}.md          (single hour)
       cc_{YYMMDD}_h{HH}t{HH}_{emoji}_{topic-slug}.md     (multi-hour)
       Examples:
         cc_260222_h10_🔧_weight-casefn-multiwindow.md
         cc_260222_h03t15_🗂️_recordset-pipeline.md

5. 📝  Writes ONE combined file with:
       - Session header + Topics at a Glance table
       - Per-topic blocks, each containing:
           · What Was Done (concise bullets)
           · Key Outcomes (files, bugs, decisions)
           · User Messages (verbatim, timestamped)
       - Complete files inventory
       - Next steps

---

Key Design Principle
--------------------

Each topic is SELF-CONTAINED.
You can read any topic and see both the summary AND the actual
user messages that drove that topic — no cross-referencing needed.

---

Files
-----

```
README.md    This file (quick reference)
SKILL.md     Full instructions for Claude
```
