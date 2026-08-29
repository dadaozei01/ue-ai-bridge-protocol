@echo off
setlocal

if "%~3"=="" (
  echo Usage: %~nx0 "C:\Program Files\Epic Games\UE_5.4" "C:\Path\Project.uproject" ModuleName
  exit /b 1
)

set ENGINE_DIR=%~1
set UPROJECT=%~2
set MODULE=%~3

"%ENGINE_DIR%\Engine\Build\BatchFiles\Build.bat" %MODULE%Editor Win64 Development -project="%UPROJECT%" -NoHotReload
