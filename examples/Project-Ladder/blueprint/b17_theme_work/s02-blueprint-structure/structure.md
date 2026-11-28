# Structure of a Work Block (Blueprint)

The three trees of this Block type, drawn by `block_structure_page.py` with the same tree as its type's Pattern
(s71 · Studio Type: Block Structure). `> ` lines are a tree: two spaces a level, `name/` a folder, `  # note` a small
word after the name, `  | words` the line's hover. A name that is not fixed, or not agreed yet, is in 〈 〉.

## Folder
> bNN_theme_〈theme〉/  | the Block that plans one theme's tool: its skills, its workbench pages, its checks
>   jNN_〈tool-part〉/  | a Job: one part of the tool to design or change
>     tNN_〈piece〉/  | a Task: one piece of that part
>       runs/rNN_〈run〉/  | one try: its settings and its receipt
>         result/  | what that try produced
>       tNN_〈piece〉.md  | the Task's face: its goal and state
>     jNN_〈tool-part〉.md  | the Job's face: its goal, close and Tasks in order
>   sNN-〈topic〉/  | a Studio topic, in the band its number names
>   related/  | what came in from outside (papers, notes, files); made when first needed
>   trace/  | a record of each change, by day
>   board.md  | the Block's face: its goal, Jobs and Studio topics

## Job-Task
> 〈Work Block (Blueprint)〉
>   〈job-group-name〉  # Job group  | a decade of Job numbers, named on the `bands:` line of board.md; one of the Job group types
>     jNN_〈job〉  # Job name  | names its type on its face (`job-type:`)
>       〈task-group-name〉  # Task group  | a decade of Task numbers, named on the Job face's `bands:` line; one of the Task group types
>         tNN_〈task〉  # Task name  | names its type on its face (`task-type:`)

## Studio
> 〈Work Block (Blueprint)〉
>   🧱 Block Structure · s0N  # Studio Type: s71 Block Structure  | The Folder, the Job-Task and the Studio of one Block type.
>     s0N-〈block-type〉-structure
>   👀 Block Job UI Preview · s1N  # Studio Type: s72 Block Job UI Preview  | One live preview per Block type: its Block page, a Job and a Task.
>     s1N-〈block-type〉-job-preview
>   📊 Report · s2N  # Studio Type: s73 Report  | A topic that answers one of the Block's Questions.
>     s2N-〈question〉
>   🧩 UI Plugin · s3N  # Studio Type: s74 UI Plugin  | A piece every page carries: the Files tree, the Trace section.
>     s3N-〈page-piece〉
>   🪜 Task Procedure · s4N  # Studio Type: 〈none yet〉  | Task methods of the relevant Task type and its owning skill.
>     s4N-〈task-method〉
>   🧰 Skill · s5N, s6N  # Studio Type: s75 Skill  | The skills that make one Block type, or one skill alone.
>     s5N-skills-〈block-type〉
>     s6N-skill-〈skill〉
>   🏷️ Studio Type · s7N, s8N  # Studio Type: 〈none yet〉  | What a topic of one band must show: its top buttons, left tabs and requirements.
>     sNN-studio-type-〈type〉
>   🧭 Guide · s9N  # Studio Type: 〈none yet〉  | How to read the Block's page.
>     s9N-〈guide〉
