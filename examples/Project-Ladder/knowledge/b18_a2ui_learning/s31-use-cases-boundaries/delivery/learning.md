# Use Cases and Boundaries

## A decision to explore

A2UI is a useful candidate when an agent or server must compose an interface for the current task while the host app controls the available components. A stable form with a fixed sequence may be simpler to maintain as ordinary application UI. The second statement is a design judgement, not an A2UI requirement. [Resource 6](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

| Situation | Design direction to investigate |
|---|---|
| The task changes which controls are useful | A catalog-constrained, dynamic surface |
| The same form is used every time | A fixed application form |
| The agent invents a component the client lacks | Catalog and validation agreement |
| The UI looks correct but triggers a sensitive operation | Application authorization and action handling |

## Connect the topics

Resources identifies the version and evidence. Concepts explains structure and values. Methods follows the action boundary. These perspectives can support **one** practice Job; each topic does not require its own Job or Task.

## A bounded practice proposal

Use one selection card and fixed input messages to test rendering, changing a value, emitting an action, and applying a response. Compare the observed sequence with s21's observation sheet. An official quickstart can provide a reference implementation. [Resource 5](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

The four Studios contain learning material. An executable practice would additionally need a pinned implementation and a matching execution contract. No Job, Task or Run result is asserted by this proposal.

## What that practice could establish

- Known input messages produce the expected interface.
- A particular explicit action carries the expected value.
- The addressed interface reflects the tested update.

It would not establish general model reliability, production readiness, or the learner's understanding. A learner should separately explain the mechanism and a counterexample.

## Try explaining

Choose between a fixed sign-up form and a travel assistant that assembles different controls for different requests. Explain your choice for each. Identify which claim needs an executable check and which needs a product decision.
