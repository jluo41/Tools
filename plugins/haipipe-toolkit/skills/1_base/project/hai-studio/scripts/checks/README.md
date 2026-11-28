# Checks

Skills define methods and record contracts; servers present their records. Checks
validate named artifacts against those owners. They are read-only and runs
locally without a browser, model call, service restart or background watcher.

From the SPACE root, using its host Python environment:

```sh
python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/checks/run.py --target examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work
python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/checks/run.py --target examples/Project-Ladder/blueprint/b17_theme_work
```

Repeat `--target` for several topics. A file inside a topic selects that topic.
A Block selects only its registered, direct Studio topics. `--root` selects the
SPACE containing the records. No target means a usage error, not a global sweep.
New, untracked files are checked when they are in the named scope.

## Coverage

| Module | Checks | Owner |
|---|---|---|
| `manifest.py` | Valid manifest, unique names, contained real file/folder/Block bindings, live-page `url` items whose `path=` exists | Studio view format |
| `freshness.py` | Whole skill-folder tabs, generated requirements and Check view freshness; a type topic that carries its own `build_type_pages.py` is compared with that generator's `built(True)` | `skills_views.py`, `type_requirements.py`, `check_views.py`, the topic's own generator |
| `placeholders.py` | Bare numbered slots in generated Studio Types | `placeholder_check.py` |

`paths.py` and `results.py` supply path and result utilities. `run.py` selects targets and calls
the small modules. Existing owner scripts remain the source of their rules.
Ordinary topics with an embedded Skills view are not Skills topics. Other Studio
renderers are not regenerated as requirement pages.

The Check view reads criteria from its declared type's `elements.md`. Comparing
its generated HTML proves freshness only: it does not execute every criterion,
verify UI interaction, or change the instance's **Not verified** mark. Source
prose quality, other record kinds and runtime UI behavior are outside these checks.

## When to run

- After a batch of relevant artifact changes, check the affected topics once.
- `skills_views.py` checks its completed writes automatically before reporting success.
- After changing these checks, run `python -m unittest discover -s plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests -p "test_*checks*.py"`.

No CI, Git hook or file watcher is installed. Other writers are not automatically
covered. Add a module only for a recurring, observable rule with a good and bad
example; use the owning contract instead of inferring correctness from a page.

## Results

Each result gives its rule, target and a failure explanation or repair command.
Exit **0** means the applicable registered checks passed; **1** means a violation;
**2** means invalid scope, missing dependency, execution error or uncovered target.
No checks is never success. Block results cover only the selected Studio topics,
not every file or every requirement in that Block. Checks do not silently repair
files or convert incomplete execution into a pass. Resolve an error and rerun the
same scope before claiming it passed.
