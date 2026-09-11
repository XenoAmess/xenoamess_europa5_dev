# 献给白绮的殖民领版图整理验收计划

本计划从仓库级[需求分析与产品合同](../../docs/requirements/colonial-region-transfer.md)派生。没有 fresh 证据的层级保持 `NOT_RUN`，不得推断为 GREEN。

## L0 静态

运行：

```powershell
python tools/validate_colonial_region_transfer_static.py
python -m unittest tests.test_colonial_region_transfer_tools
git diff --check
```

通过条件：脚本与 11 种语言本地化的 UTF-8 BOM、括号、键引用、命名空间、版本、exact-build 原版哈希和 release allowlist 全部通过。简体中文标题必须是“献给白绮的殖民领版图整理”，所有非中文标题必须包含人名 `Vivhite`。

当前预期门禁：

- `.metadata/metadata.json` 缺失时，普通静态检查报告 `PASS_WITH_GATES`，release builder 必须失败。
- Open Kaishek 通用 parser 已对当前脚本报告 `PARSED`、2276 bytes、823 CST nodes、42 blocks、0 diagnostics、`roundTrip = true`。
- Open Kaishek 尚无 EU5 Build `24187685` profile，语义覆盖仍标记 `tool-coverage RED`；通用 lossless 解析不能宣称 P 语言语义验收完成。

## L1 隔离加载

前置条件：用户在当前任务明确释放屏幕并授权启动 EU5；任务总线无屏幕冲突；原生 stub 已生成。

使用全新隔离 profile，只加载本产品。冻结 EU5 build、EXE SHA-256、metadata、Mod 树、启动参数、简中语言、分辨率、UI 缩放与 DPI。fresh 日志必须证明产品被加载，且没有归因于 `xcrt_` 的 script/localization error。

## L2 玩家行为

场景 A：宗主、目标殖民领、同 Region 的宗主直属地点、另一直属附属国地点、下层附属国地点、体系外国家地点，以及 Region 外宗主地点同时存在。

1. 打开附属国行动，OCR 找到“整理殖民领地区”。
2. 选择目标殖民领，截图和 OCR 保存确认警告。
3. 执行后读取 owner 真值：前三类体系内地点全部归目标；体系外和 Region 外地点不变。
4. 再次打开互动；若没有新地点，目标应显示为不可用。

场景 B：宗主、目标或持有待转让地点的 donor 处于战争。互动必须禁用，并显示简中原因。

场景 C：普通附属国不能成为目标；宗主与目标首都处于同一 Region 时禁用。

每个输入动作后都验证可见后置状态；OCR 只证明 UI，不替代地点 owner 真值。

## L3 高风险生命周期

- donor 在目标 Region 内仅余最后一块地：执行后检查 donor 国家生命周期、附属关系和日志。
- donor 首都位于目标 Region 但仍有 Region 外领土：执行后检查新首都、国家有效性和日志。
- 完成后保存、退出到可安全状态并重载：所有地点 owner、donor 生存状态与新首都必须保持。

每次 attempt 使用新 run ID，永久保存 manifest、日志、截图、OCR JSON、owner 对照、存档、报告和 SHA-256。失败 attempt 不覆盖。
