---
method: M05
name: Raw-data agent
type: By insight
family: Internal
card: servers/workbench-design/guide/methods/05-by-insight.md
versions:
- m1
- m2
- m3
current: m3
---

# M05 · Raw-data agent

An agent reads aggregate data of ours with its own tools, finds what to act on, and designs from its own findings, each cited; no signed handoff in between.

Its type is the Guide's card *By insight* (`05-by-insight.md`): the move, the literature and the tests come from there. A version below makes it concrete: its choice at each of the five steps.

- `m1.md`: the first version
- `m2.md`: from m1: ① sees the goal and the raw data's tools only, none of our insight (the benchmark beside the ladder); ② to ⑤ the input ladder's common steps
- `m3.md`: from m2: ① names its tool, `aggregate_query.py` beside it, the one door to the raw extract (grouped counts and rates, a group under 11 hidden, at most 30 queries, each kept with its receipt); ② to ⑤ as m2
