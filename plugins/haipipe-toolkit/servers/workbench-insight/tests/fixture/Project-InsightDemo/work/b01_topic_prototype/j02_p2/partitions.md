---
partitions:
- name: full
  where: every row
  why: the whole extract
- name: part-a
  where: <filter A>
  why: <why A>
- name: part-b
  where: <filter B>
  why: <why B>
- name: cross
  of:
  - part-a
  - part-b
  why: one test of the difference
---

# The cuts

Part of the plan, fixed before any outcome.
