Column dictionary: the format
=============================

One YAML file per table family, covering every version of the table. It holds
everything a person has to type; the worker computes the rest.

```yaml
table:
  name: SMS cohort table
  what: One parquet per release ... (one or two sentences)
  row: one message about one prescription. ... (finishes "One row is")
  grain: [prescription_id, message_type]        # the key that should be unique
  grain_candidates:                             # other keys worth testing
    - [invitation_id, prescription_id]
  time: invitation_date                         # the column the time span uses
  source: the code or delivery that makes the table (SPACE-relative path)
  example_story: reads the made-up row as one sentence (optional)
  notes:                                        # shown in Gotchas, found_by dictionary
    - a known quirk, with its evidence

groups:                                         # in reading order
  identity:
    title: Identifiers
    what: the de-identified keys that join rows
    identifying: true                           # values withheld for every column in it
  engagement:
    title: Engagement
    what: whether the SMS went out and how far the patient got

columns:
  clicked:
    group: engagement
    meaning: 1 when the patient clicked the SMS link.
    role: flag                                  # optional; inferred when absent
    identifying: false                          # optional; overrides the group
    feeds: [invitation]                         # downstream readers (ProcName, CaseFn ...)
    source: where the meaning came from (contract, ETL line, vendor note)
    notes: [a quirk of this column]             # optional
```


Rules for typing a meaning
--------------------------

1. **Source every meaning.** `source:` names the contract, code, or note it
   came from. `seed_dictionary.py` fills it for seeded meanings.
2. **"?" means untyped.** A meaning of `?` shows as `? (not described)`. A
   meaning that starts with `?` is a guess from the name; it is shown, and the
   card lists it as unconfirmed until the data owner confirms it.
3. **Say what one value means, in the row's terms.** "1 when the patient
   clicked the SMS link", not "click flag".
4. **Name renames.** When the next stage renames the column, say so:
   "the SourceFn renames it `invitation_date_utc`".
5. **A version difference is a note, not a second entry.** The card's
   `⑥ changes` finds added and removed columns itself.


Seeding
-------

```bash
python <skill>/templates/seed_dictionary.py \
  --dictionary <block>/src/column_dictionary.yaml \
  --table <version 1 parquet> --table <version 2 parquet> ... \
  --seed <contract card, newest first> ... \
  --groups-from <job>/src/column_groups.py
```

Run from the SPACE root, SPACE-relative paths only. A seed is any YAML with
`columns: [{name, meaning}]`; its top-level `procname` becomes the column's
`feeds:`. Seeds only match columns by name; a column the next stage renames
is typed by hand from the renamed entry.
