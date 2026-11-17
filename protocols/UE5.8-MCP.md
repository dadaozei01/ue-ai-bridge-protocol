# UE 5.8 MCP 验证范围

Windows x64，UE 5.8.4，BuildId 55116800。EngineWire 使用预发布版 [v0.6.0-ue58.1](https://github.com/dadaozei01/enginewire-ue54/releases/tag/v0.6.0-ue58.1)。

已实测：插件加载、MCP 连接、引擎目录安装加载；中文编辑器下的蓝图文本读写和编译；打开资产；通过 `call_editor_tool` 调用官方工具集的一个只读工具；Geometry Collection 创建、Voronoi 切割、Auto Cluster、物理设置、切割和分组的撤销重做、保存、放置 Actor，以及 PIE 落地破碎。

其他写入功能首次使用后需检查结果。关闭编辑器时的稳定性和 Fracture、PlanarCut 同时禁用时的启动尚未验证。UE 5.8 Mac 版未编译。

UE 5.8 官方 MCP 为实验性功能。2026-11-06 的一次中文编辑器测试中，`write_graph_dsl` 写入失败，`read_graph_dsl` 读回为空。英文界面未测。此结果仅限当次测试。
