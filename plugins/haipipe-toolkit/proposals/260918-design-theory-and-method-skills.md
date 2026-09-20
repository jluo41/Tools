# Proposal: design theories, designer approaches, and method skills

Date: 2026-09-18

Status: discussion draft, not an approved skill contract. No new skills are
registered by this document. No Run schema, source evidence, live workflow,
plugin UI, or skill version is changed.

## 1. Recommendation

Build reusable design-method skills, then compose them into optional designer
profiles. Do not implement personas as personality adjectives or as claims of
expertise. A profile must change what the designer does: the questions asked,
information consulted, alternatives created, and checks performed.

Keep these concepts separate:

| Concept | Meaning here | Example |
|---|---|---|
| Theory | An account of designing or design reasoning | C–K theory |
| Method skill | A bounded, repeatable capability | Explore concepts and identify knowledge gaps |
| Designer profile | A task-specific combination of methods and evidence-access timing | Independent Explorer |
| Operation | What is being done to an artifact | Compose or revise |
| Workflow | Ownership, sequencing, permissions, and completion | Existing Commission / Generate / Verify |
| Space | Reader-facing plugin presentation | Design Space or Insight Space |

The mappings below are our proposed operationalization, not an established
taxonomy of designer personalities. These sources do not validate LLM personas
or demonstrate that one prompting profile produces better designs.

## 2. Theoretical foundations

### C–K theory: concepts and knowledge develop together

Hatchuel and Weil model designing through interaction between concepts and
knowledge, including the production of new concepts and new knowledge. A
concept can remain unresolved relative to available knowledge; it need not
already be an established conclusion. The research group's explanation also
describes concepts triggering the search for additional knowledge.
[Hatchuel and Weil, 2009](https://link.springer.com/article/10.1007/s00163-008-0043-4);
[C–K research-group overview](https://www.ck-theory.org/c-k-theory/?lang=en).

Proposed application: concepts are not merely outputs of the Insight Board.
A concept can generate a precise question back to that board. Keep an idea's
promise distinct from evidence for its effectiveness. The theory's C/K spaces
are conceptual constructs, not instructions to add plugin tabs. C–K's K is
also not identical to the Knowledge rung of our DIKW workflow.

### Abduction and framing: reconsider the problem, not only the answer

Dorst's account connects design reasoning to framing and frame creation.
Dorst and Cross's study of nine experienced industrial designers examines
how problem formulations and solution ideas develop together. This is a
bounded study, not a universal ranking of designer types.
[Dorst, 2011, institutional abstract](https://opus.lib.uts.edu.au/handle/10453/18751);
[Dorst and Cross, 2001, paper](https://sites.cc.gatech.edu/classes/AY2018/cs8803cc_spring/research_papers/Dorst_Cross2001.pdf).

Proposed application: compare alternative interpretations of an ask and the
concept each would suggest. A proposed mechanism is a hypothesis, not a causal
finding. Reframing may reveal a better brief; it does not authorize silently
changing the user's audience, outcome, or scope.

### Function–Behaviour–Structure: make the translation explicit

Gero and Kannengiesser's situated FBS framework separates function, behaviour,
and structure, including expected behaviour and behaviour derived from a
structure. It accounts for reformulation as the design context develops.
[Gero and Kannengiesser, 2004](https://www.sciencedirect.com/science/article/pii/S0142694X03000735);
[author-hosted paper](https://www.johngero.com/publications/2004/04GeroKannengDesignStud.pdf).

Proposed application: connect purpose, expected response, and concrete design
features. For communication design, the proposed relationship between wording
and a human response remains an assumption unless independently supported.
An FBS diagram or a model-generated explanation cannot establish that response.

### Reflective practice: learn through making

Schön's reflection-in-action account examines professional knowing and
improvisation in practice rather than reducing competent work to applying
pre-existing formulas.
[Schön, The Reflective Practitioner, publisher description](https://www.hachettebookgroup.com/titles/donald-a-schon/the-reflective-practitioner/9780465068784/).

Proposed application: make a small prototype, inspect what it reveals, and
revise. Preserve the prototype, observable finding, and resulting change—not
a private thinking transcript. Rendering and agent inspection establish only
what was actually inspected, not user understanding or real-world effectiveness.

### Critical design: expose assumptions and values

Dunne and Raby describe critical design as using speculative proposals to
question assumptions about products and everyday life. They explicitly call
it a position rather than a method; its purpose includes exposing assumptions
and prompting debate.
[Dunne and Raby, Critical Design FAQ](https://dunneandraby.co.uk/content/bydandr/13/0).

Proposed application: construct a bounded alternative that makes an assumption
or value trade-off visible. Our challenge skill would be a local method inspired
by this position, not an exact implementation of it. A thought-provoking
prototype is not automatically suitable for operational delivery, nor is
opposition itself evidence that the original design is wrong.

### Double Diamond: distinguish understanding from solution development

The Design Council's process framework distinguishes Discover, Define,
Develop, and Deliver, and notes that learning can send a project back to earlier
work. It is a practical framework, not a theory of personality.
[Design Council, Double Diamond](https://www.designcouncil.org.uk/resources/the-double-diamond/).

Proposed application: inquiry is a legitimate design activity before or during
concept development. Do not translate the four labels into mandatory new Runs,
approval gates, or plugin Spaces. The framework's delivery/testing activities
do not expand our Design plugin's authorization to send messages or run studies.

### Design fixation: a reason to test information timing

Jansson and Smith report experiments demonstrating design fixation: adherence
to existing ideas that restricts conceptual output.
[Jansson and Smith, 1991](https://doi.org/10.1016/0142-694X%2891%2990003-F).

Proposed application: evaluate a delayed-exposure exploration profile. This
finding does not establish that withholding insights improves LLM design or
that evidence should generally be ignored. Mandatory factual and safety
constraints stay visible. Delay previous solutions, not essential constraints.

## 3. Proposed method skills

All names in this section are proposals, not installed slash commands.
Source-informed implications here are our design choices, not author-prescribed
agent procedures.

| Proposed skill | Use when | Distinct work | Inspectable output | Boundary |
|---|---|---|---|---|
| `haipipe-design-inquire` | A consequential premise or user need is unclear | Find what existing authorized insights answer; seek contradictions; identify the smallest important missing question | Decision-specific evidence assessment and prioritized questions | No fabricated findings, board settlement, signatures, or unrequested data collection |
| `haipipe-design-translate` | A relevant finding can guide concrete design choices | Map the finding to purpose, expected behaviour, design features, and checks | Candidate plus finding-to-choice mapping and assumptions | Do not transfer a measured effect to altered wording, audiences, or channels without support |
| `haipipe-design-reframe` | The brief presupposes one diagnosis or solution | Compare alternative problem frames and what each would imply | Alternative frames, concept sketches, distinguishing questions, and a scope recommendation | A changed goal is a proposal until authorized |
| `haipipe-design-explore` | The task needs genuinely different possibilities | Expand concept branches; use evidence, analogy, or delayed exposure as selected | Distinct concepts, origins, unknowns, and evidence-reconciliation notes | Novelty is not effectiveness; no invented supporting rationale |
| `haipipe-design-challenge` | A dominant assumption deserves scrutiny | Construct a coherent alternative or counterexample and identify what it reveals | Challenge concept, named assumption, trade-offs, and a discriminating observation | Do not deny sound evidence for dramatic contrast; label speculative outputs |
| `haipipe-design-prototype` | An idea is too abstract to inspect or compare | Build the smallest authorized representation, inspect, and revise | Prototype, observations, changes, and remaining uncertainty | No implied user testing, deployment, or downstream experimentation |

These capabilities are composable. They are not six mandatory sequential
stages and not six competing copies of the whole Design workflow.

### Relationship to the previously proposed personas

- Investigator: primarily `inquire`; sometimes `reframe`.
- Translator: primarily `translate`; sometimes `prototype`.
- Mechanism Builder: `reframe` + `translate`, with an explicitly hypothetical mechanism.
- Challenger: primarily `challenge`; sometimes `reframe` or `prototype`.
- Independent Explorer: `explore` with delayed exposure to previous solutions,
  followed by evidence reconciliation.

One person or agent may switch approaches within a task. Not every request
needs multiple agents. Profile names are useful shorthand, not new authority.

## 4. How insights enter a design

Record two independent choices:

1. **Method:** how the designer approaches this task.
2. **Evidence schedule:** when it sees relevant insights and prior solutions.

Possible schedules are upfront, on-demand, and after an initial concept.
Delayed exposure requires a fresh context that has not already seen the
withheld material; an instruction to forget it does not establish blindness.

For each material design decision, record only what is useful to review:

- The choice made and its purpose.
- Exact source finding and version, when one is used.
- Relationship: support, constraint, inspiration, disagreement, or context.
- Applicability and the inference connecting the source to the choice.
- What remains unknown, and what observation could change the choice.

Not every feature needs a citation. Craft, taste, and imaginative choices may
be identified as such. A signed input establishes its recorded authorization,
not the correctness of every interpretation or its applicability everywhere.

Assess insight sufficiency relative to a decision. Useful outcomes include
supported application, bounded exploration, a narrower design, a named missing
fact, and non-use because the finding is irrelevant. Do not collapse these
into a general insight quality score or reward citation volume.

Use this loop when warranted:

```text
design question → relevant insights → candidate concept → new uncertainty
                         ↑                                     │
                         └──── question to Insight owner ──────┘
```

The designer can draft the question. Searching additional material, starting
computation, modifying an InsightBoard, or recruiting participants remains
subject to the owning workflow and the user's authorization. A generation
worker may not silently replace its frozen inputs.

## 5. Skill boundary and integration proposal

Keep `haipipe-design` as the public coordinator and Folder/Item owner;
`haipipe-design-workflow` owns Runs and transitions; `haipipe-design-unit`
continues to enforce bounded production/review and the paired Result contract.
Method skills contribute behavior, not a second lifecycle or evidence authority.

Inquiry and reframing can happen before Commission. Inside an allocated Run,
use only its permitted sources, goal, output scope, and resource budget. A
new premise or materially changed goal returns to the caller. Prototyping and
method changes do not mint a Run merely because a method was invoked.

Do not add six plugin tabs, six persona-specific Item schemas, or a second
verification system. Keep Goal, Design, Insight, Run, and Delivery Spaces;
keep the user's no-Adopt decision. An approach label and a concise decision
record can be displayed inside the existing Item, if later implemented.

For each eventual `SKILL.md`, document:

- The trigger and situations in which another method fits better.
- Required inputs and authorized scope.
- Distinctive procedure, with freedom proportional to the creative task.
- Evidence-access schedule and missing-input behavior.
- Concrete deliverables and method-specific quality checks.
- Failure modes and handoffs to existing owners.

Keep theory and substantial examples in referenced material; do not copy the
entire theory survey into each skill. Separate method from operations such as
compose/revise and from review independence. New fields or names shown here
are conceptual only; the present parser does not implement them.

The intended destination, if approved, is the user's requested
`Tools/plugins/haipipe-toolkit/skills/design/` family. Today the existing
canonical skills still live under `skills/application/`; moving them needs a
separate dependency-aware change. This proposal does not perform that move.

## 6. Evaluation before adopting a skill family

Start with small comparisons of Translator, Challenger, and Independent
Explorer against the current worker. Add other methods when the brief needs
them. Compare more than one brief: strong relevant evidence, inconclusive or
conflicting evidence, no relevant evidence, and a concept with a false premise.

Keep model, budget, brief, essential constraints, and presentation format
comparable. Record the information exposure schedule. Save an Explorer's
pre-exposure artifact before revealing the insights; then preserve its revised
artifact and observable differences. Record sources actually consulted rather
than accepting a claimed reading history.

Review outputs without persona labels and randomize their order. Assess
usefulness, constraint compliance, meaningful diversity, accuracy of source
use, assumptions, and quality of the questions raised. Do not reward novelty
alone, number of citations, confidence, or explanation length. Where possible,
include qualified human review; multiple contexts of one model are not
independent human expertise.

Use method-specific tests as well: the Investigator should find an important
gap; the Challenger should expose a substantive assumption; the Translator
should preserve a source's limits. A persuasive rationale without a useful
artifact or decision is not enough. Reviewer preference and prototype
inspection do not establish downstream effectiveness.

Possible result: merge profiles that do not produce materially different
behavior, or retain methods as reference modes instead of separate skills.
These are hypotheses to test, not six abstractions that must be retained.

## 7. Proposed first implementation boundary

After agreement on this proposal:

1. Implement a small set of method instructions with one shared decision-record
   contract; pilot Translate, Explore, and Challenge first.
2. Run bounded behavioral tests without changing real evidence or deliveries.
3. Only then integrate method selection and the concise record into Design
   Items and the existing plugin.

Do not simultaneously redesign Run identities, migrate historical boards,
change evidence authority, or add adoption gates. Family version remains
`0.4.0` unless the user explicitly authorizes a version change.

## 8. Source coverage and limits

This is a focused theory-to-skill proposal, not a systematic literature review.
Primary papers, author material, institutional records, and publisher pages
were used. C–K and Dorst 2011 were checked through available abstracts and
research-group/institutional descriptions; Schön through publisher descriptions;
FBS through its publisher abstract and indexed author-paper passages. Full
text was available for Dorst and Cross 2001 and Dunne and Raby's FAQ.
Jansson and Smith's fixation claim is based on the published abstract, not a
new assessment of the full experiments. No paywalled full-text review or
empirical validation of the proposed LLM skills is claimed.

The foundational works explain or investigate designing; none directly tests
this Haipipe implementation. All skill names, profile mappings, artifact
contracts, and evaluation plans above are proposals made here.
