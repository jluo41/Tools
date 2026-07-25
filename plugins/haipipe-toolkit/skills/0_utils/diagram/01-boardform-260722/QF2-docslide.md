# Doc slides: source files as a slide, no Q wrapper
state: ✅ SETTLED
owner: JL
method: `doc:` remains a generic view; lifecycle use was superseded 260725 by canonical S faces

## Question
When a slide should just SHOW a folder's own documents, why wrap them in a Q file at all?

JL's ask (260724, after seeing the embed route): "could we don't have the embeds? but just
convert the content [1b-claims.md + _LOG_1b-claims.md] to html webpage directly. No need to
generate QB3-claims.md." A doc slide is that: a Roster line `doc: <path> <path>...` renders
the listed files straight onto one slide via the generic renderer. No face file exists, so
there is also no state pill, no Items to Finish counting, and no comment write-back target;
doc slides are views, not questions, and stay out of the settled count and the progress bar.
The capability remains useful for read-only sources, but lifecycle stages now need state,
Content, finish items, and a gate, so they use S faces instead.

## Boundary
- ✅ Covered here
  The `doc:` Roster grammar, what a doc slide shows and deliberately lacks, and which faces on
  the first consumer convert.
- ↪ Covered elsewhere
  Embeds inside a Q face (`![[path#Section]]`) remain QF1 law; a doc slide replaces the face,
  an embed enriches one.

## Items to Finish
- [x] ✍️ `doc:` grammar shipped
      parse.py reads `doc:` lines in the Roster (any group, files explicit so `_LOG_*.md` can be shown even though `_` files are excluded from Q discovery); id = first file's stem, title = its own `#` or setext title.
- [x] 🎞 Renderer shipped
      page_stage.render_doc_slide: files stacked, each under a linked header, generic rendering, missing files flagged visibly; excluded from done/N and the bar.
- [x] 🧪 Pilot on the first consumer
      The MISQ board first proved the direct-source view on 1b-claims. That historical pilot
      was later replaced by `S1b-claims.md` when stages gained the shared face contract.
- [x] 🧠 Conversion scope ruled
      JL 260724: "I think 14 ruling faces" — only rulings remain Q files. The first
      implementation used 14 Q + 8 doc slides; the current implementation preserves that
      split of responsibility as 14 Q + 8 S faces with separate progress counts.
- [x] 📖 Graduation
      The `doc:` grammar in ref/board-form.md §3 (id = first file's parent folder, else stem), one line in SKILL.md's 🗂 section, CHANGELOG 0.11.0.

## Where we are
Settled as a generic capability, then narrowed by the 260725 lifecycle design. The first
consumer now runs 14 Q faces + 8 S faces and has no `doc:` roster lines. A doc slide remains
the right tool only when a source is intentionally read-only and needs no state, checklist,
gate, or write-back target.

## Files
- `src/parse.py`
  `parse_doc` + the Roster `doc:` branch.
- `src/page_stage.py`
  `render_doc_slide`.
- `src/page_board.py`
  Index row, dispatch, and the doc-excluded progress counts.
- `0-lifecycle/`
  First consumer; the pilot slide is `1b-claims`.

## Law
- A Roster `doc:` line renders its listed files directly as one slide; files are explicit, including files normally excluded from face discovery.
- id = the first file's parent folder when it has one, else the file's stem; title = the first file's own `#`/setext title, else the id.
- Doc slides are views, not questions: no state, no Items counting, no comment target; excluded from the settled count and the progress bar.
- The deck's split of labor: rulings are Q files; lifecycle stages are S files; `doc:` is reserved for read-only source views.

## Log
260725 · lifecycle scope superseded by the shared Q/S face: the MISQ board is now 14 Q + 8 S with no doc slides; generic `doc:` support remains
260724 · scope ruled ("14 ruling faces") and applied; QF2 settled and graduated
260724 · capability shipped; pilot live on the MISQ board; scope ruling pending
