# DeepSeek Harness Prompt

Strictly follow `https://github.com/dadaozei01/ue-ai-bridge-protocol`.

First identify the exact `.uproject`, engine version and path, platform, CPU architecture, project modules, Editor Target, plugin state, and whether Unreal Editor is open. Never use a reserved version note as an execution procedure.

For verified UE 5.4:

- Project C++ belongs under `Source`, not in a plugin unless explicitly requested.
- Build the actual Editor Target; do not derive it from a module name.
- Editor assets use UE Python implementing exactly the user's request.
- Do not operate UE UI or Blueprint graph nodes by default.
- Attempt Remote Execution discovery once only.
- On discovery failure, preserve existing bridge files, atomically replace `Saved/CodexScripts/run_task.py`, and ask for one selection of `任务脚本 -> 运行任务脚本`.
- Read `Saved/CodexScripts/last_task_report.json`; success requires `"status": "success"`.

List intended files before editing and verify build output, report data, and requested asset state afterward.
