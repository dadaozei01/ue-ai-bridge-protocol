# UE 5.4 File-Level AI Automation Protocol

Start with [the cross-Agent entry rules](../docs/agent-entry.md): check the current project's button; preserve it if present, install the project-local template only if confirmed missing. Agent tasks prefer direct execution of independent scripts. A button is not a mandatory execution route.

Verification scope:

- Windows UE 5.4.4: the current toolbar-only Python bridge, live refresh, visible white play icon, legacy-menu removal, and user-click task/report verification were tested on 2026-08-31.
- macOS Apple Silicon UE 5.4: the earlier menu bridge and a real Blueprint + project C++ hybrid project were verified. The current toolbar-only UI has not been revalidated on macOS.
- Windows C++ compilation is not newly verified by a successful Python button test.

Use this protocol only after confirming that the project's `EngineAssociation` is `5.4`.

## Before Editing

Confirm and report:

- Absolute `.uproject` path.
- Absolute UE 5.4 engine path.
- Platform and CPU architecture.
- Project module names from `.uproject` and `Source/*/*.Build.cs`.
- Editor Target name from `Source/*.Target.cs`.
- Whether Python Editor Script Plugin and Editor Scripting Utilities are enabled.
- Whether Unreal Editor is currently open.
- Whether this project's task button already exists, is missing, or has an uncertain/partial installation. Preserve an existing button and task, including disabled placeholders; do not reinstall or refresh just to establish a direct connection.

For editor-asset-only work, missing project modules or an Editor Target do not require creating them. Inspect module/target details only where relevant; never repair or restore intentionally isolated startup files as a connection prerequisite.

If either required Python plugin is disabled, tell the user exactly which plugin is missing. Enable it through the project Plugin Browser, or edit the `.uproject` only with the user's authorization and a recoverable backup. A plugin-state change requires an Unreal Editor restart.

Editor Target is not necessarily the module name. Build the target declared by the `TargetRules` class whose `Type` is `TargetType.Editor`; do not construct a target name by blindly appending `Editor` to a module name.

Typical engine paths:

```text
macOS:   /Users/Shared/Epic Games/UE_5.4
Windows: C:\Program Files\Epic Games\UE_5.4
```

## Boundaries

- Do not control the Unreal Editor UI as the first approach.
- Do not create a plugin unless the user explicitly requests one.
- Do not auto-click Blueprint graph nodes.
- Do not promise full Blueprint EventGraph K2 node authoring through Python.
- Do not spend an extended session repeatedly probing Remote Execution.
- Do not overwrite existing project startup Python or task files during bridge installation.
- Do not replace or delete existing asset graphs unless the user explicitly requested replacement.
- Button/icon work must stay in Python. Do not add a C++ module, plugin, Editor Target, or alternate `.uproject` for button decoration.
- After repeated UI/API failures, stop and inspect the installed engine source; do not expand the architecture without user approval.

## Project C++

Use project C++ under the existing project module:

```text
<PROJECT>/Source/<Module>/Public/
<PROJECT>/Source/<Module>/Private/
```

Only add `.uproject` `Modules` and standard target/module files when converting a Blueprint-only project or intentionally adding a module. Blueprint assets continue to work in a project that contains C++.

macOS Apple Silicon:

```bash
<ENGINE>/Engine/Build/BatchFiles/Mac/Build.sh <EditorTarget> Mac Development \
  -project="<PROJECT>/<Name>.uproject" \
  -architecture=arm64 \
  -NoHotReload
```

Windows:

```bat
"<ENGINE>\Engine\Build\BatchFiles\Build.bat" <EditorTarget> Win64 Development ^
  -project="<PROJECT>\<Name>.uproject" ^
  -NoHotReload
```

When adding or changing `UCLASS`, `UFUNCTION`, `UPROPERTY`, `USTRUCT`, or `UENUM`, a successful build and editor restart are normally required. Live Coding can leave stale reflection data. Explain and obtain the user's agreement before restarting; never close their running editor automatically. For `.cpp` implementation-only changes, Live Coding may be attempted within the approved scope, but fall back to an agreed normal Editor Target build if results are stale.

## Materials And Editor Assets

The protocol is task-neutral. Translate the user's requested asset or material behavior into standard UE Python; do not assume a particular material type or visual effect.

For traditional material graph authoring in UE 5.4, prefer the APIs available in the installed engine, including:

- `unreal.MaterialFactoryNew`
- `unreal.MaterialEditingLibrary.create_material_expression`
- `unreal.MaterialEditingLibrary.connect_material_expressions`
- `unreal.MaterialEditingLibrary.connect_material_property`
- `unreal.MaterialEditingLibrary.layout_material_expressions`
- `unreal.MaterialEditingLibrary.recompile_material`
- `unreal.EditorAssetLibrary.save_loaded_asset`

Use `set_editor_property` on expression instances when a property is not exposed as a direct Python attribute. Before changing an existing asset, load and inspect it. Rebuild or delete its graph only when replacement is explicitly requested.

The above authoring APIs are not read-only checks. In UE 5.4.4, `recompile_material` also refreshes the editor and can create a progress window through texture-streaming data updates. A previous `Window Creation Failed / User Objects: 10000` incident remains unexplained at the resource-growth level. Do not blindly rerun that script, increase system quotas, or claim direct execution fixes the underlying crash. Read the [incident boundaries](../docs/agent-entry.md#4-已知事故边界).

## Python Execution Order

1. Independently inspect the button: preserve an existing one; install only a confirmed missing project-local button after prerequisites and conflict checks. Do not silently restart or alter plugin/startup configuration.
2. Prefer Remote Execution for the Agent task. Make one short discovery attempt, uniquely match the requested project and engine, and validate identity inside UE. Never reuse an old PID/node ID or simply choose the first discovered editor.
3. Run a separate reviewed UTF-8 script once. Keep the button's `run_task.py` and `last_task_report.json` untouched. Do not call `ue_ai_bridge_runner.run_task()` for an independent direct task. Keep direct-task receipts and results separate, matching ID/hash/identity and verifying the actual UE state.
4. If direct execution is unavailable, report the reason and obtain agreement on a fallback. Do not automatically rewrite the button task. Only for an explicitly agreed button task: back up and atomically update its script, ask the user to click the white toolbar ▶ once, then verify its report. A disabled task must not be re-enabled without explicit authorization.
5. Use command-line Python only when a separate editor process is explicitly approved, appropriate, and project plugins are already enabled. It is not an automatic fallback on the user's live project.

Use the installed engine's `remote_execution.py`, with bounded discovery, identity guards, short responses, and `finally: connection.stop()` cleanup; see [the full connection procedure](../docs/agent-entry.md#2-agent-执行功能优先直连). If a mutation times out or its result is uncertain, inspect state and logs; do not replay it automatically.

UE 5.4 Remote Execution uses UDP multicast discovery. The editor setting can be enabled while a sandboxed external tool still cannot discover it. This is an environment limitation, not proof that the user configured UE incorrectly.

## Button Bridge

Installed files:

```text
<PROJECT>/Content/Python/init_unreal.py
<PROJECT>/Content/Python/ue_ai_bridge_init.py
<PROJECT>/Content/Python/ue_ai_bridge_runner.py
<PROJECT>/Saved/CodexScripts/run_task.py
```

The current standard is [the toolbar-only Python bridge](../docs/toolbar-button-ue5.4.md). `init_unreal.py` loads the bridge module. The bridge waits for the main menu and `LevelEditor.LevelEditorToolBar.PlayToolBar`, then registers `RunTaskScriptToolbar` in section `UEAIBridge` with label `▶ 运行任务脚本`. Compact toolbars may show only the icon.

Use `entry.set_icon("EditorStyle", "PlayWorld.PlayInViewport", "Icons.Play")`. These large/small brush names exist in the installed UE 5.4.4 `StarshipStyle.cpp`; `PlayWorld.Play` does not. The tested icon is white, not a promised green icon.

Only after the toolbar succeeds, remove the old `UEAIBridgeTaskMenu` entry from `LevelEditor.MainMenu` and its `LevelEditor.MainMenu.UEAIBridgeTaskMenu` submenu. Never remove the main menu itself. If the toolbar is not ready, keep the existing menu and retry for at most 120 ticks; stop and report failure at the limit. Reloading updates the same toolbar entry without duplicating it or removing unrelated entries.

UE 5.4 does not accept a normal Python string for `ToolMenuEntry.owner`. The verified bridge therefore does not assign that property. Do not reintroduce a string owner based on APIs from another engine version.

The runner prevents overlapping execution and atomically writes:

```text
<PROJECT>/Saved/CodexScripts/last_task_report.json
```

Initial startup loading normally takes effect the next time the user opens the editor. Do not restart automatically. Later task execution does not require a restart.

For an explicitly agreed installation/repair requiring live refresh, use the guide's reload procedure only after verifying the connected project, engine version, and module file path. Leave an existing working button alone. Unregister any previous pending callback before reloading. `find_menu` and `is_menu_registered` are not interchangeable: extension-only menus created by `add_sub_menu` can be found while not marked registered.

## Task Result Contract

This section describes the optional button runner, not independent direct-task reports. Direct tasks use their own ID/hash/identity/timestamps and result evidence; do not repurpose the button's report or accept a stale `running`/`success` as a new task result.

`last_task_report.json` must have `"status": "success"`, but this is necessary, not sufficient. The runner treats a normal script return as success; a script that catches an exception and stores `"ERROR"`, `"all failed"`, or a missing result can still produce an outer success. Inspect `result` and verify the requested behavior. Required failures should raise rather than be silently swallowed. The existence of a `.uasset` file alone does not prove that its graph, properties, or connections are correct.

Tasks may publish structured details:

```python
UE_AI_BRIDGE_TASK_ID = "a-unique-id-for-this-task"
UE_AI_BRIDGE_RESULT = {
    "message": "Task-specific summary",
    "assets": ["/Game/Path/AssetName"],
}
```

Before accepting a previous `success`, compare the report's `task_id` or `task_sha256` with the current task. A successful report for an older task is not proof that the current task ran.

For a new button smoke test, use a new explicit task ID and require both ID and script SHA-256 to match, as well as timestamps after the test was prepared. Do not execute the test remotely and then count that report as a user-click test. A failed task may have a null `task_id` because execution stopped before the runner collected its namespace; use the hash and traceback for diagnosis.

## Verification

After every task:

- C++: require a successful Editor Target build and state whether a restart is required.
- Direct Python: match the independent task's receipt/report and verify the requested UE state; inspect the UE log on failure or an ambiguous response. Do not substitute the button report.
- Button Python: read `last_task_report.json`, matching the task ID/hash/timestamps and expected results.
- Assets: verify expected package paths and the requested graph or property state inside UE.
- Never claim success from file writes alone.
- Button acceptance has separate checks: visible triangle, retained execution binding, and a matching report produced after the user click. No popup is expected from a log-only test.

macOS UE editor logs are typically under:

```text
~/Library/Logs/Unreal Engine/<ProjectName>Editor/
```
