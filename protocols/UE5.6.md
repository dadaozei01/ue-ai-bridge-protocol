# UE 5.6 Notes

Status: pending direct project verification.

Start from `protocols/UE5.4.md` and verify API differences before making promises.

Expected stable principles:

- C++ features go through project `Source`.
- Materials and asset batch edits go through UE Python.
- Remote Execution is optional and may be blocked by network or sandboxing.
- Button bridge remains a reliable fallback for in-editor Python execution.

Before using on UE 5.6, verify:

- Python startup loading from `Content/Python/init_unreal.py`.
- `ToolMenus` menu registration behavior.
- Material API names.
- Build flags for macOS Apple Silicon and Windows.
