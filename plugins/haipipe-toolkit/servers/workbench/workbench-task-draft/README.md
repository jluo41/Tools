Manual: skills/1_base/workbench/workbench-task-draft/ (the skill an agent loads for this screen).

The draft Task type: everything a Task with `task-type: draft` shows. `task_draft.py` is its layout
(the frame's Spaces for a draft Task); the other modules are the Page views it embeds, `assets/` their
look, `reader/` the standalone Page server, `exporters/` the delivery builders. One folder per Task
type (b32 s41-D15): a new type is a new `workbench-task-<type>/` beside this one, or inside its theme's folder.
