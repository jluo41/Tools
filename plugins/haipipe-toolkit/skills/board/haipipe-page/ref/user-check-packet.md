# User-check packet

This is the reader-facing completion contract for a Page. It is the small
packet a person uses to inspect the result in chat; it is not a replacement for
the phase receipt, the evidence ledger, or the workflow audit bundle.

## When it is required

Return this packet after any action that changes a Page, its current plan,
Page-local evidence or display units, Page Content, or a derived Page
projection. A read-only audit returns the same packet with current statuses but
does not rebuild anything unless the person asked for a rebuild.

The main response contains only these three user-check surfaces. Detailed
source paths, logs, manifests, hashes, and phase receipts stay in the durable
records and may be mentioned only when they explain a missing or stale surface.

## The three surfaces

```text
1. Outline table
   the verified reader-facing Board Page URL; this is where the current
   generated `▤ Outline table` is read

2. Latest Display PDF(s)
   one link per current Page DISPLAY unit to its standalone `preview.pdf`;
   an unaccepted but freshly rendered preview is still a current draft

3. Latest Page-level PDF
   the compiled PDF for THIS Page/Section, not a configuration file, not a
   display preview, and not the paper-level master PDF
```

Use this exact compact shape in the user-facing reply:

```markdown
## 👀 User check

1. Outline table: [Open the Board Page](<verified configured Board URL>)
2. Latest Display PDF(s): [<Display id>](<unit>/preview.pdf) · …
3. Latest Page-level PDF: [Open the Page PDF](<page>/delivery/latex/<stem>.pdf)
```

If no DISPLAY unit is declared, write `none declared for this Page`; do not
invent a display link. If a DISPLAY unit has a fresh `preview.pdf` but its
human `accepted:` tick is still open, link it and label it `current draft ·
acceptance pending`. Human acceptance is a separate gate and does not hide a
usable draft preview. If a DISPLAY unit's `preview.pdf` is missing or stale,
write `not current` with the blocking step. If the Page PDF build failed,
write `not current` with the build failure and, when useful, label the last
successful file explicitly as `stale`, never as latest.

## Artifact identity

The current display review artifact is the unit's `preview.pdf`, generated
from the unit's frozen intake, recipe, winning asset, and wrapper. The winning
`assets/figure.pdf` is a renderer output and is not the primary user-check link
when the standalone preview exists.

The only eligible Page-level artifact is
`<page>/delivery/latex/<stem>.pdf`, the LaTeX Delivery lane's compiled Page.
There is no fallback to a page-local `latex/` directory. The returned label
must say **Page-level PDF** and must identify the one Page it represents.
Never substitute a paper master, a desk-room build, a Word export, or an
outline/configuration file. A Page that is not CHECK-closed may still return a
fresh draft Page PDF; label its lifecycle state rather than hiding the
readable artifact.

Resolve DISPLAY units only from the current lane:
`<page>/outline/evidence/display/<unit>/preview.pdf`. Do not search, read, or
return legacy `<page>/display/`, root `evidence/`, flat `display/`, or any
other compatibility lane. An old artifact may remain historical material, but
it is not eligible for the user-check packet. If the new path is absent, report
`not current · new Display lane required` and do not fall back.

## Freshness and link checks

Before returning the packet:

1. rebuild the Board when the Page or its plan changed;
2. rebuild each affected DISPLAY unit's `preview.pdf` when its intake, recipe,
   asset, or wrapper changed;
3. rebuild the Page-level PDF after Page prose or an embedded display changed;
4. verify that every linked file exists and is newer than the source it
   projects, or report it as stale;
5. verify the exact configured `JJLUO_PUBLIC_URL` Board route with a
   lightweight successful request before returning it as a link.

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

Say **Page** or **Section Page** for the third surface. Say **Display PDF** for
the standalone unit preview. Say **Outline table** for the generated plan
projection on the Board Page. Do not call the Page-level PDF a “config PDF” or
collapse these three surfaces into one generic “artifacts” list.
