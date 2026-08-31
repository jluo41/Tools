## 0.9.2 — 2026-08-21

## 0.9.3 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).


- §🪪's `bank:` row now names what its four words ARE: the cost tier under
  another name (`haipipe-probe` §💰, R13 restored 260821) — reuse is T2, run and
  code are T3, new is T4, and a card that closed at T0/T1 carries no `bank:`.
  No field added, no value renamed; the two vocabularies just stopped competing.

## 0.9.1 — 2026-08-21

- §✍️ cited "`haipipe-probe`'s entry record, §`state`" as the vocabulary's home.
  That section does not exist, and the list the reader would have found instead
  was missing `answered-local` — so this plugin was the de-facto source for a
  word it claimed to be borrowing. Now points at §🧾 Return contract, and
  `haipipe-probe` 0.17.0 carries all eight states.

## 0.8.1 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.
- Coherence pass, same law: §✍️ names the phase split (PROBE runs ① ② ③,
  EVIDENCE runs ④ ⑤) instead of crediting the whole loop to EVIDENCE; §↩
  legalizes the fold-appended forward id — the plan is authored bare, the ①
  fold writes `📮 PP<NN>` into the bullet once the card serves it, `serves:`
  stays the live join; and the retired ladder word "bound" in the satisfaction
  rule and the ↩ tag now reads "answered".

## 0.8.0 — 2026-08-19

- **A `bank: code` value is RECOMPUTED by machine.** JL 260819: "I think the
  machine should check these numbers." `checks/values.py` re-runs each value's own
  recipe against the repo and compares it to what the card quotes.
- This splits what `read: ✅` means: not "I checked the arithmetic" but "I agree
  with the judgment inside the question". Counting contract folders is mechanical;
  whether COMPILE counts as a phase is not.
- It earned itself on the first run: `PP03.v2` quoted 17 cards at `planned`, true
  when written and 13 four cards later. A person re-reading by eye does not catch
  that, because the page still looks right.
- A value with no recipe reports `unchecked`, never as passing.

## 0.7.0 — 2026-08-19

- **`PP<NN>.v<n>` · one card, many values.** A card is one question whose answer
  usually holds several numbers, and a sentence uses one of them, so citing the
  card alone could not say which (JL 260819). The id is allocated at EVIDENCE in
  a `## Values` block in `card.md`: one line per value with what it is, the
  number, and the exact place in `proof/` it was read from.
- **No `value/` folder and no `haipipe-plugin-value`.** The number already lives
  in `proof/` with its source, run and sha256; a second home for it is the rule
  that retired 🧮 proof the same day. What was missing was one more level of
  ADDRESS, which the grammar already does elsewhere: `C3.P1.B4` splits a bullet
  into sentences, `PP01.v2` splits a card into values.
- Makes two failures visible: a sentence with a number and no `PP<NN>.v<n>`, and
  a card holding a value no sentence uses.

# haipipe-plugin-probe · Changelog

## 0.1.0 · 2026-08-15
- Initial draft, round 2 of the thin-door migration (JL 260815): every live QPf plugin gains its skill; delta-only over haipipe-plugin.

## 0.1.1 · 2026-08-16
- The 🚪 tab takes the display split's structure whole (JL 260816: "follow the structure of the display plugin split"): strip, chips, per-card anchors; the filling stays probe's own.
- Storage aligned to QPf9 §1: `PP<NN>-<slug>/card.md` folders, numbered per page; the flat `<id>-<slug>.md` sketch was this file's own drift.
- Upstream, JL retired `1-probes/`: a page's `probe/` is the only pool, ruled in QPf9's Law; this file already said nothing of `1-probes/` and needs no unlearning.

## 0.4.0 · 2026-08-17
- A card becomes a real FOLDER, like a display unit (JL 260817: "让 probe 也变成一个 folder，就像 display 一样"; "这个 probe 的 plugin 内容非常的干瘪").
- The stake wall becomes a PATH, not a paragraph: `consumer/` may carry stake and never crosses, `executor/` may not and all of it may cross. `haipipe-probe` LAW 2 is now grep-checkable instead of a matter of discipline.
- `answer/` renamed `proof/`, because `executor/a-executor.md` already holds the answer in words. New §🧾: the small CSV and JSON pulled verbatim out of the task folder, with `manifest.yaml` carrying `source` · `run` · `pulled` · `rows` · `sha256` · `why` · `aggregate`, and five rules (verbatim, ≤200 rows/50 KB, aggregate only for PHI, `source:` names the task-folder path, `sha256` makes staleness computable).
- The state ladder and the 🚪 strip's three counts are now checkable by FILE: `bound` requires an answered QA file, a non-empty `a-executor.md`, and a `proof/` that holds files or says why not.

## 0.5.0 · 2026-08-17
- New §🏷 **the folder name is a NOUN, and every word in it is already on disk**, with two mechanical checks: ① the slug may not contain which/what/why/how/whether/is/does, because a card ASKS and a folder NAMES; ② every word must `grep -ril` in the task folder, or be one of a short plain list (n, coef, sample, script, run, table, log, gap, commit, spec).
- The rule is written from a real failure the same day: `PP02-control-rung-ladder` shipped with two invented words in three. `rung` and `ladder` were my metaphor for progressively added controls, which the code has called `SPEC1..SPEC5` since it was written (`CODE_REVIEW.md:52`). JL: "这三个单词里面有两个我不认识". `grep -ril rung` on the task folder returns nothing; that is the check that would have stopped it.
- Also ruled: the name is short (id + 2 or 3 words), and the same rule governs the page's `###` division headings, where the identical metaphor landed as `### 4 · Control-rung ladder` (now `### 4 · SPEC1..SPEC5`).
- The four real cards on `QC1-visitlbp` were renamed under the new rule: `PP01-ols-headline-coef`, `PP02-ols-spec1-5`, `PP03-ols-sample-n`, `PP04-ols-script`.

## 0.6.0 · 2026-08-17
- Rewritten to `haipipe-plugin-display`'s shape and density (JL 260817: "我其实想让它变得跟 display 长得差不多"; "Probe Plugin 现在是 totally rubbish"). 262 lines in 9 sections became 6 sections: three passages narrating what 0.3.0 got wrong are gone, and the chain diagram that appeared in both §🧾 and §🔗 appears once.
- **New §📎 Citation**, the section display has had since 0.2.0 and this file never had: a page's prose cites a card by id and never restates a field the card owns; the `[Q-<Sec>-<n>]` bracket is the join key `src/dialect_paper.py` resolves at build time; and the ⬜ gap is stated plainly, that a board page has no equivalent chip yet and a backticked id quotes rather than chips.
- **The state ladder was invented and is now adopted.** `raised | working | bound | concern` were this file's own words; `haipipe-probe`'s entry record already defines `planned | commissioned | answered | read | answered-local | deferred | failed | concern`. The plugin now adopts that list verbatim and adds only the DISK TEST beside each word.
- **`read:` is the done state** (JL 260817: "有没有一个状态也可以说一下这个 probe 的状态，做完了还是没做完"). `answered` is the machine's finish, `read` is the page's: a person read `a-executor.md`, wrote the A-consumer into the prose, and ticked. Only a person may tick it, and a changed `target` or a re-pulled `proof/` drops the tick — the same binding rule as a display unit's `accepted:`.
- The 🚪 strip reports four counts computed from disk (planned · commissioned · answered · read), its one-line verdict is the `read` count, and every card that is not `read` shows a 🕳 notice naming the FIRST missing step, mirroring display's no-render notice.
- Recorded the `live/plugview.py` gap: its `_STATE_BADGE` map keys on `raised`/`working`/`bound`, three words absent from the protocol's state list.
- §🧾 gains the STRUCTURE decisions, not just the rules (JL 260817: "我要的是你怎么 design 这个 structure"): Ⓐ flat, because a card holds one to three files and `tables/ logs/` would leave two of three empty; Ⓑ the filename is the source's filename unchanged, so `ls proof/` and `source:` match at a glance, with a run prefix only on collision; Ⓒ `versions/<YYMMDD>/` holds the whole folder, because a rerun moves several numbers together. Three kinds land there and nothing else: 📊 table `.csv`, 🔢 numbers `.json`, 📄 excerpt `.txt`; never a whole log, a `.dta`, a row-level record or an id.
- `manifest.yaml` gains `kind:` and `bytes:`, and `files: []` splits into two forms that are not the same thing: `pending:` (not answered yet, normal on a `planned` card) and `why_empty:` (answered, and there was never a file).
- New `ref/check-probe.py`, so the contract is enforced rather than described. Its first run on `QC1-visitlbp` found two stake-wall leaks that had been there since the migration: every `q-executor.md` carried its own PP id in its title, and one dispatched question referenced another card by id.
- New §🪪 `card.md`: the field table. Which keys exist (`state` `read` `serves` `question` `route` `bank` `dispatch` `target`), when each becomes required, and what values it may take. A field the table does not list does not exist. Recorded that `binding:` is the legacy name of `bank:` and that a head carrying prose there has no verdict word, so ② MATCH cannot be checked as done.
- New `ref/template/`: `card.md`, `consumer/q-consumer.md`, `executor/q-executor.md`, `proof/manifest.yaml`. Copy the folder to raise a card; the executor template carries the forbidden-id list inline.
- The stake regex now counts BOARD PAGE IDS as stake (`Q[A-Z]\d+`, `CD\d\d`, `C\d.P\d.B\d`), not only PP numbers. It immediately found two dispatched questions pointing the bank at `QB3` and `QC1`, ids the bank has never seen and cannot resolve.
- Applied to every `probe/` on both CMS boards: 8 cards over 3 pages (`QC1-lbp`, `QC2-cancer`, `QC1-visitlbp`) migrated from the flat `card.md` to the folder shape, all `state: raised` rewritten to the protocol's `planned`, and every card now carries `read:` and a `proof/manifest.yaml`. The checker passes on all three.
- §🚪 corrected: the proof step shows THE FILE'S CONTENT, not a file list. The 0.6.0 contract said "file list · rows · source run", the surface was built to match, and JL's verdict on it was "我也看不到你这个 file 的内容啊". A `.csv` now draws as a real table (esttab's `="…"` armour stripped, the comma inside a quoted `771,449` kept), `.json` and `.txt` come out in a `<pre>`, and `source`/`pulled`/`sha256` fold under `▸ provenance`.
- `live/plugview.py` is current with this contract: `plug_probe` reads the folder in wall order, computes the four counts from disk, prints the 🕳 first-missing-step notice, and renders each proof file (`_render_proof_file`, `_csv_cells`, `_proof_block`). Also fixed there: a folded yaml scalar (`why: >-`) printed the literal `>-`, found by reading the rendered tab rather than the parser.
- New `ref/pull-proof.py`: one run copies the file into `proof/` AND writes its manifest block, so `sha256`/`rows`/`bytes` describe the bytes that landed. Until now the pull was `cp` plus a hand-typed hash (JL 260817: "是复制过来的，还是怎么过来的？"), which proves nothing. It refuses on the size ceiling, on a same-name different-bytes collision without `--replace`, and on a kind it cannot infer; `--replace` first moves the whole `proof/` into `versions/<YYMMDD>/`. Re-pulling PP02 through it reproduced the hand-written hash exactly.
- Surface readability (JL 260817: "file 的名字、folder 的名字非常窄…不好看"): the card head is now a state badge, a `PP<NN>` chip and the slug's words as a real title in the UI face, not one cramped monospace run; a proof file's name sits on its own line and its facts (kind · rows · bytes · from run) became small chips, with `why:` in body type below.
- Two display bugs found by reading the rendered tab rather than the code: a fenced ``` block in `a-executor.md` was passed through the inline reader, so `15.3332***` rendered as `15.3332*` — the significance stars were being eaten by the bold rule; and a folded yaml scalar printed the literal `>-`. Both fixed; fenced blocks are now verbatim.
- **Proof files are EMBEDDED, not re-rendered** (JL 260817: "我想让他们把这些 file 以内嵌的方式放进来，而不是直接变成 HTML"). A `.pdf` is framed with `<object>` exactly as a display unit frames `preview.pdf`; everything else with `<iframe>` plus a link to open it alone. This is a correctness decision, not a look: all three proof bugs so far came from parsing (`15.3332***` losing its stars, a folded scalar printing `>-`, esttab's `="…"` armour), and an embedded file has nothing left to parse. The csv→HTML table renderer and its CSS are deleted.
- `cli/serve.py` gains a `guess_type` override mapping `.csv .tsv .log .do .yaml` to `text/plain`, because under `text/csv` some browsers offer a download and the embedded frame comes up blank.
- **The card now follows the display unit's shape** (JL 260817: "让这个 layout 跟 display layout 长得像一些"): head fields as README-style `key: value` rows → the framed exhibit → one `ready`/`pending` next-step line → the folder tree in a `<pre>` → and only then the wall (asked · came back · audit, folded). The folder tree is display's own move and probe had lost it.
- **Every wall step is its own PANEL, every proof file its own FIGURE** (JL 260817: "每一个 file 是不是应该分开一些？现在看着乱糟糟的"). A panel carries a header strip naming the step and the file it reads, so a card can be scanned rather than read; 🔢 proof is the LEAD panel and takes a heavier border; 🗂 audit and 📂 files are folded. The head fields became a definition grid and the next-step line an amber/green bar, so the card's three registers (what was asked, what is owed, what is on disk) are visually separate.
