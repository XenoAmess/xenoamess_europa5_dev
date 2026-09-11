# Europa Universalis V 多 Mod 仓库工作规则

## 仓库定位

- 本仓库同时管理多个相互独立的 Europa Universalis V Mod 产品。
- 每个正式产品位于仓库根目录的 `mod_<product_key>/`，拥有独立稳定 ID、版本、metadata、玩家文档、验收合同和发布历史。
- `docs/`、`tools/`、`tests/`、`fixtures/` 与 `workshop/` 是跨产品共享设施；不得把某个产品的专属规则悄悄变成其他产品的默认行为。
- 总体结构、命名与边界以 `docs/repository-architecture.md` 为准；生命周期以 `docs/development-lifecycle.md` 为准。

## 文档先行

- 新 Mod、功能、测试夹具、自动化工具或发布流程开始实施前，必须先在 `docs/` 或产品自己的文档中写明目标、范围、非目标、设计和验收标准。
- 调查得到的 EU5 方言、scope、metadata、启动、OCR、日志或存档事实必须回写知识库；CK3/Stellaris 经验未经当前 EU5 exact build 验证，不得当作 EU5 事实。
- 每个 Mod 必须维护可证伪的玩家行为合同。只有“有趣”“优化”“支持”之类目标而没有入口、动作和后置条件时，不得进入批量实现。
- 文档与代码不一致时，目标不算完成。

## 多产品结构

- 新产品使用根目录 `mod_<product_key>/`；`product_key` 与脚本、本地化、事件、变量及工具名前缀必须唯一且稳定。
- 每个产品至少维护 `README.md`、`VERSION`、EU5 生成的 `.metadata/metadata.json`、产品源码和验收计划。
- `.metadata/metadata.json` 必须先由当前 EU5 build 的内置 Mod Tools 生成 stub，再审阅并纳入仓库；禁止凭 CK3/Stellaris 经验手写猜测 schema。
- 每个产品的发布构建器命名为 `tools/build_<product_key>_release.py`，静态验证器命名为 `tools/validate_<product_key>_static.py`。
- 正式 release builder 使用精确 allowlist，只从产品源码生成 staging、manifest 与可复现 ZIP；不得直接上传开发树。
- 开发源码、外置 fixture、release staging、Workshop cache 是四种不同身份，不得混称、互相覆盖或用其中一种的结果替另一种背书。

## 单一权威来源

- 产品版本以 `mod_<product_key>/VERSION` 为唯一来源，并与 metadata 完全一致；游戏兼容版本单独表达。
- 重复内容、数值表、本地化扇出和图片投影应由权威数据与生成器产生；标记为 generated 的文件禁止手改。
- 已公开或进入存档的 key、变量、事件 ID 和产品 ID 默认只增不改；删除或更名必须先设计迁移。
- 能追加定义时不使用全目录替换。确需 `replace_paths` 时，必须记录原版文件、exact-build 哈希、覆盖原因、兼容对象和升级风险。

## EU5 exact-build 研究

- 实现机制前，先检查本机当前 EU5 原版中最接近的 `.info`、脚本、事件、GUI、本地化和 `common/tests` 定义。
- 高风险调用链必须记录：入口、当前 scope、scope 转换、trigger/effect、写入对象、生命周期和玩家可见后置条件。
- 未经原版源码、日志、存档或实机行为支持，不得仅凭字段名推断语义。
- `D:\workspace\open_kaishek` 当前没有 EU5 profile。第一个 P 语言产品宣告静态验收完成前，必须建立并验证锁定 exact build 的 EU5 profile；工具覆盖不足应标为 tool-coverage RED，不能冒充产品 RED。

## 屏幕与游戏进程硬门禁

- 本机桌面是共享资源。除非用户在当前任务中明确说明屏幕可用并授权本轮实机操作，否则禁止启动 EU5、Steam、任何游戏内 Mod Tools 或会抢占前台的 GUI 程序。
- 未获屏幕授权时只能进行源码、文档、构建、静态验证、既有日志/存档/截图分析等后台工作。
- 获得授权后，启动前仍须轮询共享任务总线，确认没有屏幕或 EU5 资源冲突；不得抢占、关闭或向其他任务的程序发送输入。
- 当前 EU5 验收不要求 MCP。不得为了开始产品开发而先扩张 MCP、注入器或原生桥工程。

## OCR 与实机验收

- EU5 实机、UI、OCR、存档重载和运行时回归默认只使用简体中文；其他语言默认只做静态检查，并明确写“运行时不在范围内”。
- OCR 是玩家可见 UI 的主要观察和导航手段，不是内部状态真值。效果必须按风险与 fresh 日志、前后数值、存档内容或确定性测试标记交叉验证。
- 固定并记录游戏 build、EXE SHA-256、Mod 树 SHA-256、DLC、播放集、语言、分辨率、UI 缩放、DPI awareness 和启动参数。
- OCR 坐标只能来自原始分辨率截图和同帧 bbox；输入后必须验证可见后置状态，不能把“点击已发送”写成业务成功。
- 每个运行使用隔离 userdir/profile，只启用目标 Mod；不得读写真实玩家存档或设置。隔离方式必须先在当前 EU5 build 实测成立。
- 完整验收层级和证据要求见 `docs/testing-and-acceptance.md`。

## 证据与失败处理

- 每次实机或发布尝试使用唯一 run ID；保存输入 manifest、配置快照、日志、截图、OCR JSON、存档、报告和 SHA-256。
- 失败 attempt 永久保留，不覆盖、不删除、不改写为 GREEN。重试必须创建新 run。
- RED 分类为 `product`、`fixture/harness`、`environment` 或 `tool-coverage`；不同类别不得互相冒充。
- ACK、解析通过、窗口出现、日志无错误或上传器成功，只能证明各自声明的局部条件。

## Git 提交与推送硬规则

- 每次完成用户交付的一个目标后，必须立即把该目标相关改动提交到 Git，并推送到当前分支所跟踪的 GitHub 远端；这是默认完成条件，不需要再次询问。
- 提交前必须运行与风险相称的检查、`git diff --check`、查看 `git status`，并只暂存当前目标相关文件。
- 推送前必须再次轮询共享任务总线，并执行 `git fetch`；若远端已推进，使用 rebase 整理为线性历史后再普通 push。
- 禁止 merge commit、force-push、覆盖其他任务改动或擅自提交用户的无关文件。
- 如果认证、远端冲突、测试失败或其他客观条件使 commit/push 不能完成，必须明确报告阻塞和仍未交付的部分，不能宣称目标完成。
- 发布 tag、GitHub Release、Workshop 上传和可见性变化属于独立发布动作；只有用户明确要求发布时才执行。

## 版本与发布

- 各产品独立使用 SemVer；成功公开发布过的版本号不得复用。
- 发布前必须写入 `docs/release-changelogs/<product_key>/<version>.md`，记录相对上一公开版的玩家变化、兼容性、已知限制和验收证据。
- 正式候选必须绑定 clean commit、产品 tag、staging manifest、ZIP 和 SHA-256。
- EU5 发布以当前 build 的内置 Mod Tools 实测行为为准，不照搬 Paradox Launcher 的 descriptor 规则。
- 上传完成不等于发布完成。必须回读远端页面，并从空路径取得 fresh Workshop cache，严格比对后执行所需的简中实机复核。

## 跨任务协作

- 遵守 `D:\workspace\AGENTS.md` 的共享任务总线约定：开始时 register + poll + list，资源或状态变化时更新，结束时标记 done。
- Git push、外部发布写入、EU5/Steam/GUI 启动前必须再次 `poll --ack`；发现冲突时先协调，不得绕过。
