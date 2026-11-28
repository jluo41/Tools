# A03 · Progress is read live, never typed in

> "please make the report to be as helpful as possible?" (JL 261118)

## 1. Need
The progress JL reads must be true at the moment he reads it, and the drawing must never carry a secret.

## 2. Now
The first sketch B was typed by hand: "first upload 0 docs, stuck". Minutes later CouchDB held 476, then
951, then 29,461 docs (curl `http://127.0.0.1:5984/notes_vault`), so the drawing was wrong.

## 3. Gap
A builder had no habit or helper to read the real state; numbers went in as literals in `sketch_b`. Reading
the state needs the CouchDB login from `deploy/.env`, with the risk of drawing it.

## 4. Methods
1. Redraw by hand after each change: stale between redraws; rejected.
2. A `probe()` in the topic's sketch: docker state, the tunnel's HTTP code, doc_count, flag file, backup,
   Docker AutoStart, QR file; secrets read from `.env` and never passed to a text element. Chosen.
3. A shared probe library in hai-studio: premature with one case; left open.

## 5. Update
- `s01-how-livesync-works/sketch_how_livesync_works.py`: `probe()`, `steps()`; feeds Design B and Now

Cases: ✅ b01_livesync s01 · ⬜ Job results topics (job_results.py reads disk already, not audited).
Run: no "password" in any .excalidraw under Project-Notes-Sync, and "live 26" stamp in s01; ✅ (261118).
Found on the way: Cloudflare answered 403 to Python's default User-Agent; the probe sends one curl uses.

## 6. Never again
Each rebuild reads the state again and stamps the time ("live 261118 16:22"), so a stale number shows its
age. The Run line fails if any canvas in the Project holds "password". Open risk: steps no machine can see
(plugin configured, overwrite confirmed, phone joined) are still typed.
