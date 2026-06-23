Lifecycle Skills — TODO
========================

1. Every lifecycle skill MUST have a ref/<name>-template.tex

   Each lifecycle stage produces a standalone-compilable .tex file. The skill
   should ship a canonical template in ref/ that the agent copies to
   0-lifecycle/<N>-<name>/<N>-<name>.tex and fills in. The template is the
   source of truth for structure; the skill procedure describes WHAT to write
   and WHY, not the full LaTeX boilerplate.

   Current status:

     [x] seed       ref/seed-template.tex      (84 lines)
     [x] pitch      ref/pitch-template.tex     (110 lines)
     [x] claims     ref/claims-template.tex    (130 lines)
     [ ] narrative   no template — procedural only, needs one
     [ ] display     inline fragments only — needs a ref/display-template.tex
     [ ] minimap     inline snippet only — needs a ref/minimap-template.tex

   For narrative, display, minimap: extract or create the template, then
   replace inline snippets in SKILL.md with a reference + reading-order
   summary (same pattern as claims v1.3.0 and pitch v1.5.2).

2. Every template should include section-level comments explaining the role

   Follow the claims template pattern: each \section* has a comment block
   with the section purpose, what the agent fills in, and what the user
   decides. The template is self-documenting.

3. Compile the template itself to verify it builds clean

   After creating or updating a template, run pdflatex on it to verify the
   placeholder content compiles. A template that doesn't compile is a bug.

Created: 2026-06-23
