# WorkBuddy Prompt

Follow my UE AI Bridge Protocol for UE 5.4 automation.

For gameplay systems, write project C++ under `Source` and compile the Editor target. Avoid plugins unless explicitly requested.

For materials, folders, asset creation, imports, and batch edits, use UE Python. If Remote Execution is not discoverable, use the installed menu bridge: update `Saved/CodexScripts/run_task.py`, then ask me to click `任务脚本 -> ▶ 运行任务脚本`.

Do not automate UE UI clicks as the default approach.
Do not promise direct Blueprint EventGraph K2 node generation through Python without verifying the API.
