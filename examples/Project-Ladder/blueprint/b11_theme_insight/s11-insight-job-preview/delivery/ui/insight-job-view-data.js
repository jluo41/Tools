window.INSIGHT = {
"board": "Insight-Example",
"levels": {
"D": "🗂 Data",
"I": "📈 Information",
"K": "🧠 Knowledge",
"W": "🧭 Wisdom",
"X": "🎯 Executive"
},
"versions": {
"data-v1": "first ten days",
"data-v2": "all sixteen days"
},
"jobs": [
{
"id": "j03",
"release": "question-v1",
"data": "data-v2",
"prep": "prep-v1",
"folder": "j03_data-v2_prep-v1_question-v1",
"closed": false,
"goal": "What the example questions (question-v1) find on data-v2, all sixteen days",
"moved": "prep",
"previous": "j02",
"order": [
"full",
"first",
"second",
"third",
"cross"
],
"tasks": [
{
"id": "t02",
"q": "D01",
"level": "D",
"name": "extract shape",
"folder": "t02_D01_extract-shape",
"mark": "⬜",
"ask": "How many rows, columns and days does the example extract hold, and how much",
"answer": "",
"sure": "",
"segments": [
[
"✅",
"full",
"r01_full",
""
]
]
},
{
"id": "t03",
"q": "D02",
"level": "D",
"name": "arm balance",
"folder": "t03_D02_arm-balance",
"mark": "⬜",
"ask": "In each segment, how many rows does each arm and each group hold, and what share",
"answer": "",
"sure": "",
"segments": [
[
"✅",
"full",
"r01_full",
""
],
[
"✅",
"first",
"r02_first",
""
],
[
"✅",
"second",
"r03_second",
""
],
[
"✅",
"third",
"r05_third",
""
]
]
},
{
"id": "t04",
"q": "I01",
"level": "I",
"name": "outcome by arm",
"folder": "t04_I01_outcome-by-arm",
"mark": "⬜",
"ask": "In each segment, what is the outcome rate in arm A and in arm B, and how wide",
"answer": "",
"sure": "",
"segments": [
[
"✅",
"full",
"r01_full",
""
],
[
"✅",
"first",
"r02_first",
""
],
[
"✅",
"second",
"r03_second",
""
],
[
"❗",
"third",
"r05_third",
"underpowered: third MDE 33.42 > 20.0"
]
]
},
{
"id": "t05",
"q": "I02",
"level": "I",
"name": "outcome by day",
"folder": "t05_I02_outcome-by-day",
"mark": "⬜",
"ask": "Across the days of the window, what is the outcome rate each day, and does it",
"answer": "",
"sure": "",
"segments": [
[
"✅",
"full",
"r01_full",
""
]
]
},
{
"id": "t06",
"q": "K01",
"level": "K",
"name": "gap by group",
"folder": "t06_K01_gap-holds",
"mark": "⬜",
"ask": "Is the gap between arm B and arm A the same in the first and second groups,",
"answer": "",
"sure": "",
"segments": [
[
"✅",
"cross",
"r04_cross",
""
]
]
},
{
"id": "t07",
"q": "W01",
"level": "W",
"name": "next round",
"folder": "t07_W01_next-round",
"mark": "⬜",
"ask": "Given the gap and the pooling verdict, what should the next round keep, change",
"answer": "",
"sure": "",
"segments": []
},
{
"id": "t08",
"q": "X01",
"level": "X",
"name": "what we found",
"folder": "t08_X01_what-we-found",
"mark": "⬜",
"ask": "In one plain line, what did the example find about arm B against arm A?",
"answer": "",
"sure": "",
"segments": []
},
{
"id": "t09",
"q": "X02",
"level": "X",
"name": "what data cannot say",
"folder": "t09_X02_what-data-cannot-say",
"mark": "⬜",
"ask": "In plain words, what can the example data not say, and which segment or question",
"answer": "",
"sure": "",
"segments": []
}
],
"compare": {}
},
{
"id": "j02",
"release": "question-v1",
"data": "data-v2",
"prep": "",
"folder": "j02_question-v1-example-questions_data-v2",
"closed": false,
"goal": "What the example questions (question-v1) find on data-v2, all sixteen days",
"moved": "data",
"previous": "j01",
"order": [
"full",
"first",
"second",
"third",
"cross"
],
"tasks": [
{
"id": "t01",
"q": "D01",
"level": "D",
"name": "extract shape",
"folder": "t01_D01_extract-shape",
"mark": "✅",
"ask": "How many rows, columns and days does the example extract hold, and how much of each column is missing?",
"answer": "960 rows and 5 columns over 16 days, 2026-01-05 to 2026-01-20; no column has a missing value.",
"sure": "exact counts on the whole extract",
"segments": [
[
"✅",
"full",
"r01_full",
"960 rows and 5 columns over 16 days, 2026-01-05 to 2026-01-20; no column has a missing value."
]
]
},
{
"id": "t02",
"q": "D02",
"level": "D",
"name": "arm balance",
"folder": "t02_D02_arm-balance",
"mark": "✅",
"ask": "In each segment, how many rows does each arm and each group hold, and what share of the segment is each?",
"answer": "The arms are close to even in every segment (arm A holds 44% to 50% of a segment), and group_3 is a small share of the rows.",
"sure": "exact counts in every segment",
"segments": [
[
"✅",
"full",
"r01_full",
"Arm A 48% and arm B 52% of 960 rows; groups: group_1 56%, group_2 37%, group_3 7%."
],
[
"✅",
"first",
"r02_first",
"Arm A 47% and arm B 53% of 541 rows; one group only (group_1)."
],
[
"✅",
"second",
"r03_second",
"Arm A 50% and arm B 50% of 351 rows; one group only (group_2)."
],
[
"✅",
"third",
"r05_third",
"Arm A 44% and arm B 56% of 68 rows; one group only (group_3)."
]
]
},
{
"id": "t03",
"q": "I01",
"level": "I",
"name": "outcome by arm",
"folder": "t03_I01_outcome-by-arm",
"mark": "🔶",
"ask": "In each segment, what is the outcome rate in arm A and in arm B, and how wide is the gap between them?",
"answer": "Arm B's outcome rate is 15 points above arm A's on the whole extract (47% against 32%), and B leads in every segment that could be read.",
"sure": "Wilson intervals per arm; the gap's interval excludes zero on full",
"segments": [
[
"✅",
"full",
"r01_full",
"Arm B 47% against arm A 32%: a gap of 15 points (95% 9 to 21)."
],
[
"✅",
"first",
"r02_first",
"Arm B 47% against arm A 31%: a gap of 17 points (95% 9 to 25)."
],
[
"✅",
"second",
"r03_second",
"Arm B 51% against arm A 35%: a gap of 16 points (95% 5 to 26)."
],
[
"⬜",
"third",
"r05_third",
"Not run yet: its Run is planned, so this segment has no answer in this Job."
]
]
},
{
"id": "t04",
"q": "I02",
"level": "I",
"name": "outcome by day",
"folder": "t04_I02_outcome-by-day",
"mark": "✅",
"ask": "Across the days of the window, what is the outcome rate each day, and does it drift up or down?",
"answer": "The outcome rate falls over the window because contacts tire of the message, about 0.6 points a day.",
"sure": "a weighted slope with a t interval; daily rates are thin",
"segments": [
[
"✅",
"full",
"r01_full",
"The outcome rate falls over the window because contacts tire of the message, about 0.6 points a day."
]
]
},
{
"id": "t05",
"q": "K01",
"level": "K",
"name": "gap by group",
"folder": "t05_K01_gap-holds",
"mark": "✅",
"ask": "Is the gap between arm B and arm A the same in the first and second groups, so that one counsel serves both?",
"answer": "POOL: one counsel serves both groups.",
"sure": "the difference's interval is 26 points wide",
"segments": [
[
"✅",
"cross",
"r04_cross",
"The gap is 17 points in the first group and 16 in the second; their difference, -1 points (95% -14 to +12, p = 0.8844), gives POOL: the difference''s 95% interval lies inside ±20 points."
]
]
},
{
"id": "t06",
"q": "W01",
"level": "W",
"name": "next round",
"folder": "t06_W01_next-round",
"mark": "⬜",
"ask": "Given the gap and the pooling verdict, what should the next round keep, change or leave undecided, and what must it not be read to say?",
"answer": "",
"sure": "",
"segments": []
},
{
"id": "t07",
"q": "X01",
"level": "X",
"name": "what we found",
"folder": "t07_X01_what-we-found",
"mark": "✅",
"ask": "In one plain line, what did the example find about arm B against arm A?",
"answer": "Arm B's outcome rate is about 15 points higher than arm A's (47% against 32%), on 960 made-up rows.",
"sure": "firm on the whole population; the two groups pool",
"segments": []
},
{
"id": "t08",
"q": "X02",
"level": "X",
"name": "what data cannot say",
"folder": "t08_X02_what-data-cannot-say",
"mark": "✅",
"ask": "In plain words, what can the example data not say, and which segment or question shows the limit?",
"answer": "It cannot speak for group_3, which has not been read yet, and it covers only 16 days; the two groups pool (their difference spans -14 to +12 points), but that says nothing of a third group.",
"sure": "these limits are exact: counts, a refused segment and an interval",
"segments": []
}
],
"compare": {
"title": "j02 against j01: only the data moved",
"against": "j01",
"rows": {
"D01": [
"600 rows and 5 columns over 10 days, 2026-01-05 to 2026-01-14; no col…",
"960 rows and 5 columns over 16 days, 2026-01-05 to 2026-01-20; no col…",
"changed",
"data moved (data-v1 → data-v2): more rows and days, as the data version adds them"
],
"D02": [
"The arms are close to even in every segment (arm A holds 40% to 48% of a…",
"The arms are close to even in every segment (arm A holds 44% to 50% of a…",
"held",
"data moved (data-v1 → data-v2): the same finding on more rows"
],
"I01": [
"Arm B's outcome rate is 19 points above arm A's on the whole extract…",
"Arm B's outcome rate is 15 points above arm A's on the whole extract…",
"not comparable",
"its page in j02 is partial"
],
"I02": [
"The daily rate runs from 28% to 50%, with a downward drift: -1.8 poin…",
"The outcome rate falls over the window because contacts tire of the m…",
"changed",
"data moved: the drift's interval now crosses zero"
],
"K01": [
"UNDETERMINED: neither pooling nor splitting is shown; only the whole-…",
"POOL: one counsel serves both groups.",
"changed",
"data moved: the verdict went from UNDETERMINED to POOL"
],
"W01": [
"Keep arm B for the next round, for the whole population; leave counse…",
"page to write",
"not comparable",
"its page in j02 is open"
],
"X01": [
"Arm B's outcome rate is about 19 points higher than arm A's (50% agai…",
"Arm B's outcome rate is about 15 points higher than arm A's (47% agai…",
"held",
"data moved (data-v1 → data-v2): the same finding on more rows"
],
"X02": [
"It cannot say whether the groups differ (the difference spans -21 to…",
"It cannot speak for group_3, which has not been read yet, and it c…",
"changed",
"data moved: it reports K01's verdict, which moved"
]
}
}
},
{
"id": "j01",
"release": "question-v1",
"data": "data-v1",
"prep": "",
"folder": "j01_question-v1-example-questions_data-v1",
"closed": true,
"goal": "What the example questions (question-v1) find on data-v1, first ten days",
"moved": "start",
"previous": "",
"order": [
"full",
"first",
"second",
"third",
"cross"
],
"tasks": [
{
"id": "t01",
"q": "D01",
"level": "D",
"name": "extract shape",
"folder": "t01_D01_extract-shape",
"mark": "✅",
"ask": "How many rows, columns and days does the example extract hold, and how much of each column is missing?",
"answer": "600 rows and 5 columns over 10 days, 2026-01-05 to 2026-01-14; no column has a missing value.",
"sure": "exact counts on the whole extract",
"segments": [
[
"✅",
"full",
"r01_full",
"600 rows and 5 columns over 10 days, 2026-01-05 to 2026-01-14; no column has a missing value."
]
]
},
{
"id": "t02",
"q": "D02",
"level": "D",
"name": "arm balance",
"folder": "t02_D02_arm-balance",
"mark": "✅",
"ask": "In each segment, how many rows does each arm and each group hold, and what share of the segment is each?",
"answer": "Arm A holds 40% to 48% of a segment's rows and arm B the rest; group_3 is the smallest group.",
"sure": "exact counts in every segment",
"segments": [
[
"✅",
"full",
"r01_full",
"Arm A 47% and arm B 53% of 600 rows; groups: group_1 58%, group_2 35%, group_3 7%."
],
[
"✅",
"first",
"r02_first",
"Arm A 47% and arm B 53% of 350 rows; one group only (group_1)."
],
[
"✅",
"second",
"r03_second",
"Arm A 48% and arm B 52% of 210 rows; one group only (group_2)."
],
[
"✅",
"third",
"r05_third",
"Arm A 40% and arm B 60% of 40 rows; one group only (group_3)."
]
]
},
{
"id": "t03",
"q": "I01",
"level": "I",
"name": "outcome by arm",
"folder": "t03_I01_outcome-by-arm",
"mark": "✅",
"ask": "In each segment, what is the outcome rate in arm A and in arm B, and how wide is the gap between them?",
"answer": "Arm B's outcome rate is 19 points above arm A's on the whole extract (50% against 31%), and B leads in every segment that could be read.",
"sure": "Wilson intervals per arm; the gap's interval excludes zero on full",
"segments": [
[
"✅",
"full",
"r01_full",
"Arm B 50% against arm A 31%: a gap of 19 points (95% 11 to 27)."
],
[
"✅",
"first",
"r02_first",
"Arm B 51% against arm A 31%: a gap of 20 points (95% 10 to 30)."
],
[
"✅",
"second",
"r03_second",
"Arm B 51% against arm A 35%: a gap of 16 points (95% 3 to 29)."
],
[
"❗",
"third",
"r05_third",
"underpowered: third MDE 42.89 > 20.0"
]
]
},
{
"id": "t04",
"q": "I02",
"level": "I",
"name": "outcome by day",
"folder": "t04_I02_outcome-by-day",
"mark": "✅",
"ask": "Across the days of the window, what is the outcome rate each day, and does it drift up or down?",
"answer": "The daily rate runs from 28% to 50%, with a downward drift: -1.8 points a day (95% -3.5 to -0.1).",
"sure": "a weighted slope with a t interval; daily rates are thin",
"segments": [
[
"✅",
"full",
"r01_full",
"The daily rate runs from 28% to 50%, with a downward drift: -1.8 points a day (95% -3.5 to -0.1)."
]
]
},
{
"id": "t05",
"q": "K01",
"level": "K",
"name": "gap by group",
"folder": "t05_K01_gap-holds",
"mark": "✅",
"ask": "Is the gap between arm B and arm A the same in the first and second groups, so that one counsel serves both?",
"answer": "UNDETERMINED: neither pooling nor splitting is shown; only the whole-population counsel stands.",
"sure": "the difference's interval is 33 points wide",
"segments": [
[
"✅",
"cross",
"r04_cross",
"The gap is 20 points in the first group and 16 in the second; their difference, -4 points (95% -21 to +12, p = 0.5992), gives UNDETERMINED: no difference shown, but its 95% interval reaches past ±20 points."
]
]
},
{
"id": "t06",
"q": "W01",
"level": "W",
"name": "next round",
"folder": "t06_W01_next-round",
"mark": "✅",
"ask": "Given the gap and the pooling verdict, what should the next round keep, change or leave undecided, and what must it not be read to say?",
"answer": "Keep arm B for the next round, for the whole population; leave counsel by group undecided until the groups can be pooled or split.",
"sure": "moderate: one window, one gap; the pooling verdict is UNDETERMINED",
"segments": []
},
{
"id": "t07",
"q": "X01",
"level": "X",
"name": "what we found",
"folder": "t07_X01_what-we-found",
"mark": "✅",
"ask": "In one plain line, what did the example find about arm B against arm A?",
"answer": "Arm B's outcome rate is about 19 points higher than arm A's (50% against 31%), on 600 made-up rows.",
"sure": "firm on the whole population; open by group",
"segments": []
},
{
"id": "t08",
"q": "X02",
"level": "X",
"name": "what data cannot say",
"folder": "t08_X02_what-data-cannot-say",
"mark": "✅",
"ask": "In plain words, what can the example data not say, and which segment or question shows the limit?",
"answer": "It cannot say whether the groups differ (the difference spans -21 to +12 points); group_3 was refused for power; and it covers only 10 days.",
"sure": "these limits are exact: counts, a refused segment and an interval",
"segments": []
}
],
"compare": {}
}
]
};
