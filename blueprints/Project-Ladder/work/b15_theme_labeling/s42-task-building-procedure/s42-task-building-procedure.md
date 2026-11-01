s42 · Task building procedure: from talking with the corpus to a signed Handoff
===============================================================================

**Tags:** `Levels`

**Stage:** shaping

**For:** a deck, and the building Task step by step, from talking with the corpus to a signed Handoff, for the people who write the toolkit skills

**Delivery type:** skill

**Topic:** every step of the 🏗 building Task (`task-type: labeling-building`, s13), drawn the way s41 drew the
items Task: one tab per Stage, Operation over Result, screens as the tab develops, and above them one workflow map of
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
├── s42-task-building-procedure.excalidraw    ① the workflow map; Ⓑ the corpus, Run by Run; Ⓐ Algorithm 1; Ⓒ one round as a loop, then the Task as a tree; Ⓔ how the agent reads the corpus; Ⓕ design versions as the corpus grows; ② ③ Contract, ④ ⑤ Initial Labeling Definition, ⑥-⑨ Rounds, ⑩ ⑪ Handoff
├── s42-task-building-procedure.png           its preview
└── history/                                  the first draft, -261014a
```

```yaml
heading: ["① The building Task: who does what", "items → your labels, your guideline"]
key: "Outcome: G*, gold D* and your answers Y_S on S, signed as the Handoff. Only you make gold."
problem: "🎯 Problem: a researcher's subjective concept cannot be defined up front; a codebook written before the data misses hard cases, and no one can say how well a labeler follows it."
novelty: "🏆 Contributions: a tool to build your own benchmark, then pick its labeler · C1 an interactive guideline, every rule yours (✨1) · C2 it transfers to a weak model · C3 a benchmark that knows where it is unsure; you read only the picks (✨2), rounds pick the most valuable (✨3), a sealed exam (✨4)."
marks: [[0, 0, "✨4"], [4, 0, "✨3"], [6, 0, "✨2"], [7, 1, "✨1"]]
lanes: ["📚 corpus", "📜 guideline", "🤖 agent", "🏷 labeling agent", "🧪 open models E", "👤 you"]
lane_w: [360, 280, 380, 370, 340, 330]
symbols:
  title: "📐 Symbols: how many items, and who reads them"
  rows:
  - ["n", "all items, |X|"]
  - ["m", "the final exam S: S_sel + S_rep"]
  - ["u", "U_rand at the start"]
  - ["r", "most you read in the talk, K"]
  - ["b", "picks: b_audit + b_hunt"]
  - ["ε", "a pool's error share"]
  - ["τ", "sure, from round 1"]
  - ["e*", "the labeler picked on S_sel"]
  - ["e_out", "a model kept out of E"]
  - ["c_•", "agent's reading budget a step"]
map:
- step: "📦 Stage 1 · Contract"
  screens: "② ③"
  cells: [[2, "seal(X, m, C)", "X (n) · groups C · 👁 0", "🔒 S_sel ∪ S_rep · R"]]
  corpus: "🔒 S (m) · pool X∖S"
  guideline: "G_0: empty"
- step: "💬 Stage 2 · Initial Labeling Definition"
  screens: "④ ⑤"
  cells: [[2, "get(sample(group))", "X∖S, M · 👁 ≤ c_ask", "items, questions"], [5, "read, write notes", "≤ r in all passes", "notes M, pass k"]]
  corpus: "K read, set aside"
  guideline: "G_0 + your notes"
- cells: [[2, "draft(M)", "your notes · 👁 0", "a draft"], [5, "✍ Sign (G_1)", "the draft", "G_1"]]
  corpus: "K final"
  guideline: "G_1"
  loop: "another pass"
  loop_to: 1
- cells: [[2, "sample(X∖(S∪K), u)", "groups C · 👁 0", "U_rand"]]
  corpus: "U_rand drawn"
- step: "🔁 Stage 3 · Rounds"
  screens: "⑥ ⑦ ⑧ ⑨"
  cells: [[2, "card(P, D, R, G_t)", "U_rand · X∖(S∪K∪D) · 👁 c_pick", "b: audit + hunt"], [5, "✍ Approve", "counts per arm only", "the batch"]]
  corpus: "b picks"
  guideline: "G_t"
- cells: [[3, "lm_labeler(B, G_t)", "engine: the agent", "Ŷ, sealed"], [4, "lm_labeler(B, G_t)", "engine: each in E", "Ŷ, sealed"]]
  corpus: "picks sealed"
- cells: [[2, "show(item, 📍)", "shuffled · no labels · 👁 b", "blind, then Ŷ"], [5, "✍ JUDGE", "your record first", "+ records"]]
  corpus: "+ b records"
- cells: [[2, "learn(D, Ŷ, G_t)", "records · 👁 ≤ c_learn", "patches"], [5, "✍ accept · reject", "each patch + effect", "G_t+1"]]
  corpus: "gold flagged"
  guideline: "G_t+1 drafted"
- cells: [[2, "extend(B, G_t+1)", "picks · rules · 👁 0", "U_hunt, U_rand grow"]]
  corpus: "U grows"
- cells: [[3, "lm_labeler(U, G_t+1)", "engine: the agent", "relabel"], [4, "lm_labeler(U, G_t+1)", "engine: each in E", "sealed"]]
  corpus: "U relabeled"
  guideline: "G_t+1 run on U"
- cells: [[2, "sort_pools · measure", "labels · U_rand audit · 👁 0", "P · bounds"], [5, "✍ Stop?", "no change · ε", "go on · stop"]]
  corpus: "gold promoted"
  guideline: "G_t ← G_t+1"
  loop: "another round: t ← t+1"
  span: "round t"
- step: "✍️ Stage 4 · Handoff"
  screens: "⑩ ⑪"
  cells: [[2, "custodian: show(S)", "🔒 S · no labels", "once, logged"], [5, "✍ label S", "each item, blind", "Y_S"]]
  corpus: "🔒 S labeled"
  guideline: "G* = G_t"
- cells: [[2, "freeze(G_t, D, Y_S)", "👁 0", "the Handoff"], [5, "✍ Sign (G*)", "G* · D* · Y_S", "signed"]]
  corpus: "D* · Y_S"
  guideline: "G*, frozen"
- cells: [[3, "🔍 lm_labeler(S, G*)", "engine: the agent", "scored"], [4, "🔍 lm_labeler(S, G*)", "each in E; e_out", "e* on S_sel"]]
  corpus: "S_rep scores e*"
  guideline: "G*; e* labels X"
algorithm:
  frame: "Ⓐ The method, as a paper writes it"
  caption: "Algorithm 1: Building one label with one human authority"
  input: "Input: items X (n); groups C; sizes m, r, u, b; ε; agent a; panel E; budgets c_•"
  output: "Output: guideline G*, gold D*, your answers Y_S on S; signed"
  lines:
  - ["S ← Seal(X, m, C);  S_sel, S_rep ← Split(S)", "held back first, never shown"]
  - ["G_0, D, P ← ∅;  R ← Register(7 pools, open)", ""]
  - ["K, M ← ∅;  repeat (K, M) ← Talk(X \\ S, K, M)", "a pass: ask, read, notes; |K| ≤ r"]
  - ["until HumanSign(Draft(M)) gives G_1", "gate: Sign (G_1)"]
  - ["U ← Sample(X \\ (S ∪ K), u, C);  t ← 1", "U_rand: random, across C"]
  - ["repeat", ""]
  - ["    B ← HumanApprove(Card(P, D, R, G_t))", "gate: counts only; round 1 random"]
  - ["    Ŷ ← Label(B, G_t, {a} ∪ E), sealed", "picks labeled before you see them"]
  - ["    D ← D ∪ Judge(B, Ŷ)", "gate: shuffled; your record first"]
  - ["    G_{t+1} ← HumanRule(Learn(D, Ŷ, G_t))", "gate: each patch; conflicts re-ruled"]
  - ["    U ← U ∪ Extend(B, G_{t+1}, X \\ (S ∪ K ∪ U))", "picks, rule neighbours, a random slice"]
  - ["    P ← SortPools(Label(U, G_{t+1}, {a} ∪ E))", "relabel under the new guideline"]
  - ["    R ← Measure(P, D, R);  t ← t + 1", "bounds from this round's U_rand audit"]
  - ["until HumanStop(R)", "gate: no rule changed, every bound < ε"]
  - ["Y_S ← Custodian(HumanBlind(S))", "gate: you label S blind, once"]
  - ["return HumanSign(Freeze(G_t, D, Y_S))", "gate: Sign (G*) → scanning"]
  notation: ["Notation", "X  the items (n);  S  the final exam (m)", "S_sel picks the labeler;  S_rep reports it", "K  read in the talk (≤ r);  M  your notes", "U  = U_rand ∪ U_hunt;  B  a round's picks", "D  your gold;  Ŷ  the readers' labels", "G_t  the guideline used in round t", "R  the register;  P  each item's pool", "a  the labeling agent;  E  the open models", "π  inclusion probability;  ε  the bound", "c_•  the agent's reading budget in a step"]
  sections: ["§3 Method", "3.1 Sealed reservation  (lines 1-2)", "3.2 Initial labeling definition  (lines 3-5)", "3.3 Calibration rounds  (lines 6-14)", "3.4 New data each round  (lines 7, 11)", "3.5 Final exam and handoff  (lines 15-16)"]
corpus:
  frame: "Ⓑ The corpus, along the way"
  total: 350
  sub: "the items at each step: what is sealed, read, labeled, still in the pool"
  parts:
    sealed: ["🔒", "sealed: the final exam"]
    read: ["💬", "K: read in the talk"]
    gold: ["🏷", "your gold"]
    H: ["H", "settled high"]
    L: ["L", "settled low"]
    N: ["N", "settled none"]
    HL: ["HL", "degree border"]
    LN: ["LN", "presence border"]
    HN: ["HN", "clash"]
    HLN: ["HLN", "unmapped"]
    pool: ["", "not yet labeled"]
    scan: ["🧪", "e*'s labels under G*"]
  notes:
  - "S, the final exam: S_sel picks the labeler, S_rep reports its score; you label it blind, once, in Stage 4"
  - "pools: H, L or N when every reader gives that label, sure; HL, LN, HN, HLN by the labels the readers split over"
  - "each round: an audit arm (random in every pool) measures, a hunt arm finds; you never see a model's label before your own"
ledger:
  frame: "Ⓑ The corpus, Run by Run: who acts, what changes"
  sub: "each Run: the items after it, who acts, what changes"
  steps: [[0, "📦 Stage 1 · Contract"], [1, "💬 Stage 2 · Initial Labeling Definition"], [3, "🔁 Stage 3 · Rounds"], [11, "✍️ Stage 4 · Handoff"], [13, "🔍 scanning, the next Task"]]
  bars:
  - [[sealed, 100], [pool, 250]]
  - [[sealed, 100], [read, 20], [pool, 230]]
  - [[sealed, 100], [read, 20], [pool, 230]]
  - [[sealed, 100], [read, 20], [pool, 230]]
  - [[sealed, 100], [read, 20], [pool, 230]]
  - [[sealed, 100], [read, 20], [gold, 30], [pool, 200]]
  - [[sealed, 100], [read, 20], [gold, 30], [pool, 200]]
  - [[sealed, 100], [read, 20], [gold, 30], [pool, 200]]
  - [[sealed, 100], [read, 20], [gold, 30], [H, 55], [L, 40], [N, 65], [HL, 18], [LN, 15], [HN, 4], [HLN, 3]]
  - [[sealed, 100], [read, 20], [gold, 30], [H, 55], [L, 40], [N, 65], [HL, 18], [LN, 15], [HN, 4], [HLN, 3]]
  - [[sealed, 100], [read, 20], [gold, 70], [H, 52], [L, 38], [N, 64], [HL, 3], [LN, 2], [HN, 1]]
  - [[sealed, 100], [read, 20], [gold, 70], [H, 52], [L, 38], [N, 64], [HL, 3], [LN, 2], [HN, 1]]
  - [[sealed, 100], [read, 20], [gold, 70], [H, 52], [L, 38], [N, 64], [HL, 3], [LN, 2], [HN, 1]]
  - [[sealed, 100], [scan, 250]]
  columns: ["Run", "🤖 agent", "🏷 labeling agent", "👤 you", "🧪 open models E", "📚 corpus", "📜 guideline", "🏷 labels"]
  rows:
  - ["corpus-contract", "seals S: 50 to pick, 50 to report", "—", "—", "—", "🔒 100 · pool 250", "G_0, empty", "none"]
  - ["definition-discussion", "shows items by group, pass by pass", "—", "reads ≤ r, writes notes", "—", "K: 20 read, out of rounds", "G_0", "notes, never labels"]
  - ["guideline-seed · sample-extend", "drafts from your notes; draws U_rand", "—", "✍ Sign (G_1)", "—", "U_rand drawn: all 230 (V1)", "G_1", "none"]
  - ["round-prepare", "card: 30 at random (round 1)", "—", "✍ Approve", "—", "30 picked", "G_1", "—"]
  - ["agent-label · weak-prelabel", "—", "labels the 30, sealed", "—", "label the 30, sealed", "—", "G_1", "sealed labels"]
  - ["human-calibration", "shows each, shuffled, no labels; reveals after your lock", "—", "✍ rules 30: first, then final", "—", "—", "G_1", "records 30"]
  - ["guideline-learn", "proposes patches; flags conflicting gold", "—", "✍ accept · reject", "—", "—", "G_2 drafted", "—"]
  - ["sample-extend", "U grows (DICES: U is all)", "—", "—", "—", "U_hunt · U_rand", "G_2", "—"]
  - ["agent-label · pool-sort · round-measure", "sorts 7 pools; bounds from the audit", "relabels U with G_2", "—", "relabel U, sealed", "H 55 · L 40 · N 65 · HL 18 · LN 15 · HN 4 · HLN 3", "G_2 run on U", "gold 30"]
  - ["round-close", "promotes gold and G_2", "—", "✍ Stop? no: rules changed", "—", "—", "G_2", "gold 30"]
  - ["round 2 … T", "audit + hunt picks (DICES: hunt within U); the same steps", "labels picks; relabels U", "✍ rules the picks", "the same, sealed", "HL 3 · LN 2 · HN 1 · HLN 0", "G_T: changed nothing", "gold 70"]
  - ["final-exam-label", "the custodian shows S, no labels", "—", "✍ labels 100, blind", "—", "🔒 S opened by you, once", "G_T", "Y_S 100"]
  - ["handoff-freeze", "freezes", "—", "✍ Sign (G*)", "—", "—", "G* = G_T", "D* 70 · Y_S"]
  - ["🔍 scanning · test", "picks e* on S_sel, reports on S_rep", "labels S, a candidate", "—", "label S; e_out too", "S scored", "G*", "e* labels X"]
  note: "Gold is only what you rule; reader labels are kept, never gold. U is relabeled before Stop. Counts are an example (DICES runs V1)."
changes:
  map:
  - {at: [1300, 132], text: "six lanes; JUDGE blind"}
  - {under: boxes, text: "problem: a codebook before the data; C1 interactive"}
  - {lane: 0, text: "corpus lane"}
  - {at: [1300, 104], text: "each box: in above, out below"}
  - {lane: 4, text: "a panel of open models"}
  - {lane: 1, text: "guideline lane"}
  - {at: [2000, 104], text: "each agent box: the call it makes"}
  - {row: 0, dy: 132, text: "S split"}
  - {row: 1, dy: 140, text: "K: was N"}
  - {row: 2, dy: 20, text: "passes"}
  - {row: 3, dy: 20, text: "U_rand: own box"}
  - {row: 4, dy: 110, text: "audit + hunt"}
  - {row: 5, dy: 20, text: "labeled first"}
  - {row: 6, dy: 20, text: "JUDGE blind"}
  - {row: 7, dy: 20, text: "gold flagged"}
  - {row: 8, dy: 20, text: "extend(U)"}
  - {row: 9, dy: 20, text: "relabel first"}
  - {row: 10, dy: 20, text: "one Stop rule"}
  - {row: 11, dy: 110, text: "S blind, once"}
  - {row: 13, dy: 20, text: "S_sel · S_rep"}
  algorithm: "lines 7-16 redone after review: two arms, picks labeled first, blind JUDGE, extend U, relabel before Stop, S labeled blind"
  corpus: "S split; picks labeled first; you label S blind (D57-D63)"
  round: "redone after review: PICK · LABEL · JUDGE · LEARN · EXTEND · MEASURE · CLOSE"
  levels: "named: Stage 1-4, Step 1-7"
  gformat: "new: the guideline format and the seven pools named"
  reader: "find_neighbours(seed, k, corpus, rank_by): one tool, five ways to rank · built: engine/corpus_tools.py (nearest works today)"
  versions: "new: four design versions, linked as the corpus grows"
  ledger: "Run by Run after review: blind JUDGE, EXTEND, relabel, S labeled blind"
round:
  frame: "Ⓒ One round, step by step, and the Task as a tree"
  sub: "Stage 3: seven Steps, the same each round; the round closes, then another round or Stop"
  steps:
  - ["Step 1 · PICK", "two arms: an audit, random from U_rand by pool (π kept), and a hunt over X∖(S∪K∪D); you see counts only; round 1 random", "🤖 proposes · ✍ you Approve", "card.md · human_batch.jsonl · prospect.md"]
  - ["Step 2 · LABEL", "the picks labeled by the agent and each model in E, sealed: Ŷ", "🏷 labeling agent · 🧪 E, sealed", "labels/picks.jsonl"]
  - ["Step 3 · JUDGE", "shuffled, blind: your label and region, locked; then Ŷ shows; your final is kept with your first", "✍ you", "sessions/events.jsonl · human_final.jsonl"]
  - ["Step 4 · LEARN", "patches from your corrections; earlier gold a patch conflicts with is flagged for a blind re-rule", "🤖 proposes · ✍ you accept · reject · narrow", "policy_draft/"]
  - ["Step 5 · EXTEND", "U grows: new picks and rule neighbours (U_hunt), a random slice (U_rand)", "🤖 agent, 👁 0", "u.jsonl"]
  - ["Step 6 · MEASURE", "relabel U under G_t+1; 7 pools; bounds from this round's U_rand audit vs your first records", "🏷 · 🧪 · 🤖", "pools.jsonl · metrics.json"]
  - ["Step 7 · CLOSE", "promote gold and G_t+1; Stop when no rule changed and every bound < ε", "🔐 keeper · ✍ you: Stop?", "checkpoint.json"]
  loop: "another round: PICK from G_t's pools"
  stop: "✍ Stop: no rule changed, every bound < ε, or an open pool accepted → Stage 4"
  from: "the law's CARD · PREPARE · PRELABEL · JUDGE · LEARN · MEASURE · CLOSE, with EXTEND and the relabel added"
tree:
  frame: "The building Task as a tree: Stages and Steps"
  sub: "Task → Stage → round → Step → Run: each with its purpose, who acts, and what it leaves"
  columns: ["Stage · Step", "Purpose", "Who", "Run", "Leaves"]
  rows:
  - [0, "📦 Stage 1 · Contract", "seal the final exam S (S_sel, S_rep); start G_0 and the register; no label is made", "🤖 agent", "corpus-contract", "corpus/ · policy G_0 · register.md"]
  - [0, "💬 Stage 2 · Initial Labeling Definition", "talk in passes (K ≤ r), sign what the label means, then draw U_rand", "🤖 asks · 👤 notes · ✍ you Sign (G_1)", "definition-discussion · guideline-seed · sample-extend", "notes M · G_1 · U_rand"]
  - [0, "🔁 Stage 3 · Rounds", "round_1, round_2, …: until a round changes no rule and every bound < ε", "", "", "rounds/round_t/"]
  - [1, "Step 1 · PICK", "audit arm + hunt arm; counts only; round 1 random", "🤖 proposes · ✍ you Approve", "round-prepare", "card.md · human_batch.jsonl · prospect.md"]
  - [1, "Step 2 · LABEL", "the picks labeled by the agent and E, sealed", "🏷 · 🧪, sealed", "agent-label · weak-prelabel", "labels/picks.jsonl"]
  - [1, "Step 3 · JUDGE", "shuffled, blind first record, lock, reveal, final", "✍ you", "human-calibration", "sessions/events.jsonl · human_final.jsonl"]
  - [1, "Step 4 · LEARN", "patches; conflicting gold flagged for a blind re-rule", "🤖 proposes · ✍ you accept · reject · narrow", "guideline-learn", "policy_draft/"]
  - [1, "Step 5 · EXTEND", "U_hunt and U_rand grow", "🤖 agent", "sample-extend (new)", "u.jsonl"]
  - [1, "Step 6 · MEASURE", "relabel U under G_t+1; 7 pools; bounds from the U_rand audit", "🏷 · 🧪 · 🤖", "agent-label · weak-prelabel · pool-sort (new) · round-measure", "pools.jsonl · metrics.json"]
  - [2, "Step 7 · CLOSE", "promote gold and G_t+1; another round or Stop", "🔐 keeper · ✍ you: Stop?", "round-close", "checkpoint.json"]
  - [0, "✍️ Stage 4 · Handoff", "you label S blind, once, through the custodian; freeze G*, D*, Y_S", "✍ you label S · ✍ Sign (G*)", "final-exam-label (new, the custodian's) · handoff-freeze", "handoff/label-v1.yaml → 🔍 scanning"]
reader:
  frame: "Ⓔ How the agent reads the corpus"
  sub: "the agent never holds the list: it calls tools over the frozen items and the map"
  tools_title: "🔧 The corpus tools"
  tools_columns: ["tool", "returns", "used for"]
  tools:
  - ["stats(filter)", "counts; the map's groups, their top words and typical items", "the overview"]
  - ["sample(group, n, seed)", "random items from one group", "an unbiased look, group by group"]
  - ["search(query)", "items by keyword (meaning: next)", "the hard cases you named"]
  - ["find_neighbours(seed, k, corpus, rank_by)", "k new items from corpus near a seed set (a pool, your corrections), ranked", "the funnel: from a pool to the next items to review"]
  - ["lm_labeler(items, guideline, engine)", "each item's label, region, confidence, reason; sealed", "LABEL: the agent and each model in E"]
  - ["get(item)", "one item's full text, logged, within the step's budget", "reading it"]
  rules_title: "📏 Where a round's picks come from"
  rules_columns: ["#", "arm or seed", "finds"]
  rules:
  - ["A", "audit arm: random from U_rand by pool, π kept", "each pool's error rate, unbiased; shared mistakes"]
  - ["1", "hunt: open border pools", "degree · presence · clash · unmapped, and neighbours"]
  - ["2", "hunt: neighbours of your corrections", "more of what the guideline just got wrong"]
  - ["3", "hunt: queries from the definition", "the hard cases you named in the talk"]
  - ["4", "hunt: 🧭 odd on the map", "H, L, N items whose nearest gold says otherwise"]
  - ["5", "hunt: diversity", "at most one per near-duplicate cluster"]
  - ["—", "never", "S, K or gold; the audit only from U_rand"]
  funnel_title: "🔻 The hunt arm: from n items to b_hunt, the agent reading at most c_pick; U included"
  funnel:
  - ["① seed", "seeds 1-4 say where to look", "👁 0", "seed sets"]
  - ["② retrieve", "find_neighbours(seeds, 10·c_pick, X∖(S∪K∪D), nearest)", "👁 0", "~10·c_pick ids"]
  - ["③ rank", "a cheap engine labels each; re-ordered by rank_by", "👁 0", "a ranked list"]
  - ["④ read, pick", "the agent reads the top c_pick; b_hunt picks, one per cluster", "👁 ≤ c_pick", "card · ✍ Approve"]
  methods_title: "🧭 rank_by: how find_neighbours orders what it finds"
  methods_columns: ["rank_by", "ranks first", "needs"]
  methods:
  - ["nearest", "the closest to the set", "the map only"]
  - ["confidence", "the panel's least confident", "the panel's labels"]
  - ["disagree", "where the panel splits most", "the panel's labels"]
  - ["classifier", "a simple model trained on your gold: its most unsure", "gold; never makes gold"]
  - ["value", "the highest v(x), below", "gold: from round 2"]
  value_title: "⚖️ The score: v(x) = unsure(x) · dense(x)^β · new(x) · (1 + γ · near(x))"
  value_columns: ["factor", "measured as", "why it counts"]
  value:
  - ["unsure(x)", "1 − the share of readers giving the majority label", "your ruling settles something open"]
  - ["dense(x)", "how many items of X sit near x, scaled 0-1", "one ruling carries over to many"]
  - ["new(x)", "distance to the nearest gold, scaled 0-1", "ground no rule has seen"]
  - ["near(x)", "1 if it neighbours a rule changed last round", "tests that G_t fixed it"]
  split: "Error = the readers' majority ≠ your first record. Error mass = size × rate, both from this round's U_rand audit (1/π weights), as a share of X; ε and b_audit are set together in the Contract. Stop: no rule changed, every upper 95% bound < ε."
  guards: "Three guards live in the tools: S only through the custodian's one logged door; every item shown is logged with who read it; each step's reading budget comes from the job's config (c_ask, c_pick, c_learn; r for the talk), and past it a tool returns ids and counts, never text."
  scale: "At scale: U is 2-5k items across the map's groups; all of X is labeled only in scanning. DICES: U is the whole pool."
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
  pools_title: "The seven pools: one rule, sort_pools"
  pools_columns: ["pool", "name", "an item is here when", "the guideline needs"]
  pools:
  - ["H · L · N", "Settled high · low · none", "every reader gives that label (any below τ: flagged unsure, audited more)", "an audit: shared mistakes hide here"]
  - ["HL", "Degree border", "the readers split over high and low", "a severity rule"]
  - ["LN", "Presence border", "the readers split over low and none", "a threshold rule"]
  - ["HN", "Clash", "the readers split over high and none", "the meaning clarified: the most valuable"]
  - ["HLN", "Unmapped", "the readers give all three", "a new rule"]
versions:
  frame: "Ⓕ Design versions: reading the corpus as it grows"
  sub: "four ways to run the rounds; the corpus grows from left to right; one is proposed, the others kept to compare"
  arrow: "bigger corpus"
  items:
  - name: "V1 · Label everything"
    how: "every reader labels every item, every round"
    cost: "items × rounds calls; fine below ~1k items"
    fits: "DICES-350"
    risk: "cost grows with the corpus"
  - name: "V2 · Development sample + search rules"
    how: "a fixed sample of 2-5k across the map's groups is labeled every round; picks by seeds 1-4"
    cost: "sample × rounds; the corpus once, in scanning"
    fits: "10k to 1M items"
    risk: "a kind of item missing from the sample stays unseen"
  - name: "V3 · Growing sample"
    how: "U = U_rand (random) ∪ U_hunt; each round EXTEND adds picks, rule neighbours and a fresh random slice"
    cost: "a little more than V2"
    fits: "any size; rare harms, long tails"
    risk: "none for counts: they come from U_rand and the audits only"
    proposed: true
  - name: "V4 · Search only"
    how: "nothing is labeled ahead; each round the rules retrieve ~200 candidates, and only those are labeled"
    cost: "lowest: candidates × rounds"
    fits: "very large or streaming corpora"
    risk: "pools are estimates; a border no rule looks for is never found"
  note: "Proposed: V3 (s42-D57): new data enters U every round, and every count stays unbiased. DICES runs V1, since U is the whole pool. A version is chosen in the Contract and written there."
screen:
  task: "Task · t03 · building"
  line: "Labeling · Block b01 · Task t03 · <label> on <dataset>"
  tabs: ["1 · Contract", "2 · Initial Labeling Definition", "3 · Rounds", "4 · Handoff"]
tabs:
- act: "Act 2 · Work › Stage 1 · Contract"
  step_arrow: "Stage 1"
  key: "First, before anyone reads an item: the items come in, the final exam S (m) is sealed and split, G_0 and the register start empty. No label is made; the agent reads no item (👁 0)."
  states:
  - title: "② Work › 1 · Contract · 1 of 2: hold back first"
    changed: "S split: S_sel picks, S_rep reports"
    tab: "1 · Contract"
    step: "📦 Stage 1 · Contract"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Items: "X · items-v3 · n items", Groups: "C · from the items Task's map", Final exam: "S · m sealed across C: S_sel + S_rep", Agent reads: "👁 0: ids and counts"}
    prompt: "/haipipe-labeling-building <task> contract: import the items, seal and split the final exam, start G_0."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the agent runs it"
  - title: "③ Work › 1 · Contract · 2 of 2: what is held back"
    tab: "1 · Contract"
    step: "📦 Stage 1 · Contract"
    chip: "✓ done"
    folded: ""
    sections:
    - {t: "📚 Corpus: 🔒 S (S_sel, S_rep) · pool X∖S"}
    - {t: "📜 Guideline G_0: empty"}
    - {t: "🗂 Register: 7 pools, all open"}
    mark: "the Contract Run writes these; it makes no label"
- act: "Act 3 · Work › Stage 2 · Initial Labeling Definition"
  step_arrow: "Stage 2"
  key: "Talk with the corpus in passes: each pass the agent asks (👁 ≤ c_ask), you read a few items and write notes, it drafts the definition; another pass, or Sign (G_1). At most r items read in all: the set K, never drawn again."
  states:
  - title: "④ Work › 2 · Definition · 1 of 2: talk, pass by pass"
    tab: "2 · Initial Labeling Definition"
    step: "💬 Stage 2 · pass k"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Pool: "X∖S, the final exam out", You read: "≤ r in all passes; |K| so far", Agent reads: "👁 ≤ c_ask a pass", Rounds: "never draw K again"}
    - title: "Pass k"
      rows: {Asked: "<the agent's questions>", Shown: "<the items, by group>", Notes: "<your notes, M>"}
    prompt: "/haipipe-labeling-building <task> definition: one more pass with me through the items, group by group; keep my notes."
    mark: "copy it, talk in Claude or Codex"
    arrow: "the agent drafts"
  - title: "⑤ Work › 2 · Definition · 2 of 2: Sign (G_1) or another pass"
    tab: "2 · Initial Labeling Definition"
    step: "💬 Stage 2 · draft after pass k"
    chip: "✍ sign"
    boxes:
    - title: "Definition · the draft"
      dashed: true
      button: "Sign · Another pass"
      mark: "you read it, then sign or talk again"
      rows: {Label: "how unsafe is the AI's last reply?", Values: "high · low · none", Low: "<what low means here>", None: "no harm in it; never 'unsure'", From: "k passes · |K| items read"}
    prompt: "/haipipe-labeling-building <task> definition: write the definition from our talk, and stop for my Sign."
    sections:
    - {t: "💬 The talk, pass by pass"}
    - {t: "📝 Your notes and hard cases"}
    - {t: "📜 Guideline G_1 · U_rand drawn"}
    mark: "after Sign: the step folds ✓, these cards stay"
- act: "Act 4 · Work › Stage 3 · Rounds"
  step_arrow: "Stage 3"
  key: "A round: you approve the pick (an audit arm and a hunt arm); the readers label the picks, sealed; you rule each pick before seeing any label; you rule each patch; U grows and is relabeled under G_t+1; Stop when no rule changed and every pool's bound < ε."
  states:
  - title: "⑥ Work › 3 · Rounds · 1 of 4: approve the pick, audit + hunt"
    changed: "two arms: an audit measures, a hunt finds"
    tab: "3 · Rounds"
    step: "🔁 Round t · PICK"
    chip: "✍ approve"
    boxes:
    - title: "Now"
      rows: {Corpus: "U = U_rand + U_hunt · gold so far", Pools: "7, sorted under G_t", Guideline: "G_t", Bounds: "each pool's error bound, from the audits"}
    - title: "This round's pick · round_t"
      dashed: true
      button: "Approve"
      mark: "you read it and approve"
      rows: {Audit arm: "b_audit from U_rand, by pool, π kept", Hunt arm: "b_hunt from X∖(S∪K∪D): seeds 1-4, v(x)", You see: "counts per arm and pool, no items", Round 1: "random from U", We expect: "<written before item 1>"}
    prompt: "/haipipe-labeling-building <task> round: propose round t's card, audit and hunt arms, and stop for my Approve."
    mark: "🧭: settled, but its neighbours' gold disagrees"
    arrow: "the picks are labeled, sealed"
  - title: "⑦ Work › 3 · Rounds · 2 of 4: rule each pick, blind first"
    changed: "blind: your record first, then the readers"
    tab: "3 · Rounds"
    step: "🔁 Round t · JUDGE · item i of b, shuffled"
    chip: "→ review"
    boxes:
    - title: "Item · <item id>"
      rows: {Before: "Person: … AI: … Person: …", Judged: "<the AI's last reply>", Arm and pool: "hidden until Lock"}
    - title: "📍 The 3-D map, no labels yet"
      rows: {This item: "the dot ringed", Neighbours: "grey until you lock", Turn it: "drag to rotate; hover for text"}
    - title: "👤 Your first record"
      dashed: true
      button: "Lock"
      mark: "you rule it, alone"
      rows: {Label: "high · low · none", Region: "H · L · N or between: HL · LN · HN · HLN", Why: "<one line>"}
    - title: "Shown after Lock"
      rows: {🏷 Agent: "low · LN · rule 3", 🧪 E: "<model 1> none · <model 2> low · <model 3> none", Gold nearby: "neighbours coloured now"}
    - title: "👤 Your final"
      dashed: true
      button: "Save"
      mark: "keep or change; both kept"
      rows: {Label: "high · low · none", Why: "<if changed, why>"}
    prompt: "/haipipe-labeling-building <task> round: show me round t's pick, one item at a time, blind first."
    mark: "only the b picked come to you; your final is gold, your first is kept"
    arrow: "the agent learns"
  - title: "⑧ Work › 3 · Rounds · 3 of 4: rule the patch"
    tab: "3 · Rounds"
    step: "🔁 Round t · LEARN"
    chip: "✍ rule"
    boxes:
    - title: "Patch · rule 4 · into G_t+1"
      dashed: true
      button: "Accept · Reject · Narrow"
      mark: "you rule it"
      rows: {Says: "<the new or changed rule>", Why: "items <a>, <b> you corrected", Conflicts: "<j> earlier gold: flagged, re-ruled blind", Checked on: "gold no rule used", Agent read: "👁 ≤ c_learn"}
    prompt: "/haipipe-labeling-building <task> round: propose rule patches from round t, with what each changes."
    mark: "one ruling per patch"
    arrow: "U grows; relabeled under G_t+1"
  - title: "⑨ Work › 3 · Rounds · 4 of 4: MEASURE · CLOSE"
    changed: "relabel first; one Stop rule"
    tab: "3 · Rounds"
    step: "🔁 Round t · MEASURE · CLOSE"
    chip: "✓ done"
    folded: ""
    sections:
    - {t: "🔁 U grew: picks, rule neighbours, a random slice"}
    - {t: "📊 The 7 pools, sorted under G_t+1"}
    - {t: "📏 Each pool's bound, from this round's U_rand audit"}
    - {t: "🤝 Each reader vs your first records"}
    - {t: "📜 Guideline: G_t ← G_t+1"}
    - {t: "⏭ Stop: no rule changed, every bound < ε", button: "Stop"}
    mark: "or you accept an open pool as a limitation"
- act: "Act 5 · Work › Stage 4 · Handoff"
  step_arrow: "Stage 4"
  key: "You label the final exam S once, blind to every reader; then G* (the last G_t, already run on U), your gold D* and your answers Y_S are frozen with their lineage and signed; scanning reads only this."
  states:
  - title: "⑩ Work › 4 · Handoff · 1 of 2: label S, then Sign (G*)"
    changed: "you label S blind, before the Sign"
    tab: "4 · Handoff"
    step: "✍️ Stage 4 · Handoff"
    chip: "✍ sign"
    boxes:
    - title: "Final exam · 🔒 S"
      dashed: true
      button: "Label blind"
      mark: "each item alone, once"
      rows: {Shown: "the item only: no reader labels, no pools", S_sel: "picks the labeler", S_rep: "reports its score", Door: "the custodian's, once, logged"}
    - title: "Handoff · handoff/label-v1.yaml"
      dashed: true
      button: "Sign (G*)"
      mark: "you sign it"
      rows: {Guideline: "G* = G_T, run on U", Gold: "D* · your rulings", Final exam: "Y_S · your answers on S", Lineage: "G_0 → G_1 → … → G_T"}
    prompt: "/haipipe-labeling-building <task> freeze: show me S blind, then freeze the Handoff, and stop for my Sign."
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
    - {t: "🔒 Your answers on S, Y_S"}
    - {t: "🔍 Next: scanning picks e* on S_sel, reports on S_rep"}
    mark: "Report shows these Result cards only, as in s41"
```


1 · The levels: Task → Stage → round → Step → Run
-------------------------------------------------

```text
🏗 building Task (t03_dices350_response_safety_labeling)
├── Stage 1 · Contract                       Run: corpus-contract           S sealed and split: S_sel · S_rep
├── Stage 2 · Initial Labeling Definition    Runs: definition-discussion · guideline-seed      ✍ Sign (G_1)
├── Stage 3 · Rounds                         round_1, round_2, … until ✍ Stop
│   └── round_t
│       ├── Step 1 · PICK      Run: round-prepare                   audit + hunt arms · ✍ Approve
│       ├── Step 2 · LABEL     Runs: agent-label · weak-prelabel   the picks, sealed
│       ├── Step 3 · JUDGE     Run: human-calibration               ✍ blind first, then final: gold
│       ├── Step 4 · LEARN     Run: guideline-learn                 ✍ accept · reject · narrow
│       ├── Step 5 · EXTEND    Run: sample-extend (new)             U_hunt · U_rand grow
│       ├── Step 6 · MEASURE   Runs: agent-label · weak-prelabel · pool-sort (new) · round-measure
│       └── Step 7 · CLOSE     Run: round-close                     ✍ Stop? → another round
└── Stage 4 · Handoff                        Runs: final-exam-label (new) · handoff-freeze   ✍ label S · ✍ Sign (G*)
```

A Stage is one tab. Stage 3 repeats in rounds; a round is a folder, `rounds/round_<t>/`, not a Run. A Step is one
Run or more, named on disk `run-labeling-<operation>-<MMDD>-<target>`.


2 · The Stages, in the law's order
----------------------------------

| tab | the engine's Run Types (ref/step-order.md) | the person's gate |
|---|---|---|
| 1 · Contract | corpus-contract (the reservation inside it) · test-reserve* · embedding-build* (done in the items Task) | none: no label is made |
| 2 · Initial Labeling Definition | discovery-search* · definition-discussion · G0 Confirm meaning · guideline-seed* | Sign (G_1) |
| 3 · Rounds | round-prepare · agent-label · weak-prelabel · human-calibration · guideline-learn · sample-extend · pool-sort · round-measure · round-close | Approve · JUDGE (first, final) · rule · Stop |
| 4 · Handoff | final-exam-label · handoff-freeze | label S · Sign (G*) |

A round folder `rounds/round_<t>/` is an episode, not a Run; its Runs are the nine above. The engine still calls the
Sign (G_1) gate G0; sample-extend, pool-sort and final-exam-label are new (Open 6).


Decided
-------

s42-D01 · Talking with the corpus is part of building, before its meaning is signed, not a Task type of its own
    (261014; JL asked "how do you think?"): the meaning needs what the person learned, and the law already has it
    (definition-discussion and discovery-search, then the G0 gate).
s42-D02 · (Stage 2 renamed: D17) The law's order (ref/step-order.md; the reviewer, 261014): 1 Contract (import, the sealed set held back,
    guideline v0, the register) before anyone reads an item; 2 Meaning (talk, then Sign at G0); 3 Rounds; 4 Handoff.
s42-D03 · (updated: K ≤ r, D64; readers' seal) Explore's notes are never labels and never gold: P0 makes no label, and gold comes only from a person's
    judgment in a closed round. The up to 30 items read in the talk are never drawn into a round, so a small model's
    seal always comes before the person's first sight (Law 2). (261014, the agent's call: the law decides it.)
s42-D04 · (updated: Stage 2, D17) The values are the engine's high · low · none (ordinal, how unsafe the reply is); none means no harm in it,
    never unsure; unsure is a note beside a label. The Meaning step writes what low means for DICES. (261014)
s42-D05 · (superseded by D12: the labeling agent labels, the person reviews) The person labels in the chat with the agent (the moderator is the only one who talks with the person);
    the Rounds tab shows the session live, read-only, item by item: first label, lock, the small models revealed,
    final. (261014)
s42-D06 · (sizes now symbols, D41; S split, D59) 50 of the 350 are held back, drawn across the items Task's groups with a seed; a round draws 20 (the
    engine's default) per arm; round 1 one arm at random, later rounds two, near a register cell and at random. Items glanced at
    in the items Task (Draw again, the map) may be in the sealed set: accepted and written in the Contract as a
    limitation, since nothing records what was seen there (s41's Open 1). (261014)
s42-D09 · ① says the problem and the novelty above the map, each novelty marked ✨1-✨4 where it happens (JL 261014:
    "what is the novelty? what is the problem we want to solve here?"; "add more here ... I want all the things
    here"). The claims are the agent's reading, not yet checked against related work (Open 3).
s42-D10 · (superseded by D23, D52) The small models are named: Haiku 4.5 (claude-haiku-4-5-20251001) leads the committee, beside one open small
    model so the results can be reproduced; each labels alone and sealed, and their agreement is never gold (JL 261014:
    "could we call it haiku 5.5?"; there is no Haiku 5.5, the newest small Claude is Haiku 4.5).
s42-D11 · Ⓑ follows the corpus, not the steps (JL 261014: "another frame to show ... the data side ... the corpus ...
    selected and chosen and labeled ... in the perspective of the corpus"): one bar of the 350 items per step, split
    into sealed · read in the talk · your gold · not yet chosen, and at the end what scanning labels.
s42-D12 · (updated by D58: your record first, then the labels) The labeling agent labels the items, not the person (JL 261014: "I don't want a human to do the labeling.
    I want the agent has a subagent to do it ... with this guideline"; chosen: "Review disagreements"). Each round
    Haiku 4.5 labels sealed, the labeling agent labels with the current guideline and names the rule it used, and the
    person reviews only where the two disagree or the labeling agent is unsure. Gold is what the person confirms or
    corrects; agreed labels are kept, never gold. This changes haipipe-labeling-building's law (the person no longer
    makes every judgment): the law and its engine still need the change (Open 6).
s42-D13 · (superseded by D23, D52, D50) The labeling agent is a strong model (Sonnet 5 or Opus 5.5) given the guideline; Haiku 4.5 is the cheap model that
    should come to match it, and scanning runs Haiku on the corpus (chosen: "Strong labels, Haiku learns").
s42-D15 · The labeling sub-agent is called the labeling agent (JL 261014: "could you call it labeling agent?").
s42-D16 · (superseded by D20, D32) Ⓓ, under Ⓑ's bars, explains each step: what you do, its input, its process, its output (JL 261014: "could you
    explain each step, what to do, input, process, and output?").
s42-D17 · (updated: a Stage, D28) Step 2 is called Initial Labeling Definition, not Meaning (JL 261014: "could we change this to the Initial
    Labeling Definition"); it matches the law's Labeling › Definition view and its G0 gate.
s42-D18 · (superseded by D20, D32) Ⓓ joins Ⓑ: one row per step, its corpus bar beside what you do, its input, process and output (JL 261014:
    "what I mean is B and D into one").
s42-D19 · (updated by D59: m) The 50 held back are called the final exam wherever they show (JL 261014: "could you add that (like final
    testing, final exam)"): they test, once building is over, whether a model with the frozen guideline matches the
    person on items nobody has seen.
s42-D20 · (updated: Ⓑ is the ledger, Ⓒ the round; panel E) Ⓑ and Ⓒ are one table (JL 261014: "these two can be merged together as well"): one row per Run, grouped
    under its step, with the corpus bar after it, then the agent, the labeling agent, you, Haiku, the corpus, the
    guideline and the labels. "You do" is the you column; "process" is the acting columns; "input → output" is the
    corpus, guideline and labels from one row to the next. The step table (D16, D18) is folded into it.
s42-D21 · Plain words for the round card (JL 261014: "a card and a forecast is very hard to understand ... we are
    trying to collect the examples from the dataset, right?"): the card is "pick this round's items", the forecast
    "what we expect", and Release is "Approve". The law keeps its own words (card, prospect, release).
s42-D22 · (superseded by D57: U grows; counts from U_rand) Every item takes part in every round (JL 261014: "the whole corpus, all the items, interact with it ... we
    got these types of items ... based on the items we just cycle around"; chosen: "Every item in the pool"): each
    round the labeling agent and Haiku label all 270 with the current guideline, each item gets a type (✅ settled:
    both agree, sure · 🤔 unsure · ⚖️ disagree), the pick comes from 🤔 and ⚖️ plus a few ✅ to check, your rulings
    are gold, your corrections drive the rules, and after a rule changes every item is labeled again. Stop when few
    🤔 ⚖️ are left and no hard region is open. Ⓑ counts the types round by round.
s42-D23 · (updated by D52: a panel E) The cheap model is a small open model, not Haiku 4.5 (JL 261014: "this could be even weaker model ... that we
    can scale up for large amount of data"): an open model of about 30B (the Qwen3 or Gemma family; the exact one is
    chosen when built) runs on our own hardware over any amount of data, can be fine-tuned on the gold, and lets a
    reader reproduce the results. It labels every item each round, sealed, and labels the corpus in scanning.
    Supersedes D10's Haiku 4.5.
s42-D24 · (updated by D61: one sort_pools rule) The sort uses both (JL 261014: "how do we do the sort here? using the embeddings method or what? maybe we can
    do it in both way?"): the two models' labels give the type (✅ same label, both sure · 🤔 same, not sure · ⚖️
    different); the items Task's map flags 🧭 a ✅ whose nearest gold neighbours carry another label, or that sits in a
    group with no gold yet. The pick takes 🤔 ⚖️ and the 🧭, spread across the map's groups. The map only picks; it
    never sets a label.
s42-D25 · (updated by D61, D63) The pools are the register's seven regions (JL 261014: "we have several types of the pools ... H, L, None, H-L,
    H-None, L-None, L-H-N, I think we have the definition as before"; the Guide's "By in-between regions"): each
    round every item lands in H, L or N when both models give that label and are sure, in HL, LN or HN when it sits
    between two labels, in HLN when the definition does not cover it. The register keeps each pool open, covered or
    risky; a round picks from the open pools and the map's 🧭; you give each ruled item its label and its region;
    Stop when no pool is open, or one is accepted as a limitation. Supersedes D22's ✅ 🤔 ⚖️ types and D24's sort.
s42-D26 · (superseded by D60-D63) One round is seven steps, each with its purpose, who acts and what it leaves: LABEL · SORT · PICK · JUDGE ·
    LEARN · MEASURE · CLOSE, drawn as a loop in Ⓒ and named on the map's rows (JL 261014: "for each round, we can
    separate them into different steps, and each step with the purpose ... I remember I discussed about this";
    "I think it is correct, please go ahead"). They are the law's CARD · PREPARE · PRELABEL · JUDGE · LEARN ·
    MEASURE · CLOSE (haipipe-labeling-building ref/step-order.md; haipipe-labeling-rounds), with every item labeled
    and sorted first and PREPARE folded into PICK.
s42-D27 · (updated by D33) The frames read ① then Ⓑ then Ⓐ, left to right, as the person arranged them (JL 261014: "I would like to
    have this arrange"); Ⓒ, the round, sits under Ⓐ, clear of the screens.
s42-D28 · (updated: Ⓒ; Open 6) The levels are named Task → Stage → round → Step → Run (JL 261014: "how do we call this, also the step? what
    is the tree like description for it"; "make things like this ... as a new frame"): the building Task has four
    Stages (its tabs); Stage 3 repeats in rounds, each a folder, not a Run; a round has seven Steps; each Step is one
    Run, LABEL two. Ⓓ draws it as one table, a tree by indent: purpose, who, Run, what it leaves. pool-sort is a new
    Run type, beside agent-label (Open 6).
s42-D29 · (updated: Step 1 · PICK; Ⓓ folded into Ⓒ) Every frame names its levels the same way (JL 261014: "add them into the sNN"): "Stage 1 · Contract" to
    "Stage 4 · Handoff" on the map, Ⓑ, the screens and the acts; "Step 1 · LABEL" to "Step 7 · CLOSE" in Ⓒ and Ⓓ.
    The face's § 1 holds the tree.
s42-D30 · (updated by D53, D60) The agent reads the corpus through tools, and a round picks by search rules (JL 261014: "if we have the very
    large corpus, it is impossible to put all the items to ask the agent to read, so we should have some searching
    rules"; "how did the agent talk to the corpus"): stats, sample, search, neighbors, contrast, get, over the frozen
    items and the map; the final exam is not in the index, and every item shown is logged. At scale the rounds run on
    a development sample (2-5k across the map's groups), the whole corpus only in scanning; DICES's sample is its
    whole pool. A pick takes items by six rules (random across groups · open pools · neighbours of corrections ·
    queries from the definition · 🧭 · diversity), each item naming its rule. Ⓔ draws it. Step 1 · LABEL labels
    the development sample, not every item (refines D22).
s42-D31 · (updated by D57: V3 proposed) Design versions are drawn side by side, linked by dashed arrows (JL 261014: "we can propose different versions
    of design, you can add them to the new frame and use ---> to link"): Ⓕ shows four ways to run the rounds as the
    corpus grows: V1 label everything · V2 development sample + search rules (proposed) · V3 growing sample · V4
    search only, each with how, cost, fit and risk. The version is chosen in the Contract.
s42-D32 · Ⓒ and Ⓓ are one frame (JL 261014: "these two can be merged together"): the round's seven Steps as a loop,
    then the Task's Stages and Steps as a tree table under it.
s42-D33 · The method frames sit left of ① (JL 261014: "we can put these method things to the left"): Ⓐ, under it Ⓒ,
    under that Ⓔ - - -▶ Ⓕ, right-aligned past the act names; Ⓑ stays right of ①, the screens below ①. Updates D27.
s42-D34 · (updated by D64: Sign (G_1)) The Handoff's Sign names what it signs, "✍ Sign (G*)", as Stage 2's says "Sign (G0)" (JL 261014: "for the
    last Sign, could we say Sign(G*)"); in the map, the ledger and the tree.
s42-D35 · (updated: six lanes; ⑥ is a screen) ① gains a fifth lane, the corpus, and every box its input above and its output below (JL 261014: "we should
    have the column for the corpus as well ... what is the input and output for each box ... before and below the
    box"). The corpus lane says what the corpus holds after each row (dashed: a state, not an actor). With the in and
    out lines ① is past a map's 200 words, so it is marked a detail frame read down (⑥ measures it). Updates D07.
s42-D36 · (updated by D41, D64) Stage 2 runs in passes (JL 261014: "we can have multiple rounds of asking and discussions"): the agent
    asks, you read a few items and write notes, it drafts the definition; another pass until you Sign (G0), still at
    most 30 items read. Drawn as a loop in ①, lines 3-4 of Algorithm 1, the ledger and the tree.
s42-D37 · (updated by D52: panel E) ①'s lanes, left to right: corpus, agent, labeling agent, small open model, you (JL 261014: "put them in
    the middle and you in the right most, and the corpus to the leftmost"): the two models in the middle, the person's
    gates on the right, the corpus they all read on the left. Updates D35.
s42-D38 · (updated by D64: Sign (G_1)) LABEL's two ways in are named (JL 261014: "the left one can be a updated G* as well, is that so?"): from
    above, the first round, G_1 from Sign (G0); from the left, every later round, G_t+1 from your accepted rules. Not
    G*: G* is only the last G_t, named when you Stop and Sign the Handoff.
s42-D39 · ① shows what changes over time, beside who acts (JL 261014: "should we have G_t+1 to G_t ... show how the
    corpus and guideline and the corpus pool is changed along the time"): two state lanes on the left, 📚 corpus (sealed,
    read, U, the 7 pools, gold) and 📜 guideline (G_0 → G_1 → G_t → G_t+1 drafted → G_t ← G_t+1 at CLOSE → G*), each
    joined down by a thin arrow; the round's loop says t ← t+1. Updates D35, D37, D38.
s42-D40 · (superseded by D59, D61) Each timeline change is the out of a box in its row (JL 261014: "will these also shown in the process box
    above and below?"): import leaves 🔒 50 · pool 300, LABEL leaves U's labels, SORT the 7 pools, JUDGE + gold, LEARN
    G_t+1 drafted, CLOSE G_t ← G_t+1, freeze G* · D*; the in lines name what the box reads (U · G_t, gold · G_t).
s42-D41 · (updated by D59) ① and Ⓐ name sizes by symbol, not number (JL 261014: "change the number from the specific number to the
    symbol"): n = |X| the items, m = |S| the sealed final exam, r the talk's most items read, b a round's picks; DICES's
    350 · 50 · 30 stay only in Ⓑ, whose bars draw an example.
s42-D42 · In the corpus and guideline lanes, one box holds the round's rows, named "round t" (JL 261014, drawn on the
    canvas: "could we add this to indicate this is the box?"): what changes inside it changes every round.
s42-D43 · (updated by D64: K) The agent has a reading budget per step (JL 261014: "agent can see at most N numbers of items ... we might
    have different types of N, please label them carefully"): c_ask a talk pass, c_pick a PICK, c_learn a LEARN; SORT,
    MEASURE, CLOSE and freeze read no text (👁 0); each labeler sees one item a call. N stays the talk's set, so the
    budgets get their own letters; ① ends with a symbols table (n m u r b c_•), Ⓐ's notation and Ⓔ's guards say it.
s42-D44 · The screens ②–⑪ follow ① (JL 261014: "update the UI based on this", screens first): sizes as symbols (n m r
    b), each step's 👁 budget, Stage 2 a pass k with Sign · Another pass, a round's screens titled by its Step (PICK,
    JUDGE, LEARN, CLOSE) with a Now card (corpus, pools, G_t), both labelers' label + region, CLOSE showing G_t ← G_t+1.
s42-D45 · (updated by D58: blind) JUDGE shows each picked item on the 3-D map (JL 261014: "for this show them, we can use the 3d embeddings as
    well"): the item ringed among its nearest neighbours, coloured by your gold so far, rotatable, hover for text (the
    items Task's 📍 Map, s41-D19); you see what it sits beside before you rule it.
s42-D46 · (updated by D60: audit + hunt arms) PICK is a funnel over the whole corpus (JL 261014: "how could we select the most valuable new data to review
    ... from the large corpus"; "what is the final score here?"): ① seed by the six rules (rule 1 now a random audit of
    the settled pools), ② retrieve neighbours over X∖S (👁 0), ③ score by the small model, v(x) = unsure · dense^β · new
    · (1 + γ·near) (information density, after Settles & Craven 2008), ④ the agent reads the top c_pick and picks b, one
    per cluster. b is split across pools by expected error mass; Stop when each pool's is under ε. Picks join U.
s42-D47 · (superseded by D48, D49) The novelty box states the paper's three contributions (JL 261014: "our main contribution is ... the
    researcher can propose their subjective labeling ... second ... it is easy to use, so that's why we have the UI
    ... a user and agent talk with the corpus ... the third one is it will be quick ... guideline and labeling at the
    same time"): C1 your own subjective label (✨1), C2 easy to use (✨2), C3 quick (✨3), kept honest by ✨4.
s42-D48 · (Stop clause superseded by D63) The contributions are what the person and others get (JL 261014: "a guideline like people are confident
    with and they can also give the good performance even for some like a weak LM"; "we are trying to build a very
    good benchmark and we can use it to apply to others"): C1 a guideline you are confident in, C2 a guideline that
    transfers (a weak model following G* labels like you, measured on S), C3 a benchmark anyone builds quickly
    with measured confidence. Stop also reads whether the weak model still gains. Updates D47.
s42-D49 · The work is framed as a tool for researchers to build their own benchmark (JL 261014: "this is a tool for
    the researcher to build their own benchmark"), and C3 is a benchmark that knows where it is unsure: every item
    keeps its region (H, L, N or a border), so an algorithm is scored on settled and border items apart. Updates D48.
s42-D50 · (updated by D59: S_sel, S_rep) The tool ends by picking the labeler (JL 261014: "and then select the most suitable tools for them to
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
s42-D53 · (updated by D60: corpus X∖(S∪K∪U)) One retrieval tool, find_neighbours(seed, k, corpus, rank_by), first named neighbor_rank (JL 261014: "what if we want the neighbours with
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
    ref/guideline-format.md and haipipe-labeling-building § The register; drawn in Ⓖ.
s42-D56 · Both labelers are one tool, lm_labeler(items, guideline, engine) (JL 261014: "what I see the things here
    are the labelers, right? ... a tool like lm_labeler(item_list, guideline, engine = xxx) ... the engine could be many
    things"): the labeling agent is one engine, each open model in E another; each call returns label, region,
    confidence and reason, sealed. Built on engine/label.py, which already has claude_sdk, codex and openai_api.
s42-D55 · (updated: the map's calls) Each agent box in ① is the call it makes (JL 261014: "for the next data extraction ... I want things like
    lm_labeler(U, G_t) ... show that in each step, how do we get the new data from the large corpus"): seal(X, m),
    get(sample(X∖S)), draft(notes), lm_labeler(U, G_t), sort_pools(A_t, P_t, 🧭), find_neighbours(pools), show(picks,
    📍), learn(D, G_t), measure · close, freeze(G_t, D), lm_labeler(X, G*); its in line names where the data comes from.
s42-D57 · New data enters U every round (JL 261014: "from the current round to the next round, we might need to get the
    new data ... this is very important"): EXTEND adds the picks and the neighbours of each new rule's evidence (U_hunt)
    and a fresh random slice (U_rand); pool sizes, error rates and Stop are estimated from U_rand and the audits only, so
    hunting never biases a count. V3 is the proposed version; DICES runs V1 (U is the whole pool).
s42-D58 · JUDGE is blind (the three reviewers, 261014: the person saw the readers' labels and gold-coloured neighbours
    before ruling, which anchors gold and inflates C2): the item and an unlabeled map; your label and region, locked;
    then the readers' labels and gold neighbours show; your final is gold, your first is kept. You still read only the
    picks. Decided by the agent on the reviewers' evidence (the law's show → first record → lock → reveal); updates D12.
s42-D59 · The final exam S is split and you label it blind once, in Stage 4 (reviewers: one ~50-item S both picked and
    scored the labeler): S_sel picks the labeler, S_rep reports its score with a confidence interval; you label all of
    S after Stop, before Sign (G*), blind to every reader; G* is yours to consult. DICES: m = 100 (50 + 50) needs a
    test-reserve Run to seal 50 more; one model family e_out is held out of E and scored only on S. Resolves Open 5.
s42-D60 · A round's pick has two arms (reviewers: error rates from hunted picks are biased): an audit, random in every
    pool with π recorded, and a hunt, find_neighbours over X∖(S∪K∪U) from seeds 1-4; round 1 is random only (the law;
    no gold yet). The card names both arms, its seed and its forecast, so it is the law's card.
s42-D61 · sort_pools is one rule (reviewers: HLN had two meanings, "sure" no threshold): an item is in H, L or N when
    every reader gives that label with confidence ≥ τ (τ set on gold); otherwise its border is the set of labels the
    readers gave (HL, LN, HN, HLN). A reader's own region is kept as a feature, never the pool.
s42-D62 · The picks are labeled before JUDGE (reviewers: picks from outside U had no labels): Step 2 runs lm_labeler on
    the picks with the agent and each model in E, sealed before the person's first record.
s42-D63 · U is relabeled under G_t+1 before the round closes, and there is one Stop rule (reviewers: G* had never been
    run on U; Stop had four wordings): MEASURE relabels U with every reader, re-sorts, bounds each pool's error mass
    (π-weighted, Horvitz-Thompson, upper 95%); Stop when a round changed no rule and every bound < ε, or you accept an
    open pool as a limitation. G* = the last G_t, already run. Each reader is scored on gold no rule used.
s42-D64 · Names that clashed are split (reviewers): the talk set is K (N stays the none pool); your notes are M; the
    gates are Sign (G_1) and Sign (G*); B is a round's picks; T each item's pool. The duplicate D54 is now D56.
s42-D65 · The hunt searches X∖(S∪K∪D), U included, and the audit draws only from U_rand (the four reviewers,
    261015: the border items sit inside U, and on DICES U is the whole pool, so X∖(S∪K∪U) was empty): EXTEND then adds
    only new picks; pool sizes come from U_rand weighted by 1/π, so they describe X∖(S∪K). Updates D57, D60.
s42-D66 · Stop is measurable (reviewers: with 2-6 audit items a pool, a bound on a rate never closes): error is the
    readers' majority against your blind first record; a pool's error mass is its size × rate, from this round's
    U_rand audit, as a share of X, so a tiny pool carries a tiny mass; ε and b_audit are set together in the Contract;
    τ is set on round 1's audit, then frozen; the accept-as-limitation exit also needs a round with no rule change.
    Updates D63.
s42-D67 · The card shows counts only, and JUDGE is shuffled (reviewers: a pick's pool tells its readers' verdict):
    you approve counts per arm and pool; each pick's arm and pool stay hidden until Lock. Updates D58, D60.
s42-D68 · Gold is never rewritten (reviewers; the law): JUDGE writes records, CLOSE promotes them; LEARN reads this
    round's records with Ŷ; a patch that conflicts with earlier gold flags it, and the item is re-ruled blind as a
    new event, the old record kept.
s42-D69 · S goes through the custodian (the law: building never writes T* gold): you label S in final-exam-label, the
    Test Custodian's Run, through its one logged door; scanning reads S the same way. The metric that picks e* is set
    in the Contract: macro-F1 and quadratic κ over the three labels. The labeling agent is a candidate on S too.
s42-D70 · Names (reviewers): Ŷ the readers' labels on the picks, P the pools (T only counts rounds), U_rand drawn by
    its own box after Sign (G_1), outside the pass loop; e*, e_out and τ join the symbols; the claim reads "you read
    only the picks".
s42-D14 · (updated: Haiku → panel E, D52) Ⓒ is the ledger, Run by Run: who acts (agent, labeling agent, you, Haiku) and what changes (corpus, guideline,
    labels) (JL 261014: "columns ... the agent, subagent of labeling, the human, the small model, the corpus, the
    guideline and the labels, and each row is a Run").
s42-D08 · Ⓐ writes the same workflow as a paper's Method would (JL 261014: "if we are going to write the ACL paper
    ... how do we write the method ... a new frame to describe the workflow with the algorithm box"): Algorithm 1 in
    pseudocode, each human gate a comment beside its line, and the Method's sections mapped to its lines.
s42-D07 · (updated: six lanes, D35, D39) ① is a workflow map, the main frame: one row per moment, three lanes (the agent, you, the small models), the
    round loop drawn closed; the screens below explain it (JL 261014: "we also need to make a workflow mindmap").


Open
----

1. ~~Should the items Task log which items a person opened~~: the corpus tools log every item shown (D30); the
   items Task's own views (Draw again, the map) should log through the same door.
2. ~~The review lives in the chat~~: JUDGE is blind and runs on the workbench's screen ⑦ (D58).
3. The novelty claims ✨1-✨3 are not yet checked against related work (LLM-assisted annotation, rubric or
   constitution refinement, perspectivist labeling, active learning).

4. The building law and engine still need the blind JUDGE gate (D58, D67) and the custodian's door for S (D69); a new Run
   type `agent-label` and the review-only gate are needed there before s42 can be built.
5. ~~Who labels S, and when~~: you, blind, once, in Stage 4 (D59).
6. The law needs three amendments before building: relabeling gold items each round for regression (Law 2, seal before
   sight), EXTEND and the relabel as Runs (sample-extend, pool-sort), and final-exam-label in Stage 4.
7. Values still to set, in the Contract: τ (sure), ε (the bound), the audit's share of b, β and γ in v(x).
8. The paper's baselines: a codebook written first (by another researcher, or G_1 frozen); a second reader labels S
   from G* alone, and a repeat subset of S measures your own consistency; G_1 vs G* on a weak model; e_out; the funnel vs random picks; do the
   border pools predict DICES's own rater disagreement.
9. The code lags the design: budgets from the config with r, find_neighbours excluding K, D and U, the parser checking
   that a region holds its label, sealed round-scoped outputs, the cheatsheet as the labelers' prompt.
10. Agree its **For:** line and **Delivery type:** (skill), proposed by the agent 261030?

(write here, or mark the drawing in red)
