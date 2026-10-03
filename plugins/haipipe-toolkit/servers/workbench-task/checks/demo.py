"""Create a synthetic Task Block for a local workbench preview.

Usage: python servers/workbench-task/checks/demo.py /tmp/task-workbench-demo
The Demo project must not already exist; no existing project is overwritten.
"""
from pathlib import Path
import argparse
import json
from datetime import datetime, timezone

import yaml


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def add_task(board, job, task, title, statuses, *, signed=False, report=False):
    folder = board / job / task
    address = board.name[:3] + job[:3] + task[:3]
    reading = ("✅ read · Demo reviewer · 2026-10-02T12:05:00Z" if signed else "⬜ unread")
    write(folder / (task + ".md"), f"""# {title}
folder-kind: task
state: 🟡 OPEN

## Opening

Synthetic demonstration data for the Task Workbench.

## Content

### 1 · Result

The demonstration Run records below show progress states.

### 2 · Conclusion

<a id="reading-current"></a>
#### READING · current

| ID | Topic | Verdict Run | Ruling | Meaning |
|---|---|---|---|---|
| R01 | {title} | {address}r01 | {reading} | Demonstration only. |
""")
    write(folder.parent / "src/config-defaults.yaml", "{}\n")
    specs = []
    for index, status in enumerate(statuses, start=1):
        name = f"r{index:02d}_example"
        specs.append({"id": name, "run_type": "task.execute", "cardinality": 1})
        write(folder / "runs" / (name + ".sh"), "#!/bin/sh\n# Synthetic demonstration Ticket.\n")
        write(folder / "scripts/config" / (name + ".yaml"), "demo: true\n")
        if status == "missing":
            continue
        result = folder / "results" / name
        receipt = {"run": name, "address": address + f"r{index:02d}", "family": "Task",
                   "operation": "execute", "target": title, "status": status,
                   "ticket": f"{task}/runs/{name}.sh", "result": f"{task}/results/{name}",
                   "started_at": None if status == "planned" else "2026-10-02T12:00:00Z",
                   "finished_at": "2026-10-02T12:04:00Z" if status in {"complete", "failed"} else None,
                   "failure": "Example validation failed: expected output column missing" if status == "failed" else None}
        write(result / "runtime.yaml", yaml.safe_dump(receipt, allow_unicode=True))
        if status == "complete":
            write(result / "metrics.json", '{"demo": true, "rows": 1200}\n')
    write(folder / "workflow/plan.yaml", yaml.safe_dump({"name": task, "run_specs": specs}))
    if report:
        write(folder / "workflow/report.yaml", yaml.safe_dump({
            "summary": {"status": "closed", "terminal_route": "CLOSE", "actual_runs": len(statuses)}}))
    return folder


def build_demo(root):
    root = Path(root).resolve()
    project = root / "TaskWorkbench-Demo"
    project.mkdir(parents=True, exist_ok=False)
    write(project / "project.yaml", "schema: haipipe-project/v1\nid: TaskWorkbench-Demo\nprofile: research\nstate: active\ngit_mode: workspace\n")
    board = project / "tasks/b11_model_comparison"
    write(board / "board.md", """# Model comparison · demo
board-kind: task-block
spine: Follow a model comparison from source checks through evaluation and interpretation.
close: Required executions pass, reports are current, and all results receive a signed reading and Page CHECK.

## Topic

Synthetic data for previewing the Workbench. No project execution is represented.
""")
    add_task(board, "j01_data_checks", "t01_source_audit", "Audit source coverage", ["complete"], signed=True, report=True)
    add_task(board, "j01_data_checks", "t02_features", "Review feature readiness", ["complete", "complete"])
    add_task(board, "j02_model_training", "t01_baseline", "Train the baseline", ["complete", "running"])
    add_task(board, "j02_model_training", "t02_tuning", "Tune model parameters", ["failed"])
    add_task(board, "j03_evaluation", "t01_metrics", "Evaluate held-out metrics", ["planned"])
    add_task(board, "j03_evaluation", "t02_robustness", "Check robustness", ["missing"])
    add_question_demo(board)
    return board


def add_question_demo(board):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from task_questions import replace_register
    rows = [
        dict(id="Q01", title="Comparable conditions",
             question="Can we compare both methods using the same data and evaluation rules?",
             hypothesis="Identical inputs and evaluation rules allow a fair comparison.",
             acceptance="Record the data version, split and metric.",
             work=[dict(path="j01_data_checks/t01_source_audit", stage="Data", role="Which records can both methods use?"),
                   dict(path="j01_data_checks/t02_features", stage="Data", role="Can both methods use comparable features?")],
             report="reports/q01_comparable_conditions/q01_comparable_conditions.md"),
        dict(id="Q02", title="Method improvement",
             question="Does the new method improve the metric consistently?",
             hypothesis="The gain survives repeated evaluations.", acceptance="Complete held-out evaluation and uncertainty analysis.",
             work=[dict(path="j01_data_checks/t01_source_audit", stage="Data", role="Reuse the same comparison conditions."),
                   dict(path="j02_model_training/t01_baseline", stage="Training", role="How does the baseline perform?"),
                   dict(path="j02_model_training/t02_tuning", stage="Training", role="Which settings improve the model?"),
                   dict(path="j03_evaluation/t01_metrics", stage="Evaluation", role="Does the gain hold on unseen data?")],
             report="reports/q02_method_improvement/q02_method_improvement.md"),
        dict(id="Q03", title="Cost and usefulness",
             question="Is the improvement worth the added cost?",
             hypothesis="The benefit justifies its resource cost.", acceptance="Compare benefits and costs against the baseline.",
             work=[], report="reports/q03_cost_usefulness/q03_cost_usefulness.md"),
    ]
    head = board / "board.md"
    text = replace_register(head.read_text(), "Questions", "questions", rows)
    text = replace_register(text, "Related resources", "resources", [
        dict(title="Evaluation protocol · example", url="https://example.test/evaluation", questions=["Q01"],
             contribution="An illustrative external reference for comparison design.", notes="Synthetic placeholder; replace with an actual source."),
    ])
    write(head, text)
    reports = [
        ("answered", "The demo inputs share the recorded comparison conditions.",
         "[Source metrics](../../j01_data_checks/t01_source_audit/results/r01_example/metrics.json)",
         "This answer applies only to the synthetic data in this example.", "Use this protocol for Question 2."),
        ("partial", "A stable improvement has not yet been established.",
         "[Baseline receipt](../../j02_model_training/t01_baseline/results/r01_example/runtime.yaml)",
         "Tuning failed and held-out evaluation is pending.", "Inspect the tuning failure, then complete evaluation."),
        ("open", "No cost conclusion is available yet.", "No cost evidence has been collected.",
         "Benefits and resource costs still need comparison.", "Define the cost comparison and its acceptance criterion."),
    ]
    for row, (state, answer, evidence, limits, next_step) in zip(rows, reports):
        # Synthetic preview sources, not accepted results from a real project.
        content = f"""# {row['title']}
state: 🔴 OPEN · synthetic demonstration, no Page CHECK
answers: {row['id']}
answer-status: {state}
results-read: {datetime.now(timezone.utc).isoformat()}

## Opening

{answer}

**Where this Page sits:** [{row['id']} in this demonstration Block](../../board.md).

**Why it matters:** This synthetic Page demonstrates how Question reports appear in the Workbench.

## Content

### 1 · Answer

#### 1.1 · Interpretation

{answer}

### 2 · Evidence

#### 2.1 · Sources

{evidence}

### 3 · Limits

#### 3.1 · Boundaries

{limits}

### 4 · Next

#### 4.1 · Action

{next_step}
"""
        write(board / row['report'], content)
        page = board / row['report']
        write(page.parent / 'page.toml', 'version = 1\nsource = ' + json.dumps(page.name)
              + '\ntitle = ' + json.dumps(row['title']) + '\n')
    scene = {"type":"excalidraw", "version":2, "source":"task-workbench-demo",
             "elements":[], "appState":{"viewBackgroundColor":"#ffffff"}, "files":{}}
    for index in (1, 2, 3):
        write(board / "studio" / f"Drawing {index}.excalidraw", json.dumps(scene))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(build_demo(args.root))
