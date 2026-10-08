# Submission-readiness reference

Use this reference at the paper's final G4 pass. Treat it as a gate, not as a
generic suggestion list. The 21-point overlay below is a heuristic adaptation
of the user-provided [pre-submission checklist](http://xhslink.com/o/4GcLUMylKr1);
venue instructions, evidence contracts, and Page ownership remain authoritative.

The overlay uses the shared Writing rubric: **Mechanics, Function, Evidence,
Readability**, with `MEETS`, `NEEDS WORK`, `N/A`, or `NOT VERIFIABLE`. Record the
criterion id, target, evidence path, smallest fix, and owner. For the compact G4
summary, map `MEETS` to `✅ closed`, `NOT VERIFIABLE` to `⚠️ human review`, and
`NEEDS WORK` to `⛔ blocker` unless a permitted noncritical waiver is recorded.
`N/A` requires a contract- or venue-based reason. The overlay is not a score and
does not replace Page CHECK, the evidence lock, or human acceptance.

## 0. Twenty-one-point narrative and submission overlay

Run the section-scoped rows on the corresponding Section Pages. Run the
whole-paper rows only after assembly, using the same checked build that will be
submitted. The Methods and whole-paper retelling checks require independent human
evidence; absent that evidence they remain `NOT VERIFIABLE`.

| ID | Criterion | Rubric axes | Owner / timing |
|---|---|---|---|
| `SUB-INTRO-01` | First sentence establishes the subject and why it matters to the intended reader. | Function, Readability | Introduction Page CHECK |
| `SUB-INTRO-02` | The introduction narrows from broad context to the study question without a missing logical step. | Mechanics, Function | Introduction Page CHECK |
| `SUB-INTRO-03` | The gap states a supported unresolved question or limitation, rather than a generic novelty claim. | Function, Evidence | Introduction Page CHECK |
| `SUB-INTRO-04` | The closing states the aim, question, or contribution and hands off cleanly to the Methods. | Function, Mechanics | Introduction Page CHECK |
| `SUB-METHOD-01` | Design parameters, variables, timing, and analysis details are sufficient to reconstruct the study. | Mechanics, Evidence | Methods Page CHECK |
| `SUB-METHOD-02` | Sample size, analytic N, exclusions, and denominators are explicit and consistent. | Evidence, Mechanics | Methods Page CHECK |
| `SUB-METHOD-03` | Tests/models, estimands, uncertainty, and design alignment are stated without statistical overclaiming. | Mechanics, Evidence | Methods Page CHECK |
| `SUB-METHOD-04` | Methods order lets a reader reconstruct the experiment or analysis and matches the Results order. | Mechanics, Readability | Methods Page CHECK plus retelling evidence |
| `SUB-RESULT-01` | Each Results unit opens with the finding or answer it is reporting. | Function, Readability | Results Page CHECK |
| `SUB-RESULT-02` | Quantitative findings provide values, relevant N/denominator, and uncertainty where applicable. | Evidence, Mechanics | Results Page CHECK |
| `SUB-RESULT-03` | Results report observed findings; mechanism or interpretation is routed to Discussion unless directly tested. | Evidence, Function | Results and Discussion Page CHECKs |
| `SUB-DISC-01` | The Discussion opening answers the research question using the accepted Results. | Function, Evidence | Discussion Page CHECK |
| `SUB-DISC-02` | The finding is placed in dialogue with relevant cited prior work. | Function, Evidence | Discussion Page CHECK |
| `SUB-DISC-03` | Verbs match the design, estimand, and uncertainty; causal strength is not inflated. | Evidence, Mechanics | Discussion Page CHECK |
| `SUB-DISC-04` | Limitations, population boundaries, generalizability, and unsupported implications are explicit. | Evidence, Readability | Discussion Page CHECK |
| `SUB-COVER-01` | The cover letter uses the exact target journal name and current submission metadata. | Mechanics | Paper delivery / venue CHECK |
| `SUB-COVER-02` | The letter explains fit with the target venue's scope and audience using current instructions. | Function, Evidence | Paper delivery / venue CHECK |
| `SUB-COVER-03` | The letter meets the target venue's length and format rule; a universal one-page cap is not assumed. | Mechanics | Paper delivery / venue CHECK |
| `SUB-WHOLE-01` | The Introduction gap and first Discussion paragraph form a question-and-answer pair. | Function, Readability | Final Paper CHECK |
| `SUB-WHOLE-02` | Figure/table order, callouts, and display-register order follow the manuscript narrative. | Mechanics, Evidence | Final Paper CHECK / assembly |
| `SUB-WHOLE-03` | An independent reader can restate the question, methods, result, and meaning from the assembled paper. | Function, Readability, Evidence | Final Paper CHECK / human review |

The Results/Discussion boundary is one cross-section finding: Results quantify
what was observed, while Discussion interprets, compares, and bounds it. Fix the
owning Section or upstream evidence/claim record rather than duplicating a new
rubric for every venue. The whole-paper rows are aggregate checks and do not
become paragraph-level requirements.

## 1. Evidence lock

- [ ] State the single primary research question, estimand, outcome, exposure,
      population, and analysis window.
- [ ] State whether the result is associational or causal, and make every verb
      match that design.
- [ ] Confirm that the primary result comes from the accepted evidence package;
      do not mix old and corrected outputs, exploratory results, or results from
      a sibling paper.
- [ ] Reconcile every reported coefficient, standard error, confidence interval,
      P value, analytic N, denominator, date, and display against one source.
- [ ] Document missing-data handling, exclusions, clustering, multiplicity, and
      prespecified versus secondary, subgroup, and sensitivity analyses.
- [ ] Mark any result that requires a rerun or an unverified aggregate as
      provisional and keep it out of the abstract, title, Key Points, and
      definitive Discussion language.

## 2. Story and claim hierarchy

- [ ] Write a one-sentence reader takeaway and use it to test the title,
      Key Points, abstract, lead Results paragraph, Discussion opening, and
      Conclusion.
- [ ] Designate exactly one `[primary]` claim. Label supporting claims as
      mechanism-compatible, dose/secondary, heterogeneity, robustness, or
      exploratory.
- [ ] Keep the paper's population and disease boundary explicit. Do not import
      the theory, outcome, or framing of a related paper merely because the data
      or feature is shared.
- [ ] Treat an inherited feature or upstream model as an exposure/enabler unless
      the current paper directly tests a new methodological claim.
- [ ] Remove claims about intent, mechanism, clinical risk, policy impact, or
      generalizability that the design and evidence do not establish.

## 3. Manuscript and reporting consistency

- [ ] Use one design label, one cohort definition, one analysis date, and one
      naming convention for the exposure and outcomes throughout.
- [ ] Methods identify setting, dates, data sources, eligibility, linkage,
      variables, model specification, uncertainty, clustering, missingness,
      ethics/IRB, and consent or waiver as applicable.
- [ ] Results begin with cohort flow and descriptive characteristics, then lead
      with the primary claim before secondary analyses.
- [ ] Report uncertainty for the main estimates and avoid treating a
      nonsignificant result as proof of equality or absence.
- [ ] Discussion separates finding, interpretation, implication, limitation,
      and speculation. It does not introduce a new result.
- [ ] Every consequential sentence has a citation, value/display binding, or an
      explicit open-evidence marker.

## 4. Displays and supplement

- [ ] Table 1, cohort flow, and the primary-association display are present when
      required by the venue or design.
- [ ] Every display has a final file, title, legend/notes, units, denominator,
      uncertainty convention, and in-text citation.
- [ ] Supplement contains its actual eMethods/eTables/eFigures, follows the
      venue's single-file and pagination rules, and is cited in sequence.
- [ ] No TODO, placeholder, draft watermark, stale N, stale year, or unbound
      display remains in the submission files.

## 5. Submission package and transparency

- [ ] Apply the target venue's current author instructions immediately before
      export; record the date and URL checked.
- [ ] Complete title page, word count, author names/degrees/affiliations,
      corresponding-author contact, cover letter, and related-manuscript
      disclosures.
- [ ] Complete funding, conflicts of interest, author contributions, data
      sharing, code/materials sharing, ethics/IRB, consent, and registration
      statements as applicable.
- [ ] Disclose generative AI or automated tools used in manuscript preparation
      according to the venue's current policy; authors remain responsible for
      all content and citations.
- [ ] Attach the required reporting checklist (for example, STROBE for an
      observational study) and confirm that the uploaded file types match the
      venue's rules.

## 6. Human reading pass

- [ ] Read the assembled manuscript in order, not only section by section.
- [ ] Replace promotional, vague, inflated, or AI-like language with precise
      patient/outcome-centered wording.
- [ ] Split clause-stacked sentences, remove repeated scaffolds, define
      abbreviations once, and check that each paragraph has one job.
- [ ] Confirm that the title and abstract do not promise more than the Results.
- [ ] Have a person approve the final evidence scope, unresolved waivers, and
      submission build.

## JAMA Internal Medicine delta (verify live before each submission)

For an Original Investigation or observational report, consult the official
[JAMA Internal Medicine Instructions for Authors](https://jamanetwork.com/journals/jamainternalmedicine/pages/instructions-for-authors)
and record the checked date. The current checklist should at least test the
following venue-specific items:

- [ ] title length, article word limit, reference range, and table/figure limit;
- [ ] Key Points with Question, Findings, and Meaning;
- [ ] structured abstract headings and word limit;
- [ ] Study Type, Data Sharing Statement, and STROBE/EQUATOR reporting;
- [ ] title page and manuscript Word-file formatting;
- [ ] main-text tables/legends, separately uploaded figures, and the required
      online-only supplement format;
- [ ] ethics/IRB placement in Methods and the journal's AI-use disclosure;
- [ ] cover letter disclosures for related manuscripts, prior reports, or
      overlapping data/features.

Do not hard-code a venue threshold from this reference without rechecking the
live instructions; venue rules can change.
