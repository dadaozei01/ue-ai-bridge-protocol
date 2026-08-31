# 跨 Agent 接入：先查按钮，执行优先直连

适用于 Codex、WorkBuddy、ZCode、DeepSeek Harness（DHS）、豆包及其他有本机文件、终端、Python 执行权限的 Agent。工具名称不是兼容性认证；纯聊天或纯云端工具不能仅凭阅读 GitHub 操作用户本机 UE。

本页规定默认工作顺序。按钮是用户保留的手动入口，直连是 Agent 优先使用的执行入口，两者独立。用户针对当前工程的限制优先于本文。

## 0. 第一次接手先只读

- 获取用户指定的绝对 `.uproject` 路径、引擎安装路径、准确版本和当前运行的编辑器。不要复用别人的盘符、PID 或 Remote Execution node ID。
- 检查 Python Editor Script Plugin、Editor Scripting Utilities 的状态。直连还要求 Python Remote Execution 已启用；按钮存在不证明远程连接可用。
- 检查当前任务、已调参数和未保存状态。只做编辑器资产任务时，没有 `Source` 或 Editor Target 是正常情况，不需要创建它们。
- 检查 Agent 自身权限。没有本机执行权限，应让用户提供本地执行环境，不假装已经连接。
- 默认仅尝试一次短时、本机范围的发现。受沙箱限制时使用工具提供的审批机制，不关闭隔离、不擅自开放外网端口。

Windows UE 5.4.4 有实测记录。其他系统/版本按各自协议说明验证，不猜跨版本 API。

## 1. 先检查按钮：有则保留，无则安装

| 检查结果 | 必须采取的动作 |
| --- | --- |
| 用户确认现有按钮，或当前注册证据能确认按钮存在 | 保留，不运行安装器，不热刷新，不改图标、绑定、启动代码或任务。继续检查直连。 |
| 确认项目没有按钮，且没有冲突的旧安装 | 按仓库已验证模板安装项目级按钮，先检查插件、权限和需写入的路径。安装不代表允许执行未知任务。 |
| 有脚本但按钮状态不明、安装残缺、存在同名自定义入口 | 只读查日志/绑定；说明差异，不当作“没有”直接覆盖或新建第二个按钮。 |
| 按钮存在，但任务是 disabled/无操作占位 | 按钮仍然有效；保持任务停用，不把停用状态当作安装失败。 |
| 插件未启用、需重启、现有启动代码冲突 | 明确告知需要的改动，等待用户确认；不自动关闭编辑器。 |

检查文件（都相对于当前工程，不是所有工程共用）：

```text
Content/Python/init_unreal.py
Content/Python/ue_ai_bridge_init.py
Content/Python/ue_ai_bridge_runner.py
Saved/CodexScripts/run_task.py
Saved/CodexScripts/bridge_debug.log
Saved/Logs/
```

结合当前会话的注册日志、已有截图/用户确认判断；文件存在只证明安装痕迹。`find_menu` 找到工具栏容器也不证明里面的特定按钮存在。不要为确认状态而点击可能有写入操作的任务。

缺少按钮时，复用 [按钮安装标准](toolbar-button-ue5.4.md) 与 `scripts/windows/install_bridge.ps1`，不新增 C++、插件模块、Target 或另一份 `.uproject`。已有任务必须保留，安装器不负责判断旧任务安全。缺失时附带的模板任务只记日志，不修改资产。

初装通常在用户下次正常打开编辑器时加载。用户允许且直连已经工作时，可按按钮指南做受控热注册；不为了验收强制重启。按钮外观与用户点击验证是单独的检查，不阻塞一个已经可用且获准的直连任务。

## 2. Agent 执行功能优先直连

### 本机连接入口

使用**当前安装引擎附带**的模块，不从旧任务复制写死的连接器：

```text
<ENGINE_INSTALL>/Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python/remote_execution.py
```

Windows UE 5.4 的外部解释器通常位于：

```text
<ENGINE_INSTALL>/Engine/Binaries/ThirdParty/Python3/Win64/python.exe
```

先检查路径确实存在。外部 Python 负责连接；`import unreal` 的资产操作在 UE 编辑器内部执行，不在普通外部 Python 中执行。

按本地模块源码执行以下步骤；这些是 API 调用顺序，不是可以跳过检查直接粘贴的整段程序：

1. 将上述 `Content/Python` 路径加入本次进程的 `sys.path`，导入 `remote_execution`。
2. 创建 `remote_execution.RemoteExecution()`，调用 `start()`，进行一次短时发现，读取 `remote_nodes`。本机默认组播 TTL 为 0；不要为了找到节点扩大网络范围。
3. 根据返回的 `project_root`、`project_name`、`engine_root`、`engine_version` 筛选用户指定的工程。目录用绝对路径规范化比较；同目录多份 `.uproject` 时还要核对工程文件名。没有唯一匹配项就停止并说明。
4. 使用这次发现的 `node_id` 调用 `open_command_connection(node_id)`。不能取列表第一个节点，也不能沿用 GitHub 示例里的历史 ID。
5. 先发只读身份查询：`unreal.Paths.get_project_file_path()`、`unreal.Paths.project_dir()`、`unreal.SystemLibrary.get_engine_version()` 和 `os.getpid()`；路径转为绝对路径后核对。确认工程文件、目录、版本、PID 属于本次目标。
6. 再核对 `unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).is_in_play_in_editor()`。正在运行 PIE 时不要擅自停止，先报告状态。
7. 通过 `run_command(..., unattended=True, raise_on_failure=False)` 执行批准的独立脚本一次，检查返回的 `success`、`result`、`output` 及资产实际状态。
8. 在 `finally` 中调用连接对象的 `stop()` 释放这次连接。它关闭的是客户端连接，不是 UE 编辑器。

以上接口已对照本机 UE 5.4.4 源码；遇到未暴露 API 先检查版本与本地定义，不通过新建 C++ 模块绕过。

### 独立任务要求

- 将任务放在 Agent 工作目录中，使用唯一文件名和任务 ID；不要写入按钮固定的 `run_task.py`。
- 发送前固定文件内容，计算 SHA-256。在 UE 内执行前再次核对文件哈希和编辑器身份；存在差异即停止。执行刚刚校验的同一份字节内容，不在校验后重新读取可能被替换的文件。
- 同一个编辑器一次只允许一个 Agent 写入任务。按钮执行器的 `_running` 只保护按钮调用，不能替独立脚本防并发；已有任务未结束时先协调，不抢占其他 Agent 的连接。
- 可以通过一条短命令读取这台机器上的已审核 UTF-8 文件，用 `with open(...)` 关闭文件，并以独立命名空间 `exec(compile(...), {})` 执行。独立命名空间**不是安全沙箱**，脚本仍拥有 UE Python 的权限。
- 不调用 `ue_ai_bridge_runner.run_task()` 来伪装独立执行。它仍会运行按钮任务、覆盖按钮报告。
- 本机 UE 5.4.4 的官方远程模块默认接收缓冲区有限；长脚本/大量输出可能导致响应解析失败。保持发送命令和回包简短，大报告写到独立的、获准的本地路径，不能覆盖按钮报告。
- 在首次写入前记录保护基线与任务开始凭据，目标已经存在就拒绝覆盖；不要把历史参数当作当前用户值回写。
- 只保存本次批准的资产，不使用 Save All，不自动挂载模型、改变后期或打开预览。需要这些动作时单独说明范围。
- 不要自动使用注册、编译、布局或打开编辑器来做“只读验证”；这些调用可能刷新编辑器或触发其他副作用。

### 独立结果与按钮结果分开

直接任务的报告至少记录任务 ID、脚本哈希、工程/版本/PID、开始结束时间、状态、已创建/修改的资产、参数回读和错误。检查任务真实结果，不只看连接返回成功。

`Saved/CodexScripts/last_task_report.json` 属于按钮执行器。它可能保留旧 `success` 或崩溃前的 `running`，不能作为新直连任务的结果。不要为“整理状态”覆盖它。

## 3. 直连失败时如何处理

- 找不到节点：说明发现结果、插件配置与 Agent 权限检查结论，不重复无限探测，不自动安装或改写按钮来代替排查。
- 网络/沙箱受限：按工具的正规权限审批流程处理，不擅自修改防火墙、组播、启动配置或端口。
- 多个工程匹配：让用户指定准确工程，不任选一个。
- 写入任务超时、响应丢失或 UE 异常：结果属于**不确定**，先只读查执行凭据、日志和目标资产；不得立即重发。异常时停止写操作，保留证据。
- 用户同意后才可改走手动按钮；修改其任务需要明确授权、备份和审核。原本停用的任务继续停用，除非用户明确要求启用。
- 启动第二个编辑器、命令行编译、重启/关闭当前 UE 都不是默认回退。

## 4. 已知事故边界

2026-08-31 的一次材质组合脚本在 `MaterialEditingLibrary.RecompileMaterial` 期间遇到 `Window Creation Failed`，进程 `User Objects: 10000`。USER 对象耗尽来源尚未查明，不能把它归因于按钮、某个插件或节点数量，也不能声称改用直连就修复了崩溃。

UE 5.4.4 的重编译路径包含编辑器刷新和可能创建进度窗口的纹理流送数据更新。避免主动打开资产编辑器不等于保证没有窗口副作用。重要实验前可以只读记录 USER 资源基线；低计数不是绝对安全证明，不自动提高系统配额。

另一次预检使用了仅原生可用的 `AssetEditorSubsystem.GetAllEditedAssets`，其 Python 形式 `get_all_edited_assets` 在该版本不可用。这是单独的 API 兼容问题，不是上述崩溃的已确认根因。

发现工程有隔离的启动恢复文件、停用任务或事故记录时，尊重当前保护状态，不恢复源码/TargetInfo，不重跑事故脚本。

## 5. 交付时告诉用户什么

报告按钮为“已有保留 / 新装待加载或验收 / 状态不明待检查”，以及实际执行方式。把以下事实分开：文件保存、UE 参数回读、编译检查、画面验证、用户点击验证。

本仓库已验证 Windows UE 5.4.4 的按钮路径与独立直连任务路径；并未逐一验证所有 Agent 产品。读取网页不会授予执行权限，`AGENTS.md` 是否自动加载也由各工具决定。第一次使用时明确要求 Agent 阅读本页。
