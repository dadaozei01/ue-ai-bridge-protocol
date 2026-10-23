# codex UE 接入提示词

先读取 https://github.com/dadaozei01/ue-ai-bridge-protocol/blob/main/docs/agent-entry.md ，并查准确引擎版本的协议。

优先使用当前工程已经配置并验证可用的 EngineWire MCP；成熟批量任务可使用编辑器内 UE Python；独立 Remote Execution 作为备用。连接方式不按 UE 版本号硬编码。

先确认目标 .uproject、实际版本、编辑器身份和任务范围。MCP 使用 search → describe → execute 与返回的 schema / nextCall；动态读取本机能力令牌，不打印或提交。Python 在 UE 编辑器内运行，不要求为已有 MCP 另开网络桥。

不安装按钮，不改现有启动文件；不因连接新增模块或 Target，不自动重启或另开编辑器。现有资产先查再改，只保存本次资产；失败或超时先检查实际状态，不盲目重发。批量执行与必要验证合理安排，不强制省额度。

Windows UE 5.4.4 的 MCP 与部分功能已实测，Mac EngineWire 尚未验证。不要将历史 Python 或 C++ 验证外推到新插件。结果分别报告参数读回、编译、保存、运行、视觉效果。
