# Paper check

The one check before a send or a co-author round: citations and values, sorted into what the paper prints wrong and
what is only not recorded. Owner: hai-paper-evidence (`/hai-paper-check` is its alias).

## ✅ Topic: Paper check ▸ every citing sentence is read against its source

```text
BEFORE                                         AFTER
cite_tasks.py: entry, DOI, signature, card     + cite_support.py sources · sheet · check
0 sentences read against a source              t99_paper_citation_check/support.yaml, one row a sentence and key
"was filled" for the source's "prescribing"    a quoted 21.6 must sit in a supporting passage; looser blocks a send
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-23 | a co-author's Word comment: the sentence said "was filled" after 21.6% of visits, Gray 2021 says "the rate of opioid prescribing was 21.6%"; nothing makes the reading a gate (topic 1) | AgreeableJama-Board Report | `cite_support.py`; the cite agent fills the sheet in its own or the sheet's words; a changed sentence is read again |

Check: scratch copy of Paper-AgreeableOpioid-Jama: 51 sentence-key pairs; 32 of 36 sources fetched from PubMed (4
have no record: Luo 2026, Gao 2015, two web sources); a supports reading whose passage lacks 21.6 is ❗; with the
source's 21.6% passage it passes. State: fixed. Guard: `tests/test_send_check.py` (6).

## 🚪 Topic: Paper check ▸ one door, wrong apart from unrecorded

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-23 | JL: should hai-paper get a skill "hai-paper-check" for citations and values? `paper_check.py` "65 to fix", `chain_check.py` "947 failures", no way to tell a wrong number from missing bookkeeping (topic 3) | AgreeableJama-Board Report | decided: no new skill, an alias; `send_check.py` runs citations (details, web, order, support) and values (printed, chain); ❗ prints wrong is the exit code, ⬜ not recorded, 🙋 a person |

Check: read-only on the real paper: ❗ 34 references drop their DOI, 2 access dates as data; ⬜ 36 keys unsigned,
the reading sheet absent, 294 numbers found and not bound, 359 unbound, chain rules 1 to 3 (947); values print
nothing wrong (0 differs). State: fixed. Open: a workbench page for the report; `paper_check.py` does not link it yet.
