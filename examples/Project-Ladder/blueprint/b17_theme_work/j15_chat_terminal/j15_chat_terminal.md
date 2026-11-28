# j15 · Chat and terminal

goal: keep the chat drawer and the terminal of servers/workbench (chat_drawer/, terminal/) healthy: each Task owns one folder and checks and updates it, one round at a time
close: when this part of servers/workbench is retired; until then the Job stays open and its Tasks keep checking
bands: t0N Chat and terminal

## Topic

How a person talks to an agent from any page: the chat drawer (a Claude session primed with the page, its permissions and its kept transcript) and the terminal. Every Job here is code work. Its delivery is the code in `plugins/haipipe-toolkit/servers/workbench/`, committed to the plugin.

A Task here never closes while its folder lives. Each Task keeps one standing Run, `runs/run-check-<folder>`, and each round is one dated pass of it: run the Task's ## Checks, fix what fails inside the folder, and write the results in the pass. A trace that changes the folder names the Task in `work:`.

Studio: none yet: a Task opens one when its design starts.

Code: `plugins/haipipe-toolkit/servers/workbench/`; each Task's face lists the files it owns, and a test sits with the file it tests.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_chat_drawer · Chat drawer
2. t02_terminal · Terminal
