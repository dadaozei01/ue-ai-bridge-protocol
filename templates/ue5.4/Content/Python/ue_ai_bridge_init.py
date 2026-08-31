import os
import traceback

import unreal


SUBMENU_NAME = "UEAIBridgeTaskMenu"
FULL_MENU_NAME = "LevelEditor.MainMenu." + SUBMENU_NAME
ENTRY_LABEL = "\u25b6 运行任务脚本"
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
                _last_error = "LevelEditor.MainMenu was not ready after 120 ticks."
                _debug(_last_error)
                _finish()
            return

        # Keep the existing menu available until the replacement button exists.
        if not _register_toolbar(menus):
            raise RuntimeError("Task toolbar is not ready.")

        # Remove only this bridge's old top-level menu, never the whole main menu.
        menus.remove_entry("LevelEditor.MainMenu", "", SUBMENU_NAME)
        menus.remove_menu(FULL_MENU_NAME)
        menus.refresh_all_widgets()
        _last_error = None
        _debug("Toolbar ready; legacy task menu removed.")
        _finish()
    except Exception:
        _last_error = traceback.format_exc()
        if _tries >= MAX_ATTEMPTS:
            _debug("Toolbar registration failed:\n" + _last_error)
            _finish()


def _register_toolbar(menus):
    """Add a toolbar button with the native play icon next to Play controls.

    Runs during startup registration, so the toolbar picks it up when built.
    Returns True when the entry is registered without error.
    """
    try:
        toolbar = menus.find_menu("LevelEditor.LevelEditorToolBar.PlayToolBar")
        if not toolbar:
            _debug("PlayToolBar not found; toolbar button skipped.")
            return False
        try:
            toolbar.add_section("UEAIBridge", "任务")
        except Exception:
            pass  # section already exists from a previous registration
        entry = unreal.ToolMenuEntry()
        entry.set_editor_property("name", "RunTaskScriptToolbar")
        entry.set_editor_property("type", unreal.MultiBlockType.TOOL_BAR_BUTTON)
        entry.set_label(ENTRY_LABEL)
        entry.set_tool_tip("Execute Saved/CodexScripts/run_task.py")
        entry.set_icon("EditorStyle", "PlayWorld.PlayInViewport", "Icons.Play")
        entry.set_string_command(
            unreal.ToolMenuStringCommandType.PYTHON,
            "",
            "import ue_ai_bridge_runner; ue_ai_bridge_runner.run_task()",
        )
        menus.remove_entry(
            "LevelEditor.LevelEditorToolBar.PlayToolBar",
            "UEAIBridge",
            "RunTaskScriptToolbar",
        )
        toolbar.add_menu_entry("UEAIBridge", entry)
        _debug("Toolbar button registered in PlayToolBar (section UEAIBridge).")
        return True
    except Exception:
        _debug("Toolbar registration failed:\n" + traceback.format_exc())
        return False


try:
    _callback_handle = unreal.register_slate_post_tick_callback(_register_menu)
except Exception:
    _debug("Could not register post-tick callback:\n" + traceback.format_exc())
