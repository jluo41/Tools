"""Isolated installer regression checks: python3 -m unittest discover -s diagnostics -p test_installers.py -v."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


class InstallerChecks:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tools-install-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / "repo"
        self.repo.mkdir()
        for name in ("install.sh", "install.ps1", "install-hooks.json"):
            shutil.copy2(REPO / name, self.repo / name)
        # Redirect only the copies' configuration root; never touch the real home.
        shell = self.repo / "install.sh"
        self.redirect_config(shell, 'CLAUDE_DIR="$HOME/.claude"',
                             'CLAUDE_DIR="$SCRIPT_DIR/test-home/.claude"')
        powershell = self.repo / "install.ps1"
        self.redirect_config(powershell,
            '$ClaudeDir   = Join-Path $userHome ".claude"',
            '$ClaudeDir   = Join-Path $ScriptDir "test-home/.claude"')
        self.write("plugins/demo/.claude-plugin/plugin.json", json.dumps({
            "name": "demo", "description": "Installer fixture", "version": "1.0.0",
        }))
        self.write("plugins/demo/skills/layer/example/SKILL.md",
                   "---\nname: example\ndescription: Fixture\nmetadata:\n  aliases: [short]\n---\n")
        self.write("plugins/demo/agents/example-agent.md", "current agent\n")
        self.project = self.base / "workspace"
        for name in (".claude", ".codex", ".agents"):
            (self.project / name).mkdir(parents=True)

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def redirect_config(self, path, old, new):
        source = path.read_text()
        self.assertEqual(source.count(old), 1,
                         f"Cannot safely redirect {path.name}; refusing to run installer")
        path.write_text(source.replace(old, new))

    def run_installer(self, verify=False, extra=(), marketplace=False):
        if self.kind == "shell":
            args = ["bash", str(self.repo / "install.sh"), "--no-marketplace",
                    "--project", str(self.project)]
            if verify:
                args.append("--verify")
        else:
            args = ["pwsh", "-NoProfile", "-File", str(self.repo / "install.ps1"),
                    "-NoMarketplace", "-Symlink", "-Project", str(self.project)]
            if verify:
                args.append("-Verify")
        if marketplace:
            args.remove("--no-marketplace" if self.kind == "shell" else "-NoMarketplace")
        result = subprocess.run(args + list(extra), capture_output=True, text=True, timeout=30)
        return result

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_install_verify_and_preserve_owned_files(self):
        own = self.project / ".claude/skills/example"
        own.mkdir(parents=True)
        (own / "personal.txt").write_text("keep me")
        for _ in range(2):
            self.assert_ok(self.run_installer())
        self.assertEqual((own / "personal.txt").read_text(), "keep me")
        self.assert_ok(self.run_installer(verify=True))
        for tool in (".codex", ".agents"):
            self.assertEqual((self.project / tool / "skills/short").resolve(),
                             self.repo / "plugins/demo/skills/layer/example")

    def test_discovery_scope_and_exclusions(self):
        for path in ("plugins/demo/skills/_old/retired/SKILL.md",
                     "plugins/demo/skills/node_modules/vendor/SKILL.md",
                     "plugins/demo/examples/skills/unrelated/SKILL.md"):
            self.write(path, "---\nname: excluded\n---\n")
        self.write("plugins/demo/agents/nested/nested-agent.md", "nested agent")
        self.write("plugins/demo/agents/_old/retired-agent.md", "retired")
        self.write("plugins/demo/agents/node_modules/vendor-agent.md", "vendor")
        self.assert_ok(self.run_installer())
        skills = self.project / ".claude/skills"
        self.assertEqual({p.name for p in skills.iterdir()}, {"example", "short"})
        agents = self.project / ".claude/agents"
        self.assertEqual({p.name for p in agents.glob("*.md")},
                         {"example-agent.md", "nested-agent.md"})

    def test_quoted_checkout_and_workspace_paths(self):
        moved = self.base / "owner's checkout"
        self.repo.rename(moved)
        self.repo = moved
        moved = self.base / "owner's workspace"
        self.project.rename(moved)
        self.project = moved
        self.assert_ok(self.run_installer())
        self.assert_ok(self.run_installer(verify=True))

    def test_verify_detects_wrong_target_without_writes(self):
        self.assert_ok(self.run_installer())
        link = self.project / ".claude/skills/example"
        link.unlink()
        wrong = self.base / "old-skill"
        wrong.mkdir()
        link.symlink_to(wrong, target_is_directory=True)
        before = link.lstat().st_mtime_ns
        result = self.run_installer(verify=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(link.lstat().st_mtime_ns, before)
        self.assertEqual(link.resolve(), wrong)

    def test_preserve_valid_relative_agent_link(self):
        agents = self.project / ".claude/agents"
        agents.mkdir()
        target = self.project / "custom-agent.md"
        target.write_text("custom")
        link = agents / "custom-agent.md"
        link.symlink_to("../../custom-agent.md")
        self.assert_ok(self.run_installer())
        self.assertTrue(link.is_symlink(), "installer deleted a valid user link")
        self.assertEqual(link.resolve(), target)

    def test_marketplace_preserves_existing_directory(self):
        market = self.repo / "test-home/.claude/plugins/marketplaces/jluo41-tools"
        market.mkdir(parents=True)
        saved = market / "local-work.txt"
        saved.write_text("keep me")
        result = self.run_installer(marketplace=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(market.is_symlink())
        self.assertEqual(saved.read_text(), "keep me")

    def test_marketplace_registration_with_quoted_checkout(self):
        moved = self.base / "owner's checkout"
        self.repo.rename(moved)
        self.repo = moved
        config = self.repo / "test-home/.claude/plugins"
        config.mkdir(parents=True)
        known = config / "known_marketplaces.json"
        known.write_text('{"existing": {"keep": true}}')
        self.assert_ok(self.run_installer(marketplace=True))
        entries = json.loads(known.read_text())
        self.assertEqual(entries["existing"], {"keep": True})
        installed = Path(entries["jluo41-tools"]["installLocation"])
        self.assertEqual(installed.resolve(), self.repo)

    def test_verify_missing_mcp_registration_is_informational(self):
        self.write("plugins/demo/mcp-servers/optional/server.py", "# fixture")
        self.assert_ok(self.run_installer())
        result = self.run_installer(verify=True)
        self.assert_ok(result)
        self.assertIn("not registered in .mcp.json", result.stdout)

    def test_hooks_preserve_custom_hooks_and_are_idempotent(self):
        config = self.repo / "test-home/.claude/settings.json"
        config.parent.mkdir(parents=True)
        guard = {"matcher": "Bash", "hooks": [{"type": "command", "command": "guard.sh"}]}
        notify = {"matcher": "*", "hooks": [{"type": "command", "command": "notify.sh"}]}
        original = {"model": "keep-model", "hooks": {"PreToolUse": [guard], "Stop": [notify]}}
        config.write_text(json.dumps(original))
        flag = "--hooks" if self.kind == "shell" else "-Hooks"
        self.assert_ok(self.run_installer(extra=(flag,)))
        first = json.loads(config.read_text())
        self.assertEqual(first["model"], original["model"])
        self.assertEqual(first["hooks"]["PreToolUse"], [guard])
        self.assertIn(notify, first["hooks"]["Stop"])
        self.assertEqual(len(first["hooks"]["Stop"]), 2)
        self.assert_ok(self.run_installer(extra=(flag,)))
        self.assertEqual(json.loads(config.read_text()), first)


class ShellInstallerTests(InstallerChecks, unittest.TestCase):
    kind = "shell"

    def test_invalid_options_fail_before_creating_links(self):
        for extra in (("--unknown",), ("--project",)):
            with self.subTest(extra=extra):
                result = self.run_installer(extra=extra)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse((self.project / ".claude/skills").exists())

    def test_discovery_ignores_skills_outside_package_skill_root(self):
        self.write("plugins/demo/examples/skills/unrelated/SKILL.md", "fixture")
        script = (self.repo / "install.sh").read_text()
        function = script.split("enumerate_skills() {", 1)[1].split("\n}\n", 1)[0]
        result = subprocess.run(
            ["bash", "-c", "enumerate_skills() {" + function +
             '\n}\nenumerate_skills "$1"', "test", str(self.repo / "plugins")],
            capture_output=True, text=True, timeout=30)
        self.assert_ok(result)
        self.assertNotIn("unrelated", result.stdout)

    def test_hooks_create_settings_directory(self):
        self.assert_ok(self.run_installer(extra=("--hooks",)))
        settings = self.repo / "test-home/.claude/settings.json"
        self.assertIn("Stop", json.loads(settings.read_text())["hooks"])

    def test_failed_verify_cleans_temporary_files(self):
        import os
        from unittest.mock import patch
        temporary = self.base / "verify-temp"
        temporary.mkdir()
        with patch.dict(os.environ, {"TMPDIR": str(temporary)}):
            self.assertEqual(self.run_installer(verify=True).returncode, 1)
        self.assertEqual(list(temporary.glob("tools-verify.*")), [])


@unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
class PowerShellInstallerTests(InstallerChecks, unittest.TestCase):
    kind = "powershell"

    def test_verify_detects_stale_installer_owned_agent_copy(self):
        self.assert_ok(self.run_installer())
        agent = self.project / ".claude/agents/example-agent.md"
        agent.unlink()
        agent.write_text("current agent\n")
        self.assert_ok(self.run_installer(verify=True))
        agent.write_text("outdated agent")
        result = self.run_installer(verify=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(agent.read_text(), "outdated agent")


class CatalogTests(unittest.TestCase):
    def test_package_inventory_and_versions(self):
        catalog = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual({Path(p["source"]).name for p in catalog["plugins"]},
                         {p.name for p in (REPO / "plugins").iterdir() if p.is_dir()})
        for path in [REPO / ".claude-plugin/marketplace.json",
                     *(REPO / "plugins").glob("*/.claude-plugin/marketplace.json")]:
            for entry in json.loads(path.read_text())["plugins"]:
                with self.subTest(catalog=str(path), plugin=entry["name"]):
                    manifest = path.parent.parent / entry["source"] / ".claude-plugin/plugin.json"
                    package = json.loads(manifest.read_text())
                    self.assertEqual(entry["name"], package["name"])
                    self.assertEqual(entry["version"], package["version"])


if __name__ == "__main__":
    unittest.main()
