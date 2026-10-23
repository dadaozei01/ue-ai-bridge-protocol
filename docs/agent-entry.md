# 跨 Agent 统一接入

优先使用当前工程已经配置并验证可用的 EngineWire MCP；成熟批量任务可使用编辑器内 UE Python；独立 Remote Execution 作为备用。连接方式不按 UE 版本号硬编码。

## 1. 只读确认目标

获取用户目标 .uproject 的绝对路径、实际引擎路径、准确版本与架构、当前编辑器 PID 与关卡。工程 EngineAssociation 可能是 GUID，不能只凭字符串判断版本。检查任务范围与未保存状态；纯资产任务没有 Source 或 Editor Target 很正常。仅检查所选执行方式所需的插件，不因使用 MCP 就强制打开 Python Remote Execution。

不能唯一确认工程时停止写入并澄清。未获准不修改插件配置、防火墙、网络范围或启动文件，不关闭编辑器、不另开同一工程。受环境限制时使用工具正规的权限机制。

## 2. EngineWire MCP

插件安装与客户端配置以 [enginewire-ue54](https://github.com/dadaozei01/enginewire-ue54) 为准；本页只定义统一操作规范。

- UE 开启 Native MCP Server 后重启生效。默认本机端点 http://127.0.0.1:3000/mcp；状态 MCP :3000 (0) 中 0 为客户端数。
- X-MCP-Capability-Token 从目标工程 Saved/MCP/capability-token 动态读取，不打印、不写入仓库，不公开网络。
- 入口 unreal：search 定位 → describe 获取当前 schema → execute 执行。使用返回的 nextCall，不臆造参数。configure 是工具组配置。
- consentGrant 按本次返回要求一次性使用，不能缓存，也不代替用户对任务的授权。
- 初次连接先只读确认工程或 Actor。MCP 可用时不再为连接安装按钮或额外 Python 网络桥。

## 3. 编辑器内 UE Python

成熟批量操作、精确参数更新或原生 MCP 未覆盖的能力，可使用 UE Python。MCP 若提供受支持的 Python 执行能力，可以沿现有连接执行，无需另建网络连接。脚本中的 import unreal 必须在编辑器内部执行，普通外部 Python 不具备该模块。

使用实际引擎暴露的 API，首次修改前 load + inspect。多步骤脚本使用独立文件、唯一任务 ID 与 SHA-256，固定内容后执行一次；记录目标工程/版本/PID、时间、资产路径、参数回读、错误和实际结果。较长脚本和报告使用获准的本地文件，避免过大的命令/回包。不要执行历史固定任务或覆盖现有启动文件。

## 4. Remote Execution 备用

仅在已有通道不适用且 Python 远程能力已配置或用户授权配置时采用。不会因为需要执行 Python 就必然另开 Remote Execution。

优先使用当前安装引擎的 Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python/remote_execution.py；检查 Python Editor Script Plugin 及任务所需 Editor Scripting Utilities。Windows 外部解释器通常是 Engine/Binaries/ThirdParty/Python3/Win64/python.exe，先核对路径。

1. 导入本机 remote_execution，创建 RemoteExecution 并 start，短时发现 remote_nodes。默认仅本机范围，不扩大组播 TTL。
2. 按 project_root / project_name / engine_root / engine_version 唯一匹配目标；规范化绝对路径，同目录多个工程再核对文件名。不能选第一个节点或复用历史 ID。
3. 使用本次 node_id 调用 open_command_connection。
4. 先在 UE 内只读核对 unreal.Paths.get_project_file_path()、project_dir()、SystemLibrary.get_engine_version()、os.getpid()。再查 LevelEditorSubsystem.is_in_play_in_editor()，不擅自停止他人的 PIE。
5. 用 run_command(..., unattended=True, raise_on_failure=False) 执行已审核独立脚本一次，检查 success/result/output 与实际状态。脚本经哈希校验后执行同一份字节，独立 exec 命名空间不是安全沙箱。
6. finally 中 stop，只关闭本次连接，不关闭编辑器。

发现失败先检查权限、插件与目标身份；不无限探测、不自动改网络或重启。历史 ue-claude-bridge/tools/ue_exec.py 选择首个响应者，缺少完整工程身份保护，不能作为自动写入的默认入口。

## 5. 写入与验收

同一编辑器协调写入任务，不同时抢写。修改现有资产前检查当前值与引用，未经任务授权不替换/删除图，不回写历史参数。保存本次目标资产，不 Save All。MCP 材质批次可能部分提交，超时也可能已执行，先读回状态再决定下一步。不要在磁盘上直接改 .uasset。

蓝图执行流从左向右，执行引脚对齐、间距一致，纯数据节点放附近下方，保留用户排布。动画生成新资产，不改 Skeleton 参考姿势；以用户场景镜头检查，不能只看资源预览。

验收分开记录：参数/节点读回、编译、保存、运行行为、实际相机视觉。文件存在或调用返回 success 均不等于任务完成；捕获异常后藏在 result 中的错误仍是失败。仅停止自己开启的测试，清理临时测试对象。

## 6. 历史保护边界

既有工程中的手动入口和启动脚本保持原状，本协议不再安装、刷新或依赖按钮。若用户另行要求清理，先核对 loader 的引用和自定义代码再处理，不能直接删除 init_unreal.py。

历史 Windows UE 5.4.4 材质编译曾出现 Window Creation Failed / User Objects: 10000，根因未确认；换通道不意味着修复崩溃，不重跑事故脚本或改系统配额。UE 5.4.4 的 get_all_edited_assets 未暴露给 Python；遇 API 失败查当前引擎源码，不猜跨版本接口。保留被故意隔离的启动恢复文件。
