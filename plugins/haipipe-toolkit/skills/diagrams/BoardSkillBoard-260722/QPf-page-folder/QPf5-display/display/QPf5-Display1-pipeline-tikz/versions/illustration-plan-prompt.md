# Rebuild spec · QPf5-Display1-small-paper

status: PLANNED, NOT RENDERED
blocker: the codex-image2 MCP bridge is not registered in this session
         (mcp-servers/codex-image2 is absent from the toolkit; the skill's
         strict rule forbids a shell/Python bitmap fallback)
renderer: haipipe-display-illustration (codex-image2 native image generation)
target_score: 9
bridge_call:
  tool: mcp__codex-image2__generate_start
  cwd: <this page folder, QPf5-display/, as the workspace>
  outputPath: figures/ai_generated/figure_v1.png   # bridge hard-locks scratch here
  system: Academic paper figure. Prefer crisp English labels.
  timeoutSeconds: 180
finalize:
  helper: paper_illustration_image2.py finalize --workspace <page folder> \
          --display-unit display/QPf5-Display1-small-paper \
          --best-image figures/ai_generated/figure_vN.png \
          --caption "A page as a small paper: the probe plugin asks once, the bank answers behind the wall, and the display intake and the page sentence cite the same card by id." \
          --label "fig:qpf5-small-paper" --placement "t"

## Final image prompt (steps 1-3 complete: plan, layout, style)

Academic method figure, clean white background, sans-serif English labels,
horizontal left-to-right flow, three coordinated muted colors (slate blue,
warm gray, soft green), thick dark arrows with large arrowheads, no shadows,
no gradients beyond subtle same-family fills, grayscale-safe.

LAYOUT, left to right, four groups with generous whitespace:

1. LEFT · a tall document panel labeled "Board page" containing two small
   elements stacked: a text line "claim: ... (PP01)" and a folder row
   "display/ · probe/" drawn as two small folder tabs attached to the
   document's lower edge. Subtitle under the panel: "a page is a small paper".

2. CENTER-LEFT · a card labeled "probe/PP01 card" with three short rows:
   "question", "state: raised -> working -> bound", "binding -> QA/3".
   This card is the visual center of the figure; slightly larger stroke.

3. CENTER-RIGHT · a vertical dashed line labeled "the wall" separating the
   page side from a panel labeled "the bank: tasks / discoveries" containing
   "QA/3-drift.md + counts.csv". One thick arrow from the card rightward
   through the wall labeled "question, general language"; one thick arrow
   returning labeled "answer, bound by id".

4. RIGHT · a panel labeled "display/unit" with rows "intake: probe: PP01",
   "recipe -> assets -> preview.pdf", and a small human silhouette with a
   checkmark labeled "a person accepts".

KEY MECHANISM to make unmistakable: TWO thin citation arrows converge on the
single probe card, one from the page's claim text ("cited in a sentence") and
one from the display unit's intake row ("cited by manifest"); annotate the
pair "ask once, cite twice". The binding arrow from bank to card is the only
place an answer path touches the page side.

AVOID: rainbow colors, 3D, glow, drop shadows, clip-art icons, thin hairline
arrows, any real number on the figure, any crossing arrows.
