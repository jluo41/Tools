# page-writing-philosophy-english · Content preview

Planning draft for discussion; not promoted Page Content.

## C1.P1.B1
plan: v0.1
bullet-sha256: e557e9c2dcdb2e6acef024a3f139cfe3506d623c7d8e95ce96f305bf406df0e4

Consider a familiar exchange. We have been working on two paragraphs of a paper's introduction. The opening finally starts with the right subject. A distracting explanation has moved out of the way. The second paragraph now follows naturally from the first. There is one sentence left that feels heavy, so I highlight it and ask the AI to make it easier to read.

## C1.P2.B1
plan: v0.1
bullet-sha256: 0ea4d267ae8094f74ff0317b9f8868902844b69232eb22c50225e3ca4defc578

The response arrives. The sentence is shorter. But the opening has also changed, the distracting explanation has returned, and a transition we had carefully removed is back in a different form.

## C1.P3.B1
plan: v0.1
bullet-sha256: 1b792f89d46b4d2c4c2c3e82fcd34b64500c017cc38ddf665015d6c52371fbc1

Now I have to read both paragraphs again. I have to explain again why the opening mattered. The time I spent making those decisions has become work I must repeat.

## C1.P4.B1
plan: v0.1
bullet-sha256: 7b42a06291b3d291e8946caed8734b9bcd73e1d733c657fd9d121de560ab7c13

This experience is the starting point for how I want to design our Page workflow. I want each round of writing to carry forward what we have already learned about the piece.

## C2.P5.B1
plan: v0.1
bullet-sha256: 87af3c53eab5bedf06723177966fc363ec872081e1ea7306dd78f37be913ab8d

An AI can give me a draft before I have fully decided what I want to say. That can be useful. Reading an actual paragraph exposes questions that an empty page does not. I may discover that I have introduced a method too early, that two apparently different points are the same point, or that the sentence I thought was essential distracts from the argument.

## C2.P6.B1
plan: v0.1
bullet-sha256: 21ac8ddf73e5cfc941e3ab3d93cd93870fd1155787cb6570b357a1ca2f5651b2

My initial instruction might be, “Start with variation in physician behavior.” After reading the draft, I become more specific: “Keep the physician as the subject. The measurement method belongs later. I want the reader to understand the behavior before we explain how we observe it.”

## C2.P7.B1
plan: v0.1
bullet-sha256: 86164b699a16a5bcd97b41422600d60260101e2f7057c89ab2c05088c2d20091

The draft has helped me articulate a requirement I could not have stated as clearly at the beginning. The next draft should inherit that requirement.

## C2.P8.B1
plan: v0.1
bullet-sha256: cab78e5618fbd859a4802c8dcceecad18fc53950d7ed0b0ed15c5b3b6ef7b4ef

This is why I distinguish a Task run from a Page run. When I delegate a task, I usually want to specify the work and its checks, then let the agent organize the execution. It might locate a source, run an analysis, or turn an accepted manuscript into a PDF. Those tasks still require judgment and verification. I simply do not need to participate in every intermediate operation.

## C2.P9.B1
plan: v0.1
bullet-sha256: b9b727dd9e222819cb34a47b79ba8cc13017fd7a73ba59957a2cac07edb40b50

Task run: I say what I want, then hand it over to the agent and leave it to do the work. We do not care how it organizes the work or exactly how steps 1, 2, and 3 proceed.

## C2.P10.B1
plan: v0.1
bullet-sha256: 3f99b120c4aa048d01aa252143a7afdbaa4418903e7df5e207a2db2fd1463eb7

A Page run gives me a different role. I participate in deciding what the work should become. The agent proposes language; I read it and make choices. Those choices change what the agent should do next. A useful writing tool must make room for that exchange throughout the work.

## C2.P11.B1
plan: v0.1
bullet-sha256: 03d069d0c74b0cb82d6182ca8406c48193945771b3c3e2e9c11faa961382eef7

Writing: There is no final result that directly tells us whether the writing is good. The writer still needs to work through every detail of each paragraph and decide the overall direction.

## C3.P12.B1
plan: v0.1
bullet-sha256: b2f9b6dfd4f0cc6e13c788da8bb0b2a0d3fc7c61ba05400b0f74dc3b9bf3a91c

I would begin a section with a small map. Each paragraph has a purpose, and the arrows explain why one paragraph follows another. If I cannot explain an arrow, I may not yet understand the transition. Seeing the whole section helps me notice that a result arrives before the reader knows the question, or that three paragraphs are all trying to establish the same motivation.

## C3.P13.B1
plan: v0.1
bullet-sha256: 97a18f187755ab871f922c5090a3b9b52e26ba8375a07c8053bd73d782c4e153

During the session, we draw the Mermaid diagram first. Then you revise the whole paragraph.

## C3.P14.B1
plan: v0.1
bullet-sha256: f77dca55c45efbe1cf343395c2674a6810411a794689fe9feddb85bbd4f103e5

Then we put one or two paragraphs in front of us. Sometimes three. Enough to read a connected passage and judge its direction, without having to review the whole paper after every change.

## C3.P15.B1
plan: v0.1
bullet-sha256: 3c46a748950e8a51c88ddeded4805938ac377895e54199eb0d664ea4003aeda9

For example, I might show two or three paragraphs in a single turn. Then I can select text, annotate it, and give feedback. You revise based on my feedback.

## C3.P16.B1
plan: v0.1
bullet-sha256: a740c89648bfdea5f2abd4f3f474daa8f8972dd5942611a59721363060862dd7

Beside the prose, I want the planned points and the evidence they need. The left side says what a sentence is trying to do. The right side shows the sentence itself. Looking between them, I can ask whether the prose actually says what the plan promised.

## C3.P17.B1
plan: v0.1
bullet-sha256: b429a1839863f34abd0abe689edc2fe7416557b453ac64d11de350da7dc1de99

I think that during SHAPE, we should shape the bullet points and also look at what the paragraph's actual content looks like.

## C3.P18.B1
plan: v0.1
bullet-sha256: 5df95f2b3135af62d2b9ff1132f7a565dd22424da0ce21e64115f3dd886ab67a

The outline will change during this process. A bullet may look precise until we try to express it. If its point needs two sentences to become clear, both sentences can realize the same bullet. If the sentences make independently removable claims, we should split the bullet and review each claim's support. If a sentence quietly introduces a new claim, we should decide whether that claim belongs and what would support it. We can start from either column and work toward agreement between them.

## C3.P19.B1
plan: v0.1
bullet-sha256: da99b11004d4a90a64ff4498efa2b0b5dc668fe0a0da623914892141ab467fe6

We want each bullet to express one complete point. Its prose may use one sentence or several; the test is whether the point is clear and logically placed.

## C4.P20.B1
plan: v0.1
bullet-sha256: 72c41b5e985346a4e2ac752e54ef776404084831e8386d1ee3a581de29833973

Much of my feedback will be untidy. I may select a phrase and write, “This makes the method sound like the main contribution.” I may dictate a half-finished thought. I may point to the end of a paragraph and say, “We have already said this. What does the reader learn here?”

## C4.P21.B1
plan: v0.1
bullet-sha256: a58e947439c01d516b94bcfc6c01e5bbaa5f3d08ad79871e29a2897dd71a7be7

I want those words preserved. A later summary such as “improved clarity and flow” loses the useful part: what bothered me, what I wanted instead, and why.

## C4.P22.B1
plan: v0.1
bullet-sha256: 1fa37a9c07ccbd4721a0f4618db196161949d5d0e20181a1f6d9e7e503c2ae35

Whatever else we do, the revision process needs to be recorded. My feedback is very valuable and must be preserved. Otherwise, we spend time revising and then lose track of what changed. That effort is wasted.

## C4.P23.B1
plan: v0.1
bullet-sha256: e8ea834eb4540f8054093cf1b753f67cc5c4df9b32160d771efc73f4e9a49253

Each feedback item should remain attached to the text I was looking at. The record should show how the agent interpreted it and what changed. If I gave four comments, I should be able to find all four responses. A comment that could not be applied should still be there, with an explanation.

## C4.P24.B1
plan: v0.1
bullet-sha256: 70fd65229ca488dc78287278da82e74b0ad38ed92693076f8f070d1b44206858

The feedback is item-based: for example, I select three or four passages and give feedback on each one.

## C4.P25.B1
plan: v0.1
bullet-sha256: 6a23b6c50745ce2dcbfae6764b3a466c2a5d8ee1e7b9173bc3a47292fff8237e

The revised passage must then come back as complete paragraphs. A list of changed sentences makes me reconstruct the reading experience in my head. I want to read the actual result, including the sentences that stayed. The version in the response should match the version saved in the workspace, so the sentence I highlight has an unambiguous home.

## C5.P26.B1
plan: v0.1
bullet-sha256: 8f83593fe5b47fc6c6a996e15cecddbb2faba68b45f74863022de61c245031db

The scope of a revision matters just as much as its quality. If I ask for a shorter sentence, I expect a shorter sentence. If I ask to change the emphasis, the agent should examine what the sentence makes prominent. If I say the paragraph's logic is wrong, then we can reconsider its structure and revise the bullets with it.

## C5.P27.B1
plan: v0.1
bullet-sha256: 8a1528447fa903ad01774fe8689ffd7dc4fe5269eaa9b3e9419dadc801870e72

Local edits: Change words, sentences, or clauses. Adjust the subject, verb, or sentence structure without changing the meaning. Shift the emphasis and make the logic read smoothly, so a newly introduced element does not distract from the main point. Paragraph rewrite: If the whole paragraph does not work and its logic is confused, it may need to be rewritten.

## C5.P28.B1
plan: v0.1
bullet-sha256: 7b16727b0263529b5992826d5a2c012ac04b691bd9336257d3a250347bb80811

Once I say a paragraph is right, that decision should survive the next turn. We may need to reopen it later, but we should know that we are doing so and why. Otherwise, every small request becomes an invitation to reconsider everything, and the author must keep guarding sentences that were already settled.

## C5.P29.B1
plan: v0.1
bullet-sha256: deae58d2c63748ef8e44e962c0aa0e0d01f882d82dd4b79ea5c4443b8718a010

For example, once we have finished a paragraph and settled its bullets during outlining and drafting, we consider that paragraph settled for now and stop changing it.

## C6.P30.B1
plan: v0.1
bullet-sha256: 80e1e06eca923a3613faa171dac6a0d5bc1aa7aeffa6a4a2aad3348c83e8b514

The run gives this work a durable identity. It might cover an entire introduction, or only two paragraphs that need attention. A run contains steps. Each step records one meaningful input and the response it produced: the starting brief and first draft, then the comments and revised draft, and eventually the decision to accept the result. A version marks a revision episode in that history. It does not add another execution level between a run and its steps.

## C6.P31.B1
plan: v0.1
bullet-sha256: 1970a0b0518ece3b16e1dc2ef20abaddae8f8cf41acf19be7031305505da8aa4

A step is under the run. Do you get it?

## C6.P32.B1
plan: v0.1
bullet-sha256: 7bbb991c7c5d2e337cb8629a81a44af562cb1405a70a5a09dfc3a230f8b446ef

A step should be small enough to understand. I should be able to open it and see the old wording, my feedback, the change, and the resulting passage. The current workspace shows what we are writing now. The history lets us recover what we wrote before and the decisions that brought us here.

## C6.P33.B1
plan: v0.1
bullet-sha256: 35a0804cc33feb1c5aea559d581809b1802c8d503ce6d82b58f0397b829bbca0

Waiting for me to read is part of the process. The model does not need to stay running while I am away. When I return, perhaps in a different session, the saved work should tell us which paragraphs are accepted, which comments remain open, and where to continue.

## C7.P34.B1
plan: v0.1
bullet-sha256: f889cfc68c18e11660d09f7722aaa362cae6874487c60a8762b3472f973a6198

Speed matters here too. If I comment on one sentence, I want the revised passage back while I still remember what I was trying to fix. A full PDF build or a wider evidence search can happen separately when needed. The comment and the new wording still need to be saved promptly. Otherwise, the next interruption could lose the very exchange that would have helped us resume.

## C7.P35.B1
plan: v0.1
bullet-sha256: 917d1e7ebf358e55017df0d2d8c3866ce383f6de072a4f9658aa8b1482e19f49

Some things can run in the background, right? But when we are making adjustments and using the system, there should not be too much delay.

## C7.P36.B1
plan: v0.1
bullet-sha256: 3928c0ae72267c0a8047ace02e078cbf4190de3f270237501425c66118b84613

There will still be days when I need an uninterrupted hour to rethink a section. I want the smaller moments to count as well. A five-minute exchange might settle a transition, preserve a new idea, or explain why a sentence feels wrong. When I sit down for longer, those decisions should already be there. I want to resume the thought as readily as I reopen the document.

## C7.P37.B1
plan: v0.1
bullet-sha256: c1e4a35fa001f36c1ccc7020acd071bbf757adbf38a02df516e34951bd0d8a80

When I accept a version, we keep it. If I come back a week later with a new idea, we begin another version from that accepted text. I can change my mind without erasing the earlier decision. If an older sentence turns out to be better, we can bring it forward and record the choice.

## C8.P38.B1
plan: v0.1
bullet-sha256: 2a0c769eb5beb8c4fd2d2d18541238e91e7db325cc7e213c0a12a6ea7f7e5947

Evidence work fits alongside this exchange. We can agree on a paragraph's organization while a citation or numerical result is still being checked. Any missing support stays explicit in the working materials. An agent can carry out the search or calculation and return the result.

## C8.P39.B1
plan: v0.1
bullet-sha256: d0222c9c07804d1ab4da5a7f5d094fb414b4860fe1219431b951c3017e756fd0

For evidence, for example, we can use Discovery to find citations, or run regressions or code to supply evidence, and insert it into the draft we have already settled.

## C8.P40.B1
plan: v0.1
bullet-sha256: aefaffb6870cc6d88ff72dfdc7e959f0024cbe6e96f9ee78838a4e1d1d5e80ad

Sometimes the result fits the claim, and we fill the agreed place. Sometimes it contradicts what we had hoped to say. Then we bring that finding back to the affected paragraph. Human agreement about wording cannot make unsupported evidence true, and an evidence worker should not quietly rewrite the argument to conceal a mismatch.

## C8.P41.B1
plan: v0.1
bullet-sha256: c6d0d72191a04949f8b93e1c82f724b8f04c006227d9d19521fd35b6d9a21d0e

Once the wording and evidence are settled, producing the formal page and its exports should carry that work forward faithfully. A PDF build should not become another unrequested prose revision. I want to recognize the paragraph we agreed on when I open the finished document.

## C8.P42.B1
plan: v0.1
bullet-sha256: 2c74ee5c9ee31942da301f0ae5f7fdd78e1380f2a0f6833b70b3faaaf0adb64c

I will only check these: The Outline table Display PDFs or other evidence PDFs The final Page PDF

## C9.P43.B1
plan: v0.1
bullet-sha256: 531db980732111536286c7d70711dc34b3c9c6d70f91f7463f781471f86f3bc0

Over time, these records could also teach us how I prefer to write. Some preferences may recur: concrete subjects, a clear purpose for each sentence, explanations that arrive when the reader needs them. Others belong to a particular passage. “Do not discuss measurement here” may be exactly right for an opening paragraph and exactly wrong for the next section.

## C9.P44.B1
plan: v0.1
bullet-sha256: 94d675f4dd694b5b8266d4d5d1eded0c63d54bd54cfc9a650efbf7b1dd6ea512

Across many runs or rounds, we can keep these records to summarize and reflect on later, and turn those reflections into writing rules for future work.

## C9.P45.B1
plan: v0.1
bullet-sha256: 07172eb7743fb5a882ed2bea885fb02cae76bde7c1b5fb968439e8cc4f963370

Keeping the context makes that distinction possible. A useful writing rule can point back to examples of where it helped. We can examine the original comment and its effect before deciding to apply it more widely.

## C10.P46.B1
plan: v0.1
bullet-sha256: 10674c6fa061d35609a2e9260ce1c25cad83a514e99e255b573011f41ac74466

I want to be able to return wherever I happen to be. Writing should not require me to sit down in an office, or find a table at a coffee shop, before I can begin. Sometimes I have ten minutes between meetings. Sometimes I am waiting for an appointment and suddenly understand what the second paragraph should say. I want to open that paragraph and work on it while the thought is still clear.

## C10.P47.B1
plan: v0.1
bullet-sha256: a34677d8da743b0215ed9bd6be44f0aec4c7bbd84dd77d2637d1f9375737d884

We should not have to sit down at a desk in an office, or settle in at Starbucks and order a coffee, before we start writing. I want to be able to say, anytime and anywhere, "I want to write this paragraph" or "I want to write this section," and pick it up from where we left off. You know what I mean? I can pick it up again.

## C10.P48.B1
plan: v0.1
bullet-sha256: bd488652128ce1b538f8fa6a18dd1fb126db8d416e960efa6a557571dec33b78

Those ten minutes can disappear before I write a word. I open a Word document and find the text we saved. But if we saved only the manuscript, I must remember the discussion around it. Why did we remove that example? Was this sentence agreed, or was it still a suggestion? What was bothering me about the transition? The words are there. Recovering the reasons can take the whole break.

## C10.P49.B1
plan: v0.1
bullet-sha256: 52fec9134950fefb1e3073edff60a410177bcd1418de5d118ce79aaff24436bc

If I simply open a Word document, I have only the text; the context from our earlier work is gone. What we are doing now is saving that context too, so we can move smoothly to the next step.

## C10.P50.B1
plan: v0.1
bullet-sha256: aa639d8a98c9ed242078eaf9b76c9baadbbeb839f0c1a2772d99e5b9beb74994

This is what I mean by vibe writing, alongside vibe coding. I want to describe what I have in mind, read what the AI proposes, and shape the paragraph or section through our exchange. I should be able to select a sentence on my phone, dictate a rough objection, read a revision, and leave. Later, on another device or in another conversation, we should continue from that exchange. I should not have to explain the section again.

## C10.P51.B1
plan: v0.1
bullet-sha256: 8eade331344fb29a0d297bcfc36cc12240e22093b7bb2d4894ae0b98563e193e

Vibe writing and vibe coding. That is what I said.

## C10.P52.B1
plan: v0.1
bullet-sha256: ba51b4fa0d9a35b308e044fc5bb79a2e35765bbb6b4afc595783f348ab7c2581

The context we save must help with that return. Beside the current passage, I want a short account of where we stopped: the opening is agreed; the next paragraph still introduces measurement too early; one citation is being checked. My original comment should remain available if the summary leaves something out. The paragraph map can remind me where this passage leads. I can then spend the few minutes I have making the next decision.

## C10.P53.B1
plan: v0.1
bullet-sha256: 01ea53b2ef102e2b3d32a0112eb6d0c2504eb6736455c01235a3ddb8959b758c

Saving every message is useful, but making me reread the entire conversation would defeat the purpose. The tool should recover the relevant working state before it proposes another change. It needs to distinguish a settled choice from an open question, and an abandoned suggestion from the current plan. That knowledge should live with the work, so continuing does not depend on keeping one particular chat alive.

## C10.P54.B1
plan: v0.1
bullet-sha256: 436952a71d0ec359309943595e5871f1a0fa1976132deb7d226d557100ae2fb4

I do not want maintaining this history to become another job for the author. My part should remain familiar: read, select, comment, discuss, accept, continue. The system should preserve the exchange as it happens. The reading surface can stay quiet, with the paragraphs in front of me and direct links to their bullets and evidence.

## C10.P55.B1
plan: v0.1
bullet-sha256: fc8254ca5378ede8362f87b84faeeba1e718dbefad42e32c186cb929779d339a

That is the experience I want to return to the next morning. I open the work, find the paragraph we finally agreed on, and see the reason we chose its opening. The second paragraph still has one unresolved comment. I select the sentence, explain what I mean, and we continue from there.

## C10.P56.B1
plan: v0.1
bullet-sha256: 3c35280653e417bc952775d781f3fce010b940c243e558acb51846e0683f0e94

Edition note: Blockquotes are translations or light edits of JL's words, not verbatim English quotations. See the original-quotation edition for the exact words. The example exchanges are illustrative.

## C10.P57.B1
plan: v0.1
bullet-sha256: 1fdb651cfb2ab12182a9c11650021f9b88af165dc9f24172e509eded3de34c7b

Design note: This essay describes the intended Page writing experience discussed on September 11, 2026, not a claim that every capability is implemented.

## C10.P58.B1
plan: v0.1
bullet-sha256: ee655e360310ad711a2c0d7a793b5392c11bdeeec1487087f92a57c44d0c1a58

Illustrations: Detailed edition . Cartoon edition . Compare both series
