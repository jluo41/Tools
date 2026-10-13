"""excalidraw-task: a Task made on a small Block, drawn and checked; the face's short words win; one topic per Task."""
import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import task_drawing as td  # noqa: E402
from draw import MAP_WORDS, Drawing  # noqa: E402

PAGE = """# Decoding and Sampling

## Opening

How do greedy search and sampling shape generated text?
This page files 2 videos.

## Content

### 1 · Concept · Decoding and sampling

**What it is**: A model scores every token at each step. Decoding picks the next token
from those scores, by a rule or at random.

**How it works**: Softmax turns scores into probabilities.

- **Greedy**: take the top token every step.
- **Top-p**: keep the smallest set reaching p, then sample.

**Why it matters**: The same model writes very different text under different settings.

**The videos on this page**:

| # | Run | Video | Length | Interview | State |
|---|---|---|---|---|---|
| 1 | r01 | presence penalty explained | 3m 37s | · | drafted |
| 2 | r02 | greedy versus sampling | 3m 15s | ★ | drafted |

**How the videos fit**: r02 is the overview. r01 covers the penalties in full.

**Interview questions**:

- *Why not beam search for chat?* The likeliest text is often dull.
- *What does temperature change?* How peaked the distribution is.

### 2 · r01 · presence penalty explained

**r01**: This video explains presence and frequency penalties.
```text
Video     → https://www.bilibili.com/video/BV1/
Title     → 存在惩罚和频率惩罚
Creator   → GreekCodeBear · 3m 37s · interview-marked: no
State     → drafted from the transcript; claims not checked against the video
```

[Bilibili video](https://www.bilibili.com/video/BV1/) · [Result Card](runs/r01_v/result/r01_v.md)

**Key points**: A picked token looks likelier next time, so the model loops. The fix lowers the scores of tokens
already written. Presence takes a fixed amount; frequency takes more with every repeat.
- **Interview hook**: Presence is for topic variety; frequency is for word loops.
- **Check before reuse**: the exact formula on screen; the range of -2 to 2.

### 3 · r02 · greedy versus sampling

**r02**: This video compares greedy decoding and sampling.
```text
Video     → https://www.bilibili.com/video/BV2/
Title     → 贪心还是采样
Creator   → GreekCodeBear · 3m 15s · interview-marked: yes
State     → drafted from the transcript; claims not checked against the video
```

**Key points**: Greedy is short-sighted. Sampling cuts the tail, then draws at random.
- **Interview hook**: Greedy is locally best; sampling suits open tasks.
- **Check before reuse**: the on-screen example.

## Aims
"""


class TaskDrawingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project-Example" / "discovery" / "b51_serve"
        job = self.block / "j01_decoding"
        job.mkdir(parents=True)
        (self.block / "board.md").write_text("# b51 · serve\n")
        (job / "j01_decoding.md").write_text("# j01 · decoding\n")           # a Job's own face: not a Task
        for name in ("t01_sampling", "t02_more"):
            (job / name).mkdir()
            (job / name / f"{name}.md").write_text(PAGE)
        self.job = job

    def tearDown(self):
        self.tmp.cleanup()

    def quiet(self, fn, *a, **k):
        with contextlib.redirect_stdout(io.StringIO()):
            return fn(*a, **k)

    def frames(self, drawing: Path):
        els = json.loads(drawing.read_text())["elements"]
        return els, [e for e in els if e["type"] == "frame"]

    def test_a_job_makes_one_topic_per_task_and_reads_the_page(self):
        outs = self.quiet(td.make, self.job, 1)
        self.assertEqual([o.parent.name for o in outs], ["s01-t01-sampling", "s02-t02-more"])
        topic = outs[0].parent
        self.assertEqual(topic.parents[1], self.block.resolve())              # the Block's studio, not the Job's
        self.assertIn("name: j01_decoding/t01_sampling", (topic / f"{topic.name}.md").read_text())
        els, frames = self.frames(outs[0])
        names = [f["name"] for f in frames]
        self.assertEqual(len(frames), 3)                                       # the idea, then one per video
        self.assertTrue(names[0].startswith("⓪ t01 · Decoding and Sampling"))
        self.assertEqual([n.split(" · ")[0] for n in names[1:]], ["r02", "r01"])   # How the videos fit's order
        text = " ".join(" ".join(e.get("text", "").split()) for e in els if e["type"] == "text")
        self.assertIn("🎯 How do greedy search and sampling shape generated text?", text)
        self.assertNotIn("This page files", text)                              # the Opening's question line only
        self.assertIn("Softmax turns scores into probabilities.", text)                # How it works: its lead line
        self.assertIn("① Greedy take the top token every step.", text)               # then its steps, point and why
        self.assertIn("This video explains presence and frequency penalties.", text)
        self.assertIn("❓ the exact formula on screen", text)
        self.assertIn("then r01: covers the penalties in full", text)
        self.assertIn("▪ Why not beam search for chat? The likeliest text is often dull.", text)   # with its answer
        self.assertIn("🔗 https://www.bilibili.com/video/BV1/", text)
        self.assertIn("Result Card", (topic / f"{topic.name}.md").read_text())   # the face's list of videos

    def test_the_face_words_win_and_keep_seven(self):
        topic = self.quiet(td.make, self.job / "t01_sampling", 3)[0].parent
        face = topic / f"{topic.name}.md"
        face.write_text(face.read_text().replace("  videos: {}", "\n".join([
            "  videos:", "    r01:", "      name: Presence vs frequency penalty",
            "      says: Penalties lower repeated tokens to break a loop.",
            "      points: [A picked token loops, Lower the scores of used tokens]",
            "      hook: Presence once; frequency per repeat.", "      check: [The on-screen formula]",
            "      role: the two penalties"])))
        els, frames = self.frames(self.quiet(td.draw, topic))
        self.assertIn("r01 · Presence vs frequency penalty", [f["name"] for f in frames])
        text = " ".join(" ".join(e.get("text", "").split()) for e in els if e["type"] == "text")
        self.assertIn("then r01: the two penalties", text)
        self.assertIn("❓ The on-screen formula", text)
        for f in frames:                                                       # ⑦: few words, none small
            words, small = Drawing.words_small(els, f["id"])
            self.assertLessEqual(words, MAP_WORDS, f["name"])
            self.assertEqual(small, 0, f["name"])

    def test_one_topic_per_task(self):
        self.quiet(td.make, self.job / "t01_sampling", 1)
        with self.assertRaises(SystemExit) as err:
            self.quiet(td.make, self.job, 5)
        self.assertIn("t01_sampling is drawn already", str(err.exception))
        self.assertEqual(td.tasks_of(self.block), [])                          # a Block is neither a Task nor a Job
        self.assertTrue(re.match(r"^\[.*t02_more", str(td.tasks_of(self.job)[1:])))


if __name__ == "__main__":
    unittest.main()
