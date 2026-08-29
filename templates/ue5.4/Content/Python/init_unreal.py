import os
import runpy
import traceback
import unreal

BRIDGE_OWNER = "UEAIBridge"
MENU_NAME = "UEAIBridge.TaskMenu"
ENTRY_NAME = "RunTaskScript"
MENU_LABEL = "任务脚本"
ENTRY_LABEL = "▶ 运行任务脚本"

PROJECT_DIR = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
TASK_SCRIPT = os.path.join(PROJECT_DIR, "Saved", "CodexScripts", "run_task.py")
DEBUG_LOG = os.path.join(unreal.Paths.project_saved_dir(), "CodexScripts", "bridge_debug.log")

_done = False
_tries = 0
_callback_handle = None


def _debug(message):
    try:
        os.makedirs(os.path.dirname(DEBUG_LOG), exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as handle:
            handle.write(str(message) + "\n")
    except Exception:
        pass
    unreal.log("[UEAIBridge] " + str(message))


def _run_task():
    try:
        if not os.path.exists(TASK_SCRIPT):
            unreal.log_warning("[UEAIBridge] Task script does not exist: " + TASK_SCRIPT)
            return
        runpy.run_path(TASK_SCRIPT, run_name="__main__")
    except Exception:
        unreal.log_error("[UEAIBridge] Task script failed:\n" + traceback.format_exc())


def _register_menu(_delta_seconds):
    global _done, _tries, _callback_handle

    if _done:
        return

    _tries += 1
    try:
        menus = unreal.ToolMenus.get()
        main_menu = menus.find_menu("LevelEditor.MainMenu")
        if not main_menu:
            if _tries < 120:
                return
            _debug("LevelEditor.MainMenu was not ready after 120 ticks.")
            _done = True
            return

        if not menus.is_menu_registered(MENU_NAME):
            sub_menu = main_menu.add_sub_menu(
                BRIDGE_OWNER,
                "",
                MENU_NAME,
                MENU_LABEL,
                "Run project task scripts from Saved/CodexScripts/run_task.py",
            )
        else:
            sub_menu = menus.find_menu(MENU_NAME)

        entry = unreal.ToolMenuEntry()
        entry.set_editor_property("owner", BRIDGE_OWNER)
        entry.set_editor_property("name", ENTRY_NAME)
        entry.set_editor_property("type", unreal.MultiBlockType.MENU_ENTRY)
        entry.set_label(ENTRY_LABEL)
        entry.set_string_command(
            unreal.ToolMenuStringCommandType.PYTHON,
            "",
            "import runpy; runpy.run_path(r'%s', run_name='__main__')" % TASK_SCRIPT.replace("\\", "\\\\"),
        )
        sub_menu.add_menu_entry("", entry)
        menus.refresh_all_widgets()
        _debug("Menu registered. Task script: " + TASK_SCRIPT)
        _done = True

        if _callback_handle is not None:
            unreal.unregister_slate_post_tick_callback(_callback_handle)
            _callback_handle = None
    except Exception:
        _debug("Menu registration failed:\n" + traceback.format_exc())
        _done = True


try:
    _callback_handle = unreal.register_slate_post_tick_callback(_register_menu)
except Exception:
    _debug("Could not register post tick callback:\n" + traceback.format_exc())
