# UE AI Bridge Protocol

A project-scoped, direct-first workflow for AI coding tools working with Unreal Engine projects.

The protocol defines how a task reaches Unreal Editor and how its result is verified. It does not prescribe the content of a material, Blueprint, gameplay system, or other user task.

## Core Rule

```text
Inspect the exact project and engine version first.
Check the current project's button before installing anything.
Existing button: preserve it, its loader, and its current task; do not reinstall.
Confirmed missing button: install the project-local Python button after prerequisite checks.
Agent execution: prefer direct Remote Execution of a separate reviewed script.
Never overwrite run_task.py merely because direct discovery failed.
C++ features go through project Source + an Editor Target build.
Editor assets go through Unreal Python running inside the editor.
The button is the user's manual entry, not an Agent's mandatory connection method.
Project plugins are not the default home for project-specific features.
Do not control the Unreal Editor UI unless the user explicitly requests it.
```

## 给所有 Agent 的统一入口

**先检查：有按钮就保留，没有按钮才安装。执行功能优先直连，不默认走按钮。**

先读 [跨 Agent 接入说明](docs/agent-entry.md)，再读准确版本的协议。适用于有本机文件、终端和 Python 执行权限的工具；仅能浏览网页的聊天工具不能因此获得本机 UE 控制权。不同工具是否自动读取 `AGENTS.md` 不作保证。

把下面这句话连同工程路径发给 WorkBuddy、ZCode、DeepSeek Harness（DHS）、豆包、Codex 等工具：

> 请先读取 https://github.com/dadaozei01/ue-ai-bridge-protocol/blob/main/docs/agent-entry.md 。先只读检查当前工程、UE 版本和按钮；已有按钮不改，确认没有才按仓库模板安装。执行功能优先直连当前 UE，运行独立脚本，不替换按钮的 run_task.py。不要自动重启、覆盖原资产或重发结果不明的任务。

## Verified Coverage

- Windows UE **5.4.4**: the current toolbar-only Python bridge was checked against installed engine source, displayed in a real editor, refreshed without restarting, and executed by a user clicking the white play triangle. The resulting task ID and script SHA-256 matched. See [the button standard / 按钮使用标准](docs/toolbar-button-ue5.4.md).
- Windows UE **5.4.4**: direct execution of an independent script was also used to create and verify a separate material instance while preserving the button's disabled task, existing asset parameters, and protected files. This is not proof that every asset operation, Agent product, or other engine version is safe or verified.
- macOS Apple Silicon UE 5.4: the earlier menu bridge, Python execution, and project C++ compilation were verified. **The new toolbar-only UI has not been revalidated on macOS.** This update does not establish Windows project C++ build coverage.
- `protocols/UE5.5.md`: reserved; not an execution procedure.
- `protocols/UE5.6.md`: reserved; not an execution procedure.
- `protocols/UE5.8-MCP.md`: reserved; not an execution procedure.

Never treat an unverified version note as proof that a connection or API works.

## UE 5.4 Execution Paths

1. Python Remote Execution: preferred for Agents; discover the current editor, validate its exact identity, then run a separate reviewed task file. Do not route this through `ue_ai_bridge_runner.run_task()`.
2. In-editor button bridge: retain or install the user's manual entry as described below. Using it for an Agent task, replacing its task, or asking for a click is an explicitly agreed fallback, not an automatic consequence of discovery failure.
3. Unreal command-line Python: only for a separately approved offline/unattended editor process. Do not launch another editor on the live project as an automatic fallback.
4. Project C++ build: only for separately requested runtime/reflected features, using the actual Editor Target. Connection and button work do not require new C++.

The button bridge is not a network connection. Unreal loads project Python at startup and registers a **white play triangle (▶) in the top toolbar**, labeled `▶ 运行任务脚本`. It is separate from Unreal's game Play button and executes the current task inside the editor. The old `任务脚本` top-level menu is removed only after the toolbar button is ready.

Button appearance is Python-only work: do not add C++ modules, plugins, Editor Targets, or another `.uproject` just to add an icon. Use the [verified icon names and acceptance checks](docs/toolbar-button-ue5.4.md), not guessed APIs.

## Required UE Plugins

Check these per project for UE Python asset automation. If disabled, explain the required enablement and restart and obtain approval; never interrupt a running editor automatically:

- Python Editor Script Plugin
- Editor Scripting Utilities

## Install The UE 5.4 Bridge

**Do not run an installer when the current project already has its task button.** Read startup/bridge files and current registration evidence first. A toolbar/menu container existing is not proof that the specific button exists. If installation is partial or visibility is uncertain, inspect and report rather than overwriting it. See [the decision table](docs/agent-entry.md#1-先检查按钮有则保留无则安装).

For a confirmed missing button, install project-locally using the shipped template after checking permissions, existing files, and plugins. Do not install globally. Preserve any pre-existing task, including a deliberately disabled placeholder. Do not click an unreviewed preserved task or change it just to run an installation smoke test.

Windows PowerShell (current toolbar verified on UE 5.4.4):

```powershell
.\scripts\windows\install_bridge.ps1 -ProjectDir "C:\absolute\path\to\Project"
```

macOS helper (ships the same template; **new toolbar requires separate macOS validation**):

```bash
./scripts/mac/install_bridge.sh "/absolute/path/to/Project"
```

For a separately requested upgrade, back up existing bridge, startup, and task files first. The installer overwrites the two bridge modules, preserves existing startup code (appending its loader if needed), and leaves an existing `Saved/CodexScripts/run_task.py` untouched. **Inspect that task before clicking**; an old diagnostic script may still modify or delete assets. Startup loading normally takes effect the next time the user opens the editor. Do not restart it automatically; a live refresh is only for an explicitly agreed installation/repair, not a prerequisite for direct execution.

## Task Contract

### Preferred: independent direct task

Prepare a separate, uniquely named UTF-8 task in the Agent workspace, keep it immutable for the attempt, and record its task ID and SHA-256. Validate project/engine/process identity inside UE before its first mutation. Execute once through the current direct connection and verify the requested UE state. Store direct-task evidence separately; **do not read or overwrite `last_task_report.json` as if it described this direct task**. Details and failure handling are in [the direct-first guide](docs/agent-entry.md#2-agent-执行功能优先直连).

### Optional: explicitly agreed button task

Only when the user has agreed to use the button for this task, the AI tool may back up and update:

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
AGENTS.md                 Entry pointer and shared Agent safety rules
docs/                      Direct-first Agent entry and verified button standard
templates/ue5.4/           UE 5.4 button bridge files
scripts/mac/               macOS installers and build helpers
scripts/windows/           Windows installers and build helpers
harness-prompts/           Reusable instructions for AI tools
tests/                     Repository contract checks
```
