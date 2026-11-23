# Paper theme UI plan

An author who questions a sentence should be able to find the figure behind it, decide on the wording, and resume reading the same paragraph. Design the path in both directions. From the Board, follow a claim into the version and the Section where the paper makes it. From a sentence, follow its evidence back to the source.

## Four screens for design review

| Screen | What the reader sees | What a selection opens |
| --- | --- | --- |
| Theme blueprint · Block UI | Views down the left, Paper and Grant types across the top. Each populated cell names its Sections. Job UI and Task UI use the same matrix. | A Section opens its purpose, layout, source, owning skill and example when one exists. Use Cases opens examples. Grant-specific entries describe the proposed design. |
| Paper Board · Story | Direction, Pitch, Theory, Research Questions, Related, Venues and Story by Section, as their sources become available. In Story by Section, the arc comes first, then the Sections in reader order. | Select Results to see its reader question, moves, claims and displays. Open the writing version to see how it arranges that story. Identify the version by name when there is more than one. |
| Writing Version · Structure | The Board story followed by the version’s Sections in compile order. Each closed row pairs a Section name with the reader’s question. | Expand Results for its moves, figures and paragraph plan. Open the Section draft from that row. Return to the same version and expanded row. |
| Section Task · Write | Manuscript text with evidence and edit marks at the sentences they address. The title tray gathers decisions. | Open a marked sentence for the proposed wording, reason and evidence. Accept or keep the sentence through the Draft workflow. Keep the paragraph, scroll and open card in place during updates. |

The wireframes follow a fictional paper about library opening hours. Its Results sentence claims that longer hours *caused* more evening visits. The linked figure compares visits before and after the change. The proposed wording describes the observed difference. This example tests whether an author can judge an edit using its evidence without losing the paragraph.

## How the UI maps to the files

| Content | Owner | Other places that read it |
| --- | --- | --- |
| Paper question, story arc and claims | Board Story topic | Board Story, Board Displays and version Structure |
| Closest related work | Board related records | Idea and Story |
| Section narrative, order and handoffs for one venue | Writing Job face and version records | Structure and the Section panel for that version |
| A printed value, citation or figure | Its evidence Job and Task result | Board Evidence or Displays and the sentence that uses it |
| A sentence, proposed edit and author's decision | Section Draft Task and its existing writer | Draft Lab, the Section marks and the title tray |

Keep the seven Board views and their current names. Review Content holds the selected view's material. Around the Work gathers its supporting records below. Render a supporting section when it contains something. In the blueprint, a revised manuscript is a use case of Writing Version, and an abstract or reviewer response can use the Draft interface. The three matrices define the wider coverage. [Block views](block-views.md) · [Job views](job-views.md) · [Task views](task-views.md)

## First implementation and acceptance

1. **Connect the existing surfaces.** Walk Story → named version → Results → sentence on the Paper example. Record the first point where a reader has to find the same object again. When multiple versions exist, check the destination against the selected version.
2. **Finish one sentence decision.** Open the figure, return, and accept or keep the wording. Apply an external update elsewhere in the draft. Verify that focus, scroll and open folds persist, and that a reviewed proposal stays handled while its sentence is unchanged.
3. **Check a narrow screen.** At 390 px, stack the Section selector above its content. Keep the sentence card directly below its sentence. In the blueprint, allow the reader to choose one type and inspect its views. Verify keyboard navigation and the return path on the rendered workbench.
4. **Extend by content need.** Check values, citations, displays and submission against their existing contracts. Prototype Grant with a funding call and a specific aim once a Grant example exists. Use that example to decide which shared sections need a distinct layout.

The Figma prototype links the four screens. Its sentence card illustrates the decision before it is taken. Persistence, source navigation and narrow-screen behavior are acceptance checks for the running workbench.
