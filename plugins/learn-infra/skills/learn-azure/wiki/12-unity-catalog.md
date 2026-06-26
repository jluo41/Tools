Unity Catalog
=============

What it is
----------

Unity Catalog is Databricks' data governance layer. It organizes data and
models into a three-level namespace.

The hierarchy
-------------

    Metastore (one per region, shared across workspaces)
      └── Catalog (e.g. "reach_catalog")
            └── Schema (e.g. "reach_adhd")
                  ├── Tables
                  ├── Volumes (file storage)
                  └── Models (MLflow registered models)

Why it matters
--------------

- Model Serving requires models to be registered in Unity Catalog.
- Volumes are where we store pipeline data (_WorkSpace files).
- Tables can be used for structured data (we mostly use Volumes + parquet).

How to check
------------

    -- In a notebook or SQL editor:
    SHOW CATALOGS;
    SHOW SCHEMAS IN reach_catalog;
    SHOW VOLUMES IN reach_catalog.reach_adhd;
    SHOW MODELS IN reach_catalog.reach_adhd;
