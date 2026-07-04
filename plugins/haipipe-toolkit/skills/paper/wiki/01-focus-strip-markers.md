# Focus Strip Markers: 🔥 and 🚀

The two-line focus strip uses two distinct markers on both the stage line and the phase line.

## Markers

| Marker | Meaning |
|---|---|
| 🔥 | **Active now** -- the stage or phase we are currently working on |
| 🚀 | **Frontier** -- the farthest stage or phase the paper has ever reached |
| ✅ | Completed (artifact exists on disk with real content) |
| ⬜ | Not started |
| -- | Skipped (not applicable to this stage/section) |

## Rules

1. 🔥 and 🚀 can coexist on the same line. They mark different things.
2. When 🔥 and 🚀 land on the same stage or phase, collapse to `🔥🚀`.
3. The **stage line** has at most one 🔥 and one 🚀.
4. The **phase line** has at most one 🔥 and one 🚀.
5. The phase line always describes the 🔥 stage's phases.
6. `cite`/`val`/`disp` are the probe phase's sub-tracks. Stages without them show a single `probe ⬜` / `probe --` slot instead.

## Examples

**Redoing seed while paper has reached section-edit:**
```
stage:   seed 🔥  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  section-edit 🚀
phase:   draft 🔥🚀  │  probe: cite ⬜  val ⬜  disp ⬜  │  revise ⬜  │  check ⬜
```
- 🔥 seed: we are actively reworking the seed right now
- 🚀 section-edit: the paper had reached section-edit before this session
- draft 🔥🚀: within seed, draft is both where we are and the farthest phase

**Working at the frontier (active = frontier):**
```
stage:   seed ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  section-edit 🔥🚀
phase:   draft 🔥🚀  │  probe: cite ⬜  val ⬜  disp ⬜  │  revise ⬜  │  check ⬜
```
- 🔥🚀 collapsed: we are working at the frontier, pushing it forward

**Loopback to pitch while frontier is display:**
```
stage:   seed ✅  claims ✅  venue ✅  pitch 🔥  narrative ✅  display 🚀  section-edit ⬜
phase:   draft ✅  │  probe: cite ⬜  val --  disp --  │  revise 🔥🚀  │  check ⬜
```
- 🔥 pitch: loopback to revise the pitch
- 🚀 display: the paper had reached display stage

## Why two markers

A paper often loops back: redo seed after results shift, revisit pitch after a reframe, update claims mid-editing. One marker cannot show both "where I am" and "how far this paper has gotten." Two markers keep both visible in one glance.
