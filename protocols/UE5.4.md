# UE 5.4 File-Level AI Automation Protocol

Use this protocol when an AI coding tool works on a UE 5.4 project.

## Before Editing

Confirm:

- Project path: `<PROJECT>/<Name>.uproject`
- Engine path:
  - macOS default: `/Users/Shared/Epic Games/UE_5.4`
  - Windows default: `C:\Program Files\Epic Games\UE_5.4`
- Platform and architecture:
  - macOS Apple Silicon: compile with `-architecture=arm64`
  - Windows: compile with `Win64`

macOS editor logs are usually under:

```text
~/Library/Logs/Unreal Engine/<ProjectName>Editor/
```

They are often not under the project `Saved/Logs` folder.

## Do Not Default To

- Do not control the UE UI as the first approach.
- Do not auto-click Blueprint graph nodes.
- Do not create a plugin unless the user explicitly asks.
- Do not assume UE Python can generate full Blueprint EventGraph K2 node logic.
- Do not rely on Remote Execution as the only path.

## C++ Features

Use project C++, not a plugin, unless the user explicitly asks for a plugin.

Write code under:

```text
<PROJECT>/Source/<Module>/Public/
<PROJECT>/Source/<Module>/Private/
```

Only add `.uproject` `Modules` when converting a Blueprint-only project or adding a new module.

macOS Apple Silicon compile command:

```bash
<ENGINE>/Engine/Build/BatchFiles/Mac/Build.sh <Module>Editor Mac Development \
  -project="<PROJECT>/<Name>.uproject" \
  -architecture=arm64 \
  -NoHotReload
```

Windows compile command:

```bat
"<ENGINE>\Engine\Build\BatchFiles\Build.bat" <Module>Editor Win64 Development ^
  -project="<PROJECT>\<Name>.uproject" ^
  -NoHotReload
```

When adding or changing `UCLASS`, `UFUNCTION`, `UPROPERTY`, `USTRUCT`, or `UENUM`, ask the user to restart UE after a successful compile. Live Coding can leave stale reflection data.

For `.cpp` implementation-only changes, Live Coding may be attempted, but if behavior is stale or compile fails, close UE and compile normally.

## Materials And Assets

Use standard UE Python asset APIs:

```python
tools = unreal.AssetToolsHelpers.get_asset_tools()
mat = tools.create_asset(name, folder, unreal.Material, unreal.MaterialFactoryNew())
```

Use old/standard material editing APIs:

- `unreal.MaterialFactoryNew`
- `unreal.MaterialEditingLibrary.create_material_expression`
- `unreal.MaterialEditingLibrary.connect_material_expressions`
- `unreal.MaterialEditingLibrary.connect_material_property`
- `unreal.MaterialEditingLibrary.layout_material_expressions`
- `unreal.MaterialEditingLibrary.recompile_material`
- `unreal.EditorAssetLibrary.save_loaded_asset`

Use `set_editor_property` for expression properties:

```python
expr.set_editor_property("parameter_name", "BaseColor")
```

Do not use direct assignment for properties that may not be exposed as Python attributes.

Material shading rule:

- Pure self-lit VFX: `MSM_UNLIT` + Emissive Color.
- Surface that keeps its own color and still emits light: `MSM_DEFAULT_LIT` + Base Color + Emissive Color.

## Execution Priority For Python Tasks

Use this order:

1. Remote Execution if the current UE instance is discoverable.
2. In-editor button bridge: update `Saved/CodexScripts/run_task.py`, then user clicks the menu item.
3. StartupScripts: install a one-shot startup script, user restarts UE once, script removes or reports the hook.
4. Offline command-line Python task, when permissions allow it.

UE 5.4 Python Remote Execution uses multicast discovery. It may be enabled in UE and still not be discoverable from a sandboxed external tool.

## Button Bridge

The bridge is optional but recommended for frequent material and asset work.

Files:

```text
<PROJECT>/Content/Python/init_unreal.py
<PROJECT>/Saved/CodexScripts/run_task.py
```

`init_unreal.py` registers a menu item. `run_task.py` is the task body AI tools rewrite.

The bridge requires one restart after installation. Later task execution does not require a restart.

## Verification

After every task:

- Check compile output for C++ tasks.
- Check UE logs for Python tasks.
- Confirm expected `.uasset` files exist on disk.
- Tell the user whether a UE restart is required.
