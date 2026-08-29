@echo off
setlocal

if "%~3"=="" (
  echo Usage: %~nx0 "C:\Program Files\Epic Games\UE_5.4" "C:\Path\Project.uproject" EditorTargetName
  exit /b 1
)

set ENGINE_DIR=%~1
set UPROJECT=%~2
set EDITOR_TARGET=%~3

"%ENGINE_DIR%\Engine\Build\BatchFiles\Build.bat" "%EDITOR_TARGET%" Win64 Development -project="%UPROJECT%" -NoHotReload
