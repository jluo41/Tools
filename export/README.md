# export

A smaller repository can carry one part of this one: the skills of a few themes, the base skills they load, the
workbench host and pages that show them, and the installers. The part is a **profile** here; the smaller
repository is a **target**. Work happens here. A target only receives, so a fix is made once.

```text
export/profiles/<name>.yaml     what a profile takes: include (paths), exclude (globs), agents_from, map
export/export_profile.py        writes a profile, at one commit, into a target
```

A profile is named for what it holds (`insight-design`), never for who uses it. A target says who it is for in its
own files, which an export never writes: its `export.yaml` (the profile, and the files it keeps), `README.md`,
`AGENTS.md` and `.claude-plugin/marketplace.json`. The installers read the marketplace name from that file and the
source from the checkout's own git remote, so a target registers under its own name beside this repository.

## A target

```yaml
# <target>/export.yaml
profile: insight-design
keep:
  - README.md
  - AGENTS.md
  - .claude-plugin/marketplace.json
```

```bash
python export/export_profile.py <target> --check     # the skills and paths an exported file names but the profile leaves out
python export/export_profile.py <target> --dry-run   # what would be written and removed
python export/export_profile.py <target>             # export HEAD; --rev <commit> for another one
python export/export_profile.py <target> --commit    # and commit in the target, naming the source commit
```

## The rules

- **Only committed content travels.** Files are read from the commit (`git archive`), never from the working tree,
  so another session's unfinished edit stays here. `<target>/.export/source.yaml` names the commit.
- **A target's files are the profile's.** Each export writes them fresh and removes the ones the profile no longer
  takes (`<target>/.export/files.txt` lists the previous export). Nobody edits them in the target.
- **Before a target goes anywhere shared,** run `--check` and read what is left out, run the target's tests from
  inside it, and scan it for addresses, hosts and home paths. A profile excludes what does not belong; the fix for
  a private value is made here, in its source file.
- **A target with no share door** drops `cli/wb_share.py` and `_host/live/share.py`; the host starts without them
  and `/wb share` refuses.
