# UE AI Bridge Protocol

跨 Agent 的 Unreal Engine 操作规范，统一连接选择、工程身份核验、资产保护与结果验收。

优先使用当前工程已经配置并验证可用的 EngineWire MCP；成熟批量任务可使用编辑器内 UE Python；独立 Remote Execution 作为备用。连接方式不按 UE 版本号硬编码。

## 给其他 Agent 的入口

> 先读 https://github.com/dadaozei01/ue-ai-bridge-protocol/blob/main/docs/agent-entry.md 。确认目标工程和版本；优先已验证的 EngineWire MCP，成熟批量工作可用 UE Python，Remote Execution 备用。先查再改，不覆盖用户资产，不盲目重发结果不明的写入。

- [统一接入流程](docs/agent-entry.md)
- [UE 5.4 的 Python / C++ 注意事项](protocols/UE5.4.md)
- [EngineWire 安装、Windows 编译包与客户端配置](https://github.com/dadaozei01/enginewire-ue54)
- [Claude 接入与历史备用工具](https://github.com/dadaozei01/ue-claude-bridge)
- [通用提示词](harness-prompts/universal.md)

本协议不再提供按钮安装器、工具栏模板或点击验收流程；正常接入不需要安装按钮。既有工程中的按钮及启动脚本不自动卸载或改写。旧版文件可从 Git 历史查找，不应作为当前执行要求。

## 验证范围

- Windows UE 5.4.4：独立 Python Remote Execution 曾实测；2026-10-23 已实测 EngineWire MCP 的连接、蓝图、材质与 Niagara 操作。
- macOS Apple Silicon UE 5.4：历史 Python 与工程 C++ 有实测；EngineWire Mac 二进制尚未编译或验证。
- UE 5.5 / 5.6 / 5.8 文件为预留记录，不是执行程序；不按版本推定存在“官方 MCP”或兼容能力。

阅读 GitHub 不会赋予本机权限，Agent 名称也不代表兼容性认证。仅网页聊天环境不能因此直接操作 UE。

维护检查：python -m unittest discover -s tests -v。检查只验证仓库约定，不证明实时连接或视觉效果。
