# Universal Harness Prompt

Give the following text to any AI coding harness before it works on an Unreal project:

```text
Use the UE AI Bridge Protocol from https://github.com/dadaozei01/ue-ai-bridge-protocol.

First inspect the .uproject and select the protocol for the exact installed engine version. A reserved or unverified version file is not an execution procedure and must not be treated as proof that a connection works.

For a verified UE 5.4 project, work at file level. Use project Source plus the actual Editor Target for C++ features. Use Unreal Python inside the editor for materials and editor assets. Do not default to a plugin, Unreal UI automation, or Blueprint-node clicking. Try Remote Execution only once; if discovery fails, use the installed button bridge. Preserve existing startup and task files. Give each task a unique UE_AI_BRIDGE_TASK_ID, write it atomically to Saved/CodexScripts/run_task.py, have it executed once in Unreal, then read Saved/CodexScripts/last_task_report.json and match the task ID before claiming success.

Check Python Editor Script Plugin and Editor Scripting Utilities. If either is disabled, name the missing plugin and explain that enabling it requires an Unreal Editor restart. Do not silently rewrite the .uproject without authorization.

Do not assume a material type or effect. Implement exactly the behavior requested by the user. Do not use instructions for UE 5.5, 5.6, 5.8, or another version until that version is marked verified in the repository.
```
