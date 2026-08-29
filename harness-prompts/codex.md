# Codex Prompt

Use my UE AI Bridge Protocol.

Do not start by controlling the Unreal Editor UI. Do not default to plugins. Do not auto-click Blueprint graph nodes.

For C++ features:

- Edit the project `Source` folder directly.
- If the project is Blueprint-only, add the standard project module files and `.uproject` `Modules` entry.
- Compile the Editor target.
- On macOS Apple Silicon, compile with `-architecture=arm64` and `-NoHotReload`.
- If adding or changing `UCLASS`, `UPROPERTY`, `UFUNCTION`, `USTRUCT`, or `UENUM`, tell me to restart UE after compile.

For materials and asset creation:

- Use standard UE Python and old/standard Material APIs.
- Prefer Remote Execution only if it is discoverable.
- If Remote Execution is unreliable, update `Saved/CodexScripts/run_task.py` and ask me to click the UE menu item.
- If the bridge is not installed, install `Content/Python/init_unreal.py` and `Saved/CodexScripts/run_task.py`, then ask me to restart UE once.

Required UE plugins for Python asset automation:

- Python Editor Script Plugin
- Editor Scripting Utilities

Do not promise full Blueprint EventGraph K2 node generation through UE Python unless verified in this exact engine version.
