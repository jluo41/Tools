How interactive writing allocates, advances and closes Page Runs (structure, scratch, section, paragraph, revise); moved from SKILL.md.

## 🤝 Interactive writing first

For collaborative drafting or feedback-led revision, load
`interactive-writing-run.md` and its `writing-step-template.md` before
editing. One Page owns many sibling Page Runs. RP allocation states its scope
explicitly:

```text
`run-structure-<slug>`          Page Structure Run: SHAPE + SURVEY
`run-scratch-<slug>` Human Scratch capture: Section or paragraph group
`run-section-<slug>`             Section-level writing
`run-paragraph-<slug>`  Paragraph-level writing
`run-revise-<slug>` Revise: compare two frozen texts of one target, settle each change
```

`run-structure-<slug>` is the initial Structure Run. It is one shared Run for the
Page's SHAPE and SURVEY cycles: it settles direction, coverage/non-coverage,
high-level section flow, ordered Bullets, paragraph jobs, Point roles, typed
Evidence Item decisions, and the structure list. It does not write
adopted prose or execute material evidence work. Several people may contribute
Steps to this same Run; record `participants` on the Run and `contributors` on
each Step, and do not create a child Run per person. The full contract is
`structure-run.md`. After the Structure Run closes, Section Runs use
`run-section-<slug>`, and fixed paragraph or paragraph-group Runs use
`run-paragraph-<slug>`.
`run-structure-<slug>` and later ids are reserved for a genuinely independent
post-closure structural goal, not for a Survey pass or a new participant.
Scratch is available once a selected Outline exists. It records a person's
rough thinking at Section (`C1`) or whole paragraph group (`C1.P1`) in the
current Outline grammar; there is no separate subsection node, and the B rows
are reading material only. Save keeps the Scratch Run open,
and a manually triggered AI Summary closes it. Scratch does not edit Draft prose
and does not replace the later Structure, Section, or Paragraph Run.
Human feedback advances Steps inside the selected Run's Version. A chat turn
or review window alone does not create another Run. A later independently
commissioned Section drafting/revision session does create a new `run-section-<slug>`
Run; a complete draft → review/rating → diagnose → revise cycle inside that
session is one Step, not a new Run. For a paragraph target, reopen the same
Run in a new Version when the target and goal remain fixed. `rp` means Run of
Page; its typed sequences are independent from one another and from the
native `rNN` sequence used by delegated Task Runs. New allocation uses only
the explicit kind tokens; retired compact identities remain readable history.
A mismatched kind or paragraph target is Held and cannot unlock later work.

If the closed index has `N` paragraphs, paragraph candidates satisfy
`1 <= K <= N`; the paragraph serial/range is recorded separately from the RP
sequence number.

When a person enters, continues, resumes, or asks to review an open Page Run
before giving feedback, return the pre-Step review packet from
`../../haipipe-draft/ref/user-check-packet.md`: show the latest complete
candidate, the frozen Structure description for each selected
paragraph, chat-only `S1...Sn` labels, the exact review scope, the proposed next
Step number, and the three direct workspace links. Do not append a new Step
until feedback, acceptance, or an explicit close arrives.

New interaction candidates are proposed through
`../../haipipe-draft/fn/runs.md`. Proposal is read-only planning, not allocation:
it creates no typed RP identity, Ticket, Result, runtime receipt, or live Runs
row. After human selection, resume a matching open Page Run; otherwise allocate
the next typed RP only for a genuinely independent goal. A direct bounded feedback request is an
implicit selection and need not be proposed back to the person first.

While the current structure Run is open, resume it and show no Section or
paragraph candidates. After the structure contract closes, show unallocated
Section candidates and paragraph-group candidates in frozen `P01..PN` reading
order, but allocate only the selected next candidate from the matching kind.
Sequential work is the default; parallel Page Runs require explicit selection
and non-overlapping targets. If the plan changes, recompute unallocated
candidates only and never renumber an allocated typed RP.

Code, search, Discovery, data, rendering, build, and other independently
testable output work stays in the owner-native Task Run lane. A later human
acceptance gate does not convert the producing Task Run into a Page Run.

Use three commit boundaries during interactive work:

```text
Step            current candidate + dependent Bullets → live Draft Space
Page Run close  accepted paragraph group + explicit ready Evidence contract
Page release    all RP Runs + required RE Results → Content + RD delivery + CHECK
```

The foreground Step is deliberately small. Save the verbatim feedback, complete
candidate, affected Bullets, narrow source/protected-scope check, and current
Version/Step; then return the passage. Do not block it on a full build, complete
test suite, export, or browser verification. Evidence records change during a
Step only when the feedback changes a citation, value, or figure requirement.
For every material wording change, save clean Before/After text, a short local
change label, and why the edit was made. Do not infer a broader preference in
the foreground Step. The Runs presenter derives granular visual Track Changes;
neither diff markup nor an unconfirmed preference enters Page Content or shared
policy. Do not duplicate classification in a separate table; status,
navigation, acceptance-only, and presenter-only Steps use `Changes` without a
Track Changes card.

For ordinary follow-up wording feedback, use the rapid foreground budget:
reuse stable context already loaded in the session, read only `working.md`, the
latest saved-result tail, the exact target slice, and its dependent Bullet, then
make one bounded file patch and one narrow scope check. Do not reread the
whole Page or Version, run `outline-pass.py`, run full tests,
verify the browser, or generate delivery before returning the current Step.
Keep the Step record complete but compact; broader preference synthesis and
whole-Page review wait for a checkpoint or an explicit request.

Each ordinary Step is record-first. It captures the person's feedback, performs
the requested edit, records a local reason, and returns the candidate. It does
not perform preference inference, taxonomy building, or whole-Run analysis.
After explicit Page Run closure, prepare one output-only post-run analysis
proposal according to `post-run-analysis.md`. If it is heavy, ask for
explicit approval before dispatching it. Do not wait for approval or analysis
before starting the next Page Run, and never let it mutate the closed writing
record or Page Content. Follow `interactive-execution-policy.md` for all
inter-Run and inter-Step work.

Closing one RP Run never adopts Content or builds delivery. It settles that
Run's text and Bullets and requires every Evidence obligation to be explicit
and ready (`none` or a bound CITE, VALUE, or DISPLAY Result). Required
Discovery, citation, figure, or computation work remains a Supporting Run
feeding an RE and must be ready before the RP becomes complete. CONTENT begins
only after every planned RP is complete and every required RE Result is bound;
one Page-level CONTENT pass then adopts all accepted candidates and reruns the
declared web/LaTeX/Word lanes' fixed Delivery Runs (`run-delivery-<lane>`).

SHAPE and SURVEY remain planning cycles inside the one `run-structure-<slug>`, not one
Run each. They can be used inside this independently closable interactive Run.
`haipipe-draft-writing` (`ref/`)
owns prose revision, `haipipe-draft-review` judges it; `haipipe-draft-writing` adopts agreed wording and builds
delivery. Do not redraft accepted paragraphs at that handoff. This protocol
uses agent-authored Markdown records; it adds no runtime service or UI controls.
