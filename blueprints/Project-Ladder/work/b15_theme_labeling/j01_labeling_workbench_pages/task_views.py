"""Each labeling Task view drawn from its step slide (the Subjective Labeling deck, version 12, in
s03-agent-role/delivery/deck; JL 261101: "you should read the steps here, in this slides, and then you think how do
design it"). One method for every view:

1. its step slide (deck pages 7 to 15, by file: build/v12/slide-N.png) is the frame: In → who works → Out, your part, next;
2. its close-up screen (pages 16 to 23), when the deck has one, draws the Results;
3. COVER lists every box and arrow of the slide and where it lands on the screen; check() fails when a place is
   missing, so a box cannot be dropped silently.

The two loops (JL 261101: "loop within the meaning loop and expression loop, and loop from expression to the
meaning"): 🧭 meaning runs Loop 1, 2, 3 (JL 261101: "Loop 1, Step 1 report"), each making m01, m02, m03: the agent writes
the loop's interaction report with /haipipe-labeling-interaction (a /haipipe-interaction collect Run), you answer it,
Update applies it. 🛠 expression runs rounds e01, e02 under one approved meaning (Rewrite → Run → Evaluate), and its
round report sends expression back to meaning. Only the meaning Task asks you ("we hope that the interaction is only
available in the meaning loop task"); elsewhere your part is a prompt to copy, a sign gate, or none. Each strip shows
the loop.

Each view: an optional strip, then ⚙️ Process (the slide's flow and your part) and 📊 Results (its Out in detail), each
group numbered from 1, then next. Report shows the Results only. Item text never appears; names are the public
DICES-350 dataset's or placeholders in angle brackets; the case texts are the deck's own synthetic ones.
"""
import re

# a section: (title, kind, *args). kinds: big(words, state) · kv(rows, verbs) · tiles(items) · table(head, rows, verbs)
# · bars(caption, bars) · chain(steps, verb) · tabs(items, detail) · line(words) · picture(name, verbs)
# · rows(rows, foot) · strip(words) · agent(items) · card(question, cases, options, verbs) · compare(...) · checklist(...)
# · callout(title, words, verb) · flow(in, who, out) · ask(words, verb, mode) · turns(label, turns)
# · prompt(title, lines, fields): added by view() from PROMPT, never written in STEP
H, L_, N = "high", "low", "none"
def m_turns(now, *after):
    """🧭 meaning's loops as this view sees them (JL 261101: "Loop 1, Step 1 report"): Loop 1 and Loop 2 made m01 and
    m02, Loop 3 at this view's moment, then what follows."""
    return ("", "turns", "🧭 meaning loops", [("Loop 1", "made m01"), ("Loop 2", "made m02"), ("Loop 3", now, "now"), *after])


def x_turns(now, *after):
    """🛠 expression's rounds under one approved meaning (m02): e01 done, e02 at this view's moment."""
    return ("", "turns", "🛠 rounds under m02", [("e01", "wording issue"), ("e02", now, "now"), *after])


CARDS = [("Q1 · Does a safe refusal count as none? · e02", "Needs your judgment", "Open"),     # · e02: the round
         ("Q2 · Is L04's reference label wrong? · e02", "Draft saved", "Open"),                 # report that sent it
         ("Q3 · Does a rude refusal count as low? · e02", "More evidence requested", "Open")]   # (simulation 261101)

STEP = {
    # ── 📦 items · step 0 (page 7): the corpus becomes items the human and executors judge ──────────────────────────
    "A1": [("1 · 📥 Read the raw file", "flow", ("Raw corpus", "diverse_safety_adversarial", "_dialog_350.csv"),
            ("🤖 Agent", "read and describe the table", "r05_raw_read"), ("Table card", "43,050 rows × 41 columns", "")),
           ("2 · 📊 Basic description", "tiles", [("43,050", "rows"), ("41", "columns"), ("350", "chats"), ("123", "raters")]),
           ("3 · 🎲 Random samples", "table", ("chat", "rater", "turn", "answer"),
            [("<chat id>", "<rater>", "<turn>", "<answer>")] * 3, ("Draw again",)),
           ("4 · ⚠️ Watch out", "line", "duplicate rows, and the answer columns labeling must never read")],
    "A2": [("1 · 🛠 Make the items", "flow", ("Raw corpus", "43,050 rows · 350 chats", ""),
            ("🤖 Agent + itemization tools", "build and validate the recipe", "r04_main_text_rebuild"),
            ("350 annotation items", "id · target · context · source", "")),
           ("", "ask", "✅ you confirmed the target and its context: the recipe items_transform.py is signed", "", "done"),
           ("2 · 🎲 Random items", "table", ("item", "before", "judged", "after"),
            [("<item id>", "<earlier turns>", "<the AI's last reply>", "none")] * 3, ("Draw again",)),
           ("3 · ✅ Check items", "tiles", [("350", "unique ids"), ("3", "turns before, median"), ("0", "duplicates")])],
    "A3": [("1 · 🗺 Embed the items", "flow", ("Annotation items", "350 items", ""), ("🤖 Agent", "embed with minilm", "r06_embedding_minilm"),
            ("Corpus map", "items placed by meaning", "")),
           ("", "ask", "✍️ Your sign: agree the map before cases are drawn from it", "Agree", "gate"),
           ("2 · 📍 The map", "picture", "every item placed by meaning, coloured by group", ("Open map",)),
           ("3 · 🧩 Groups", "tiles", [("group 1", "<size>"), ("group 2", "<size>"), ("group 3", "<size>"), ("group 4", "<size>")])],
    "A4": [("1 · ✂️ Split related items together", "flow", ("Annotation items", "one chat = one source group", ""),
            ("🤖 Agent", "split by source group", "r07_split_by_chat"), ("Train · Test", "Train <n> · Test <n>", "")),
           ("2 · 📊 The two roles", "tiles", [("Train · <n>", "expression development"), ("Test · <n>", "staging check, audited")]),
           ("3 · 🔒 Who reads what", "table", ("set", "the rewriting", "the auditor", "you"),
            [("Train", "yes", "yes", "yes"), ("Test", "never", "yes", "yes")], ())],
    # ── 📏 ground truth: the dataset's own labels, kept apart ─────────────────────────────────────────────────────
    "B": [("1 · 📏 Keep the dataset's labels apart", "flow", ("DICES-350 answer keys", "experts' gold · raters' votes", ""),
           ("🤖 Agent", "copy and fence them", ""), ("Fenced labels", "only the score Task reads them", "")),
          ("2 · 🗝 Answer keys", "tiles", [("experts' gold", "one key per chat"), ("raters' votes", "123 per chat")]),
          ("3 · 📊 How the raters split", "bars", "share of raters saying unsafe, per chat", [("0-25%", 9), ("25-50%", 5), ("50-75%", 3), ("75%+", 2)])],
    # ── 🧭 meaning · steps 1 to 4 (pages 8 to 11, close-ups 16 to 19): the only Task that asks you ─────────────────
    "C1": [("1 · 🎯 Frame the labeling task", "flow", ("Rough idea + prepared items", "goals · use cases · constraints", "items, context, old labels"),
            ("🤖 Agent", "inspect items; surface assumptions", "r01_collect_frame"),
            ("Initial task agreement", "purpose · target population", "provisional labels")),
           ("1 · 📜 Initial task agreement", "big", "How unsafe is the AI's last reply: high, low or none?",
            "agreed as frame f01 · labels provisional"),
           ("2 · ❓ What you confirmed", "kv", [("What to judge", "how unsafe the AI's last reply is"),
                                              ("Old or new", "a new standard, from my own judgment"),
                                              ("Context", "the earlier turns of each chat")], ())],
    "C2": [m_turns("report ready"),
           ("1 · 🔍 Prepare interaction report-03", "flow", ("Human sources + reports", "ideas · notes · decisions",
                                                           "round report e02 · cases"),
            ("🤖 Alignment Agent", "/haipipe-labeling-interaction", "r06_collect_report_m03"),
            ("Interaction report-03", "cards with evidence", "for you to decide")),
           # the rules first (JL 261101 on its mind map: "could you put them to the top?"): the report and its cases
           # ask about them, each card's Q tag on the rule it questions
           ("1 · 🧠 Guideline rules, as a mind map", "mindmap", ("m01", "m02"), "m02",
            ("Response safety:", "how unsafe is the reply?"),
            [("high", ["helps cause serious harm", "encourages self-harm"]),
             ("low", [("risky advice, with a warning", "Q2"), ("rude or dismissive tone", "Q3")]),
             ("none", [("safe refusal", "Q1"), "harmless reply"])]),
           ("2 · 🙋 Interaction report", "rows", [("Loop 3 · report-03", "waiting for you", "Answer"),
                                                ("Loop 2 · report-02", "Answered", "Open"),
                                                ("Loop 1 · report-01", "Answered", "Open")],
            "each card: question + evidence · rule + label · alternatives · difficulty"),
           ("3 · 📌 Typical cases", "table", ("item", "set", "current label", "card"),
            [("L01 · refusal + hotline", "Train", "none", "Q1"), ("L05 · harmful method", "Train", "high", ""),
             ("L06 · harmless reply", "Train", "none", "")], ()),
           ("4 · ⚠️ Hard cases", "table", ("item", "set", "current label", "card"),
            [("L04 · risky, with warning", "Train", "low · uncertain", "Q2"), ("L03 · rude refusal", "Test", "none · uncertain", "Q3")], ()),
           ("5 · 🎲 Random cases", "table", ("item", "set", "current label", "card"),
            [("<item>", "Train", "low", ""), ("<item>", "Test", "none", "")], ())],
    "C3": [m_turns("waiting for you"),
           ("1 · 🙋 Collect preferences", "flow", ("Interaction report-03", "earlier decisions", "evidence beside each card"),
            ("🙋 You", "confirm · clarify · revise · defer", "r06_collect_report_m03"),
            ("Decision record", "preference · reason", "scope · version")),
           ("", "ask", "🙋 Interaction · Loop 3 · report-03 waits for your answers", "", "interaction"),
           ("2 · 📦 Decision card", "card", "Q1 · Does a safe refusal count as none?",
            [("Case A", "I can't help with that, but here is a hotline."), ("Case B", "I won't answer that.")],
            ["A  Both count as none", "B  Only a refusal that offers help counts as none", "C  Use a separate refusal label",
             "None of these: write my own rule", "Defer: show more evidence"]),
           ("3 · 🗒 Loop 3's cards", "rows", CARDS)],
    "C4": [m_turns("made m03", ("Loop 4", "opens next")),
           ("1 · 🔁 Integrate feedback and check alignment", "flow",
            ("Your answers", "r06's answer_collection.md", "+ earlier decisions and rules"),
            ("🤖 Alignment Agent", "reconcile; apply approved changes", "r07_update_m03"),
            ("Guideline m03", "rules as a mind map", "+ reference labels l03")),
           # your sign (JL 261101, r01_collect_task_work_views Q6 A): expression never runs on a meaning you have not seen
           ("", "ask", "✍️ Your sign: approve m03 and l03; expression starts only after it", "Approve m03", "gate"),
           # the guideline Update made, on top as in Report (JL 261101: "could you put them to the top?"); each Q tag
           # on the rule its answer set
           ("1 · 🧠 Guideline rules, as a mind map", "mindmap", ("m01", "m02", "m03"), "m03",
            ("Response safety:", "how unsafe is the reply?"),
            [("high", ["helps cause serious harm", "encourages self-harm"]),
             ("low", [("risky advice, with a warning", "Q2"), "rude or dismissive tone"]),
             ("none", [("any refusal, with or without a hotline", "Q1"), "harmless reply"])]),
           ("2 · 📜 What your answers changed", "compare", "Q1 · A safe refusal counts as none.", "Refusals: none",
            "A refusal counts as none, with or without a hotline.", "Q3 deferred: a rude refusal goes to Loop 4.", "Review"),
           ("3 · ✅ Approved reference labels", "rows", [("L04 · Train · now low · Q2", "Needs review", "Open"),
                                                        ("L01 · Train · stays none · Q1", "Needs review", "Open")]),
           ("4 · 🧭 Where it goes", "tiles", [("ready", "after your sign: m03 + l03 → 🛠 expression"),
                                             ("open", "rude refusal → Loop 4's report")]),
           ("5 · 🧾 Meaning history", "chain", [("frame", "f01 ← r01 answers"), ("Loop 1", "m01 ← r02 answers"),
                                               ("Loop 2", "m02 ← r04 answers"), ("Loop 3", "m03 ← r06 answers")])],
    # ── 🛠 expression · steps 5 and 6 (pages 12 to 14: Step 5, the round report 12a, Step 6; close-ups 20 and 22) ────
    "D1": [("", "strip", "🔒 approved meaning m02 · fixed during rewriting"), x_turns("rewriting"),
           ("1 · ✏️ Rewrite expression", "flow", ("Approved rules m02", "Train error analysis only", ""),
            ("🤖 Execution & Audit Agent", "wording · order · examples", "r04_rewrite_m02_e02"),
            ("Expression e02", "", "")),
           ("2 · ✏️ What the wording changed", "table", ("part", "e01", "e02"),
            [("instruction", "<before>", "<after>"), ("order", "<before>", "<after>"), ("examples", "<before>", "<after>")], ())],
    "D2": [("", "strip", "🔒 approved meaning m02 · expression e02 · reference labels hidden from executors"), x_turns("running"),
           ("1 · ▶️ Run label executors", "flow", ("m02 + expression e02", "Train + Test items", ""),
            ("🤖 Label executors", "Qwen 3.5 4B · 8B · Qwen 3.8 27B", "r05_run_m02_e02"),
            ("Labels on Train and Test", "", "")),
           ("2 · ▶️ Executor runs", "table", ("model", "Train", "Test", "state"),
            [("Qwen 3.5 4B", "<n>", "<n>", "done"), ("Qwen 3.5 8B", "<n>", "<n>", "done"), ("Qwen 3.8 27B", "<n>", "<n>", "running")], ())],
    "D3": [x_turns("to meaning", ("e03", "waits for m03")),
           ("1 · 📊 Evaluate and analyze errors", "flow",
            ("Labels + reference labels", "gold/versions/l02", "hidden from the executors"),
            ("🤖 Execution & Audit Agent", "score by set; sort errors", "r06_evaluate_m02_e02"),
            ("Round report e02", "errors by kind", "and where the round goes")),
           ("1 · 📋 Round report e02", "rows", [("1 wrong label, 2 rule gaps → meaning, Loop 3", "sent to meaning", "Open in meaning")]),
           ("2 · 🔍 Errors, by kind", "tiles", [("expression issue", "3 · next wording, e03"), ("wrong label", "1 suspected"),
                                               ("rule gap", "2 found"), ("executor limit", "none")]),
           ("3 · 📊 Labeling performance", "table", ("model", "Train quality", "Test quality", "coverage"),
            [("Qwen 3.5 4B", "<q>", "<q>", "<c>"), ("Qwen 3.5 8B", "<q>", "<q>", "<c>"), ("Qwen 3.8 27B", "<q>", "<q>", "<c>")], ())],
    "D4": [("", "strip", "frozen package: rules m03 · expression e03 · reference labels l03 · model settings x02"),
           ("1 · 🔒 Freeze a version and check release readiness", "flow",
            ("Frozen package", "rules + expression", "+ labels + model settings"),
            ("🤖 Agent + evaluation tools", "review staging evidence", "and acceptance criteria"),
            ("Pass or fail", "pass: release a qualified version", "fail: expression or meaning")),
           ("", "ask", "✍️ Your sign: the release, once every criterion below is met", "Sign release", "wait"),
           ("2 · ✅ Release criteria", "checklist", [("Quality + coverage floors", "not yet"), ("Strong-model non-regression", "not yet"),
                                                   ("Cost per accepted item", "not yet")], "", ""),
           ("3 · 🧾 Fresh data for claims", "line", "claims about unseen items need data beyond the audited staging set")],
    # ── 🔍 scanning · step 7 (page 15, close-ups 21 and 23): new meaning issues go back to 🧭 meaning ───────────────
    "E1": [("1 · 🚚 Label at scale", "flow", ("Large unlabeled corpus", "release h01", "= m03 · e03 · l03 · x02"),
            ("🤖 Agent + executor", "the qualified executor", "label batches; track versions"), ("Labeled batches", "", "")),
           ("", "checklist", [("Freeze guideline and expression", "not yet"), ("Meet release criteria", "not yet"),
                              ("Review and audit policy, in h01", "not yet")], "", ""),
           ("2 · 📦 Batches", "table", ("batch", "items", "risky", "state"), [("batch 1", "<n>", "<n>", "not started")], ()),
           ("3 · 🔗 Outputs, linked", "kv", [("Guideline version", "h01"), ("Labels", "with provenance and a quality report")], ())],
    "E2": [("1 · 🔍 Review and audit", "flow", ("Labeled batches", "", ""), ("🤖 Agent", "risk cases + random samples", "for review"),
            ("Accepted labels", "with review status", "")),
           ("", "ask", "✍️ Your check: risky cases and a random sample, against m03", "Open", "gate"),
           ("2 · 📊 Audit findings", "rows", [("agree with the reference label", "<n> items", ""),
                                             ("disagree with the reference label", "<n> items", ""), ("unsure", "<n> items", "")]),
           ("3 · 🧭 New meaning issue?", "callout", "New meaning issue?",
            "1 audit issue on Test item T07 → 🧭 meaning, the next loop's report", "Open in meaning")],
    "E3": [("1 · 📦 Deliver the accepted data", "flow", ("Accepted labels", "", ""), ("🤖 Agent", "package with provenance", ""),
            ("Accepted labeled data", "guideline version", "labels + provenance + quality")),
           ("", "ask", "✍️ Your sign: accept the delivery · 1 open issue, T07, in meaning", "Sign", "wait"),
           ("2 · 🏷 Labels by value", "bars", "the corpus, by label", [(N, 220), (L_, 90), (H, 40)]),
           ("3 · 🧾 What ships with them", "line", "human-approved acceptance does not mean every item was reviewed by hand")],
    # ── 📊 score ───────────────────────────────────────────────────────────────────────────────────────────────────
    "F": [("1 · 📊 Score the final labels", "flow", ("Final labels + answer keys", "t05's labels · t02's keys", ""),
           ("🤖 Agent", "agreement, by value", ""), ("Score", "against experts · raters", "")),
          ("2 · 🎯 Agreement", "tiles", [("with the experts", "<κ>"), ("with the raters", "<κ>")]),
          ("3 · 👥 Raters' spread", "bars", "where the final labels sit among the 123 raters", [("below", 4), ("middle", 9), ("above", 4)])],
}

# every box and arrow of a step slide, and the section of the view it lands in (title words, or a kind)
COVER = {
    "C1": [("Rough idea", "Frame the labeling task"), ("Prepared corpus items", "Frame the labeling task"),
           ("Agent: inspect items; surface assumptions", "Frame the labeling task"), ("Calls tools", "Frame the labeling task"),
           ("Human confirms (3 questions)", "What you confirmed"), ("Initial task agreement", "Initial task agreement"),
           ("Next: explore cases in the Alignment Loop", "next")],
    "C2": [("Human sources", "Prepare interaction report-03"), ("Corpus + audit reports", "Prepare interaction report-03"),
           ("Alignment Agent: search · compare · group", "Prepare interaction report-03"), ("Typical cases", "Typical cases"),
           ("Hard cases", "Hard cases"), ("Random checks", "Random cases"), ("Decision report: its 4 parts", "Interaction report"),
           ("Generate this round", "Interaction report"), ("Flags are hypotheses", "prompt"), ("Next: review in Workbench", "next")],
    "C3": [("Audit issues + earlier decisions", "Collect preferences"), ("Meaning Loop Agent prepares each round", "Collect preferences"),
           ("Workbench: new preference round", "Decision card"), ("Cards 1 to 3", "Loop 3's cards"),
           ("Human: confirm · clarify · revise · defer", "Collect preferences"), ("Optional chat", "prompt"),
           ("Decision record", "Collect preferences"), ("Reconcile with earlier decisions", "prompt")],
    "C4": [("Submitted feedback", "Integrate feedback and check alignment"), ("Earlier decisions", "Integrate feedback and check alignment"),
           ("Alignment Agent: reconcile, apply", "Integrate feedback and check alignment"),
           ("Structured adaptive guideline", "Guideline rules"), ("Approved reference labels", "Approved reference labels"),
           ("Recheck affected items across both sets", "Approved reference labels"), ("Open or conflicting → next report", "Where it goes"),
           ("Ready for Execution & Audit", "Where it goes"), ("Clarify with the human", "prompt")],
    "D1": [("Approved rules stay fixed during rewriting", "strip"), ("Rewrite expression: wording · order · examples", "Rewrite expression"),
           ("Train error analysis only", "Rewrite expression")],
    "D2": [("Run label executors on Train + Test", "Run label executors"), ("Reference labels hidden from executors", "strip")],
    "D3": [("Evaluate labeling performance by set", "Labeling performance"), ("Analyze errors", "Errors, by kind"),
           ("Expression issue · wrong label · rule gap · executor limit", "Errors, by kind"),
           ("Round report → Meaning Loop Agent", "Round report e02"), ("Model disagreement is a flag", "Errors, by kind")],
    "D4": [("Frozen package", "Freeze a version and check release readiness"), ("Agent + evaluation tools", "Freeze a version and check release readiness"),
           ("Quality + coverage floors · non-regression · cost", "Release criteria"), ("Human review + reference labels", "ask"),
           ("Pass / Fail", "Freeze a version and check release readiness"), ("Fresh data for generalization claims", "Fresh data for claims")],
    "E1": [("Large unlabeled corpus", "Label at scale"), ("Agent + qualified executor", "Label at scale"),
           ("Outputs linked: guideline version · labels + provenance + quality report", "Outputs, linked")],
    "E2": [("Review + audit: risk cases + random samples", "Review and audit"), ("New meaning issue → Steps 2 to 4", "New meaning issue?")],
    "E3": [("Accepted labeled data", "Deliver the accepted data"), ("Acceptance is not hand review of every item", "What ships with them")],
}

# each agent step's prompt (JL 261101: "prepare the prompt template that the user can enter and copy to the chat
# session"): the page fills the step's real inputs, you fill the fields, Copy prompt, paste it into the Task's session.
# Your own step has one too (C3, JL 261101: "we should also have a box where we can enter the template and then we
# copy it to the chat"): it sends your answers and notes on. A prompt is you → the agent, an interaction the agent → you.
NOTES = (("your notes", "optional: what to look at first"),)
SESSION = {"A": "dices350-items", "B": "dices350-ground-truth", "C": "dices350-safety-meaning",     # each Task's chat
           "D": "dices350-safety-expression", "E": "dices350-safety-scanning", "F": "dices350-safety-score"}
PROMPT = {
    "A1": ("Data · read the raw file", [
        "Use /haipipe-labeling on t01_dices350_items, step Data: read",
        "diverse_safety_adversarial_dialog_350.csv; describe its rows, columns and what never to read."], NOTES),
    "A2": ("Items · make the items", [
        "Use /haipipe-labeling on t01_dices350_items, step Items: build the item recipe",
        "(target, context, source) and check it on 20 random items before making all 350."], NOTES),
    "A3": ("Embedding · embed the items", [
        "Use /haipipe-labeling on t01_dices350_items, step Embedding: embed every item with minilm,",
        "then draw the corpus map and name its groups."], NOTES),
    "A4": ("Split · Train and Test", [
        "Use /haipipe-labeling on t01_dices350_items, step Split: split by chat, one source group each;",
        "Test is never read by the rewriting."], NOTES),
    "B": ("Labels · fence the dataset's labels", [
        "Use /haipipe-labeling on t02_dices350_ground_truth_profile: copy the experts' gold and the",
        "raters' votes, and fence them so that only the score Task reads them."], NOTES),
    "C1": ("Frame · your rough idea", [
        "Use /haipipe-labeling on t03_dices350_response_safety_meaning, step Frame: read the items",
        "(t01_dices350_items) and the old labels' sources, surface the assumptions in my idea below,",
        "then ask me the three frame questions through /haipipe-labeling-interaction."],
        (("Goal", "flag unsafe AI replies, and how unsafe they are", True),
         ("Use cases", "screen chatbot replies before release", True), ("Constraints", "only the public DICES-350 data", True))),
    "C2": ("Report · Loop 3's interaction report", [
        "Use /haipipe-labeling-interaction on t03_dices350_response_safety_meaning, Loop 3: prepare",
        "interaction report-03 from my sources, earlier decisions and round report e02, its cases grouped",
        "typical, hard and random. Flags are hypotheses: no rule or label changes until I answer."], NOTES),
    "C3": ("Preferences · send my answers", [
        "Use /haipipe-labeling-interaction on t03_dices350_response_safety_meaning, Loop 3: save my",
        "answers to report-03 with my notes below, then start Update."],
        (("your notes", "optional: context for the decision record"),)),
    "C4": ("Update · apply my answers", [
        "Use /haipipe-labeling on t03_dices350_response_safety_meaning, step Update: read r06's",
        "answer_collection.md; write meaning m03 and labels l03, each rule naming its card; recheck",
        "affected items; anything unclear becomes a card for Loop 4, never a guess. Then wait for my sign."], NOTES),
    # one prompt runs a whole round (JL 261101, r01_collect_task_work_views Q7 A): Rewrite's; Run's and Evaluate's
    # stay, for a rerun of that step alone
    "D1": ("Rewrite · the whole round e02", [
        "Use /haipipe-labeling on t04_dices350_response_safety_expression, round e02: rewrite the wording",
        "under meaning m02 from Train errors only, run the executors, evaluate, and stop at round report e02.",
        "Change no rule and ask me nothing: rule or label questions go to the round report."], NOTES),
    "D2": ("Run · rerun the executors", [
        "To rerun this step alone (Rewrite's prompt runs the whole round): use /haipipe-labeling on",
        "t04_dices350_response_safety_expression, step Run: label Train and Test with m02 + e02 on",
        "Qwen 3.5 4B, 8B and Qwen 3.8 27B; keep the reference labels hidden."], NOTES),
    "D3": ("Evaluate · rerun round report e02", [
        "To rerun this step alone (Rewrite's prompt runs the whole round): use /haipipe-labeling on",
        "t04_dices350_response_safety_expression, step Evaluate: score by set and model, sort errors",
        "into the four kinds, and write round report e02 with its route."], NOTES),
    "D4": ("Release · check readiness", [
        "Use /haipipe-labeling on t04_dices350_response_safety_expression, step Release: freeze",
        "m03 · e03 · l03 · x02, check the floors, non-regression and cost, and report pass or fail."], NOTES),
    "E1": ("Batches · label at scale", [
        "Use /haipipe-labeling on t05_dices350_response_safety_scanning, step Batches: label the corpus",
        "in batches under release h01, each label linked to its versions."], NOTES),
    "E2": ("Audit · pick what I review", [
        "Use /haipipe-labeling on t05_dices350_response_safety_scanning, step Audit: pick the risky cases",
        "and a random sample for my review; a meaning issue goes to meaning's next Report."], NOTES),
    "E3": ("Final labels · deliver", [
        "Use /haipipe-labeling on t05_dices350_response_safety_scanning, step Final labels: package the",
        "accepted labels with their provenance and the quality report."], NOTES),
    "F": ("Agreement · score", [
        "Use /haipipe-labeling on t06_dices350_response_safety_score: score the final labels against",
        "the experts' gold and the raters' votes, by value."], NOTES),
}

CAPTION = {"A1": "the raw file, read and described", "A2": "how the raw file became items", "A3": "the items placed on a map by meaning",
           "A4": "how the items split into Train and Test", "B": "the answer keys that came with the dataset",
           "C1": "what we judge, agreed before any rule", "C2": "the rules now, then Loop 3's report and the cases it asks about",
           "C3": "report-03: your answers", "C4": "the rules your answers made, what changed, and where the loop goes",
           "D1": "the wording, rewritten under a fixed meaning", "D2": "the models labeling Train and Test",
           "D3": "how the models did, and where the round report sends it", "D4": "whether the frozen version is ready",
           "E1": "the corpus labeled in batches", "E2": "risky cases and a random sample, checked",
           "E3": "the accepted labels, and what ships with them", "F": "the final labels against the experts"}
NEXT = {"A1": "🛠 Items", "A2": "🗺 Embedding", "A3": "✂️ Split", "C1": "🔍 Report", "C2": "🙋 Preferences",
        "C4": "🛠 expression · Rewrite (m03)", "D1": "▶️ Run", "D2": "📊 Evaluate",
        "D4": "🔍 scanning · Batches", "E1": "🔍 Audit", "E2": "📦 Final labels"}


def view(key, section):
    """A view's sections in two groups, as the previous version's Operation and Result (JL 261031): ⚙️ Process is the
    step slide's flow and your part (section 1 and what follows it untitled); 📊 Results are its Out in detail. Strips and
    the loop's iterations sit above both groups. Work shows everything, then the next step; Report shows the Results only."""
    secs = STEP[key]
    n_lead = 0                                   # the version strip and the loop's iterations lead the view
    while n_lead < len(secs) and secs[n_lead][0] == "" and secs[n_lead][1] in ("strip", "turns"):
        n_lead += 1
    lead, body = secs[:n_lead], secs[n_lead:]
    k = next((i for i, s in enumerate(body[1:], 1) if s[0]), len(body))   # where the step's own cards start
    process, results = body[:k], body[k:]
    if key in PROMPT:                            # an agent step's prompt starts it, right under its flow; your own step's
        title, lines, fields = PROMPT[key]       # comes after you answer, so it sits last (Report shows no Process)
        who = process[0][3][0] if process and process[0][1] == "flow" else ""
        at = len(process) if who.startswith("🙋") else 1
        process = process[:at] + [("", "prompt", title, lines, fields, SESSION[key[0]])] + process[at:]
    if section == "report":                     # what came out: the flow's Out sits in the Results already
        keep = []
        for s in results:
            if s[1] in ("kv", "agent", "card", "checklist", "ask"):
                continue
            if s[1] == "rows":
                s = s[:2] + ([(w, st, "") for w, st, _ in s[2]],) + s[3:]
            elif s[1] in ("table", "picture"):
                s = s[:-1] + ((),)
            elif s[1] == "callout":
                s = s[:-1] + ("",)
            keep.append(s)
        return lead + [("group", "📊 Results")] + numbered(keep)
    return (lead + [("group", "⚙️ Process")] + numbered(process) + [("group", "📊 Results")] + numbered(results)
            + ([("next", NEXT[key])] if key in NEXT else []))


def numbered(secs):
    """Each group counts its own sections from 1 (JL 261101: "the index within process and results should started
    from 1, 2, 3")."""
    out, n = [], 0
    for s in secs:
        if s[0] and s[0] not in ("next", "group"):
            n += 1
            s = (re.sub(r"^\d+ · ", f"{n} · ", s[0]),) + s[1:]
        out.append(s)
    return out


def check():
    """Every slide box in COVER lands on its view: a section whose title holds the words, or a kind; only the
    🧭 meaning views carry an interaction; every step has a prompt to copy to the chat (JL 261101)."""
    problems = []
    for key, rows in COVER.items():
        secs = view(key, "work")
        titles = " | ".join(str(s[0]) for s in secs)
        kinds = {s[1] for s in secs if len(s) > 1 and isinstance(s[1], str)} | {s[0] for s in secs}
        for box, place in rows:
            if place not in titles and place not in kinds:
                problems.append(f"{key}: slide box '{box}' has no place '{place}'")
    for key, secs in STEP.items():
        for s in secs:
            if s[1] == "ask" and len(s) > 4 and s[4] == "interaction" and not key.startswith("C"):
                problems.append(f"{key}: an interaction outside the meaning Task")
            for words, size, room in fits(s):
                if wide(words, size) > room:
                    problems.append(f"{key}: '{words}' is {wide(words, size):.0f} px, its box holds {room:.0f}")
        if any(s[1] == "flow" for s in secs) and key not in PROMPT:
            problems.append(f"{key}: a step with no prompt to copy to the chat")
    for key, (title, lines, fields) in PROMPT.items():
        for words, size, room in fits(("", "prompt", title, lines, fields)):
            if wide(words, size) > room:
                problems.append(f"{key}: prompt line '{words[:40]}…' is {wide(words, size):.0f} px, its box holds {room:.0f}")
    return problems


def wide(words, size):
    """About how wide a line draws: 0.47 × the font size per letter, an emoji as two letters."""
    return sum(2 if ord(c) > 0x2500 else 1 for c in words) * 0.47 * size


def fits(s, w=640):
    """Each line a section draws inside a box, with its font size and the room the box leaves."""
    if s[1] == "flow":
        bw = (w - 2 * 34) / 3 - 14
        return [(box[0], 13, bw) for box in s[2:5]] + [(ln, 11, bw) for box in s[2:5] for ln in box[1:3] if ln]
    if s[1] == "tiles":
        tw = (w - 10 * (len(s[2]) - 1)) / len(s[2]) - 14
        return [(a, 15, tw) for a, _ in s[2]] + [(b, 10, tw) for _, b in s[2]]
    if s[1] == "rows":
        return [(r[0], 15, w - 264) for r in s[2]]
    if s[1] == "prompt":
        return [(ln, 12, w - 40) for ln in s[3]] + [(f[1], 12, w - 152) for f in s[4]]
    if s[1] == "table":
        cw = (w - 10) / len(s[2]) - 12
        return [(c, 11, cw) for c in s[2]] + [(c, 11, cw) for row in s[3] for c in row]
    if s[1] == "mindmap":
        leaves = [lf if isinstance(lf, str) else lf[0] for _, ls in s[5] for lf in ls]
        return [(ln, 12, 150) for ln in s[4]] + [(lf, 12, w - 330 - 70) for lf in leaves]
    return []


if __name__ == "__main__":
    bad = check()
    print("\n".join(bad) if bad else f"coverage ok: {sum(len(r) for r in COVER.values())} slide boxes on {len(COVER)} views")
