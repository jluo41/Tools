# 🧩 Work Block
example: blueprints/Project-Ladder/work/b90_example_paper_results

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Block

### Title and section
show: h1
folder: the Block folder's name

### Type line
show: dl.job-identity
folder: the face's type and use case

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Block has

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
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: overview
topic: 1 · 🎯 Goal · fixed
topic: 2 · 🗺️ Work map · fixed
topic: 3 · 📋 Requirements · fixed
topic: 4 · 🧠 MindMap · fixed

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: overview

## Plan + Results

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: standing
topic: 1 · 🗃️ Data preparation · free
topic: 2 · 📈 Statistical analysis · free

### Job row
show: details.job-row
view: standing
folder: `jNN_<job>/`

### Task and Run row
show: .fold-row
view: standing
folder: `tNN_<task>/`, `runs/rNN_<slug>/`

### Marks
show: .lc-marks
view: standing
folder: the card files in `records/`

### Question card
show: .lc-ask
view: standing
folder: `runs/rNN_collect_<slug>/question_collection.md`

## Findings

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: findings
topic: 1 · 🔢 Values · fixed
topic: 2 · 🧠 Maps · fixed

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: findings
folder: one tab per table or map

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

# 📐 Blueprint Block
example: blueprints/Project-Ladder/work/b16_theme_paper

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Block

### Title and section
show: h1
folder: the Block folder's name

### Type line
show: dl.job-identity
folder: the face's type and use case

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Block has

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
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: overview
topic: 1 · 🎯 Goal · fixed
topic: 2 · 🗺️ Work map · fixed
topic: 3 · 📋 Requirements · fixed
topic: 4 · 🧠 MindMap · fixed

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: overview

## Design

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: design
topic: 1 · 🧭 High-level design

## Plan + Results

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: standing
topic: 1 · 🧱 Jobs · free

### Job row
show: details.job-row
view: standing
folder: `jNN_<job>/`

### Task and Run row
show: .fold-row
view: standing
folder: `tNN_<task>/`, `runs/rNN_<slug>/`

### Marks
show: .lc-marks
view: standing
folder: the card files in `records/`

## Findings

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: findings
topic: 1 · 🗂 Topics · free

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: findings
folder: one tab per table or map

## Delivery

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: delivery
topic: 1 · 📦 Deliverables · fixed

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: delivery

## Block UI

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: ui-block
topic: 1 · 🧭 Work Structure
topic: 2 · 📋 Block Type × View Button
topic: 3 · 🖥️ The page, live
topic: 4 · 🎬 Walkthroughs
topic: 5 · 🔍 Review rounds

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: ui-block

## Job UI

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: ui-job
topic: 1 · 🧭 Work Structure
topic: 2 · 📋 Job Type × View Button
topic: 3 · 🖥️ The pages, live
topic: 4 · 🎬 Walkthroughs
topic: 5 · 🔍 Review rounds

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: ui-job

## Task UI

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: ui-task
topic: 1 · 🧭 Work Structure
topic: 2 · 📋 Task Type × View Button
topic: 3 · 🖥️ The pages, live
topic: 4 · 🎬 Walkthroughs
topic: 5 · 🔍 Review rounds

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: ui-task

## Docs

### Section
show: section.work-section-group[aria-label="Report content"] details.band-sec
view: docs
topic: 1 · Block pages
topic: 2 · Job pages
topic: 3 · Task pages
topic: 4 · Skill rules

### Left tab, right content
show: section.work-section-group[aria-label="Report content"] .pb-tabset
view: docs

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

# 🤝 Collaboration Block
example: blueprints/Project-Ladder/cowork/b01_example_data_request

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Block

### Title and section
show: h1
folder: the Block folder's name

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Block has

### Goal line
show: .focus-goal
folder: the face's purpose, goal or aim

### Pages rail
show: nav.focus-rail.left
folder: sibling and child folders

### Sections rail
show: nav.focus-rail.right
folder: Report, then the Around the Work sections

## Plan + Results

### Job row
show: details.job-row
view: standing
folder: `jNN_<job>/`

### Task and Run row
show: .fold-row
view: standing
folder: `tNN_<task>/`, `runs/rNN_<slug>/`

### Marks
show: .lc-marks
view: standing
folder: the card files in `records/`

### Question card
show: .lc-ask
view: standing
folder: `runs/rNN_collect_<slug>/question_collection.md`

## Around the Work

### Work its Jobs
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

# 🔎 Inquiry Block
example: blueprints/Project-Ladder/discovery/b01_example_prior_work

## Page frame

### Path
show: .focus-crumb
folder: the folders from the SPACE down to this Block

### Title and section
show: h1
folder: the Block folder's name

### 🙋 Waiting tray
show: [popovertarget=wait-tray]
folder: every orange mark and waiting question on the page

### View buttons
show: .section-views
folder: the views every work Block has

### Goal line
show: .focus-goal
folder: the face's purpose, goal or aim

### Pages rail
show: nav.focus-rail.left
folder: sibling and child folders

### Sections rail
show: nav.focus-rail.right
folder: Report, then the Around the Work sections

## Plan + Results

### Job row
show: details.job-row
view: standing
folder: `jNN_<job>/`

### Task and Run row
show: .fold-row
view: standing
folder: `tNN_<task>/`, `runs/rNN_<slug>/`

### Marks
show: .lc-marks
view: standing
folder: the card files in `records/`

### Question card
show: .lc-ask
view: standing
folder: `runs/rNN_collect_<slug>/question_collection.md`

## Around the Work

### Work its Jobs
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
