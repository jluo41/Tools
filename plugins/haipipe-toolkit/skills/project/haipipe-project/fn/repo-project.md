fn-repo-project: Create a Repo-Backed Project (GitHub repo + submodule)
=========================================================================

Creates a project that is its OWN git repo on GitHub, added as a submodule of the workspace. Papers inside it are submodules of the project (nested submodules).

Naming convention decides the kind:

```
Proj{A,B,C,D}-*   legacy plain directory inside the workspace (fn/project.md)
Project-*         repo-backed: own GitHub repo + submodule (THIS fn)
```

Parameters (NO baked-in org -- this skill serves many workspaces and owners):

```
--org <owner>      REQUIRED, resolved in this order:
                   1. explicit --org flag
                   2. ASK the user, suggesting candidates from the workspace's
                      existing .gitmodules URLs and `gh api user/orgs`
                   Never assume an org.
--private          default visibility (confirm if the user wants public)
location           examples/<Project-Name> (default)
```

The nesting picture:

```
Physician-SPACE                          (workspace repo)
└── examples/Project-<Name>/            submodule -> github.com/<org>/Project-<Name>
    └── papers/Paper-<X>-<Venue>/       submodule OF THE PROJECT -> its own paper repo
```

Why repo-backed: the project is SELF-CONTAINED and org-shareable. Collaborators clone `<org>/Project-<Name>` (with its papers) without receiving the whole workspace. The paper submodule URLs live in the PROJECT's `.gitmodules`, not the workspace's.


Step 0 -- Preflight (all must pass before creating anything)
------------------------------------------------------------

```sh
gh auth status                                   # authenticated?
gh repo view <org>/<Project-Name> 2>&1           # exists → ADOPT mode; free → CREATE mode
ls examples/<Project-Name> 2>&1                  # must FAIL (path free)
git -C . rev-parse --show-toplevel               # confirm we are in the workspace root
```

Org must be resolved (flag or ask) BEFORE preflight; there is no default org.

ADOPT mode: if the repo already exists under the org, do NOT stop and do NOT recreate -- just pull it: skip Step 1, go straight to Step 2 (submodule add clones the existing content), then in Step 3 create only the container folders that are missing. Never force-push over existing history.

If auth fails or the local path is already taken, STOP and report. Never overwrite an existing path.


Step 1 -- Create the GitHub repo (empty, private; SKIP in ADOPT mode)
----------------------------------------------------------------------

```sh
gh repo create <org>/<Project-Name> --private
```


Step 2 -- Add as submodule of the workspace
--------------------------------------------

From the workspace root:

```sh
git submodule add git@github.com:<org>/<Project-Name>.git examples/<Project-Name>
```

(Cloning an empty repo warns; that is fine. The pointer records after the first push.)


Step 3 -- Scaffold inside the project
--------------------------------------

```
examples/<Project-Name>/
├── README.md          # repo front page: 2-3 sentences, what this project studies
├── .gitignore         # _WorkSpace/, .paper-console.yaml, .probe-console.yaml, *.aux etc.
├── tasks/             # internal structure owned by /haipipe-task
├── probes/            # internal structure owned by /haipipe-probe
├── discoveries/       # internal structure owned by /haipipe-discovery
├── insights/          # internal structure owned by /haipipe-insight
├── diagram/           # EMPTY at setup; authored later via /diagram-ascii on request
└── papers/            # papers land here, each as a submodule of THIS repo (/haipipe-paper-*)
```

Create the top-level folders only (ADOPT mode: create only what's missing). Each world's internal structure is scaffolded later by its owning skill when first used; this fn never restates their rules.

Repo-backed projects DO get a top-level `README.md` (it is the repo's front page). The plain-dir rule "no README at top level" applies only to fn/project.md projects.

QUICK BY DEFAULT: setup = folders + README + .gitignore, nothing else. No metadata questionnaire, no diagram authoring. If the user explicitly asks for the project diagram, collect (research question, why it matters, in/out of scope) and author `01-story.txt` + `02-boundary.txt` via `/diagram-ascii`, one call per file; otherwise `diagram/` stays empty.


Step 4 -- First push (inside the project)
------------------------------------------

```sh
cd examples/<Project-Name>
git add -A && git commit -m "Scaffold <Project-Name>: container folders"
git branch -M main
git push -u origin main
```


Step 5 -- Bump the workspace pointer
-------------------------------------

```sh
cd <workspace-root>
git add .gitmodules examples/<Project-Name>
git commit -m "Add Project-<Name> as submodule (<org>, private)"
```


Papers inside a Project-* repo
-------------------------------

Each paper is a submodule OF THE PROJECT, one level down. Same recipe relative to the project:

```sh
gh repo create <org>/Paper-<X>-<Venue> --private            # paper may use a different owner
cd examples/<Project-Name>
git submodule add git@github.com:<org>/Paper-<X>-<Venue>.git papers/Paper-<X>-<Venue>
# scaffold the paper folder via /haipipe-paper-lifecycle folder, commit, push
```

The paper's URL goes into the PROJECT's `.gitmodules`. The workspace never lists it.


The double-bump ceremony (REQUIRED knowledge)
----------------------------------------------

Nested submodules update INSIDE-OUT. An inner commit is invisible upstream until each parent bumps its pointer:

```
edit paper        → commit + push in the paper repo
                  → cd project:   git add papers/<...>; commit "bump paper ref"; push
                  → cd workspace: git add examples/<...>; commit "bump project ref"
```

One bump per work session is enough (not per commit). Fresh clones need `git clone --recurse-submodules` or `git submodule update --init --recursive`.


Report
-------

Print: repo URL, submodule path, scaffold tree, and next steps:
`/haipipe-paper-lifecycle folder <paper-path>` (first paper) or `/haipipe-task` (first task-group).
