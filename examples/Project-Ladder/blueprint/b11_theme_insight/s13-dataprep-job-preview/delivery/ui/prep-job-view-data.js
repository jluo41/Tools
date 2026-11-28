window.PREP = {
"block": "InsightDataPrep-Example",
"set": "Example",
"store": "_WorkSpace/insight-ready",
"serves": [
"Insight-Example"
],
"jobs": [
{
"id": "j01",
"prep": "prep-v1",
"folder": "j01_prep-v1_example-ready",
"closed": true,
"signed": "✅ 261126",
"hash": "d7fe454e751b",
"from": "",
"goal": "prep-v1, example ready: the code chain that turns a raw export into a folder ready for insight, frozen once a person signs it",
"about": "The first prep version: three steps turn the made-up export into a ready folder. t01 writes the experiment card, t02 checks the keys, t03 writes the rows with their manifest and dictionary.",
"steps": [
{
"id": "t01",
"name": "experiment",
"folder": "t01_experiment",
"goal": "Write the experiment card from the raw export: arms, groups, days",
"reads": "ctx.raw example.parquet",
"writes": "experiment_card.json and .md",
"checks": [
"the raw export holds example.parquet with date, arm, group, outcome, score"
],
"agreed": "✅ 261126",
"about": "The card comes first (rule 7); a later step and every question read what it found about the arms and the days."
},
{
"id": "t02",
"name": "source",
"folder": "t02_source",
"goal": "Read the raw export, cut each date to its day, and check its keys before anything uses it",
"reads": "ctx.raw example.parquet",
"writes": "rows.parquet (dates cut to the day); metrics.json with its counts and checks",
"checks": [
"no key column is empty",
"arms are A or B",
"groups are group_1, group_2 or group_3",
"outcome is 0 or 1"
],
"agreed": "✅ 261126",
"about": "A row with an unknown arm or group stops the Run here, not inside a question."
},
{
"id": "t03",
"name": "prepare",
"folder": "t03_prepare",
"goal": "Write the ready folder the questions read: the rows, their manifest and dictionary",
"reads": "ctx.prev rows.parquet",
"writes": "example.parquet, manifest.json, data_dictionary.csv (the ready folder)",
"checks": [
"the rows hold exactly the five dictionary columns",
"the dictionary holds no record value"
],
"agreed": "✅ 261126",
"about": "The ready folder has the shape of a data version folder, so question-v1's scripts read it unchanged."
}
],
"used": [
{
"board": "Insight-Example",
"job": "j03",
"folder": "j03_data-v2_prep-v1_question-v1",
"data": "data-v2",
"release": "question-v1",
"mark": "✅",
"run": "r01_example",
"ready": "_WorkSpace/insight-ready/Example_data-v2@prep-v1/",
"steps": {
"t01_experiment": {
"mark": "✅",
"seconds": 0.6,
"file": "experiment_card.json",
"metrics": {
"stated": "nothing stated",
"settings": {
"arms": {
"A": 459,
"B": 501
},
"groups": [
"group_1",
"group_2",
"group_3"
]
},
"time": {
"first_day": "2026-01-05",
"last_day": "2026-01-20",
"calendar_days": 16,
"active_days": 16,
"gaps": [],
"rows_per_day": {
"min": 60,
"max": 60
},
"utc_and_local_time": "not checkable: the export holds days, not times",
"send_hours": "not checkable: the export holds days, not times"
},
"checks": {
"settings": "not checkable: nothing stated",
"time": "not checkable: nothing stated"
}
}
},
"t02_source": {
"mark": "✅",
"seconds": 0.0,
"file": "metrics.json",
"metrics": {
"rows": 960,
"columns": [
"date",
"arm",
"group",
"outcome",
"score"
],
"checks": {
"keys not empty": "pass",
"arms known": "pass",
"groups known": "pass",
"outcome 0 or 1": "pass"
}
}
},
"t03_prepare": {
"mark": "✅",
"seconds": 0.0,
"file": "",
"metrics": {}
}
}
}
]
}
]
};
