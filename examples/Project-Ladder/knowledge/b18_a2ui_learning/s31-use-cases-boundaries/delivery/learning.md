# Use Cases and Boundaries

## A decision to explore

**A2UI fits when the screen depends on the task and the app keeps the components.**

- ✅ **Good fit:** an agent composes the interface for this request, from the app's catalog.
- ➖ **Maybe not:** a stable form with a fixed order is often simpler as ordinary app UI (a design judgement, not an A2UI rule).

| 🧭 Situation | 🔍 Direction to look at |
|---|---|
| 🔀 The task changes which controls help | a dynamic surface, limited by the catalog |
| 📝 The same form every time | a fixed app form |
| 🧩 The agent asks for a component the app lacks | catalog and validation agree |
| ⚠️ It looks right but triggers a sensitive action | app authorization and action handling |

🔍 **Look for:** "When to use A2UI" in [Resource 6](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

## Connect the topics

**Every topic feeds the same decision; one practice Job is enough.**

- 📚 **Resource** (s01): which version and which evidence
- 🧭 **Method** (s11, s21, s22): structure and values, the action boundary, the six steps
- 🤔 **Question** (s41, s42): what changes in a chatbot, and who writes the JSON
- 🧪 One practice Job (j01) can serve them all; no topic needs its own Job or Task.

## A bounded practice proposal

**One card, fixed messages, four checks.**

- 🆕 Render one selection card from fixed input messages.
- 🔢 Change a value on the device.
- 📤 Send one action.
- 📥 Apply one response.
- 🔍 Compare what you see with the table in s21, step 5; Travel A2UI is a reference ([Resource 5](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)).

⚠️ A plan only: no Job, Task or Run result is claimed. Running it needs a pinned version and a matching execution contract.

## What that practice could establish

**What it would show, and what it would not.**

- ✅ Known messages produce the expected interface.
- ✅ An explicit action carries the expected value.
- ✅ The addressed interface shows the tested update.
- ❌ Not: that a model is reliable in general.
- ❌ Not: that it is ready for production.
- ❌ Not: that the learner understood; that needs its own explanation and a counterexample.

## Try explaining

**Choose for two apps, and say why.**

- 📝 A fixed sign-up form.
- 🧳 A travel assistant that builds different controls for each request.
- ⚖️ For each: which claim needs a check you can run, and which needs a product decision?
