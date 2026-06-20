# 4-edit — wiring (how the plugin loads this)

How the `haipipe` plugin discovers and exposes the pieces of `4-edit`, what is
live, and the one optional step.

## Discovery model (convention-based)

`.claude-plugin/plugin.json` lists no skills/agents/commands explicitly — the
plugin auto-discovers by convention:

| Piece | Discovered from | How it's invoked |
|-------|-----------------|------------------|
| **Skills** | `skills/**/SKILL.md` with a `name:` frontmatter | by skill name (e.g. invoke `haipipe-paper-edit`; `/haipipe-paper-edit` resolves to it) |
| **Agents** | top-level `agents/*.md` | as a `subagent_type` for the Agent tool |
| **Commands** | top-level `commands/*.md` | as `/command` |

## Status of 4-edit pieces

| Piece | Path | Registered? |
|-------|------|-------------|
| `haipipe-paper-edit` (orchestrator) | `skills/paper/3-edit/haipipe-paper-edit/SKILL.md` | ✅ on next reload (valid `name:`) |
| `haipipe-paper-edit-content` + 5 topic stubs | `skills/paper/3-edit/paper-edit-*/SKILL.md` | ✅ on next reload |
| 4 stage agents | `skills/paper/3-edit/agents/*.md` | ⚠️ **not** as `subagent_type` (nested, not in top-level `agents/`) |
| `/haipipe-paper-edit` command | — | n/a — invoked by skill name, like every skill here |

> Skills created mid-session aren't hot-loaded; `haipipe-paper-edit` etc. appear in the
> skill list after the next Claude Code reload. (That's why they're absent from
> the current session's list — they exist on disk and are valid.)

## The agents: two ways to run them

The plugin registers agents by **symlinking nested `skills/.../agents/*.md` into
the top-level `agents/`** (e.g. `agents/claim-verifier-agent.md` →
`../skills/probe/agents/reviewers/claim-verifier-agent.md`). Our 4 agents are
nested but **not yet symlinked**, so they are not first-class `subagent_type`s.

**Option A — inline dispatch (default, works today, no registration).**
The orchestrator spawns each stage by **reading `agents/paper-edit-<stage>.md` and
passing its body as the Agent-tool prompt**. No `subagent_type` needed; fan-out
works now. This is what `haipipe-paper-edit/SKILL.md` instructs.

**Option B — register as `subagent_type`s (optional, matches plugin pattern).**
Add relative symlinks into the top-level `agents/` so they can be dispatched by
name. From the plugin root (`Tools/plugins/haipipe-toolkit/`):

```sh
cd agents
for a in format-checker annotator improver cleaner; do
  ln -s ../skills/paper/3-edit/agents/paper-edit-$a.md paper-edit-$a.md
done
```

Note (Windows): this repo's existing `agents/` symlinks are git symlinks that
check out as plain text when `core.symlinks=false`. Create these on a checkout
with symlinks enabled, or via `git update-index --cacheinfo 120000,…`, so git
records them as real symlinks. Option A avoids this entirely.

## Verifier script

`scripts/check_comment_only.sh` gates that a pass changed no prose:

```sh
scripts/check_comment_only.sh           <orig.tex> <new.tex>   # annotate / comment-only gate (prose byte-identical)
scripts/check_comment_only.sh --mode words <orig.tex> <new.tex>   # format-check gate (same words, re-wrap allowed)
```

Exit 0 = pass, 1 = prose changed, 2 = usage error. The orchestrator should run it
after Stage 1 (`--mode words`) and Stage 2 (default) on every touched file.

## Checklist to go fully live

- [ ] Reload Claude Code so the skills register (then `haipipe-paper-edit` is invocable).
- [ ] (Optional) Symlink the 4 agents into top-level `agents/` for first-class
      `subagent_type` dispatch — otherwise inline dispatch is used.
- [ ] Wire `scripts/check_comment_only.sh` into the orchestrator's verify step
      (already referenced in `haipipe-paper-edit/SKILL.md`).
