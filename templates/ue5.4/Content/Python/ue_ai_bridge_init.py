import os
import traceback

import unreal


SUBMENU_NAME = "UEAIBridgeTaskMenu"
FULL_MENU_NAME = "LevelEditor.MainMenu." + SUBMENU_NAME
ENTRY_NAME = "RunTaskScript"
MENU_LABEL = "任务脚本"
ENTRY_LABEL = "运行任务脚本"
MAX_ATTEMPTS = 120

DEBUG_LOG = os.path.join(
    unreal.Paths.project_saved_dir(), "CodexScripts", "bridge_debug.log"
)

_done = False
_tries = 0
_callback_handle = None
_last_error = None


def _debug(message):
    try:
        os.makedirs(os.path.dirname(DEBUG_LOG), exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as handle:
            handle.write(str(message) + "\n")
    except Exception:
        pass
    unreal.log("[UEAIBridge] " + str(message))


def _finish():
    global _done, _callback_handle
    _done = True
    if _callback_handle is not None:
        unreal.unregister_slate_post_tick_callback(_callback_handle)
        _callback_handle = None


def _register_menu(_delta_seconds):
    global _tries, _last_error

    if _done:
        return

    _tries += 1
    try:
        menus = unreal.ToolMenus.get()
        main_menu = menus.find_menu("LevelEditor.MainMenu")
        if not main_menu:
            if _tries >= MAX_ATTEMPTS:
                _debug("LevelEditor.MainMenu was not ready after 120 ticks.")
                _finish()
            return

        if menus.is_menu_registered(FULL_MENU_NAME):
            _debug("Menu already registered: " + FULL_MENU_NAME)
            _finish()
            return

        # UE 5.4 does not accept a Python string for ToolMenuEntry.owner.
        sub_menu = main_menu.add_sub_menu(
            "",
            "",
            SUBMENU_NAME,
            MENU_LABEL,
            "Run the current project task script",
        )

        entry = unreal.ToolMenuEntry()
        entry.set_editor_property("name", ENTRY_NAME)
        entry.set_editor_property("type", unreal.MultiBlockType.MENU_ENTRY)
        entry.set_label(ENTRY_LABEL)
        entry.set_tool_tip("Execute Saved/CodexScripts/run_task.py")
        entry.set_string_command(
            unreal.ToolMenuStringCommandType.PYTHON,
            "",
            "import ue_ai_bridge_runner; ue_ai_bridge_runner.run_task()",
        )
        sub_menu.add_menu_entry("", entry)
        menus.refresh_all_widgets()
        _debug("Menu registered: " + FULL_MENU_NAME)
        _finish()
    except Exception:
        _last_error = traceback.format_exc()
        if _tries >= MAX_ATTEMPTS:
            _debug("Menu registration failed:\n" + _last_error)
            _finish()


try:
    _callback_handle = unreal.register_slate_post_tick_callback(_register_menu)
except Exception:
    _debug("Could not register post-tick callback:\n" + traceback.format_exc())
