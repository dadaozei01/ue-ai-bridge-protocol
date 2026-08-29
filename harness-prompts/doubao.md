# Doubao Prompt

请严格按我的 UE AI Bridge Protocol 执行。

不要默认操作 UE 界面，不要默认创建插件，不要自动点蓝图节点。

C++ 功能：直接改项目 `Source`，编译 Editor 目标。Mac Apple Silicon 必须使用 `-architecture=arm64 -NoHotReload`。新增或修改 `UCLASS / UPROPERTY / UFUNCTION / USTRUCT / UENUM` 后告诉我需要重启 UE。

材质和资产：用 UE Python 的标准老接口。Remote Execution 能连上就直接执行；连不上就更新 `Saved/CodexScripts/run_task.py`，让我在 UE 里点 `任务脚本 -> ▶ 运行任务脚本`。

按钮桥由 `Content/Python/init_unreal.py` 注册菜单，只负责入口；具体任务只写 `run_task.py`。
