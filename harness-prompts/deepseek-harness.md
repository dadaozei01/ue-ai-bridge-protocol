# DeepSeek Harness Prompt

Use the UE AI Bridge Protocol at `https://github.com/dadaozei01/ue-ai-bridge-protocol`.

Inspect the exact `.uproject`, installed engine version/path, platform, architecture, project modules, actual Editor Target, plugin state, and whether Unreal Editor is open before editing. Select the protocol for the exact installed engine version. Reserved version notes are not execution procedures.

The toolbar-only bridge is verified on **Windows UE 5.4.4**. Historical macOS Apple Silicon UE 5.4 Python/menu and C++ checks do not validate the new toolbar on macOS, other patch versions, or Windows C++ builds. Read `protocols/UE5.4.md` and `docs/toolbar-button-ue5.4.md`; report unverified combinations instead of claiming compatibility.

- Work at file level. Use Unreal Python inside the editor for the user's requested editor-asset work; do not assume a material type or effect.
- For separately requested C++ features, use project `Source` and the actual Editor Target, not a module name. Do not default to plugins. Reflection changes require a successful build and editor restart.
- The bridge button uses Python ToolMenus only: a white **▶** in the top toolbar, with label `▶ 运行任务脚本` where visible. Its icon is `set_icon("EditorStyle", "PlayWorld.PlayInViewport", "Icons.Play")`. Reuse the shipped template; do not invent style keys.
- Never add C++ modules, plugins, Target files, or another `.uproject` just to create or beautify this button. Do not change project module declarations for the icon. Repeated API failures are a reason to inspect the installed engine source, not to expand architecture without approval.
- Remove only the bridge's legacy task menu, and only after its toolbar entry is ready. Keep unrelated menus and all runtime Python/task files. Do not add a replacement panel.
- Preserve user changes. Before installation/upgrading, back up bridge files: installers overwrite the bridge init and runner, preserve an existing task, and preserve/extend startup Python. They do not automatically back up files. Inspect a preserved task before any click.
- Check Python Editor Script Plugin and Editor Scripting Utilities. If disabled, explain the required enablement/restart; do not silently rewrite the `.uproject`.
- Probe Remote Execution discovery once. If it fails, assign a unique `UE_AI_BRIDGE_TASK_ID`, atomically update `Saved/CodexScripts/run_task.py`, and ask the user to click the white **▶** once. Do not control the UE UI or click Blueprint nodes by default.
- Read `Saved/CodexScripts/last_task_report.json`. Acceptance requires `status: success`, matching current `task_id` **and** `task_sha256`, fresh start/finish timestamps, no error, and the expected result/asset state. A caught task exception or nested `ERROR` must not be treated as success just because the runner finished.
- For a button test, use a reviewed no-asset-change task, then wait for the user's click. A report produced by direct/remote runner execution does not prove the button works. Verify visible appearance separately.
- Do not promise full Blueprint EventGraph generation through Python.
