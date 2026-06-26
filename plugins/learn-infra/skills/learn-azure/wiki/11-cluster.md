Clusters
========

What it is
----------

A cluster is a set of VMs that run your code. Databricks manages the
infrastructure — you configure size, runtime, and libraries.

Cluster vs Serverless
---------------------

  Cluster (classic) ........... You pick VM type, node count, runtime.
                                Full control. Predictable environment.
                                Requires vCPU quota.

  Serverless SQL warehouse .... Databricks manages everything. Pay per query.
                                Uses Python 3.10 (may be incompatible).
                                No vCPU quota needed from your subscription.

  Serverless compute .......... For notebooks/jobs. Databricks-managed.
                                Also Python 3.10.

For our pipeline: USE CLASSIC CLUSTERS. Serverless Python 3.10 is too
incompatible with our pandas 1.5.3 / Python 3.9 codebase.

Key configuration
-----------------

  Runtime ........... Use Databricks Runtime ML (includes MLflow, sklearn, etc.)
  Node type ......... Standard_DS3_v2 (4 cores, 14 GB) is a good starting point
  Workers ........... 0 for single-node (dev), 2+ for production
  Auto-terminate .... Always set this (e.g. 30 min idle) to save costs
  Init script ....... Use to install custom packages at cluster start

    # Example init script (stored in a Volume)
    #!/bin/bash
    pip install pandas==1.5.3 datasets tqdm

How to check
------------

In workspace: Compute -> All-purpose compute
CLI: databricks clusters list (requires Databricks CLI)
