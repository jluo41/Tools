# 🏛️ PMAP — Precision Medicine Analytics Platform

## What it is
PMAP is the Johns Hopkins secure, HIPAA-compliant platform for integrating, storing, and analyzing clinical and research data. It is built on the Microsoft Azure cloud and has two parts: a large-scale data repository and a cloud-based analytics and knowledge-delivery layer. (Source: https://pm.jh.edu/platform-pmap/)

## What data it holds
Clinical EMR data, open clinical notes, imaging (radiology, pathology), genomic and molecular data, wearable data, and operational/financial data. (Source: https://pm.jh.edu/platform-pmap/)

## How the pieces fit
- **PMAP** is the umbrella platform. The secure desktops, storage, and compute below all sit under it.
- **SAFE / SAFER** (`20-safe.md`, `21-safer.md`): secure virtual desktops where you actually work with the data.
- **Crunchr** (`50-crunchr.md`): Jupyter/RStudio data-science environment, reachable only from SAFE.
- **Databricks** (`40-databricks.md`): Spark + notebooks for larger analytics and model training, including the REACH enclave.
- **Discovery** (`30-discovery.md`): high-performance computing.
- Data can be modeled in **OMOP** common data model on PMAP. (Source: https://pm.jh.edu/how-it-works/omop/)

## Access
- Start at the PMAP portal: https://pm.jh.edu/  and researcher resources: https://pm.jh.edu/researchers/
- Research using PMAP requires IRB review. See the IRB guidance: https://www.hopkinsmedicine.org/institutional-review-board/guidelines-policies/guidelines/research-using-pmap
- PMAP consultation / onboarding request: [TODO: JL paste the internal request link]
- PMAP Cookbook (step-by-step internal docs): [TODO: JL paste link]

## Support
- ICTR PMAP service page: https://ictr.johnshopkins.edu/service/informatics/pmap/
- Help desk / contact: [TODO: JL]

📄 Public facts verified 2026-06-25 from pm.jh.edu and hopkinsmedicine.org. Internal links are TODO.
