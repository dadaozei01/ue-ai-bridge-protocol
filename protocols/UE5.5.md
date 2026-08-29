# UE 5.5 Notes

Status: pending direct project verification.

Do not use this file as an execution procedure.

Start from `protocols/UE5.4.md` and verify API differences before making promises.

Expected stable principles:

- Prefer project C++ over plugins for project-specific gameplay tools.
- Prefer UE Python for materials and asset creation.
- Treat Remote Execution as optional.
- Avoid automatic UE UI control unless explicitly requested.
- Do not promise full Blueprint EventGraph node generation through Python until verified.

Before using on UE 5.5, verify:

- Python `ToolMenus` API names.
- `MaterialEditingLibrary` method availability.
- Build script flags for the installed engine.
- C++ target `IncludeOrderVersion`.
