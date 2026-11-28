---
mindmap: 1
title: Grant Block Structure
written: true
---

# Grant Block Structure

- Structure <!-- n01 -->
  - Jobs <!-- n02 -->
    - [job-type] Story † <!-- map-e0a730d56b0a -->
      Group: Story.
      - [job-name] Research case <!-- map-072e7033166f -->
        - [task-type] draft <!-- map-e00a865272be -->
          - [task-name] Specific aims <!-- map-d0923fdc6e57 -->
            Group: Aims.
          - [task-name] Significance <!-- map-7297eeba9592 -->
            Group: Rationale.
          - [task-name] Research plan <!-- map-916ef286fba6 -->
            Group: Approach.
    - [job-type] Evidence † <!-- map-e8d8672327f4 -->
      Group: Evidence.
      - [job-name] Preliminary evidence <!-- map-fe50430f91f1 -->
        - [task-type] value ‡ <!-- map-8b4fc04c9b48 -->
          - [task-name] Pilot measurements <!-- map-f5223e1846f1 -->
            Group: Values.
        - [task-type] evidence ‡ <!-- map-be2911187ba6 -->
          - [task-name] Closest-work citation check <!-- map-98d2f2f9f557 -->
            Group: Citations.
        - [task-type] Unresolved † <!-- map-2af248b69ef2 -->
          - [task-name] Source provenance <!-- map-98ae6d107bbf -->
            Group: Checks.
    - [job-type] Display <!-- map-34e108c0896d -->
      Group: Display.
      - [job-name] Main <!-- map-e10eaccde3ef -->
        - [task-type] Unresolved † <!-- map-490094494654 -->
          - [task-name] Study design figure <!-- map-82cc45a3cbb3 -->
            Group: Figures.
      - [job-name] Appendix <!-- map-d31d01d50442 -->
        - [task-type] Unresolved † <!-- map-e4cc6490081f -->
          - [task-name] Feasibility summary table <!-- map-3d150bb7f0f3 -->
            Group: Tables.
      - [job-name] Explore <!-- map-aab2e49dca22 -->
    - [job-type] Writing Version <!-- map-c8a7369cd961 -->
      Group: Writing.
      - [job-name] Letter of intent <!-- map-b0c6ad6e0f16 -->
        - [task-type] draft <!-- map-f6e699d5fec6 -->
          - [task-name] Research pitch <!-- map-8d20803c9745 -->
            Group: Application.
      - [job-name] Full application <!-- map-afd0d3729a22 -->
        - [task-type] draft <!-- map-a50ead2e839e -->
          - [task-name] Research strategy <!-- map-1d303509c817 -->
            Group: Application.
          - [task-name] Budget justification <!-- map-9322d1bd9ec1 -->
            Group: Attachments.
        - [task-type] Unresolved † <!-- map-b256ff84c4de -->
          - [task-name] Upload package <!-- map-5a890796bcb8 -->
            Group: Submission.
      - [job-name] Revision <!-- map-653a8a0393a9 -->
        - [task-type] draft <!-- map-0c9a01951b65 -->
          - [task-name] Reviewer response <!-- map-4e2e02aeb4fa -->
            Group: Review.
    - [job-type] Presentation † <!-- map-94ac5ddf4492 -->
      Group: Presentation.
      - [job-name] Slides <!-- map-5fef1d020b6d -->
        - [task-type] draft <!-- map-55d5faae484e -->
          - [task-name] Research pitch <!-- map-a68ce1ec439a -->
            Group: Content.
      - [job-name] Video <!-- map-9e19c98c84dd -->
      - [job-name] Poster <!-- map-f3958464671b -->
  - Studio <!-- n50 -->
    - Research design <!-- n51 -->
      - Aims and rationale <!-- n52 -->
    - Communication <!-- n53 -->
      - Application narrative <!-- n54 -->
    - Names illustrate possible discussions, not required records <!-- n55 -->
    - Groups are metadata <!-- n56 -->
    - Each sNN topic is a real discussion record beside the Jobs <!-- n57 -->
  - Types and names <!-- n58 -->
    - Job Type selects a contract <!-- n59 -->
    - Job Name identifies an instance <!-- n60 -->
    - Task Type selects its skill and workflow <!-- n61 -->
    - Task Name names a deliverable <!-- n62 -->
    - Groups organize records separately from types <!-- n63 -->
    - Writing Version is a current reader label, not an emitted job-type field <!-- n64 -->
    - draft and evidence are registered Task types <!-- n65 -->
    - Legacy Paper value faces use unregistered value <!-- n103 -->
    - Legacy citation evidence conflicts with the registered numeric executor <!-- n104 -->
    - Grant Values, Citations and Checks Task mappings remain unresolved <!-- n105 -->
    - Grant names are proposed targets, not current Grant records <!-- n106 -->
    - display is upstream input preparation, not final asset production <!-- n66 -->
    - Story, consolidated Evidence and Presentation Job contracts remain proposed <!-- n67 -->
    - Final display asset, packaging and media Task types remain unresolved <!-- n68 -->
  - Type rules <!-- n69 -->
    - Job group then Job then Task group then Task <!-- n70 -->
    - Groups add no folder layer <!-- n71 -->
    - Block then Job then Task then Run then Result <!-- n72 -->
    - Block owns the physical Delivery root <!-- n73 -->
    - Work owns computation and returned Results <!-- n74 -->
    - Discovery owns source acquisition <!-- n75 -->
    - Idea identity and reviewed revision stay at source <!-- n76 -->
- Draw <!-- n77 -->
  - [Connected organization](structure/jobs.html) <!-- n78 -->
  - Four type/name levels, each parent once <!-- n79 -->
  - Studio organization stays alongside work <!-- n80 -->
- Examples <!-- n81 -->
  - Bind actual Grant Blocks and use their names <!-- n82 -->
  - Check real routes before showing entries <!-- n83 -->
  - No numbered fake records or invented bindings <!-- n84 -->
- Skills <!-- n85 -->
  - One top view in this same structure Studio <!-- n86 -->
  - Relevant skill entries <!-- n87 -->
    - Functions <!-- n88 -->
    - Inputs and outputs <!-- n89 -->
    - Workflow and checks <!-- n90 -->
  - No new Studio for each skill or function <!-- n91 -->
- Shared view arrangement <!-- n92 -->
  - Top controls choose Structure, Draw, Examples or Skills <!-- n93 -->
  - Structure has Jobs and Studio as left entries <!-- n94 -->
  - Right content shows the selected item <!-- n95 -->
  - One item can use the full width <!-- n96 -->
  - Shared renderer supplies the shell <!-- n97 -->
- Implementation boundary <!-- n98 -->
  - Grant scaffold already exists <!-- n99 -->
  - Five-group scaffold and reader are proposed <!-- n100 -->
  - The authored Studio views are installed <!-- n101 -->
  - Call-specific templates and Grant handoff remain proposed <!-- n102 -->
