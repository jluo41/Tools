The portal packet: the built files uploaded as they are, one per portal slot, and its states (haipipe-paper-assemble).

## 📮 The portal packet · what is uploaded as it is (0.13.0)

JL 261102: "here we might want to say the final delivery content that are ready to submit directly in the
portal". A send ends in a venue's portal, slot by slot (manuscript, supplement, one file per figure, cover letter,
source, forms). paper-build.toml `[portal]` names each slot and the built file that fills it; the build copies those
files into `delivery/<writing Job>/portal/` and writes `portal/portal.md`, one row per slot with its state. A person
uploads the folder's files into the slots the table names, and nothing else.

```text
[portal]              folder = "portal" (GENERATED, emptied every build)
[[portal.upload]]     slot · from (a path or glob under delivery/<job>/; all = true takes every match)
                      · as (its name in the packet) · draft = true (the build's G4 state applies)
                      · matches = "latex" (a ZIP made by hand: stale when a file in it differs from latex/)
                      · note (one line beside the slot)
states                ✅ ready · 🔶 built, not approved (draft = true while the build is DRAFT)
                      · ❗ stale · ⬜ missing (a slot the venue asks for that has no file yet)
receipt               build-manifest.json "portal": folder, uploads (slot, files, state, detail), ready, total
```

List every slot the venue asks for, also the ones with no file yet, so a missing form shows as ⬜ instead of being
forgotten.
One manuscript slot only: the file the venue's call asks for (MISQ: the PDF), never a Word copy beside it
(Pp-AgreeableRx 261122: "Manuscript (Word)" next to the PDF; JL: one manuscript only). The slots come from `venues/<venue>/call.md` or the version's submission report (its `checklist.md`).

A file made AFTER the build (a venue ZIP from `npj-zip.sh` or `arxiv-zip.sh`) reaches the packet only through
`build.py portal` (0.14.1), which rewrites the packet from the last manifest: it copies the newest file in and checks
`matches` again. The ZIP script calls it as its last step, so the order is build.py, then the ZIP script, and
`portal/` never holds an older ZIP under the new day's name (FairGlucose 261103).
The packet never decides the send: `sent` is still a person's line in `delivery/delivery.md` (haipipe-delivery),
and the Writing view of the paper workbench shows the packet under the assembled paper.
