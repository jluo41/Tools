# Q · option parity between the Python and the TypeScript Agent SDK

Two lists, then their difference.

1 · In the installed Python package `claude_agent_sdk`, count and list the fields
    of the `ClaudeAgentOptions` dataclass. Report the package version.

2 · In the TypeScript Agent SDK packed inside a Claude Code VS Code extension
    (the extension host bundle, `extension.js`), list every command-line flag its
    argument builder can emit for the `claude` process. Report the extension
    version.

Then report the difference both ways:

- flags emitted by the TypeScript builder with no matching Python option
- Python options with no matching emitted flag

Deliverable: a QA digest with both lists and the unmatched set.
Accepted: an exact count on each side plus the unmatched set, which may be empty.
