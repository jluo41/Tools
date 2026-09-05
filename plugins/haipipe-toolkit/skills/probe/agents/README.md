# Probe agents · compatibility only

`haipipe-probe-q-executor-agent` remains solely to read or finish an
un-migrated QA-bank batch. It is not part of the current Page workflow and may
not mint Page-local Probe/PageX storage.

For new work, SURVEY records Execution or Discovery Supporting Runs directly;
LAND consumes their Results through one frozen Local Input and one local Page
Run. The current contracts are:

```text
board/page-plugins/haipipe-plugin-outline/ref/item-table.md
board/page-workflows/haipipe-page-evidence/SKILL.md
board/page-plugins/haipipe-plugin-runs/SKILL.md
```

The compatibility agent still dispatches only consumer-neutral questions and
must never receive Page claims or stakes. Its returned QA path may be cited by
a migrated Supporting Run Result; it is never itself a current Page binding.
