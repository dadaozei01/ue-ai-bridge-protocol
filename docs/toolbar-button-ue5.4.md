# UE 5.4 工具栏按钮标准：只保留白色 ▶

## 先检查，避免重复安装

统一入口见 [跨 Agent 接入说明](agent-entry.md)。**当前项目已有按钮就保留，确认没有才安装；Agent 执行功能优先直连独立脚本，不默认使用按钮。**

- 已有按钮：不重装、不热刷新、不修改现有绑定/启动脚本，不替换 `run_task.py` 做测试。
- 确认缺失：使用本页的项目级 Python 模板安装；先检查插件、权限和已有文件。不要全局安装。
- 文件存在但可见性/注册状态不明：先只读检查日志、当前注册证据或请用户确认，不当作缺失直接覆盖。
- 任务停用：按钮仍可保留，停用的任务继续停用。按钮存在不等于 Remote Execution 已启用。
- 直连失败：先报告并协商回退，不自动修改按钮任务，也不自动重启编辑器。

以下安装、热刷新和点击验收步骤，仅适用于缺失按钮的安装或用户明确要求的修复/升级；不是每次接手项目都要运行的流程。

## 实测范围

2026-08-31，Windows UE **5.4.4** 实际工程验证：Python 注册工具栏、白色三角显示、当前编辑器热刷新、移除旧菜单、用户亲自点击后生成匹配任务 ID 和 SHA-256 的成功报告。

这是按钮桥接的验证，不代表 Windows C++ 编译、所有资产 API 或其他 UE 版本已经验证。此前 macOS Apple Silicon UE 5.4 的旧菜单桥接/C++ 有实测记录；**本次工具栏版尚未在 macOS 重新验证**。5.5、5.6、5.8-MCP 仍为预留协议。

## 最终外观与行为

- 顶部工具栏增加一个白色 **▶**，名称为 `▶ 运行任务脚本`。
- 在测试布局中位于「平台」附近；位置随窗口布局、播放状态变化，不要依赖固定屏幕坐标。
- 紧凑工具栏可以只显示图标；它不是 UE 自带的绿色游戏 Play 按钮。
- 不再显示顶部「任务脚本」菜单，不创建额外工具面板。
- 点击只执行当前工程的 `Saved/CodexScripts/run_task.py`，结果由原执行器写到 `last_task_report.json`。
- 移除菜单不等于删除任务文件。`init_unreal.py`、`ue_ai_bridge_init.py`、`ue_ai_bridge_runner.py` 和 `run_task.py` 仍需保留。

## 固定实现

直接使用仓库中的 [Python 模板](../templates/ue5.4/Content/Python/ue_ai_bridge_init.py)，不要让 AI 重新猜一套接口。

| 项目 | 标准值 |
| --- | --- |
| 工具栏 | `LevelEditor.LevelEditorToolBar.PlayToolBar` |
| 分组 | `UEAIBridge` |
| 按钮名称 | `RunTaskScriptToolbar` |
| 按钮类型 | `unreal.MultiBlockType.TOOL_BAR_BUTTON` |
| 样式集 | `EditorStyle` |
| 大图标 | `PlayWorld.PlayInViewport` |
| 小图标 | `Icons.Play` |

```python
entry.set_label("\u25b6 运行任务脚本")
entry.set_icon("EditorStyle", "PlayWorld.PlayInViewport", "Icons.Play")
entry.set_string_command(
    unreal.ToolMenuStringCommandType.PYTHON,
    "",
    "import ue_ai_bridge_runner; ue_ai_bridge_runner.run_task()",
)
```

上述图标键来自本机 UE 5.4.4 的 `Engine/Source/Editor/EditorStyle/Private/StarshipStyle.cpp`。**不要使用不存在的 `PlayWorld.Play`，也不要保证图标为绿色。** 图标名称写入成功不代表 Slate 找到了图标，仍需检查画面。

每次注册定点替换该按钮，保留其他工具栏项目。只有工具栏注册成功之后，才移除旧菜单：

```python
menus.remove_entry("LevelEditor.MainMenu", "", "UEAIBridgeTaskMenu")
menus.remove_menu("LevelEditor.MainMenu.UEAIBridgeTaskMenu")
```

不清空整个主菜单。若工具栏尚未准备好，保留旧入口并有限重试；120 ticks 后停止。`_done` 仅表示回调已结束，不独自证明注册成功；同时检查 `_last_error`、日志和画面。

## 安装与升级

1. 确认准确的 `.uproject`、UE 版本、插件状态及当前打开的工程。
2. 检查 Python Editor Script Plugin 和 Editor Scripting Utilities；如需启用或重启，先说明并取得用户同意，不自动关闭当前编辑器。
3. 升级前备份现有启动脚本、两个桥接模块和任务脚本。安装器会覆盖两个桥接模块，不自动为它们备份。
4. 在仓库目录运行 Windows 安装器：

   ```powershell
   .\scripts\windows\install_bridge.ps1 -ProjectDir "C:\absolute\path\to\Project"
   ```

5. 初装可等用户下次正常打开编辑器时加载，不自动重启。已有启动代码会保留，必要时追加 loader；已有 `run_task.py` 不会被安装器替换。
6. **点击前先检查旧任务内容**：保留下来的诊断脚本可能含有删除测试资产等操作。只有用户明确同意按钮测试和任务替换时，才备份后换成下面的安全测试；停用占位脚本不能擅自启用。

日常更新 `run_task.py` 不需要重启。不要为了刷新按钮关闭用户尚未保存的工程。

### 已连接编辑器的热刷新

仅在用户同意的安装/修复中，且 Remote Execution 已经能发现当前编辑器时使用；发现失败就停止并报告，不自动重启、切换执行路径或持续调整网络配置。已有工作按钮不做热刷新。

在调用下列代码前，核对远端 `unreal.Paths.project_dir()`、`unreal.SystemLibrary.get_engine_version()` 和 `ue_ai_bridge_init.__file__`，确保是已确认的工程、5.4 版本和项目 Python 文件。不要把一个工程的成功当成另一个工程的验证。

```python
import importlib
import unreal
import ue_ai_bridge_init

pending = getattr(ue_ai_bridge_init, "_callback_handle", None)
if pending is not None:
    unreal.unregister_slate_post_tick_callback(pending)

importlib.reload(ue_ai_bridge_init)
ue_ai_bridge_init._register_menu(0.0)
assert ue_ai_bridge_init._done
assert ue_ai_bridge_init._last_error is None
assert unreal.ToolMenus.get().find_menu(
    "LevelEditor.MainMenu.UEAIBridgeTaskMenu"
) is None
```

这只是注册检查，不能替代可见按钮和点击测试。旧版 `add_sub_menu` 创建的是扩展菜单，`find_menu` 有结果时 `is_menu_registered` 仍可能是 False，不要据此误判菜单不存在。

## 新按钮的安全验收

### 1. 准备新的任务

每次验收填写一个新的、可识别的 `UE_AI_BRIDGE_TASK_ID`。先备份旧任务，再写临时文件并原子替换 `Saved/CodexScripts/run_task.py`，不要让编辑器读到写了一半的脚本。

```python
import unreal

UE_AI_BRIDGE_TASK_ID = "replace-with-a-new-unique-task-id"
UE_AI_BRIDGE_RESULT = {
    "message": "Toolbar button test completed.",
    "assets_modified": False,
    "engine_version": unreal.SystemLibrary.get_engine_version(),
}
unreal.log("[UEAIBridge] BUTTON_TEST_OK: " + UE_AI_BRIDGE_TASK_ID)
```

此测试不创建、修改、保存或删除资产，也不弹窗；画面没有变化是正常的。`assets_modified: False` 是任务自报信息，仍必须检查脚本本身确实没有资产写操作。

### 2. 用户点击一次

确认白色 ▶ 可见，让用户亲自点击一次。用户正在操作编辑器时，不抢鼠标；需要自动点击时先取得用户授权。不要先用远程执行器运行这个新测试，再把那份报告当作点击证据。

### 3. 核对报告

读取当前工程的 `Saved/CodexScripts/last_task_report.json`，同时确认：

- `status` 为 `success`。
- `task_id` 等于刚才写入的新编号。
- `task_sha256` 等于当前脚本文件的 SHA-256。
- 开始/结束时间属于这次测试，不是旧报告。
- `error` 为空，`result` 符合预期；没有隐藏的失败步骤。

在 Windows 上可用 `Get-FileHash -Algorithm SHA256` 计算脚本哈希。完整验收是：**图标可见 → 用户点击 → 新任务成功 → ID/哈希匹配**。

执行器只把“脚本正常返回”记为 success。若任务自己捕获异常，并把 `ERROR`、`all failed`、`not found` 放进结果，它仍可能写出外层 success。必要步骤失败应抛出异常，或由验收明确判失败；不要只看最外层状态。

## 避免再次损坏工程启动

- 给按钮加图标不需要新建 C++ 模块、插件、Editor Target 或第二个 `.uproject`。
- 不为了按钮美化向 `.uproject` 添加 `Modules` 启动依赖。
- 不把本地编译的访问拒绝误判成“需要重装 UE”，先读构建日志。
- 不默认删 `Source`、`Binaries`、`Intermediate`，也不直接清空所有模块声明。
- 发现连续失败、需要改架构时停止，核对本机 API，向用户说明范围变化。
- 若先前改造已导致缺失模块：先检查源码、引用和日志，备份后仅撤销确认无业务依赖的错误加载要求；不要把它当成通用自动修复。
- UE 5.4 的 `Missing target file` 与 `Missing Modules` 不是同一个提示。前者在已核对本机启动逻辑的恢复场景中可选择 No 跳过构建；不能因此断言任意缺失模块都可忽略。

## 可直接交给 AI 的短指令

> 先检查当前项目是否已有按钮：有则保留，不重装、不替换任务；确认没有才按本仓库 Windows UE 5.4.4 标准安装项目级白色 ▶。标签为「▶ 运行任务脚本」，图标使用 EditorStyle / PlayWorld.PlayInViewport / Icons.Play，不新增 C++、插件、Target 或工程 Modules。Agent 执行功能优先直连独立脚本，直连失败先报告，不自动覆盖 run_task.py。只有明确同意的按钮验收才准备新测试，用户点击后核对状态、任务 ID、哈希、时间和结果，禁止用旧报告代替验收。
