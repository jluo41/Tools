# The scripts

Part of haipipe-studio's topic contract (`ref/topic-contract.md`).


```text
scripts/canvas.py        the merge-safe writer (moved here from a design Block's studio/_build/)
scripts/render_png.py    the offline PNG preview (moved the same way)
scripts/new_topic.py     topic · session
```

Every builder imports these from here (the copies in a design Block's `studio/_build/` are
retired). A Block that still keeps older snapshots by stem in a folder of its own
(`.<stem>.seed.json`, from before snapshots sat beside their drawings) can append that folder
to `canvas.LEGACY_DIRS`; better, move each snapshot beside its drawing.
