# deepseek-harness UE 接入提示词

先读取 https://github.com/dadaozei01/ue-ai-bridge-protocol/blob/main/docs/agent-entry.md 与 https://github.com/dadaozei01/ue-ai-bridge-protocol/blob/main/docs/blueprint-layout.md ，并查准确引擎版本的协议；EngineWire 的调用方式见 https://github.com/dadaozei01/enginewire-ue54 的 docs/agent-guide.md。本地技能副本与线上冲突时以线上为准。

优先使用当前工程已经配置并验证可用的 EngineWire MCP；成熟批量任务可使用编辑器内 UE Python；独立 Remote Execution 作为备用。连接方式不按 UE 版本号硬编码。

## 连接

- 端点为 HTTP MCP http://127.0.0.1:3000/mcp（8090/8091 不是这个接口）。UE 状态栏 MCP :3000 (n) 中 n 为已连接客户端数。
- 请求头 X-MCP-Capability-Token 每次连接时从目标工程读取，优先 Saved/MCP/scoped-capability-token，没有再读 Saved/MCP/capability-token。不打印、不贴进对话、不提交，不对外开放端口。客户端支持动态请求头脚本时用脚本读取；不支持时说明配置方法，由用户手动填写。
- 连上后先只读确认 .uproject 绝对路径、实际引擎版本、编辑器 PID 与当前关卡，必须与用户指定的工程唯一匹配；确认不了就停下澄清，不连第一个响应的 UE。
- Failed to connect 多为 UE 未启动或 3000 端口未监听；401 多为令牌属于别的工程或已重新生成。不通过关闭沙箱或扩大网络范围排错。

## 调用

- 入口 unreal：search → describe → execute，每一步照抄返回的 nextCall，参数只用 describe 列出的名称，不臆造 action/subAction。consentGrant 按本次返回一次性回传，不缓存，也不代替用户对任务的授权。
- execute 成功后也检查 warnings[] 与 expectations[]，先修正再继续。
- MCP 与编辑器内 UE Python 由 Agent 自行选择，不询问用户：少量、规则简单的操作直接用 MCP；资源多、规则复杂或会反复用的批量任务写 UE Python，经 MCP 在编辑器内执行，不另开 Remote Execution；完成后说明用了哪种。

## 边界

- 不安装按钮，不改现有启动文件；不因连接新增模块或 Target，不自动重启或另开编辑器。
- 现有资产先查再改，保留用户调参；只改任务指定对象，CDO 与关卡实例分开对待；只保存本次资产，不 Save All，不在磁盘上直接改 .uasset。
- 失败或超时先读回实际状态，不盲目重发。命名要求与实际资产对不上时，先列出实际名称再问。
- 批量执行与必要验证合理安排，不强制省额度。

## 蓝图排版

按 blueprint-layout.md 执行，要点：创建节点就带坐标（16 的倍数，可为对齐引脚微调）；正常长度优先紧凑单行，确实超长才按段折行；每行白色执行引脚中心水平，按节点形态补偿 NodePosY，而不是令 NodePosY 相同；数据计算放在执行线下方分道汇总，同级成列，双输入组居中、三输入中间对齐且上下均布；变量就近取值，Get 的位置按其宽度加短连线留白计算；跨行与长距离执行线用外侧转接点；修改已有图表时保留用户布局；不为排版反复全图读取或截图，碰撞自动挪位时只读回该节点及相邻节点补正。

## 验收

分别报告参数/节点读回、编译、保存、运行行为与实际镜头画面；调用返回 success 不等于任务完成。Windows UE 5.4.4 的部分 MCP 操作已实测；Mac（Apple Silicon、UE 5.4.4）已实测蓝图创建、批量写图表、生成 Actor、编辑器内 Python 与 PIE；其他写入首次使用后检查结果。不要将历史 Python 或 C++ 验证外推到新插件。

第一步：连上 MCP 后只读报告目标工程路径、引擎版本、PID 与当前关卡，等用户确认后再开始任务。
