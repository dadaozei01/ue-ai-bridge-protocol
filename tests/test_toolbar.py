"""Test the Python registration boundary; these tests do not render Slate."""
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ROOT / "templates/ue5.4/Content/Python"
MAIN = "LevelEditor.MainMenu"
LEGACY = MAIN + ".UEAIBridgeTaskMenu"
TOOLBAR = "LevelEditor.LevelEditorToolBar.PlayToolBar"
BUTTON = ("UEAIBridge", "RunTaskScriptToolbar")


class Entry:
    def __init__(self):
        self.props = {}

    def set_editor_property(self, name, value):
        self.props[name] = value

    def set_label(self, value):
        self.label = value

    def set_tool_tip(self, value):
        self.tooltip = value

    def set_icon(self, *values):
        self.icon = values

    def set_string_command(self, *values):
        self.command = values


class Menu:
    def __init__(self, registry, name):
        self.registry = registry
        self.name = name
        self.entries = {}

    def add_sub_menu(self, owner, section, name, label, tooltip):
        entry = Entry()
        entry.props["name"] = name
        self.add_menu_entry(section, entry)
        child = Menu(self.registry, self.name + "." + name)
        self.registry.menus[child.name] = child
        return child

    def add_section(self, *args):
        pass

    def add_menu_entry(self, section, entry):
        self.entries[(section, entry.props["name"])] = entry


class Registry:
    def __init__(self):
        self.menus = {name: Menu(self, name) for name in (MAIN, TOOLBAR)}

    def find_menu(self, name):
        return self.menus.get(name)

    def is_menu_registered(self, name):
        return name in self.menus

    def remove_entry(self, menu, section, name):
        if menu in self.menus:
            self.menus[menu].entries.pop((section, name), None)

    def remove_menu(self, name):
        self.menus.pop(name, None)

    def refresh_all_widgets(self):
        pass


class ToolbarTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        self.registry = Registry()
        self.callbacks = {}
        self.messages = []
        self.previous_modules = {
            name: sys.modules.get(name) for name in ("unreal", "ue_ai_bridge_runner")
        }
        fake = types.ModuleType("unreal")
        fake.Paths = types.SimpleNamespace(
            project_saved_dir=lambda: str(self.project / "Saved"),
            project_dir=lambda: str(self.project),
            convert_relative_path_to_full=lambda path: path,
        )
        fake.SystemLibrary = types.SimpleNamespace(get_engine_version=lambda: "5.4-test")
        fake.ToolMenus = types.SimpleNamespace(get=lambda: self.registry)
        fake.ToolMenuEntry = Entry
        fake.MultiBlockType = types.SimpleNamespace(MENU_ENTRY="menu", TOOL_BAR_BUTTON="toolbar")
        fake.ToolMenuStringCommandType = types.SimpleNamespace(PYTHON="python")
        fake.log = fake.log_warning = fake.log_error = self.messages.append
        fake.register_slate_post_tick_callback = self.register_callback
        fake.unregister_slate_post_tick_callback = lambda handle: self.callbacks.pop(handle, None)
        sys.modules["unreal"] = fake
        self.bridge = self.load_module("toolbar_under_test", "ue_ai_bridge_init.py")

    def register_callback(self, callback):
        handle = len(self.callbacks) + 1
        self.callbacks[handle] = callback
        return handle

    def load_module(self, name, filename):
        spec = importlib.util.spec_from_file_location(name, PYTHON_DIR / filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def tearDown(self):
        for name, original in self.previous_modules.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original
        self.temp.cleanup()

    def seed_legacy_menu(self):
        self.registry.menus[MAIN].add_sub_menu("", "", "UEAIBridgeTaskMenu", "old", "")

    def test_cold_start_registers_only_toolbar_with_large_and_small_play_icons(self):
        self.bridge._register_menu(0)
        self.assertIn(BUTTON, self.registry.menus[TOOLBAR].entries)
        entry = self.registry.menus[TOOLBAR].entries[BUTTON]
        self.assertEqual(entry.label, "\u25b6 运行任务脚本")
        self.assertEqual(entry.icon, ("EditorStyle", "PlayWorld.PlayInViewport", "Icons.Play"))
        self.assertNotIn(LEGACY, self.registry.menus)
        self.assertEqual(self.callbacks, {})

    def test_upgrade_removes_only_legacy_bridge_menu(self):
        self.seed_legacy_menu()
        unrelated = Entry()
        unrelated.props["name"] = "UnrelatedMenu"
        self.registry.menus[MAIN].add_menu_entry("", unrelated)
        self.bridge._register_menu(0)
        self.assertNotIn(LEGACY, self.registry.menus)
        self.assertNotIn(("", "UEAIBridgeTaskMenu"), self.registry.menus[MAIN].entries)
        self.assertIs(self.registry.menus[MAIN].entries[("", "UnrelatedMenu")], unrelated)

    def test_repeated_refresh_keeps_one_button_and_preserves_unrelated_toolbar_entry(self):
        self.bridge._register_menu(0)
        unrelated = Entry()
        unrelated.props["name"] = "UnrelatedAction"
        toolbar = self.registry.menus[TOOLBAR]
        toolbar.add_menu_entry("Other", unrelated)
        self.bridge._done = False
        self.bridge._register_menu(0)
        self.assertEqual(set(toolbar.entries), {BUTTON, ("Other", "UnrelatedAction")})
        self.assertIs(toolbar.entries[("Other", "UnrelatedAction")], unrelated)

    def test_missing_toolbar_preserves_legacy_menu_and_recovers_on_later_tick(self):
        self.seed_legacy_menu()
        toolbar = self.registry.menus.pop(TOOLBAR)
        self.bridge._register_menu(0)
        self.assertFalse(self.bridge._done)
        self.assertIn(LEGACY, self.registry.menus)
        self.registry.menus[TOOLBAR] = toolbar
        self.bridge._register_menu(0)
        self.assertTrue(self.bridge._done)
        self.assertIsNone(self.bridge._last_error)
        self.assertNotIn(LEGACY, self.registry.menus)
        self.assertIn(BUTTON, toolbar.entries)

    def test_missing_toolbar_stops_retrying_at_limit(self):
        self.seed_legacy_menu()
        del self.registry.menus[TOOLBAR]
        for _ in range(self.bridge.MAX_ATTEMPTS):
            self.bridge._register_menu(0)
        self.assertEqual(self.bridge._tries, self.bridge.MAX_ATTEMPTS)
        self.assertTrue(self.bridge._done)
        self.assertEqual(self.callbacks, {})
        self.assertIn(LEGACY, self.registry.menus)

    def test_missing_main_menu_timeout_records_failure(self):
        del self.registry.menus[MAIN]
        for _ in range(self.bridge.MAX_ATTEMPTS):
            self.bridge._register_menu(0)
        self.assertTrue(self.bridge._done)
        self.assertEqual(self.callbacks, {})
        self.assertIsNotNone(self.bridge._last_error)
        self.assertIn("LevelEditor.MainMenu", self.bridge._last_error)
        self.assertNotIn(BUTTON, self.registry.menus[TOOLBAR].entries)

    def test_button_command_runs_real_runner_and_writes_matching_report(self):
        task_dir = self.project / "Saved/CodexScripts"
        task_dir.mkdir(parents=True)
        task = task_dir / "run_task.py"
        task.write_text('UE_AI_BRIDGE_TASK_ID = "toolbar-test-1"\n'
                        'UE_AI_BRIDGE_RESULT = {"assets_modified": False}\n', encoding="utf-8")
        runner = self.load_module("ue_ai_bridge_runner", "ue_ai_bridge_runner.py")
        sys.modules["ue_ai_bridge_runner"] = runner
        self.bridge._register_menu(0)
        self.assertFalse((task_dir / "last_task_report.json").exists())
        self.assertIn(BUTTON, self.registry.menus[TOOLBAR].entries)
        entry = self.registry.menus[TOOLBAR].entries[BUTTON]
        exec(entry.command[2], {})
        report = json.loads((task_dir / "last_task_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "success")
        self.assertEqual(report["task_id"], "toolbar-test-1")
        self.assertFalse(report["result"]["assets_modified"])
        import hashlib
        self.assertEqual(report["task_sha256"], hashlib.sha256(task.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
