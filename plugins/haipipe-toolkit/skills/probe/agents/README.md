# Probe agents · retired

There are no live agents in this directory. The former question collector was
removed when Task and Discovery moved to the shared Run/Result contract.

For new work, SURVEY records Execution or Discovery Supporting Runs directly;
LAND consumes their Results through one frozen Local Input and one local Page
Run. The current contracts are:

```text
board/page-plugins/haipipe-plugin-outline/ref/item-table.md
board/page-workflows/haipipe-page-evidence/SKILL.md
board/page-plugins/haipipe-plugin-runs/SKILL.md
```

New work is routed by the Page Evidence Workspace: SURVEY records Supporting
Run ids, LAND creates one consumer-owned Local Run, and the resulting Result is
the only current Page binding.
