# WorkBuddy Prompt

Follow `https://github.com/dadaozei01/ue-ai-bridge-protocol` and select only the protocol verified for the project's exact Unreal Engine version.

For verified UE 5.4, use project `Source` plus the actual Editor Target for C++ and UE Python inside the editor for requested editor-asset work. Do not default to plugins, UI automation, Blueprint-node clicking, or a particular material type.

Try Remote Execution discovery once. If it fails, preserve the installed bridge, atomically update `Saved/CodexScripts/run_task.py`, use `任务脚本 -> 运行任务脚本`, and read `Saved/CodexScripts/last_task_report.json` before reporting success.
