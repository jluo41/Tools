# Chat sessions: presentation and storage proposal

[Concept picture](04-sessions-and-records.png)

## Presentation

Project → Timeline → Sessions: conversations grouped into meaningful episodes. Each episode shows the ask, the change, the reason, and links to the affected content and evidence. Theme and Block scope filters the same records. A Brick's thread opens that same history filtered to its address. Resume opens the original provider conversation when it is available; otherwise a new session can continue from the saved record with an explicit continuation link.

The default workbench presents curated work records. Raw conversation belongs in the original chat or a separate authorized source reader; the existing per-theme transcript visibility contract still applies.

## Storage proposal

One canonical archive per conversation, using the existing studio/chat convention at a declared owning scope:

```
<owner>/studio/chat/<session-folder>/
  session.yaml       stable provider + session ID, source locator, export cursor
  events.jsonl       available original message/tool events, preserved in order
  transcript.md      readable projection generated from events
  assets/            referenced attachments when exported

<scope>/runs/run-<verb>-<target>/passes/pNN-MMDD/
  pass.md            episode, source message range, files and qualified Brick addresses
```

The archive stays at its chosen home when the conversation touches more scopes. Other scopes link to it. A transcript is not copied into each pass. Studio topic passes remain valid homes for episodes consisting of deliberation; existing Draft review passes are read where they live.

Use provider + native session ID as identity; the display title can change. Record available source events incrementally, with idempotent checkpoints, and retain source IDs and timestamps. Save an episode at a meaningful goal boundary and checkpoint it before a handoff or interruption. A closed pass is preserved; later work creates another pass.

Each episode links to the exact source messages, the paths and content addresses it changed, relevant before/after versions, and authoritative decision records. AI summaries describe decisions; they do not manufacture approval. An index joining sessions to passes and targets is derived and rebuildable.

When a provider does not expose a full export, record which data was available and preserve its source locator. Do not describe a summary or a readable projection as a complete raw archive.

## Current repository support

- chat_sessions.py keeps registered Claude chats as transcript.md and digest.md, currently restricted to folded Page folders.
- The readable transcript is a projection of Claude JSONL; tool calls are summarized, so it is not a complete raw-event export.
- The existing digest uses the first human ask and final assistant response. It does not yet segment a conversation into meaningful episodes.
- frame_sessions.py reads Run/Studio passes and Draft review entries, groups them by owner folder, and links touched files.
- Session-based grouping, source message ranges, provider-neutral export, cross-Block discovery and Brick-level history linking need additional implementation.
- This is a design proposal; no runtime code was changed.

Generated using built-in image_gen.imagegen. Exact prompt: [04-session-prompt.txt](04-session-prompt.txt).

