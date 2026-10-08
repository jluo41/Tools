## 2026-09-28 · No content hashes (JL 260928)

- Local change to the vendored body: `KILL_ARGUMENT.json` records `audited_inputs` (paper-relative path to modification time) instead of `audited_input_hashes`. An audit is `STALE` when a listed file is newer than `generated_at`; no sha256 is written or rehashed.

## 2026-09-22 · vendored

- Copied from ARIS `skills/kill-argument` at `0472e53` (https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) as a project-provided skill the ideation family may call. Body unchanged; the frontmatter gained `metadata.haipipe` (vendored_from, vendored_on, local_changes). Adversarial attack/defense pass compared by `haipipe-idea-pressure-test`.
- Its `../shared-references/*.md` links are ARIS's shared folder and stay upstream paths; read them at `references/aris/skills/shared-references/`.

