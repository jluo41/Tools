# ⚡ Databricks on PMAP / REACH

## What it is here
Databricks is the Spark + notebook environment used for larger analytics and model work on PMAP data, including the REACH enclave. We used it in the REACH project to train models and build endpoints for deployment.

## REACH enclave
REACH (inHealth Research Enclave for Analyzing Clinical Health data) is a secure, HIPAA-compliant environment with de-identified structured EMR data and clinical notes for research. (Source: https://www.hopkinsmedicine.org/inhealth/research)
- REACH Databricks workspace URL: [TODO: JL paste your workspace URL]
- How to get a REACH / Databricks account: [TODO: JL]

## Train a model + build an endpoint (existing skills in this repo)
We already have skills for the Databricks model-train and deploy flow. Use them instead of re-explaining the steps:

| Step | Skill | Use for |
|---|---|---|
| Init a SuperLearner project | `/sl-init` | scaffold a training project |
| Iterate / fit | `/sl-iterate` | run + improve training |
| Scale up | `/sl-scale` | larger runs |
| Validate | `/sl-validate` | check the trained model |
| Status | `/sl-status` | where the run stands |
| Develop endpoint on Databricks | `haipipe-end-develop-databricks` | build a serving package on Databricks |
| Deploy endpoint on Databricks | `haipipe-end-deploy-databricks` | serve the model on Databricks |
| Local deploy / MLflow | `haipipe-end-deploy-local`, `haipipe-end-deploy-mlflow` | non-Databricks targets |

[TODO: JL confirm this maps to how REACH actually trains + deploys, and add any REACH-specific cluster config, cluster policy, or library install notes.]

## Deploy a REACH-trained model
Yes, you can serve a REACH-trained model on Databricks: MLflow Model Registry -> Model Serving endpoint (a REST API). Full steps, the skills to use, and the governance gate are in `90-howtos/deploy-model-databricks-reach.md`. Note: deploying AI on human-subjects data needs an AI HSR Consult first (`70-ai-hsr-consult.md`).

## Cluster / runtime notes
- Cluster sizes, runtime version, allowed libraries, MLflow tracking URI: [TODO: JL]
- Getting data into the notebook (mount points, catalog/schema names): [TODO: JL]

## Links
- inHealth research / REACH: https://www.hopkinsmedicine.org/inhealth/research
- OMOP on PMAP (data model you query): https://pm.jh.edu/how-it-works/omop/

📄 The skill table is real and lives in this repo. REACH-specific URLs and cluster config are TODO.
