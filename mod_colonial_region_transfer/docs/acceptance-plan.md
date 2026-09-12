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

选择器 scope 回归条件：`select_trigger.enabled` 中宗主首都门禁、受影响 donor 战争门禁和可转让地点查询必须都引用 `scope:recipient.capital.region`；脚本中不得使用会解析为互动发起者的 `root.capital.region` 代指候选殖民领。

生命周期回归条件：effect 必须先冻结完整 `xcrt_transfer_locations` 临时列表，再执行所有权变更；L3 的末块领地场景同时放置下层附属国地点，证明 donor 消失不会截断已冻结的转让集合。

验收场景由 `fixtures/colonial_region_transfer/` 的外置 overlay 布置，只能合成到按 run ID 创建的一次性验收树。准备器同时以 ASCII 播放集名称和 UTF-8 JSON 生成只启用该投影的 `playsets.json`，避免本地化播放集名称经 PowerShell 默认编码往返后损坏 JSON。overlay 的 event/localization 以及场景说明均不属于产品 runtime allowlist；L0 必须证明正式 staging 和 ZIP 中没有 `xcrt_acceptance_` key 或 fixture 路径。夹具只负责布置与标记状态，L2 的执行动作仍必须来自玩家可见的“整理殖民领地区”互动。

当前预期门禁：

- `.metadata/metadata.json` 已由 EU5 Build `24187685` 的内置 Mod Tools 生成；静态检查验证 stable ID、版本与产品目录一致。metadata 缺失的安全拒绝仍由工具测试覆盖。
- 初版脚本曾由 Open Kaishek 通用 parser 做过 lossless round-trip，但修复后的当前脚本尚未由锁定 Build `24187685` 的 EU5 profile 复验；本机记录的 Open Kaishek 工作树当前不存在，语义覆盖仍标记 `tool-coverage RED`。
- run `xcrt-20260912T064111-dev-runtime` 已通过隔离加载、主成功路径、存档与重载审计、简中 OCR、无工作量重复执行禁用和 userdir 保护；完整结果见 [`acceptance-report.md`](acceptance-report.md)。战争与宗主首都同 Region 的可见禁用路径仍须在后续离线 Steam run 覆盖。
- 本轮用户已明确授权把机器、屏幕、Steam 与 EU5 视为独占资源，并要求忽略当前不可用的共享任务总线；该总线缺失不再阻止本轮实机与发布动作。

## L1 隔离加载

前置条件：用户在当前任务明确释放屏幕并授权启动 EU5；任务总线无屏幕冲突；原生 stub 已生成。

使用全新隔离 profile，只加载本产品。冻结 EU5 build、EXE SHA-256、metadata、Mod 树、启动参数、简中语言、分辨率、UI 缩放与 DPI。fresh 日志必须证明产品被加载，且没有归因于 `xcrt_` 的 script/localization error，包括不得出现缺失 `WE_PERFORM_xcrt_cleanup_colonial_region_ACTION` 或 `ACTION_xcrt_cleanup_colonial_region_PERFORMED_ON_US` message type。

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
- donor 首都位于目标 Region 但仍有 Region 外领土：执行后检查国家有效性、首都和日志；允许引擎按产品警告选择迁都或清理该国，但必须证明互动没有把 Region 外地点直接转给目标殖民领。
- 完成后保存、退出到可安全状态并重载：目标 Region 与体系外地点 owner 必须保持；记录并复核 donor 的实际生命周期结果，不把“必然迁都并存活”当作产品保证。

每次 attempt 使用新 run ID，永久保存 manifest、日志、截图、OCR JSON、owner 对照、存档、报告和 SHA-256。失败 attempt 不覆盖。
