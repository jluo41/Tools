CoWork Workbench Table
======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. One CoWork Block is one
workbench (`/w/<block>`). Rows run input → process → output: Scope states the Block,
who to ask, its links and its drawings; Work moves the Jobs (one line of work each),
the Questions, the emails and the meetings; Check finds who we wait on, the drafts not
sent and the reports to judge; Delivery holds the answered reports and the done Jobs. Folder is
where the run writes: `Block ›` is the Block folder (`cowork/bNN_<topic>/`), `Tools ›`
the workbench's server folder (`servers/workbench-cowork/`); `none` writes no file, only a verdict.

Agents: the Block-level writes (a job page, the Questions register, an email draft, meeting
notes, a drawing) need an agent of their own, planned as `haipipe-cowork-agent (new)`;
a draft or a register change is judged by `haipipe-cowork-reviewer-agent (new)`, never
by the agent that wrote it. Reports are Pages: `haipipe-page-writing-agent` writes,
`haipipe-page-check-agent` checks. No agent sends a message: the person signs the send.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | none | none | none | none | none |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check | Tools › related/papers.md |
| board | Scope | Block | Update the Block status | haipipe-cowork-agent (new) | haipipe-cowork | none | Block › board.md (header) |
| board | Scope | People | Add a person | haipipe-cowork-agent (new) | haipipe-cowork | none | Block › j00_people/j00_people.md |
| board | Scope | Resources | Add a resource | haipipe-cowork-agent (new) | haipipe-question | none | Block › board.md (Related resources) |
| board | Scope | RoadMap Draw | Draw | haipipe-cowork-agent (new) | workbench-studio | none | Block › studio/<name>.excalidraw |
| board | Work | Jobs | Open a job | haipipe-cowork-agent (new) | haipipe-cowork | the request | Block › jNN_<job>/jNN_<job>.md |
| board | Work | Jobs | Update a job | haipipe-cowork-agent (new) | haipipe-cowork | none | Block › jNN_<job>/jNN_<job>.md (header) · Timeline.md · CHECKLIST.md |
| board | Work | Questions | Ask a Question | haipipe-cowork-agent (new) | haipipe-question-asking | the question | Block › board.md (Questions) · reports/qNN_<topic>/ |
| board | Work | Questions | Review the questions | haipipe-cowork-reviewer-agent (new) | haipipe-question-review | a change | none |
| board | Work | Questions | Write the report | haipipe-page-writing-agent | haipipe-page-writing | none | Block › reports/qNN_<topic>/ |
| board | Work | Emails | Draft an email | haipipe-cowork-agent (new) | haipipe-writing | the send | Block › jNN_<job>/emails/<thread>.md · CHECKLIST.md |
| board | Work | Meetings | Write meeting notes | haipipe-cowork-agent (new) | haipipe-cowork | none | Block › jNN_<job>/meetings/YYYY-MM-DD-<topic>.md |
| board | Check | Waiting on | Draft a follow-up | haipipe-cowork-agent (new) | haipipe-writing | the send | Block › jNN_<job>/emails/<thread>.md |
| board | Check | Drafts | Review a draft | haipipe-cowork-reviewer-agent (new) | haipipe-writing | the send | none |
| board | Check | Reports | Check a report | haipipe-page-check-agent | haipipe-page-check | release or hold | none |
| board | Delivery | Reports | none | none | none | none | none |
| board | Delivery | Done jobs | none | none | none | none | none |
