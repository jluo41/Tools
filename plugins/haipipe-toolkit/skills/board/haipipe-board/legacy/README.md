# Legacy compatibility

Nothing in this folder defines current Board or Page authoring.

| File | Retained only for |
|---|---|
| `pagex.py` | opening already-rendered historical PageX links; read-only |
| `meetingpage.py` | migrating old Page-local meeting Pages |
| `xcal.py` | reseeding old Board-wide Excalidraw scenes |
| `aims-fold-to-p.py` | one-time Aim grammar migration |
| `states-merge.py` | one-time retired State-section migration |
| `states-fixup.py` | second pass for that State migration |
| `evidence.py` | inspecting the retired route-based evidence-topic shape |
| `topic_entry_contract.py` | checking that same historical evidence shape |

Current commands live in `../cli/`. Current code must not import a legacy
writer. The only runtime exception is the read-only PageX view bridge used to
keep old links navigable.
