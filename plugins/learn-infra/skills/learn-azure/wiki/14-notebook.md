Notebooks
=========

What it is
----------

Databricks notebooks are interactive documents (like Jupyter) that run on
a cluster. They support Python, SQL, Scala, and R cells.

Key differences from local Jupyter
----------------------------------

- Code runs on the cluster, not your laptop.
- %pip installs go to the cluster (lost on restart unless in init script).
- dbutils is available for file ops, secrets, and notebook chaining.
- display() replaces plt.show() for rich output.

Package installation
--------------------

    # In a notebook cell — installs for this session only
    %pip install pandas==1.5.3 datasets tqdm

    # For persistent installs, use a cluster init script (see 11-cluster.md)

dbutils essentials
------------------

    dbutils.fs.ls("/Volumes/...")           # list files
    dbutils.fs.cp(src, dst)                 # copy files
    dbutils.fs.rm(path, recurse=True)       # delete
    dbutils.notebook.run("path", timeout)   # run another notebook
    dbutils.secrets.get("scope", "key")     # access secrets

Notebook chaining (our Z01 pattern)
------------------------------------

Our Z01_run_databricks orchestrator uses dbutils.notebook.run() to chain
stage notebooks sequentially:

    dbutils.notebook.run("./01_source", timeout_seconds=3600)
    dbutils.notebook.run("./02_record", timeout_seconds=3600)
    # ...each notebook runs one pipeline stage
