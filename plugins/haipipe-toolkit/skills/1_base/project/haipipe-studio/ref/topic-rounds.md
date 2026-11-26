# Rounds

Part of haipipe-studio's topic contract (`ref/topic-contract.md`).


A round on a topic is one working session (a chat that redrew it, a person's marks answered) or one meeting about it
(JL 261029). It is kept inside the topic, `passes/pNN-<MMDD>/pass.md`: its title, `kind: session|meeting`, Notes,
Decided, Started (what it sent to Work), Read (what it used from `related/`) and Changed. `new_topic.py session` writes
it. Older rounds in `runs/run-draw-<sNN>/passes/` and older `chat/` summaries stay readable until moved in.
