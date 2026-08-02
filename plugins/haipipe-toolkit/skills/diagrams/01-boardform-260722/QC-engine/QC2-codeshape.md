# The code's shape: one Law, three files

state: 🟡 PARTIAL · two files split, the folder's shape settled, the live layer's last item open
owner: JL
method: every split is a mechanical move under an output-identical gate, features second; a module is named for what it renders or serves, never for its layer (JL 260724)
session: 83eefb3a-b51d-4ef6-9383-05b7e994f893
## Opening
How should the Board code be split as it grows without changing what it produces or how consumers use it?

Large files make each new feature harder to place, review, and test.
The risky part is preserving one parser and the same static output while code moves across modules.
The answer governs the renderer, browser assets, and live server rather than any single refactor.
It succeeds when each split is mechanically provable and every module has one recognizable job.

**Covered elsewhere**: `build.py` → `assets/`: `QC2a`. The `src/` render split: `QC2b`. `serve.py` → `live/`: `QC2c`. What SKILL.md exports about all this: `QC1`. The round trip the split files sit inside: `QC4`.

## Diagram

```
   one Law ── "mechanical move under an output-identical gate, features second"
        │
        ├── 🏗  build.py  →  assets/*.css *.js       QC2a  ✅ the template out of the parser
        ├── 🧩  src/ modules, named by what they render QC2b  ✅ page_question.py page_stage.py
        └── 🔌  serve.py  →  live/ mixins + thin CLI   QC2c  🟡 the live layer, moved area by area
```

## Content
### §1 Why one Law, three files
`QC2a` moved the CSS/JS out of `build.py` so the grammar stayed but the 800-line JS string left.
`QC2b` split the render Python into `src/` modules named for the page they render, giving each future feature a seat before it is written.
`QC2c` is `QC2b`'s deferred half: the same move on `serve.py`, held back only while the live layer was still forming.
Each face records its own gate; this page records only that the gate is the same one every time.

### §2 The folder's own shape, not just each file's
Splitting big files inward left a second problem untouched: what the engine folder LOOKS like from outside.
JL saw it through the new RELATED FOLDERS browser (260801): "为什么有那么多 .py 文件是在最外面的?它不应该放到哪一个文件夹内部吗?" — 25 loose `.py` at the top level, 11 of them tests.
The browser did not cause the mess; it made a mess that had been accumulating visible, which is the argument for having it.
The tests moved first because they were free: nothing imports them, so `tests/` cost one `conftest.py` and one re-pointed `HERE`, and the suite still reports the same 50 passed.
The remaining 14 were then defended with a reference count: `serve.py` named 73 times outside this folder, `build.py` 64, `stage.py` 51, `check.py` 50, so moving them would be a repo-wide migration rather than a tidy.
That reasoning was wrong, and correcting it is the useful part. A reference count measures how much DOCUMENTATION would drift, not what would break: of those hundreds of mentions only 15 actually EXECUTE a path, in 6 `SKILL.md` files. The real rule is simpler and is what JL said: **a skill folder presents `SKILL.md` and folders; runnable scripts live in `cli/`, the render library in `src/`, the server in `live/`, the suite in `tests/`.**
One file is exempt and the exemption is external: `status.py` is invoked by the reply-footer automation with an absolute path, so it stays at the top level.
What no test could have caught, and `check.py` did: the board's own `## Links` still named the old paths, so 96 rendered hrefs went dead the moment the files moved. That is the argument for running the checker after a move, not just the suite.

## Aims
- [x] 🧪 build.py's template split out under a byte-identical gate (QC2a)
- [x] 🧪 the src/ render split, modules named by what they render (QC2b)
- [ ] 🧠 the live layer's last sequencing item (QC2c) closes before this topic is done
- [x] 🗂 The 11 tests left the top level for `tests/` (260801)
      Baseline first (50 passed), then `git mv`, then `tests/conftest.py` to put the engine dir on `sys.path`, then `HERE`/`root` re-pointed one level up so `HERE / "serve.py"` and `root.parents[1]` still mean what they meant. 50 passed again; `SKILL.md`'s file table now names `tests/`.
- [x] 🗂 The 13 runnable scripts moved into `cli/` (260801, JL ruled)
      The top level is now `SKILL.md`, `CHANGELOG.md`, `status.py`, and folders. `status.py` stays because the reply-footer automation invokes it by absolute path.
      The first costing was wrong and is worth keeping as the lesson: 73/64/51/50 counted PROSE mentions on board pages. What decides a migration is how many places EXECUTE a path, and that was 15, in 6 `SKILL.md` files.

## States
Two of three files are split and settled; the live layer split is built and serving, with one sequencing item left because QD2's chat is about to be rewritten as a session host.
The folder's own shape is settled: 25 top-level `.py` → 1. The engine now presents `SKILL.md`, `CHANGELOG.md`, `status.py`, and folders (`cli/ src/ live/ tests/ checks/ assets/ ref/ vendor/`).

- 260801 JL · 🗂 The top level was called out, and the tests moved
      JL, reading the RELATED FOLDERS browser: "为什么有那么多 .py 文件是在最外面的?它不应该放到哪一个文件夹内部吗?我感觉这样不行,这个结构很差."
      He is right, and the browser earning its keep on its first day is the incidental result: it made a slow accumulation visible in one screen.
      The free half shipped immediately: 11 `test_*.py` into `tests/`, guarded by a before-and-after suite run (50 passed → 50 passed) rather than by inspection, since `HERE` silently meant "the engine dir" in seven files and `root.parents[1]` in one more.
      The second half was first deferred behind a reference count, and JL pushed back: "你为啥不放在 src 里面 ... 它本身是一个 skill folder." He was right and the count was measuring the wrong thing: only 15 of those mentions execute a path. All 13 runnable scripts then moved into `cli/`, and `check.py` caught what the suite could not, 96 dead hrefs from `## Links` still naming the old paths, now back to 0.

### Decision Now
- [ ] 🧠 JL confirms the split family reads as one topic now that the three pages sit under QC2
- [x] 🗂 Rule the top level: JL ruled all of them into folders (260801)
      JL: "你为啥不放在 src 里面,反而把它放在外面? ... 因为它本身是一个 skill folder,你这么多 Python 的文件放外面,感觉不对吧?"
      Done as `cli/` rather than `src/`, because `src/` is the render LIBRARY and these 13 are all executable entries (every one has `__main__`); mixing them would lose the distinction the QC2b split was for.

## Files
- `cli/build.py` · `src/` · `cli/serve.py`
  The three files the Law is applied to; the two entries moved into `cli/` on 260801.
- `QC-engine/QC2a-buildsplit.md` · `QC-engine/QC2b-srcsplit.md` · `QC-engine/QC2c-livesplit.md`
  The family, one file each.

## Log
260801 1330 · The 13 runnable scripts moved into cli/ on JL's ruling (top level = SKILL.md + CHANGELOG.md + status.py + folders); HERE re-pointed to the engine dir in 12 scripts, tests/conftest.py now adds cli/, 6 SKILL.md command paths rewritten, board.md ## Links repointed; 50 passed and check.py 96 error -> 0 error. Board Map also shut by default (JL: "默认的话就合起来")
260801 1200 · The 11 test_*.py moved to tests/ on JL's "这个结构很差" (25 top-level .py -> 14): baseline 50 passed, conftest.py added, HERE/root re-pointed one level up, 50 passed again, SKILL.md file table updated; the remaining 14 are costed in Decision Now by external reference count
260801 0140 · Repointed sibling ref QC7 -> QC4 after the full renumber (JL 260801)
260801 0130 · Opened as the split family's parent overview when QC2/QC3/QC8 were regrouped into QC2a/QC2b/QC2c (JL 260801)
