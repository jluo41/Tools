Skill: cc-session-summary
=========================

Export and summarize a Claude Code session into a single, self-contained file.
Each topic includes what was done AND the user's actual messages — fully integrated.

On invocation, read this file fully, then execute Steps 1–5 below.

---

Invocation
----------

```
/cc-session-summary  [output_folder]
```

- output_folder   Optional. Path relative to project root.
                  If omitted, Claude auto-detects the best folder (see Step 3).
                  Example: examples/ProjC-Model-WeightPredict/cc-archive

---


Step 1 — Find the Session File 🔍
==================================

Run this Python snippet to locate the most recent session JSONL:

```python
import os, pathlib, json

project_root = os.getcwd()
slug = project_root.replace("/", "-")
projects_dir = os.path.expanduser(f"~/.claude/projects/{slug}")
files = sorted(pathlib.Path(projects_dir).glob("*.jsonl"),
               key=lambda p: p.stat().st_mtime, reverse=True)
session_file = str(files[0])
print(session_file)
```

The project slug is the project root path with slashes replaced by dashes.
Example: /Users/jluo/Desktop/WellDoc-SPACE  →  -Users-jluo-Desktop-WellDoc-SPACE


---


Step 2 — Extract All User Messages 📥
=======================================

Parse the JSONL and collect real user messages only.
Filter out: tool results, system continuations, interrupt messages.
Convert all timestamps from UTC to local time.

```python
import json
from datetime import datetime
from pathlib import Path

def extract_user_inputs(session_file):
    SKIP_PREFIXES = (
        "This session is being continued",
        "Please continue the conversation from where",
        "[Request interrupted by user]",
    )
    entries = []
    with open(session_file) as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("type") != "user":
                continue
            content = obj.get("message", {}).get("content", "")
            ts_raw  = obj.get("timestamp", "")
            # Skip tool results (content is a list with tool_use_id blocks)
            if isinstance(content, list):
                continue
            text = content.strip() if isinstance(content, str) else ""
            if not text:
                continue
            if any(text.startswith(p) for p in SKIP_PREFIXES):
                continue
            # Convert UTC → local time
            if ts_raw:
                dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                ts = dt.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
                dt_local = dt.astimezone()
            else:
                ts = "unknown time"
                dt_local = None
            entries.append({"ts": ts, "dt": dt_local, "text": text})
    return entries
```

Returns a list of dicts: `[{"ts": "...", "dt": datetime, "text": "..."}, ...]`


---


Step 3 — Auto-Detect Output Folder 📂
=======================================

If the user did NOT provide an output_folder, scan the session JSONL to find
which project folder was most active. Use that folder as the save location.

```python
import json, re
from collections import Counter
from pathlib import Path

def detect_output_folder(session_file):
    """
    Scan tool calls in the session for file paths accessed.
    Find the most-accessed top-level project subfolder (examples/, code-dev/, etc.)
    and use cc-archive as the save target subfolder.
    """
    folder_counts = Counter()
    top_level_folders = [
        "examples/",
        "Tools/plugins/research/skills/",
        "code-dev/", "code/", "config/", "_WorkSpace/",
    ]

    with open(session_file) as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            # Look in assistant tool_use blocks
            if obj.get("type") != "assistant":
                continue
            content = obj.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") != "tool_use":
                    continue
                inp = block.get("input", {})
                # Check file_path, command, and other string values
                for val in inp.values():
                    if not isinstance(val, str):
                        continue
                    for folder in top_level_folders:
                        if folder in val:
                            # Extract the specific subfolder and append cc-archive
                            idx = val.index(folder)
                            rest = val[idx:]
                            parts = rest.split("/")
                            if folder == "examples/" and len(parts) >= 2:
                                key = f"examples/{parts[1]}/cc-archive"
                            elif folder == "Tools/plugins/research/skills/":
                                key = "Tools/plugins/research/skills/cc-archive"
                            else:
                                key = folder.rstrip("/") + "/cc-archive"
                            folder_counts[key] += 1

    if folder_counts:
        best = folder_counts.most_common(1)[0][0]
        return best
    return "cc-archive"  # fallback
```

Print the detected folder so the user can confirm or override.


---


Step 4 — Generate Filename 🏷️
================================

Choose a filename that identifies this session at a glance.

Format (single hour):   cc_{YYMMDD}_h{HH}_{emoji}_{topic-slug}_{author}.md
Format (multi-hour):    cc_{YYMMDD}_h{HH}t{HH}_{emoji}_{topic-slug}_{author}.md

**Prefix distinction**:
  cc_  →  session export / transcript            (this skill — cc-session-summary)
  di_  →  discussion / planning / review log     (coding-by-logging skill)
Do NOT use cc_* for discussion docs. Keep them separate.

Rules:

  cc_          — Fixed prefix for session exports. Lets you find all logs instantly:
                   ls cc_*.md           all session exports
                   ls cc_260222*.md     all exports from one day

  YYMMDD       — Local date of the FIRST user message (2-digit year).
                 Example: 2026-02-22  →  260222

  h{HH}        — Local hour (zero-padded) of the FIRST user message.
  h{HH}t{HH}  — Use this form if session spans more than one hour.
                 h = start hour,  t = end hour (both zero-padded).
                 Examples:
                   h10          session starts and ends within 10:xx
                   h03t15       session runs from ~03:xx to ~15:xx

  {author}     — System username of the local user. Detect via:
                   import os; author = os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
                 Example: jluo, alice, bob

  {emoji}      — Pick ONE emoji that best represents the main theme:
                   🔧  engineering / building / debugging
                   🧠  research / design decisions / architecture
                   📊  data analysis / experiments / metrics
                   🚀  launch / deployment / new project setup
                   🐛  bug hunting / debugging session
                   📋  documentation / planning / review
                   🔬  modeling / ML / science
                   🗂️  data pipeline / ETL / preprocessing
                   ⚙️  configuration / infrastructure / setup

  topic-slug   — 3–5 word kebab-case summary of the session's main theme
                 Examples:
                   weight-casefn-multiwindow-design
                   mlpredictor-tlearner-inference
                   caseset-pipeline-debugging
                   aidata-config-and-training

Full example filenames:
  cc_260222_h10_🔧_weight-casefn-multiwindow_{author}.md
  cc_260222_h03t15_🗂️_recordset-height-weight-pipeline_{author}.md
  cc_260221_h22t02_🔬_mlpredictor-slearner-realdata_{author}.md

Pick the emoji, hour range, and slug by reading the session — do not ask the user.


---


Step 5 — Write the Combined Session File 📝
=============================================

Write ONE file to {output_folder}/{filename}.

The file has this structure:

  Part 1: Session header + Topics at a Glance table
  Part 2: One block per topic — summary + key outcomes + user messages
  Part 3: Files inventory + Next steps


Format Rules
------------

🔑  Use these EXACT heading conventions (NO ## or ### markdown headers):

    Top-level title:
        {emoji} Session Log — {Project Name} — {Topic}
        ================================================

    Topic headers:
        Topic 1 — <Topic Name> <emoji>
        ================================

    Sub-sections inside a topic:
        What Was Done
        -------------

        Key Outcomes
        ------------

        User Messages
        -------------

🔑  Emoji guidelines:
        🕐  Time / timestamps
        📁  Files created or modified
        🔧  Code built or fixed
        💡  Design decisions or discussions
        ✅  Completed / verified
        ❌  Error encountered
        🐛  Bug found and fixed
        📊  Data / analysis / visualization
        🗺️  Planning / overview
        📋  Documentation / export
        ⚠️  Important note or caveat
        🔜  Next steps / pending
        📨  Message reference

🔑  Each topic block must include ALL THREE sub-sections:

    1. What Was Done   — concise bullet summary (outcomes, not process)
    2. Key Outcomes    — files, decisions, bugs, results with emoji prefixes
    3. User Messages   — the actual verbatim user inputs for this topic,
                         each with its timestamp, formatted as:

        [N] `2026-02-22 10:39 EST`
        > User message text here, verbatim.
        > Wrapped naturally if long.

        (blank line between messages — no --- separator)


Template
--------

Paste this and fill in:

========================================================
{emoji} Session Log — {Project Name} — {Topic}
========================================================

🕐 Session span:  {first_ts}  →  {last_ts}
📨 Total messages: {N}
📂 Saved to: {output_folder}/{filename}

---


Topics at a Glance
------------------

| #   | Topic   | Time          | Messages |
|-----|---------|---------------|----------|
| 1   | <topic> | <start>–<end> | 1–N      |
| 2   | <topic> | <start>–<end> | N–M      |


---


Topic 1 — <Topic Name> 🗺️
===========================

🕐 <start_ts>  →  <end_ts>   (messages 1–N)

What Was Done
-------------

- <bullet 1>
- <bullet 2>
- <bullet 3>

Key Outcomes
------------

📁  <file created>  —  <what it is>
✅  <result>
🐛  <bug found and fixed>

User Messages
-------------

[1] `<timestamp>`
> <verbatim user message>

[2] `<timestamp>`
> <verbatim user message>


Topic 2 — <Topic Name> 📊
===========================

🕐 <start_ts>  →  <end_ts>   (messages N–M)

What Was Done
-------------

- ...

Key Outcomes
------------

...

User Messages
-------------

[N] `<timestamp>`
> <verbatim user message>


...


📁 Files Created This Session
==============================

| File              | Type    | Description      |
|-------------------|---------|------------------|
| path/to/file.py   | Builder | <what it does>   |
| ...               | ...     | ...              |


---


🔜 Next Steps
=============

| Priority | Task                           |
|----------|--------------------------------|
| 1        | <highest priority next action> |
| 2        | ...                            |


---


Writing Rules
=============

✅  Be concise in "What Was Done" — each bullet max 1–2 lines
✅  Focus on OUTCOMES not process ("Built X" not "Discussed and then decided to build X")
✅  Group related messages into one topic even if they span multiple back-and-forths
✅  Name topics descriptively: not "Discussion" but "WeightDay RecordFn Design"
✅  Always include bug/error entries with 🐛 — they are valuable for future reference
✅  User messages are verbatim — do NOT paraphrase or shorten them
✅  Every user message in the session must appear in exactly one topic
✅  The files inventory at the end must be COMPLETE — list every file touched


---


MUST NOT
========

❌  Do NOT use ## or ### markdown headers — use ===== and ----- only
❌  Do NOT summarize Claude's responses — only summarize WHAT WAS ACCOMPLISHED
❌  Do NOT paraphrase or edit user messages — they must be verbatim
❌  Do NOT skip the timestamp on any message
❌  Do NOT use UTC timestamps — always convert to local time
❌  Do NOT produce two separate files — everything goes in ONE combined file
❌  Do NOT ask the user to pick the filename or folder — determine both automatically
