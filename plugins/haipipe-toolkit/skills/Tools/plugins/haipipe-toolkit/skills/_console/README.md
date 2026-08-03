# _console

Review ledgers. A review is a PROCESS artifact and must never ship inside the
skill it reviews, so `/haipipe-skill-diagnose` writes here instead of into the
bucket.

- One file per TOPIC, named `<YYMMDD>-<SLUG>.md`.
- The date is the day the file is BORN and is never re-dated.
- A later session APPENDS to the existing file rather than opening a new one.
- The user replies inline in these files, in the `> JL:` slot of each
  `> {CC->JL}:` thread. First reply wins.

Created 260803, on the first run of `/haipipe-skill-diagnose` that needed it:
the skill had pointed here since v1.3.0 and the folder had never been made, so
every earlier run either wrote its ledger into the bucket or skipped the step.
