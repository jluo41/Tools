# Release use choices

for: b02.j01.t04-s03:labeling_walkthrough.example_response_safety.example_expression @ example_release_choices

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form. -->

Round e02 is released; these three choices say how its labels are used.

## Q1 · Serving executor
Two stand-in executors met the floors; one labels new chats.
**Which executor labels new chats?**
- [x] A · Stand-in A, which reads the rules.
- [ ] B · Stand-in B, which fears refusals.
Why A: Its Test kappa met the floor; B's Train kappa did not.

## Q2 · Fresh check
The staging set was audited; unseen chats were not.
**How is a claim about unseen chats checked?**
- [x] A · Label 30 fresh synthetic chats blind, then compare.
- [ ] B · Make no claim beyond the staging set.
Why A: A claim needs data the rounds never saw.

## Q3 · Next round
Rule questions go back to meaning; wording alone can still improve.
**Does expression run round e03?**
- [x] A · No; reopen only when a round report asks.
- [ ] B · Yes, to lower the cost per item.
Why A: e02 met every criterion at no model cost.
