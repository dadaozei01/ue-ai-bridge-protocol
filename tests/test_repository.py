import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_ue54_menu_does_not_assign_string_owner(self):
        python_dir = ROOT / "templates/ue5.4/Content/Python"
        for path in python_dir.glob("*.py"):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertNotIn('set_editor_property("owner"', source)

    def test_reinstall_preserves_existing_task_script(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "Test Project"
            project_dir.mkdir()
            (project_dir / "TestProject.uproject").write_text("{}\n", encoding="utf-8")

            installer = ROOT / "scripts/mac/install_bridge.sh"
            subprocess.run([str(installer), str(project_dir)], check=True, capture_output=True)

            task_script = project_dir / "Saved/CodexScripts/run_task.py"
            marker = "# user task must survive reinstall\n"
            task_script.write_text(marker, encoding="utf-8")

            subprocess.run([str(installer), str(project_dir)], check=True, capture_output=True)
            self.assertEqual(task_script.read_text(encoding="utf-8"), marker)

    def test_compile_helpers_accept_editor_target_name(self):
        mac_source = (ROOT / "scripts/mac/compile_editor_arm64.sh").read_text(
            encoding="utf-8"
        )
        win_source = (ROOT / "scripts/windows/compile_editor_win64.bat").read_text(
            encoding="utf-8"
        )

        self.assertIn("EDITOR_TARGET", mac_source)
        self.assertNotIn('${MODULE}Editor', mac_source)
        self.assertIn("EDITOR_TARGET", win_source)
        self.assertNotIn("%MODULE%Editor", win_source)

    def test_bridge_has_machine_readable_task_report(self):
        runner = ROOT / "templates/ue5.4/Content/Python/ue_ai_bridge_runner.py"
        self.assertTrue(runner.is_file())
        source = runner.read_text(encoding="utf-8")
        self.assertIn("last_task_report.json", source)
        self.assertIn("os.replace", source)
        self.assertIn("task_sha256", source)

    def test_repository_does_not_ship_specific_material_examples(self):
        self.assertFalse((ROOT / "examples/materials/standard_red_material.py").exists())
        self.assertFalse((ROOT / "examples/materials/flicker_emissive_material.py").exists())

        tracked_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in list(ROOT.glob("*.md"))
            + list((ROOT / "protocols").glob("*.md"))
            + list((ROOT / "harness-prompts").glob("*.md"))
        ).lower()
        self.assertNotIn("flicker", tracked_text)
        self.assertNotIn("glow material", tracked_text)
        self.assertNotIn("red material", tracked_text)

    def test_unverified_versions_are_not_execution_procedures(self):
        for name in ("UE5.5.md", "UE5.6.md", "UE5.8-MCP.md"):
            with self.subTest(name=name):
                source = (ROOT / "protocols" / name).read_text(encoding="utf-8")
                self.assertIn("Do not use this file as an execution procedure.", source)

    def test_universal_harness_prompt_routes_to_exact_version(self):
        source = (ROOT / "harness-prompts/universal.md").read_text(encoding="utf-8")
        self.assertIn("exact installed engine version", source)
        self.assertIn("last_task_report.json", source)

        for path in (ROOT / "harness-prompts").glob("*.md"):
            with self.subTest(path=path.name):
                prompt = path.read_text(encoding="utf-8")
                self.assertIn("last_task_report.json", prompt)
                self.assertNotIn("▶", prompt)

    def test_ue54_protocol_distinguishes_target_from_module(self):
        source = (ROOT / "protocols/UE5.4.md").read_text(encoding="utf-8")
        self.assertIn("Editor Target is not necessarily the module name", source)
        self.assertIn("last_task_report.json", source)


if __name__ == "__main__":
    unittest.main()
