---
compares: j01_code-v1-example-questions_data-v1
with: j02_code-v1-example-questions_data-v2
moved: data
rule: held when the finding's direction and verdict stay; changed names what moved; a page not written is not comparable
---

# j02 against j01: only the data moved

One clock moved (data-v1 → data-v2, the same analysis plan), so every change below has that one cause. 4 changed · 2 held · 2 not comparable.

| question | previous | this | status | why |
|---|---|---|---|---|
| D01 | 600 rows and 5 columns over 10 days, 2026-01-05 to 2026-01-14; no col… | 960 rows and 5 columns over 16 days, 2026-01-05 to 2026-01-20; no col… | changed | data moved (data-v1 → data-v2): more rows and days, as the data version adds them |
| D02 | The arms are close to even in every cut (arm A holds 40% to 48% of a… | The arms are close to even in every cut (arm A holds 44% to 50% of a… | held | data moved (data-v1 → data-v2): the same finding on more rows |
| I01 | Arm B's outcome rate is 19 points above arm A's on the whole extract… | Arm B's outcome rate is 15 points above arm A's on the whole extract… | not comparable | its page in j02 is partial |
| I02 | The daily rate runs from 28% to 50%, with a downward drift: -1.8 poin… | The outcome rate falls over the window because contacts tire of the m… | changed | data moved: the drift's interval now crosses zero |
| K01 | UNDETERMINED: neither pooling nor splitting is shown; only the whole-… | POOL: one counsel serves both groups. | changed | data moved: the verdict went from UNDETERMINED to POOL |
| W01 | Keep arm B for the next round, for the whole population; leave counse… | page to write | not comparable | its page in j02 is open |
| X01 | Arm B's outcome rate is about 19 points higher than arm A's (50% agai… | Arm B's outcome rate is about 15 points higher than arm A's (47% agai… | held | data moved (data-v1 → data-v2): the same finding on more rows |
| X02 | It cannot say whether the groups differ (the difference spans -21 to… | It cannot speak for group_3 (group_3 has not been read yet), and it c… | changed | data moved: it reports K01's verdict, which moved |
