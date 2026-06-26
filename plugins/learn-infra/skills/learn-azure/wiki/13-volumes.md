Volumes
=======

What it is
----------

A Volume is Databricks' file-based storage inside Unity Catalog. It's where
our _WorkSpace data lives in the cloud. Think of it as a cloud folder that
notebooks can read/write via /Volumes/... paths.

Two types
---------

  Managed volume ..... Databricks controls the underlying storage location.
                       Easier to set up. Data deleted if volume is dropped.

  External volume .... Points to an existing cloud storage location (ADLS,
                       S3). You manage the storage. Volume is just a pointer.

Our setup
---------

    /Volumes/reach_catalog/reach_adhd/reach_space/_WorkSpace/
      ├── 0-RawDataStore/
      ├── 1-SourceStore/
      ├── 2-RecStore/
      ├── ...
      └── 6-EndpointStore/

Upload data to volumes:

    # From notebook
    dbutils.fs.cp("file:/local/path", "/Volumes/catalog/schema/volume/path")

    # From local machine (Databricks CLI)
    databricks fs cp local_file dbfs:/Volumes/catalog/schema/volume/path

Access in code
--------------

    # In a Databricks notebook, volumes appear as regular file paths:
    import pandas as pd
    df = pd.read_parquet("/Volumes/reach_catalog/reach_adhd/reach_space/_WorkSpace/1-SourceStore/...")
