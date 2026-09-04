# field-test · version history

0.4.0 · 260829 · JL
- RENAMED `haipipe-fieldtest` -> `field-test`, two changes in one. The `haipipe-` prefix marks a skill that OPERATES the HAI-Pipe lifecycle and speaks its vocabulary (stage letters, task-folders, Pages, units); this one is a method that takes any skill family, real work and a written expectation, and returns law patches. It joins the unprefixed methods in `0_utils`: `claude-response-format`, `diagram-ascii`, `notebook-cell-python`, and `remote-error` (renamed the same day, same reason). JL: "I want to rename the /haipipe-fieldtest to be /field-test as well."
- `fieldtest` written as one word became `field-test`, matching the hyphen the description itself has used since 0.1.0 ("The field-test method for a skill family"). The bare word `fieldtest` STAYS in the trigger list as an alias, because that is what a person types.
- Swept: `SKILL.md:2` name, `:11` title, `:4` trigger `/field-test`; `haipipe-skillset-status/SKILL.md:36`; `remote-error/SKILL.md:21,315` + its CHANGELOG; `haipipe-insight-workflow/CHANGELOG.md:25`. The friction-log folder the method produces followed the id: `diagrams/PaperSkillBoard-260725/_fieldtest/` -> `_field-test/`, with `board.md:58` updated.
- No rule, desk, law or scorecard column changed. This is a rename only.

0.3.0 · 260828 · JL
- THE SCORECARD: every run now records, at settle, time (from `date` stamps, field and design desks separately), tokens (operator-pasted `/cost` for the field session, exact task receipts for every dispatched judge), format quality (checker before→after, CHECK rounds to CLOSE), semantic quality (ledger tally, frictions by severity, the independent CHECK's verdict), a TAX LINE naming every avoidable spend with its lesson, and a rate with unit and grade named. JL: "把 metric evaluation 也加进去 … 记录下来之后,以后我们做 Field Test 就不用说这么多了."
- Commission anatomy gains ⑧ THE clock: stamps from the `date` command, never estimated — the 260828 page-family run caught itself fabricating stamps (its F12) and confessed; the header records start, the Close block records end and carries the /cost paste.
- Law 9, metrics are recorded never recalled: a scorecard rebuilt from memory is the same defect as an expectation written after the run.
- Calibration baked in from the two 260828 runs: repair-grade 13 pages / 14 min / 12 frictions; close-grade 1 page / 30 min / 213k judge tokens with ~27% settling as tax (a judge bought against a known-dirty version; a rework a skipped exit-sweep forced).


0.1.0 · 260827 · JL
- New toolkit-wide method skill, named and extracted from the insight-family validation run of the same day (A00 board, 14 frictions, session pair InsightPart / Test2Learn-Insight).
- Briefly born as `haipipe-coldrun`; renamed within the hour on JL's correction that the method's center is not the cold context but the REAL TASK run against a PRE-REGISTERED EXPECTATION — the rename added the expectation ledger, the three settle outcomes (MATCH / SKILL GAP / EXPECTATION GAP), and the law that the field desk never sees the ledger.
- Three desks (design / field / monitor), the seven-part commission packet, eight laws (expectation before run, freeze the baseline, designer never grades, four-valued friction, behavior pass ≠ done, three triage bins, loop until dry on fresh slices, monitor never intervenes).
- Generalizes the board family's QF2 fresh-agent-run from a one-shot route proof to a convergence loop whose unit of progress is one settled divergence.

0.2.0 · 260828 · JL
- The automated loop: the field desk gains its spawned-subagent form (cold by construction; commission = prompt, report = return, the human message-bus disappears), and the run is bracketed by the auto charter — person signs decision classes in, signatures and joined-ledger review out. The four quality guards (expectation ledger, refusal-is-convergence, receipts on pages, teeth proven to FAIL) are untouched: the charter automates attention, never authority.
- Prompted by JL's full-automation directive after round 2 of the insight-family fieldtest, in which the human relayed four decisions verbatim — the charter is that relay, formalized and bounded.

0.2.1 · 260828 · JL
- Packet anatomy ③ gains the vocabulary clause: commissions use the target family's own state words — round 3's `proposed`-for-`planned` slip was caught and corrected by the field desk, the first time the executor corrected the designer.
