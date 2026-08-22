# value-rules · what an agent checks before a person's 🧮 `read:`

Seeded 260818. `read:` means "a person read the answer"; what an agent can
establish is everything AROUND that: that the number in the prose is the number
in the file, and that the file is the one the card asked for.

## Rules

```text
R1  THE PROSE NUMBER EQUALS THE PROOF NUMBER. Every figure the page states
    from this card appears, character for character, in a file under the
    card's proof/. A rounded number names its rounding.
R2  target: RESOLVES. The card's `target:` path exists and is the QA file
    that answers this card's own Q-executor, not a topic-similar neighbour.
R3  proof/ CARRIES ITS PROVENANCE. Every pulled file has source, run and
    sha256 in the manifest, and each sha256 matches the bytes on disk.
R4  THE ANSWER ANSWERS THE QUESTION ASKED. executor/'s A-executor addresses
    executor/'s Q-executor. A bank that answered a different question is a
    finding, not a value.
R5  serves: NAMES REAL ADDRESSES. Every `C<n>.P<n>.B<n>` in `serves:` exists
    in the approved outline of the round that raised the card.
R6  THE STATE LADDER IS THE PLUGIN'S, ALL EIGHT OF IT. `planned ·
    commissioned · answered · answered-local · read · deferred · failed ·
    concern`, the list `haipipe-plugin-probe` §✍️ and `ref/check-probe.py`
    both carry, and nothing outside it. `raised`, `working` and `bound` were
    retired at haipipe-plugin-probe 0.7.0 and are defects where they appear.
    ⚠️ Until 260821 this rule named only the first four, so a legally
    `deferred`, `failed` or `concern` card FAILED R6 — the rule reported the
    ladder it had been given, not a defect on the card.
R7  NO STAKE CROSSED. executor/ contains no claim id, no page id, and no
    sentence from consumer/. The wall is a path, and this rule is what
    proves it held.
R8  ONE QUESTION, ONE CARD. No second card on this page asks the same
    Q-executor. A duplicate is the exact failure the PP id exists to prevent.
R9  THE AGENT WRITES `checked:`, NEVER `read:`. Two fields, two authors, the
    same split `approve-rules.md` R10 fixes for an outline:

    ```text
    checked: ✅ auto <YYMMDD> · value-rules R1-R8 pass   🤖 the agent
    read:    ✅ JL <YYMMDD>                              🧑 the person
    ```

    Added 260821, and this file already knew it: the closing note below said
    an agent "may pass R1-R8 and still not write it" without naming what it
    writes instead. Now it has a field.
```

## 🚫 NOT rules

```text
"is this number surprising enough to report?"
"was this the right question to ask the bank?"
"does this number change the paper's story?"
```

What a number MEANS is the page's argument and is re-judged each time, so it
is a person's 🛑. And `read:` itself stays a person's tick under
haipipe-plugin-probe: an agent that passes R1-R8 writes `checked:` (R9) and
stops there.
