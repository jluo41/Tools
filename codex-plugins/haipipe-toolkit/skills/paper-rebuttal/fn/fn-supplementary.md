fn-supplementary: Create Anonymous Supplementary
==================================================

Set up an anonymous GitHub repo with a README containing full experiment
tables, and wrap it with anonymous.4open.science for double-blind venues.

---

Input
======

  User provides: experiment results (tables, metrics, analyses)
  User provides: GitHub credentials (gh CLI authenticated)

---

Steps
======

Step 1: Organize results by rebuttal point
--------------------------------------------

  Create a single README.md organized by point (P1, P2, ...):

  For each point:
    1. "Why we investigated this" — 2-3 sentences
    2. Tables with full results (no truncation — this is the detail page)
    3. "What this means" — 2-3 sentences

  Include navigation links at the top (anchor links to each section).

  Template:
    ## P1: [Title]
    ### Why we investigated this
    [context]
    ### Results
    [full tables]
    ### What this means
    [conclusion]

Step 2: Create GitHub repo
----------------------------

  Create a new PRIVATE repo with a generic name:
    gh repo create {generic-name} --private

  Generic name examples:
    - icml-2026-rebuttal
    - paper-rebuttal-supplementary
    - rebuttal-results

  Do NOT use:
    - Paper title or acronym (reveals identity)
    - Author names or institution
    - Internal project names

Step 3: Push README
---------------------

  Push the README.md to the repo:
    - Create temp directory
    - git init, add, commit, push
    - Verify repo renders correctly: gh api repos/{owner}/{repo}/readme

Step 4: Create anonymous wrapper
-----------------------------------

  anonymous.4open.science requires browser login. Instruct user:

    1. Go to https://anonymous.4open.science
    2. Login with GitHub
    3. Click "Anonymize"
    4. Paste repo URL: https://github.com/{owner}/{repo}
    5. Add terms to anonymize: username, real name, institution,
       company, project names
    6. Copy the anonymous URL

  The anonymous URL format:
    https://anonymous.4open.science/r/{repo-name}-{id}/

Step 5: Verify
----------------

  Check the anonymous URL works:
    curl -s -o /dev/null -w "%{http_code}" {anonymous-url}/README.md

  Verify content renders:
    - All sections present
    - Tables formatted correctly
    - No identifying information visible

Step 6: Update rebuttal drafts
--------------------------------

  Replace URL placeholders in all rebuttal files:
    sed -i 's|REPLACE_WITH_ANONYMOUS_URL|{anonymous-url}|g' C-rebuttal-writing/rebuttal-*.md

  Verify all files updated:
    grep -l "anonymous.4open.science" C-rebuttal-writing/rebuttal-*.md

---

Updating the Supplementary
============================

If results change after initial setup:
  1. Update README.md locally
  2. Push to the GitHub repo (private)
  3. anonymous.4open.science mirrors automatically
     (may take a few minutes to refresh)
  4. Verify the anonymous URL shows updated content

---

Output
=======

  - GitHub repo (private) with README.md
  - Anonymous URL for double-blind reference
  - All rebuttal drafts updated with the URL
