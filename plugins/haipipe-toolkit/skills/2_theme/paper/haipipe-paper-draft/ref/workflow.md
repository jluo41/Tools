# The Section workflow · W0 to W5, from an empty Section to a draft ready for the person

JL 261116: "I want to have a /haipipe-paper-draft workflow, so when I open a new secton draft, then I can run the tasks
one by one and get a close to review draft"; "the editing should be accept by AI themselves, after several rounds of no
imrpovements, or something not sure, the AI will leave the comments, and human will join".

The same method as [`section-method.md`](section-method.md) (S1 to S3, D1 to D3), put in order as six steps. Each step
is judged from a file, never from memory: `cli/section_workflow.py <Section Task>` prints the six lines and the next step.

```text
W0 examples ─▶ W1 plan 🙋 sign ─▶ W2 write ─▶ W3 rate ─▶ W4 fix ─┐
                                                ▲                 │ something kept
                                                └─────────────────┘
                                     two rounds kept nothing, or all 8+ ─▶ W5 ready 🙋
```

| Step | Who | Done when (read from disk) |
| --- | --- | --- |
| W0 Examples | the session (SKILL.md § Examples first) | the face's `examples:` names a topic with section screenshots, or says `none · <reason>` |
| W1 Plan | the session proposes, **the person signs** | the newest Draft's `approved:` holds ✅ (`page.py sign`) |
| W2 Write | haipipe-draft-writing | § 3 has a sentence for every § 1 Bullet; then `page.py adopt` and `export` |
| W3 Rate | fresh agents: `haipipe-draft-eval-paragraph-agent`, `haipipe-draft-eval-sentence-agent` | the revise record's newest Pass with sentence lines rated the newest Draft version |
| W4 Fix loop | writer, then `haipipe-draft-ab-reader-agent` | every sentence 8 or more, or each one under 8 has an open AI comment |
| W5 Ready | the session builds; **the person joins** | the Section's PDF under `delivery/<job>/<task>/` is newer than the Draft |

## W4, the loop

1. Each sentence under 8 gets a rewrite; a paragraph with three or more under 8 is rewritten whole (section-method D2).
2. A fresh blind A/B reader judges each pair. "Easier, same meaning" is kept, and the AI writes it into the next Draft
   version itself: no card waits for the person. Anything else is dropped.
3. A sentence with no fix, or whose fix was dropped, gets an AI comment in `draft/records/<stem>-comments.md`: one
   plain question about that sentence only (section-method D3).
4. W3 rates again. Stop when every sentence is 8 or more, or after two rounds in a row that kept nothing.
5. Never touched: a sentence the person checked (✓), a claim, a number, a story choice.

## What the person sees at W5

The open AI comments first, then each sentence the loop changed (its 🕘 history shows old and new), then a ✓ per
sentence (D4, D5). Each Pass of W3 writes a `Standard:` line naming the rule files it rated under and their dates.

## Not built yet

One Run per step (`runs/rNN_wN_<slug>/`), the 🤖 mark on AI-changed sentences, and the step line in Draft Lab. Until
then the step state comes from `cli/section_workflow.py`.
