# Content preview during SHAPE

The Bullet Workspace is a two-column writing workbench, grouped by paragraph:
left = Bullet and linked Evidence; right = actual candidate prose.
Use the right column while shaping the plan, including v0 and unapproved
revisions. Read paragraph joins the candidate sentences in Bullet order so a
person can judge argument, voice, and continuity together.

## Reading-first presentation

Keep the left/right comparison at phone widths too: roughly 40% Bullet and
60% prose, separated by a thin rule. Do not stack the candidate underneath
each Bullet or show permanent textareas. Render prose as readable text; tapping
it opens that cell's editor, with Save and Cancel. Successful saves return to
reading mode unless newer unsaved typing arrived during the request. Cancel
restores the last saved text (or the original Content seed), not a blank field.

Paragraph headings toggle their rows. Use sentence case and compact addresses;
keep the full address in the markup for links. An authored `[Role]` stays
visible beside the Bullet; never invent a role for legacy text. Notes and
Bullet-edit controls live under a small per-Bullet disclosure. Collapse Page diagnostics,
progress and plan process details by default. Keep Evidence links and stale
draft warnings visible. The two column labels already explain the view: do not
repeat “Content preview”, provenance or Save buttons in every resting cell.
This is a shared renderer rule, not a paper-specific HTML override.

Do not show `+ Bullet` or an append form. A person may simply read and copy a
sentence into chat with comments. Retain Read paragraph and existing editors;
removing the add control is not a request to remove other functionality.

## Joint Bullet/sentence revision

For a Section Page, one row means one substantive Bullet and exactly one
candidate sentence. The compact `[Role]` says what that sentence does (for
example `[Phenomenon]`, `[Evidence]`, `[Explanation]`, `[Question]`); the head
states its actual point, not a command to a future writer. Revise either
column first, then revisit the other. If two sentences repeat one point,
remove repetition; if they make distinct points, split the Bullets and review
their evidence contracts. If one sentence consumes two redundant Bullets,
merge the points instead of keeping a shared realization. Never satisfy this
rule by replacing full stops with semicolons in a compound sentence.

The reading view shows authored LaTeX citation commands as literal text, while
the adjacent Evidence links carry the source identity, readiness, and audit
trail. Preserve the commands unchanged in the authored candidate, resting
prose, and editor so a reader can verify both the citation placement and its
Evidence Card without opening the editor.
Likewise, preserve a full missing-evidence placeholder in the authored preview
and editor, but show it in resting prose and Read paragraph as an ordinary
parenthetical citation label, for example `(E33C.SystemStakes)`. Do not render
a chip, box, colour state, or card inside the draft sentence. The full Evidence
contract, status, and direct link remain in the adjacent Bullet & Evidence
column; do not repeat a long verification message inside the reading view.

Keep ordinary conversational changes in the same unapproved working Shape
and preview record. Fork an approved Shape only once, preserving its file;
subsequent saves do not allocate another version or request another approval.
An explicit review checkpoint can freeze/approve the working version. Until
then, changes to the preview do not promote published Page Content or PDFs.

The Section preview writer rejects obvious multiple-sentence entries and
retains unsaved text for repair. Sentence-boundary checks handle decimals,
common abbreviations, citation commands and Evidence placeholders; they are
not a semantic verdict that the sentence contains one idea or reads naturally.
Inspect each pair and read each assembled paragraph before claiming success.

SHAPE may draft and revise these sentences directly. In collaborative writing,
the persistent Writing Run records each human exchange as a Step; do not
allocate a separate Run for each conversational edit. Keep the Bullet concise and place actual prose in
the preview record. A missing factual Result appears as an explicit placeholder
such as `[E01-VALUE-count pending]`, never a guessed number or citation. A
candidate can be useful for discussion while evidence is incomplete.

## Markdown authority

The authored record is `outline/<stem>-preview.md`. It is created on first
preview save. Rendering alone creates no files. Each record names one stable
Bullet, the Shape version it was drafted against, and a SHA-256 of that
Bullet's parsed body (head and continuations):

```markdown
# <stem> · Content preview

Planning draft for discussion; not promoted Page Content.

## C1.P1.B1
plan: v0.3
bullet-sha256: <SHA-256 of iter_plan_bullets(plan)[…]["body"]>

The actual candidate sentence, with [E01-CITE-source pending] if needed.
```

Preview saves update this Markdown record; they do not change a Shape's
approval or the Page source. Bullet edits still create an unapproved working
Shape when the active Shape is approved. A changed Bullet body marks its
candidate `Bullet changed · review this draft`. Retain its text for comparison;
review and save against the new Bullet to refresh its binding. Removed Bullet
records remain on disk until explicitly reconciled; never silently reassign
them to another address.

The live `edit-preview` action requires the displayed Bullet fingerprint and
preview record token. Stale submissions are rejected; edits remain in the
textarea. Save succeeds without reloading the workspace. The page warns before
navigation with unsaved drafts. A blank saved record deliberately clears a
candidate and does not restore old Content on reload.

## Existing Content and later promotion

### Feedback stays in the Page Run

The Bullet Workspace does not show a separate Comments disclosure or comment
composer. A person copies the sentence into chat and gives feedback through
the active Page Run, so wording, rationale, and acceptance remain in one Step
history instead of a second review queue.

Historical preview records may still contain signed comment lanes from the
retired composer after their candidate prose:

```markdown
## C1.P1.B1
plan: v1.2
bullet-sha256: <existing Bullet fingerprint>

Physicians differ in their prescribing decisions.

> Comment JL · [PC0123456789abcdef0123456789abcdef] Say which decision differs. · 260911 1200 UTC
> Quote: Physicians differ in their prescribing decisions.
> Shape: v1.2
>> Codex · Addressed: Specified opioid prescribing. · 260911 1230 UTC
```

The `PC` id is an opaque UUID-derived identity, not a sentence position. These
signed lanes are archival review apparatus, never candidate prose and never
part of the published Page or PDF. Preview saves preserve them even after a
sentence is cleared. Do not render, delete, or silently reassign them; new
feedback belongs to the active Page Run.

### Direct Markdown editing and the Page Mermaid Structure

Link the current unapproved `outline/<stem>-outline-v*.md` for Bullet heads,
roles, Notes, and Evidence expectations, and `<stem>-preview.md` for candidate
sentences at matching `C.P.B` headings. Preserve approved Shapes and stable
addresses. Do not manually invent `bullet-sha256` values: after a Bullet change,
review its retained candidate and save against the changed Bullet to refresh
the binding. Ordinary edits reuse the same working version. Generated HTML and
evidence snapshots are not editing targets.

`rp00_mermaid-structure` owns one derived `<stem>-logic.mmd` that presents the
whole Page argument and its frozen `P01..PN` reading order. Mark its source
Shape and provisional findings explicitly; arrows mean argument flow, not
causal proof. The plan remains authority: this map is the first Page Run's
review artifact, not a second plan or another process record.

The live Bullet Workspace renders the map as a read-only Mermaid card at the
top of the `By part` lens, above the plan and reading table. While `rp00` is
`ready`, `running`, `waiting-for-feedback`, or `blocked`, expand the card for
review. If the source is absent, show an expanded blocker naming the expected
file instead of silently omitting the interaction. After `rp00` is complete,
keep an existing map available but collapsed by default. Its source remains in
a folded block. A map may contain branches and may show more argument moves
than the final manuscript paragraph grouping; label that relationship in its
source note. Refresh the plan, paragraph index, and Mermaid together after
structural changes.

### Promotion boundary

Before a candidate exists, explicit `realizes:` links may show current Page
prose as a starting point, labelled for review. For a Section, seed only a
single sentence with exactly one Bullet backlink and no duplicate realization
of that Bullet. A multi-sentence or multi-Bullet span requires remapping;
leave its candidate empty, explain why in the editor, and preserve the old
Content source. Never guess which sentence belongs where or display “See B1”
as another Section Bullet's completed prose. For non-Section Pages only, a
shared source passage may appear once at its first Bullet, with other linked
Bullets naming that address; the read-through must not repeat it.

CONTENT can adopt this preview once its normal entry conditions are met.
When an interactive Writing Version/Step contains explicit scoped acceptance,
adopt that exact wording and preserve its trace; no new drafting Run or
automatic revision of paragraph seams is required. If the evidence changes
the meaning, return to the affected human Writing Step. An unaccepted preview
may be used by an explicitly delegated writing commission under its own
profile. A UI preview save by itself does not save a complete Writing Step,
approve prose, refresh a PDF or close a Page. The agent records the exchange
under `haipipe-page-workflow/ref/interactive-writing-run.md`.

Return the existing direct Bullet Workspace URL (`lens=div`) for this two-column
view and the Evidence Workspace URL (`lens=workspace&seg=items`). When the
response concerns one Bullet, append its authored address as
`focus=C<n>.P<m>.B<k>`; opening the URL must select Bullet Workspace, expand
the containing paragraph, and focus that exact row. Use the same route whether
the Page is Board-hosted or standalone. In a preview-only pass, state that the
right column is a planning draft and the published Content/PDF has not been
refreshed.
