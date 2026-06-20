Minimal Sandwich Dry Run
========================

This fixture shows the smallest useful completed run on disk.

It is not a runnable experiment. It is a reference shape for:

- one project-level append-only log
- one narrative
- one probe
- one discovery
- two tasks
- local `status.yaml` and `site.md` files that summarize local state

Read it in this order:

1. `_haipipe/project.log.jsonl`
2. `_haipipe/project.status.yaml`
3. `narratives/N001_toy-claim/site.md`
4. `probes/P001_first-check/site.md`
5. `discoveries/D001_prior-art/site.md`
6. `tasks/T001_baseline/site.md`
7. `tasks/T002_candidate/site.md`

The rule to notice: each object points to the next object's files. It does not
contain those files.
