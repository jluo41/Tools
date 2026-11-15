By citation check
=================

One Discovery method card. The Discovery workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by citation check`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Verify: How is a paper's identity and citation made true?
move: Look up each paper's title, authors, year and DOI in a database and compare them with the card and its BibTeX; what cannot be matched stays marked NEEDS-VERIFICATION.
comes from: Jergas & Baethge 2015, quotation errors in medical papers; Walters & Wilder 2023, fabricated citations from a chatbot
reads: the Result card · the one-entry .bib · a database record
returns: the card's verification line, and a person's sign on each unmatched paper
test now: T3 citation true
test in use: T3 citation true


What the literature says
------------------------

rationale: Across 28 studies, about one quote in four had an error [Jergas 2015], and a chatbot invented a large share of the citations it wrote [Walters 2023]; both make a lookup of each citation necessary.
context: Quotation accuracy in medical journals, and fabricated citations from language models [Jergas 2015; Walters 2023].
steps: 1. Look the DOI up. 2. Compare title, authors and year. 3. Compare the BibTeX entry. 4. Mark it verified, or NEEDS-VERIFICATION.
strengths: A false citation is found before a report uses it (ours).
limitations: A paper with no DOI cannot be matched this way and goes to a person (ours).


Applied to AI
-------------

agent: haipipe-discovery-reviewer-agent checks the card and the .bib; the person signs what stays unmatched.
steps: 1. Read the card and the .bib. 2. Look the paper up. 3. Write the verification line. 4. Stop for the person.
returns: a verification line on each card.
verify: No card says verified without a matching database record (T3).
risk: An agent may copy the DOI from the card instead of looking it up; the check reads the database (ours).
evidence on ai: A model-written citation was often fabricated [Walters 2023].
skill: haipipe-discovery-search
