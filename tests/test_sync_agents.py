"""Regression checks for scoped agent generation without invoking any agent."""

import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts import sync_agents


class ScopedGenerationTests(unittest.TestCase):
    """Check drift and tool isolation using disposable output directories."""

    def setUp(self):
        """Copy canonical inputs and isolate all generated output."""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / "agents" / "roles"
        shutil.copytree(sync_agents.SOURCE_DIR, source)
        self.codex = self.root / ".codex" / "agents"
        self.claude = self.root / ".claude" / "agents"
        self.patch = patch.multiple(
            sync_agents, ROOT=self.root, SOURCE_DIR=source,
            SHARED_PATH=source / "_shared.md", CODEX_DIR=self.codex,
            CLAUDE_DIR=self.claude,
        )
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def sync(self, check=False, tool="codex"):
        """Run synchronization while suppressing expected diagnostic output."""
        with contextlib.redirect_stdout(io.StringIO()):
            return sync_agents.sync(check, tool)

    def test_codex_only_preserves_claude(self):
        """A Codex-only operation must not inspect or rewrite Claude outputs."""
        self.claude.mkdir(parents=True)
        sentinel = self.claude / "unrelated.md"
        sentinel.write_bytes(b"existing Claude configuration\r\n")
        self.assertEqual(self.sync(), 0)
        self.assertEqual(self.sync(check=True), 0)
        self.assertEqual(len(list(self.codex.glob("*.toml"))), 5)
        self.assertEqual(sentinel.read_bytes(), b"existing Claude configuration\r\n")

    def test_drift_is_detected_without_repair(self):
        """Check mode reports changes and leaves the changed file intact."""
        self.sync()
        target = self.codex / "tester.toml"
        target.write_text("invalid TOML drift", encoding="utf-8")
        self.assertEqual(self.sync(check=True), 1)
        self.assertEqual(target.read_text(encoding="utf-8"), "invalid TOML drift")

    def test_claude_only_preserves_codex(self):
        """A Claude-only operation leaves all existing Codex output untouched."""
        self.codex.mkdir(parents=True)
        sentinel = self.codex / "unrelated.toml"
        sentinel.write_bytes(b"# existing Codex configuration\r\n")
        self.assertEqual(self.sync(tool="claude"), 0)
        self.assertEqual(self.sync(check=True, tool="claude"), 0)
        self.assertEqual(len(list(self.claude.glob("*.md"))), 5)
        self.assertEqual(sentinel.read_bytes(), b"# existing Codex configuration\r\n")

    def test_claude_no_edit_role_restrictions(self):
        """Only review/test roles deny editors; every role denies chaining."""
        self.sync(tool="claude")
        for name in sync_agents.ROLE_NAMES:
            content = (self.claude / f"{name}.md").read_text(encoding="utf-8")
            header = content.split("---", 2)[1]
            expected = "disallowedTools: Agent"
            if name in ("tester", "code-reviewer"):
                expected += ", Write, Edit, NotebookEdit"
            self.assertIn(expected + "\n", header)

    def test_claude_weakened_restrictions_are_rejected(self):
        """Validation rejects missing editor restrictions for Tester."""
        shared = sync_agents.SHARED_PATH.read_text(encoding="utf-8")
        role = sync_agents.parse_source(sync_agents.SOURCE_DIR / "tester.md", shared)
        content = sync_agents.render_claude(role).replace(
            "disallowedTools: Agent, Write, Edit, NotebookEdit", "disallowedTools: Agent"
        )
        with self.assertRaisesRegex(ValueError, "restrictions mismatch"):
            sync_agents.validate_claude(content, role)

    def test_missing_output_is_detected(self):
        """A missing role is drift, not a successful validation."""
        self.assertEqual(self.sync(check=True), 1)
        self.assertFalse(self.codex.exists())

    def test_weakened_tester_boundary_is_rejected(self):
        """The old production-code-only guard no longer satisfies the role."""
        source = sync_agents.SOURCE_DIR / "tester.md"
        source.write_text(source.read_text(encoding="utf-8").replace(
            sync_agents.ROLE_BOUNDARIES["tester"], "Do not change production code,"
        ), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing role boundary"):
            self.sync()

    def test_unexpected_codex_role_is_rejected(self):
        """Do not silently overwrite or delete an unknown agent definition."""
        self.codex.mkdir(parents=True)
        (self.codex / "extra.toml").write_text("# preserve", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unexpected generated agent"):
            self.sync()


if __name__ == "__main__":
    unittest.main()
