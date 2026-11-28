# A Job's current results as a topic

Part of hai-studio's topic contract (`ref/topic-contract.md`).

A Job can have a topic that shows what its Runs have produced so far. It is an `sNN-<topic>/` beside the Jobs, and
the Block's page shows it with the Job marked. `scripts/job_results.py` makes it; its builder redraws it.

```bash
python $S/job_results.py <block>                                 # one topic per Job not drawn yet
python $S/job_results.py <block> --jobs j11_x,j12_y --slug <s> --title '<t>'   # a group of Jobs, a frame each
```

1. **From disk, every build**: each Task, each Run (`runs/<run>/result/`, or the older `results/<run>/`), its state
   and its headline values (a before and after pair as one: `acc 26.1% → 41.0%`), a source Run's title.
2. **Words in the face**: the `results:` yaml holds per Job its `reading` (the frame's key point), per Run the
   values to `show` (`at: <file>:<key>`), and the `open` points. The face's "Runs on disk" list is generated.
3. **More Jobs than the level's topic limit**: group the Jobs that share their Tasks into one topic, one frame per
   Job and a first frame with a row per Job.
4. **The whole Job** (why it exists, what goes in and out, what it concluded, its tables and pictures): draw it with
   `hai-draw job` (`job_drawing.py make <job>`), or `adopt` a one-Job results topic: its builder then calls
   hai-draw job, and its `results:` words move into a `job:` yaml.
