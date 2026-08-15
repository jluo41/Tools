Model Serving
=============

What it is
----------

Databricks Model Serving hosts ML models as REST API endpoints. You register
a model in Unity Catalog, then create a serving endpoint that wraps it.

The flow
--------

    Train model (notebook/job)
      -> Log with MLflow (mlflow.log_model)
      -> Register in Unity Catalog (mlflow.register_model)
      -> Create serving endpoint (UI or API)
      -> POST JSON to endpoint URL -> get predictions

Key concepts
------------

  MLflow model .......... A serialized model + metadata + requirements.
                          Logged with mlflow.pyfunc.log_model().

  Registered model ...... A named model in Unity Catalog with versions.
                          E.g. reach_catalog.reach_adhd.adhd_predictor

  Serving endpoint ...... A live REST API that loads one model version
                          and serves predictions.

  Pyfunc wrapper ........ Custom Python class wrapping your model.
                          Defines load_context() and predict() methods.

Endpoint invocation
-------------------

    import requests

    url = "https://<workspace>.azuredatabricks.net/serving-endpoints/<name>/invocations"
    headers = {"Authorization": "Bearer <token>"}
    payload = {"dataframe_records": [{"col1": val1, "col2": val2, ...}]}

    response = requests.post(url, json=payload, headers=headers)
    predictions = response.json()

Cost note
---------

Serving endpoints bill per hour while active. Scale to zero is available
but has cold-start latency. Turn off endpoints when not in use.
