# 献给白绮的殖民领版图整理：需求分析与产品合同

状态：`released / workshop-public`

产品 key：`colonial_region_transfer`

产品目录：`mod_colonial_region_transfer/`

脚本与本地化前缀：`xcrt_`

分析日期：2026-09-11

后续维护：包含殖民领与非殖民领在内的所有合格直属领土型附属国，见[二期需求分析与实施计划](colonial-region-transfer-phase-2.md)。该计划尚未实现，不改变本文件记录的 0.1.0 已发布行为。

## 原始需求

> 点一个殖民地
>
> 殖民地互动里多一个选项
>
> 能够把该地区的所有自己的地以及自己附属的地都划给他
>
> 主要是为了版图好看()

## 需求拆解

原文中的“殖民地”解释为殖民领附属国，而不是一个尚未建成的殖民据点；“该地区”解释为所选殖民领首都所在的 EU5 `region`；“自己附属的地”包括玩家直属及更下层附属国持有的地点。这样无需再选地点，能以一次附属国互动清理一个完整 Region 内同一宗主体系的犬牙交错领土。

玩家价值可以写成一句话：宗主从附属国互动中选择一个直属殖民领，一次把该殖民领首都 Region 内、宗主体系持有的全部地点划给它，以整理版图。

中文展示名为“献给白绮的殖民领版图整理”，互动选项名为“整理殖民领地区”；非中文语境中的人名统一写作 `Vivhite`，英文展示名为 “For Vivhite: Colonial Border Cleanup”。献词属于 Mod 标题，不重复添加到每条互动按钮和说明中。

### 术语与边界

| 原文 | 可验证定义 |
| --- | --- |
| 点一个殖民地 | 在 `CATEGORY_SUBJECT_ACTIONS` 中选择玩家的直属殖民领附属国作为 `scope:recipient`。 |
| 该地区 | `scope:recipient.capital.region`。不是 Area、Subcontinent、殖民范围或殖民特许状范围。 |
| 自己的地 | Region 内 `owner = scope:actor` 的全部可拥有地点。 |
| 自己附属的地 | Region 内 owner 为 `scope:actor` 的任意层级附属国的全部可拥有地点。 |
| 都划给他 | 对上述地点执行 `change_location_owner = scope:recipient`；目标已经持有的地点保持不变。 |
| 为了版图好看 | 不改变 Region 外领土，不夺取独立国、敌国或其他宗主体系的领土，不附加金钱、威望或外交惩罚。 |

## 玩家行为合同

- 入口：国家外交/附属国互动的“附属国行动”分类。
- 可选目标：行动发起者的直属殖民领附属国；普通附属国、独立国、建筑国家与人口国家不可选。
- 前置条件：宗主、目标以及在目标 Region 内拥有待转让地点的附属国均不在战争中；宗主首都不能与目标殖民领首都位于同一 Region；至少存在一个尚不属于目标的可转让地点。
- 玩家动作：选择“整理殖民领地区”，阅读明确的不可逆警告并确认。
- 成功后置条件：目标 Region 内所有原属宗主或其任意层级附属国的可拥有地点都由目标殖民领持有；互动本身不选择或转让 Region 外及体系外地点。失去首都或全部领土后由 EU5 触发的迁都、国家消失及其间接后果属于下述明确警告的生命周期风险。
- 无工作量：没有待转让地点时目标项禁用，并显示原因；不得产生空操作的成功假象。
- 重复执行：第一次成功后，在没有新增待转让地点的情况下不可再次执行；后来取得新地点后可再次执行。
- AI 边界：`ai_tick = never`，AI 永不主动执行；本产品只提供玩家工具。
- 存档边界：不写持久变量，不注册 on_action，不要求新游戏；效果完成后的所有权变化必须在保存并重载后保持。

### “全部”带来的有意风险

“全部”不静默排除附属国首都。若另一个附属国的全部国土都位于目标 Region，该国可能在最后一个地点被转让后失去全部领土并消失；若其首都被转让但仍有 Region 外领土，游戏可能重选首都，也可能保留失效首都指针并在存档重载时清理该国。该行为符合原始的一键清图诉求，但必须同时满足以下条件：

- 交互说明和确认文案明确提示可能导致其他附属国消失或迁都；
- 战争期间禁用，避免在战争参与者集合仍活跃时改写国家生存状态；
- L3 实机验收覆盖“附属国在 Region 内仅剩最后一块地”和“首都在 Region 内、另有 Region 外领土”两个高风险场景；
- 在 L3 通过前，不得把该版本标记为运行时 GREEN 或公开发布候选。

## 非目标

- 不转让目标 Region 外的任何地点。
- 不改变核心、整合等级、控制者、人口、建筑、文化、宗教或市场。
- 不吞并目标殖民领，不调用原版“合并殖民地”的整国吞并流程。
- 不提供 Area/Subcontinent/自定义框选等第二种地理口径。
- 不让 AI 使用，不做自动月度整理，不增加 MCP、输入注入或 GUI 自动化。
- 当前运行时与 OCR 只验收简体中文；EU5 当前内置的其他语言必须提供完整本地化并通过 L0 静态检查，但不以静态结果冒充运行时验证。
- 上一轮源码实现不包含 Workshop 发布、tag 或 GitHub Release；本轮接管是否完成这些动作，以后文的明确接管范围及全部发布门禁为准。

## exact-build 原版依据

适用基线：Steam App `3450310`，Build ID `24187685`，`eu5.exe` SHA-256 `c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef`。

| 原版证据 | SHA-256 | 被本产品采用的事实 |
| --- | --- | --- |
| `game/in_game/common/country_interactions/give_location_to_subject.txt` | `82f5bdf0c0c85637e7e1d81c9722d09083e7672fa08cfc8d9f91c6f9f6a489f3` | `type = subject`、`CATEGORY_SUBJECT_ACTIONS`、`scope:actor`/`scope:recipient`、地点选择和 `change_location_owner`。 |
| `game/in_game/common/country_interactions/give_subject_location_to_other_subject.txt` | `58e84f71ad9219b2d1d81530d1b648d86b310b91fcda3c179d04e13e8022ee6e` | 宗主可重划两个附属国之间的地点，且原版单地点工具主动排除首都。 |
| `game/in_game/common/country_interactions/merge_colonies.txt` | `0aa4d7b3704c1f3c26ec2259bcdb08561acd7993aab925c12c1a2f32a1ffac2a` | `is_colonial_overlord`、`is_colonial_subject`、殖民领选择、战争门禁与 `ai_tick = never`。 |
| `game/in_game/common/country_interactions/readme.txt` | `2656714d72427abacd2497fc23bc80940a91df64f8c4f5d24c3839866a6ead23` | `show_message = no` 与 `show_message_to_target = no` 是关闭双方自动互动消息的正式字段。 |
| `game/in_game/events/debug/qa_debug.txt` | `26664f3b8013c860dcf96690d5bd6e7544a3544198128fb9b56e13bedf30976e` | 原版存在 `capital.region = { every_location_in_region = { ... change_location_owner = ... } }` 的整 Region 批处理模式。 |
| `game/main_menu/localization/simp_chinese/country_interactions_l_simp_chinese.yml` | `86833fac8166602c67ba03a06e722b91e3c87ffcaa9ff03012a9f28f80511628` | 互动本地化位于 `main_menu/localization/simp_chinese`，文件使用 UTF-8 BOM，且存在名称、动作、描述、效果与确认文案键族。 |

辅助事实：当前构建还在原版脚本中使用 `any_location_in_region`、`every_subject_or_below`、`is_subject_or_below_of` 和 `owner ?= { is_subject_of = ... }`。这些证据仅证明语法形态和 scope 路径存在；在 Open Kaishek 建立锁定该 build 的 EU5 profile、并完成游戏日志验收以前，不能宣称 Mod 脚本语义已被工具或引擎验证。

## 技术设计

EU5 Build `24187685` 会为 country interaction 默认查找 `WE_PERFORM_<key>_ACTION` 与 `ACTION_<key>_PERFORMED_ON_US` message type。该产品已有玩家确认弹窗且不需要执行后的重复消息，因此必须使用原版 `country_interactions/readme.txt` 声明的 `show_message = no` 和 `show_message_to_target = no`；不得用覆盖全局 `main_menu/gui/messagetypes.txt` 的方式消除错误。

产品只追加一个唯一命名的 country interaction，不覆盖任何原版文件：

1. `type = subject`，分类使用 `CATEGORY_SUBJECT_ACTIONS`，AI 禁用。
2. `select_trigger` 只从 `scope:actor.every_subject` 提供直属殖民领，并保存为 `scope:recipient`。
3. 可用性检查在 `scope:recipient.capital.region` 中查找至少一个可拥有地点，其 owner 是宗主或宗主的任意层级附属国，且 owner 不是目标。
4. effect 进入同一个 Region，迭代同一集合并将 owner 改为 `scope:recipient`。
5. 交互用一条汇总 tooltip 隐藏逐地点效果洪流；不保存变量，不添加核心，不修改控制者。

预期写入面仅为：

- `in_game/common/country_interactions/xcrt_colonial_region_transfer.txt`
- `main_menu/localization/<language>/xcrt_colonial_region_transfer_l_<language>.yml`，覆盖当前构建的 `braz_por`、`english`、`french`、`german`、`japanese`、`korean`、`polish`、`russian`、`simp_chinese`、`spanish` 与 `turkish`
- 产品 README、VERSION、验收计划，以及由当前 EU5 Mod Tools 生成并冻结的 `.metadata/metadata.json`

正式 release builder 使用精确 allowlist；开发文档、测试证据、缓存和仓库工具不得进入 Mod ZIP。

### 首轮接管复核：选择器 scope 修正

在 `select_trigger` 的 `visible`/`enabled` 中，当前候选对象是 `this`，互动发起者仍是 `root`/`scope:actor`；`target_flag = recipient` 同时把当前候选暴露为 `scope:recipient`。因此所有依赖候选殖民领首都 Region 的条件必须显式使用 `scope:recipient.capital.region`，不能使用 `root.capital.region`。

初版源码错误使用了 `root.capital.region`：宗主首都门禁实际把宗主首都 Region 与自身比较，使所有目标恒为不可用；战争 donor 与可转让地点检查也错误落在宗主首都 Region。修复验收要求为：

- 选择器中不得再出现 `root.capital.region`；
- 宗主首都、受影响 donor 与待转让地点三条判断都以 `scope:recipient.capital.region` 为同一地理真源；
- 静态测试必须锁定这一 scope 不变量，实机 L2 仍需覆盖目标可用与三类禁用原因。

全量 effect 还必须先把符合条件的地点加入本次执行的临时 scope list，再迭代该快照转让。不能在原始 Region 迭代器中一边重新判断附属关系一边转让：转走 donor 的最后一块地可能先触发国家消失或附属树重挂，令尚未遍历到的下层附属国从动态条件中漏出。快照只保存地点句柄，不写入存档或持久变量。

### 2026-09-12 接管、验收与发布范围

本轮接管目标是把已有源码推进到可公开交付：复核并修复产品缺陷，补齐当前 EU5 Mod Tools 原生 metadata，在隔离简中环境完成 L1–L3，生成可复现候选，从 Workshop fresh cache 复核后提交并推送发布记录。初版合同中的“本轮不发布 Workshop”只约束上一轮源码实现，已被本轮用户明确要求的发布工作取代；发布仍不得越过实机验收或 fresh-cache 门禁。本轮用户已明确授权把机器、屏幕、Steam 与 EU5 视为独占资源，并要求忽略不可用的共享任务总线，因此该缺失总线不再构成本轮门禁。

验收夹具只负责把隔离存档布置成可复现状态，不能替代产品的真实附属国互动入口。夹具采用外置 overlay：在临时验收树中叠加到产品源码，记录自己的文件哈希和 exact-build 地点依赖，且永不进入 release allowlist、staging、ZIP 或 Workshop cache。首个成功场景固定覆盖：目标殖民领、宗主同 Region 地点、仅余末块领地的直接 donor、该 donor 的下层附属国、首都需要迁移且仍有 Region 外领地的 donor、同 Region 体系外国家，以及 Region 外宗主地点。

正式 release builder 的产品合同为：

- 仅接受工作树干净、HEAD 与 `colonial_region_transfer-v<VERSION>` 精确 tag 一致的候选；
- 把 allowlist 投影到独立 staging，并为每个文件记录相对路径、大小和 SHA-256；
- 使用固定排序、时间戳、权限与压缩参数生成 ZIP，拒绝覆盖既有同版本输出；
- `--check` 在两个一次性目录中独立构建，并逐字节比较 staging、manifest 与 ZIP；
- metadata 缺失或静态验证未通过时，在写入 release 输出前拒绝构建。

## 验收矩阵

| 层级 | 场景 | 可证伪断言 | 所需证据 |
| --- | --- | --- | --- |
| L0 | 结构、编码与静态合同 | 唯一 `xcrt_` key；括号、重复键、11 种语言的本地化引用、UTF-8 BOM、allowlist、版本一致性通过；非中文标题使用 `Vivhite`。 | 静态验证报告、输入哈希、`git diff --check`。 |
| L0 | P 语言语义工具覆盖 | Open Kaishek 的 EU5 exact-build profile 能解析并 round-trip 产品脚本；否则标记 `tool-coverage RED`。 | profile 身份、解析 JSON、诊断列表。 |
| L1 | 隔离加载 | 只启用本 Mod 时，fresh 日志确认 Mod 被加载，且无本产品归因的 script/localization error。 | fresh 日志、加载配置、Mod 树哈希。 |
| L2 | 主成功路径 | 宗主直属地和另一个附属国的地位于目标首都 Region；确认后全部归目标，Region 外不变。 | 前后地点 owner 清单、简中 UI 截图、OCR JSON、日志。 |
| L2 | 体系外隔离 | 同 Region 的独立国/敌国地点不变。 | 前后 owner 对照。 |
| L2 | 禁用路径 | 普通附属国不可选；战争中、同首都 Region 或无待转让地点时不可执行，并显示可读原因。 | 简中截图与 OCR、日志。 |
| L3 | 末块领地 | 另一个附属国仅有一个待转让地点时，结果符合引擎生命周期且无产品错误。 | 前后国家/地点状态、日志、存档。 |
| L3 | 首都生命周期 | donor 首都被转让但仍有 Region 外领土时，互动不直接转让 Region 外地点；迁都、失效首都指针或重载清理由引擎决定并如实记录。 | 前后首都与 owner、日志、存档。 |
| L3 | 保存重载 | 成功后保存并重载，目标 Region、体系外地点和 Region 外非目标所有权断言保持；donor 实际生命周期结果与产品警告一致。 | 重载后 owner 清单、日志、简中截图。 |

## 当前门禁状态

- 需求与 Build `24187685` 的七项 exact-build 哈希：已基线化并复核通过。
- EU5 Mod Tools 原生 stub/metadata：已由当前 Build `24187685` 的内置 Mod Tools 生成，stable ID 为 `xenoamess.colonial_region_transfer`。
- 静态验证：metadata、脚本、11 种语言、版本与 allowlist 均通过；11 项工具测试通过。由于本机记录的 Open Kaishek 工作树不存在，当前结果仍为 `PASS_WITH_GATES`，语义工具覆盖单独标记 `tool-coverage RED`。
- 隔离简中实机：run `xcrt-20260912T064111-dev-runtime` 的加载、主成功路径、存档 owner、重载后审计、无工作量重复执行禁用、OCR 与真实 userdir 保护均通过；产品归因运行时错误为 0。两条历史脚本错误来自旧夹具对已被引擎清理国家的无效解引用，热修夹具后在同一进程通过，未重启游戏。
- 补充负路径 run `xcrt-20260912T044732Z-full-gates-runtime` 已取得战争与宗主首都同 Region 的原生可见禁用原因；同一 run 另取得互动、确认和执行结果三张无控制台的 `2560x1440` 实机展示图。
- 2026-09-13，用户审阅当前证据后明确判定验证已经充分并批准立即发布。因此产品验收门禁关闭；Open Kaishek profile 缺失仍保留为独立的 `tool-coverage RED`，不冒充产品 RED。
- `0.1.0` 已由 tag `colonial_region_transfer-v0.1.0` 的 commit `0e26c1ea12dbde40024db67d135994ac80cf8e56` 可复现构建并公开发布到 Workshop item [`3800505751`](https://steamcommunity.com/sharedfiles/filedetails/?id=3800505751)。上传结果、匿名页面回读、三张媒体回读与 fresh Workshop cache 严格比对均已通过；发布后 Steam 已恢复离线并保持运行。
