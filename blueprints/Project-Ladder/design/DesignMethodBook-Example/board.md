---
board-kind: design-method-book
serves: design/Design-Example
goal: The example's design method, one signed release at a time
---

# DesignMethodBook-Example · the example's design method

The recipe that turns a goal and its inputs into N designs, in five steps (① See input · ② Reason ideas · ③ Conduct
process · ④ Review item · ⑤ Review whole), one Job per release (`jNN_method-vN_<slug>/`), frozen once a person signs
it. A Design Board's Job pins one release and one inputs version (`method-vN × inputs-vM`); a release is cut from
`proposals/`. Every word here is a placeholder.

## Topic

Each release is cut from a registered method version in the Guide's library (`haipipe-design-method/methods/`), and
says which one in its `from:` line. The Board's Jobs and its experiment come back here as proposals; a person signs
the next release.

```text
DesignMethodBook-Example/
├── board.md                              this face; serves design/Design-Example
├── j01_method-v1_goal-only/              method-v1, from M01 m2: the goal and the shared rules only, signed
├── j02_method-v2_overall-performance/    method-v2, from M02 m1: adds past released designs, signed
└── proposals/                            the backlog: the next release is cut from here
```

## Releases

| release | from | ① sees | signed | used by |
|---|---|---|---|---|
| method-v1 | M01 m2 | Goal · how much is set | ✅ 261106 | j01, j02 |
| method-v2 | M02 m1 | Goal · how much is set · Examples | ✅ 261108 | j03 |
