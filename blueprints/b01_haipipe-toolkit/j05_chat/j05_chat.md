# j05 · Chat

job-of: b01_haipipe-toolkit (new 261009)
spine: What we do about chat: the old in-page chat and terminal (kept, no longer served), and how a workbench Run reaches Claude Code working in the project folder.
close: Each recorded question has a report Page with an answer status, and every answered question names the server, skill or MCP change that settled it.

## Topic

The workbench once carried a chat and a terminal in a side drawer (`servers/workbench/chat.py`, `term.py` and the
drawer's chat and terminal scripts). No live page loads them any more: the frame's right panel is Disk and Runs, and
each Run's prompt is one click away. The code stays where it is and is still served (JL 261009: "don't delete
it"); `chat-code.md` maps every file, route and dependent, and what retiring it would take (Q01).

The open question is the bridge: how a Run's button hands the work to Claude Code working in the project folder.
Three ways (JL 261009, "how could I make it as the mcp, which can call the claude code to do it?"):

```text
A  button ─▶ the server starts claude -p in the SPACE (headless) ─▶ the run folder
B  Claude Code ─▶ an MCP server over the workbench: next Run · run card · prompt ─▶ record a pass
C  button ─▶ a request in runs/<run>/ ─▶ the MCP inbox ─▶ a Claude Code session does it
```

What each must solve: permissions (a headless run cannot ask; a fixed tool list per run type), security (a page
that starts an agent needs loopback or real auth), lifecycle (a long run outlives a server restart: detached, logged,
resumed by session id), collisions (two agents on the same files: a lock per Block), and context (start in the SPACE
root so skills, AGENTS.md and memory load; whose login pays).

## Questions

```yaml
questions:
- id: Q01
  title: Does the workbench keep an in-page chat?
  question: With no live page loading the chat drawer, do we keep, move or retire the in-page chat and terminal?
  hypothesis: 'Retire it from the server and keep the code here: the right panel is Disk and Runs, and a Run''s
    prompt already opens the work in Claude Code.'
  acceptance: Answered when the decision is recorded; if retired, the server no longer mounts the chat or
    terminal, the code sits in legacy/ with chat-code.md's map, and the tests pass.
  work: []
  report: reports/q01_in_page_chat/q01_in_page_chat.md
- id: Q02
  title: How does a workbench Run reach Claude Code?
  question: How does a Run's button hand the work to Claude Code working in the project folder, by headless run, by
    an MCP server over the workbench, or by a request queue the MCP reads?
  hypothesis: 'The MCP first (B), then the queue (C): one agent under its own permission prompts; a headless runner
    (A) only for unattended hard Runs, with a fixed tool list.'
  acceptance: Answered when one way is built and a Run started from the workbench lands a pass in its run folder.
  work: []
  report: reports/q02_run_to_agent/q02_run_to_agent.md
```
