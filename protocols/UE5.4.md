# UE 5.4 操作协议

先读 [统一接入流程](../docs/agent-entry.md)。优先使用当前工程已经配置并验证可用的 EngineWire MCP；成熟批量任务可使用编辑器内 UE Python；独立 Remote Execution 作为备用。连接方式不按 UE 版本号硬编码。

## 版本与预检

核对实际 UE 5.4 引擎版本、工程绝对路径、PID、架构和所选通道。Windows 5.4.4 的 EngineWire 连接与部分蓝图/材质/Niagara 有实测；Mac EngineWire 尚未验证。历史 Mac Python / C++ 实测不能外推为 MCP 可用。

Python Editor Script Plugin、Editor Scripting Utilities 按任务需要检查；Remote Execution 仅在采用该备用通道时需要。插件变更若需重启，先说明并取得当前任务授权，不自动关闭编辑器。纯资产任务不需要新建 Source、Target、插件或另一个 .uproject。

## MCP 与蓝图

按 search → describe → execute 的当前 schema 操作。MCP 支持的蓝图节点/连线可直接编辑，不能沿用旧 Python 桥接“必须让用户粘贴”的限制；单凭 UE Python API 不应承诺完整 K2 图编写。需要时先查当前插件能力，而非猜节点格式。

## Python 材质与资产

成熟批处理可以通过已验证的编辑器内 Python 执行。UE 5.4 常用 MaterialFactoryNew、MaterialEditingLibrary.create_material_expression / connect_material_expressions / connect_material_property / layout_material_expressions / recompile_material 与 EditorAssetLibrary.save_loaded_asset。属性未直接暴露时查 set_editor_property 支持。

先 load/inspect，确认任务范围后改图并保存指定资产。编译和布局是写入，不当作只读验证；材质编译可能触发编辑器刷新。历史事故边界见接入流程。

## Project C++

仅在用户任务需要运行时/反射功能时使用工程 Source 和实际 Editor Target。Editor Target is not necessarily the module name：读取 Source/*.Target.cs 中 Type=TargetType.Editor 的 TargetRules，不盲目拼接模块名 + Editor。

Windows：

```bat
"<ENGINE>\Engine\Build\BatchFiles\Build.bat" <EditorTarget> Win64 Development -project="<PROJECT>\<Name>.uproject" -NoHotReload
```

Mac Apple Silicon：

```sh
"<ENGINE>/Engine/Build/BatchFiles/Mac/Build.sh" <EditorTarget> Mac Development -project="<PROJECT>/<Name>.uproject" -architecture=arm64 -NoHotReload
```

UCLASS/UFUNCTION/UPROPERTY/USTRUCT/UENUM 变更通常需要成功构建与编辑器重启，Live Coding 可能残留过期反射。先说明重启需求，遵守用户授权。实现层 .cpp 变更可在适用范围内使用 Live Coding，结果过期时采用正常构建。不是所有连接任务都需要 C++。

## 验收

按当前任务分别核对资产路径、节点/属性、编译、保存、运行和场景镜头。独立脚本结果记录任务 ID、SHA-256、工程/版本/PID 与时间；不得用历史报告代替。超时/失败先查当前状态，不盲目重发。禁止为了接入安装或刷新按钮，旧工程入口不自动卸载。
