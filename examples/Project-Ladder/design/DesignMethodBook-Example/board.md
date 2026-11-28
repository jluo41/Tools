---
board-kind: design-method-book
channel: sms
serves: design/Design-Example
goal: The example message designer, the method types it uses, each version signed
---

# DesignMethodBook-Example · the example message designer

A designer for one channel: here, sms (`channel:`, the same line its Board carries). The channel's own rules are
the Guide's venue pack (`venue/venue-sms/`); the application's shared rules stay on the Board, signed there. It holds the method types it uses, one Job per
type (`jNN_M0x-<slug>/`), and inside each the versions a person signed (`mK.md`, frozen). A method type says how much
a design sees (the goal only, past designs, the insight's evidence); a version says how its five steps are written
(① See input · ② Reason ideas · ③ Conduct process · ④ Review item · ⑤ Review whole). A Design Board designs the same
kind of thing on one set of materials, and each of its Jobs pins one type, one version and one inputs version
(`M0x-<slug>-mK × inputs-vM`). Every word here is a placeholder.

## Topic

The types come from the Guide's library (`hai-design-method/methods/`), which every designer shares. Types sit
side by side and are compared; only a new version of one type is a change to it. A method does not change when the
materials do: new materials are a new inputs version on the Board. The Board's Jobs and its experiment come back
here as proposals; a person signs the next version.

```text
DesignMethodBook-Example/
├── board.md                        this face; channel sms; serves design/Design-Example
├── j01_M01-goal-only/              M01: the goal and the shared rules only; m2 signed
├── j02_M02-overall-performance/    M02: adds past released designs; m1 signed
└── proposals/                      the backlog: the next version of a type is cut from here
```

## Method types

| type | version | ① sees | signed | used by |
|---|---|---|---|---|
| M01 goal only | m2 | Goal · how much is set | ✅ 261106 | j01, j02 |
| M02 overall performance | m1 | Goal · how much is set · Examples | ✅ 261108 | j03 |
