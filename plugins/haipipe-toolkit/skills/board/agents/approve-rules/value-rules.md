# value-rules · what an agent checks before 🔢 `read:`

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
R6  THE STATE LADDER IS THE PLUGIN'S. `planned · commissioned · answered ·
    read` and nothing else. `raised`, `working` and `bound` were retired at
    haipipe-plugin-probe 0.7.0 and are defects where they still appear.
R7  NO STAKE CROSSED. executor/ contains no claim id, no page id, and no
    sentence from consumer/. The wall is a path, and this rule is what
    proves it held.
R8  ONE QUESTION, ONE CARD. No second card on this page asks the same
    Q-executor. A duplicate is the exact failure the PP id exists to prevent.
```

## 🚫 NOT rules

```text
"is this number surprising enough to report?"
"was this the right question to ask the bank?"
"does this number change the paper's story?"
```

What a number MEANS is the page's argument and is re-judged each time, so it
is a person's 🛑. And `read:` itself stays a person's tick under
haipipe-plugin-probe: an agent may pass R1-R8 and still not write it.
