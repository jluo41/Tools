# User-check packet

This is the reader-facing completion contract for a Page. It is the small
packet a person uses to inspect the result in chat; it is not a replacement for
the phase receipt, the evidence ledger, or the workflow audit bundle.

## When it is required

Technical file intake, standalone source editing and static-site setup use the
handoff in `standalone.md`. They do not require a scholarly writing Run, PDF,
Board membership or formal review packet. For substantive writing and formal
delivery below, a verified standalone Page workspace may supply the same
Outline/Evidence routes; Board hosting is optional. Always use the repository's
configured reader-facing origin.

Return this packet after any action that changes a Page, its current plan,
Page-local evidence or display units, Page Content, or a derived Page
projection. A read-only audit returns the same packet with current statuses but
does not rebuild anything unless the person asked for a rebuild.

Select the routine writing packet below for a feedback Step. The four-surface
packet is for formal review/delivery. For that formal packet, the main response
contains these four user-check surfaces plus the read-only Delivery Workspace
consistency receipt. Detailed
source paths, logs, manifests, hashes, and phase receipts stay in the durable
records and may be mentioned only when they explain a missing or stale surface.

When a person says enter, continue, resume, or review an open Page Run before
giving new feedback, use the pre-Step review packet below. It shows the latest
saved candidate, the fixed structure/Section/paragraph scope, the frozen
Mermaid Structure description for every selected paragraph when prose is in
scope, and the next proposed Step number. It does not append a new Step or
claim a new durable record. Never return only a status summary or links when
the person has asked to enter a Step: return the full selected scope, Mermaid
descriptions where applicable, sentence labels for prose, review scope, and
all three links.

## Routine interactive writing · return what the person can review

### Entering or resuming an open Step · pre-Step review packet

Use this packet before new feedback arrives:

```markdown
## ✍️ <rp-struct-NN | rp-sec-NN | rp-para-NN_Pxx[-Pyy]> · next Step <vNNN/sNNN>

### P01 · <C.P> · <Mermaid Structure description>

> **S1** <latest complete saved sentence>
>
> **S2** <latest complete saved sentence>

### P02 · <C.P> · <Mermaid Structure description>

> **S3** <latest complete saved sentence>
>
> **S4** <latest complete saved sentence>

Review scope: <the numbered paragraphs and plan addresses in this Run>
Reply with sentence-numbered feedback, acceptance, or an explicit close.

[Draft Space](<verified direct URL>) · [Evidence Space](<verified direct URL>) · [Current Run](<verified Runs URL with &run=<exact-run-id>>)
```

The `next Step` label is a proposed input location, not a saved Step. For a
Section-level Run, the saved Step must include the complete draft →
review/rating → diagnose → revise cycle and the post-revision
review/diagnosis. Do not
write `sNNN` to the Version journal until the person supplies feedback,
acceptance, or an explicit close. Resolve each description from the closed
`rp-struct-01` index or its authored `outline/<stem>-logic.mmd`; if
the description is missing or ambiguous, show a named blocker rather than
inventing one.

After a saved writing Step:

1. Start with the exact durable identity as the heading:
   `## <rp-struct-NN | rp-sec-NN | rp-para-NN_Pxx[-Pyy]> · <vNNN/sNNN>`.
   For example, `## rp-para-01_P03 · v001/s003`. The Run id states which
   interaction is open;
   its scope suffix states the fixed structure, Section, or paragraph target.
2. Immediately show the complete saved candidate for the fixed Run scope. For
   a paragraph Run, show the full selected one-to-three paragraphs in reader
   order, including unchanged sentences. Put each paragraph under its own
   visible `### PNN · Cn.Pm · <Mermaid Structure description>` label and its
   own Markdown blockquote. For a Section Run, show the complete Section
   candidate followed by its review/rating, diagnosis, revision summary, and
   post-revision review/diagnosis. For a structure/Bullet Run, show the
   Mermaid map, ordered Bullets, and the `P01..PN` index. Sentence labels are
   chat review coordinates only. Prefix every sentence with a stable bold
   review label, but do not write those labels into the Workspace candidate or
   final Page Content. Use exactly the saved Workspace's reader
   projection, not a newly polished chat version. Keep evidence placeholders
   honest in the source; use the same compact labels as the Workspace in the
   chat passage.
3. Then briefly explain what changed and why. Default to one concise paragraph,
   not a fixed three-bullet status block. Use itemized dispositions only when
   several feedback items genuinely need separate treatment. Distinguish
   agent-applied from human-accepted, and name an unresolved item instead of
   hiding it in a summary. Do not append a routine Content-state line unless
   that state itself changed.
   Do not add an empty Bullets/Evidence recap. Add evidence commentary only
   when this Step changed or left unresolved a citation, value, or figure need.
   The durable Current Run record also keeps one Track Changes card per material
   wording change: clean Before and After text, a local change type, and the
   reason. The presenter
   computes red strikethrough deletion and green underlined insertion at the
   smallest practical word/punctuation span; unchanged context stays plain.
   Use a whole-sentence deletion/insertion only when the whole sentence changed.
   Keep source prose free of diff markup. Interactive Page Steps defer
   preference inference to post-run analysis; a non-record-first host may ask
   explicitly for a provisional Page-local inference.
   Put the classification in the card heading rather than a duplicate table.
   Acceptance, status, navigation, and presenter-only Steps create no Track
   Changes card. Current Run expands only the latest Step; earlier Steps remain
   collapsed until the reader opens them.
4. Show the Section Mermaid before the paragraph only when the argument or
   paragraph relationships changed; a wording edit needs no repeated diagram.
5. For a routine writing packet, put **all three direct clickable links at the very end**:
   `[Draft Space](<verified …&lens=div>) ·
   [Evidence Space](<verified …&lens=evidence>) ·
   [Current Run](<verified …/_board/runs?path=…&file=…&run=<exact-run-id>>)`. The
   Current Run route opens the readable Run projection and expands its current
   Step plus prior history; it is not a raw Markdown, result-directory, or
   Python implementation link.
   Nothing, including source paths or a work summary, follows those links. A
   formal delivery packet adds `[Delivery Workspace](<verified …&lens=delivery>)`
   after the Current Run link; that receipt is the source-to-artifact check,
   not a second human approval gate.

The current candidate is `planning draft`, not automatically published Content.
Do not append the full audit packet, PDF or whole Section to each local turn.
Provide them when explicitly requested or when this turn actually changed those
artifacts. A stale PDF is labelled stale and never delays a prose-only turn.

Between Steps or Runs, follow
`../../page-workflows/haipipe-page-workflow/ref/interactive-execution-policy.md`.
If a heavy action is useful, return its scoped approval request first; do not
start it silently while preparing the next paragraph packet.

Save raw feedback before editing, and save/re-read the updated Markdown and Step
result before saying it is available. The live Outline reads Markdown: a local
preview save does not require a full Board/PDF build. Perform narrow mapping,
evidence-boundary and unchanged-scope checks. Only refresh affected generated
surfaces needed for this response; remaining work is named, not falsely
reported as complete. Use exact routes previously verified against the configured
public origin while their origin and routing remain unchanged. A new or changed
route needs a lightweight HTTP check; a routine writing Step does not need browser
automation or a full rebuild. If a route is unavailable, say so concisely rather
than inventing a live link or substituting a localhost/raw-HTML URL.

## The four surfaces (JL 260907: "在写 page 的时候，response 里要强调")

```text
1. Draft and Evidence Spaces
   return both direct links from the same verified Board route:
     🧭 Draft Space  `<Board URL…&lens=div>` · Mermaid + read-only paragraph/Draft table
     ▤ Outline table    `<Board URL…>` · the compact Page projection
   The `lens=div` link is the direct Draft Space route; do not make the
   reader open the default Page and hunt for the tab.
   `<Board URL>` means the verified page-specific `/_board/outline?path=…&file=…`
   route; preserve its query and append these parameters (use `?` only when a
   base route has no query string).

2. Evidence you can open now
   return the direct Evidence Space route even when no item is ready:
     `<Board URL…&lens=evidence>`
   one compact card per current Result, grouped by type:
     🖼 DISPLAY  the unit's standalone `preview.pdf` (figure or table);
                an unaccepted but freshly rendered preview is still a current draft
     📚 CITE     the current typed CITE Result card in Evidence Space
     🧮 VALUE    the item's card in the Evidence Space (one-URL route
                `lens=evidence&focus=run-<item>`), which names the value,
                its Run and its Result
   plus the direct Evidence Space → typed section/card link above.  Do not use the
   embedded `/_board/evidence?...&embed=1` iframe URL as the primary response
   link; it is an implementation detail of the Outline plugin.
   An item that is not ready is listed as `not current · <blocking step>`.

3. Content state
   during SHAPE: label the right column `planning draft`; state that Page
   Content and PDF were not refreshed by preview edits.
   after CONTENT/WRITE: the Page version and whether Revise ran
   (`revised · owner policy checked · style verdict ✓`) or not (`first draft · not yet
   revised`). When Writing DNA is used, the Content state may also name its
   frozen profile and `full`/`partial` status; detailed artifact and exemplar
   provenance remains in the Paragraph Run trace. A first draft is never
   presented as final content.

4. Latest Page-level PDF (delivery)
   the compiled PDF for THIS Page/Section from `delivery/latex/<stem>.pdf`,
   shown AFTER Revise; before Revise it is labelled `draft PDF`. Not a
   configuration file, not a display preview, and not the paper-level master.
```

For formal review/delivery, use this compact shape. Put the clickable links
in the final user-check block, after prose/status commentary:

```markdown
## 👀 User check

1. Draft Space: [Open Draft Space](<verified configured Board URL…&lens=div>)
   Outline table: [Open Outline table](<verified configured Board URL>)
2. Evidence Space: [Open Evidence Space](<verified configured Board URL…&lens=evidence>)
     🖼 [<Display id>](<resolved Result payload>/preview.pdf) · 📚 [<CITE item>](<…&lens=evidence&focus=run-<item>>) · 🧮 [<Value id>](<…&lens=evidence&focus=run-<item>>)
3. Content: v<G>.<S> · revised · owner policy checked · style verdict ✓   (or: first draft · not yet revised)
4. Latest Page-level PDF: [Open the Page PDF](<page>/delivery/latex/<stem>.pdf)
```

If no Evidence Item is declared, write `none declared for this Page`; do not
invent a link. If a DISPLAY Result has a fresh payload `preview.pdf` but its
human `accepted:` gate is still open, link it and label it `current draft ·
acceptance pending`. Human acceptance is a separate gate and does not hide a
usable draft preview. If a DISPLAY Result's `preview.pdf` is missing or stale,
write `not current` with the blocking step. If the Page has no Content yet,
surface 3 reads `no Content yet · <current Run or named blocker> · <next action>` and surface 4 is omitted. If
the Page PDF build failed, write `not current` with the build failure and, when
useful, label the last successful file explicitly as `stale`, never as latest.

## Artifact identity

The current display review artifact is the `preview.pdf` inside the current
DISPLAY Result payload, generated from its frozen intake, recipe, winning asset,
and wrapper. The Result payload is the user-check link; a retired Outline
Evidence unit is never substituted.

The citation and value surfaces are the Evidence Space item cards reached by
the one-URL route (`lens=evidence&focus=run-<item>`). A card names the current
Result payload and its provenance; do not paste raw numbers or create a second
citation register in the Page Folder.

The only eligible Page-level artifact is
`<page>/delivery/latex/<stem>.pdf`, the LaTeX Delivery lane's compiled Page.
There is no fallback to a page-local `latex/` directory. The returned label
must say **Page-level PDF** and must identify the one Page it represents.
Never substitute a paper master, a desk-room build, a Word export, or an
outline/configuration file. A Page that is not CHECK-closed may still return a
fresh draft Page PDF; label its lifecycle state rather than hiding the
readable artifact.

Resolve DISPLAY previews and CITE payloads only from the current Result named
by the Evidence Item card. Do not search, read, or return `outline/evidence/`,
flat `display/` or `bibex/`, root `evidence/`, or any other compatibility lane.
An old artifact belongs in `_archive/legacy-outline-evidence/` and is not
eligible for the user-check packet. If the current Result or payload is absent,
report `not current · Result required` and do not fall back.

## Freshness and link checks

Before returning the packet:

1. for formal delivery, rebuild the Board when its generated Page projection
   changed; for a routine writing Step, use the live-source checks above;
2. rebuild each affected DISPLAY unit's `preview.pdf` when its intake, recipe,
   asset, or wrapper changed, and the citation register when the `.bib` changed;
3. before calling a formal version revised, use its actual scoped writing/review
   record; do not rerun a prose-changing worker over human-accepted text.
   Rebuild the requested Page-level PDF after adopted Page prose or an embedded
   display changed. Routine preview changes do not refresh published Content;
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
