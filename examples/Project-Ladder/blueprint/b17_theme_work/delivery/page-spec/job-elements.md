# 🧩 Job
example: examples/Project-Ladder/work/b01_example_work

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Job

### Title and section
show: h1
folder: the Job folder's name

### Type line
show: dl.job-identity
folder: the face's type and use case

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Job has

### Goal line
show: .focus-goal
folder: the face's purpose, goal or aim

### Pages rail
show: nav.focus-rail.left
folder: sibling and child folders

### Sections rail
show: nav.focus-rail.right
folder: Report, then the Around the Work sections

## Overview

### Section
show: [data-job-pane="j11"] [data-view="overview"] details.band-sec
view: overview
topic: 1 · 📋 Brief · fixed
folder: the selected Job's face, embedded in its owning Block
code: servers/workbench/page/job_task_views/job_overview.py

### Top views
show: [data-job-pane="j11"] .jov-views
view: overview
folder: Goal, Requirements and MindMap from the selected Job; missing text disables its view

### Task groups and inspection
show: [data-job-pane="j11"] .jov-tree
view: overview
folder: the Job's bands and its real tNN Tasks; clicks inspect records within the Block

### Expanded reading
show: [data-job-pane="j11"] [data-jov-expand]
view: overview
folder: the same Overview content, without changing the Block route or title

### Left tab, right content
show: [data-job-pane="j11"] .job-overview .pb-tabset
view: overview
folder: Topics and Work Structure, with a local list toggle

## Plan + Results

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: standing
topic: 1 · 🧱 Tasks · free

### Job row
show: details.job-row
view: standing

### Run row
show: ul.wk-runs li
view: standing
folder: `runs/rNN_<slug>/`

### Marks
show: .lc-marks
view: standing
folder: the Block's `records/`

### Question card
show: .lc-ask
view: standing
folder: `runs/rNN_collect_<slug>/`

## Findings

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: findings
topic: 1 · 🔢 Values · fixed

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: findings
folder: one tab per table

## Delivery

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: delivery
topic: 1 · 📦 Deliverables · fixed

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: delivery

## Around the Work

### 🎨 Studio
show: .focus-content
view: section=studio
folder: `sNN-<topic>/`

### 🙋 Interactions
show: .focus-content
view: section=interactions
folder: collect Runs at this level and below

### ⚖️ Decisions
show: .focus-content
view: section=decisions
folder: decided questions and their answers

### 📚 Things to Know
show: .focus-content
view: section=know
folder: what the work wants the reader to know

### 📝 Checklist
show: .focus-content
view: section=checklist
folder: what is left to do

### 🕒 Timeline
show: .focus-content
view: section=timeline
folder: git commits and Run passes

### 🧰 Skills
show: .focus-content
view: section=skills
folder: the skills that work on this folder

### Files
show: .focus-content
view: section=files

# 🤝 Collaboration Job
example: examples/Project-Ladder/cowork/b01_example_cowork/j02_review_board_amendment

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Job

### Title and section
show: h1
folder: the Job folder's name

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Job has

### Goal line
show: .focus-goal
folder: the face's purpose, goal or aim

### Pages rail
show: nav.focus-rail.left
folder: sibling and child folders

### Sections rail
show: nav.focus-rail.right
folder: Report, then the Around the Work sections

## Around the Work

### Work its Tasks
show: .focus-content
view: section=work

### Studio drawings, mind maps, slides
show: .focus-content
view: section=studio

### Interactions 🙋 waits on you
show: .focus-content
view: section=interactions

### Delivery what it has handed over
show: .focus-content
view: section=delivery

### Timeline what happened when
show: .focus-content
view: section=timeline

### Skills the skills that work on it
show: .focus-content
view: section=skills

### Files the folder itself
show: .focus-content
view: section=files

# 👥 People
example: examples/Project-Ladder/cowork/b01_example_cowork/j00_people

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Job

### Title and section
show: h1
folder: the Job folder's name

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Job has

### Goal line
show: .focus-goal
folder: the face's purpose, goal or aim

### Pages rail
show: nav.focus-rail.left
folder: sibling and child folders

### Sections rail
show: nav.focus-rail.right
folder: Report, then the Around the Work sections

## Around the Work

### Work its Tasks
show: .focus-content
view: section=work

### Studio drawings, mind maps, slides
show: .focus-content
view: section=studio

### Interactions
show: .focus-content
view: section=interactions

### Delivery
show: .focus-content
view: section=delivery

### Timeline what happened when
show: .focus-content
view: section=timeline

### Skills the skills that work on it
show: .focus-content
view: section=skills

### Files the folder itself
show: .focus-content
view: section=files

# 🔎 Inquiry Job
example: examples/Project-Ladder/discovery/b01_example_discovery/j01_policy_effect_inquiry

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Job

### Title and section
show: h1
folder: the Job folder's name

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Job has

### Goal line
show: .focus-goal
folder: the face's purpose, goal or aim

### Pages rail
show: nav.focus-rail.left
folder: sibling and child folders

### Sections rail
show: nav.focus-rail.right
folder: Report, then the Around the Work sections

## Around the Work

### Work its Tasks
show: .focus-content
view: section=work

### Studio drawings, mind maps, slides
show: .focus-content
view: section=studio

### Interactions 🙋 waits on you
show: .focus-content
view: section=interactions

### Delivery what it has handed over
show: .focus-content
view: section=delivery

### Timeline what happened when
show: .focus-content
view: section=timeline

### Skills the skills that work on it
show: .focus-content
view: section=skills

### Files the folder itself
show: .focus-content
view: section=files
