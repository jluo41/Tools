# PP01 — every entry state, one each

## QX1 — a planned entry
### q-executor
Does the demo source exist and is it reachable?
### q-consumer
* Q-Seed-1 — "does it exist?"
### bank binding
**route**: task
**bank**: new
**target**: NEW tasks/T01_demo/QA/9-absent.md
**state**: planned
### a-executor

## QX2 — a correctly harvested entry
### q-executor
Does the demo source exist and is it reachable?
### q-consumer
* Q-Seed-2 — "does it exist?"
### bank binding
**route**: task
**bank**: reuse
**target**: tasks/T01_demo/QA/1-good.md
**state**: read
### a-executor
Yes: the demo store exists.

## QX3 — answered but never harvested
### q-executor
Does the demo source exist?
### q-consumer
* Q-Seed-3 — "does it exist?"
### bank binding
**route**: task
**bank**: reuse
**target**: tasks/T01_demo/QA/1-good.md
**state**: answered
### a-executor

## QX4 — a terminal concern
### q-executor
Is the construct measuring what it claims to measure?
### q-consumer
* Q-Seed-4 — "construct validity"
### bank binding
**route**: none
**state**: concern
### a-executor

## QX5 — read, but the target QA is a lying receipt
### q-executor
Does the second demo source exist?
### q-consumer
* Q-Seed-5 — "does it exist?"
### bank binding
**route**: task
**bank**: reuse
**target**: tasks/T01_demo/QA/2-lying.md
**state**: read
### a-executor
Claimed yes.
