# UE 5.4 File-Level AI Automation Protocol

Status: verified on macOS Apple Silicon with an installed Epic Games UE 5.4 build and a real Blueprint + project C++ hybrid project.

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

When adding or changing `UCLASS`, `UFUNCTION`, `UPROPERTY`, `USTRUCT`, or `UENUM`, compile successfully and restart Unreal Editor. Live Coding can leave stale reflection data. For `.cpp` implementation-only changes, Live Coding may be attempted, but fall back to a normal Editor Target build if results are stale.

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

## Python Execution Order

1. If Remote Execution is already known to work in the current environment, use it.
2. Otherwise perform one short discovery attempt; if no node is found, stop probing and use the button bridge.
3. For the button bridge, atomically update `Saved/CodexScripts/run_task.py`, ask the user to select the menu command once, then read `last_task_report.json`.
4. Use command-line Python only when a separate editor process is appropriate and project plugins are already enabled.

UE 5.4 Remote Execution uses UDP multicast discovery. The editor setting can be enabled while a sandboxed external tool still cannot discover it. This is an environment limitation, not proof that the user configured UE incorrectly.

## Button Bridge

Installed files:

```text
<PROJECT>/Content/Python/init_unreal.py
<PROJECT>/Content/Python/ue_ai_bridge_init.py
<PROJECT>/Content/Python/ue_ai_bridge_runner.py
<PROJECT>/Saved/CodexScripts/run_task.py
```

`init_unreal.py` loads the bridge module. The bridge waits for `LevelEditor.MainMenu`, registers `任务脚本 -> 运行任务脚本`, and then unregisters its post-tick callback.

UE 5.4 does not accept a normal Python string for `ToolMenuEntry.owner`. The verified bridge therefore does not assign that property. Do not reintroduce a string owner based on APIs from another engine version.

The runner prevents overlapping execution and atomically writes:

```text
<PROJECT>/Saved/CodexScripts/last_task_report.json
```

The bridge requires one restart after initial installation. Later task execution does not require a restart.

## Task Result Contract

A task succeeds only when `last_task_report.json` has `"status": "success"`. The existence of a `.uasset` file alone does not prove that its graph, properties, or connections are correct.

Tasks may publish structured details:

```python
UE_AI_BRIDGE_TASK_ID = "a-unique-id-for-this-task"
UE_AI_BRIDGE_RESULT = {
    "message": "Task-specific summary",
    "assets": ["/Game/Path/AssetName"],
}
```

Before accepting a previous `success`, compare the report's `task_id` or `task_sha256` with the current task. A successful report for an older task is not proof that the current task ran.

## Verification

After every task:

- C++: require a successful Editor Target build and state whether a restart is required.
- Python: read `last_task_report.json` and inspect the UE log on failure.
- Assets: verify expected package paths and the requested graph or property state inside UE.
- Never claim success from file writes alone.

macOS UE editor logs are typically under:

```text
~/Library/Logs/Unreal Engine/<ProjectName>Editor/
```
