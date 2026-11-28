# Two A2UI approaches for DeepSeek Harness

Both projects let an agent describe UI as data rather than emit executable HTML or JavaScript. A trusted component catalog renders that description inside DSH. The important difference is not how many widgets they ship; it is what each surface is allowed to become after the answer appears.

| Question | [dsh-a2ui](dsh-a2ui), `v0.4.0` (`2ca5914`) | [dsh-genui-a2ui](dsh-genui-a2ui), `v0.5.4` (`93e2a4b`) |
| --- | --- | --- |
| What does the model write? | A2UI 1.0 JSON messages to `a2ui`; `a2ui_catalog` loads guidance on demand. | A2UI Express to `a2ui_render` or `a2ui_ask`; the Host compiles it to validated A2UI messages. The shared protocol does not make the tools or extension catalogs interchangeable. |
| What lives across turns? | Each call is a self-contained transcript snapshot. Updates compose within a call; a later call creates a new card. | Inline and answer cards coexist with a live dock that can update an existing surface. Superseded answer cards become read-only snapshots. |
| How does the reader interact? | Sorting, tabs, hover, and sliders stay local. Explicit actions send a queued user message. | Local bindings also support linked filters and computed values. A blocking ask can collect structured input in the current turn, or settle without an answer. |
| What does that cost? | Simpler ownership and replay; each changed view consumes another card. | Better for ongoing review; more lifecycle states to test, plus a compiler and lazy-loaded rendering dependencies. |

## What Tools-SPACE should borrow

Keep the [file system → UI map](../PRINCIPLE.md) authoritative. Use the chat card to **show** a saved artifact or **collect** a decision, not to store Project, Block, Task, Run, or review state. A read-only answer card should retain what the reader actually saw and link to the source artifact. A live dock should project the latest saved state; sort order, filters, and expanded rows can stay local. A submit button should send an explicit intent and stable target ID to the existing writer. The writer should recheck access and the expected revision, reject stale or duplicate submissions, and save a receipt before the UI reports success. Skipping or timing out is not approval.

Start with ChimeSky's snapshot semantics as the default. Borrow Geekhyt's live dock and blocking ask only for tasks that need to stay current or cannot continue without a human decision. Neither upstream needs to become a dependency of the workbench.

## Reading path and pilot

1. **Read one card end to end.** Start with ChimeSky's [architecture guide](dsh-a2ui/docs/ARCHITECTURE.md), [shared validator](dsh-a2ui/src/shared/validate.ts), and [partial JSON scanner](dsh-a2ui/src/shared/partial-json.ts). Note how replay starts from settled tool data and how a streaming preview stays inert until validation.
2. **Follow one decision.** Read Geekhyt's [development guide](dsh-genui-a2ui/docs/DEVELOPMENT.md), [turn projection](dsh-genui-a2ui/src/client/shell/turn-surfaces.ts), and [ask implementation](dsh-genui-a2ui/src/host/ask-tool.ts). Compare the [replay tests](dsh-genui-a2ui/tests/deterministic-replay-fuzz.spec.ts) and [ask lifecycle model](dsh-genui-a2ui/specs/AskLifecycle.tla) with ChimeSky's simpler per-call boundary.
3. **Pilot one file-backed review.** Pick a saved review artifact with a stable ID. Render a read-only card that links to it and verify that reopening the chat neither changes the snapshot nor fires an action. Then try a single structured decision using the existing writer. Verify that reload, duplicate submit, a stale revision, and skip/timeout do not create an incorrect write. Add a live dock only if the pilot shows a need for cross-turn updates.

This is a source review of the pinned upstream commits, not a performance benchmark or a compatibility test. Both repositories are MIT-licensed; their third-party notices remain in the submodules. Neither was installed or enabled in DSH as part of this review.
