---
title: Paper Job UI aligned with Work
date: 2026-11-26 17:32
topic: s13-paper-job-preview
aim: Store the reviewed Paper, Grant and Idea Job UI designs in b16 Studio with truthful live/proposal boundaries.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/trace/261126/1732_paper_job_ui.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s13-paper-job-preview/s13-paper-job-preview.md
  what: Paper Job scope and shared Work structure; preserve historical decisions
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s13-paper-job-preview/s13-paper-job-preview.html
  what: Live Paper example and proposed design entry
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s13-paper-job-preview/delivery/ui/paper-job-main.html
  what: Interactive Paper and Grant Job proposal
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s11-idea-job-preview/s11-idea-job-preview.md
  what: Idea Job preview scope and missing live-example obligation
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s11-idea-job-preview/s11-idea-job-preview.html
  what: Idea proposal entry without a fabricated live page
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s11-idea-job-preview/delivery/ui/idea-job-main.html
  what: Interactive Idea Job and assessment Task proposal
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/job-ui-design.md
  what: Proposed content mapping, implementation plan and acceptance
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md
  what: Record the user topic, evidence, design and remaining implementation
changed:
- examples/Project-Ladder/blueprint/b16_theme_paper/trace/261126/1732_paper_job_ui.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s13-paper-job-preview/s13-paper-job-preview.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s13-paper-job-preview/s13-paper-job-preview.html
- examples/Project-Ladder/blueprint/b16_theme_paper/s13-paper-job-preview/delivery/ui/paper-job-main.html
- examples/Project-Ladder/blueprint/b16_theme_paper/s11-idea-job-preview/s11-idea-job-preview.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s11-idea-job-preview/s11-idea-job-preview.html
- examples/Project-Ladder/blueprint/b16_theme_paper/s11-idea-job-preview/delivery/ui/idea-job-main.html
- examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/job-ui-design.md
- plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md
---

# Paper Job UI aligned with Work

## Prompts

- **17:32** 那你知道你该去怎么去设计吗？然后你能不能比如说做一个 plan，然后设计一下这些东西呢？然后跟其他的保持一致，尤其是跟这个 work block 里面内容，就是说保持一致吧。你明白我意思吗？
- **18:06** OK，好，那你执行吧。然后执行完了给我讲。

## Check

- Four HTML scripts pass node vm.Script syntax checks. Nine planned files exist, each under 700 lines; current Markdown links resolve; the prior s12 face is preserved verbatim as quoted history. Focused git diff --check passes.
- Studio extraction: Paper exposes seven distinct origin-relative live Page sources and one Effect; Idea exposes one existing quick view. A08 Paper: zero findings. A08 Idea: exactly one documented missing live view; remains open.
- Chrome on the running Tailscale host: b16 Studio discovers s12 and s14. Paper Page loads the real Writing and Review examples. Paper Effect and Idea Effect load their delivered files.
- All six Paper semantic Job types open Main with the Task row hidden. Grant Application → Specific aims → Plan/Revise works; a local answer changes the mark to a check and removes the waiting tray. Switching Letters → Application restores Specific aims. Idea Assessment opens Closest work and its assessment/source/decision controls.
- Keyboard Enter opens Overview; the content dot opens its dialog. Fixed the Display Task-topic collision by reserving Main for the Job overview and naming the group Main displays. Single-preview entries fill the available width.
- 390px checks: Idea entry outer and inner widths are 390/390; Grant preview is 390/390, with no horizontal document overflow. Screenshots inspected; viewport override reset. No page JavaScript errors observed; two unrelated Zotero extension connection errors excluded.
- Fresh-context workbench-paper validation by review_job_design_integration passed: navigation, source ownership and live/proposal boundaries agree. No production renderer, current page-spec matrix or research data changed.

## Summary

Integrated the reviewed Paper/Grant and Idea Job designs into b16 Studio using the approved nine files. Paper compares real Page examples with an interactive Effect; Idea offers a clearly identified Effect while its missing live example remains open. The proposed specification aligns navigation and Main with Work, defines six Paper Job types plus one Idea Job type, and records the remaining implementation. T06 remains open for production composition, Review dispatch, canonical examples and regression coverage.

