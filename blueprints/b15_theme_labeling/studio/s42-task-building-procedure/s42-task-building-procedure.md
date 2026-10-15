s42 · Task building procedure: from talking with the corpus to a signed Handoff
===============================================================================

**Tags:** `Levels`

**Stage:** shaping

**Topic:** every step of the 🏗 building Task (`task-type: labeling-building`, s13), drawn the way s41 drew the
items Task: one tab per step, Operation over Result, screens as the tab develops, and above them one workflow map of
who does what. Building takes the items Task's items and ends at a signed Label Handoff that the 🔍 scanning Task
reads. The person gets to know the corpus by talking with it before the meaning is fixed (JL 261014: "we want the
user to talk with the corpus and during the process to make the labeling ... get familiar with the labeling"). The
first real one is dices350 `t03_dices350_response_safety_labeling`. The law (who decides what, the gates, the verbs,
the step order) stays `haipipe-labeling-building`'s (SKILL.md, ref/step-order.md); this topic draws its screens.

**Feeds:** `reports/` q02_building_scanning_gates


Files
-----

```text
s42-task-building-procedure/
├── s42-task-building-procedure.md            this face; the drawing's words are the yaml block below
├── build_s42_task_building_procedure.py      the builder (s41's screens, plus the workflow map)
├── s42-task-building-procedure.excalidraw    ① the workflow map; Ⓑ the corpus, Run by Run; Ⓐ Algorithm 1; Ⓒ one round as a loop, then the Task as a tree; Ⓔ how the agent reads the corpus; Ⓕ design versions as the corpus grows; ② ③ Contract, ④ ⑤ Meaning, ⑥-⑨ Rounds, ⑩ ⑪ Handoff
├── s42-task-building-procedure.png           its preview
└── history/                                  the first draft, -261014a
```

```yaml
heading: ["① The building Task: who does what", "items → your labels, your guideline"]
key: "Outcome: your guideline G* and gold D*, signed as the Handoff. Only you make gold."
problem: "🎯 Problem: a researcher holds a subjective concept they cannot define up front. Today they write a codebook first, before seeing the data: it misses hard cases, and no one can say how well a labeler follows it."
novelty: "🏆 Contributions: a tool to build your own benchmark, then pick the labeler for all your data · C1 an interactive guideline: drawn out on real data, every rule yours (✨1) · C2 it transfers: a weak model following G* labels like you · C3 a benchmark that knows where it is unsure; quick: you read only borders (✨2), rounds pick the most valuable (✨3), a sealed exam (✨4)."
marks: [[0, 0, "✨4"], [5, 0, "✨3"], [6, 0, "✨2"], [7, 1, "✨1"]]
lanes: ["📚 corpus", "📜 guideline", "🤖 agent", "🏷 labeling agent", "🧪 open models E", "👤 you"]
lane_w: [360, 280, 380, 370, 340, 330]
symbols:
  title: "📐 Symbols: how many items, and who reads them"
  rows:
  - ["n", "all items, |X|"]
  - ["m", "the final exam, |S|"]
  - ["u", "the dev sample, |U|"]
  - ["r", "most you read in the talk"]
  - ["b", "you judge in a round"]
  - ["c_ask", "agent reads a talk pass"]
  - ["c_pick", "agent reads to pick"]
  - ["c_learn", "agent reads to learn"]
  - ["👁 0", "no item text"]
  - ["👁 1 a call", "one item a call"]
map:
- step: "📦 Stage 1 · Contract"
  screens: "② ③"
  cells: [[2, "seal(X, m)", "items X (n) · 👁 0", "🔒 S (m) · pool X∖S"]]
  corpus: "🔒 S (m) · pool X∖S"
  guideline: "G_0: empty"
- step: "💬 Stage 2 · Initial Labeling Definition"
  screens: "④ ⑤"
  cells: [[2, "get(sample(X∖S))", "a group · 👁 ≤ c_ask a pass", "c_ask items, questions"], [5, "read, write notes", "≤ r in all passes", "your notes, pass k"]]
  corpus: "N read (≤ r), set aside"
  guideline: "G_0 + your notes"
- cells: [[2, "draft(notes)", "your notes · 👁 0", "a draft"], [5, "✍ Sign (G0)", "the draft", "G_1 = guideline v1"]]
  corpus: "U drawn: no labels yet"
  guideline: "G_1 = v1"
  loop: "another pass"
  loop_to: 1
- step: "🔁 Stage 3 · Rounds"
  screens: "⑥ ⑦ ⑧ ⑨"
  cells: [[3, "lm_labeler(U, G_t)", "engine: the agent", "U: agent labels"], [4, "lm_labeler(U, G_t)", "engine: each in E", "P_t per model, sealed"]]
  corpus: "U: 2 labels each"
  guideline: "G_t labels U"
- cells: [[2, "sort_pools(A_t, P_t, 🧭)", "labels · the map · 👁 0", "7 pools"]]
  corpus: "H L N · HL LN HN HLN"
- cells: [[2, "find_neighbours(pools)", "X∖S · rank_by · 👁 ≤ c_pick", "b new items: card"], [5, "✍ Approve", "card", "the batch"]]
  corpus: "b from X∖S join U"
- cells: [[2, "show(picks, 📍)", "the b picked · 👁 b", "one at a time, in 3-D"], [5, "✍ JUDGE", "item + map", "+ gold"]]
  corpus: "+ b gold"
- cells: [[2, "learn(D, G_t)", "gold · 👁 ≤ c_learn", "G_t+1 drafted"], [5, "✍ accept · reject", "each rule + effect", "G_t+1 kept"]]
  corpus: "earlier gold rechecked"
  guideline: "G_t+1 drafted"
- cells: [[2, "measure · close", "pools · G_t+1 · 👁 0", "G_t ← G_t+1"], [5, "✍ Stop?", "error · weak", "go on · stop"]]
  corpus: "border pools shrink"
  guideline: "G_t ← G_t+1"
  loop: "another round: t ← t+1"
  span: "round t"
- step: "✍️ Stage 4 · Handoff"
  screens: "⑩ ⑪"
  cells: [[2, "freeze(G_t, D)", "last G_t · gold · 👁 0", "G* · D*"], [5, "✍ Sign (G*)", "G* · D*", "Handoff"]]
  corpus: "gold D* · 🔒 S unseen"
  guideline: "G* = last G_t"
- cells: [[4, "🔍 lm_labeler(X, G*)", "the best engine on 🔒 S", "all of X labeled"]]
  corpus: "🔒 S opened once"
  guideline: "G*, frozen"
algorithm:
  frame: "Ⓐ The method, as a paper writes it"
  caption: "Algorithm 1: Building one label with one human authority"
  input: "Input: items X (n); groups C; sealed m; talk r; round size b; labeling agent a; small models E"
  output: "Output: guideline G*, gold labels D*, signed"
  lines:
  - ["S ← SealedDraw(X, m, C)", "held back first, never shown"]
  - ["G_0 ← ∅;  R ← Register(7 cells, open);  D ← ∅", ""]
  - ["N ← ∅;  repeat N ← N ∪ Talk(X \\ S, N)", "a pass: ask, read, notes; ≤ r items"]
  - ["until HumanSign(Definition(N)) gives G_1", "gate: definition (G0)"]
  - ["U ← DevSample(X \\ (S ∪ N), C)", "U: the development sample"]
  - ["t ← 1", ""]
  - ["repeat", ""]
  - ["    A_t ← { a(x, G_t) : x ∈ U }", "the labeling agent labels every item"]
  - ["    P_t ← { e(x) : e ∈ E, x ∈ U }, sealed", "so does the small model, sealed"]
  - ["    T_t ← Pool(A_t, P_t, V, D)", "H · L · N · HL · LN · HN · HLN; V flags 🧭"]
  - ["    pick_t ← HumanApprove(Funnel(T_t, D, X \\ S))", "gate: approve; seed, retrieve, score, read"]
  - ["    D ← D ∪ Human(pick_t, A_t, P_t)", "gate: rule each one"]
  - ["    U ← U ∪ pick_t", "picks from the whole corpus join U"]
  - ["    G_{t+1} ← HumanRule(Propose(D, G_t))", "gate: rule"]
  - ["    R ← Measure(T_t, D, R);  t ← t + 1", "count the pools; open · covered · risky"]
  - ["until HumanStop(R)", "gate: stop, each pool's error mass < ε"]
  - ["return HumanSign(Freeze(G_t, D))", "gate: freeze → scanning"]
  notation: ["Notation", "X  the items (n);  U  the development sample (u)", "S  the sealed set (m): the final exam", "N  items read in the talk (≤ r)", "D  your gold labels", "G_t  the guideline after round t", "R  the register: 7 pools;  T_t  each item's pool", "a, A_t  the labeling agent, its labels", "E, P_t  the small model, its sealed labels", "V  the items' map (embeddings)", "c_•  the agent's reading budget in a step", "v(x)  an item's value;  ε  the stop threshold"]
  sections: ["§3 Method", "3.1 Sealed reservation  (line 1)", "3.2 Initial labeling definition  (lines 3-5)", "3.3 Calibration rounds  (lines 7-16)", "3.4 Picking from the whole corpus  (lines 11, 13)", "3.5 Freeze and handoff  (line 17)"]
corpus:
  frame: "Ⓑ The corpus, along the way: each step, its input, process, output"
  total: 350
  sub: "the 350 items at each step: what is sealed, read, labeled, still in the pool"
  parts:
    sealed: ["🔒", "sealed: the final exam"]
    read: ["💬", "read in the talk"]
    gold: ["🏷", "your gold"]
    H: ["H", "settled high"]
    L: ["L", "settled low"]
    N: ["N", "settled none"]
    HL: ["HL", "degree border"]
    LN: ["LN", "presence border"]
    HN: ["HN", "clash"]
    HLN: ["HLN", "unmapped"]
    pool: ["", "not yet labeled"]
    scan: ["🧪", "small model's labels under G*"]
  rows:
  - [["1 · Contract"], [sealed, 50], [pool, 300]]
  - [["2 · Initial Labeling Definition"], [sealed, 50], [read, 30], [pool, 270]]
  - [["3 · Round 1"], [sealed, 50], [read, 30], [gold, 6], [agreed, 14], [pool, 250]]
  - [["   Round 2"], [sealed, 50], [read, 30], [gold, 18], [agreed, 42], [pool, 210]]
  - [["   Round t: Stop"], [sealed, 50], [read, 30], [gold, 30], [agreed, 70], [pool, 170]]
  - [["4 · Handoff"], [sealed, 50], [read, 30], [gold, 30], [agreed, 70], [pool, 170]]
  - [["🔍 scanning"], [sealed, 50], [scan, 300]]
  notes:
  - "the sealed 50 are the final exam: untouched until scanning tests the models against your blind labels"
  - "7 pools each round: H, L, N when both models give that label, sure; HL, LN, HN between two; HLN when the definition does not cover it"
  - "the map flags 🧭 an H, L or N item whose gold neighbours differ; you rule the open pools and the 🧭, and that is gold"
  table:
    columns: ["step", "👤 you do", "input", "process", "output"]
    rows:
    - ["Stage 1 · Contract", "nothing: the agent runs it", "items-v3 (350) · the map's groups", "hold back 50 as the final exam, across the groups, by a seed; start an empty guideline and the register", "🔒 50 sealed · pool 300 · guideline v0 · 7 cells open"]
    - ["Stage 2 · Initial Labeling Definition", "talk with the agent, write notes; ✍ Sign", "the pool, 300", "read up to 30 items, group by group; the agent asks, then proposes the definition and its values", "30 read, set aside · your notes · definition signed (G0) · guideline v1"]
    - ["3 · Round 1", "✍ Approve the pick; ✍ rule each disagreement; ✍ accept or reject each rule", "the pool, 270 · guideline v1", "draw 20 at random; the small model labels sealed; the labeling agent labels with v1; where they differ or it is unsure, you rule", "gold 6 · agreed 14 · guideline v2 · checkpoint"]
    - ["   Round 2", "the same", "the pool, 250 · G_1 · the register", "draw 40: 20 near an open hard region, 20 at random; the same labeling and review", "gold 18 · agreed 42 · G_2"]
    - ["   Round t: Stop", "✍ Stop", "the checkpoint · the register", "rounds go on until no hard region is open, or you accept one as a limitation", "gold 30 · agreed 70 · 170 never drawn"]
    - ["Stage 4 · Handoff", "✍ Sign", "the last checkpoint", "freeze the guideline, your gold and their lineage; nothing new is made", "handoff/label-v1.yaml: G* · gold 30"]
    - ["🔍 scanning", "❓ label the 50 blind", "the Handoff · 🔒 50 · the other 300", "the small model and the labeling agent label the 50 and are scored against you; then the small model labels the 300", "scores · 300 labels under G*"]
ledger:
  frame: "Ⓑ The corpus, Run by Run: who acts, what changes"
  sub: "each Run: the 350 items after it, who acts, what changes"
  steps: [[0, "📦 Stage 1 · Contract"], [1, "💬 Stage 2 · Initial Labeling Definition"], [3, "🔁 Stage 3 · Rounds: every item, every round, in 7 pools"], [11, "✍️ Stage 4 · Handoff"], [12, "🔍 scanning, the next Task"]]
  bars:
  - [[sealed, 50], [pool, 300]]
  - [[sealed, 50], [read, 30], [pool, 270]]
  - [[sealed, 50], [read, 30], [pool, 270]]
  - [[sealed, 50], [read, 30], [pool, 270]]
  - [[sealed, 50], [read, 30], [pool, 270]]
  - [[sealed, 50], [read, 30], [H, 60], [L, 45], [N, 70], [HL, 30], [LN, 35], [HN, 10], [HLN, 20]]
  - [[sealed, 50], [read, 30], [H, 60], [L, 45], [N, 70], [HL, 30], [LN, 35], [HN, 10], [HLN, 20]]
  - [[sealed, 50], [read, 30], [gold, 30], [H, 58], [L, 44], [N, 68], [HL, 22], [LN, 27], [HN, 6], [HLN, 15]]
  - [[sealed, 50], [read, 30], [gold, 30], [H, 58], [L, 44], [N, 68], [HL, 22], [LN, 27], [HN, 6], [HLN, 15]]
  - [[sealed, 50], [read, 30], [gold, 30], [H, 58], [L, 44], [N, 68], [HL, 22], [LN, 27], [HN, 6], [HLN, 15]]
  - [[sealed, 50], [read, 30], [gold, 60], [H, 75], [L, 55], [N, 72], [HL, 4], [LN, 3], [HN, 1]]
  - [[sealed, 50], [read, 30], [gold, 60], [H, 75], [L, 55], [N, 72], [HL, 4], [LN, 3], [HN, 1]]
  - [[sealed, 50], [scan, 300]]
  columns: ["Run", "🤖 agent", "🏷 labeling agent", "👤 you", "🧪 small model", "📚 corpus", "📜 guideline", "🏷 labels"]
  rows:
  - ["corpus-contract", "holds back 50: final exam", "—", "—", "—", "items-v3: 🔒 50 · pool 300", "v0, empty", "none"]
  - ["definition-discussion", "shows items, asks, pass by pass", "—", "reads, writes notes", "—", "30 read, out of rounds", "v0", "notes, never labels"]
  - ["G0 · definition", "proposes it", "—", "✍ Sign", "—", "—", "v1: high · low · none", "none"]
  - ["weak-prelabel", "—", "—", "—", "labels all 270, sealed", "—", "v1", "its 270, sealed"]
  - ["agent-label", "dispatches", "labels all 270 with v1, a rule each", "—", "—", "—", "v1", "the agent's 270"]
  - ["sort into pools", "places each item in a pool; the map flags 🧭", "—", "—", "revealed to the agent", "H 60 · L 45 · N 70 · HL 30 · LN 35 · HN 10 · HLN 20", "v1", "a pool per item"]
  - ["round-prepare: pick", "picks 30 by the search rules, each with its rule", "—", "✍ Approve", "—", "30 picked", "v1", "—"]
  - ["human-calibration", "shows each one", "—", "✍ rules 30; 8 corrected", "—", "—", "v1", "gold 30"]
  - ["guideline-learn", "proposes rules from the 8", "—", "✍ accept · reject", "—", "—", "v2", "—"]
  - ["round-close", "counts the pools; HL, LN open", "—", "✍ Stop?", "—", "HL 22 · LN 27 · HN 6 · HLN 15", "G_1", "gold 30 · H L N 170"]
  - ["round 2 … t", "picks the open pools", "relabels all with G_t", "✍ rules the pick", "relabels all, sealed", "HL 4 · LN 3 · HN 1 · HLN 0", "G_2 … G_t", "gold 60 · H L N 202"]
  - ["handoff-freeze", "freezes", "—", "✍ Sign (G*)", "—", "🔒 50 still unseen", "G*", "D_cal*: gold 60"]
  - ["🔍 scanning · test", "scores", "labels the 50", "❓ labels the 50, blind", "labels the 50", "🔒 50 opened once", "G*", "who matches you"]
  note: "Gold is only what you rule; H, L, N labels are kept, never gold. After a rule changes, every item is labeled again. Counts are an example."
changes:
  map:
  - {at: [1300, 132], text: "four lanes: the labeling agent labels, you review the disagreements"}
  - {under: boxes, text: "problem: a codebook before the data; C1 interactive"}
  - {lane: 0, text: "corpus lane"}
  - {at: [1300, 104], text: "each box: in above, out below"}
  - {lane: 4, text: "a panel of open models"}
  - {lane: 1, text: "guideline lane"}
  - {row: 0, dy: 132, text: "S held back: the final exam"}
  - {row: 1, dy: 140, text: "counts as symbols: n, m, r, b"}
  - {row: 2, dy: 20, text: "Stage 2 renamed"}
  - {row: 2, dy: 110, text: "talk in passes"}
  - {row: 3, dy: 110, text: "dev sample only; Ⓔ"}
  - {row: 7, dy: 60, text: "loop carries G_t+1"}
  - {row: 4, dy: 20, text: "all labeled, sorted: 7 pools"}
  - {row: 4, dy: 60, text: "renamed: pick, Approve"}
  - {row: 7, dy: 20, text: "rows: 7 steps (Ⓒ)"}
  - {row: 9, dy: 110, text: "Sign (G*): what it signs"}
  - {row: 5, dy: 20, text: "👁 reading budgets"}
  - {row: 5, dy: 60, text: "PICK: a funnel over X∖S (Ⓔ)"}
  - {at: [2000, 104], text: "each agent box: the call it makes"}
  - {row: 6, dy: 110, text: "shown on the 3-D map"}
  - {row: 8, dy: 120, text: "one box: one round"}
  algorithm: "lines 3-4: talk in passes · line 11: the pick funnel over X∖S · line 16: stop by error mass"
  corpus: "the sealed 50 named the final exam · Ⓑ and Ⓓ in one: each step's bar beside what you do, its input, process, output"
  round: "Ⓒ and Ⓓ in one: the round's loop, then the Task as a tree"
  levels: "named: Stage 1-4, Step 1-7"
  gformat: "new: the guideline format and the seven pools named"
  reader: "find_neighbours(seed, k, corpus, rank_by): one tool, five ways to rank · built: engine/corpus_tools.py (nearest works today)"
  versions: "new: four design versions, linked as the corpus grows"
  ledger: "every item in one of 7 pools each round: H L N grow, HL LN HN HLN shrink · Ⓑ and Ⓒ in one"
round:
  frame: "Ⓒ One round, step by step, and the Task as a tree"
  sub: "Stage 3: seven Steps, the same each round; the round closes, then another round or Stop"
  steps:
  - ["Step 1 · LABEL", "every item of the development sample gets a label from both models, under G_t", "🏷 labeling agent · 🧪 small model, sealed", "labels/agent.jsonl · prelabels/small.jsonl"]
  - ["Step 2 · SORT", "each item goes into one of the 7 pools; the map flags 🧭", "🤖 agent", "pools.jsonl"]
  - ["Step 3 · PICK", "choose by the six search rules, each item naming its rule; write what we expect first", "🤖 proposes · ✍ you Approve", "card.md · human_batch.jsonl · prospect.md"]
  - ["Step 4 · JUDGE", "rule each picked item: its label and its region; this is gold", "✍ you, in the chat", "sessions/events.jsonl · human_final.jsonl"]
  - ["Step 5 · LEARN", "turn your corrections into rule changes, each with its effect on earlier gold", "🤖 proposes · ✍ you accept · reject · narrow", "policy_draft/"]
  - ["Step 6 · MEASURE", "count the pools; how often you, the labeling agent and the small model agree", "🤖 agent", "metrics.json · coverage.json"]
  - ["Step 7 · CLOSE", "check the round, promote the gold and G_t+1, settle the register", "🔐 keeper · ✍ you: Stop?", "checkpoint.json"]
  loop: "another round: LABEL again, with G_t+1"
  stop: "✍ Stop: no pool open → Stage 4 · Handoff"
  from: "the law's CARD · PREPARE · PRELABEL · JUDGE · LEARN · MEASURE · CLOSE, with every item labeled and sorted first"
tree:
  frame: "The building Task as a tree: Stages and Steps"
  sub: "Task → Stage → round → Step → Run: each with its purpose, who acts, and what it leaves"
  columns: ["Stage · Step", "Purpose", "Who", "Run", "Leaves"]
  rows:
  - [0, "📦 Stage 1 · Contract", "hold back the final exam; start guideline v0 and the register; no label is made", "🤖 agent", "corpus-contract", "corpus/ · policy v0 · register.md"]
  - [0, "💬 Stage 2 · Initial Labeling Definition", "talk with the corpus in passes, then sign what the label means", "🤖 asks · 👤 notes · ✍ you Sign (G0)", "definition-discussion · guideline-seed", "notes · definition · guideline v1"]
  - [0, "🔁 Stage 3 · Rounds", "round_1, round_2, …: repeat until no pool is open", "", "", "rounds/round_t/"]
  - [1, "Step 1 · LABEL", "every item of the development sample gets a label from both models, under G_t", "🏷 labeling agent · 🧪 small model, sealed", "agent-label · weak-prelabel", "labels/agent.jsonl · prelabels/small.jsonl"]
  - [1, "Step 2 · SORT", "each item goes into one of the 7 pools; the map flags 🧭", "🤖 agent", "pool-sort (new)", "pools.jsonl"]
  - [1, "Step 3 · PICK", "choose by the six search rules, each item naming its rule; write what we expect first", "🤖 proposes · ✍ you Approve", "round-prepare", "card.md · human_batch.jsonl · prospect.md"]
  - [1, "Step 4 · JUDGE", "rule each picked item: its label and its region; this is gold", "✍ you, in the chat", "human-calibration", "sessions/events.jsonl · human_final.jsonl"]
  - [1, "Step 5 · LEARN", "turn your corrections into rule changes, each with its effect on earlier gold", "🤖 proposes · ✍ you accept · reject · narrow", "guideline-learn", "policy_draft/"]
  - [1, "Step 6 · MEASURE", "count the pools; how often you, the labeling agent and the small model agree", "🤖 agent", "round-measure", "metrics.json · coverage.json"]
  - [2, "Step 7 · CLOSE", "check the round, promote the gold and the next guideline, settle the register; another round or Stop", "🔐 keeper · ✍ you: Stop?", "round-close", "checkpoint.json"]
  - [0, "✍️ Stage 4 · Handoff", "freeze the guideline, your gold and their lineage; nothing new is made", "🤖 freezes · ✍ you Sign (G*)", "handoff-freeze", "handoff/label-v1.yaml → 🔍 scanning"]
reader:
  frame: "Ⓔ How the agent reads the corpus"
  sub: "the agent never holds the list: it calls tools over the frozen items and the map"
  tools_title: "🔧 The corpus tools"
  tools_columns: ["tool", "returns", "used for"]
  tools:
  - ["stats(filter)", "counts; the map's groups, their top words and typical items", "the overview"]
  - ["sample(group, n, seed)", "random items from one group", "an unbiased look, group by group"]
  - ["search(query)", "items by meaning (the map) and by keyword", "the hard cases you named"]
  - ["find_neighbours(seed, k, corpus, rank_by)", "k new items from corpus near a seed set (a pool, your corrections), ranked", "the funnel: from a pool to the next items to review"]
  - ["lm_labeler(items, guideline, engine)", "each item's label, region, confidence, reason; sealed", "LABEL: the agent and each model in E"]
  - ["contrast(item)", "near items the panel labels differently", "pairs: which is worse?"]
  - ["get(item)", "one item's full text", "reading it"]
  rules_title: "📏 The seeds: where a round searches"
  rules_columns: ["#", "rule", "finds"]
  rules:
  - ["1", "random audit of H · L · N", "shared mistakes; each pool's error rate"]
  - ["2", "open border pools", "degree · presence · clash · unmapped, and neighbours"]
  - ["3", "neighbours of your corrections", "more of what the guideline just got wrong"]
  - ["4", "queries from the definition", "the hard cases you named in the talk"]
  - ["5", "🧭 odd on the map", "H, L, N items whose nearest gold says otherwise"]
  - ["6", "diversity", "at most one per near-duplicate cluster"]
  - ["—", "never", "the final exam, or items read in the talk"]
  funnel_title: "🔻 The pick funnel: from n items to b, the agent reading at most c_pick"
  funnel:
  - ["① seed", "the six rules say where to look", "👁 0", "seeds"]
  - ["② retrieve", "find_neighbours(pool, 10·c_pick, X∖S, nearest)", "👁 0", "~10·c_pick ids"]
  - ["③ rank", "the panel labels each; ranked by rank_by below", "👁 0", "a ranked list"]
  - ["④ read, pick", "the agent reads the top c_pick; b picks, one per cluster", "👁 ≤ c_pick", "card · ✍ Approve"]
  methods_title: "🧭 rank_by: how find_neighbours orders what it finds"
  methods_columns: ["rank_by", "ranks first", "needs"]
  methods:
  - ["nearest", "the closest to the set", "the map only"]
  - ["confidence", "the panel's least confident", "the panel's labels"]
  - ["disagree", "where the panel splits most", "the panel's labels"]
  - ["classifier", "a simple model trained on your gold: its most unsure", "gold; never makes gold"]
  - ["value", "the highest v(x), below", "all of the above"]
  value_title: "⚖️ The score: v(x) = unsure(x) · dense(x)^β · new(x) · (1 + γ · near(x))"
  value_columns: ["factor", "measured as", "why it counts"]
  value:
  - ["unsure(x)", "1 − agreement of the labelers' regions, with the panel's entropy", "your ruling settles something open"]
  - ["dense(x)", "how many items of X sit near x, scaled 0-1", "one ruling carries over to many"]
  - ["new(x)", "distance to the nearest gold, scaled 0-1", "ground no rule has seen"]
  - ["near(x)", "1 if a rule changed last round covers it", "tests that G_t+1 fixed it"]
  split: "Across pools, b is split by expected error mass: a pool's size in X (estimated from U) × its error rate in past audits; within a pool, the highest v(x) first. Stop when every pool's error mass is under ε."
  guards: "Two guards live in the tools, not in the agent: the final exam is not in the index, so no tool returns it; every item shown to anyone is logged, so we know what a person has seen; and each step has a reading budget (c_ask, c_pick, c_learn): past it, a tool returns ids, counts and labels, never text."
  scale: "At scale the rounds run on a development sample U of 2-5k items across the map's groups; the panel labels U every round; all of X is labeled only in scanning. DICES: U is the whole pool."
gformat:
  frame: "Ⓖ The guideline: what each G_t holds"
  sub: "one source of rule cards, rendered for two readers; only your rulings change it"
  source: "📐 rules.yaml + classes + borders"
  source_note: "the source: changed only by your rulings"
  readers:
  - ["📖 guideline.md", "for you: every rule with its evidence and history"]
  - ["🤖 cheatsheet.md", "for the labelers: short, in order; their prompt"]
  sections_title: "The seven sections"
  sections:
  - ["§1", "Question and scope", "the question; what is judged, what is context"]
  - ["§2", "Classes", "per value: definition · includes · excludes · 2 anchors"]
  - ["§3", "Rules", "R1 … Rk in order of precedence: rule cards"]
  - ["§4", "Borders", "per border pool: what is hard, its rules"]
  - ["§5", "Procedure", "context → rules in order → class → region"]
  - ["§6", "Uncertainty", "what to do when unsure; none never means unsure"]
  - ["§7", "Changes", "G_t−1 → G_t: each rule added, narrowed, dropped"]
  card_title: "One rule card"
  card: ["- id: R4", "  if:   \"<a condition on one item>\"", "  then: low", "  border: LN", "  precedence: 2", "  evidence: [<gold ids>]", "  since: G_2", "  why: \"<your reason, your words>\"", "  status: active"]
  laws: ["only your rulings activate a rule", "every rule has gold behind it", "each rule keeps its regression items", "never deleted: narrowed or dropped"]
  pools_title: "The seven pools, named"
  pools_columns: ["pool", "name", "means", "the guideline needs"]
  pools:
  - ["H · L · N", "Settled high · low · none", "every reader agrees", "a random audit: shared mistakes hide here"]
  - ["HL", "Degree border", "present; how much is unclear", "a severity rule"]
  - ["LN", "Presence border", "present at all?", "a threshold rule"]
  - ["HN", "Clash", "opposite readings of the concept", "the meaning clarified: the most valuable"]
  - ["HLN", "Unmapped", "anything plausible; no rule yet", "a new rule"]
versions:
  frame: "Ⓕ Design versions: reading the corpus as it grows"
  sub: "four ways to run the rounds; the corpus grows from left to right; one is proposed, the others kept to compare"
  arrow: "bigger corpus"
  items:
  - name: "V1 · Label everything"
    how: "both models label every item, every round"
    cost: "items × rounds calls; fine below ~1k items"
    fits: "DICES-350"
    risk: "cost grows with the corpus"
  - name: "V2 · Development sample + search rules"
    how: "a fixed sample of 2-5k across the map's groups is labeled every round; picks by the six rules"
    cost: "sample × rounds; the corpus once, in scanning"
    fits: "10k to 1M items"
    risk: "a kind of item missing from the sample stays unseen"
    proposed: true
  - name: "V3 · Growing sample"
    how: "V2, but each round adds items the search rules find near open pools and 🧭"
    cost: "a little more than V2"
    fits: "rare harms, long tails"
    risk: "the sample drifts toward the hard cases; counts need weights"
  - name: "V4 · Search only"
    how: "nothing is labeled ahead; each round the rules retrieve ~200 candidates, and only those are labeled"
    cost: "lowest: candidates × rounds"
    fits: "very large or streaming corpora"
    risk: "pools are estimates; a border no rule looks for is never found"
  note: "Proposed: V2, with V1 for a corpus this small (DICES runs V1 and V2 alike) and V3 when a pool keeps coming back open. A version is chosen in the Contract and written there."
screen:
  task: "Task · t03 · building"
  line: "Labeling · Block b01 · Task t03 · <label> on <dataset>"
  tabs: ["1 · Contract", "2 · Initial Labeling Definition", "3 · Rounds", "4 · Handoff"]
tabs:
- act: "Act 2 · Work › Stage 1 · Contract"
  step_arrow: "Stage 1"
  key: "First, before anyone reads an item: the items come in, the final exam S (m) is held back, the guideline G_0 and the register start empty. No label is made; the agent reads no item (👁 0)."
  states:
  - title: "② Work › 1 · Contract · 1 of 2: hold back first"
    changed: "sizes as symbols: n, m; 👁 0"
    tab: "1 · Contract"
    step: "📦 Stage 1 · Contract"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Items: "X · items-v3 · n items", Groups: "C · from the items Task's map", Final exam: "S · m sealed, across C, seed <s>", Agent reads: "👁 0: ids and counts"}
    prompt: "/haipipe-labeling-building <task> contract: import the items, hold back the sealed set, start guideline v0."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the agent runs it"
  - title: "③ Work › 1 · Contract · 2 of 2: what is held back"
    tab: "1 · Contract"
    step: "📦 Stage 1 · Contract"
    chip: "✓ done"
    folded: ""
    sections:
    - {t: "📚 Corpus: 🔒 S (m) · pool X∖S"}
    - {t: "📜 Guideline G_0: empty"}
    - {t: "🗂 Register: 7 pools, all open"}
    mark: "the Contract Run writes these; it makes no label"
- act: "Act 3 · Work › Stage 2 · Initial Labeling Definition"
  step_arrow: "Stage 2"
  key: "Talk with the corpus in passes: each pass the agent asks (👁 ≤ c_ask), you read a few items and write notes, it drafts the definition; another pass, or Sign (G0). At most r items read in all."
  states:
  - title: "④ Work › 2 · Initial Labeling Definition · 1 of 2: talk, pass by pass"
    changed: "talk in passes; r and c_ask"
    tab: "2 · Initial Labeling Definition"
    step: "💬 Stage 2 · pass k"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Pool: "X∖S, the final exam out", You read: "≤ r in all passes; N so far", Agent reads: "👁 ≤ c_ask a pass", Rounds: "never draw N again"}
    - title: "Pass k"
      rows: {Asked: "<the agent's questions>", Shown: "<the items, by group>", Notes: "<your notes>"}
    prompt: "/haipipe-labeling-building <task> definition: one more pass with me through the items, group by group; keep my notes."
    mark: "copy it, talk in Claude or Codex"
    arrow: "the agent drafts"
  - title: "⑤ Work › 2 · Initial Labeling Definition · 2 of 2: Sign (G0), or another pass"
    changed: "another pass, or Sign"
    tab: "2 · Initial Labeling Definition"
    step: "💬 Stage 2 · draft after pass k"
    chip: "✍ sign"
    boxes:
    - title: "Definition · the draft"
      dashed: true
      button: "Sign · Another pass"
      mark: "you read it, then sign or talk again"
      rows: {Label: "how unsafe is the AI's last reply?", Values: "high · low · none", Low: "<what low means here>", None: "no harm in it; never 'unsure'", From: "k passes · N items read"}
    prompt: "/haipipe-labeling-building <task> definition: write the definition from our talk, and stop for my Sign."
    sections:
    - {t: "💬 The talk, pass by pass"}
    - {t: "📝 Your notes and hard cases"}
    - {t: "📜 Guideline G_1 = v1"}
    mark: "after Sign: the step folds ✓, these cards stay"
- act: "Act 4 · Work › Stage 3 · Rounds"
  step_arrow: "Stage 3"
  key: "A round: both labelers label U with G_t; SORT puts each item in one of 7 pools; you approve the pick (b); you rule each pick, which is gold; you rule each rule; CLOSE makes G_t ← G_t+1, then another round or Stop."
  states:
  - title: "⑥ Work › 3 · Rounds · 1 of 4: approve the pick"
    changed: "the pick funnel: seed, score, read"
    tab: "3 · Rounds"
    step: "🔁 Round t · PICK"
    chip: "✍ approve"
    boxes:
    - title: "Now"
      rows: {Corpus: "U (u): 2 labels each · gold so far", Pools: "H · L · N · HL · LN · HN · HLN, a count each", Guideline: "G_t"}
    - title: "This round's pick · round_t"
      dashed: true
      button: "Approve"
      mark: "you read it and approve"
      rows: {Pick: "b items, one per cluster, from all of X∖S", Split: "by error mass: HL <b_1> · LN <b_2> · … · audit <b_7>", Each item: "its seed (rule 1-6) · its v(x)", Funnel: "~10·c_pick retrieved → scored → c_pick read → b", We expect: "<written before item 1>"}
    prompt: "/haipipe-labeling-building <task> round: label U with G_t, sort it into the 7 pools, and pick round t."
    mark: "🧭: settled, but its neighbours' gold disagrees"
    arrow: "the session opens"
  - title: "⑦ Work › 3 · Rounds · 2 of 4: rule each pick"
    changed: "both labelers give label + region; the item on the 3-D map"
    tab: "3 · Rounds"
    step: "🔁 Round t · JUDGE · item i of b · pool HL"
    chip: "→ review"
    boxes:
    - title: "Item · <item id>"
      rows: {Before: "Person: … AI: … Person: …", Judged: "<the AI's last reply>"}
    - title: "🏷 Labeling agent · G_t"
      rows: {Label: "low · region LN", Why: "rule 3: <the rule it used>"}
    - title: "🧪 Open models E, sealed till now"
      rows: {<model 1>: "none · region N", <model 2>: "low · region LN", <model 3>: "none · region N"}
    - title: "📍 Where it sits · the 3-D map"
      dashed: true
      rows: {This item: "the dot ringed, pool HL", Neighbours: "its <k> nearest, coloured by your gold", Group: "<the group it is in>", Turn it: "drag to rotate; hover a dot for its text"}
    - title: "👤 Your ruling"
      dashed: true
      button: "Save"
      mark: "you rule it"
      rows: {Label: "high · low · none", Region: "H · L · N or between: HL · LN · HN · HLN", Why: "<one line>"}
    prompt: "/haipipe-labeling-building <task> round: show me round t's pick, one item at a time."
    mark: "only the b picked come to you; each ruling is gold"
    arrow: "the agent learns"
  - title: "⑧ Work › 3 · Rounds · 3 of 4: rule each change, G_t+1"
    changed: "👁 c_learn; the patch drafts G_t+1"
    tab: "3 · Rounds"
    step: "🔁 Round t · LEARN"
    chip: "✍ rule"
    boxes:
    - title: "Patch · rule 4 · into G_t+1"
      dashed: true
      button: "Accept · Reject · Narrow"
      mark: "you rule it"
      rows: {Says: "<the new or changed rule>", Why: "items <a>, <b> disagreed", Changes: "<k> earlier gold labels", Agent read: "👁 ≤ c_learn"}
    prompt: "/haipipe-labeling-building <task> round: propose rule patches from round t, with what each changes."
    mark: "one ruling per patch"
    arrow: "the round closes"
  - title: "⑨ Work › 3 · Rounds · 4 of 4: CLOSE, G_t ← G_t+1"
    changed: "the guideline moves on here"
    tab: "3 · Rounds"
    step: "🔁 Round t · MEASURE · CLOSE"
    chip: "✓ done"
    folded: ""
    sections:
    - {t: "📊 The 7 pools, round by round"}
    - {t: "🏷 Your gold: + b"}
    - {t: "📜 Guideline: G_t ← G_t+1"}
    - {t: "🤝 Each model vs you, round by round"}
    - {t: "🗂 Register: each pool open · covered · risky"}
    - {t: "⏭ Another round (t ← t+1), or Stop", button: "Stop"}
    mark: "Stop: no pool open, or you accept one as a limitation"
- act: "Act 5 · Work › Stage 4 · Handoff"
  step_arrow: "Stage 4"
  key: "Nothing new is made: G* = the last G_t and your gold D* are frozen with their lineage and signed; scanning reads only this. S (m) is still unseen."
  states:
  - title: "⑩ Work › 4 · Handoff · 1 of 2: Sign (G*)"
    tab: "4 · Handoff"
    step: "✍️ Stage 4 · Handoff"
    chip: "✍ sign"
    boxes:
    - title: "Input"
      rows: {Checkpoint: "round t, Stop signed", Agent reads: "👁 0"}
    - title: "Handoff · handoff/label-v1.yaml"
      dashed: true
      button: "Sign (G*)"
      mark: "you sign it"
      rows: {Guideline: "G* = G_t", Gold: "D* · your rulings", Lineage: "G_0 → G_1 → … → G_t, t rounds", Final exam: "S (m), still unseen"}
    prompt: "/haipipe-labeling-building <task> freeze: freeze the Handoff from the last checkpoint, and stop for my Sign."
    mark: "copy it, run it in Claude or Codex"
    arrow: "you sign"
  - title: "⑪ Work › 4 · Handoff · 2 of 2: signed"
    tab: "4 · Handoff"
    step: "✍️ Stage 4 · Handoff"
    chip: "✓ signed"
    folded: ""
    sections:
    - {t: "✍️ Handoff, signed"}
    - {t: "📜 Guideline G*"}
    - {t: "🏷 Your gold, D*"}
    - {t: "🔍 Next: scanning, S opened once"}
    mark: "Report shows these Result cards only, as in s41"
```


1 · The levels: Task → Stage → round → Step → Run
-------------------------------------------------

```text
🏗 building Task (t03_dices350_response_safety_labeling)
├── Stage 1 · Contract                       Run: corpus-contract           50 held back: the final exam
├── Stage 2 · Initial Labeling Definition    Runs: definition-discussion · guideline-seed      ✍ Sign (G0)
├── Stage 3 · Rounds                         round_1, round_2, … until ✍ Stop
│   └── round_t
│       ├── Step 1 · LABEL     Runs: agent-label · weak-prelabel   every item, both models
│       ├── Step 2 · SORT      Run: pool-sort (new)                 7 pools; the map flags 🧭
│       ├── Step 3 · PICK      Run: round-prepare                   ✍ Approve
│       ├── Step 4 · JUDGE     Run: human-calibration               ✍ your rulings: gold
│       ├── Step 5 · LEARN     Run: guideline-learn                 ✍ accept · reject · narrow
│       ├── Step 6 · MEASURE   Run: round-measure                   count the pools
│       └── Step 7 · CLOSE     Run: round-close                     ✍ Stop? → another round
└── Stage 4 · Handoff                        Run: handoff-freeze            ✍ Sign (G*) → 🔍 scanning
```

A Stage is one tab. Stage 3 repeats in rounds; a round is a folder, `rounds/round_<t>/`, not a Run. Each Step is
one Run (LABEL two), named on disk `run-labeling-<operation>-<MMDD>-<target>`.


2 · The Stages, in the law's order
----------------------------------

| tab | the engine's Run Types (ref/step-order.md) | the person's gate |
|---|---|---|
| 1 · Contract | corpus-contract (the reservation inside it) · embedding-build* (done in the items Task) | none: no label is made |
| 2 · Meaning | discovery-search* · definition-discussion · G0 Confirm meaning · guideline-seed* | meaning (Sign) |
| 3 · Rounds | round-prepare · weak-prelabel* · human-calibration · guideline-learn · round-measure · round-close | release · item (first, final) · rule · stop |
| 4 · Handoff | handoff-freeze | freeze (Sign G*) |

A round folder `rounds/round_<t>/` is an episode, not a Run; its Runs are the six above.


Decided
-------

s42-D01 · Talking with the corpus is part of building, before its meaning is signed, not a Task type of its own
    (261014; JL asked "how do you think?"): the meaning needs what the person learned, and the law already has it
    (definition-discussion and discovery-search, then the G0 gate).
s42-D02 · The law's order (ref/step-order.md; the reviewer, 261014): 1 Contract (import, the sealed set held back,
    guideline v0, the register) before anyone reads an item; 2 Meaning (talk, then Sign at G0); 3 Rounds; 4 Handoff.
s42-D03 · Explore's notes are never labels and never gold: P0 makes no label, and gold comes only from a person's
    judgment in a closed round. The up to 30 items read in the talk are never drawn into a round, so a small model's
    seal always comes before the person's first sight (Law 2). (261014, the agent's call: the law decides it.)
s42-D04 · The values are the engine's high · low · none (ordinal, how unsafe the reply is); none means no harm in it,
    never unsure; unsure is a note beside a label. The Meaning step writes what low means for DICES. (261014)
s42-D05 · (superseded by D12: the labeling agent labels, the person reviews) The person labels in the chat with the agent (the moderator is the only one who talks with the person);
    the Rounds tab shows the session live, read-only, item by item: first label, lock, the small models revealed,
    final. (261014)
s42-D06 · 50 of the 350 are held back, drawn across the items Task's groups with a seed; a round draws 20 (the
    engine's default) per arm; round 1 one arm at random, later rounds two, near a register cell and at random. Items glanced at
    in the items Task (Draw again, the map) may be in the sealed set: accepted and written in the Contract as a
    limitation, since nothing records what was seen there (s41's Open 1). (261014)
s42-D09 · ① says the problem and the novelty above the map, each novelty marked ✨1-✨4 where it happens (JL 261014:
    "what is the novelty? what is the problem we want to solve here?"; "add more here ... I want all the things
    here"). The claims are the agent's reading, not yet checked against related work (Open 3).
s42-D10 · The small models are named: Haiku 4.5 (claude-haiku-4-5-20251001) leads the committee, beside one open small
    model so the results can be reproduced; each labels alone and sealed, and their agreement is never gold (JL 261014:
    "could we call it haiku 5.5?"; there is no Haiku 5.5, the newest small Claude is Haiku 4.5).
s42-D11 · Ⓑ follows the corpus, not the steps (JL 261014: "another frame to show ... the data side ... the corpus ...
    selected and chosen and labeled ... in the perspective of the corpus"): one bar of the 350 items per step, split
    into sealed · read in the talk · your gold · not yet chosen, and at the end what scanning labels.
s42-D12 · The labeling agent labels the items, not the person (JL 261014: "I don't want a human to do the labeling.
    I want the agent has a subagent to do it ... with this guideline"; chosen: "Review disagreements"). Each round
    Haiku 4.5 labels sealed, the labeling agent labels with the current guideline and names the rule it used, and the
    person reviews only where the two disagree or the labeling agent is unsure. Gold is what the person confirms or
    corrects; agreed labels are kept, never gold. This changes haipipe-labeling-building's law (the person no longer
    makes every judgment): the law and its engine still need the change (Open 4).
s42-D13 · The labeling agent is a strong model (Sonnet 5 or Opus 5.5) given the guideline; Haiku 4.5 is the cheap model that
    should come to match it, and scanning runs Haiku on the corpus (chosen: "Strong labels, Haiku learns").
s42-D15 · The labeling sub-agent is called the labeling agent (JL 261014: "could you call it labeling agent?").
s42-D16 · Ⓓ, under Ⓑ's bars, explains each step: what you do, its input, its process, its output (JL 261014: "could you
    explain each step, what to do, input, process, and output?").
s42-D17 · Step 2 is called Initial Labeling Definition, not Meaning (JL 261014: "could we change this to the Initial
    Labeling Definition"); it matches the law's Labeling › Definition view and its G0 gate.
s42-D18 · Ⓓ joins Ⓑ: one row per step, its corpus bar beside what you do, its input, process and output (JL 261014:
    "what I mean is B and D into one").
s42-D19 · The 50 held back are called the final exam wherever they show (JL 261014: "could you add that (like final
    testing, final exam)"): they test, once building is over, whether a model with the frozen guideline matches the
    person on items nobody has seen.
s42-D20 · Ⓑ and Ⓒ are one table (JL 261014: "these two can be merged together as well"): one row per Run, grouped
    under its step, with the corpus bar after it, then the agent, the labeling agent, you, Haiku, the corpus, the
    guideline and the labels. "You do" is the you column; "process" is the acting columns; "input → output" is the
    corpus, guideline and labels from one row to the next. The step table (D16, D18) is folded into it.
s42-D21 · Plain words for the round card (JL 261014: "a card and a forecast is very hard to understand ... we are
    trying to collect the examples from the dataset, right?"): the card is "pick this round's items", the forecast
    "what we expect", and Release is "Approve". The law keeps its own words (card, prospect, release).
s42-D22 · Every item takes part in every round (JL 261014: "the whole corpus, all the items, interact with it ... we
    got these types of items ... based on the items we just cycle around"; chosen: "Every item in the pool"): each
    round the labeling agent and Haiku label all 270 with the current guideline, each item gets a type (✅ settled:
    both agree, sure · 🤔 unsure · ⚖️ disagree), the pick comes from 🤔 and ⚖️ plus a few ✅ to check, your rulings
    are gold, your corrections drive the rules, and after a rule changes every item is labeled again. Stop when few
    🤔 ⚖️ are left and no hard region is open. Ⓑ counts the types round by round.
s42-D23 · The cheap model is a small open model, not Haiku 4.5 (JL 261014: "this could be even weaker model ... that we
    can scale up for large amount of data"): an open model of about 30B (the Qwen3 or Gemma family; the exact one is
    chosen when built) runs on our own hardware over any amount of data, can be fine-tuned on the gold, and lets a
    reader reproduce the results. It labels every item each round, sealed, and labels the corpus in scanning.
    Supersedes D10's Haiku 4.5.
s42-D24 · The sort uses both (JL 261014: "how do we do the sort here? using the embeddings method or what? maybe we can
    do it in both way?"): the two models' labels give the type (✅ same label, both sure · 🤔 same, not sure · ⚖️
    different); the items Task's map flags 🧭 a ✅ whose nearest gold neighbours carry another label, or that sits in a
    group with no gold yet. The pick takes 🤔 ⚖️ and the 🧭, spread across the map's groups. The map only picks; it
    never sets a label.
s42-D25 · The pools are the register's seven regions (JL 261014: "we have several types of the pools ... H, L, None, H-L,
    H-None, L-None, L-H-N, I think we have the definition as before"; the Guide's "By in-between regions"): each
    round every item lands in H, L or N when both models give that label and are sure, in HL, LN or HN when it sits
    between two labels, in HLN when the definition does not cover it. The register keeps each pool open, covered or
    risky; a round picks from the open pools and the map's 🧭; you give each ruled item its label and its region;
    Stop when no pool is open, or one is accepted as a limitation. Supersedes D22's ✅ 🤔 ⚖️ types and D24's sort.
s42-D26 · One round is seven steps, each with its purpose, who acts and what it leaves: LABEL · SORT · PICK · JUDGE ·
    LEARN · MEASURE · CLOSE, drawn as a loop in Ⓒ and named on the map's rows (JL 261014: "for each round, we can
    separate them into different steps, and each step with the purpose ... I remember I discussed about this";
    "I think it is correct, please go ahead"). They are the law's CARD · PREPARE · PRELABEL · JUDGE · LEARN ·
    MEASURE · CLOSE (haipipe-labeling-building ref/step-order.md; haipipe-labeling-rounds), with every item labeled
    and sorted first and PREPARE folded into PICK.
s42-D27 · The frames read ① then Ⓑ then Ⓐ, left to right, as the person arranged them (JL 261014: "I would like to
    have this arrange"); Ⓒ, the round, sits under Ⓐ, clear of the screens.
s42-D28 · The levels are named Task → Stage → round → Step → Run (JL 261014: "how do we call this, also the step? what
    is the tree like description for it"; "make things like this ... as a new frame"): the building Task has four
    Stages (its tabs); Stage 3 repeats in rounds, each a folder, not a Run; a round has seven Steps; each Step is one
    Run, LABEL two. Ⓓ draws it as one table, a tree by indent: purpose, who, Run, what it leaves. pool-sort is a new
    Run type, beside agent-label (Open 4).
s42-D29 · Every frame names its levels the same way (JL 261014: "add them into the sNN"): "Stage 1 · Contract" to
    "Stage 4 · Handoff" on the map, Ⓑ, the screens and the acts; "Step 1 · LABEL" to "Step 7 · CLOSE" in Ⓒ and Ⓓ.
    The face's § 1 holds the tree.
s42-D30 · The agent reads the corpus through tools, and a round picks by search rules (JL 261014: "if we have the very
    large corpus, it is impossible to put all the items to ask the agent to read, so we should have some searching
    rules"; "how did the agent talk to the corpus"): stats, sample, search, neighbors, contrast, get, over the frozen
    items and the map; the final exam is not in the index, and every item shown is logged. At scale the rounds run on
    a development sample (2-5k across the map's groups), the whole corpus only in scanning; DICES's sample is its
    whole pool. A pick takes items by six rules (random across groups · open pools · neighbours of corrections ·
    queries from the definition · 🧭 · diversity), each item naming its rule. Ⓔ draws it. Step 1 · LABEL labels
    the development sample, not every item (refines D22).
s42-D31 · Design versions are drawn side by side, linked by dashed arrows (JL 261014: "we can propose different versions
    of design, you can add them to the new frame and use ---> to link"): Ⓕ shows four ways to run the rounds as the
    corpus grows: V1 label everything · V2 development sample + search rules (proposed) · V3 growing sample · V4
    search only, each with how, cost, fit and risk. The version is chosen in the Contract.
s42-D32 · Ⓒ and Ⓓ are one frame (JL 261014: "these two can be merged together"): the round's seven Steps as a loop,
    then the Task's Stages and Steps as a tree table under it.
s42-D33 · The method frames sit left of ① (JL 261014: "we can put these method things to the left"): Ⓐ, under it Ⓒ,
    under that Ⓔ - - -▶ Ⓕ, right-aligned past the act names; Ⓑ stays right of ①, the screens below ①. Updates D27.
s42-D34 · The Handoff's Sign names what it signs, "✍ Sign (G*)", as Stage 2's says "Sign (G0)" (JL 261014: "for the
    last Sign, could we say Sign(G*)"); in the map, the ledger and the tree.
s42-D35 · ① gains a fifth lane, the corpus, and every box its input above and its output below (JL 261014: "we should
    have the column for the corpus as well ... what is the input and output for each box ... before and below the
    box"). The corpus lane says what the corpus holds after each row (dashed: a state, not an actor). With the in and
    out lines ① is past a map's 200 words, so it is marked a detail frame read down (⑥ measures it). Updates D07.
s42-D36 · Stage 2 runs in passes (JL 261014: "we can have multiple rounds of asking and discussions"): the agent
    asks, you read a few items and write notes, it drafts the definition; another pass until you Sign (G0), still at
    most 30 items read. Drawn as a loop in ①, lines 3-4 of Algorithm 1, the ledger and the tree.
s42-D37 · ①'s lanes, left to right: corpus, agent, labeling agent, small open model, you (JL 261014: "put them in
    the middle and you in the right most, and the corpus to the leftmost"): the two models in the middle, the person's
    gates on the right, the corpus they all read on the left. Updates D35.
s42-D38 · LABEL's two ways in are named (JL 261014: "the left one can be a updated G* as well, is that so?"): from
    above, the first round, G_1 from Sign (G0); from the left, every later round, G_t+1 from your accepted rules. Not
    G*: G* is only the last G_t, named when you Stop and Sign the Handoff.
s42-D39 · ① shows what changes over time, beside who acts (JL 261014: "should we have G_t+1 to G_t ... show how the
    corpus and guideline and the corpus pool is changed along the time"): two state lanes on the left, 📚 corpus (sealed,
    read, U, the 7 pools, gold) and 📜 guideline (G_0 → G_1 → G_t → G_t+1 drafted → G_t ← G_t+1 at CLOSE → G*), each
    joined down by a thin arrow; the round's loop says t ← t+1. Updates D35, D37, D38.
s42-D40 · Each timeline change is the out of a box in its row (JL 261014: "will these also shown in the process box
    above and below?"): import leaves 🔒 50 · pool 300, LABEL leaves U's labels, SORT the 7 pools, JUDGE + gold, LEARN
    G_t+1 drafted, CLOSE G_t ← G_t+1, freeze G* · D*; the in lines name what the box reads (U · G_t, gold · G_t).
s42-D41 · ① and Ⓐ name sizes by symbol, not number (JL 261014: "change the number from the specific number to the
    symbol"): n = |X| the items, m = |S| the sealed final exam, r the talk's most items read, b a round's picks; DICES's
    350 · 50 · 30 stay only in Ⓑ, whose bars draw an example.
s42-D42 · In the corpus and guideline lanes, one box holds the round's rows, named "round t" (JL 261014, drawn on the
    canvas: "could we add this to indicate this is the box?"): what changes inside it changes every round.
s42-D43 · The agent has a reading budget per step (JL 261014: "agent can see at most N numbers of items ... we might
    have different types of N, please label them carefully"): c_ask a talk pass, c_pick a PICK, c_learn a LEARN; SORT,
    MEASURE, CLOSE and freeze read no text (👁 0); each labeler sees one item a call. N stays the talk's set, so the
    budgets get their own letters; ① ends with a symbols table (n m u r b c_•), Ⓐ's notation and Ⓔ's guards say it.
s42-D44 · The screens ②–⑪ follow ① (JL 261014: "update the UI based on this", screens first): sizes as symbols (n m r
    b), each step's 👁 budget, Stage 2 a pass k with Sign · Another pass, a round's screens titled by its Step (PICK,
    JUDGE, LEARN, CLOSE) with a Now card (corpus, pools, G_t), both labelers' label + region, CLOSE showing G_t ← G_t+1.
s42-D45 · JUDGE shows each picked item on the 3-D map (JL 261014: "for this show them, we can use the 3d embeddings as
    well"): the item ringed among its nearest neighbours, coloured by your gold so far, rotatable, hover for text (the
    items Task's 📍 Map, s41-D19); you see what it sits beside before you rule it.
s42-D46 · PICK is a funnel over the whole corpus (JL 261014: "how could we select the most valuable new data to review
    ... from the large corpus"; "what is the final score here?"): ① seed by the six rules (rule 1 now a random audit of
    the settled pools), ② retrieve neighbours over X∖S (👁 0), ③ score by the small model, v(x) = unsure · dense^β · new
    · (1 + γ·near) (information density, after Settles & Craven 2008), ④ the agent reads the top c_pick and picks b, one
    per cluster. b is split across pools by expected error mass; Stop when each pool's is under ε. Picks join U.
s42-D47 · The novelty box states the paper's three contributions (JL 261014: "our main contribution is ... the
    researcher can propose their subjective labeling ... second ... it is easy to use, so that's why we have the UI
    ... a user and agent talk with the corpus ... the third one is it will be quick ... guideline and labeling at the
    same time"): C1 your own subjective label (✨1), C2 easy to use (✨2), C3 quick (✨3), kept honest by ✨4.
s42-D48 · The contributions are what the person and others get (JL 261014: "a guideline like people are confident
    with and they can also give the good performance even for some like a weak LM"; "we are trying to build a very
    good benchmark and we can use it to apply to others"): C1 a guideline you are confident in, C2 a guideline that
    transfers (a weak model following G* labels like you, measured on S), C3 a benchmark anyone builds quickly
    with measured confidence. Stop also reads whether the weak model still gains. Updates D47.
s42-D49 · The work is framed as a tool for researchers to build their own benchmark (JL 261014: "this is a tool for
    the researcher to build their own benchmark"), and C3 is a benchmark that knows where it is unsure: every item
    keeps its region (H, L, N or a border), so an algorithm is scored on settled and border items apart. Updates D48.
s42-D50 · The tool ends by picking the labeler (JL 261014: "and then select the most suitable tools for them to
    generalize it"): scanning scores each candidate labeler (weak open models, the labeling agent, a classifier) on S
    under G*, and the best one labels all of X; its score on S is the confidence the labels carry. Updates D49.
s42-D51 · The problem is the codebook written before the data (JL 261014: "many sociologists ... have very subjective
    conceptions ... they want to have the reliable things ... people are doing it using their proposed guideline. But
    this is not interactive ... without seeing the real data they are not sure what ... rules they will have"): today a
    guideline is fixed first and its performance unknown; C1 is an interactive guideline, drawn out on real data.
s42-D52 · The small model is a panel, E (JL 261014: "we might need to provide a list of models, to test and run it to
    get the performance"): each open model labels U every round, sealed; MEASURE scores each against your gold, round
    by round, so you watch which model G_t teaches best; the pick of the labeler for all of X is made on S only
    (scanning), never on the gold the rounds chose. Panel agreement stays a sampling signal, never gold.
s42-D53 · One retrieval tool, neighbor_rank(items, k, corpus, method) (JL 261014: "what if we want the neighbours with
    (item_list, k) ... the item_list is a H pool, or the HL pool ... rank them with the confidences ... the simple model
    to rank them"): a set in (a pool, your corrections, the talk's hard cases), k new items out of the corpus, ordered
    by one named method: nearest, confidence, disagree, classifier (trained on your gold only), or value. The funnel's
    retrieve and rank are this one call; S is never in its corpus. Named find_neighbours(seed, k, corpus, rank_by) (JL
    261014: "why not make it to be: extract, or just find_neighbour should be okay"): plain, and says what it does.
s42-D54 · The guideline has a format and the pools have names (JL 261014: "another issue we haven't make sure is the
    guideline format"; "for the seven pool, I think we could name each of them"): one source of rule cards rendered
    for two readers (guideline.md for the person, cheatsheet.md as the labelers' prompt); seven sections; a rule card
    (if · then · border · precedence · evidence · since · why · status); pools named Settled high · low · none, Degree
    border (HL), Presence border (LN), Clash (HN), Unmapped (HLN). Written in haipipe-labeling-guideline
    ref/guideline-format.md and haipipe-labeling-building § The register; not yet drawn.
s42-D54 · Both labelers are one tool, lm_labeler(items, guideline, engine) (JL 261014: "what I see the things here
    are the labelers, right? ... a tool like lm_labeler(item_list, guideline, engine = xxx) ... the engine could be many
    things"): the labeling agent is one engine, each open model in E another; each call returns label, region,
    confidence and reason, sealed. Built on engine/label.py, which already has claude_sdk, codex and openai_api.
s42-D55 · Each agent box in ① is the call it makes (JL 261014: "for the next data extraction ... I want things like
    lm_labeler(U, G_t) ... show that in each step, how do we get the new data from the large corpus"): seal(X, m),
    get(sample(X∖S)), draft(notes), lm_labeler(U, G_t), sort_pools(A_t, P_t, 🧭), find_neighbours(pools), show(picks,
    📍), learn(D, G_t), measure · close, freeze(G_t, D), lm_labeler(X, G*); its in line names where the data comes from.
s42-D14 · Ⓒ is the ledger, Run by Run: who acts (agent, labeling agent, you, Haiku) and what changes (corpus, guideline,
    labels) (JL 261014: "columns ... the agent, subagent of labeling, the human, the small model, the corpus, the
    guideline and the labels, and each row is a Run").
s42-D08 · Ⓐ writes the same workflow as a paper's Method would (JL 261014: "if we are going to write the ACL paper
    ... how do we write the method ... a new frame to describe the workflow with the algorithm box"): Algorithm 1 in
    pseudocode, each human gate a comment beside its line, and the Method's sections mapped to its lines.
s42-D07 · ① is a workflow map, the main frame: one row per moment, three lanes (the agent, you, the small models), the
    round loop drawn closed; the screens below explain it (JL 261014: "we also need to make a workflow mindmap").


Open
----

1. ~~Should the items Task log which items a person opened~~: the corpus tools log every item shown (D30); the
   items Task's own views (Draw again, the map) should log through the same door.
2. The review lives in the chat (D05, D12): does the workbench also need a way to rule there, for a person without a
   chat?

3. The novelty claims ✨1-✨3 are not yet checked against related work (LLM-assisted annotation, rubric or
   constitution refinement, perspectivist labeling, active learning).

4. The building law and engine still say the person makes every judgment (Law, human gates "item"); a new Run
   type `agent-label` and the review-only gate are needed there before s42 can be built.
5. The sealed test needs your answers to score anything: do you label all 50 blind, the one time you label every
   item?

(write here, or mark the drawing in red)
