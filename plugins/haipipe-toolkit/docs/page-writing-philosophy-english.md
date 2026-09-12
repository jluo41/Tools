# The Paragraph We Finally Agreed On

*Why I want AI writing tools to remember the decisions behind the draft.*

*English reading edition. JL's blockquotes have been translated from Chinese where needed and lightly edited for spelling, grammar, and repeated spoken fillers. They are not verbatim English quotations. The meaning, emphasis, and order are preserved; the surrounding prose and section headings are unchanged. The example exchanges in the surrounding prose remain illustrative, not transcripts. Read the [original-quotation edition](page-writing-philosophy.md) for JL's exact words.*

Consider a familiar exchange. We have been working on two paragraphs of a paper's introduction. The opening finally starts with the right subject. A distracting explanation has moved out of the way. The second paragraph now follows naturally from the first. There is one sentence left that feels heavy, so I highlight it and ask the AI to make it easier to read.

The response arrives. The sentence is shorter. But the opening has also changed, the distracting explanation has returned, and a transition we had carefully removed is back in a different form.

Now I have to read both paragraphs again. I have to explain again why the opening mattered. The time I spent making those decisions has become work I must repeat.

This experience is the starting point for how I want to design our Page workflow. I want each round of writing to carry forward what we have already learned about the piece.

## A draft helps me discover what I mean

An AI can give me a draft before I have fully decided what I want to say. That can be useful. Reading an actual paragraph exposes questions that an empty page does not. I may discover that I have introduced a method too early, that two apparently different points are the same point, or that the sentence I thought was essential distracts from the argument.

My initial instruction might be, “Start with variation in physician behavior.” After reading the draft, I become more specific: “Keep the physician as the subject. The measurement method belongs later. I want the reader to understand the behavior before we explain how we observe it.”

The draft has helped me articulate a requirement I could not have stated as clearly at the beginning. The next draft should inherit that requirement.

This is why I distinguish a Task run from a Page run. When I delegate a task, I usually want to specify the work and its checks, then let the agent organize the execution. It might locate a source, run an analysis, or turn an accepted manuscript into a PDF. Those tasks still require judgment and verification. I simply do not need to participate in every intermediate operation.

> Task run: I say what I want, then hand it over to the agent and leave it to do the work. We do not care how it organizes the work or exactly how steps 1, 2, and 3 proceed.

A Page run gives me a different role. I participate in deciding what the work should become. The agent proposes language; I read it and make choices. Those choices change what the agent should do next. A useful writing tool must make room for that exchange throughout the work.

> Writing: There is no final result that directly tells us whether the writing is good. The writer still needs to work through every detail of each paragraph and decide the overall direction.

## See the argument before polishing the sentences

I would begin a section with a small map. Each paragraph has a purpose, and the arrows explain why one paragraph follows another. If I cannot explain an arrow, I may not yet understand the transition. Seeing the whole section helps me notice that a result arrives before the reader knows the question, or that three paragraphs are all trying to establish the same motivation.

> During the session, we draw the Mermaid diagram first. Then you revise the whole paragraph.

Then we put one or two paragraphs in front of us. Sometimes three. Enough to read a connected passage and judge its direction, without having to review the whole paper after every change.

> For example, I might show two or three paragraphs in a single turn. Then I can select text, annotate it, and give feedback. You revise based on my feedback.

Beside the prose, I want the planned points and the evidence they need. The left side says what a sentence is trying to do. The right side shows the sentence itself. Looking between them, I can ask whether the prose actually says what the plan promised.

> I think that during SHAPE, we should shape the bullet points and also look at what the paragraph's actual content looks like.

The outline will change during this process. A bullet may look precise until we try to express it. If it needs two sentences to make two separate points, we should revisit the bullet. If a sentence quietly introduces a new claim, we should decide whether that claim belongs and what would support it. We can start from either column and work toward agreement between them.

> We want one sentence to express one point. Each point is one bullet point. So we still need to map bullet points to sentences.

## Keep the feedback with the words it refers to

Much of my feedback will be untidy. I may select a phrase and write, “This makes the method sound like the main contribution.” I may dictate a half-finished thought. I may point to the end of a paragraph and say, “We have already said this. What does the reader learn here?”

I want those words preserved. A later summary such as “improved clarity and flow” loses the useful part: what bothered me, what I wanted instead, and why.

> Whatever else we do, the revision process needs to be recorded. My feedback is very valuable and must be preserved. Otherwise, we spend time revising and then lose track of what changed. That effort is wasted.

Each feedback item should remain attached to the text I was looking at. The record should show how the agent interpreted it and what changed. If I gave four comments, I should be able to find all four responses. A comment that could not be applied should still be there, with an explanation.

> The feedback is item-based: for example, I select three or four passages and give feedback on each one.

The revised passage must then come back as complete paragraphs. A list of changed sentences makes me reconstruct the reading experience in my head. I want to read the actual result, including the sentences that stayed. The version in the response should match the version saved in the workspace, so the sentence I highlight has an unambiguous home.

## A sentence edit should stay a sentence edit

The scope of a revision matters just as much as its quality. If I ask for a shorter sentence, I expect a shorter sentence. If I ask to change the emphasis, the agent should examine what the sentence makes prominent. If I say the paragraph's logic is wrong, then we can reconsider its structure and revise the bullets with it.

> 1. Local edits: Change words, sentences, or clauses. Adjust the subject, verb, or sentence structure without changing the meaning. Shift the emphasis and make the logic read smoothly, so a newly introduced element does not distract from the main point.
>
> 2. Paragraph rewrite: If the whole paragraph does not work and its logic is confused, it may need to be rewritten.

Once I say a paragraph is right, that decision should survive the next turn. We may need to reopen it later, but we should know that we are doing so and why. Otherwise, every small request becomes an invitation to reconsider everything, and the author must keep guarding sentences that were already settled.

> For example, once we have finished a paragraph and settled its bullets during outlining and drafting, we consider that paragraph settled for now and stop changing it.

## One run, with steps we can return to

The run gives this work a durable identity. It might cover an entire introduction, or only two paragraphs that need attention. A run contains steps. Each step records one meaningful input and the response it produced: the starting brief and first draft, then the comments and revised draft, and eventually the decision to accept the result. A version marks a revision episode in that history. It does not add another execution level between a run and its steps.

> A step is under the run. Do you get it?

A step should be small enough to understand. I should be able to open it and see the old wording, my feedback, the change, and the resulting passage. The current workspace shows what we are writing now. The history lets us recover what we wrote before and the decisions that brought us here.

Waiting for me to read is part of the process. The model does not need to stay running while I am away. When I return, perhaps in a different session, the saved work should tell us which paragraphs are accepted, which comments remain open, and where to continue.

## Vibe writing, wherever I happen to be

I want to be able to return wherever I happen to be. Writing should not require me to sit down in an office, or find a table at a coffee shop, before I can begin. Sometimes I have ten minutes between meetings. Sometimes I am waiting for an appointment and suddenly understand what the second paragraph should say. I want to open that paragraph and work on it while the thought is still clear.

> We should not have to sit down at a desk in an office, or settle in at Starbucks and order a coffee, before we start writing. I want to be able to say, anytime and anywhere, "I want to write this paragraph" or "I want to write this section," and pick it up from where we left off. You know what I mean? I can pick it up again.

Those ten minutes can disappear before I write a word. I open a Word document and find the text we saved. But if we saved only the manuscript, I must remember the discussion around it. Why did we remove that example? Was this sentence agreed, or was it still a suggestion? What was bothering me about the transition? The words are there. Recovering the reasons can take the whole break.

> If I simply open a Word document, I have only the text; the context from our earlier work is gone. What we are doing now is saving that context too, so we can move smoothly to the next step.

This is what I mean by vibe writing, alongside vibe coding. I want to describe what I have in mind, read what the AI proposes, and shape the paragraph or section through our exchange. I should be able to select a sentence on my phone, dictate a rough objection, read a revision, and leave. Later, on another device or in another conversation, we should continue from that exchange. I should not have to explain the section again.

> Vibe writing and vibe coding. That is what I said.

The context we save must help with that return. Beside the current passage, I want a short account of where we stopped: the opening is agreed; the next paragraph still introduces measurement too early; one citation is being checked. My original comment should remain available if the summary leaves something out. The paragraph map can remind me where this passage leads. I can then spend the few minutes I have making the next decision.

Saving every message is useful, but making me reread the entire conversation would defeat the purpose. The tool should recover the relevant working state before it proposes another change. It needs to distinguish a settled choice from an open question, and an abandoned suggestion from the current plan. That knowledge should live with the work, so continuing does not depend on keeping one particular chat alive.

## Return the revision while the thought is fresh

Speed matters here too. If I comment on one sentence, I want the revised passage back while I still remember what I was trying to fix. A full PDF build or a wider evidence search can happen separately when needed. The comment and the new wording still need to be saved promptly. Otherwise, the next interruption could lose the very exchange that would have helped us resume.

> Some things can run in the background, right? But when we are making adjustments and using the system, there should not be too much delay.

There will still be days when I need an uninterrupted hour to rethink a section. I want the smaller moments to count as well. A five-minute exchange might settle a transition, preserve a new idea, or explain why a sentence feels wrong. When I sit down for longer, those decisions should already be there. I want to resume the thought as readily as I reopen the document.

When I accept a version, we keep it. If I come back a week later with a new idea, we begin another version from that accepted text. I can change my mind without erasing the earlier decision. If an older sentence turns out to be better, we can bring it forward and record the choice.

## Evidence can change what we are able to say

Evidence work fits alongside this exchange. We can agree on a paragraph's organization while a citation or numerical result is still being checked. Any missing support stays explicit in the working materials. An agent can carry out the search or calculation and return the result.

> For evidence, for example, we can use Discovery to find citations, or run regressions or code to supply evidence, and insert it into the draft we have already settled.

Sometimes the result fits the claim, and we fill the agreed place. Sometimes it contradicts what we had hoped to say. Then we bring that finding back to the affected paragraph. Human agreement about wording cannot make unsupported evidence true, and an evidence worker should not quietly rewrite the argument to conceal a mismatch.

Once the wording and evidence are settled, producing the formal page and its exports should carry that work forward faithfully. A PDF build should not become another unrequested prose revision. I want to recognize the paragraph we agreed on when I open the finished document.

> I will only check these:
>
> 1. The Outline table
> 2. Display PDFs or other evidence PDFs
> 3. The final Page PDF

## Let repeated feedback teach us how to write

Over time, these records could also teach us how I prefer to write. Some preferences may recur: concrete subjects, a clear purpose for each sentence, explanations that arrive when the reader needs them. Others belong to a particular passage. “Do not discuss measurement here” may be exactly right for an opening paragraph and exactly wrong for the next section.

> Across many runs or rounds, we can keep these records to summarize and reflect on later, and turn those reflections into writing rules for future work.

Keeping the context makes that distinction possible. A useful writing rule can point back to examples of where it helped. We can examine the original comment and its effect before deciding to apply it more widely.

I do not want maintaining this history to become another job for the author. My part should remain familiar: read, select, comment, discuss, accept, continue. The system should preserve the exchange as it happens. The reading surface can stay quiet, with the paragraphs in front of me and direct links to their bullets and evidence.

That is the experience I want to return to the next morning. I open the work, find the paragraph we finally agreed on, and see the reason we chose its opening. The second paragraph still has one unresolved comment. I select the sentence, explain what I mean, and we continue from there.

---

*Design note: This essay expresses the Page writing philosophy discussed on September 11, 2026. It describes the intended experience, not a claim that every interface, synchronization, or background capability has been implemented.*
