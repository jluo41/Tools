# q-executor
🧱 STAKE FORBIDDEN · this is the ONLY file that is dispatched.

How many outline plans in this repo pass all four self-consistency checks, and which check fails most often?

**Where to look**
`haipipe-board/src/plan_shape.py` implements all four: `check_coverage`, `check_serves`, `check` (shape), and `checks/values.py` for the value one. Every plan is at `<page>/outline/<stem>-outline-v<N>.md`; use the highest version per page.

**What a complete answer contains**
The number of plans found, the number passing all four, and a count per check of how many plans it fails. Name the pages behind each count rather than only the totals.

**How to return it**
Counts with the command that produced them. If a check cannot run on some plans, say which and why rather than excluding them silently.
