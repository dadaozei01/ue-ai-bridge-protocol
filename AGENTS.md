# UE AI Bridge: Agent entry

Read `docs/agent-entry.md` and the protocol for the exact installed UE version before acting on a user's Unreal project. This repository contains shared instructions and templates, not authorization to mutate every project.

- Inspect first. Confirm the exact `.uproject`, editor identity, version, enabled plugins, and current project-local task button.
- Existing button: preserve the button, startup loader, bridge modules, and task file. No reinstall, duplicate registration, automatic refresh, or smoke-test replacement.
- Confirmed missing button: install the project-local Python template after prerequisite and safety checks. Do not install globally. Partial/uncertain installation is not a license to overwrite.
- Prefer direct Remote Execution of a separate reviewed task. Do not invoke the button runner or overwrite `Saved/CodexScripts/run_task.py` for a direct task.
- A disabled task stays disabled unless the user explicitly asks to change it.
- Discovery failure: report the blocker and agree on a fallback. Never automatically switch to rewriting the button task, enabling network settings, restarting, or launching another editor.
- No new C++ modules, targets, plugins, or startup changes merely to connect. Do not restore files intentionally isolated during startup recovery.
- No automatic asset overwrite, deletion, scene assignment, or post-process change beyond the requested scope. Preserve user-tuned parameters; save only explicitly approved assets.
- A failed or timed-out mutation may already have side effects. Inspect receipts/logs/current state before any further action; do not blindly replay it.
- Keep credentials, private project paths, assets, logs, and generated task receipts out of public commits. Use placeholders in published instructions.

When maintaining this repository, keep README, the UE 5.4 protocol, the button guide, and all harness prompts consistent. Run `python -m unittest discover -s tests -v`. Offline tests do not prove a real visible button, a click, network reachability, or an asset's visual result; report those separately.
