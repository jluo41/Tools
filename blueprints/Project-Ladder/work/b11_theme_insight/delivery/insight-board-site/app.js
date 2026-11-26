/* Insight Systems Map: one script for every page. It draws the frame (view buttons on top, the view's pages on the
   left, the page's outline on the right), the folder explorers and the UI tables. Read from haipipe-insight
   (ref/insight-ladder.md, dataprep.md, run-report.md) and servers/workbench-insight. */
(function () {
  "use strict";
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* ── the site: views, each with its pages ─────────────────────────────────────────────── */
  // a view's pages, in groups: [group label or "", [[file, title], ...]]
  const VIEWS = [
    { key: "overview", label: "Overview", groups: [["", [["index.html", "The principle"]]]] },
    { key: "work", label: "Work", groups: [
      ["Folder", [["work-blocks.html", "Block folders"], ["work-chats.html", "Chat folders"], ["work-chat-qa.html", "What a chat keeps"]]],
      ["UI", [["work-folder-page.html", "Folder to page"], ["work-levels.html", "Levels and views"], ["work-marks.html", "Marks"]]]] },
    { key: "define", label: "Define", groups: [
      ["Folder", [["define-skills.html", "Skill folders"], ["define-servers.html", "Server folders"], ["define-blueprints.html", "Blueprint folders"]]],
      ["UI", [["define-blueprint-page.html", "The blueprint page"]]]] },
    { key: "map", label: "The Map", groups: [["", [["map-three-views.html", "Three views"], ["map-elements.html", "Folder to element"],
      ["map-one-run.html", "One Run, four places"], ["map-sessions.html", "Session view"], ["map-rule.html", "The rule"]]]] },
  ];
  const pagesOf = (v) => v.groups.flatMap(([, ps]) => ps);
  const here = $("#main").dataset.page;
  const view = VIEWS.find((v) => pagesOf(v).some(([f]) => f === here)) || VIEWS[0];

  function frame() {
    $("#bar").innerHTML = `<div class="bar-in"><a class="brand" href="index.html">Insight Systems</a><nav class="views" aria-label="Views">`
      + VIEWS.map((v) => `<a href="${pagesOf(v)[0][0]}"${v === view ? ' aria-current="true"' : ""}>${esc(v.label)}</a>`).join("") + "</nav></div>";
    $("#side").innerHTML = `<p class="side-h">${esc(view.label)}</p>` + view.groups.map(([g, ps]) =>
      (g ? `<p class="tab-group">${esc(g)}</p>` : "") + `<ul class="tabs">`
      + ps.map(([f, title]) => `<li><a href="${f}"${f === here ? ' aria-current="page"' : ""}>${esc(title)}</a></li>`).join("") + "</ul>").join("");
  }

  /* ── the three folder trees: name · title · what it holds · who writes it · where the UI shows it ── */
  const n = (name, title, what, by, ui, kids) => ({ name, title, what, by, ui, kids });
  const TREES = {
    skills: { root: "plugins/haipipe-toolkit/", start: "door", nodes: [
      n("skills/2_theme/insight/", "The insight theme's skills", "One folder per skill. Each holds SKILL.md and, where it needs them, ref/, scripts/, tests/ and agents/.",
        "Workbench-Insight-UI, the session that owns the theme", "The Skills rail of every insight page lists this level's skills.", [
        Object.assign(n("haipipe-insight/", "The door", "Makes and audits the three Blocks and runs them: the Question Book, the DataPrep Block and the Board.",
          "Workbench-Insight-UI", "/haipipe-insight leads the Skills rail on every insight page.", [
          n("ref/", "The rules and the runners", "insight-ladder.md, dataprep.md, run-report.md; run_job.py runs a question on a segment, run_prep.py a prep version, run_report.py lays out and checks a Run's report.",
            "Workbench-Insight-UI", "Not drawn. A hard Run's ticket calls ref/run_job.py; the pages show what it wrote."),
          n("scripts/insight_ladder.py", "The scaffold", "Makes each folder and keeps the gates: prototype, board, data, job, prep, step, sign, audit, run.",
            "Workbench-Insight-UI", "Not drawn. A button's prompt asks an agent to run it."),
          n("tests/", "The guards", "One test file per rule: the ladder, DataPrep, Run reports and the rest.", "Workbench-Insight-UI", "Not drawn."),
        ]), { id: "door" }),
        n("haipipe-insight-workflow/", "The router", "ref/run-cards.md holds every button: its label, level, space, the Run it names, its skill, agent, signer and prompt. scripts/run_cards.py checks them.",
          "Workbench-Insight-UI", "Each button in a Runs panel is one card; pressing it copies the card's prompt."),
        n("haipipe-insight-evidence-plan/", "Plan the evidence", "Turns what would answer a question into needs (compute, cite or judge) for a reviewer to agree.",
          "Workbench-Insight-UI", "Question page › Work: the Plan the evidence button."),
        n("haipipe-insight-check/", "The checks", "Read-only checks that an answer fits its question, and the Job's close.",
          "Workbench-Insight-UI", "Task page: Check alignment. Job page: Close the Job."),
        n("folder-kinds/", "What each level may say", "haipipe-insight-data, -information, -knowledge and -wisdom write a level's page; -meta says what the extract holds; -question runs proposals and triage.",
          "Workbench-Insight-UI", "Task page › Write the report: the button names the question's level skill."),
        n("haipipe-insight-bind/ · haipipe-page-insight/", "Older page layouts", "The answering page of the register board and the task-side Insight Page, still read until carried over.",
          "Workbench-Insight-UI", "Pages of the older layouts only."),
        n("workbench-insight/", "The theme's page rules", "SKILL.md; ref/topics.md, every topic a Report or the user raised and what changed; ref/workbench-table.md, every button in one table.",
          "Workbench-Insight-UI", "Not drawn. It is the record of why each page looks as it does."),
      ]),
      n("skills/1_base/project/", "Shared skills the theme uses", "One owner per Block folder kind, the same in every theme.", "the project theme", "Their folders show on every theme's pages.", [
        n("haipipe-job/", "Jobs, jNN", "A Job and its Tasks and Runs.", "the project theme", "Job and Task pages."),
        n("haipipe-studio/", "Studio topics, sNN", "A topic thought through and drawn, with its passes.", "the project theme", "The Studio section."),
        n("haipipe-chat/", "Chats, cNN", "Saves a kept session as QAs: new_chat.py new, refresh, list, check; the Stop hook chat_hook.py.", "the project theme", "The Session view and 🧵."),
        n("haipipe-run/", "Soft Runs and passes", "runs/run-<verb>-<target>/ and passes/pNN-<MMDD>/pass.md, written by soft_run.py.", "the project theme", "Runs panels; passes in the Session view."),
      ]),
      n("agents/", "Who does a Run", "haipipe-insight-agent makes; haipipe-insight-reviewer-agent checks. A check is never done by the agent that made the thing.",
        "Workbench-Insight-UI", "Each card names its agent; the workbench table lists them."),
    ] },

    blueprints: { root: "blueprints/Project-Ladder/", start: "bui", nodes: [
      n("work/b11_theme_insight/", "The insight plugin's blueprint Block", "A Block like any other, planning the insight theme: its own jNN, sNN and cNN, plus the UI's definition.",
        "Workbench-Insight-UI and the people designing the theme", "Its /wb page is the Define UI.", [
        n("board.md", "Its face", "theme · package · spine · close · session; ui-block, ui-job and ui-task name the example Blocks the definition links to.",
          "the people designing the theme", "The page's header, and its example links."),
        Object.assign(n("ui/", "The UI's definition", "block-views.md, job-views.md, task-views.md: each level's views and the buttons in each; view-guide.json: each view's specification and example; acceptance.md: what was checked.",
          "Workbench-Insight-UI", "A table per level on the blueprint page; each button opens its specification and an example page."), { id: "bui" }),
        n("j01_insight_workbench_pages/", "A design Job", "t01_board_page, t02_job_page, t03_task_page: building each level's page.",
          "Workbench-Insight-UI", "Job and Task pages of the blueprint Block."),
        n("sNN-<topic>/", "Studio topics", "s01-insight-ladder to s61-insight-slides: the design thought through and drawn, the element UI (s32) among them.",
          "haipipe-studio", "The Studio section."),
        n("cNN_<slug>/", "Kept chats", "The sessions that decided the design, kept as QAs. None is kept here yet; b10's c01 is the first in Tools.",
          "haipipe-chat new_chat.py", "The Session view."),
        n("delivery/", "What it hands over", "insight-slides/, and this site, insight-board-site/.", "Workbench-Insight-UI", "The Delivery section."),
      ]),
      n("insight/Insight-Example/", "An example Board", "Placeholder work in the real Work Folder shape: Jobs, Tasks and Runs, no real data.",
        "Workbench-Insight-UI", "Opened from the blueprint page's example links; drawn by the real page code."),
      n("insight/InsightQuestionBook-Example/", "An example Question Book", "Placeholder questions and releases in the real shape.",
        "Workbench-Insight-UI", "Opened from the blueprint page's example links."),
      n("work/b10_project_workbench/", "The shared workbench's blueprint Block", "The frame every theme fills; it holds the first kept chat, c01_plugin_principle_and_chat.",
        "the project theme", "Its own /wb page."),
    ] },

    blocks: { root: "<Project>/insight/", start: "task", nodes: [
      n("InsightQuestionBook-<Topic>/", "The Question Book", "The questions and the code that answers them, one release per Job.", "insight_ladder.py prototype",
        "Question Book page: Questions · Ideas · Versions.", [
        n("board.md", "Its face", "board-kind: prototype · serves: the Boards it feeds.", "the scaffold", "The page's title and facts."),
        n("cNN_<slug>/", "A kept chat", "One session that decided something or changed files, kept as QAs. A chat that edited a question and reran it on a Board names both Blocks in its paths.",
          "haipipe-chat new_chat.py", "Session view rows; 🧵 on the folders it wrote."),
        n("proposals/<slug>.md", "The backlog", "A new question, a fix, a retirement or a segment, each with its level, where it came from and why.",
          "the Propose Runs of a Job or a Board", "Question Book › Ideas."),
        n("jNN_question-vN_<slug>/", "A release", "release.yaml, partitions.md (the segments), thresholds.yaml, src/; frozen once a person signs it.",
          "run-open-version, then run-sign-release", "Release page: its questions, its segments, its signature.", [
          n("tNN_<L><NN>_<slug>/", "A question", "question.md and scripts/<slug>.py, its one entry script.", "run-plan-evidence, run-write-script, each reviewed by another agent",
            "Question page: its plan and its script."),
        ]),
      ]),
      n("InsightDataPrep-<Set>/", "The DataPrep Block", "The code that turns a raw export into a ready folder. Code only, no data.", "insight_ladder.py dataprep",
        "No page draws it yet; its buttons are written in run-cards.md § Data Prep.", [
        n("jNN_prep-vK_<slug>/", "A prep version", "A chain of steps; signed, then frozen with its hash pinned.", "run-review-steps, run-sign-prep",
          "No page yet; run-cards.md § Prep holds Review the steps and Sign.", [
          n("tNN_<step>/", "A step", "step.md (goal, reads, writes, checks, the cut and params keys it reads) and scripts/<script>.py with run(ctx).",
            "run-write-script, reviewed by another agent", "No page yet; run-cards.md § Step holds its buttons."),
        ]),
      ]),
      n("Insight-<Dataset>/", "The Board", "One dataset, its data versions, and a Job per set of versions.", "insight_ladder.py board",
        "Board page: Findings · Questions · Data · Advice · Jobs.", [
        n("board.md", "Its face", "dataset · prototype · dataprep · versions: (each data version's raw export, cut and params) · session:.",
          "the scaffold and data …", "Board › Data shows each version's columns, counts and files, never a row. session: names the chat every prompt runs in."),
        n("sNN-<topic>/", "A Studio topic", "A topic thought through and drawn, beside the Jobs; its passes are episodes.", "haipipe-studio",
          "The Studio section, a drawing per topic; its passes in the Session view."),
        Object.assign(n("cNN_<slug>/", "A kept chat", "One session, numbered in time order: its face cNN_<slug>.md holds the session's name, the date, the goal, the paths it wrote and the QAs.",
          "haipipe-chat new_chat.py, the only writer", "Session view: one row per chat, its goal as the title; 🧵 on every folder in its paths.", [
          n("cNN_<slug>.md", "The chat's face", "session · provider · date · goal · paths · cards, then # cNN · title, a summary, ## QA.",
            "new_chat.py; refreshed by the Stop hook when an answer ends", "Opens from its Session view row."),
        ]), { id: "bchat" }),
        n("delivery/handoff-<W>.md", "A handoff", "The Wisdom counsel, naming its pair of versions; signed by a person.", "run-draft-handoff", "The Delivery section and Board › Advice."),
        n("runs/run-<type>-<target>/", "The Board's soft Runs", "Add a version, add a Job, coverage, tracks, propose: each a card run.yaml and its passes.",
          "agents, through their skills", "The Board's Runs panel."),
        Object.assign(n("jNN_data-vM_prep-vK_question-vN/", "A Job", "One version of the data, the prep code and the questions. Frozen once its close is signed.",
          "insight_ladder.py job", "Job page: Findings · Changes · Progress · MindMap.", [
          n("jNN_….md", "The Job's face", "data · prep · prep-hash · release · hash · moved · ready · session.", "the scaffold; t01's Run adds ready:",
            "The page's facts; moved: and previous: drive Changes; session: ends every copied prompt."),
          n("reports/vs-<prev>.md", "The comparison", "One row per question: held, changed, new finding, new question, dropped, not comparable, and why.",
            "run-compare-jNN", "Job › Changes."),
          n("runs/", "The Job's soft Runs", "launch · power · report · check-report · compare · propose · close.", "agents, through their skills", "The Job's Runs panel."),
          n("t01_prep-vK_<slug>/runs/r01_<dataset>/", "The prep Run", "Every prep step in one Run; writes the ready folder and the Job's ready:.",
            "ref/run_prep.py", "Its run page shows its report; the Board does not list a three-version Job yet."),
          Object.assign(n("tNN_<L><NN>_<slug>/", "A question Task", "One question of the release, one place after its release number.", "the scaffold, from release.yaml",
            "Task page: Answer · Changes · Method · MindMap.", [
            n("tNN_….md", "The Task's page", "answer · how-sure · check · takeaways (one line per segment), then a section per segment.",
              "run-write-tNN through the level's skill; run-check-tNN by another agent", "Task › Answer: the big line; takeaways fill the By segment tabs."),
            n("runs/rNN_<segment>/", "A hard Run", "The question on one segment: run.sh, run.yaml, result/, report.md.", "ref/run_job.py through its ticket",
              "Task › By segment, Job › Progress, Board › Findings; it opens on its run page.", [
              n("run.yaml", "The Run's card", "status · n · power · the script's hash · the reason when refused.", "ref/run_job.py", "The mark beside the Run: ✅ ⬜ 🏃 ❗."),
              n("result/", "The result", "Tables, figures, partition_power.csv, runtime.yaml, tables.md, provenance/. Cleared on every rerun.",
                "ref/run_job.py", "Run page › Tables; its figures on Task › Answer."),
              n("report.md", "The Run's report", "A headline, a few sentences citing their tables, a caveat. Kept across reruns.",
                "haipipe-insight-agent; checked by haipipe-insight-reviewer-agent", "Run page › Report, first; its headline stands in for the takeaway until the page is written."),
            ]),
            n("runs/run-write-tNN/", "A soft Run", "Its card run.yaml and passes/pNN-<MMDD>/pass.md, one per episode.", "an agent, through the level's skill",
              "Task › Runs panel; its button copies the prompt."),
          ]), { id: "task" }),
        ]), { id: "job" }),
      ]),
    ] },

    chats: { root: "a chat lives in two places", start: "cface", nodes: [
      n("<Project>/insight/Insight-<D>/cNN_<slug>/", "The kept chat, in its Block", "Saved when a session decided something or changed files. Beside the Block's Jobs and Studio topics.",
        "haipipe-chat new_chat.py new", "Session view row; 🧵 on what it wrote.", [
        Object.assign(n("cNN_<slug>.md", "Its face", "session · provider · date · goal · paths (SPACE-relative, every file it wrote) · cards, then a summary and ## QA: one QA per turn.",
          "new_chat.py, from the session file", "The row's title is its goal; its paths join it to the Folder and Element views."), { id: "cface" }),
      ]),
      n("~/.claude/projects/<working-dir>/", "Claude Code's own folder", "Named for the working folder the chat ran in, outside every repository.", "Claude Code", "Nowhere in the workbench.", [
        n("<session-id>.jsonl", "The transcript", "Every message and tool call, one line each. The QAs are read from it; it is never copied into a Block.",
          "Claude Code", "Nowhere: a transcript may hold printed rows, which a page must never show."),
        n("<session-id>/", "Its side files", "Large tool results and subagents' transcripts.", "Claude Code", "Nowhere in the workbench."),
        n("memory/", "What a chat keeps across chats", "MEMORY.md and one fact per file, read at the start of every chat in this folder.", "the chats themselves", "Nowhere in the workbench."),
      ]),
      n("~/.claude/haipipe-chat/kept.json", "The kept sessions", "The ids of sessions saved with --from, so the Stop hook refreshes their QAs once each time an answer ends.",
        "new_chat.py; read by chat_hook.py", "Not drawn."),
      n("Other episodes in the Block", "Passes", "A soft Run's passes/pNN-<MMDD>/pass.md and a Studio topic's passes carry the same front matter as a chat face.",
        "the agent doing the Run; haipipe-studio", "Session view rows, beside the kept chats."),
      n("Named sessions", "Who talks to whom", "Workbench-Insight-UI owns the theme's skills and pages. A Block session runs a Board's Jobs and sends Reports to it by SendMessage; it never edits the skills.",
        "the people who start them", "A Report's topics land in workbench-insight/ref/topics.md."),
    ] },
  };

  /* ── a folder explorer: the tree in the page, a node's card opening under it; the outline lists the folders ── */
  function explorer(box) {
    const t = TREES[box.dataset.tree], flat = {};
    (function index(list, prefix, depth) {
      list.forEach((x, i) => { x.key = x.id || `${prefix}-${i}`; x.depth = depth; flat[x.key] = x; if (x.kids) index(x.kids, x.key, depth + 1); });
    })(t.nodes, box.dataset.tree, 0);
    const icon = (x) => (x.kids || x.name.endsWith("/") ? "📁" : "📄");
    const draw = (list) => list.map((x) => `<li role="none" data-key="${x.key}"><button type="button" role="treeitem" id="node-${x.key}" `
      + `data-id="${x.key}" aria-expanded="false"><span class="mk" aria-hidden="true">${icon(x)}</span>${esc(x.name)}</button>`
      + (x.kids ? `<ul role="group">${draw(x.kids)}</ul>` : "") + "</li>").join("");
    box.innerHTML = `<p class="mono root">${esc(t.root)}</p><ul class="tree" role="tree" aria-label="Folders">${draw(t.nodes)}</ul>`;

    function open(key, scroll) {
      box.querySelectorAll(".card-open").forEach((c) => c.remove());
      box.querySelectorAll("button[data-id]").forEach((b) => b.setAttribute("aria-expanded", "false"));
      const x = flat[key], btn = box.querySelector(`button[data-id="${key}"]`);
      btn.setAttribute("aria-expanded", "true");
      btn.insertAdjacentHTML("afterend", `<div class="card-open"><h3>${esc(x.title)}</h3><p>${esc(x.what)}</p><dl>`
        + (x.by ? `<dt>Written by</dt><dd>${esc(x.by)}</dd>` : "") + (x.ui ? `<dt>In the UI</dt><dd class="ui">${esc(x.ui)}</dd>` : "") + "</dl></div>");
      markOutline(`node-${key}`);
      if (scroll) btn.scrollIntoView({ block: "center", behavior: "smooth" });
    }
    box.addEventListener("click", (e) => { const b = e.target.closest("button[data-id]"); if (b) open(b.dataset.id, false); });
    open(t.start, false);
    return Object.values(flat).filter((x) => x.depth < 2).map((x) => ({ id: `node-${x.key}`, text: x.name, depth: x.depth, act: () => open(x.key, true) }));
  }

  /* ── the UI tables ─────────────────────────────────────────────────────────────────────── */
  const LEVELS = [
    ["Board", "Insight-<Dataset>/", "Findings · Questions · Data · Advice · Jobs", "insight_focus_board.py"],
    ["Job", "jNN_data-vM_prep-vK_question-vN/", "Findings · Changes · Progress · MindMap", "insight_focus_job.py"],
    ["Task", "tNN_<L><NN>_<slug>/", "Answer · Changes · Method · MindMap", "insight_focus_task.py"],
    ["Hard Run", "runs/rNN_<segment>/", "Report · Tables · Receipt · files, in a pop-out at /_board/insight-run?run=<path>", "insight_view_task.py"],
    ["Question Book", "InsightQuestionBook-<Topic>/", "Questions · Ideas · Versions", "insight_focus_book.py"],
    ["Release", "jNN_question-vN_<slug>/", "its questions · its segments · its signature", "insight_focus_book.py"],
    ["Question", "tNN_<L><NN>_<slug>/ in a release", "its plan and its script", "insight_focus_book.py"],
    ["Data Prep", "InsightDataPrep-<Set>/", "its prep versions", "no page yet"],
    ["Prep", "jNN_prep-vK_<slug>/", "its steps", "no page yet"],
    ["Step", "tNN_<step>/", "its script", "no page yet"],
    ["Prep Task", "t01_prep-vK_<slug>/", "its one Run", "its run page only"],
  ];
  const MAP = [
    ["Board page", "map-board", [["board.md versions:", "Data: each version's columns, counts and files, never a row"],
      ["delivery/handoff-<W>.md", "Advice, and the Delivery section"], ["sNN-<topic>/", "the Studio section, a drawing per topic"],
      ["runs/run-<type>-<target>/run.yaml", "a row in the Runs panel"]]],
    ["Job page", "map-job", [["Job face moved: and previous:, reports/vs-<prev>.md", "Changes: one row per question and why"],
      ["every Task's runs/rNN_<segment>/run.yaml", "Progress: one cell per question and segment, with its mark"]]],
    ["Task page", "map-task", [["Task face answer: and how-sure:", "Answer: the big line and how sure it is"],
      ["Task face takeaways:, else each report.md headline", "By segment tabs; the same lines fill Board › Findings"],
      ["result/fig_*.png", "Answer figures"], ["the release's question.md and evidence plan", "Method"]]],
    ["Run page", "map-run", [["report.md beside result/", "Report, first, with ✅ or ❗"], ["result/tables.md", "Tables"],
      ["result/runtime.yaml", "Receipt, folded"], ["run.yaml status:", "the mark; a refused Run's reason where its answer would sit"]]],
    ["Sessions", "map-sessions", [["<Block>/cNN_<slug>/cNN_<slug>.md", "a Session view row: its date and goal, its folders as links"],
      ["paths: on a chat face or a pass", "🧵 on each folder and file it names, and the folders above them"],
      ["cards: on a chat face or a pass", "🧵 beside the item on its page"]]],
    ["Every page", "map-all", [["run-cards.md, one card per button", "the buttons in each Runs panel; each copies its prompt"],
      ["session: on board.md or a Job face", "the line that ends every copied prompt: Run this in the Claude session …"]]],
  ];
  const FAN = [
    ["Task page", "By segment", "its takeaway, its figure, its power"],
    ["Job page", "Progress", "one cell of the questions × segments grid"],
    ["Board page", "Findings", "the segment's answer, beside the other segments"],
    ["Run page", "pop-out", "its report first, then its tables and receipt"],
  ];
  function tables() {
    const lv = $("#levels-body");
    if (lv) lv.innerHTML = LEVELS.map(([l, f, v, by]) =>
      `<tr><th scope="row">${esc(l)}</th><td class="mono">${esc(f)}</td><td>${esc(v)}</td><td class="mono mut">${esc(by)}</td></tr>`).join("");
    const mg = $("#map-groups");
    if (mg) mg.innerHTML = MAP.map(([title, id, rows]) => `<h3 id="${id}">${esc(title)}</h3><div class="scroll"><table class="map">`
      + `<thead><tr><th scope="col">File or field</th><th scope="col">Element</th></tr></thead><tbody>`
      + rows.map(([f, e]) => `<tr><td class="mono">${esc(f)}</td><td>${esc(e)}</td></tr>`).join("") + "</tbody></table></div>").join("");
    const fan = $("#fan");
    if (fan) fan.innerHTML = `<div class="fan-src"><p class="mono">runs/r01_full/</p><p class="mut">one question on one segment</p></div>`
      + `<ul class="fan-to">${FAN.map(([p, v, w], i) => `<li id="fan-${i}"><b>${esc(p)}</b><span class="mono">${esc(v)}</span><em>${esc(w)}</em></li>`).join("")}</ul>`;
  }

  /* ── the outline: the page's headings, or its tree's folders ─────────────────────────────── */
  function markOutline(id) {
    document.querySelectorAll("#outline a").forEach((a) => a.classList.toggle("on", a.dataset.to === id));
  }
  function outline(items) {
    const box = $("#outline");
    if (!items.length) { box.hidden = true; return; }
    box.innerHTML = `<p class="side-h">On this page</p><ul>` + items.map((it, i) => `<li class="d${it.depth || 0}">`
      + `<a href="#${esc(it.id)}" data-to="${esc(it.id)}" data-i="${i}">${esc(it.text)}</a></li>`).join("") + "</ul>";
    box.addEventListener("click", (e) => {
      const a = e.target.closest("a[data-i]");
      if (!a) return;
      e.preventDefault();
      const it = items[+a.dataset.i];
      if (it.act) it.act(); else document.getElementById(it.id).scrollIntoView({ behavior: "smooth", block: "start" });
      markOutline(it.id);
    });
  }

  /* ── start ───────────────────────────────────────────────────────────────────────────────── */
  frame();
  tables();
  const trees = [...document.querySelectorAll(".tree-box[data-tree]")];
  const fromTree = trees.length ? explorer(trees[0]) : null;
  const heads = [...document.querySelectorAll("#main h3[id], #main li[id^='fan-']")].map((h) => ({
    id: h.id, text: h.tagName === "LI" ? h.querySelector("b").textContent : h.textContent }));
  outline(fromTree || heads);
  if (fromTree) markOutline(fromTree.find((x) => document.querySelector(`#${x.id}[aria-expanded="true"]`))?.id || "");
})();
