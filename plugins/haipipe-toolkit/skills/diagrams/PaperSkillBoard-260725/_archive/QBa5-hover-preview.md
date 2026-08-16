# Hover preview without hidden truth
state: ✅ SETTLED
owner: JL
method: resolve typed attachments into optional hover cards while preserving a readable no-script page

## Question
What should a reader see when hovering over a citation, value, table, figure, or other Display reference?

The Board can make source inspection immediate, but the hover layer must remain a convenience rather than the only place evidence exists. Every attachment needs a visible fallback link or drawer, and the generated page must still contain the full readable substance when scripts are removed.

## Boundary
- ✅ Covered here
  HTML interaction for sentence attachments and the no-script fallback.
- ↪ Covered elsewhere
  Attachment identity and provenance are `QBa4`; the generic Display preview is produced under `QD2`.

## Content
### Preview by attachment type
```
Citation   title, authors, year, venue, key, source link, verification state
Value      rendered value, unit, source path, producing run, verification state
Display    thumbnail or table preview, caption job, owning S page, live asset
```

### Progressive enhancement
Hover opens the quickest view.
Click opens a persistent drawer or the owning page.
Without JavaScript, the semantic id, state, and source link remain visible in the HTML.

### Resolution
The Board resolves semantic ids at build time where possible.
A missing or ambiguous target is rendered as an explicit broken attachment rather than silently dropped.

## Items to Finish
- [x] 👁 Choose hover as an inspection convenience
      The reader can see the object without leaving the sentence.
- [x] 🧱 Preserve a no-script reading path
      Hover enhancement may not hide the only copy of provenance or Content.
- [ ] 📐 Define each preview card schema
      Citation, Value, and Display need different compact fields.
- [ ] 🧪 Build three live examples
      Test one citation, one value, and one table or figure with broken-target cases.

## Where we are
The interaction direction follows the Board's enhancement invariant.
The attachment resolver and preview cards do not yet exist.

## Files
- `haipipe-board/build.py`
  The build-time resolver.
- `haipipe-board/assets/`
  The optional hover and drawer behavior.
