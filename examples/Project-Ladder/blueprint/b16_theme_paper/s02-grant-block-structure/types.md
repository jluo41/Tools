# Types of a Grant Block

The shared Block Structure contract owns these four lists. Names in 〈 〉 are proposed semantic contracts, not registered execution values. The `for:` and `holds:` lines give the scope and owner; they do not migrate existing records.

example: examples/Project-Ladder/paper/Grant-Example

## Job group type

### Story
for: Organize the shared research argument.
holds: One shared Story Job; its question, contribution and narrative are content, not automatically Tasks.

### Evidence
for: Organize the evidence the argument uses.
holds: A shared evidence collection; source Work and Discovery Results retain ownership.

### Display
for: Organize figures and tables by their role.
holds: Main, Appendix or Explore Jobs; each display has a source and an intended claim.

### Writing
for: Organize manuscript or application versions.
holds: Writing Jobs with their own content, Review and Submission Task groups.

### Presentation
for: Organize audience-facing formats.
holds: Slides, Video or Poster Jobs; a format is a name, not a registered execution type.

## Job type

### 〈Story〉
for: Develop the shared argument.
holds: Question, contribution and narrative. hai-paper-story owns the content; a separate Story Job execution contract requires definition.

### 〈Evidence〉
for: Keep values, citations and their checks together.
holds: Returned source Results and provenance. hai-paper-evidence owns the consumer; consolidated Job creation requires implementation.

### Display
for: Produce figures or tables for a chosen role.
holds: Main, Appendix or Explore is the Job name. Paper reads display Jobs; final-asset Task routing must follow its material owner.

### Writing Version
for: Produce one manuscript or application version.
holds: Narrative, Section Tasks, comments and submission material. hai-paper and hai-paper-draft own it; current faces infer the kind from the folder, without job-type.

### 〈Presentation〉
for: Develop a talk, video or poster.
holds: Script, assets and export requirements. A new presentation executor is not registered by this catalog.

## Task group type

### 〈Content〉
for: Group material by its role in the Job.
holds: Named groups such as Main text, Appendix, Values, Citations, Figures or Tables; each instance names only the groups it needs.

### 〈Checks〉
for: Group verification of the Job output.
holds: Source checks and assessment questions, linked to their records.

### Review
for: Resolve feedback on a Writing Job.
holds: Comment intake and responses in this Writing Job; hai-paper-comments owns comment identity.

### Submission
for: Prepare a Writing Job for its destination.
holds: Cover letter, required attachments and portal preparation; submission authority stays with the person.

## Task type

### draft
for: Write a Section or prose deliverable.
holds: The shared draft lifecycle, evidence references and review gates; hai-paper-draft owns Paper prose.

### value
for: Read the value Tasks declared by the Paper example.
holds: Returned numbers and provenance. This is an observed task-type in Paper-Example; its mapping to the shared numeric executor needs reconciliation.

### evidence
for: Read citation Tasks declared by the Paper example.
holds: Citation source checks owned by hai-paper-evidence. The shared numeric evidence executor has a different scope; this catalog records that conflict.

### description
for: Read portal-preparation Tasks declared by the Paper example.
holds: Existing portal records use this field; the target Submission group needs an explicit packaging contract before new scaffolding.

### 〈Display asset〉
for: Make the final figure or table.
holds: A design, source data references and exported asset; do not reuse the upstream display-input executor as the asset owner.

### 〈Presentation asset〉
for: Produce a slide, video or poster asset.
holds: Approved content, assets and export requirements; exact execution routing remains to be defined.
