# Doubao Prompt

先读 `docs/agent-entry.md`。**先检查当前项目按钮：有则保留，确认没有才安装项目级模板。执行功能优先直连 UE，运行独立脚本，不默认通过按钮。** 需要本机文件、终端和 Python 执行权限；只读 GitHub 不会获得用户电脑的控制权。

已有按钮不重装、不热刷新、不重复注册，不修改启动入口、桥接模块或任务文件。停用任务保持停用。有文件但按钮状态不明时先检查并报告，不能当作缺失直接覆盖。安装缺失按钮不等于授权执行被保留的旧任务或重启编辑器。

请遵循 `https://github.com/dadaozei01/ue-ai-bridge-protocol`。先识别准确的 `.uproject`、引擎版本与路径、平台、架构、模块、真实 Editor Target、插件状态和编辑器是否打开。预留版本说明不能作为已验证的执行流程。

新按钮标准只实测于 **Windows UE 5.4.4**。历史 macOS Apple Silicon UE 5.4 的 Python/菜单及 C++ 验证，不代表新工具栏在 macOS 或其他补丁版本已验证，也不代表 Windows C++ 编译已验证。先读 `protocols/UE5.4.md` 和 `docs/toolbar-button-ue5.4.md`，明确报告未验证的组合。

- 编辑器资产使用 UE 内部 Python，严格按用户要求实现，不预设材质类型或效果。只有用户另行要求 C++ 功能时才使用项目 `Source` 和真实 Editor Target；反射改动通常需要编译成功并重启，但重启需先与用户协商。资产任务不要求补建模块或 Target，不默认创建插件。
- 按钮只使用 Python ToolMenus：顶部工具栏白色 **▶**，显示文字时为 `▶ 运行任务脚本`。复用仓库模板，图标使用 `set_icon("EditorStyle", "PlayWorld.PlayInViewport", "Icons.Play")`，不要猜图标名称。
- 不得为了按钮或图标新增 C++ 模块、插件、Target、第二份 `.uproject`，或更改项目模块声明。多轮 API 失败后应检查本机引擎源码，不得未经授权扩大架构。
- 仅在确认缺失按钮的安装或用户明确要求的修复/升级中，新工具栏按钮就绪后才移除桥接自己的旧任务菜单。已有正常按钮保持不动，保留其他菜单及 Python/任务文件，不添加替代面板。
- 安装或升级前先备份：安装器会覆盖桥接 init 和 runner，保留已有任务并保留/补充启动 Python，不会自动备份。点击前检查被保留的任务内容。
- 检查 Python Editor Script Plugin 和 Editor Scripting Utilities；缺失时说明启用与重启要求，不擅自修改 `.uproject`。
- 用当前引擎附带的 Remote Execution 模块做一次短时发现，唯一匹配指定工程和版本，并在 UE 内再次验证身份；不使用旧 node ID/PID，不任选第一个节点。优先单次执行独立、经过审核的脚本，不调用 `ue_ai_bridge_runner.run_task()`。单独记录任务 ID、SHA-256、工程身份、时间和结果，保持按钮任务及其报告不变。
- 直连不可用时报告原因并协商回退，不自动改写 `Saved/CodexScripts/run_task.py`、开启网络配置、重启或启动第二个编辑器。只有明确同意改走按钮，才备份后以唯一 `UE_AI_BRIDGE_TASK_ID` 原子更新任务，并请用户点击一次白色 **▶**。不默认操作 UE 界面或点击蓝图节点。
- 仅在明确同意的按钮任务中读取 `Saved/CodexScripts/last_task_report.json`；同时核对 `status: success`、当前 `task_id`、脚本的 `task_sha256`、新的起止时间、无错误，以及任务结果和资产状态。该文件不是独立直连任务的报告。脚本吞掉异常或结果中有 `ERROR`，不能因外层成功就宣称任务成功。
- 测试按钮时先准备经过检查、不修改资产的任务，再等待用户点击。远程直接调用 runner 产生的报告不能算按钮点击验收；外观需单独确认。
- 不承诺仅用 Python 完整生成任意蓝图 EventGraph。
- 响应不明、超时或写入失败时先只读查凭据、日志及实际状态，不盲目重发。保留用户已调参数、停用任务和隔离的启动恢复文件；不自动挂模型、修改后期、保存无关资产或重启 UE。`Window Creation Failed / User Objects: 10000` 的资源增长根因仍未知，不能宣称直连修复了崩溃。
