# Codex Prompt

Use the protocol at `https://github.com/dadaozei01/ue-ai-bridge-protocol`.

Inspect the `.uproject`, installed engine, platform, architecture, modules, and actual Editor Target before editing. Use only a protocol marked verified for that exact engine version.

For verified UE 5.4 work:

- Keep project-specific C++ under project `Source`; do not default to a plugin.
- Compile the actual Editor Target. On macOS Apple Silicon use `-architecture=arm64 -NoHotReload`.
- Use UE Python inside the editor for requested material and editor-asset tasks without assuming a material type or effect.
- Do not control UE UI or auto-click Blueprint nodes by default.
- Probe Remote Execution once. If discovery fails, atomically update `Saved/CodexScripts/run_task.py` and use `任务脚本 -> 运行任务脚本`.
- Read `Saved/CodexScripts/last_task_report.json` before claiming success.
- Preserve existing startup Python, task files, assets, and unrelated user changes.

Reflection changes require a successful build and Unreal Editor restart. Do not promise full Blueprint EventGraph generation through Python.
