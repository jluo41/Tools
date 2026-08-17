# Start: Reshape HAIPipe Application

Use this file to start a fresh Codex session for reorganizing the HAIPipe Application skill family.

The new session should treat HAIPipe Paper as a structural reference, not as a template to copy blindly.

```text
Please help me reorganize and simplify the HAIPipe Application skill family.

Start by reading these files and folders:

1. Tools/plugins/haipipe-toolkit/skills/application/start.md
2. Tools/plugins/haipipe-toolkit/skills/application/
3. Tools/plugins/haipipe-toolkit/skills/application/haipipe-application/SKILL.md
4. Tools/plugins/haipipe-toolkit/skills/application/README.md
5. Tools/plugins/haipipe-toolkit/skills/paper/
6. Tools/plugins/haipipe-toolkit/skills/paper/diagram/01-haipipe-paper-260725/board.md

Use the HAIPipe Paper redesign discussion as the main comparison point. Determine which structural ideas should also apply to Application and which differences must remain intentional.

Important Application-specific behavior to preserve:

- Application delivers an intervention, not a manuscript.
- Its venue is an output modality such as SMS, email, dashboard, UI card, or report.
- Its evidence ladder is descriptions -> themes -> claims -> advice.
- Venue selection can skip stages and change the required settlement depth.
- Evidence must enter through the EVIDENCE phase rather than being produced inside Application.
- Application continues through artifact, review, deploy, and iterate.

The desired working model is:

Application Board -> choose a question or queue item -> open the owning page -> run the appropriate skill or worker -> write the result and handoff back onto that same item.

Do not create separate request or handoff sidecar files when the owning stage or queue page already exists.

For the first turn:

1. Inspect the current Application structure and compare it with Paper.
2. Identify duplicated, misplaced, oversized, contradictory, or historical material.
3. Propose a compact target folder and skill architecture.
4. Propose the Question Groups and Questions for an Application redesign Board.
5. Give me a phased plan.
6. Do not make complex runtime skill changes yet.

Stop after presenting the plan and proposed Board design so I can review them.

After I approve the plan, create the Application Board and work through it question by question. When actual skills are later revised, validate them through a fresh-context agent as required by AGENTS.md.
```

The intended sequence is:

```text
read current Application
        ↓
compare with Paper design
        ↓
design Application Board questions
        ↓
JL reviews the plan
        ↓
revise Application incrementally
        ↓
fresh-context validation
```
