#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 /path/to/YourProject"
  echo "Example: $0 \"/Users/me/Unreal Projects/MyProject\""
  exit 1
fi

PROJECT_DIR="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Project directory does not exist: $PROJECT_DIR" >&2
  exit 1
fi

shopt -s nullglob
UPROJECTS=("$PROJECT_DIR"/*.uproject)
shopt -u nullglob
if [[ ${#UPROJECTS[@]} -eq 0 ]]; then
  echo "No .uproject file found directly under: $PROJECT_DIR" >&2
  exit 1
fi

mkdir -p "$PROJECT_DIR/Content/Python"
mkdir -p "$PROJECT_DIR/Saved/CodexScripts"

PYTHON_DIR="$PROJECT_DIR/Content/Python"
TASK_DIR="$PROJECT_DIR/Saved/CodexScripts"
INIT_FILE="$PYTHON_DIR/init_unreal.py"

cp "$REPO_ROOT/templates/ue5.4/Content/Python/ue_ai_bridge_init.py" "$PYTHON_DIR/ue_ai_bridge_init.py"
cp "$REPO_ROOT/templates/ue5.4/Content/Python/ue_ai_bridge_runner.py" "$PYTHON_DIR/ue_ai_bridge_runner.py"

if [[ ! -f "$INIT_FILE" ]]; then
  cp "$REPO_ROOT/templates/ue5.4/Content/Python/init_unreal.py" "$INIT_FILE"
elif ! grep -q "UE_AI_BRIDGE_LOADER_START" "$INIT_FILE"; then
  {
    echo
    echo "# UE_AI_BRIDGE_LOADER_START"
    echo "import ue_ai_bridge_init  # noqa: F401"
    echo "# UE_AI_BRIDGE_LOADER_END"
  } >> "$INIT_FILE"
fi

if [[ ! -f "$TASK_DIR/run_task.py" ]]; then
  cp "$REPO_ROOT/templates/ue5.4/Saved/CodexScripts/run_task.py" "$TASK_DIR/run_task.py"
else
  echo "Preserved existing task script: $TASK_DIR/run_task.py"
fi

echo "Installed UE AI button bridge:"
echo "  $INIT_FILE"
echo "  $PYTHON_DIR/ue_ai_bridge_init.py"
echo "  $PYTHON_DIR/ue_ai_bridge_runner.py"
echo "  $TASK_DIR/run_task.py"
echo
echo "Restart Unreal Editor once. Then use: 任务脚本 -> 运行任务脚本"
