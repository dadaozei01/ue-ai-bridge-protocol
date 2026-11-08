# deepseek-harness UE 接入提示词

简单机械操作（建文件夹、移动、改名、复制等）走 agent-entry.md 第 0 节：两项及以上用一个 UE Python 脚本做完，不逐项调用 MCP，不读其他文档。

先读取以下文档并照做，本地技能副本与线上冲突时以线上为准：

- https://github.com/dadaozei01/ue-ai-bridge-protocol/blob/main/docs/agent-entry.md （接入、边界与验收）
- https://github.com/dadaozei01/ue-ai-bridge-protocol/blob/main/docs/blueprint-layout.md （写蓝图图表时的节点排版）
- https://github.com/dadaozei01/enginewire 的 docs/agent-guide.md （EngineWire MCP 的连接与调用）

优先使用已验证的 EngineWire MCP；批量任务可经 MCP 在编辑器内运行 UE Python；独立 Remote Execution 仅作备用。令牌从目标工程动态读取，不打印、不提交；客户端无法动态读取时告诉用户怎么配置。

第一步：连上后只读报告目标 .uproject 路径、引擎版本、编辑器 PID 与当前关卡，等用户确认后再开始任务。
