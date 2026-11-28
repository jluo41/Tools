# Use Cases and Boundaries

## Where you start

**Two apps; one question decides which gets A2UI.**

- 🧳 **A travel assistant:** each request needs different controls (flights today, hotels tomorrow).
- 📝 **A sign-up form:** the same fields, in the same order, every time.
- 💡 The method below decides between them, and names what to check either way.

🔍 **Look for:** "When to use A2UI" in [Resource 6](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

## 1. Ask the question

**Does the request change what the screen should show?**

- 🔀 **Yes:** "BER to SFO today, 2 back on Oct 19" needs two flight cards with passenger counts; another request needs other controls.
- ➖ **No:** a sign-up form asks for the same name, email and password every time.

✅ **You know it when:** you can answer yes or no for one screen of your own app.

## 2. Choose

**Yes leads to an A2UI surface; no leads to ordinary app UI.**

- ✅ **Where it helps:** the agent composes the screen for this request, from the app's catalog.
- ❌ **Where it does not:** a fixed form is often simpler to build and test as ordinary app UI.
- ⚠️ This is a design judgement, not an A2UI rule.

| 🧭 Situation | 🔍 Choose |
|---|---|
| 🔀 The task changes which controls help | an A2UI surface, limited by the catalog |
| 📝 The same form every time | a fixed app form |

✅ **You know it when:** you can say both sides for your screen.

## 3. Check the boundaries

**Two limits hold whichever you choose.**

- 🧩 **A component the app lacks:** the agent may ask for one; the catalog rejects it (see s42, step ③).
- ⚠️ **A sensitive action:** a card that looks right may trigger a payment; your app checks and authorizes the action.

🔍 **Look for:** the catalog as "the guardrail" in [Resource 5](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

✅ **You know it when:** you can name who stops each one.

## 4. Plan a practice

**One card, fixed messages, four checks; a plan, not a result.**

- 🆕 Render one selection card from fixed input messages.
- 🔢 Change a value on the device.
- 📤 Send one action.
- 📥 Apply one response.
- 🔗 It draws on s11 (structure and values), s21 (the tap) and s22 (the steps); the practice Job j01 would hold it.
- ✅ It would show that known messages draw the expected card and an action carries the expected value.
- ❌ It would not show that a model is reliable, that it is ready for production, or that you understood it.

⚠️ A plan only: no Job, Task or Run result is claimed.

✅ **You know it when:** you can say what the practice would prove and what it would not.

## Try explaining

**Choose for two apps, and say why.**

- 📝 A fixed sign-up form.
- 🧳 A travel assistant that builds different controls for each request.
- ⚖️ For each: which claim needs a check you can run, and which needs a product decision?
