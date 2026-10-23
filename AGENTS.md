# UE Agent entry

Read docs/agent-entry.md and the exact installed UE version notes. 优先使用当前工程已经配置并验证可用的 EngineWire MCP；成熟批量任务可使用编辑器内 UE Python；独立 Remote Execution 作为备用。连接方式不按 UE 版本号硬编码。

- 只读确认 .uproject、引擎、版本、PID 与当前关卡，禁止取第一个发现的编辑器。
- 按 MCP 返回的 schema 与 nextCall 执行；能力授权不代替用户授权。
- 保留现有启动脚本与用户入口，不为连接新增 C++ 模块、Target 或另一份工程。
- 不自动覆盖资产、保存全部脏关卡、重启编辑器或启动第二个编辑器。结果不明先读回再重试。
- 不发布令牌、用户资产、截图、私有路径或任务日志。
- 维护 README、协议、Agent 提示词的一致性，运行 python -m unittest discover -s tests -v。
