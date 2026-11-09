# Paper workbench

The Paper Board uses the shared Report frame from `../workbench/`.
`paper_focus.py` adapts the paper's content and Topic roles; the eight supporting
sections, rail, files and previews use the same renderers as Work.

## Board views

Idea, Story, Data + Paper Plan, Support blocks, Evidence, Displays and Writing
retain their paper-specific content. Report combines that content and its
existing actions under **Review Content**, followed by **Around the Work**.
Work is no longer a separate Board rail entry. Old `section=work&group=work-story`
links open Report's Story view, and similarly for the other Board views.
Delivery remains an entry to the paper's assembled outputs.

Related appears in both Idea and Story when reference records exist. Story by
Section appears in both Story and Displays when the Story contains a section
narrative. Both entry points render the same source content.

Around the Work and the right rail share the names, icons, order and renderers
declared in `work_frame.SHARED`: Studio, Interactions, Decisions, Things to Know,
Checklist, Timeline, Skills and Files. These sections are unnumbered. Studio is
shown once in this group, rather than repeated inside Idea and Story content.

## Ownership

Every supporting section uses the same selection:

1. An explicit `view:` on a page or Run takes priority.
2. Otherwise, its linked Topic determines the view. A Topic's explicit `view:`
   takes priority over tags; existing paper roles (including `story-current:`)
   adapt untagged legacy Topics without editing their source files.
3. Unassigned records remain available in the right rail. Their location in an
   evidence or writing Job does not assign them to Evidence or Writing.

Use the keys `idea`, `story`, `plan`, `explore`, `evidence`, `displays`, and `draft`
for `view:` metadata, placed in the face header or Run YAML. Topic tags also
recognize Writing, Support blocks and Data + Paper Plan. `for:` links on pages
and interaction records can identify the related Topic.

The rail aggregates the Board and its descendants. A view's Files uses only
selected Topic/Run directories and assigned page faces. Tools · Skills uses the
same selection as Skills; Tools · UI includes the paper adapter and source
renderers. No source records are copied, moved or relabeled for display.

Version Jobs, evidence/submission Jobs, draft Sections and evidence Tasks keep
their specialized Report/Work workflows in this Board-first rollout. The classic
frame also remains supported; its renderers are independent of the new adapter.

Focused Job headers share Work's Job type / Use case display. The type follows
the same version, display, value, citation or submission branch that renders the
page. Use case comes only from the Job face's explicit `use-case:` header; it is
omitted when absent. Initial drafts and revisions remain Writing Version Jobs.

## Validation

`tests/test_paper_focus.py` covers the live Board route, old links, all eight
sections' scope, explicit overrides and version compatibility. Run it with the
other Paper tests and the shared frame tests:

```sh
PYTHONPATH=plugins/haipipe-toolkit/servers/_host python -B -m pytest -q \
  plugins/haipipe-toolkit/servers/workbench-paper/tests \
  plugins/haipipe-toolkit/servers/workbench/tests/test_work_frame.py \
  plugins/haipipe-toolkit/servers/workbench/tests/test_focus_page.py
```

Use a Python environment with the host dependencies. Inspect the live
Paper-Example Board in `blueprints/Project-Ladder/paper/`, including each view,
the eight rail destinations, a legacy Work link, and desktop/narrow layouts.
