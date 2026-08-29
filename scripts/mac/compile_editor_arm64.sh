#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 /path/to/UE_5.4 /path/to/Project.uproject ModuleName"
  exit 1
fi

ENGINE_DIR="$1"
UPROJECT="$2"
MODULE="$3"

"$ENGINE_DIR/Engine/Build/BatchFiles/Mac/Build.sh" "${MODULE}Editor" Mac Development \
  -project="$UPROJECT" \
  -architecture=arm64 \
  -NoHotReload
