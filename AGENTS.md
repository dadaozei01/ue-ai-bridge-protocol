# UE Agent entry

Read docs/agent-entry.md and the exact installed UE version notes. 优先使用当前工程已经配置并验证可用的 EngineWire MCP；成熟批量任务可使用编辑器内 UE Python；独立 Remote Execution 作为备用。连接方式不按 UE 版本号硬编码。

- 简单机械操作（建文件夹、移动、改名、复制等）走 agent-entry.md 第 0 节：两项及以上用一个 UE Python 脚本做完，不逐项调用 MCP，不读其他文档。
- 只读确认 .uproject、引擎、版本、PID 与当前关卡，禁止取第一个发现的编辑器。
- 按 MCP 返回的 schema 与 nextCall 执行；能力授权不代替用户授权。
- 保留现有启动脚本与用户入口，不为连接新增 C++ 模块、Target 或另一份工程。
- 不自动覆盖资产、保存全部脏关卡、重启编辑器或启动第二个编辑器。结果不明先读回再重试。
- 不发布令牌、用户资产、截图、私有路径或任务日志。
- 写蓝图图表时创建节点就带坐标，按 docs/blueprint-layout.md 保持规整易读：执行线单独一行，数据计算在下方分道汇总，变量就近取值并对齐引脚，保留用户布局，不为排版额外截图验证。
- 维护 README、协议、Agent 提示词的一致性，运行 python -m unittest discover -s tests -v。


蓝图排版：创建时带坐标；正常长度优先紧凑单行，确实超长才按段折行；每行白色执行引脚水平对齐（不要求节点 Y 相同）；数据就近分道汇总；双输入组居中、三输入中间对齐且上下均布；跨行用外侧转接点；保留用户布局，仅对异常局部核对。
