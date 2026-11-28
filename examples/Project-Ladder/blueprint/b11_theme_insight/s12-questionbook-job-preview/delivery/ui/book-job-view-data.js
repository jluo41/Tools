window.BOOK = {
"book": "InsightQuestionBook-Example",
"levels": {
"D": "🗂 Data",
"I": "📈 Information",
"K": "🧠 Knowledge",
"W": "🧭 Wisdom",
"X": "🎯 Executive"
},
"jobs": [
{
"id": "j02",
"release": "question-v2",
"folder": "j02_question-v2_example-follow-up",
"title": "example follow-up",
"closed": false,
"signed": "",
"from": "question-v1",
"goal": "question-v2, example follow-up: the questions and their scripts on the segments it fixes",
"about": "The second analysis plan, still a draft: every question of question-v1 kept, and one new Knowledge question, K02, from the proposal `gap-over-the-window` (j02's comparison). The proposal `second-and-third` (a segment) is still open. Unsigned: no Board Job runs it yet.",
"segments": [
[
"full",
"every row"
],
[
"first",
"the largest group, asked on its own"
],
[
"second",
"the second group, asked on its own"
],
[
"cross",
"one test of whether the first and second groups differ"
],
[
"third",
"the small group, kept so the example shows a segment too thin to answer"
]
],
"tasks": [
{
"id": "t01",
"q": "D01",
"level": "D",
"name": "extract shape",
"question": "what does the example extract hold?",
"ask": "How many rows, columns and days does the example extract hold, and how much of each column is missing?",
"change": "kept",
"home": "j01",
"method": {
"ask": "describe",
"answer": "count",
"read": "table"
},
"needs": [
[
"E1",
"compute",
"the extract's size, its window and the share missing in each column"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t02",
"q": "D02",
"level": "D",
"name": "arm balance",
"question": "are the arms and groups the size we expect in each segment?",
"ask": "In each segment, how many rows does each arm and each group hold, and what share of the segment is each?",
"change": "kept",
"home": "j01",
"method": {
"ask": "describe",
"answer": "count",
"read": "table"
},
"needs": [
[
"E1",
"compute",
"the rows and share of the segment in each arm"
],
[
"E2",
"compute",
"the rows and share of the segment in each group"
]
],
"asked": "all",
"agreed": "✅ 261106"
},
{
"id": "t03",
"q": "I01",
"level": "I",
"name": "outcome by arm",
"question": "how often does the outcome happen in each arm?",
"ask": "In each segment, what is the outcome rate in arm A and in arm B, and how wide is the gap between them?",
"change": "kept",
"home": "j01",
"method": {
"ask": "compare",
"answer": "rate",
"read": "interval"
},
"needs": [
[
"E1",
"compute",
"the outcome rate in each arm, with its 95% interval"
],
[
"E2",
"compute",
"the gap, arm B minus arm A, in points, with its 95% interval"
]
],
"asked": "all",
"agreed": "✅ 261106"
},
{
"id": "t04",
"q": "I02",
"level": "I",
"name": "outcome by day",
"question": "does the outcome rate move across the days of the window?",
"ask": "Across the days of the window, what is the outcome rate each day, and does it drift up or down?",
"change": "kept",
"home": "j01",
"method": {
"ask": "compare",
"answer": "rate",
"read": "trend"
},
"needs": [
[
"E1",
"compute",
"the outcome rate on each day, with its 95% interval"
],
[
"E2",
"compute",
"the drift, in points per day, with its 95% interval"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t05",
"q": "K01",
"level": "K",
"name": "gap by group",
"question": "is the arm gap the same in the first and second groups?",
"ask": "Is the gap between arm B and arm A the same in the first and second groups, so that one counsel serves both?",
"change": "kept",
"home": "j01",
"method": {
"ask": "test",
"answer": "pool or split",
"read": "verdict"
},
"needs": [
[
"E1",
"cite",
"the gap B - A in the first and in the second group"
],
[
"E2",
"compute",
"the two groups' gaps, their difference, and the pooling verdict"
],
[
"E3",
"judge",
"whether one counsel serves both groups"
]
],
"asked": "cross",
"agreed": "✅ 261106"
},
{
"id": "t06",
"q": "W01",
"level": "W",
"name": "next round",
"question": "what should the next example round keep or change?",
"ask": "Given the gap and the pooling verdict, what should the next round keep, change or leave undecided, and what must it not be read to say?",
"change": "kept",
"home": "j01",
"method": {
"ask": "counsel",
"answer": "judge",
"read": "handoff"
},
"needs": [
[
"E1",
"cite",
"the groups' gaps and the pooling verdict"
],
[
"E2",
"judge",
"the counsel"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t07",
"q": "X01",
"level": "X",
"name": "what we found",
"question": "what did the example find, in one line?",
"ask": "In one plain line, what did the example find about arm B against arm A?",
"change": "kept",
"home": "j01",
"method": {
"ask": "summarize",
"answer": "judge",
"read": "one line"
},
"needs": [
[
"E1",
"cite",
"the arm rates"
],
[
"E2",
"cite",
"the gap B - A"
],
[
"E3",
"cite",
"whether one counsel serves both groups"
],
[
"E4",
"judge",
"the one plain line"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t08",
"q": "X02",
"level": "X",
"name": "what data cannot say",
"question": "what can this data not say?",
"ask": "In plain words, what can the example data not say, and which segment or question shows the limit?",
"change": "kept",
"home": "j01",
"method": {
"ask": "summarize",
"answer": "judge",
"read": "one line"
},
"needs": [
[
"E1",
"cite",
"the window's length and size"
],
[
"E2",
"cite",
"the segment too thin to answer"
],
[
"E3",
"cite",
"the pooling verdict and its interval"
],
[
"E4",
"judge",
"the limits in plain words"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t09",
"q": "K02",
"level": "K",
"name": "gap over the window",
"question": "does the arm gap hold across the window?",
"ask": "Does the gap between arm B and arm A hold in both halves of the window, or does it move with the daily drift?",
"change": "new",
"home": "j02",
"method": {
"ask": "test",
"answer": "replicate",
"read": "verdict"
},
"needs": [
[
"E1",
"cite",
"the gap on the whole extract"
],
[
"E2",
"cite",
"the daily drift"
],
[
"E3",
"compute",
"the gap in each half of the window and their difference, with a verdict"
],
[
"E4",
"judge",
"whether the gap holds over time"
]
],
"asked": [
"full"
],
"agreed": "⬜"
}
]
},
{
"id": "j01",
"release": "question-v1",
"folder": "j01_question-v1_example-questions",
"title": "example questions",
"closed": true,
"signed": "✅ 261106",
"from": "",
"goal": "question-v1, example questions: the questions and their scripts on the segments it fixes",
"about": "The first analysis plan of the example: eight questions, from what the extract holds (Data) to the plain answers a leader reads first (Executive), on five segments. It takes no proposal: it is the first.",
"segments": [
[
"full",
"every row"
],
[
"first",
"the largest group, asked on its own"
],
[
"second",
"the second group, asked on its own"
],
[
"cross",
"one test of whether the first and second groups differ"
],
[
"third",
"the small group, kept so the example shows a segment too thin to answer"
]
],
"tasks": [
{
"id": "t01",
"q": "D01",
"level": "D",
"name": "extract shape",
"question": "what does the example extract hold?",
"ask": "How many rows, columns and days does the example extract hold, and how much of each column is missing?",
"change": "new",
"home": "j01",
"method": {
"ask": "describe",
"answer": "count",
"read": "table"
},
"needs": [
[
"E1",
"compute",
"the extract's size, its window and the share missing in each column"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t02",
"q": "D02",
"level": "D",
"name": "arm balance",
"question": "are the arms and groups the size we expect in each segment?",
"ask": "In each segment, how many rows does each arm and each group hold, and what share of the segment is each?",
"change": "new",
"home": "j01",
"method": {
"ask": "describe",
"answer": "count",
"read": "table"
},
"needs": [
[
"E1",
"compute",
"the rows and share of the segment in each arm"
],
[
"E2",
"compute",
"the rows and share of the segment in each group"
]
],
"asked": "all",
"agreed": "✅ 261106"
},
{
"id": "t03",
"q": "I01",
"level": "I",
"name": "outcome by arm",
"question": "how often does the outcome happen in each arm?",
"ask": "In each segment, what is the outcome rate in arm A and in arm B, and how wide is the gap between them?",
"change": "new",
"home": "j01",
"method": {
"ask": "compare",
"answer": "rate",
"read": "interval"
},
"needs": [
[
"E1",
"compute",
"the outcome rate in each arm, with its 95% interval"
],
[
"E2",
"compute",
"the gap, arm B minus arm A, in points, with its 95% interval"
]
],
"asked": "all",
"agreed": "✅ 261106"
},
{
"id": "t04",
"q": "I02",
"level": "I",
"name": "outcome by day",
"question": "does the outcome rate move across the days of the window?",
"ask": "Across the days of the window, what is the outcome rate each day, and does it drift up or down?",
"change": "new",
"home": "j01",
"method": {
"ask": "compare",
"answer": "rate",
"read": "trend"
},
"needs": [
[
"E1",
"compute",
"the outcome rate on each day, with its 95% interval"
],
[
"E2",
"compute",
"the drift, in points per day, with its 95% interval"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t05",
"q": "K01",
"level": "K",
"name": "gap by group",
"question": "is the arm gap the same in the first and second groups?",
"ask": "Is the gap between arm B and arm A the same in the first and second groups, so that one counsel serves both?",
"change": "new",
"home": "j01",
"method": {
"ask": "test",
"answer": "pool or split",
"read": "verdict"
},
"needs": [
[
"E1",
"cite",
"the gap B - A in the first and in the second group"
],
[
"E2",
"compute",
"the two groups' gaps, their difference, and the pooling verdict"
],
[
"E3",
"judge",
"whether one counsel serves both groups"
]
],
"asked": "cross",
"agreed": "✅ 261106"
},
{
"id": "t06",
"q": "W01",
"level": "W",
"name": "next round",
"question": "what should the next example round keep or change?",
"ask": "Given the gap and the pooling verdict, what should the next round keep, change or leave undecided, and what must it not be read to say?",
"change": "new",
"home": "j01",
"method": {
"ask": "counsel",
"answer": "judge",
"read": "handoff"
},
"needs": [
[
"E1",
"cite",
"the groups' gaps and the pooling verdict"
],
[
"E2",
"judge",
"the counsel"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t07",
"q": "X01",
"level": "X",
"name": "what we found",
"question": "what did the example find, in one line?",
"ask": "In one plain line, what did the example find about arm B against arm A?",
"change": "new",
"home": "j01",
"method": {
"ask": "summarize",
"answer": "judge",
"read": "one line"
},
"needs": [
[
"E1",
"cite",
"the arm rates"
],
[
"E2",
"cite",
"the gap B - A"
],
[
"E3",
"cite",
"whether one counsel serves both groups"
],
[
"E4",
"judge",
"the one plain line"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
},
{
"id": "t08",
"q": "X02",
"level": "X",
"name": "what data cannot say",
"question": "what can this data not say?",
"ask": "In plain words, what can the example data not say, and which segment or question shows the limit?",
"change": "new",
"home": "j01",
"method": {
"ask": "summarize",
"answer": "judge",
"read": "one line"
},
"needs": [
[
"E1",
"cite",
"the window's length and size"
],
[
"E2",
"cite",
"the segment too thin to answer"
],
[
"E3",
"cite",
"the pooling verdict and its interval"
],
[
"E4",
"judge",
"the limits in plain words"
]
],
"asked": [
"full"
],
"agreed": "✅ 261106"
}
]
}
],
"proposals": [
[
"gap-over-the-window",
"Since K01 was narrowed to the pooling test, no Knowledge question tests whether the gap holds across the window, and no question reads I02 any more. I02's drift was downward on data-v1 and crosses zero on data-v2 (vs-j01): a replication across the window's halves would say whether the gap moves with it."
],
[
"second-and-third",
"group_3 is refused for power on every data version (40 rows, then 68). A segment of group_2 and group_3 together would read the small group beside its neighbour instead of not at all."
]
]
};
