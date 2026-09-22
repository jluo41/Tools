# Change ledger · the Result of a Revise Run

The ledger is the Revise Run's `Saved result`. It reuses the Step template's
`#### Track changes` block so the existing Run Space renderer draws it: one
`##### <id> · <kind>` card per change, clean text only, red deletions and green
insertions computed by the presenter. Revise adds one field per card,
`###### Decision`, and one header block naming the two inputs.

```markdown
## Step s001

### Human feedback
Compare v002 (accepted) with v003 (candidate) of rp-para-01_P03.

### Saved result

#### Inputs
- Before: results/rp-para-01_P03/v002.md · sha256 <hash>
- After:  results/rp-para-01_P03/v003.md · sha256 <hash>
- Target: C1.P3

#### Track changes

##### R01 · wording

###### Before
<exact prior text>

###### After
<exact candidate text>

###### Why
Answers F02: the sentence claimed more than the estimate supports.

###### Decision
accept

###### Inferred preference
Hedge effect sizes with the interval, not with adverbs.

###### Preference status
candidate

##### R02 · claim
…

#### Handoff
- accepted text → rp-para-01_P03 NEW_VERSION v004 · <date>
```

## The direct-edit Step

When the person saves a paragraph box in Draft Space → Revise, the server
writes the same shape with three fixed choices: `#### Inputs` names the Outline file (Before:
its Draft fields as rendered; After: the same file after the Save) and the
paragraph target; each card carries a `###### Target` line with the Bullet
address, `###### Decision` is `accept` because the person typed the text, and
`###### Preference status` reads `edited directly by the person in Draft Space
→ Revise`. A sentence written into an empty Draft is a `first draft` card whose
Before is `(no draft)`; a cleared Draft is a `deletion` card whose After is
`(removed)`. Every Save appends one more `## Step sNNN` to the same open Run
and continues the `Rnn` numbering; there is no Handoff block, because the
Drafts already sit where the writing Run adopts them.

## Rules

- **One row, one material change.** Whitespace, formatting, and presenter-only
  differences are not rows. A moved sentence is one `structure` row, not a
  delete and an add.
- **Kinds** come from the Step template: `wording`, `claim`, `evidence`,
  `structure`, `citation`, `tone`. Unclassified rows are a finding, not a kind.
- **Decision** is exactly `accept`, `reject`, or `modify: <text>`. A missing
  Decision keeps the Run `Waiting`; the presenter shows the row without a
  Decision line.
- **Why** names the feedback item (`F02`) or the purpose. A row with no Why is
  `Held` by the reviewer, not accepted by default.
- **Inferred preference** is optional and always a candidate; `Preference
  status` is `candidate`, `confirmed` (the person said so), or `rejected`.
- **Inputs are frozen.** Both hashes are recorded before the first row; a
  changed input is a new Revise Run.
- **Handoff** names the writing Run and the Version that received the accepted
  text, or says `none` when every row was rejected.
