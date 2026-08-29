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

mkdir -p "$PROJECT_DIR/Content/Python"
mkdir -p "$PROJECT_DIR/Saved/CodexScripts"

cp "$REPO_ROOT/templates/ue5.4/Content/Python/init_unreal.py" "$PROJECT_DIR/Content/Python/init_unreal.py"
cp "$REPO_ROOT/templates/ue5.4/Saved/CodexScripts/run_task.py" "$PROJECT_DIR/Saved/CodexScripts/run_task.py"

echo "Installed UE AI button bridge:"
echo "  $PROJECT_DIR/Content/Python/init_unreal.py"
echo "  $PROJECT_DIR/Saved/CodexScripts/run_task.py"
echo
echo "Restart Unreal Editor once. Then use: 任务脚本 -> ▶ 运行任务脚本"
