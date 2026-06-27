# 💡 How to deploy a REACH-trained model on Databricks

Short answer: yes, you can. The supported path is MLflow Model Registry -> Databricks Model Serving endpoint, which gives you a REST API. Use the existing repo skills to run it; the steps below are the pattern, and the REACH-specific enablement plus governance are the gates.

## Governance gate first
Serving an AI/ML model that was trained on human-subjects data is an AI-in-HSR decision, not only an engineering one. Before you stand up an endpoint:
- Get an AI HSR Consult from the JHM Office of Human Subjects Research. See `../70-ai-hsr-consult.md`.
- Confirm REACH / Data Trust terms allow serving a model trained on REACH data, and where the endpoint may be called from. [TODO: JL]

## Use the existing skills (preferred)
| Step | Skill |
|---|---|
| Build the serving package on Databricks | `haipipe-end-develop-databricks` |
| Deploy / serve on Databricks | `haipipe-end-deploy-databricks` |
| Or serve via MLflow | `haipipe-end-deploy-mlflow` |

These already encode our flow. Prefer them over hand-running the Serving UI.

## The Databricks pattern (what those skills do under the hood)
1. Log the trained model to MLflow and register it (Unity Catalog or Workspace Model Registry). Needs MLflow 1.29 or higher.
2. Create a Model Serving endpoint: open Serving in the sidebar, click Create serving endpoint, name it, pick the model and version, set the traffic percentage, pick the compute scale-out size.
3. The endpoint is a REST API. Query it from an allowed client.
4. For repeatable promotion, use an MLflow deployment job: evaluate -> approve -> deploy.
(Source: Databricks Model Serving docs, links below.)

## REACH-specific unknowns [TODO: JL]
- Is Model Serving enabled in the REACH workspace, and under which compute / cluster policy?
- Unity Catalog or Workspace Model Registry in REACH?
- Where may the endpoint be called from: inside the enclave only, or exposed? What are the PHI egress rules?
- Endpoint auth, and the MLflow tracking URI for REACH.

## Links
- Deploy models using Model Serving: https://docs.databricks.com/aws/en/machine-learning/model-serving/
- Tutorial, deploy and query a custom model: https://docs.databricks.com/aws/en/machine-learning/model-serving/model-serving-intro
- Log, load, and register MLflow models: https://docs.databricks.com/aws/en/mlflow/models
- AI HSR Consult: `../70-ai-hsr-consult.md`
- See also: `../40-databricks.md`

📄 Databricks pattern verified 2026-06-25 from docs.databricks.com. REACH enablement and governance are TODO.
