# ZCode Prompt

Use file-level UE automation.

- C++: project `Source` + Editor build.
- Materials/assets: UE Python + standard material APIs.
- Bridge fallback: `Content/Python/init_unreal.py` registers a menu; task body lives in `Saved/CodexScripts/run_task.py`.
- Do not use plugins by default.
- Do not control UE UI by default.
- Do not rely on Remote Execution if multicast discovery fails.
- Do not promise full Blueprint graph node authoring through UE Python unless verified.
