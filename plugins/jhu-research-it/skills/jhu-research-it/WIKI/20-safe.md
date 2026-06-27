# 🔒 SAFE — Secure Analytic Framework Environment (SAFE Desktop)

## What it is
SAFE Desktop is a secure virtual machine (a cloud-based virtual desktop) for accessing datasets and analytical tools inside PMAP. It emulates a normal desktop and is fully HIPAA compliant. (Source: https://researchit.jhu.edu/safer/ , https://www.hopkinsmedicine.org/news/articles/2019/05/precision-medicine-in-three-steps-step-2)

## Tools available on it
SAS, Stata, RStudio, Anaconda (Python), PowerBI, and NVivo. (Source: search of researchit.jhu.edu, 2026-06-25)

## Who can use it and cost
- SAFE is free up to 100 GB for all JHU faculty and staff with a JHED ID.
- At present only JH staff can submit the SAFE Desktop request form. (Source: researchit.jhu.edu)
- Access works from any device over a secure connection using your JHED ID.

## How to request
- SAFER and SAFE Desktop overview: https://researchit.jhu.edu/safer/
- SAFE Desktop request form: [TODO: JL paste the exact form URL]
- Storage / access overview: https://researchit.jhu.edu/storage-access/

## Related
- Larger storage: SAFESTOR appears as the `R:` drive on SAFE/SAFER (up to 100 TB, first 10 TB free for 3 years). (Source: researchit.jhu.edu)  Request: [TODO: JL]
- Crunchr (Jupyter/RStudio) is reachable only from inside SAFE. See `50-crunchr.md`.
- SAFE vs SAFER: use SAFE for relatively small, uncomplicated projects; SAFER is the research virtual desktop tier. See `21-safer.md`.

## Notes / constraints
- SAFE is a locked-down environment. Outbound internet, file transfer in/out, and installing new software are restricted. [TODO: JL confirm the egress and software-install policy] This matters for things like installing CLI tools. See `90-howtos/install-codex-in-safe.md`.

📄 Public facts verified 2026-06-25. Request-form URL and egress policy are TODO.
