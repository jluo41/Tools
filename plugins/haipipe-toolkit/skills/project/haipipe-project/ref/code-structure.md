# Project-level code placement

Read `project.yaml.profile` before deciding whether root-owned code is legal.

## Research

A `research` Project does not own a root software package. Execution code
belongs to its BJTR Job/Task under `tasks/`; generated output belongs to the
Job or its consumer-owned store. Reusable SPACE libraries remain in the SPACE's
own code package, outside the Project.

Root `src/`, `scripts/`, `configs/`, `tests/`, and `docs/` are migration
debt for this profile. Do not move them automatically: first determine whether
the Project should be reclassified or the code belongs to a Job.

## Software

A `software` Project is itself a package or product repository. Conventional
root structure is valid:

```text
src/
tests/
scripts/
configs/
docs/
pyproject.toml or another build manifest
```

Tasks may describe development or evaluation work but should call the package,
not duplicate its implementation.

## Hybrid

A `hybrid` Project combines a root software artifact with research worlds.
The same no-duplication rule applies: root code owns the reusable product;
Task-owned `scripts/` own bounded experimental pipelines; Job `src/` owns
code shared only by sibling Tasks in that Job.

## Universal boundary

No profile permits root `results/`. Runtime output belongs to the Task/Job
contract or a consumer-owned store. Upstream repositories that are not the
Project's product belong under `external/` and remain read-only.
