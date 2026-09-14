# EU5 测试与 OCR 验收规范

状态：现行总纲。当前不要求 MCP。

## 1. 验收语言与屏幕门禁

- 实机、UI、OCR、保存重载和运行时回归默认只覆盖简体中文。
- 其他语言检查 key 集合、编码、文件头、动态 token、引用、raw key 和中文占位泄漏，但不宣称运行时通过。
- 没有用户对当前运行明确给出的屏幕授权，不得启动 EU5、Steam 或任何前台 GUI。
- 屏幕授权不是永久授权；每轮实机启动前重新确认共享任务总线没有资源冲突。

## 2. 分层模型

### L0：静态与构建

证明：

- 产品文件、metadata、命名空间、编码和本地化合同。
- 脚本结构与当前 `open_kaishek` EU5 profile 所覆盖的语义。
- 权威数据与生成文件 parity。
- release allowlist、测试内容剥离和 deterministic build。

L0 不能证明引擎 scope、运行时效果或 UI。

### L1：真实加载

使用隔离 profile 和唯一目标 Mod，证明：

- 实际加载树与预期 SHA-256 一致。
- Mod 在播放集中启用，版本、checksum 与 DLC 已记录。
- 能进入目标界面。
- fresh 日志没有可归因于产品的阻塞性加载/解析错误。

### L2：单项机制

通过玩家真实入口执行决议、事件、任务、互动、on_action、GUI 或状态转换，断言：

- 可见与不可见条件。
- 可用与不可用条件。
- 成本、取消和失败路径。
- effect 的精确后置状态。
- 重复执行、幂等或叠加合同。
- AI 边界和 scope 反向场景。

### L3：玩家闭环与生命周期

覆盖入口、操作、反馈及后续状态；按产品风险增加保存重载、对象死亡/消失、国家切换、延迟事件、跨周期、旧存档或兼容组合。

### P：发布与 fresh-cache

从空路径重新取得玩家实际下载的 Workshop cache，严格验证 manifest 允许的 metadata 规范化和其余文件；再对该缓存执行所需 L1–L3。P 未通过不能写“发布完成”。

## 3. OCR 的职责边界

OCR 可以证明：

- 玩家看见了正确标题、正文、选项、tooltip、数字和错误原因。
- 页面、窗口或列表确实切换。
- 没有 raw key、fallback、明显截断或测试文案。

OCR 不能单独证明：

- 点击实际执行了目标 effect。
- 屏幕上的相同数字来自目标脚本。
- scope、存档序列化、AI 路径或隐藏状态正确。
- 上传内容与本地源码字节一致。

因此业务断言至少使用“可见 UI + 日志/数值/存档/测试标记”中的两个独立证据面；高风险持久化必须包含保存重载后的证据。

## 4. 输入安全

- runner 在首次截图和输入前声明 Per-Monitor DPI awareness。
- 固定原始分辨率和 UI 缩放；截图预览缩放后的坐标不得用于点击。
- 优先使用已实测的稳定快捷键或物理扫描码，其次 OCR 文字定位，绝对坐标最后使用。
- 输入前保存同帧截图和 OCR bbox；输入后等待并验证新的可见状态。
- 重复文字必须结合窗口区域、层级和相邻锚点消歧。
- “输入 API 接受”只是 transport ACK，不是产品后置条件。

以上优先级来自 Stellaris 的可复用经验，但每个快捷键、扫描码、窗口布局和恢复动作都必须在 EU5 exact build 重新验证。

## 5. 隔离运行

第一次获得屏幕授权后，先完成无 Mod 基线并确认 EU5 的真实用户目录、日志路径、存档格式和隔离参数。不得只因其他 Paradox 游戏支持 `-userdir` 就假定 EU5 同样成立。

每个 run 必须：

1. 使用唯一 run ID 和一次性隔离 profile。
2. 固定语言、分辨率、UI 缩放、DLC、播放集和唯一目标 Mod。
3. 启动前清理本轮隔离日志，但不清理尚未闭合场景的相关历史 run。
4. 冻结 EXE、产品树、fixture、配置和启动参数哈希。
5. 退出后证明本轮进程树归零，并验证真实玩家目录未改变。

## 6. EU5 原生测试能力

当前安装 build 在 `game/in_game/common/tests` 自带测试定义与说明，支持按年份检查 `success`、`failure`、`end_year`、`fail_on_end_year` 及受限日志 effect。

产品可以在确认加载与触发方式后建立外置 acceptance-only tests，用来记录内部状态；这些文件必须由 release allowlist 排除。原生测试日志不能替代玩家真实入口、OCR UI 或保存重载证据。

## 7. run 证据合同

```text
_runtime/<run-id>/
├─ manifest.json
├─ config-snapshot/
├─ screenshots/
├─ ocr/
├─ logs/
├─ saves/
├─ actions.jsonl
├─ report.json
└─ hashes.json
```

报告至少记录：Git commit、游戏 build、EXE SHA-256、产品树 SHA-256、fixture SHA-256、场景断言、实际结果、证据相对路径和 SHA-256、进程清理和保护目录前后状态。

失败分类：

- `product RED`：产品违反行为合同。
- `fixture/harness RED`：夹具、OCR、坐标、时序或断言有误。
- `environment RED`：屏幕、输入法、Steam、依赖或进程环境不满足前提。
- `tool-coverage RED`：parser、profile、OCR adapter 或原生测试尚不支持该语义。

修复后创建新 run，只重跑受影响边界。失败记录永久保留，至少写入受 Git 管理的报告并包含 run ID、RED 分类、原因、替代结果和关键证据哈希；不得覆盖或改写为 GREEN。完整运行证据仅保留至对应场景闭合；报告落盘后清理 `_runtime/` 中已被替代的完整 run。
