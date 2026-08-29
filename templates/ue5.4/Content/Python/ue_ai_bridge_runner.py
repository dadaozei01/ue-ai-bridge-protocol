import datetime
import hashlib
import json
import os
import runpy
import traceback

import unreal


PROJECT_DIR = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
SCRIPT_DIR = os.path.join(PROJECT_DIR, "Saved", "CodexScripts")
TASK_SCRIPT = os.path.join(SCRIPT_DIR, "run_task.py")
REPORT_PATH = os.path.join(SCRIPT_DIR, "last_task_report.json")

_running = False


def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _engine_version():
    try:
        return unreal.SystemLibrary.get_engine_version()
    except Exception:
        return "unknown"


def _task_sha256():
    try:
        digest = hashlib.sha256()
        with open(TASK_SCRIPT, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def _write_report(report):
    os.makedirs(SCRIPT_DIR, exist_ok=True)
    temporary_path = REPORT_PATH + ".tmp"
    with open(temporary_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, default=str)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary_path, REPORT_PATH)


def run_task():
    global _running

    if _running:
        unreal.log_warning("[UEAIBridge] A task is already running.")
        return False

    _running = True
    report = {
        "status": "running",
        "started_at": _utc_now(),
        "finished_at": None,
        "engine_version": _engine_version(),
        "task_script": TASK_SCRIPT,
        "task_id": None,
        "task_sha256": _task_sha256(),
        "result": None,
        "error": None,
    }

    try:
        _write_report(report)
        if not os.path.isfile(TASK_SCRIPT):
            raise FileNotFoundError("Task script does not exist: " + TASK_SCRIPT)

        namespace = runpy.run_path(TASK_SCRIPT, run_name="__main__")
        report["task_id"] = namespace.get("UE_AI_BRIDGE_TASK_ID")
        report["result"] = namespace.get("UE_AI_BRIDGE_RESULT")
        report["status"] = "success"
        unreal.log("[UEAIBridge] Task completed: " + TASK_SCRIPT)
        return True
    except Exception:
        report["status"] = "failed"
        report["error"] = traceback.format_exc()
        unreal.log_error("[UEAIBridge] Task failed:\n" + report["error"])
        return False
    finally:
        report["finished_at"] = _utc_now()
        try:
            _write_report(report)
        except Exception:
            unreal.log_error(
                "[UEAIBridge] Could not write task report:\n" + traceback.format_exc()
            )
        _running = False
