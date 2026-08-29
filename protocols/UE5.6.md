# UE 5.6 Notes

Status: pending direct project verification.

Do not use this file as an execution procedure.

Start from `protocols/UE5.4.md` and verify API differences before making promises.

Expected stable principles:

- C++ features go through project `Source`.
- Materials and asset batch edits go through UE Python.
- Remote Execution is optional and may be blocked by network or sandboxing.
- The UE 5.4 button bridge is a candidate fallback, but is not verified here.

Before using on UE 5.6, verify:

- Python startup loading from `Content/Python/init_unreal.py`.
- `ToolMenus` menu registration behavior.
- Material API names.
- Build flags for macOS Apple Silicon and Windows.
