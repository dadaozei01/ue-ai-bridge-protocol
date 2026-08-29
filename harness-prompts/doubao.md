# Doubao Prompt

请严格遵循 `https://github.com/dadaozei01/ue-ai-bridge-protocol`，先识别项目准确的 UE 版本，只允许使用标记为已实测的对应版本协议。

对于已验证的 UE5.4：C++ 写入项目 `Source`，编译 `Target.cs` 中真实存在的 Editor Target；编辑器资产使用 UE 内部 Python，并严格按用户描述实现，不预设材质类型或效果。不要默认创建插件、操作 UE 界面或点击蓝图节点。

Remote Execution 只探测一次。发现失败后，保留已有桥接文件，原子替换 `Saved/CodexScripts/run_task.py`，执行一次 `任务脚本 -> 运行任务脚本`，然后读取 `Saved/CodexScripts/last_task_report.json`。只有报告状态为 `success` 才能宣布成功。
