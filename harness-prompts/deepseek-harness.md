# DeepSeek Harness Prompt

Strictly follow my UE AI Bridge Protocol.

First identify:

- `.uproject` path
- UE engine path
- platform
- CPU architecture
- whether Python Editor Script Plugin and Editor Scripting Utilities are enabled

Rules:

- Do not operate Unreal Editor UI unless I explicitly ask.
- Do not default to plugins.
- Do not waste time trying to auto-click Blueprint graph nodes.
- Do not rely on Remote Execution as the only path.
- Do not claim UE Python can create full Blueprint EventGraph logic until verified.

C++:

- Use project `Source`, not a plugin.
- Compile Editor target.
- macOS Apple Silicon: use `-architecture=arm64 -NoHotReload`.
- Windows: use `Win64 -NoHotReload`.
- Reflection changes require UE restart.

Materials and assets:

- Use UE Python.
- Prefer standard Material APIs: `MaterialFactoryNew` and `MaterialEditingLibrary`.
- If Remote Execution fails, use the in-editor button bridge.
- The button bridge uses:
  - `Content/Python/init_unreal.py`
  - `Saved/CodexScripts/run_task.py`
- Only rewrite `run_task.py` for each task. Do not put task logic into `init_unreal.py`.

Before editing, list files to change. After editing, verify logs and generated `.uasset` files.
