# r01_read_portal · read the portal, read only

A person starts this Run: only a person logs in, and the walk needs a saved draft of this send in the venue's portal.

1. The person opens the portal in their own browser, logs in, and opens the draft.
2. An agent reads each step of the portal, top to bottom, and writes `result/portal-fields.yaml`: every step and field,
   its options, what the portal says about it (`says`) and what the draft holds now (`now`).
3. Nothing is typed, ticked, uploaded, saved or submitted during the walk. Stop at any screen that would change the draft.
4. Keep ids stable across walks: `portal-values.yaml` is keyed by them. Put no link holding a session or a token in the file.

A later walk is a new Run (r02_…); `portal_fill.py` reads the highest-numbered one that has the file.
