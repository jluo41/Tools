CODE-PULLING.md — Git Workflow for This Repo
============================================

This repo (Tools) is a git repo that contains nested submodules.
Pushing and pulling requires working in the right repo in the right order.

---

Repo Structure
--------------

```
WellDoc-SPACE/               (outer repo: github.com:JHU-CDHAI/WellDoc-SPACE)
+-- Tools/                   (submodule: github.com:jluo41/Tools)
    +-- plugins/
        +-- research/        (submodule: github.com:jluo41/research-skills)
        +-- logseq/          (submodule: github.com:jluo41/logseq-skills)
        +-- chronicle/       (submodule: github.com:jluo41/chronicle-skills)
```

Three separate git repos, nested two levels deep.
Changes must be committed and pushed innermost-first.

---

PULLING (getting latest code)
==============================

From the WellDoc-SPACE root, pull everything recursively:

```bash
git submodule update --init --recursive
```

This pulls Tools and all plugin submodules in one command.

To also pull the latest from each submodule's remote (not just the pinned ref):

```bash
git submodule update --remote --recursive
```

---

PUSHING (sending changes)
==========================

Push must go innermost-first: plugin → Tools → WellDoc-SPACE.

The problem: submodules are checked out in DETACHED HEAD by default,
which means `git push` does not know which branch to push to.

Always check out `main` before committing in a submodule.

Step 1: Push changes inside a plugin (e.g., research)
------------------------------------------------------

```bash
cd Tools/plugins/research

# Check current state
git status
git branch      # if showing "(HEAD detached at ...)", check out main first

# Switch to main if in detached HEAD
git checkout main
git pull        # sync with remote before making changes

# Stage and commit
git add <changed files>
git commit -m "your message"
git push origin main

cd ../..   # back to Tools/
```

Step 2: Update Tools to point at the new plugin commit
------------------------------------------------------

```bash
cd Tools     # must be in Tools root

git checkout main
git pull

git add plugins/research   # (or whichever plugin changed)
git commit -m "Update research submodule"
git push origin main

cd ..        # back to WellDoc-SPACE/
```

Step 3: Update WellDoc-SPACE to point at the new Tools commit
-------------------------------------------------------------

```bash
cd WellDoc-SPACE   # or just stay at root

git add Tools
git commit -m "Update Tools submodule ref"
git push origin main
```

---

COMMON PROBLEMS
===============

Problem: "HEAD detached" after git submodule update
----------------------------------------------------

git submodule update checks out a specific commit, not a branch.
Always run `git checkout main` inside the submodule before making changes.

```bash
# Diagnosis
cd Tools/plugins/research
git branch   # shows "(HEAD detached at abc1234)"

# Fix
git checkout main
git pull
```

Problem: "non-fast-forward" push rejected
------------------------------------------

Remote has commits you don't have locally. Pull first.

```bash
git pull        # fast-forward if no local commits
# or
git pull --rebase   # if you have local commits to rebase on top
git push origin main
```

Problem: "untracked files would be overwritten by merge"
---------------------------------------------------------

A file exists locally that the remote wants to create.
Save it, remove it, pull, then restore.

```bash
cp <file> /tmp/<file>.bak
rm <file>
git pull
# re-apply your changes
```

Problem: staged changes blocking pull
--------------------------------------

Stash, pull, pop stash.

```bash
git stash
git pull
git stash pop
```

---

QUICK REFERENCE
===============

Task                                Command
----------------------------------  -----------------------------------------
Pull all submodules (pinned refs)   git submodule update --init --recursive
Pull all submodules (latest remote) git submodule update --remote --recursive
Check which branch you are on       git branch
Switch to main in submodule         git checkout main && git pull
Push a plugin change                cd plugins/<name> && git push origin main
Update Tools ref after plugin push  git add plugins/<name> && git commit && git push
Update outer repo after Tools push  cd .. && git add Tools && git commit && git push
See all submodule states            git submodule status --recursive
