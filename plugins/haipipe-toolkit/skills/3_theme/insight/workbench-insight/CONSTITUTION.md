# workbench-insight · Constitution

These rules govern the theme's content, previews and default entry. Shared UI rules also apply.

## A01 · Open the owning Work Block

**Rule:** Theme design opens in `examples/Project-Ladder/blueprint/b11_theme_insight`, with the relevant Studio selected. Default delivery links are verified Tailscale Block routes. Internal HTML, SVG and mindmap documents remain embedded content. Job/Task selections retain their owning Block title and route.

**Check:** Open the real b11 Studio and inspect the Block route; each Job preview must keep its example's Block identity. Record acceptance in the active Trace.

## A02 · Structure uses Folder Tree; Draw is separate

**Rule:** Structure › Folder, Job-Task and Studio use the existing vertical Folder Tree, including available inline examples: native details/summary, branch lines, level colours and readable labels. Structure has no mindmap cards, wires, zoom or font scaling. Draw has its own binding; S71 requires one owned Excalidraw canvas, full width. Missing canvases remain a recorded gap, never a reason to render a mindmap in Structure. Source links, authored notes and real ownership remain intact.

**Check:** delivery/structure/check_structure.py inspects each actual Structure fragment for Folder Tree markup and absence of mindmap content. Negative probes restore a mindmap body and a Draw binding separately; both must fail. Retained membership, authored edits and source identity checks still apply. Accept the expanded tree inside b11 on desktop and phone; do not substitute Draw acceptance for Structure acceptance.

## A03 · Shared Bands, referenced Studio Types

**Rule:** Band classification and order come from the shared registry; Studio Type is a separate instance contract. Reference shared definitions. Add a theme type only for an actual distinct responsibility. Omit empty type groups; actual Work Blocks show instances without compulsory type definitions. Keep existing directories and drawings when their type classification changes.

**Check:** The structure check rejects a local bands override and requires source references for s01–s03 and s99. b11 owns content and bindings; Work owns the shared registry, reader and service lifecycle.

## A04 · Rules and examples share their content item

**Rule:** Block Structure uses Structure / Job types / Task types / Draw / Skills. The shared block_types_pages.py generates the two type views from each instance's types.md. Folder, Job-Task and Studio pair naming rules with available actual examples. A rule uses contract names and 〈variable names〉; an instance uses verified paths. One source is referenced at multiple scopes, never copied for display.

**Check:** The structure check verifies the paired content, source paths, catalog-generated type views and the five-view manifest. The real example opens through the shared corner dot.

## A05 · Previews distinguish execution from design

**Rule:** Block Job UI Preview embeds real Block Job/Task selections, owning type contracts, QuickHtml proposals and Draw. Outputs stay in their files. Concrete implementation comparisons use the shared Checklist; no extra Delivery/Instances top view is required for this type. Other Studio types retain their own contracts.

**Check:** build_job_previews.py --check verifies real file targets, Block-only routes and actual selected folders. Browser acceptance checks the selection and proposal independently. A proposal is not evidence that the real page implements its behavior.

## A06 · Skills state the current contract

**Rule:** Skill instructions describe the current responsibilities and supported operations. Decisions and event narratives are kept in the owning Block's Trace. Preserve active dependencies until their callers and generated sources can be changed together.

**Check:** check_structure.py scans the current instruction bodies for replaced-UI narratives. Fresh-context invocation verifies source membership, execution ownership, neutral questions, independent review and actual human signatures.


## A07 · Catalogs separate grouping from responsibility

**Rule:** Each of the three Block Structure instances has types.md with Job group type, Job type, Task group type and Task type sections. Every real type states for, holds, source and owner. A missing layer states why it is absent and contains no fabricated type. The catalog describes the existing semantic contract; version ids, segments and DIKWX labels do not become new Job/Task types. Resolve all release members and preserve their authoritative source references.

**Check:** check_structure.py rejects missing catalogs, undocumented absence, missing responsibilities/owners and unlisted types. It checks full Book membership, Board question pins and Prep code/execution ownership. Shared block_types_pages.py --check validates the generated views. Shared absent-layer and source-aware member support remain explicit interface gaps; zero types is never a successful inventory.

## A08 · A Work Block's Studio organization names its real scope

**Rule:** Structure › Studio defines applicable ordinary Work bands and numbering from hai-studio's writer, with proposed topic purposes in 〈〉 and their Block/Job/Task owner. It is separate from the Blueprint Band registry. Actual examples preserve existing identifiers and use the shared configured-band, group-order and tag readers; no proposed topic is inserted into the actual tree. No empty Studio is created to fill a category.

**Check:** check_structure.py compares proposed ranges to the shared writer and actual topics to their source owner/band. The source model preserves identities, authored words and branches during refresh. The browser shows the rule and available actual example in their own folds.
