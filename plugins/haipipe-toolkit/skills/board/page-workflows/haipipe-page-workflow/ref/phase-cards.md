# Page phase cards · six fields in one order

The canonical detailed map is `workflow-table.md`. These cards are the compact
operating view every phase skill and workflow surface may quote.

```text
❓ ASKS     the one question the cycle answers
📥 READS    what must exist before it starts
📤 WRITES   the exact authority it may change
🚪 EXITS    the testable close condition
✋ TICK     person-reserved gate, or none
🔀 ROUTES   the legal next authorities
```

## 🔁 The Page loop

```text
00 CONTEXT              01 OUTLINE                    02 EVIDENCE
   PREPARE ───────────▶    SHAPE ─▶ SURVEY ─────────▶    LAND ─▶ EMBED
      ▲                     ▲                            │       │
      │ policy drift        └────────────────────────────┴───────┘
      │                                 new plan v<N+1>
      │                                             │ approved + folded
      │                                             ▼
      └──────────── 04 CHECK ◀──────────── 03 CONTENT
                         ▲                    WRITE
                         └──── built version ───┘
```

`CONTEXT`, `OUTLINE`, and `EVIDENCE` use the same
`haipipe-plugin-outline` surface. They do not share phase authority:

```text
Context Workspace    CONTEXT prepares governing inputs
Bullet Workspace     OUTLINE shapes the argument
Evidence Workspace   OUTLINE surveys; EVIDENCE lands and embeds
```

## 00 · CONTEXT / PREPARE · `haipipe-page-context`

```text
❓ ASKS     what exact context may later Page phases rely on?
📥 READS    Page/Folder identity · owning workflow · Page Type · policy ·
            requirements · related information · feedback · discussion ·
            Files/Log/Skills · current plan/evidence/run receipts
📤 WRITES   generated outline/<stem>-context.md and one phase receipt
🚪 EXITS    identity and authorities resolved; every required source addressed
            and fresh; missing/conflicting inputs explicit
✋ TICK     none
🔀 ROUTES   OUTLINE/SHAPE · CONTEXT/PREPARE · HOLD
🚫 RUNS     none: Collect, Resolve, Freeze are PREPARE movements
```

## 01A · OUTLINE / SHAPE · `haipipe-page-outline`

```text
❓ ASKS     what will this Page say, and what typed ready evidence does each
            Bullet expect?
📥 READS    frozen Context · Page Type outline policy · current Page · prior
            plan · feedback and decisions
📤 WRITES   outline/<stem>-outline-v<N>.md; SHAPE fields in
            <stem>-evidence-items.md; open Discussion and one Log record
🚪 EXITS    arc/coverage/target/value/shape checks pass; each item has an
            E<NN>-VALUE|CITE|DISPLAY-<slug> name, expectation, and acceptance
✋ TICK     approved: is person-reserved; copilot waits, auto records it owed
🔀 ROUTES   OUTLINE/SURVEY · CONTENT/WRITE · OUTLINE/SHAPE ·
            CONTEXT/PREPARE · HOLD
🚫 RUNS     none: plan and Evidence Item specifications are not Runs
```

## 01B · OUTLINE / SURVEY · `haipipe-page-outline`

```text
❓ ASKS     which upstream Results support each item, and which one local Run
            makes its focal ready evidence?
📥 READS    approved or policy-forwarded typed item contracts ·
            Execution/Discovery Ticket and Result inventories · allowed
            page-local static sources
📤 WRITES   Supporting Runs · one Local Input plan · one indexed Local Run ·
            Decide in outline/<stem>-evidence-items.md
🚪 EXITS    every route is honestly classified; Local Input contents named;
            exactly one pjNNtNNrNN local route per item; Decide signed or
            durably owed under auto policy
✋ TICK     Decide is person-reserved; copilot waits, auto records it owed
🔀 ROUTES   EVIDENCE/LAND · OUTLINE/SHAPE · OUTLINE/SURVEY ·
            CONTEXT/PREPARE · HOLD
🚫 RUNS     none: it inventories/reserves; LAND allocates and executes
```

## 02A · EVIDENCE / LAND · `haipipe-page-evidence`

```text
❓ ASKS     does every make-item have valid Supporting Results, one frozen
            input, and one accepted local typed Result?
📥 READS    decided item table · named Tickets/receipts/Results · worker gates
📤 WRITES   allocated Tickets and Results · frozen Local Input · full ids and
            Result binding in <stem>-evidence-items.md · generated status
🚪 EXITS    all Supporting Results pass; each local VALUE/CITE/DISPLAY Result
            satisfies its item Acceptance contract
✋ TICK     only worker-specific gates already declared by the selected worker
🔀 ROUTES   EVIDENCE/EMBED · OUTLINE/SURVEY · OUTLINE/SHAPE ·
            CONTEXT/PREPARE · EVIDENCE/LAND · HOLD
⚙ RUNS     0..N Execution/Discovery supports, then exactly one Page Evidence
            Item local Run per make-item
```

## 02B · EVIDENCE / EMBED · `haipipe-page-evidence`

```text
❓ ASKS     what does each ready local Result mean for its target Bullet?
📥 READS    accepted local Results · current approved plan
📤 WRITES   outline v<N+1> with Answered:/Drawn:/Routed: appends;
            approved: resets to ⬜; never changes the Result
🚪 EXITS    every ready item is folded; contradictions are explicit findings
✋ TICK     none; the new plan returns to the SHAPE approval gate
🔀 ROUTES   OUTLINE/SHAPE, always
🚫 RUNS     none: consumes and interprets existing Results
```

## 03 · CONTENT / WRITE · `haipipe-page-content`

```text
❓ ASKS     does one built Page version realize only what the approved,
            evidence-aware plan supports?
📥 READS    fresh Context · approved folded plan · ready Evidence Results ·
            Page Type and narrative/style policy · current Page
📤 WRITES   Page Content and authorized Opening/Aims · Division Writing
            Tickets/Results and promotion trace · current delivery artifacts · Log
🚪 EXITS    commissioned divisions accepted/promoted; artifacts current; a
            fresh pre-check says ready
✋ TICK     none
🔀 ROUTES   CHECK · CONTENT · CONTEXT · OUTLINE · EVIDENCE · HOLD
⚙ RUNS     normally one Page Division Writing Run per commissioned division;
            Draft/Revise/Build/Pre-check are internal movements
```

## 04 · CHECK / CHECK · `haipipe-page-check`

```text
❓ ASKS     is this exact built Page version closable, and who acts next?
📥 READS    immutable source/render version · Context · plan · evidence trace ·
            Page Type closing rule · CONTENT trail · human-gate evidence
📤 WRITES   check receipt and findings/comments in the declared review surface
🚪 EXITS    CLOSE or one named backward route
✋ TICK     accepted: and the Folder owner's declared ruling when applicable;
            never written by the machine judge
🔀 ROUTES   CLOSE · CONTEXT · OUTLINE · EVIDENCE · CONTENT · HOLD
🚫 RUNS     none: CHECK is a gate, not a Level-4 Run
```

## Person-reserved acts

| Act | Authority path | Owning cycle |
|---|---|---|
| `approved:` | `outline/<stem>-outline-v<N>.md` | SHAPE |
| `Decide` | `outline/<stem>-evidence-items.md` | SURVEY |
| worker-specific verification/acceptance | worker authority named by LAND | LAND |
| Page/display `accepted:` and Folder ruling | Page/review authority | CHECK |

The Context record contains pointers to these acts but owns none of them.
