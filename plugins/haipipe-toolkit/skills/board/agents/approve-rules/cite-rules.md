# cite-rules · what an agent checks before a person's 📚 `verified`

Seeded 260818. The binding law comes first, because it is the one this file
may never relax.

## ⛔ The law that outranks every rule below

```text
a machine may SUBSET or TRANSCRIBE a real bibtex record.
It may NEVER COMPOSE one.
```

`haipipe-plugin-outline/ref/evidence/citations.md` citation law. An agent that
cannot find the record does NOT write a plausible one; it reports the key as
unfound and stops. Every rule
below assumes the entry already exists because a person or a resolver landed it.

## Rules

```text
R1  IT RESOLVES. The DOI, arXiv id, or title+year resolves to one real record
    at a real source. Record WHICH source and the exact query.
R2  THE FIELDS MATCH THE SOURCE. Author list, year, title, venue and volume
    equal what the source returned. A one-character drift in a title is a
    transcription error, not a style choice.
R3  NO INVENTED FIELD. Any field not present at the source is absent here.
    An agent may drop fields; it may never add one.
R4  THE KEY IS UNIQUE ON THE PAGE. No two entries share a key, and no key
    collides with a different work.
R5  EVERY \citep{key} IN THE PROSE EXISTS IN THE .bib. The reverse too: an
    entry nothing cites is reported, not silently kept.
R6  THE CITATION SUPPORTS THE SENTENCE IT SITS IN. The cited work's abstract
    or the quoted passage must contain the claim being attributed to it.
    ⬅ this is the one rule an agent must READ for, not pattern-match
R7  UNVERIFIED IS EXPLICIT. An entry with no `verified` field carries
    `verified = {}`, so a count can say "3 of 7 still unverified" instead of
    reading absence as either state.
R8  THE AGENT WRITES `checked`, NEVER `verified`. Two fields, two authors,
    the same split `approve-rules.md` R10 fixes for an outline. A bibtex
    entry has no `key: value`, so the field's host syntax wins:

    ```text
    checked  = {auto <YYMMDD>}   R1-R7 pass    🤖 the agent
    verified = {JL <YYMMDD>}                   🧑 the person
    ```

    Added 260821. Not promoted from a break: the 260818 two-field ruling was
    written into `approve-rules.md` alone, so this file still named a person's
    tick as the agent's output field. R7's `verified = {}` stays exactly as
    written — an empty brace is the ABSENCE of the person's tick, and an agent
    may neither fill it nor remove it.
```

## 🚫 NOT rules

```text
"is this the right literature to cite here?"
"is this the strongest source for this claim?"
"should this paragraph cite anything at all?"
```

Which works a page should stand on is the page's argument, so it is a person's
🛑 and a person's proposal.
