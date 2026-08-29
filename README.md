# UE AI Bridge Protocol

A file-first workflow for AI coding tools working with Unreal Engine projects.

The protocol defines how a task reaches Unreal Editor and how its result is verified. It does not prescribe the content of a material, Blueprint, gameplay system, or other user task.

## Core Rule

```text
Inspect the exact project and engine version first.
C++ features go through project Source + an Editor Target build.
Editor assets go through Unreal Python running inside the editor.
Remote Execution is optional, never the only execution path.
Project plugins are not the default home for project-specific features.
Do not control the Unreal Editor UI unless the user explicitly requests it.
```

## Verified Coverage

- `protocols/UE5.4.md`: verified against a real UE 5.4 macOS Apple Silicon project, engine source, startup logs, menu registration, Python task execution, and project C++ compilation.
- `protocols/UE5.5.md`: reserved; not an execution procedure.
- `protocols/UE5.6.md`: reserved; not an execution procedure.
- `protocols/UE5.8-MCP.md`: reserved; not an execution procedure.

Never treat an unverified version note as proof that a connection or API works.

## UE 5.4 Execution Paths

1. In-editor button bridge: the repeatable fallback for Python asset tasks.
2. Python Remote Execution: use only when the current editor instance is immediately discoverable.
3. Unreal command-line Python: use for a separate offline or unattended editor process when appropriate.
4. Project C++ build: use for runtime logic, reflected APIs, Blueprint-callable functions, and Sequencer integration.

The button bridge is not a network connection. Unreal loads project Python at startup, registers a menu command, and executes the task file inside the editor when the menu command is selected.

## Required UE Plugins

Enable these per project for UE Python asset automation, then restart Unreal Editor:

- Python Editor Script Plugin
- Editor Scripting Utilities

## Install The UE 5.4 Bridge

macOS:

```bash
./scripts/mac/install_bridge.sh "/absolute/path/to/Project"
```

Windows PowerShell:

```powershell
.\scripts\windows\install_bridge.ps1 -ProjectDir "C:\absolute\path\to\Project"
```

The installer preserves an existing `Content/Python/init_unreal.py` and an existing `Saved/CodexScripts/run_task.py`. Restart Unreal Editor once after initial installation.

## Task Contract

The AI tool writes only the current task to:

```text
<PROJECT>/Saved/CodexScripts/run_task.py
```

For a complete write, write a temporary file first and atomically replace `run_task.py`. After the user selects `任务脚本 -> 运行任务脚本`, the bridge writes:

```text
<PROJECT>/Saved/CodexScripts/last_task_report.json
```

The report contains `running`, `success`, or `failed`, timestamps, engine version, task ID, script SHA-256, optional task result data, and a traceback on failure. Each task should set a unique `UE_AI_BRIDGE_TASK_ID`; the AI tool must match that ID or the script hash before accepting a report as current. A task can expose structured result data by assigning a JSON-compatible value to `UE_AI_BRIDGE_RESULT`.

## Universal Harness Prompt

Use [harness-prompts/universal.md](harness-prompts/universal.md) as the first message to Codex, DeepSeek Harness, WorkBuddy, Doubao, ZCode, or a similar tool.

## Repository Layout

```text
protocols/                 Version-specific verified rules or reserved notes
templates/ue5.4/           UE 5.4 button bridge files
scripts/mac/               macOS installers and build helpers
scripts/windows/           Windows installers and build helpers
harness-prompts/           Reusable instructions for AI tools
tests/                     Repository contract checks
```
