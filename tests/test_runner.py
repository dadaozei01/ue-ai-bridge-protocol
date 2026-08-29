import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "templates/ue5.4/Content/Python/ue_ai_bridge_runner.py"


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.temp_dir.name)
        self.task_dir = self.project_dir / "Saved/CodexScripts"
        self.task_dir.mkdir(parents=True)

        fake_unreal = types.ModuleType("unreal")
        fake_unreal.Paths = types.SimpleNamespace(
            project_dir=lambda: str(self.project_dir) + "/",
            convert_relative_path_to_full=lambda path: path,
        )
        fake_unreal.SystemLibrary = types.SimpleNamespace(
            get_engine_version=lambda: "5.4-test"
        )
        fake_unreal.log = lambda _message: None
        fake_unreal.log_warning = lambda _message: None
        fake_unreal.log_error = lambda _message: None
        sys.modules["unreal"] = fake_unreal

        spec = importlib.util.spec_from_file_location("ue_ai_bridge_runner_test", RUNNER_PATH)
        self.runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.runner)

    def tearDown(self):
        sys.modules.pop("unreal", None)
        self.temp_dir.cleanup()

    def read_report(self):
        return json.loads((self.task_dir / "last_task_report.json").read_text())

    def test_success_report_contains_task_result(self):
        (self.task_dir / "run_task.py").write_text(
            'UE_AI_BRIDGE_TASK_ID = "task-123"\n'
            'UE_AI_BRIDGE_RESULT = {"value": 42}\n',
            encoding="utf-8",
        )

        self.assertTrue(self.runner.run_task())
        report = self.read_report()
        self.assertEqual(report["status"], "success")
        self.assertEqual(report["result"], {"value": 42})
        self.assertEqual(report["engine_version"], "5.4-test")
        self.assertEqual(report["task_id"], "task-123")
        self.assertEqual(len(report["task_sha256"]), 64)

    def test_failure_report_contains_traceback(self):
        (self.task_dir / "run_task.py").write_text(
            'raise RuntimeError("expected failure")\n', encoding="utf-8"
        )

        self.assertFalse(self.runner.run_task())
        report = self.read_report()
        self.assertEqual(report["status"], "failed")
        self.assertIn("expected failure", report["error"])
