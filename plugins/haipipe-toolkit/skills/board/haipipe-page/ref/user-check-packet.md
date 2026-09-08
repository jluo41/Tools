# User-check packet

This is the reader-facing completion contract for a Page. It is the small
packet a person uses to inspect the result in chat; it is not a replacement for
the phase receipt, the evidence ledger, or the workflow audit bundle.

## When it is required

Return this packet after any action that changes a Page, its current plan,
Page-local evidence or display units, Page Content, or a derived Page
projection. A read-only audit returns the same packet with current statuses but
does not rebuild anything unless the person asked for a rebuild.

The main response contains only these four user-check surfaces. Detailed
source paths, logs, manifests, hashes, and phase receipts stay in the durable
records and may be mentioned only when they explain a missing or stale surface.

## The four surfaces (JL 260907: "在写 page 的时候，response 里要强调")

```text
1. Outline table
   the verified reader-facing Board Page URL; this is where the current
   generated `▤ Outline table` is read. This IS the Page link.

2. Evidence you can open now
   one line per typed Evidence Item whose Result is ready, grouped by type:
     🖼 DISPLAY  the unit's standalone `preview.pdf` (figure or table);
                an unaccepted but freshly rendered preview is still a current draft
     📚 CITE     the Page's citation register `outline/evidence/bibex/<stem>-bib.html`,
                or the Evidence Workspace 📚 Citations segment when no register is built
     🧮 VALUE    the item's card in the Evidence Workspace (one-URL route
                `lens=workspace&seg=items&focus=run-<item>`), which names the value,
                its Run and its Result
   plus ONE link to the Evidence Workspace → Evidences of this Page.
   An item that is not ready is listed as `not current · <blocking step>`.

3. Content state
   after CONTENT/WRITE: the Page version and whether Revise ran
   (`revised · humanizer ✓ · style verdict ✓`) or not (`first draft · not yet
   revised`). A first draft is never presented as final content.

4. Latest Page-level PDF (delivery)
   the compiled PDF for THIS Page/Section from `delivery/latex/<stem>.pdf`,
   shown AFTER Revise; before Revise it is labelled `draft PDF`. Not a
   configuration file, not a display preview, and not the paper-level master.
```

Use this exact compact shape in the user-facing reply:

```markdown
## 👀 User check

1. Outline table: [Open the Board Page](<verified configured Board URL>)
2. Evidence you can open now: [Evidence Workspace](<Board URL…&lens=workspace&seg=items>)
   🖼 [<Display id>](<unit>/preview.pdf) · 📚 [citations](<page>/outline/evidence/bibex/<stem>-bib.html) · 🧮 [<Value id>](<…&seg=items&focus=run-<item>>)
3. Content: v<G>.<S> · revised · humanizer ✓ · style verdict ✓   (or: first draft · not yet revised)
4. Latest Page-level PDF: [Open the Page PDF](<page>/delivery/latex/<stem>.pdf)
```

If no Evidence Item is declared, write `none declared for this Page`; do not
invent a link. If a DISPLAY unit has a fresh `preview.pdf` but its human
`accepted:` tick is still open, link it and label it `current draft ·
acceptance pending`. Human acceptance is a separate gate and does not hide a
usable draft preview. If a DISPLAY unit's `preview.pdf` is missing or stale,
write `not current` with the blocking step. If the Page has no Content yet,
surface 3 reads `no Content yet · phase <PHASE>` and surface 4 is omitted. If
the Page PDF build failed, write `not current` with the build failure and, when
useful, label the last successful file explicitly as `stale`, never as latest.

## Artifact identity

The current display review artifact is the unit's `preview.pdf`, generated
from the unit's frozen intake, recipe, winning asset, and wrapper. The winning
`assets/figure.pdf` is a renderer output and is not the primary user-check link
when the standalone preview exists.

The citation surface is the Page's own register
`outline/evidence/bibex/<stem>-bib.html` (built by the bibex door from
`outline/evidence/bibex/<stem>.bib`). The value surface is the Evidence
Workspace item card reached by the one-URL route the compact Outline table
already uses (`lens=workspace&seg=items&focus=run-<item>`); do not paste raw
numbers into the packet, the card is the reader's source.

The only eligible Page-level artifact is
`<page>/delivery/latex/<stem>.pdf`, the LaTeX Delivery lane's compiled Page.
There is no fallback to a page-local `latex/` directory. The returned label
must say **Page-level PDF** and must identify the one Page it represents.
Never substitute a paper master, a desk-room build, a Word export, or an
outline/configuration file. A Page that is not CHECK-closed may still return a
fresh draft Page PDF; label its lifecycle state rather than hiding the
readable artifact.

Resolve DISPLAY units only from the current lane:
`<page>/outline/evidence/display/<unit>/preview.pdf`, and citations only from
`<page>/outline/evidence/bibex/`. Do not search, read, or return legacy
`<page>/display/`, flat `bibex/`, root `evidence/`, or any other compatibility
lane. An old artifact may remain historical material, but it is not eligible
for the user-check packet. If the new path is absent, report `not current ·
new lane required` and do not fall back.

## Freshness and link checks

Before returning the packet:

1. rebuild the Board when the Page or its plan changed;
2. rebuild each affected DISPLAY unit's `preview.pdf` when its intake, recipe,
   asset, or wrapper changed, and the citation register when the `.bib` changed;
3. run Revise (humanizer, then the fresh-context style verdict) before calling
   Content revised; then rebuild the Page-level PDF after Page prose or an
   embedded display changed;
4. verify that every linked file exists and is newer than the source it
   projects, or report it as stale;
5. verify the exact configured `JJLUO_PUBLIC_URL` Board route with a
   lightweight successful request before returning it as a link; the Evidence
   Workspace deep links share that origin.

The Board link must use the configured public origin and the resolved Board
slug/Page id. If the request fails, do not render the URL as a clickable
reader-facing link: write `Outline table: not available · Board route
verification failed` and name the service blocker. The configured URL may be
shown in backticks as diagnostic context only. Never return `localhost`,
`127.0.0.1`, `file://`, or a raw source Markdown path as the reader-facing
Outline link.

This packet is intentionally new-layout-only. Compatibility discovery is not
part of its contract.

## Scope language

Say **Page** or **Section Page** for the fourth surface. Say **Display PDF** for
the standalone unit preview, **citations** for the register, **value card** for
a VALUE item. Say **Outline table** for the generated plan projection on the
Board Page. Say **revised** only after Revise actually ran. Do not call the
Page-level PDF a “config PDF” or collapse these four surfaces into one generic
“artifacts” list.
