# PageX · legacy migration input only

PageX is not part of the active Page workflow. New Evidence Item records do
not carry `PageX Bindings`, and the Outline plugin exposes no PageX workspace
or evidence segment.

Use the current split:

```text
Related Page/Folder relationship
  → Context Workspace · navigation, policy, requirement, or bounded context

Cross-Folder evidentiary material
  → Supporting Run · full bNNjNNtNNrNN id · accepted Result

Governed static material already owned by this Page
  → Local Input · exact path + frozen hash
```

## Migrate one legacy binding

For every existing `PageX Bindings` value:

1. Identify what role the old link actually played.
2. If it only orients the reader or constrains the Page, preserve the source as
   a Related Page/Files row and let CONTEXT project it.
3. If it supplies evidence from another Folder, resolve or commission the
   owning Execution/Discovery Run and write that Result under `Supporting
   Runs` with its full global id.
4. If it is immutable, governed material already inside the Page boundary,
   name it in `Local Input` with its hash.
5. Remove `PageX Bindings` from the current Evidence Item record on its next
   SURVEY pass. Never delete historical files or receipts merely to modernize
   the current graph.

The old `outline/evidence/pagex/` lane and PageX service routes may remain
read-only so historical Pages render and can be migrated. They are not valid
new write targets, Run families, Result types, or authority sources.
