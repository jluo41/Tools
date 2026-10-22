#!/usr/bin/env python3
"""Every type skill carries one `## Type contract` (ref/types.md § The type contract), so the type door reads
every kind of Task the same way (JL 261021: "the task to all kinds of the tasks")."""

import re
import unittest
from pathlib import Path

import yaml

SKILL = Path(__file__).resolve().parents[1]
FAMILY = SKILL.parent
KEYS = ["task-type", "skill", "does", "worker", "config", "ticket", "result", "heavy", "roles", "companions",
        "plan_sample"]
ROLES = {"trial", "make", "fix", "check", "describe", "figures", "evidence", "publish"}


def contract(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## Type contract[ \t]*\n(.*?)(?=^## |\Z)", text)
    if not m:
        return {}
    fence = re.search(r"(?ms)^```ya?ml[ \t]*\n(.*?)^```", m.group(1))
    return (yaml.safe_load(fence.group(1)) or {}) if fence else {}


class TypeContractTest(unittest.TestCase):
    def setUp(self):
        self.types = (SKILL / "ref" / "types.md").read_text(encoding="utf-8")
        self.skills = sorted(FAMILY.glob("*/haipipe-task-for-*/SKILL.md"))

    def test_every_type_skill_is_in_the_type_table(self):
        self.assertGreaterEqual(len(self.skills), 12)
        for md in self.skills:
            with self.subTest(skill=md.parent.name):
                self.assertIn(md.parent.name, self.types)

    def test_every_type_skill_carries_its_contract(self):
        for md in self.skills:
            with self.subTest(skill=md.parent.name):
                c = contract(md)
                self.assertEqual(KEYS, list(c), "the keys of ref/types.md § The type contract, in order")
                self.assertEqual(md.parent.name, c["skill"])
                self.assertTrue(set(c["roles"]) <= ROLES, c["roles"])
                for value in re.split(r"\s*[|·]\s*", str(c["task-type"])):
                    self.assertIn(value, self.types, "each task-type value is named in ref/types.md")
                self.assertIn("runs/", str(c["ticket"]), "a ticket lives in its Run's folder")
                self.assertIn("result/", str(c["result"]), "a Result is runs/<run>/result/")
                sample = str(c["plan_sample"])
                if sample != "none":
                    for one in re.findall(r"[\w./{},-]+\.yaml", sample):
                        for path in self.expand(md.parent, one):
                            self.assertTrue(path.is_file(), path)

    @staticmethod
    def expand(folder: Path, pattern: str) -> list[Path]:
        m = re.match(r"(.*)\{([^}]*)\}(.*)", pattern)
        names = [m.group(1) + part + m.group(3) for part in m.group(2).split(",")] if m else [pattern]
        return [folder / n for n in names]


if __name__ == "__main__":
    unittest.main()
