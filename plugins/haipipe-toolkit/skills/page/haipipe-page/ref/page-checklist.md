# Page configuration and completion checklist

Use this checklist when creating a Page, auditing its configuration, or claiming
whole-Page completion. It applies to standalone and Board-mounted Pages: Board
membership does not change what the Page owns. For a narrow edit, assess the
affected checks without expanding the request into a full audit.

This is an operational checklist over `../SKILL.md`, `page-template.md` and
`standalone.md`, not another Page schema or a new Run. Resolve any
declared Page owner before applying its additional requirements.

## 1. Declare what is being checked

- [ ] Identify the existing Page Face/Folder, or the input and new destination.
      Do not wrap an existing Page in another Page Folder.
- [ ] State the operation: technical file intake, authored Page creation,
      content completion, source editing, static export, live hosting, or Board
      registration. Several may apply; their outcomes remain separate.
- [ ] Identify the Page's purpose and semantic owner, if declared. Do not invent
      a Page Type, a research workflow, or Board membership for an ordinary file.

## 2. Configuration: can this Page be used independently?

- [ ] One authoritative Page Face is identifiable. Its title, owner and current
      state are explicit. An `unassigned` owner is an unresolved assignment,
      not evidence of human ownership or acceptance.
- [ ] The Folder uses its same-stem Face, or an explicit registration identifies
      the Face. For standalone registration, `page.toml` resolves valid local
      paths; its optional `content` agrees with the Face's `source-content:`.
- [ ] Imported content has one editable copy inside the Folder. On intake,
      compare its bytes with the input and confirm the original was not changed.
      Subsequent intentional edits need not match the original intake hash.
- [ ] Required local assets resolve inside the package. Name network resources
      and unbundled dynamic/backend dependencies: a standalone Page runtime does
      not imply the imported content is offline-capable or a packaged web app.
- [ ] The Page can be inspected and rendered through the Page entry point without
      a Board registry. Check the actual render for the requested creation/build,
      not just command exit status; inspect imported HTML and its asset requests.
- [ ] Generated `delivery/` files are outputs, never a second editing authority.
      Create only the process/workbench lanes actually used by this Page.

Configuration can pass while content remains a draft. Default Opening and
backstage-target scaffolding provides structure, not substantive completion.
Missing evidence of a check means **untested**, not pass.

## 3. Two Page areas: what must the reader find?

The reader-facing Page has only two areas:
**Opening → Content**. Outline, Aims, Stage Contract, Files, Discussion, Log,
and similar records are backstage Folder/Run records. They remain auditable
and available through their owning Spaces, but they are not additional Page
sections and should not interrupt the reading flow.

| Area | What it must contain | Completion test |
|---|---|---|
| Opening | A Page-specific explanation of the subject, why it matters, and what this Page covers. | A new reader can identify the purpose and boundary without guessing from the title. Generic intake text, placeholders and internal addresses alone do not pass. Opening is never omitted. |
| Content | The actual work promised by Opening and applicable backstage requirements: authored material or the bound imported file. | The material is readable, its relevant assets/links work, and it fulfills the declared scope. A filename, blank heading, stock sample or successful build alone does not pass. Technical imports do not require scholarly rewriting. |

The following backstage records are checked separately when the Page uses
them; they do not expand the Page Face:

| Backstage record | Owner | Completion test |
|---|---|---|
| Outline / Draft | Draft Space and `outline/` | The current plan, Bullets, Drafts, and the Structure list remain addressable and internally consistent. |
| Aims / requirements | Run Space, CHECK, and `outline/` records | Targets and completion tests are available to the workflow even when no `## Aims` is rendered on the Page. |
| Stage Contract | Page configuration and upstream records | Required inputs, venue, and handoff are resolvable without appearing in the reading surface. |

The Outline check also requires one uninterrupted Page-global paragraph
sequence: `P1, P2, …, PN`. `P` does not reset when `C` changes, so after
`C1.P3` the next paragraph is `C2.P4`; `B` restarts within each paragraph.

### Missing areas and legitimate exceptions

- **Outline not initialized:** the base contract permits no visible Outline on
  the Page when no plan exists. A technical import may therefore be configured
  successfully while the Draft Space is **deferred: no plan yet**. It is not an
  Outline pass and must not be presented as a complete planning workflow. Do not
  fabricate a plan, evidence or Shape approval merely to make intake pass.
- **Content omission:** a Q decision Page may omit Content where its resolved
  contract permits this; report **N/A** with that reason. S Pages may not omit
  Content. An ordinary file import has actual bound Content, not this exception.
- **Open targets:** backstage target records may still be unmet. Distinguish
  “targets correctly recorded” from “targets achieved.” If a target remains in
  the requested completion scope, do not claim that scope complete. A held or
  waiting tick does not waive a required target.
- **Evidence and review:** apply the owning evidence/writing/Run requirements
  when the Page makes substantive claims or a research delivery is requested.
  Mark unsupported claims and pending human gates explicitly. A technical
  import does not trigger a new evidence Run, PDF or scholarly acceptance gate.
  Packaging an imported claim does not verify its truth.

## 4. Delivery: check only the surfaces requested

| Requested capability | Acceptance check | What it does not prove |
|---|---|---|
| Open/edit source | Identify the actual editable Face/content. If a save was requested, verify the scoped saved source and its rendered result; preserve unrelated edits and the original input. | Showing the Source tab alone does not prove save-back works. Do not make an unsolicited content edit just to test saving. |
| Static website | Build the current `delivery/web/` and inspect the reading output and required assets. | A static export neither runs a server nor supports source save-back. |
| Hosted reading/working Page | Start or reuse an authorized listener/deployment; verify the exact configured reader-facing URL. State read-only versus writable; apply the standalone token and privacy rules. | A successful build or a loopback-only check does not prove reader reachability. Do not publish private inputs without authority. |
| Board integration | Register the same Face under the requested Board group, build and verify the mounted Page/navigation. Respect the current beneath-Board-root discovery limit. | Do not copy the Page, silently relocate it, or claim support for arbitrary external folders. |
| Formal content/research delivery | Follow the resolved owner and `user-check-packet.md`; report the current version, required checks and actual human acceptance separately. | This checklist cannot substitute for human approval or mark a draft accepted. |

Board owns group order, navigation and group descriptions. Page owns its own
Opening, Content, and planning sources. Removing membership must not remove
the Page's content. Board integration is **N/A: standalone requested** when no
Board was requested; it is not a prerequisite for Page completion.

## 5. Return the result without creating another authority

Use **pass**, **missing**, **deferred**, **untested**, or **N/A (reason)** for
each applicable check. Attach an inspected source, rendered observation, test
result or actual decision as evidence. A heading's presence is not evidence
that its content is complete. Do not collapse all checks into one green tick.

For a whole-Page audit, use this compact report shape:

| Check | Status | Evidence or next action |
|---|---|---|
| Source/configuration | … | … |
| Opening | … | … |
| Outline | … | … |
| Content | … | … |
| Aims: structure / targets | … / … | … |
| Requested delivery surfaces | … | Name each requested surface separately. |
| Review / human acceptance, if applicable | … | … |

End with separate conclusions for **configuration**, **content completion**,
**review/acceptance**, and **hosting**. A configuration-only request can be
complete with content still draft and hosting not requested; say exactly that.
Required missing, deferred or untested checks prevent completion of their
respective scope. N/A needs a contract- or request-based reason, not convenience.

Keep this reusable checklist here. Do not automatically create a Page-local
`CHECKLIST.md`, a fifth Page section, another status ledger, or new manifest
fields. Report findings in the response; use existing Aims, plan or Run
records only when updating that Page is authorized. Audits alone are read-only.
The Markdown `setup` command writes a deterministic mechanical audit to its
Result as `checks.json` and repeats it in `report.md`. Mechanical failures block
the command. Its `bullet_head_readability` gate rejects clipped or dangling
heads, planner imperatives, and setup heads outside a provisional 4–24 word
range. Setup preserves a complete source clause instead of cutting at a word
limit; the structure Run performs the semantic rewrite into its stricter
4–11-word house style. Argument coherence still requires the Bullet-only reading
test and remains explicitly untested;
Aim achievement and human acceptance are also untested or deferred.
This document remains the authority for the distinction between those gates.
