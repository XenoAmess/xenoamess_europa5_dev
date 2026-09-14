# 献给白绮的附属地整合：二期需求分析与实施计划

状态：`implementation-in-progress / 0.2.0 source-complete / runtime-and-publication-pending`

分析日期：2026-09-14

实施版本：`0.2.0`（`VERSION` 与 metadata 已更新；Workshop 远端仍须在 P4 上传后回读）

沿用产品 key：`colonial_region_transfer`

沿用 stable ID：`xenoamess.colonial_region_transfer`

二期工作展示名：献给白绮的附属地整合

二期英文工作名：For Vivhite: Subject Territory Consolidation

本文件是已发布 [0.1.0 产品合同](colonial-region-transfer.md)的增量合同与实施计划，不改写 0.1.0 的历史事实。截至 2026-09-14，二期源码、版本、metadata、11 种本地化、外置验收夹具、静态工具与新缩略图输入已经落地；Open Kaishek exact-build profile 与 L0 已通过，隔离实机、发布构建、Workshop 上传和 fresh-cache 回读仍须按 P3/P4 完成。

## 原始二期需求

> 包含殖民领，以及非殖民领的，所有附属国都可以用这个互动

## 结论

二期保留 0.1.0 的殖民领路径，并把同一个互动扩展到所有直属、领土型附属国。目标不再要求 `is_colonial_subject = yes`，宗主也不再要求 `is_colonial_overlord = yes`；除此之外，目标首都 `Region`、转让集合、战争门禁、宗主首都保护、快照后批量转让、AI 禁用和生命周期警告均保持不变。

二期同时替换当前正式缩略图：使用已经生成并由用户选定的“白绮人物形象 + 附属领土汇聚”图，替代 0.1.0 的纯制图徽章。用户已在 2026-09-14 当前任务中明确确认拥有参考头像的使用权；该确认关闭参考权利待确认门禁，但不等于已经授权本轮提前发布 0.2.0。

这里的“所有”是属性集合，不是硬编码的附属类型 allowlist：当前或未来 exact build 中，只要候选是行动发起者的直属附属国、属于可持有地点的国家类型并拥有有效首都，就应进入候选集合。殖民领是该集合的一员，不是特例或排除项。

`state_bank`、`trade_company` 等 `building` 型附属关系，以及可能出现的 `pop`/`army` 型对象，不是本互动的领土接收者。它们没有“以自身首都 Region 整合可拥有地点”的稳定玩家语义，原版地点转让互动也排除 `building` 与 `pop` 国家。它们必须从目标列表排除或显示明确不可用原因，不能因遍历 `every_subject` 而被误收。

## 相对 0.1.0 的需求差异

| 维度 | 已发布 0.1.0 | 二期 0.2.0 目标 |
| --- | --- | --- |
| 展示名 | 献给白绮的殖民领版图整理 | 献给白绮的附属地整合 |
| 入口 | 附属国行动 | 不变 |
| 宗主可见条件 | 必须是殖民宗主 | 拥有至少一个合格直属领土型附属国 |
| 可选目标 | 直属殖民领 | 包含殖民领和非殖民领在内的所有合格直属领土型附属国 |
| 地理范围 | 目标首都所在 `Region` | 不变 |
| 地点来源 | 宗主及其任意层级附属国 | 不变 |
| 目标之外的下层附属国 | 可作为 donor，但不能直接成为目标 | 不变；二期只扩展附属类型，不扩展关系层级 |
| 效果 | 快照后把合格地点转给目标 | 不变 |
| AI | `ai_tick = never` | 不变 |
| 正式缩略图 | 纯制图徽章 `icon-512.png` | 换为已选定的 `icon-vivhite-subject-consolidation-v2-512.png`，同时表达白绮与附属地汇聚 |
| 产品身份 | `colonial_region_transfer` / `xenoamess.colonial_region_transfer` | 保留，避免拆分 Workshop 身份和稳定 ID |
| 脚本根 key | `xcrt_cleanup_colonial_region` | 保留已公开 key；用本地化将玩家文案泛化，不做破坏性更名 |

## 二期玩家行为合同

- 入口：国家外交/附属国互动的“附属国行动”分类。
- 可选目标：行动发起者的直属、领土型附属国；殖民领与非殖民领一视同仁。候选必须拥有有效首都。`building`、`pop`、`army` 型附属对象以及独立国不可选。
- 关系层级：目标必须满足 `is_subject_of = scope:actor`。`scope:actor` 的更下层附属国仍可贡献待转让地点，但不会越过其直属宗主直接成为本次目标。
- 地理真源：唯一范围为 `scope:recipient.capital.region`，不是 Area、Province、Subcontinent 或附属类型的传统活动范围。
- 前置条件：宗主与目标均不在战争中；在目标 Region 内拥有待转让地点的任意层级附属国均不在战争中；宗主首都不在目标 Region；至少有一个尚不属于目标的可转让地点；目标满足其附属类型的领土接收硬限制。
- 玩家动作：选择泛化后的“整合附属地”互动，阅读不可逆和附属国生命周期警告并确认。
- 成功后置条件：执行开始时，目标 Region 内由宗主或宗主任意层级附属国持有、且尚不属于目标的全部可拥有地点，均在同一次操作中转给目标；Region 外和宗主体系外地点不变。
- 失败/取消：取消时不产生任何所有权变化；任一硬前置条件不满足时不得执行，也不得出现空操作成功提示。
- 重复执行：没有新增待转让地点时不可再次执行；后来出现新地点时可以再次执行。
- AI 边界：AI 永不主动使用。
- 保存边界：不新增持久变量或 on_action；所有权结果和实际发生的国家生命周期结果在保存重载后保持。

### 附属类型自身限制

“所有附属国可用”不等于绕过原版附属类型的领土上限。当前原版 `give_location_to_subject` 对 `tusi` 只在其已有地点数少于 15 时允许再给一个地点。二期是批量转让，不能只检查执行前 `num_locations < 15` 后一次塞入多个地点；实现前必须用当前 EU5 方言验证一种原子计算最终地点数的方案，并保证 Tusi 执行后不超过 15。若无法证明该批量约束，Tusi 路径保持门禁未关闭，二期不得以“所有附属国”发布。

实现前还要复核 current exact build 是否存在其他由原版地点转让路径施加的接收限制。发现新限制时，以目标自身规则优先，并把条件和可见禁用原因追加到本合同；不得静默绕过。

2026-09-14 的首轮简中实机验收暴露了两项必须分别保留的事实。第一，参数化数量 helper 的诊断结果不稳定，因此产品的选择器与 effect 门禁都采用显式 `OR = { NOT = { is_subject_type = tusi } AND = { is_subject_type = tusi ... } }`，并展开为 14 组字面量数量比较；参数化 helper 不再用于这两处保护。第二，runs `xcrt-20260913T212843Z-phase2-acceptance`、`xcrt-20260913T231422Z-phase2-tusi-fixed` 与 `xcrt-20260914T004551Z-phase2-tusi-explicit` 使用法国在加勒比调用 `create_country_from_location { subject_type = tusi }`，违反原版 `can_country_have_tusi` / `is_country_valid_for_tusi_subject` 创建条件；引擎实际创建的是非土司附属对象。第三个 run 的最小诊断明确显示 `NOT = { is_subject_type = tusi }`，故先前把 14→16 归因于 `trigger_if` 的结论撤回，这三次尝试按 `fixture/harness RED` 保留且不得作为产品语义证据。run `xcrt-20260914T033418Z-phase2-tusi-historical` 又证明，把真实 `GYT` 从 `LNG` 改挂到 `CHI` 会在 `make_subject_of` 时将关系降级为非土司；该 run 同样按 `fixture/harness RED` 保留。最终夹具必须保持 1337 开局原生的 `LNG`→`GYT` 土司关系不变，只把 `GYT` 首都暂移至隔离的加勒比 Region，再验证 14→15 成功以及 14→16、15→16 禁用；只有目标类型审计、真实互动和后置数量同时成立才能关闭土司门禁。

## 二期缩略图替换合同

- 人物参考：用户提供的白绮头像，来源为 <https://i0.hdslb.com/bfs/face/718c36bc01a173d0c42c0d1131f67e31055244c7.jpg>，调查副本 SHA-256 `b52b0624a3c2b2114f66a6c7ba839880d1dc89adaa91de0f5ca6bfc302160ca6`。参考原图不进入产品源码、release staging 或 Workshop cache。
- 权利状态：用户于 2026-09-14 明确确认拥有该参考头像的使用权；二期不再以“等待参考权利确认”为门禁。
- 选定母版：`workshop/colonial_region_transfer/media/icon-vivhite-subject-consolidation-v2-source.png`，1254×1254，SHA-256 `1868bdba33f394872f44c5fac78b031e7d6e4e47849452b387e075f573d375c7`。
- 正式上传输入：`workshop/colonial_region_transfer/media/icon-vivhite-subject-consolidation-v2-512.png`，512×512，SHA-256 `ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a`。
- 被替换对象：0.1.0 当前正式预览 `icon-512.png`，以及 fresh Workshop cache 中对应的 `.metadata/thumbnail.png`；两者当前 SHA-256 均为 `8db0837c6e1e7804543a0b80bfe038a4534f882f060ed0fc0c52beadb19b9e8d`。
- 玩家可见合同：白绮的浅冰蓝短发、紫红眼睛、圆形金色眼镜和黑金发饰清楚可辨；外围领土碎片由金色制图线路汇聚为一个完整 Region；不得出现文字、字母、旗帜、EU5/Steam 标志、商标或水印。
- 缩略图合同：512 px 上传输入和 64 px 页面预览都必须保持人物为第一视觉中心、领土汇聚为第二视觉中心。现有 64 px 本地投影已完成首轮人工审阅，但正式发布仍须复核 Steam 实际渲染。
- 发布原子性：缩略图替换与 0.2.0 内容上传属于同一个发布目标。若 Mod Tools 未接受新图、远端仍显示旧图、远端图损坏，或 fresh cache 的 `.metadata/thumbnail.png` 与选定输入不一致，则发布门禁为 RED；不能只发布脚本后宣称二期完成。
- 历史保全：不覆盖或删除 `icon-source.png`、`icon-512.png` 及 0.1.0 媒体 manifest。新图沿用独立文件名和 candidate manifest，使旧发布证据继续可复核。

## 当前 exact-build 附属类型盘点

2026-09-14 复核本机 Steam App `3450310`：仍为 Build `24187685`，`eu5.exe` SHA-256 仍为 `c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef`。

`game/in_game/common/subject_types/` 当前定义 20 个附属类型。二期预期目标矩阵如下；“预期可选”仍须由 L0 语义工具和 L2 实机矩阵验证，不能把文件名盘点当成运行时 GREEN。

| 分组 | 当前 Build 类型 | 二期期望 |
| --- | --- | --- |
| 殖民领 | `colonial_nation` | 可选；必须保留 0.1.0 回归路径 |
| 常规领土型 | `appanage`、`conquistador`、`dominion`、`fiefdom`、`march`、`secessionists`、`tributary`、`vassal` | 可选 |
| 地域/制度特有领土型 | `pronoia`、`hanseatic_member`、`imperial_free_city`、`direct_imperial_free_city`、`samanta`、`maha_samanta`、`pradhana_maha_samanta`、`tusi`、`uc_bey` | 可选；各自创建条件不应被互动改写 |
| 非领土型 | `state_bank`、`trade_company` | 不可选；两者在原版 subject type 中明确为 `type = building` |

当前目录只有 `colonial_nation` 声明 `is_colonial_subject = yes`。二期不能把 18 个预期领土型类型写成手工 OR 列表；应从直属附属国集合按领土能力筛选，使新增的合格附属类型无需再改 Mod 才能进入候选，同时由 exact-build 复核防止新非领土类型误入。

### 原版证据

| 原版证据 | SHA-256 | 本次采用的事实 |
| --- | --- | --- |
| `binaries/eu5.exe` | `c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef` | 当前可执行文件仍与 Build `24187685` 基线一致。 |
| `game/in_game/common/subject_types/readme.txt` | `06a72f97064d4f88bd1582dd50890a337ddd95b602f275dc57407f33bf842837` | `subject type.type` 表达可使用该附属类型的 country type，当前文档列出 `location/pop/building/army`。 |
| `game/in_game/common/subject_types/colonial_nation.txt` | `f39406149eec6a7dbc84bac977c9831b081d32667daeb56b2c7b92806483af58` | `colonial_nation` 声明 `is_colonial_subject = yes`；二期仍须包含它。 |
| `game/in_game/common/subject_types/state_bank.txt` | `c90271bca606e9f3129e2ee57d169112c50f4d2e066f312f49d621863a302bae` | `state_bank` 是 `type = building`，不属于领土接收目标。 |
| `game/in_game/common/subject_types/trade_company.txt` | `5bcdc8852af7dd5633d04bb4c2c01113ca85f3b06a2a466b23301109bc641d55` | `trade_company` 是 `type = building`，不属于领土接收目标。 |
| `game/in_game/common/country_interactions/give_location_to_subject.txt` | `82f5bdf0c0c85637e7e1d81c9722d09083e7672fa08cfc8d9f91c6f9f6a489f3` | 原版从 `every_subject` 选择目标、排除 `building/pop`，并对 `tusi` 应用 15 地点上限。 |
| `game/in_game/common/country_interactions/move_subject_capital.txt` | `7c103ee37ff67c8fc6118ea44144d3e7c42ba8c6fd1a4e266f043cb67808e6f0` | 原版对通用直属附属国使用 `every_subject`，并在需要领土语义时排除 `building/pop`。 |

这些证据支持二期的候选集合形状，但不证明批量转让对每种特殊附属类型都安全。尤其是 Tusi 最终数量、无首都对象、附属类型切换和 donor 消失期间的 scope 生命周期，仍须按后续计划验证。

## 技术设计约束

高风险调用链保持为：

```text
玩家打开附属国行动
  → scope:actor.every_subject 枚举直属候选
  → 领土能力与有效 capital 筛选
  → 候选保存为 scope:recipient
  → scope:recipient.capital.region 计算唯一 Region
  → 同一 Region 内冻结宗主体系地点列表
  → 复核目标、战争、数量与 Region 门禁
  → 遍历快照执行 change_location_owner = scope:recipient
  → UI、owner 真值、日志与重载交叉验证
```

实施必须满足：

1. 删除殖民专属入口门禁，不能再以 `is_colonial_overlord = yes` 决定整个互动是否出现。
2. `interaction_source_list` 继续使用 `scope:actor.every_subject`；去掉 `is_colonial_subject = yes` 过滤，保留直属关系、领土型 country type 与有效首都约束。
3. 选择器、`potential` 和 effect 的接收者保护必须使用同一业务谓词。不能只扩大 UI 列表而让 effect 接受不同集合，也不能只靠隐藏按钮保护业务效果。
4. `scope:recipient.capital.region` 仍是选择器检查与 effect 的共享地理真源；禁止退回 `root.capital.region`。
5. 继续先冻结 `xcrt_transfer_locations`，再修改所有权，防止 donor 的最后地点被转走后改变附属树并截断遍历。
6. 保留 `xcrt_cleanup_colonial_region` 根 key、`xcrt_` 前缀、stable ID 和 Workshop item。殖民专属的本地化 key 可保留为兼容别名或只增不删；玩家可见文案全部改为“附属地/subject territory”语义。
7. metadata 名称、说明和版本应通过当前 build 的 Mod Tools 工作流更新并审阅；不得创建第二个 stable ID。实施版本按向后兼容的功能扩展规划为 `0.2.0`。
8. 正式 staging 仍只包含产品 allowlist；扩展后的 fixture、类型矩阵和测试数据不得进入 Workshop ZIP。
9. 0.2.0 的 Mod Tools 上传输入必须选择已冻结哈希的新 512 px 图；当前 build 将上传图投影到 Workshop cache 的 `.metadata/thumbnail.png`，因此发布报告必须同时记录输入图、远端页面显示和 fresh-cache 文件。是否把 thumbnail 纳入 release ZIP 由 exact-build Mod Tools 的实测身份决定，不能把 Workshop 上传资产误称为普通 runtime 源码。

## 实施计划与退出条件

### P0：冻结二期基线与未决机制

- 将上述七项原版哈希加入静态基线或产品 validator。
- 生成一份 current exact build 的 subject type 盘点，检查新增/删除类型、country type 与所有原版“给地点”限制。
- 在 Open Kaishek 建立并锁定 Build `24187685` 的 EU5 profile，验证候选谓词、`exists = capital`、批量 Tusi 数量计算以及 effect 保护写法；无法覆盖时标记 `tool-coverage RED`。

退出条件：目标谓词和 Tusi 最终数量算法不再依赖字段名猜测，20 类型矩阵与 exact build 对齐。

### P1：泛化互动与玩家文案

- 修改既有 `xcrt_cleanup_colonial_region`，以合格直属领土型附属国替代殖民专属筛选。
- 保持 Region、donor 集合、战争门禁、宗主首都门禁、地点快照和 AI 边界不变。
- 增加 effect 侧接收者与关键前置条件复核。
- 泛化 11 种内置语言的标题、动作、说明、效果、确认和不可用原因；简中作为运行时权威文案，其他语言只做静态验收。
- 将选定的白绮人物关联图登记为 0.2.0 唯一缩略图输入，保持旧图和旧 manifest 只读；更新产品 README、Workshop 草稿及媒体引用。
- 更新 metadata、产品 README、Workshop 草稿、validator、builder allowlist 和工具测试；本阶段不上传。

退出条件：L0 证明不再存在殖民专属可见门禁，殖民领回归仍在，18 个预期领土型类型不是手工 allowlist，所有引用均有本地化；新缩略图的路径、尺寸与 SHA-256 和 candidate manifest 一致。

### P2：扩展隔离夹具与静态回归

- 保留现有殖民领主路径场景，新增普通 `vassal` 目标的同构成功场景。
- 建立 exact-build 目标矩阵夹具：逐一证明 18 个预期领土型类型能进入候选；`state_bank`、`trade_company` 和构造出的非领土型对象不能进入候选。
- 为无法由 fixture 安全创建的历史/制度类型保留可复现的 `fixture/harness RED`，不得用其他类型的结果代替。
- 增加 Tusi 14→15 可执行、14→超过 15 禁用、15→更多禁用的边界场景。
- 复用并扩展战争、同首都 Region、无工作量、体系外隔离、donor 末块领地和首都迁移场景。

退出条件：静态测试、工具测试和 fixture 合成通过；任何未覆盖类型被明确记录，不能笼统宣称“所有”。

### P3：简中 L1–L3 实机验收

- L1：全新隔离 profile 只加载候选 Mod，fresh 日志无产品归因错误。
- L2：分别用殖民领、普通非殖民附属国和至少一个制度特有附属国完成真实 UI 操作，核对 Region 内/外与体系内/外 owner。
- L2：通过候选矩阵确认所有可构造领土型类型的可见性；确认两种 `building` 型附属关系不可选且没有坏 scope tooltip。
- L3：验证 Tusi 上限、donor 最后地点、首都迁移/国家清理、取消、重复执行和保存重载。
- 发布前本地媒体复核：在 512 px 与 64 px 检查人物身份特征、领土汇聚主题、安全边距和禁用元素；该检查只关闭本地素材门禁，不替代 Steam 页面回读。

退出条件：简中 UI/OCR、owner 真值、fresh 日志和重载存档共同支持合同；失败 attempt 永久保留并正确分类。

### P4：候选与发布（仅在用户另行明确要求时）

- 写 `docs/release-changelogs/colonial_region_transfer/0.2.0.md`，从 clean commit 构建可复现 staging、manifest 和 ZIP。
- 绑定 `colonial_region_transfer-v0.2.0` tag，更新同一 Workshop item，不创建新产品身份。
- 通过当前 EU5 Mod Tools 把选定的 512 px 图设置为该 Workshop item 的新正式缩略图，与 0.2.0 内容在同一发布目标中完成。
- 回读远端页面，确认显示的是白绮人物关联图而非旧制图徽章；从空路径取得 fresh Workshop cache，要求 `.metadata/thumbnail.png` 与选定输入逐字节一致，并执行必要的简中回归。
- 完成 GitHub commit/push；GitHub Release 仍需单独明确指令。

退出条件：只有发布门禁全部通过，才能把本文件状态从 `planned` 改为 `released`。本次文档任务不授权 P4。

## 二期最低验收矩阵

| 层级 | 场景 | 可证伪断言 | 证据 |
| --- | --- | --- | --- |
| L0 | 产品身份与兼容 | stable ID、产品 key、Workshop item、脚本根 key 不变；目标版本为 0.2.0。 | metadata diff、VERSION、静态报告。 |
| L0 | 通用选择器 | 源码不再要求殖民宗主或殖民目标；使用属性谓词覆盖 current build 的 18 个领土型类型。 | exact-build 类型清单、P 语言解析、静态断言。 |
| L0 | 非领土排除 | `building/pop/army` 型对象不能成为地点接收目标；无首都对象不会产生坏 scope。 | 静态断言、解析诊断。 |
| L0 | 新缩略图身份 | 二期唯一上传输入为已选定的 512×512 图片，路径、尺寸、字节数和 SHA-256 与 candidate manifest 一致；旧发布媒体未被覆盖。 | 图片检查、candidate manifest、Git diff。 |
| L1 | 隔离加载 | 候选被唯一加载，11 种本地化无缺失，产品归因错误为 0。 | manifest、Mod 树哈希、fresh 日志。 |
| L2 | 殖民领回归 | 殖民领仍可执行，结果与 0.1.0 合同一致。 | 简中 UI/OCR、前后 owner、日志。 |
| L2 | 非殖民主路径 | 普通 vassal 目标可执行，同 Region 合格地点全归目标，边界地点不变。 | 简中 UI/OCR、前后 owner、日志。 |
| L2 | 全类型候选矩阵 | 每个可构造的 current-build 领土型附属类型均出现；`state_bank`、`trade_company` 不出现。 | 类型逐项结果、截图/OCR、日志；未构造项单独 RED。 |
| L2 | 禁用与取消 | 战争、同首都 Region、无工作量、无有效首都、违反类型上限时不可执行；取消无变化。 | 禁用原因、前后 owner、日志。 |
| L3 | Tusi 批量上限 | 操作后的最终地点数不超过 15；恰好 15 的路径成功，超限路径不产生部分转让。 | 前后计数、owner、日志、存档。 |
| L3 | 生命周期与重载 | donor 末块/首都风险如实呈现；Region 外与体系外边界在保存重载后保持。 | 存档、重载审计、日志、简中截图。 |
| P | 同一 Workshop item | fresh cache 与 0.2.0 staging 一致，远端标题和说明已泛化，远端预览已换成白绮人物关联图，`.metadata/thumbnail.png` 与选定输入哈希一致。 | 上传回执、匿名回读/截图、cache manifest、缩略图 SHA-256。 |

## 非目标

- 不创建第二个 Mod、stable ID 或 Workshop item；二期是现有产品的向后兼容功能扩展。
- 不允许直接选择更下层附属国；如将来需要越级目标，另立需求并单独分析外交与 scope 语义。
- 不改变目标 Region 的定义，不增加 Area、Province、Subcontinent 或框选模式。
- 不改变宗主体系外领土，不自动吞并国家，不更改核心、控制、文化、宗教、市场或附属类型。
- 不保证 donor 首都一定迁移或国家一定存活；沿用 0.1.0 的显式生命周期风险合同。
- 不让 AI 使用，不增加自动周期执行。
- 不创建或发布 GitHub Release；本轮发布授权只覆盖既有 Steam Workshop item 的 0.2.0 更新、对应产品 tag 与普通 Git 推送。
