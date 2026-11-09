---
partitions:
- name: full
  where: []
  why: every row
- name: first
  where:
  - column: group
    eq: group_1
  why: the largest group, asked on its own
- name: second
  where:
  - column: group
    eq: group_2
  why: the second group, asked on its own
- name: cross
  of:
  - first
  - second
  why: one test of whether the first and second groups differ
- name: third
  where:
  - column: group
    eq: group_3
  why: the small group, kept so the example shows a cut too thin to answer
---

# The cuts

Part of the plan, fixed before any outcome (run-set-cuts; a person signs them). `full` is every row; `first`,
`second` and `third` are the three made-up groups; `cross` holds no rows of its own and tests once whether the first
and second groups differ. `third` is small on purpose: a powered question refuses it with its minimum detectable
effect, and that refusal is an answer.
