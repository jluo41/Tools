# j04 · HaiChat, the agent drawer

job-of: b03_inlab-human (261009)
spine: `servers/haichat-inlab/haichat_api.py`: one Claude Agent SDK client per browser session, streamed, every tool call blocked on the clinician's Allow or Deny.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

Standalone only (embedded in a HAI-Chat thread, Mattermost is the chat). It runs on the local Claude Code login,
mounts the same endpoint-predict engine as MCP, and relays each tool approval to the browser: the hard part of a
page that starts an agent.

## Questions

```yaml
questions:
- id: Q01
  title: Is HaiChat the bridge the toolkit's chat Job asks for?
  question: b01_haipipe-toolkit j05_chat Q02 asks how a workbench Run reaches Claude Code; HaiChat already runs
    an agent from a page with per-tool approval. Can the workbench reuse it, and what would it need?
  hypothesis: Reuse its approval relay and session handling as the reference for j05's headless way, rather than
    rebuilding them in the old chat drawer.
  acceptance: Answered when j05_chat's Q02 records whether HaiChat's pattern is adopted, with what changes.
  work: []
  report: reports/q01_haichat_as_bridge/q01_haichat_as_bridge.md
- id: Q02
  title: Can the console's action list become an MCP that drives a workbench?
  question: 'The console lets a person and the agent drive the UI through one list of actions (web/src/actions.ts:
    view/open, panel/set, highlight/set, model/select, run/start …), the agent''s tools dispatching the same ConsoleAction
    a click does, gated by Allow/Deny when they act. Could the toolkit''s workbench expose its own actions the same
    way, as an MCP? (Linked both ways with Tools/blueprints/b01_haipipe-toolkit/j05_chat Q02; evidence: studio j02
    s21.)'
  hypothesis: 'Yes: one action list per workbench, served as an MCP; navigation auto, acts gated, every agent act
    badged where it happened.'
  acceptance: Answered when j05_chat Q02 records whether this pattern is adopted, and a first action list is drafted
    for the workbench.
  work: []
  report: reports/q02_actions_as_mcp/q02_actions_as_mcp.md
```
