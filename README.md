# UE AI Bridge Protocol

Portable workflow rules and templates for using AI coding tools with Unreal Engine projects.

Core rule:

```text
Do not start by controlling the Unreal Editor UI.
C++ features go through project Source + Editor build.
Materials and assets go through Unreal Python inside the editor.
Remote Execution is optional acceleration, not a required dependency.
Plugins are not the default solution.
```

This repository is meant to be handed to Codex, DeepSeek Harness, WorkBuddy, Doubao, ZCode, or similar tools before they work on a UE project.

## Recommended Workflow

1. Identify the project `.uproject`, engine path, platform, and CPU architecture.
2. For C++ features, edit the project `Source` folder and compile the Editor target.
3. For materials, material instances, folders, imports, and asset batch edits, use UE Python.
4. If UE Python Remote Execution works, use it.
5. If Remote Execution is unreliable, use the in-editor Python button bridge.
6. For one-shot fully automatic asset work, use `StartupScripts` and remove the startup hook afterwards.
7. Avoid automatic UE UI clicking unless the user explicitly asks for it.

## Current Version Coverage

- `protocols/UE5.4.md`: verified workflow for UE 5.4 on macOS Apple Silicon and Windows.
- `protocols/UE5.5.md`: compatibility notes, pending direct verification.
- `protocols/UE5.6.md`: compatibility notes, pending direct verification.
- `protocols/UE5.8-MCP.md`: placeholder for future MCP-based workflow.

## Bridge Concept

The button bridge is not Remote Execution.

- Remote Execution: an external Python process discovers and connects to UE through Python Remote Execution. In UE 5.4 this uses UDP multicast discovery and can be unreliable in sandboxed environments.
- Button bridge: UE loads `Content/Python/init_unreal.py` at startup, registers a menu item, and the user clicks the item to run `Saved/CodexScripts/run_task.py` inside UE.

The bridge costs one UE restart to install. After that, AI tools update `run_task.py`, and the user clicks the menu item to execute immediately.

## Required UE Plugins

Enable these for Python asset automation:

- Python Editor Script Plugin
- Editor Scripting Utilities

## Repository Layout

```text
protocols/                 Version-specific rules
templates/ue5.4/            Button bridge template files
scripts/mac/                macOS helper scripts
scripts/windows/            Windows helper scripts
examples/materials/         UE Python material examples
examples/cpp/               C++ feature examples
harness-prompts/            Prompts for different AI tools
```
