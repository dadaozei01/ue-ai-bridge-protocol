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

- Windows UE **5.4.4**: the current toolbar-only Python bridge was checked against installed engine source, displayed in a real editor, refreshed without restarting, and executed by a user clicking the white play triangle. The resulting task ID and script SHA-256 matched. See [the button standard / 按钮使用标准](docs/toolbar-button-ue5.4.md).
- macOS Apple Silicon UE 5.4: the earlier menu bridge, Python execution, and project C++ compilation were verified. **The new toolbar-only UI has not been revalidated on macOS.** This update does not establish Windows project C++ build coverage.
- `protocols/UE5.5.md`: reserved; not an execution procedure.
- `protocols/UE5.6.md`: reserved; not an execution procedure.
- `protocols/UE5.8-MCP.md`: reserved; not an execution procedure.

Never treat an unverified version note as proof that a connection or API works.

## UE 5.4 Execution Paths

1. In-editor button bridge: the repeatable fallback for Python asset tasks.
2. Python Remote Execution: use only when the current editor instance is immediately discoverable.
3. Unreal command-line Python: use for a separate offline or unattended editor process when appropriate.
4. Project C++ build: use for runtime logic, reflected APIs, Blueprint-callable functions, and Sequencer integration.

The button bridge is not a network connection. Unreal loads project Python at startup and registers a **white play triangle (▶) in the top toolbar**, labeled `▶ 运行任务脚本`. It is separate from Unreal's game Play button and executes the current task inside the editor. The old `任务脚本` top-level menu is removed only after the toolbar button is ready.

Button appearance is Python-only work: do not add C++ modules, plugins, Editor Targets, or another `.uproject` just to add an icon. Use the [verified icon names and acceptance checks](docs/toolbar-button-ue5.4.md), not guessed APIs.

## Required UE Plugins

Enable these per project for UE Python asset automation, then restart Unreal Editor:

- Python Editor Script Plugin
- Editor Scripting Utilities

## Install The UE 5.4 Bridge

Windows PowerShell (current toolbar verified on UE 5.4.4):

```powershell
.\scripts\windows\install_bridge.ps1 -ProjectDir "C:\absolute\path\to\Project"
```

macOS helper (ships the same template; **new toolbar requires separate macOS validation**):

```bash
./scripts/mac/install_bridge.sh "/absolute/path/to/Project"
```

Before upgrading, back up the existing bridge, startup, and task files. The installer overwrites the two bridge modules, preserves existing startup code (appending its loader if needed), and leaves an existing `Saved/CodexScripts/run_task.py` untouched. **Inspect that task before clicking**; an old diagnostic script may still modify or delete assets. Restart Unreal Editor once after initial installation. A verified live refresh is also described in the button guide; normal task changes do not need a restart.

## Task Contract

The AI tool writes only the current task to:

```text
<PROJECT>/Saved/CodexScripts/run_task.py
```

For a complete write, write a temporary file first and atomically replace `run_task.py`. After the user clicks the toolbar ▶ once, the bridge writes:

```text
<PROJECT>/Saved/CodexScripts/last_task_report.json
```

The report contains `running`, `success`, or `failed`, timestamps, engine version, task ID, script SHA-256, optional task result data, and a traceback on failure. Each task should set a unique `UE_AI_BRIDGE_TASK_ID`; the AI tool must match that ID or the script hash before accepting a report as current. A task can expose structured result data by assigning a JSON-compatible value to `UE_AI_BRIDGE_RESULT`.

For button acceptance, match **both the new task ID and SHA-256**, plus fresh timestamps and `status: success`. Inspect the result data too: caught exceptions can leave a `success` report containing failed steps. Registration logs or a successful remote call alone do not prove that the user clicked a working visible button. Safe smoke tests only log and report; no popup or scene change is expected.

## Universal Harness Prompt

Use [harness-prompts/universal.md](harness-prompts/universal.md) as the first message to Codex, DeepSeek Harness, WorkBuddy, Doubao, ZCode, or a similar tool.

## Repository Layout

```text
protocols/                 Version-specific verified rules or reserved notes
docs/                      Verified button standard, migration, and acceptance
templates/ue5.4/           UE 5.4 button bridge files
scripts/mac/               macOS installers and build helpers
scripts/windows/           Windows installers and build helpers
harness-prompts/           Reusable instructions for AI tools
tests/                     Repository contract checks
```
