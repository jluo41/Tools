"""items_task.py, the items Task's three steps (b15 s41), on a made-up corpus: plan proposes, the worker refuses an
unsigned recipe or build, the items keep the answers out, a revision is a new version, the map is built."""
from __future__ import annotations

import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import items_task as IT  # noqa: E402

REPLIES = ["Sure, here is a picnic plan with sandwiches and fruit for the park",
           "I cannot help with that request because it could hurt someone badly",
           "Taxes are due in April; keep your receipts and file on time this year",
           "That sounds like a lovely hike along the river with your family today"]


def corpus(root: Path) -> Path:
    """Made-up ratings: 8 chats × 3 raters; `gold` is the experts' key, `verdict` each rater's answer."""
    folder = root / "_WorkSpace" / "LabelingStore" / "demo" / "corpus" / "raw"
    folder.mkdir(parents=True)
    path = folder / "ratings.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "rater_id", "chat_id", "context", "reply", "gold", "gold_reason", "verdict"])
        n = 0
        for chat in range(1, 9):
            for rater in range(1, 4):
                n += 1
                w.writerow([n, f"r{rater}", chat, f"ASK: question number {chat} about a plan\nBOT: a short answer\n"
                                                  f"ASK: and a follow up {chat}",
                            REPLIES[chat % 4] + f" {chat}", "Yes" if chat % 2 else "No",
                            "the reply gives harmful steps in detail" if chat % 2 else "the reply is plainly fine",
                            ["Yes", "No", "Unsure"][(chat + rater) % 3]])
    return path


class ItemsTaskTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / "env.sh").write_text("")
        corpus(self.root)
        job = self.root / "Project-X" / "labeling" / "b01_demo" / "j01_demo_safety"
        self.task = job / "t01_demo_items"
        self.task.mkdir(parents=True)
        (job / "j01_demo_safety.md").write_text("# j01\n\ndataset: Demo-8\ndata: _WorkSpace/LabelingStore/demo/corpus/raw/\n")
        (self.task / "t01_demo_items.md").write_text("# Demo as items\ntask-type: items\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_worker(self, run: Path):
        """What the ticket does: the worker under the Run's config, writing its result/."""
        env = {"HAIPIPE_CONFIG": str(self.task / "scripts" / "config" / f"{run.name}.yaml"),
               "RESULT_DIR": str(run / "result"), "HEAVY_DIR": str(self.root / "_heavy" / run.name)}
        (run / "result").mkdir(exist_ok=True)
        saved = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        try:
            IT.worker_main()
        finally:
            for k, v in saved.items():
                os.environ.pop(k) if v is None else os.environ.__setitem__(k, v)
        (run / "result" / "runtime.yaml").write_text(f"run: {run.name}\nstatus: complete\n")

    def edit(self, run: Path, change):
        path = self.task / "scripts" / "config" / f"{run.name}.yaml"
        cfg = IT.read_yaml(path)
        change(cfg)
        IT.write_yaml(path, cfg)

    def describe(self) -> Path:
        run = IT.plan(self.task, "describe")
        cfg = IT.read_yaml(self.task / "scripts" / "config" / f"{run.name}.yaml")
        self.assertEqual(cfg["unit"], "chat_id")                       # the guesses the agent corrects
        self.assertIn("reply", cfg["text"])
        self.assertTrue((self.task / "scripts" / "prepare.py").is_file())
        self.assertIn("notebook: off", (self.task / "scripts" / "config" / f"{run.name}.yaml").read_text())

        def typed(c):
            c["one_row_is"] = "One rater's verdict on one chat."
            c["background"] = {"what": "a made-up corpus", "license": "none"}
            c["labels"] = {"expert": ["gold", "gold_reason"], "rater": ["verdict"]}
            c["text"] = ["context", "reply"]
        self.edit(run, typed)
        self.run_worker(run)
        return run

    def test_three_steps_from_raw_rows_to_a_map(self):
        d = self.describe()
        card = json.loads((d / "result" / "description.json").read_text())
        self.assertEqual(card["grain"]["proof"]["distinct_chat_id"], 8)
        self.assertEqual(card["grain"]["proof"]["distinct_rater_id"], 3)
        self.assertEqual({lb["column"]: lb["counted_per"] for lb in card["labels"]},
                         {"gold": "chat_id", "gold_reason": "chat_id", "verdict": "row"})
        self.assertEqual(card["background"]["what"], "a made-up corpus")
        self.assertNotIn("picnic", json.dumps(card["synth_df"]))        # text is never shown in the made-up row
        self.assertEqual(len(card["samples"]["rows"]), 5)

        run = IT.plan(self.task, "items")
        cfg = IT.read_yaml(self.task / "scripts" / "config" / f"{run.name}.yaml")
        r = cfg["recipe"]
        self.assertEqual((r["unit"], r["main"], r["item_id"]), ("chat_id", "reply", "demo8-{chat_id}"))
        self.assertEqual(r["context_before"], {"column": "context", "turns": {"ASK": "ASK", "BOT": "BOT"}})
        self.assertEqual(cfg["out"], "_WorkSpace/LabelingStore/demo/corpus/items-v1")
        with self.assertRaises(SystemExit):                             # a recipe nobody signed never runs
            self.run_worker(run)
        self.edit(run, lambda c: c["recipe"]["context_before"].update(turns={"ASK": "Person", "BOT": "AI"}))
        IT.sign(self.task, run.name, "a person")
        self.run_worker(run)
        res = run / "result"
        self.assertTrue(json.loads((res / "check.json").read_text())["passed"])
        store = self.root / "_WorkSpace/LabelingStore/demo/corpus/items-v1"
        items = IT.read_jsonl(store / "items.jsonl")
        self.assertEqual(len(items), 8)
        self.assertEqual(items[0]["item_id"], "demo8-1")
        self.assertTrue(items[0]["context_before"].startswith("Person: question number 1"))
        self.assertNotIn("gold", items[0])                              # the answers stay out of the items
        truth = IT.read_jsonl(store / "items.ground-truth.jsonl")
        self.assertEqual(truth[0]["gold"], "Yes")
        self.assertEqual(len(IT.read_jsonl(store / "items.raters.jsonl")), 24)
        stats = json.loads((res / "stats.json").read_text())
        self.assertEqual(sum(stats["words_judged"]["histogram"]["counts"]), 8)

        again = IT.plan(self.task, "items", notes="keep only the last turn before the reply", revise_of=run.name)
        cfg = IT.read_yaml(self.task / "scripts" / "config" / f"{again.name}.yaml")
        self.assertTrue(again.name.endswith("_revise"))
        self.assertEqual((cfg["revise_of"], cfg["out"]), (run.name, "_WorkSpace/LabelingStore/demo/corpus/items-v2"))
        self.assertEqual(cfg["notes"], "keep only the last turn before the reply")
        IT.sign(self.task, again.name, "a person")
        self.run_worker(again)
        self.assertTrue((store.parent / "items-v2" / "items.jsonl").is_file())
        self.assertEqual(IT.latest(self.task, "items"), again)

        emb = IT.plan(self.task, "embed", model="tfidf-svd")
        with self.assertRaises(SystemExit):                             # a build nobody agreed never runs
            self.run_worker(emb)
        IT.sign(self.task, emb.name, "a person")
        self.edit(emb, lambda c: c.update(groups=2, map="pca"))
        self.run_worker(emb)
        res = emb / "result"
        self.assertEqual(len(json.loads((res / "map.json").read_text())), 8)
        self.assertEqual(len(json.loads((res / "map3d.json").read_text())), 8)
        groups = json.loads((res / "groups.json").read_text())
        self.assertEqual(sum(g["size"] for g in groups), 8)
        self.assertTrue(all(g["typical"] for g in groups))
        self.assertTrue((self.root / "_heavy" / emb.name / "vectors.npy").is_file())
        self.assertEqual([s["operation"] for s in IT.status(self.task)], ["describe", "items", "items", "embed"])

    def test_a_version_is_never_rewritten_and_a_closed_run_is_never_signed(self):
        self.describe()
        run = IT.plan(self.task, "items")
        IT.sign(self.task, run.name, "a person")
        self.run_worker(run)
        with self.assertRaises(SystemExit):
            IT.sign(self.task, run.name, "a person")
        (run / "result" / "runtime.yaml").write_text("status: failed\n")      # rerun the same Run: refused
        with self.assertRaises(SystemExit):
            IT.make_items(IT.read_yaml(self.task / "scripts" / "config" / f"{run.name}.yaml"), self.root, run / "result")

    def test_next_says_who_does_what_from_the_job_folder(self):
        job = self.task.parent
        n = IT.next_step(job)                                   # a Job folder finds its one items Task
        self.assertEqual((n["step"], n["who"]), ("describe", "agent"))
        self.assertEqual(n["files"], ["_WorkSpace/LabelingStore/demo/corpus/raw/ratings.csv"])
        self.describe()
        run = IT.plan(self.task, "items")
        n = IT.next_step(job)
        self.assertEqual((n["step"], n["who"], n["run"]), ("items", "person", run.name))   # the person signs
        self.assertIn("press Sign", n["do"])
        IT.sign(self.task, run.name, "a person")
        n = IT.next_step(job)
        self.assertEqual((n["step"], n["who"]), ("items", "agent"))
        self.assertTrue(n["command"].startswith("bash ") and n["command"].endswith(f"{run.name}.sh"))

    def test_draw_again_reads_live_and_writes_nothing(self):
        self.describe()
        before = sorted(p.as_posix() for p in self.root.rglob("*"))
        a = IT.sample(self.task, "raw", 1)
        b = IT.sample(self.task, "raw", 1)
        c = IT.sample(self.task, "raw", 2)
        self.assertEqual(a, b)
        self.assertNotEqual([r["row"] for r in a["rows"]], [r["row"] for r in c["rows"]])
        self.assertEqual(len(a["rows"]), 5)
        self.assertEqual(sorted(p.as_posix() for p in self.root.rglob("*")), before)


if __name__ == "__main__":
    unittest.main()
