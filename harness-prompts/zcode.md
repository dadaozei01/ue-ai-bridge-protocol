# ZCode Prompt

Use `https://github.com/dadaozei01/ue-ai-bridge-protocol`. Detect the exact Unreal Engine version and use only a protocol marked verified for that version.

For verified UE 5.4, use project `Source` and the actual Editor Target for C++, and UE Python inside the editor for the user's requested editor-asset task. Do not default to plugins, UI control, Blueprint-node clicking, or a material type.

Probe Remote Execution once. If discovery fails, preserve the bridge, atomically update `Saved/CodexScripts/run_task.py`, use `任务脚本 -> 运行任务脚本`, and verify `Saved/CodexScripts/last_task_report.json` before claiming success.
