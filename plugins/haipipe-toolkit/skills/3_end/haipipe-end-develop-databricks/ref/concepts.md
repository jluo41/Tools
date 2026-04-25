haipipe-end-develop-databricks — Concepts (DEFERRED)
======================================================

Placeholder for the Databricks training-target specialist. To be filled in
when `platform-databrick-training/` is added to the project.

---

Expected backing repo
---------------------

`platform-databrick-training/` (sibling of this checkout, not yet present).
Anticipated layout (mirrors `platform-sagemaker-training/`):

```
platform-databrick-training/
├── notebooks/                       Databricks notebooks (training entry)
├── wheels/                          packaged training wheel(s)
├── scripts/
│   ├── build_wheel/
│   │   └── build_training_wheel.py  build training wheel
│   ├── build_training_job/
│   │   └── build_training_job.py    compose Databricks Job spec
│   └── run_training_job/
│       ├── run_train_local_system.py    --stage system
│       ├── run_train_local_cluster.py   --stage cluster (attached)
│       └── run_databricks_job.py        --stage job (managed)
├── config/                          project YAML configs
└── job-specs/                       Databricks Job JSON definitions
```

---

Job shape (planned)
-------------------

```
Preprocess (optional)  →  Train  →  Reorganize       (linear, single Job)
                                       ║
                                       ╚══════════►  RegisterUCModel
```

Implementation choices to settle before lifting "deferred":

  - **Task type**: notebook task (interactive-friendly) vs wheel task
    (reproducible, version-pinned).
  - **Registry**: Unity Catalog (`databricks-uc`) vs workspace MLflow.
    UC is the strategic default; workspace registry is the fallback for
    workspaces that haven't enabled UC.
  - **Cluster**: dedicated job cluster (clean, slow start) vs all-purpose
    cluster (faster, less reproducible).

---

Required Databricks surface
---------------------------

  - Workspace URL + token (via `DATABRICKS_HOST` / `DATABRICKS_TOKEN` or
    profile in `~/.databrickscfg`)
  - UC catalog + schema (or workspace MLflow registry)
  - Cluster spec: instance pool or node-type IDs, libraries to install
  - Storage: DBFS or Unity Catalog volume for the workspace artifacts

---

Output contract (planned)
--------------------------

After a successful develop run, the consumer (`-deploy-databricks`) gets:

  (a) UC model URI:   `models:/<catalog>.<schema>.<model_name>/<version>`, or
  (b) Workspace URI:  `models:/<model_name>/<version>` (non-UC workspaces)

plus the Endpoint_Set export under `_WorkSpace/6-EndpointStore/<endpoint_set>/`
for non-Databricks deploy targets.

---

Cross-skill boundaries
----------------------

Same boundary as `-develop-sagemaker`: this skill OWNS the build, the deploy
specialists OWN the serve, the Endpoint_Set artifact is the contract between
them.

---

Lifting "deferred"
-------------------

When `platform-databrick-training/` is added:
  1. Replace the placeholder procedures in `SKILL.md` with concrete commands.
  2. Update the description frontmatter — drop the `STATUS: DEFERRED` prefix.
  3. Add this skill to the no-args dashboard fan-out in
     `../haipipe-end/SKILL.md`.
  4. Update `Tools/plugins/haipipe-toolkit/docs/2-folder-tree.txt` to drop
     the deferred marker.
