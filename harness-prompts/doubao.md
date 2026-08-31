# Doubao Prompt

请遵循 `https://github.com/dadaozei01/ue-ai-bridge-protocol`。先识别准确的 `.uproject`、引擎版本与路径、平台、架构、模块、真实 Editor Target、插件状态和编辑器是否打开。预留版本说明不能作为已验证的执行流程。

新按钮标准只实测于 **Windows UE 5.4.4**。历史 macOS Apple Silicon UE 5.4 的 Python/菜单及 C++ 验证，不代表新工具栏在 macOS 或其他补丁版本已验证，也不代表 Windows C++ 编译已验证。先读 `protocols/UE5.4.md` 和 `docs/toolbar-button-ue5.4.md`，明确报告未验证的组合。

- 编辑器资产使用 UE 内部 Python，严格按用户要求实现，不预设材质类型或效果。只有用户另行要求 C++ 功能时才使用项目 `Source` 和真实 Editor Target；反射改动需要编译成功并重启。不要默认创建插件。
- 按钮只使用 Python ToolMenus：顶部工具栏白色 **▶**，显示文字时为 `▶ 运行任务脚本`。复用仓库模板，图标使用 `set_icon("EditorStyle", "PlayWorld.PlayInViewport", "Icons.Play")`，不要猜图标名称。
- 不得为了按钮或图标新增 C++ 模块、插件、Target、第二份 `.uproject`，或更改项目模块声明。多轮 API 失败后应检查本机引擎源码，不得未经授权扩大架构。
- 只有新工具栏按钮就绪后，才移除桥接自己的旧任务菜单。保留其他菜单及 Python/任务文件，不添加替代面板。
- 安装或升级前先备份：安装器会覆盖桥接 init 和 runner，保留已有任务并保留/补充启动 Python，不会自动备份。点击前检查被保留的任务内容。
- 检查 Python Editor Script Plugin 和 Editor Scripting Utilities；缺失时说明启用与重启要求，不擅自修改 `.uproject`。
- Remote Execution 只探测一次。发现失败后，为当前任务设置唯一 `UE_AI_BRIDGE_TASK_ID`，原子替换 `Saved/CodexScripts/run_task.py`，请用户点击一次白色 **▶**。不要默认操作 UE 界面或点击蓝图节点。
- 读取 `Saved/CodexScripts/last_task_report.json`；必须同时核对 `status: success`、当前 `task_id`、当前脚本的 `task_sha256`、新的起止时间、无错误，以及任务结果和所需资产状态。脚本吞掉异常或结果中有 `ERROR`，不能因外层成功就宣称任务成功。
- 测试按钮时先准备经过检查、不修改资产的任务，再等待用户点击。远程直接调用 runner 产生的报告不能算按钮点击验收；外观需单独确认。
- 不承诺仅用 Python 完整生成任意蓝图 EventGraph。
