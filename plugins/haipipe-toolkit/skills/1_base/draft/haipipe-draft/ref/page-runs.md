This file holds the Page Run families inside Outline: Run names, Run bookends, adoption and the RP kinds, moved from `SKILL.md`.

## 🏃 Page Run families inside Outline

Load `ref/page-run-families.md` before naming or allocating a Page Run. Workbench
Outline's Run Space presents three semantic areas plus the owner-native
Supporting group, in both standalone and Board-hosted mode:

```text
Page Writing  RP · run-structure- · run-scratch- · run-section- · run-paragraph- · run-revise-
              · run-auto-write- · run-evidence-embed- · run-context-  (each + <slug>)
Page Evidence RE · run-value-<item slug> · run-display-… · run-citation-…
Page check       run-check-<slug>
RD         run-delivery-webpage · run-delivery-latex · run-delivery-word · one fixed Run per lane, rerun by `page.py export`
Supporting native rNN/riNN/rlNN/global identity · Task/Discovery grouping
```

**Run names (JL 260928: "remove rp-xxx, make it readable").** A Page Run is
`run-<kind>-<slug>`: `kind` is a word (structure, section, paragraph,
scratch, revise, auto-write, evidence-embed, context, check, citation, value,
display), `slug` two to four words (its purpose, its target such as `c1-p2`, or
its Evidence Item's slug); a taken name gets `-2`. The name carries no day (JL
261007: a run is worked in passes, each dated inside it); an older dated name
`run-<kind>-<MMDD>-<slug>` still reads, and `page.py run-names` drops its day. The three Delivery Runs are fixed and never numbered. Each run is
its own folder (0.125, JL 261009; haipipe-run 0.31.0): `runs/<name>/` holds its ticket
`<name>.md` (a Delivery Run's is its command, `<name>.sh`), its card `run.yaml`, and
`passes/pNN-<MMDD>/`, one per close. The older flat `runs/<name>.md` ↔ `results/<name>/`
still reads. The one grammar is `src/run_names.py`; the paths are `src/run_folders.py`.
Older names (`rp-sec-07`, `re-value-07_x`, `rd01_latex`) still read;
`page.py run-names <page>` renames a Page's runs once, moves each into its own folder
(its result folder becoming the first pass), keeps older numbered Delivery builds as
history, and writes each built lane's Delivery Run ticket.

**Run bookends (JL 260928).** A Page Writing Run has two bookends the person
calls. `page.py open-run <page> --kind <kind> [--slug] [--target] [--goal]`
writes the ticket when it starts; while it is open, only the Draft file
(`draft/<stem>-draft-v<N>.md`) changes; `page.py close-run <page> <run>
[--summary]` writes the result folder, its one log entry, decision threads and
evidence notes once, when the person says the Run is over. Page Content adoption and
the Delivery Runs (web → LaTeX → Word, `page.py export`) follow only when the person asks. Contract:
`../haipipe-draft-workflow/ref/interactive-writing-run.md` §🔖. Adoption is one
command, `cli/page.py adopt <page> [--dry-run]` (`src/page_adopt.py`): it writes
the current Draft's `## 3 · Draft` sentences into `## Content` in Draft order,
each on its `realizes:` line, writes each sentence's evidence lines (`> Value:`,
`> Citation:`, `> Display:`, `> Supporting Run:`; `src/evidence_lines.py`) from the
Bullet's `Evidence:` / `Answered:` / `Drawn:` items and the Evidence Markdown's
bound Result and Supporting Runs, keeps every `>` line that names no Evidence Item
(a hand note, a review mark), drops and names those of a cut sentence, leaves a Draft still
marked `[open …]` or `[block …]` off the Page, and refuses (writing nothing) when
the Draft's paragraphs and the Page's differ or when a sentence would have to be
added, cut or moved across untagged material (a fenced block, a list). Afterwards
`health` sync passes.

This is a projection, not a second Run registry. Page Run names carry no
counter (a name is its kind and slug), and all are distinct from native `rNN`/`riNN`/`rlNN`
counters. Execution, Discovery, Insight (`riNN`), Design, and other native
families retain their identities under Supporting Runs; Page never renames
them. Supporting members are grouped by parent Task for readability, but the
external Results remain references and are never copied. A Page Run and a
Task `r01` may coexist; neither renames or consumes the other. RP kinds:

```text
run-structure-<slug>   Page Structure Run: SHAPE + SURVEY
run-scratch-<target>   Human Scratch capture at C1 or C1.P1 (Section/paragraph group)
run-section-<slug>     Section-level writing
run-paragraph-<target> Paragraph-level writing (target: p03 or p03-p05)
```

The first `run-structure-…` is the initial Structure Run and contains both the SHAPE and
SURVEY cycles. It is one shared Ticket/Result even when several people
participate: record `participants` on the Run and `contributors` on each Step.
A later `run-structure-…` is an independent structure/Bullet refinement, not a new
participant or Survey pass. These Runs settle Page direction, coverage and
non-coverage, high-level section flow, ordered Bullets, Point roles, paragraph
jobs, typed evidence decisions, and the structure list. After structure closes, Section Runs use
`run-section-…`; paragraph Runs use `run-paragraph-p03[-p05]` and expose their exact
Page-global paragraph target. `RE` uses the focal-result kinds `value`,
`display`, and `citation`; `DISPLAY` covers table, figure, and algorithm block
through `display_kind`. One RE Result/Card may expose many `$V_xxx$`,
`\figure{D_xxx}`, `\table{D_xxx}`, `\algorithm{D_xxx}`, and `\cite{C_xxx}` labels; a
label is not another Run. The Result root `labels:` manifest is the shared
binding source; Draft Space and Evidence Card renderers must preserve the
authored token in expandable provenance even when a resolved value is shown.
While a structure Run is open, its review artifact is the Structure card at
the top of the shared Draft Space: the plan's `## C<n>` and `### C<n>.P<m>`
headings as plain text, read from the selected Outline, which the person can
click into and edit (rename, reorder, add or drop empty paragraphs; points
stay with their heading). There is no map file; a plan without divisions
shows only the `run-structure` button, never an empty card.

The canonical Page Run namespace has no new aliases. The kind token must match
the scope, and a paragraph target must be exact; a mismatched identity is held
as a contract error and cannot unlock later work. Retired compact identities in
existing records remain readable history but are not allocated for new Runs. A
Run-controller invocation is a **Page workflow pass**,
not a Page Run object. Owner-native Run receipts remain machine workflow
records: Page-heavy standalone Folders commonly use `workflow/receipts/`, while
the current Board controller's compatibility bundle uses
`<board>/_runs/page/<page-id>/`. An unallocated `new-*` route is still only an
Evidence plan.
