# 献给白绮的附属地整合 0.2.0 验收报告

状态：L0_GREEN / L1-L3_IN_PROGRESS / WORKSHOP_PUBLISHED

本报告只记录 0.2.0。0.1.0 的既有实机与发布事实保留在
[acceptance-report.md](acceptance-report.md)，不得混用。

## 当前结论

| 层级 | 状态 | 结论 |
| --- | --- | --- |
| L0 静态合同 | PASS | 12 项 exact-build 哈希、20 类型清单、metadata、脚本、11 种语言、土司双重原子矩阵、新缩略图与 release allowlist 通过。 |
| Open Kaishek | PASS (static) | eu5-1.3.11-build-24187685 profile 对 interaction 与 scripted triggers 均返回 VALIDATED；profile 明确不声明 runtime 语义。 |
| L1 隔离加载 | IN_PROGRESS | 简中 fresh 隔离运行能加载产品和夹具；全场景日志门禁与重载仍待关闭。夹具启动早期出现本地化 key 预载警告，玩家事件 UI 后续显示正确中文；原版市场 law 报错亦随夹具大范围 donor 隔离出现，均不能冒充产品脚本错误或无错误的 L1 GREEN。 |
| L2 玩家行为 | IN_PROGRESS | 原生土司通过真实“附属国行动”完成 14→15；普通直属附庸通过同一真实入口完成 1→4，独立国与 Region 外地点边界保持；9+2 通用类型基线已从真实全局目标选择器关闭。殖民回归、受限类型合法上下文、关系层级和其余禁用路径仍待关闭。 |
| L3 高风险路径 | IN_PROGRESS | 原生直属土司 14→15 成功并通过 owner/数量/关系审计；15→16 真实 UI 禁用且审计证明无部分转让。普通直属附庸正向路径、两个排除边界及真实确认框取消均已关闭；生命周期与保存重载仍待完成。 |
| Workshop 发布 | PASS | 0.2.0 内容、标题、说明、改动说明与白绮主题缩略图已更新；匿名回读、远端原图及空路径 fresh cache 均通过。 |

## L0 证据

- 产品版本：0.2.0；stable ID：xenoamess.colonial_region_transfer。
- EU5：1.3.11 (Pavia)，Steam Build 24187685；eu5.exe SHA-256
  c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef。
- interaction SHA-256：ecc9c26bc2643c8f97714bc075e7489e88e81624e31c0171aef7a0cbe91cff8f。
- scripted triggers SHA-256：
  e5e2b974a67a464f2c7448db2caac4fff722a229572ee2c74ca388e71fcc00cb。
- 35 项 Python 工具测试通过（外置夹具额外 donor 冻结/隔离、精确补集审计、受限类型合法上下文、逐类型矩阵诊断与历史证据策略亦纳入回归）。
- Open Kaishek 聚合测试通过，其中 EU5 profile 5 项测试通过。
- 选择器和效果侧的土司矩阵均为：既有 1..14 个地点时最多接收 14..1 个地点；
  既有 15 个地点没有成功分支。
- 新缩略图：512×512，SHA-256
  ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a。

## 原生土司：已关闭的玩家行为切片

成功 run `xcrt-20260915T191700Z-phase2-tusi-isolated-donors` 使用简中、2560×1440、
EU5 1.3.11 Build 24187685、离线 Steam、独立 userdir，只启用产品及外置夹具；
投影 Mod 树 SHA-256 `fba842fcdd112243bb5c33524ec23e7558616b1e194363284f6e08fec862a8b0`。
`.10` 建立原生 `LNG`→`GYT` 直属土司、泥西首都、14 地点；`.11` 迁走宗主首都并
隔离整个目标 Region 的其他附属树 donor。只读 `.15` 显示双方和平、宗主首都在目标
Region 外、合格候选最多一个；国家面板再次确认 `GYT` 仍为 14 地点原生直属土司。
玩家从梁王国外交面板的管理附属国找到建塘小酋邦，在真正的“附属国行动 → 整合附属地”
确认后，UI 显示 15 地点及候选地点归属 `GYT`；`.12` 只给出“通过：土司14→15且没有裁员”。
`.13` 增加第 16 个候选地点后，该互动按钮变灰并显示“条件未满足”；再次 `.15`
确认其余四项门禁仍为通过，`.14` 只给出“通过：超限时没有转让”，故此禁用可归于
土司 15 地点保护，而不是宗主首都或额外 donor 污染。真实确认操作与只读事件审计
互相独立；本切片没有发现已确认的产品缺陷，夹具修正不进入 Workshop 产品发布包。

关键原始截图 SHA-256（完整截图/输入回执仅需保留至本场景闭合）：`.15` 前置诊断
`0d5e6ad82a76027b352d147198c2a0d36b71a19e204029b58d7942a0047887c2`；
目标原生关系 `aac5b5efd4913edbb74eee48eb20a3bbf2c7d09d4f5d3f543a21a5ec6fb2f76e`；
真实确认后 `1242526a8053e189fe8f6274d9c3efdb29ec0501800945f1797dea80bce23e7e`；
`.12` 成功审计 `2018761810747f24217903d6a492b1d6773c891c2adaddc921172ab72d7f73bf`；
15→16 灰色按钮 tooltip `c311370c1663b611e96ed62a6d92113a3bbcee3c5488d400f96d45fffd73c2fa`；
`.15` 排除其他门禁 `60881aa667aa2b4e30caba2dad1734ec5b3bd860a11480e2a41f722029e587a2`；
`.14` 不转让审计 `a1dc6372c5f96320f62d4f0412d7add8e0596026c7004028b8f23dcd5b31cb78`。
本 run 的 `error.log` SHA-256
`ea164f2d25103a58832fff4e8128ec23fa3c3a7f4becbd197656ebee186e796a`：
03:20:49 的 `xcrt_acceptance.*` 未识别本地化 key 均发生在启动预载，之后事件
实机实际显示中文；03:53 之后 `common/laws/01_common.txt:2022` 的 market unset
错误来自原版 law 链，不来自产品 interaction/trigger，但夹具大范围迁移地点使它复现。
这些日志问题仍列为独立 `fixture/harness` 加载/隔离风险，不把整个 L1 判为 GREEN；
后续新场景需检查是否在不隔离 63 个原生附属国时仍复现。

此前尝试 `xcrt-20260914T230900Z-phase2-tusi-native-actor-capital-outside-r2` 与
`xcrt-20260915T115400Z-phase2-tusi-native-diagnostics` 维持永久 `fixture/harness RED`：
宗主迁都只能解除同 Region 首都门禁；夹具遗漏原生附属树的额外 donor，实际
14→15 仍禁用。前者由后者的 `.15` 多 donor 诊断替代，后者由本 fresh run 的
四项 PASS、14→15 玩家确认及 `.12` 后置审计替代。失败不能改写为 GREEN，
完整失败运行证据仅在本切片闭合前保留。

失败/被替代的土司尝试永久记录如下。哈希均指当时的原始截图；替代结果为上面的
fresh 原生土司 run，不得把任何历史 RED attempt 改写为 GREEN。仅创建 profile
而没有实际输入/业务断言的 `085504Z`、`190500Z` 两个半成品目录不是验收 attempt。

| run ID（前缀 `xcrt-`） | RED 类别和原因 | 关键截图 SHA-256 |
| --- | --- | --- |
| `20260913T212843Z-phase2-acceptance` | `fixture/harness`：法国新建目标不满足土司创建限制；数量 helper 诊断亦不稳定 | `b8e38ea0c04e258e18992cfb54365d40d7969427ce92d0b04e76dcffc30915b3` |
| `20260913T231422Z-phase2-tusi-fixed` | `fixture/harness`：仍用不具备土司合法性的法国目标 | `18c27bd0bd5ddf70668f63c8a260eb6b85994e850e67755649389e15900714b4` |
| `20260914T004551Z-phase2-tusi-explicit` | `fixture/harness`：诊断证实创建对象不是土司，旧 `trigger_if` 产品结论撤回 | `0eed2c49fd9c63df77088cad17e106e0f5d39c3bf05882ef7966265a6c24428c` |
| `20260914T033418Z-phase2-tusi-historical` | `fixture/harness`：把真实 GYT 改挂 CHI 时原生土司关系降级 | `63fe57eaf1f0c3f4a02f559c2d3eedb4f74240d96f09399fbb68003b7f5d03cb` |
| `20260914T065741Z-phase2-tusi-native-relation` | `fixture/harness`：把目标首都移出合法 Region 时关系降级 | `0cf5f68a69d5cb6c850e196f243204ba4d2375a180d8bfcd305a71700c158c1c` |
| `20260914T085818Z-phase2-tusi-native-south-china` | `fixture/harness`：保留原生关系但 14→15 被同 Region 宗主首都保护和额外 donor 混杂 | `e4f88b4d6666eed8a2b6829863d2cbea4c57e83745b7488d5ea0a395561bcc8b` |
| `20260914T184900Z-phase2-tusi-native-actor-capital-outside` | `tool-coverage`：输入法键位下旧字符方式不能稳定启闭游戏控制台，无法完成业务断言；后来 Python 物理 scan code 已补齐 | `161bca4c45b295591c13a3e8873cb7d58f7fbc517432c3b9c39e8979a5f37ffb` |
| `20260914T230900Z-phase2-tusi-native-actor-capital-outside-r2` | `fixture/harness`：宗主迁都后 14→15 仍禁用，原生附属树 donor 未隔离 | `457d707440edf5d733b249dc81d67af42c482248e01f8c84ad7759265202b6bd` |
| `20260915T115400Z-phase2-tusi-native-diagnostics` | `fixture/harness`：`.15` 后置诊断证明整个目标 Region 仍有多个 donor | `bb59f31e299f166637f9942da54c2d6985704e838c07ecf1cbee90da5e2f5085` |

## 普通直属附庸：正向路径与取消路径均已关闭

run `xcrt-20260915T232000Z-phase2-vassal-fresh` 使用同一 exact build、简中、
2560×1440、离线 Steam 与隔离 userdir；投影 Mod 树 SHA-256 仍为
`fba842fcdd112243bb5c33524ec23e7558616b1e194363284f6e08fec862a8b0`。
外置 `.8` 只负责建立确定性前置状态：`XCRTT` 是葡萄牙的普通直属附庸并持有 Tortuga；
直属 donor `XCRTD` 持有 Guahaba 与 Region 外 Porto Santo；其下层附庸 `XCRTS`
持有 Baynoa；独立 `XCRTI` 持有 Iguamuco；葡萄牙持有 Marien。

玩家在真正的外交“附属国行动”中搜索“整合”，目标按钮可用。第一次进入确认框后选择
取消，国家面板仍显示 `XCRTT` 只有 1 个地点；但只读 `.9` 在这个部分满足状态没有形成
可见 fail 选项，因此该次夹具审计不能证明每一个 owner 均未变化。第二次从同一真实入口
确认后，`XCRTT` 面板显示 4 个地点且仍明确是
葡萄牙直属附庸；地图 tooltip 显示 Iguamuco 仍是独立同名国家的首都，Porto Santo
仍属于另一个葡萄牙直属附庸 `XCRTD`，该 donor 仍只有 1 个地点。由此普通附庸正向
1→4、独立国排除和 Region 外排除均通过；没有发现产品缺陷，不需要 0.2.1 或再次发布。

关键截图 SHA-256：取消后目标仍为 1 个地点
`6724a6387e41f90e9f0a582602c4ae350dcaecd08bc089507e8515b48762f38c`；
真实确认后直属目标为 4 个地点
`d457a66e5a6bbd6690862f5d1015558c87795d6899659c86e5f1ed4e63abdd94`；
Iguamuco 独立首都边界
`a83aa0fd5bf4fa79cefee0bd2f9d6d119af2fa7d457001dcd011519bfa001c3f`；
Porto Santo 仍属 1 地点 `XCRTD`
`f33f54c6f6048084c2662664ece1be273fe0638ec4faba37dbe01e5b237d8d1d`。
本 profile 没有在当前启动前清空旧日志：整份 `game.log` / `error.log` SHA-256 分别为
`1dea9fdc4533ede8cab9591499cf1ebfffc35bec899d7bc124e2a9e5adf2d1fe` 与
`c1775623c5c6100be8f88001e294403dd8b81bab2845ebab46c287f84df4a62a`；
检出的 `08:24`–`08:26` fixture 本地化错误早于当前 `10:19` 启动，当前启动段没有新增
可归因于产品 interaction/trigger 的脚本错误。日志未清空与 `.9` 不可见共同分类为
`fixture/harness RED`，不能把本 run 用作完整 L1 GREEN，也不能把历史错误嫁接为产品 RED。
`.9` 不可见的关键截图 SHA-256 为
`6043777b7a3086e09317fb56cfd16dfc64d48d6169e6d94e10943c4b7fda5687`；
它由后续 UI/地图边界检查替代了正向后置审计。该 run 的 `.9` 夹具失败永久维持
`fixture/harness RED`，不得因后续成功而改写；完整运行目录只保留到下面的新取消场景闭合。

取消补审计 run `xcrt-20260916T084500Z-phase2-vassal-cancel-audit` 从 fresh profile
重新建立同一状态，投影 Mod 树 SHA-256 为
`29c3028c2cab66179b800774a41e50197d39a5a4c068aee0db79135d1f35ad28`。
新增只读 `.16` 使用 exact-build `NAND` 表达完整条件的精确补集；布置后它只显示 PASS，
玩家随后从真实“管理附属国 → 附属国行动 → 整合附属地”进入确认框并点击取消，第二次
`.16` 仍只显示 PASS。这同时证明 Tortuga、Marien、Guahaba、Baynoa、Iguamuco、
Porto Santo 的 owner，`XCRTT`/`XCRTD`/`XCRTS` 的地点数量，以及直属、下层附属和
独立关系均无变化；取消路径因此 GREEN。

关键截图 SHA-256：操作前 `.16` 精确审计
`38f16de0b364ac64fa03a2417bdb5e6dc138e0e9dcbc680d5545e66fa7e0a4ae`；
真实互动选择页 `9d856bea45dd2cdb6a40765afb27fa37938b6a170bb405e6a3a8ae3fd68f577f`；
确认框取消 `756a7d9235fcfe61bd78051670febf7cb6ed71cf3fe11c8a46faca54911fd932`；
取消后 `.16` 精确审计
`d1c990536b63873724f41acdc23ae302c72c28a3a92ae6ccf7d00f9e7cb62f54`。
本 run 的 `game.log` / `error.log` SHA-256 分别为
`c30a56f62034bf2dc9f741f45e5b2273668a85f877d4c795c68d36e8f6577c36` 与
`7c85ed93b36edf9c41fb2ae8d07fc084c189e44cc6a7b32d654c91ccedc914bd`。
启动首轮事件数据库加载仍报告外置夹具 `xcrt_acceptance.*` 本地化 key 尚未识别，进入
游戏后的事件标题、正文和按钮实际显示正确中文；日志没有命中产品
`xcrt_colonial_region_transfer` key。其余命中为离线 DLC/Workshop、原版重复名称与
原版数据错误，故这些噪声继续分类为 `fixture/harness` 或 `environment`，不冒充产品 RED，
也不据此宣称完整 L1 GREEN。场景已经闭合；失败摘要与上述哈希永久保留，完整运行证据
可按证据策略清理。

## 附属类型矩阵：首轮夹具聚合审计 RED

run `xcrt-20260916T153700Z-phase2-subject-matrix` 使用 fresh 简中隔离 profile、离线
Steam 与投影 Mod 树 SHA-256
`29c3028c2cab66179b800774a41e50197d39a5a4c068aee0db79135d1f35ad28`。
`.20` 完成布置后，`.21` 只显示“失败：至少一个类型未正确创建”。此时尚未进入产品
真实目标列表，且 `.21` 只能聚合判断 20 个夹具对象，不能指出具体失败类型；因此该
attempt 永久分类为 `fixture/harness RED`，不得改写为产品 RED 或后续 GREEN。

聚合 FAIL 截图 SHA-256 为
`7018f2c37ca04c5d6ecd8917cb81fb8502ba2bb4bc901c0ca68716f48ecfea40`；
`game.log` / `error.log` SHA-256 分别为
`3b49a77e0aba9ba12d39912caca338ccb12dcd05a355a744e4ad39bb6d419361` 与
`c1a2fa74383daef4412673b01d33dccc80619550d340e2e9f29f8b0b92526de4`。
后续 fresh run 必须使用新增只读 `.22` 逐类型诊断，再修正夹具并重新开始矩阵；完整
运行目录仅保留到该矩阵诊断/替代场景闭合。

## 附属类型矩阵：逐类型诊断 RED

run `xcrt-20260916T185200Z-phase2-subject-matrix-diagnostics` 使用 fresh 简中隔离 profile、
离线 Steam 与投影 Mod 树 SHA-256
`39e7253ce1d305dd78ccf499947aa02e65b49f8f9a457f37b3c8959f85c5e1c8`。
`.20` 布置后 `.21` 再次显示聚合失败；同一世界状态的只读 `.22` 将失败精确收敛为
`appanage (XMAPP)`、`hanseatic_member (XMHAN)`、
`direct_imperial_free_city (XMDIFC)`、`march (XMMAR)` 与
`tributary (XMTRI)`。这一步尚未打开产品真实目标列表，故该 attempt 永久分类为
`fixture/harness RED`，不是产品 RED。

聚合 FAIL 与逐类型 FAIL 截图 SHA-256 分别为
`818adaead3a118be2daca2d0411044a5d6eb35bd1d031b862adeb373fb38482a` 与
`f58eac57d3a72905e7839f54fbed4c03e67f7a8b2e1272a82f9bc6c64fab3354`；诊断时
`game.log` / `error.log` SHA-256 分别为
`1c071de0846b1537694707b6fb426b6d05ecf1463703a006c6fbad1f94cf022c` 与
`c43e96b679b54dbcd932d3e8bd8dfdf5b916ab819965e1b4035323799a54701d`。
日志另明确报告 tag `XMDIFC` 无法解析，证明该对象未创建；其余四类至少有一项合同不成立。
结合 exact-build 的 `common/subject_types` 定义，这五类均不适合继续使用夹具原有的一步式
创建路径。替代夹具先建立独立 location 国家，再以 `make_subject_of` 建立精确关系；必须
在后续 fresh run 重新验证 `.21` 为 GREEN 后，才进入真实产品目标列表。完整运行目录仅
保留到该矩阵诊断/替代场景闭合。

## 附属类型矩阵：首次替代夹具重试 RED

run `xcrt-20260916T203500Z-phase2-subject-matrix-retry` 使用 fresh 简中隔离 profile、
离线 Steam 与投影 Mod 树 SHA-256
`44b94373ec7b9e4eb25a48a358de6b813734a6e81b50c1002d3b5af1bbb0d596`。
该版本先创建独立 location 国家，再在同一 event option 中以新定义的 `c:XM*` tag
重新取 scope 并调用 `make_subject_of`。`.21` 与 `.22` 仍显示同五类失败；日志在夹具
对应行明确报告动态 tag 尚未注册，随后 `make_subject_of` 得到空 scope。故该 attempt
永久分类为 `fixture/harness RED`，证明失败点是夹具的 option 内 scope 时序，不是产品。

聚合 FAIL 与逐类型 FAIL 截图 SHA-256 分别为
`8451d634f41115f5e7465c16bc406ed1159f24acec3e54e5bcd2be5f988f57a7` 与
`2a84d5291b2919b478e87455703db58ff66d231bb2cd11e20ab8b742f132d2d9`；诊断时
`game.log` / `error.log` SHA-256 分别为
`3e1ceaa150d55d5b682b8ee47767046d6402cf7049c101ef4a1e5f0aa3dd94c8` 与
`6c9eab8fe5145edf07285d720b559088df944d7b5211decf4715a5785845ba29`。
下一版替代夹具把 `make_subject_of` 放回 `create_country_from_location` 所提供的新国家
scope 内执行；仍须以新的 fresh run 重做聚合审计。完整运行目录仅保留到矩阵场景闭合。

## 附属类型矩阵：created-scope 重试 RED

run `xcrt-20260916T215800Z-phase2-subject-matrix-retry2` 使用 fresh 简中隔离 profile、
离线 Steam 与投影 Mod 树 SHA-256
`0347ba171c653a33fea6223ae896eb260cc87d19f2c622df2ec0c83543c56fa7`。
该版已把 `make_subject_of` 放进 `create_country_from_location` 的新国家 scope；创建阶段
不再出现动态 tag 或空 scope 错误，但 `.21` / `.22` 仍指向同五类，且最终日志只对
`XMDIFC` 报告 tag 不存在。故该 attempt 永久分类为 `fixture/harness RED`：四个对象需要
继续区分关系、类型、country_type 与首都，`XMDIFC` 则确认对象生命周期未成立。

聚合 FAIL 与逐类型 FAIL 截图 SHA-256 分别为
`e667c3c4b226ee9821eb810f65b0a5d9c4419bf4c452ee409d60fcc67dda047b` 与
`c1b02f66ca79362b1adace44ffd019f66368eba2086ae09e996dede09f3ce91a`；诊断时
`game.log` / `error.log` SHA-256 分别为
`3413f287e21b30026468c3a8aacdd31d4a33465e5b84fd4d37a6f81eea808ddf` 与
`9903a479b43f9a07ead10eb6da64c126f2ea4d94b6af1766c70c4c13d942b69e`。
本 run 已是 RED；保存上述原始哈希后热加载只读 `.23`–`.28` 完成根因定位：

- `.23` `appanage`、`.24` `hanseatic_member`、`.26` `march`、`.27` `tributary` 均为
  “对象存在、直属关系、country_type=location、首都存在”通过，只有精确附属类型失败；
  对应截图 SHA-256 为
  `49ed0258666079c42a51a4e24c64b2117a05dfda5a6663468b8ba8c9610ae342`、
  `de70ac59d5886ffa3562c0886d8aa9f6eec672ecd77ae45eb1acbbadc3e72907`、
  `98f5d9f9ff1a0d9ae8cd4a333678f809c689f71f78db5fdf4bf71f9d26774a98`、
  `9a0cb4acb9a5ea96396e10884fdb9cb20bc4ef716dae3116d8d3c6ad4f6a274b`。
- `.25` 证明 `XMDIFC` 对象不存在，截图 SHA-256
  `a1ef272d8bdb9d69d782440b0ed57e5f8f63d878d0e0cc76e2ec8074ba564404`。
- `.28` 进一步证明四个幸存关系全部被引擎规范化为普通 `vassal`，截图 SHA-256
  `1f1ec1ac99ef03d5d54e7b954ff9ae38b023432b9d69d86737f236bb6f70f63f`。

exact-build 原版给出了合法替代路径：`FRA -> ALE appanage`、
`HSA -> LUB hanseatic_member`、`TUN -> BTL tributary` 是初始关系；`march` 要求宗主 rank
不低于目标且目标关系未锁定；`direct_imperial_free_city` 必须在 HRE 直属自由市状态下由
皇帝/leader 持有。该阶段方案因此先改为 13+2 通用塞尔维亚基线与五个合法上下文子场景，
而不是继续强造互斥状态；后续 fresh run 暴露的另外四类上下文限制见下一节。任何 GREEN
结论仍必须来自未热改投影的后续 fresh run。

## 附属类型矩阵：13+2 基线拆分验证 RED

run `xcrt-20260917T004000Z-phase2-subject-matrix-baseline` 使用 fresh 简中隔离 profile、
离线 Steam 与投影 Mod 树 SHA-256
`98e922285de9ac09a70c192358ad9efb087a89e68211bff8f499853b4b235e6e`。`.20` 布置后，
`.21` 显示聚合失败；只读 `.22` 仅显示 `samanta`、`maha_samanta`、
`pradhana_maha_samanta` 与 `tusi` 四项失败，其余 9 个 location 类型与两个 building 类型
均满足逐项合同。故该 attempt 永久分类为 `fixture/harness RED`，没有产品 RED 证据。

聚合 FAIL 与逐类型 FAIL 截图 SHA-256 分别为
`092bd1acffb0b4cb0ba4a823a41ba326290591f70c267880dbb0ab25de869875` 与
`9feb548e10585c381334a258892b6945c5949e3c5796f3324b48ae3d879327a5`；关闭进程后的
`game.log` / `error.log` SHA-256 分别为
`20d87141eac6b40511346ea402c2cff5d5d6425b3fae60e7204957beb2a2f162` 与
`25234ae432e8799b85e4c173375bb1822d91781c7ab4b10e5292bbf583779b7d`。
exact-build 定义确认前三类受印度 advance/升级链约束，`tusi` 受中华帝国与目标地域文化
上下文约束。替代方案把塞尔维亚基线收敛为 9+2，以原生 Delhi samanta 链单独覆盖三类，
并复用已经闭合的原生 `LNG`→`GYT tusi` 场景；所有新结论仍必须来自 fresh run。

## 附属类型矩阵：9+2 通用基线 GREEN

run `xcrt-20260917T031000Z-phase2-subject-matrix-baseline-9plus2` 使用 fresh 简中隔离
profile、离线 Steam 与投影 Mod 树 SHA-256
`80bed38eef4fcd3cf80f34be984ff5d3bff52900d7d937b9de0e89e5ccd78893`。
投影中的 Phase 2 fixture 与夹具简中本地化 SHA-256 分别为
`936a41acaedc3330b4519879537bcc997d16bb367ed4bfd0d60d1a3f53901177` 与
`995576b41243f5a7ce1038284837fc4256441f1481691e2312d84ca226093841`。
`.20` 建立九个领土型与两个 building 型直属对象后，`.21` 只显示
“通过：9+2基线夹具状态成立”；该审计截图 SHA-256 为
`0b8e585fb5f26f1f0a60702e0e132651afe3ca16c7eeca9be07d2ea707d3015b`，因此无需调用
仅用于失败诊断的 `.22`。

同帧建立关系后，游戏的国家外交列表尚未刷新；把日期推进到 1337-05-01 后暂停，真实
“打开所有外交行动 → 附属国行动”中的“整合附属地”行显示候选计数 `9`，截图 SHA-256
`2c9ad13fc3d935c8b1a6d9a3dcb6e2e53975b312fa6c942a6cb0387b3d138e5f`。进入真实目标
选择器后，九个可用对象全部出现：`secessionists`、`colonial_nation`、`fiefdom`、
`conquistador`、`dominion`、`vassal`、`imperial_free_city`、`uc_bey`、`pronoia`；
`state_bank` 与 `trade_company` 两个 building country 均未出现。选择器截图 SHA-256
`177c2910a0409ca0a7eb4d9192cfa00f22fd2643477799fcc889903f93ae299d`，其 OCR JSON
SHA-256 为 `3d897163bcd0ef9bf910a2668f0ce53e5a44ff6f74c4373f50fa780ac325ec26`；OCR
识别出九个目标名称及“整合附属地”，会话实际同时注册 CUDA 与 CPU provider。

原有 Python 输入工具不能把 EU5 面板稳定滚动到目标行。本轮先补充并回归验证了显式
client/screen 坐标的 `wheel` 与保证异常时释放鼠标键的 `drag`；实机使用 `drag` 成功
进入上述真实选择器。日期刷新与滚动能力均属于 `fixture/harness` / `tool-coverage`
处理，不是产品缺陷。正常退出进程后的 `game.log` / `error.log` SHA-256 分别为
`fe11da624665a7f4c4d3d4d18dc23a192371dcb6f9a7cf1dc851e17178824402` 与
`e1586d022cbe2163f74e6171cb621523be3ee3f2cf2bbd192d7d605268f2df19`；两份日志均未命中
产品 `xcrt_colonial_region_transfer` key。本 9+2 切片已经闭合；失败 attempt 的永久摘要
继续保留，完整运行证据可按仓库证据策略清理。受限类型仍须在各自合法上下文中继续验收，
本节 GREEN 不替代那些尚未执行的场景。

## 原生 appanage：启动语言未预置 RED

run `xcrt-20260917T111000Z-phase2-native-appanage` 使用 fresh 隔离 profile、离线 Steam
与投影 Mod 树 SHA-256
`80bed38eef4fcd3cf80f34be984ff5d3bff52900d7d937b9de0e89e5ccd78893`。
法国开局的只读 `.30` 审计显示原生 `FRA -> ALE appanage` 的直属关系、精确类型、
`country_type = location` 与首都合同全部成立，截图 SHA-256 为
`25b99feb3bc709fe98f2ebbeb5f30d87072bc8077b0d8e56517a529e9740dbc0`。真实
“管理附属国”入口中的“阿朗松伯国”面板列出产品动作“整合附属地”；面板截图与
原始分辨率 OCR JSON SHA-256 分别为
`9c69a28307acf03322a75dd9369ac88c1c76c9634fb318686b5c7ecacb60f466` 与
`7892dd7006a56830662479364c8a99aa8ec29291d2d941d2bd1f123f2edbed36`。悬停提示还显示
当前状态“条件未满足”及“整合条件已经变化；没有转让任何地点”，对应截图与 OCR JSON
SHA-256 分别为
`abc0d3790951a300cb4206b7495bbde1f114430168b390a8c81cd6fa17b84662` 与
`b9e3b483551327fe62a9103137d5c0cdb08f4f795a700a5e68024967ab6cdf43`。这些观察支持
产品类型筛选接纳 `appanage`，但不能覆盖本 run 的夹具门禁失败。

本 run 在首次启动后才通过 UI 把语言切换为 `l_simp_chinese`。因此事件定义初次校验时，
仅提供简中的验收 fixture 本地化尚未加载，fresh `error.log` 记录
`Unknown loc key xcrt_acceptance.*` 及由这些缺键引起的 `custom_tooltip` PostValidate
错误；正常退出后的 `game.log` / `error.log` SHA-256 分别为
`ed1bff327814286c7c9fe9fde50cf2162e280b97369eb7ae0511336bcfdcfd16` 与
`65a94241e4744b367b153ca70fc617ea90103be43ae4c53ca0ec83c2516accca`。该问题属于
`fixture/harness RED`，不是产品 RED；attempt 摘要永久保留。Python 准备器已改为在
启动前为 fresh profile 写入 `System.language = "l_simp_chinese"`，必须用未复用本 run
状态的 fresh retry 关闭场景。

## 原生 appanage：简中预置 fresh retry GREEN

run `xcrt-20260917T191500Z-phase2-native-appanage-retry` 使用全新隔离 profile、离线 Steam
与投影 Mod 树 SHA-256
`80bed38eef4fcd3cf80f34be984ff5d3bff52900d7d937b9de0e89e5ccd78893`。准备器在首次启动前
写入 `System.language = "l_simp_chinese"`；`pdx_settings.json` SHA-256 为
`89d64b7e8ece79d66ef900971328e6ad560b25203d992f96262abf1f8a92f0d1`。首次语言确认界面已
以简中显示，进入主菜单前后的 fresh 日志均未出现 `Unknown loc key xcrt_acceptance.*`。

法国开局的只读 `.30` 审计只显示“通过：受限附属关系合同成立”，证明原生
`FRA -> ALE appanage` 的直属关系、精确类型、`country_type = location` 与首都合同成立；
截图与原始分辨率 OCR JSON SHA-256 分别为
`9922d6a8d1c8abe7ef6e831fdcba81924b1c1baffc1bde1ec60be2a59ce8a6dd` 与
`acee3b149393e0da496a0d94c849f2817b658677261a2dac62c7168c2b410856`。随后从真实
“管理附属国”入口选择“阿朗松伯国”，同一产品动作面板显示“整合附属地”；截图与
OCR JSON SHA-256 分别为
`16af346145aea943236871ca4a1ce959f519f1ac5e0e9628db4b84201cd371e1` 与
`3957846172898410199eb437165368f84213c86c59249f7861433744b9cea209`。

EU5 经游戏内菜单正常退出。最终 `game.log` / `error.log` SHA-256 分别为
`d4aa4fe4b724e3dc18e43e633e7137028cbbe9fbb3f3fe7978457f5176d9870c` 与
`dbca3f01a6c8ce4ba771edd1063dea06631256300ce1c68d2be2e8690bffa3d5`；`error.log` 未命中
任何 `xcrt` key，`game.log` 仅含两个 fixture 事件文件的正常加载记录。该 fresh retry
将原生 `appanage` 场景关闭为 GREEN；上一 attempt 的 `fixture/harness RED` 摘要永久
保留，完整运行证据可按仓库策略清理。本场景没有发现产品缺陷，因此不触发再次发布。

## 原生 hanseatic_member：GREEN

run `xcrt-20260917T210000Z-phase2-native-hanseatic-member` 使用全新隔离 profile、离线
Steam 与投影 Mod 树 SHA-256
`80bed38eef4fcd3cf80f34be984ff5d3bff52900d7d937b9de0e89e5ccd78893`。准备器在首次启动前
写入 `System.language = "l_simp_chinese"`；`pdx_settings.json` SHA-256 为
`89d64b7e8ece79d66ef900971328e6ad560b25203d992f96262abf1f8a92f0d1`，首次语言确认界面
直接以简中显示。

汉萨开局的只读 `.31` 审计只显示“通过：受限附属关系合同成立”，证明原生
`HSA -> LUB hanseatic_member` 的直属关系、精确类型、`country_type = location` 与首都
合同成立；截图与原始分辨率 OCR JSON SHA-256 分别为
`5fb3aa41b5609bfeac9329024f3ff84d5ceccfe222d48c21df2c6a147fd433a6` 与
`241b2ce26ce8c4618f7e2a780deca04452c6393050669ce07dc3aac0fc3d0408`。随后从真实
“管理附属国”入口选择“吕贝克自由市”，同一产品动作面板显示“整合附属地”；截图与
OCR JSON SHA-256 分别为
`d76f2b1cd9e34e89b215346b5a235be7fc83632b8cb74ca461f1378c4d5b02c5` 与
`75d37f6f3e3b22ecb5ba13e6a98a30720fb0a28f78f4112653b0db8e2893ff22`。

EU5 经游戏内菜单正常退出。最终 `game.log` / `error.log` SHA-256 分别为
`adbe66f08529e32c943d930b820b08f4bb729dbfa884a70f879f855b00cbf1d9` 与
`2c7ea1d746b91f00f5e385de6d0ec87f6ef77230e8c2d35490e001e2a3fda8ab`；`error.log`
没有任何 `xcrt` key 或产品/fixture 路径，现有记录均来自 exact-build 原版与离线后端，
其中包括 `muscovite_succession_war.txt` 的原版脚本错误。本场景关闭为 GREEN，完整运行
证据可按仓库策略清理；没有发现产品缺陷，因此不触发再次发布。

## 原生 tributary：GREEN

run `xcrt-20260917T221000Z-phase2-native-tributary` 使用全新隔离 profile、离线
Steam 与投影 Mod 树 SHA-256
`80bed38eef4fcd3cf80f34be984ff5d3bff52900d7d937b9de0e89e5ccd78893`。准备器在首次启动前
写入 `System.language = "l_simp_chinese"`；`pdx_settings.json` SHA-256 为
`89d64b7e8ece79d66ef900971328e6ad560b25203d992f96262abf1f8a92f0d1`，首次语言确认界面
直接以简中显示。

突尼斯开局的只读 `.32` 审计显示“通过：受限附属关系合同成立”，证明原生
`TUN -> BTL tributary` 的直属关系、精确类型、`country_type = location` 与首都合同
成立；截图与原始分辨率 OCR JSON SHA-256 分别为
`58bae3d0c3db2c3da8d9a7ced4c768c57a4c8c23b0d4f52b3cd88299360f6431` 与
`f035a985debc2702f3c8f4c9b0e608ac46b6923d49c485d000d0fe178b06f3f3`。随后从真实
“管理附属国”入口选择原版简中名称“泰利斯伯国”，并在同一产品动作面板中检索到
“整合附属地”；截图与 OCR JSON SHA-256 分别为
`4a22501aba5a478f808fe06167dbef1fb02b865a8308ad2d7cb786ab93f9fc5c` 与
`958c4ca2de4d4ff466875a49405e0ee57216a4c8babe5722fe99e15e854520d2`。

EU5 经游戏内菜单正常退出。最终 `game.log` / `error.log` SHA-256 分别为
`defbf99cad545c34e9e5fea81b30f9e6300209e121868197822957d8977e815e` 与
`0fe5df6d7ec916503370d4a145fe3398864fbd962468a8da69549aa98a6f779d`；`error.log`
没有任何 `xcrt` key、产品 key 或产品/fixture 路径。现有记录来自 exact-build 原版、
离线后端与验收输入上下文，不构成产品错误。本场景关闭为 GREEN，完整运行证据可按仓库
策略清理；没有发现产品缺陷，因此不触发再次发布。

## 原生 march：聚合审计 RED

run `xcrt-20260917T235500Z-phase2-native-march` 使用 fresh 简中隔离 profile、离线
Steam 与投影 Mod 树 SHA-256
`80bed38eef4fcd3cf80f34be984ff5d3bff52900d7d937b9de0e89e5ccd78893`。塞尔维亚开局执行
`.33` 后，`.34` 显示“失败：受限附属关系合同不成立”；失败截图与原始分辨率 OCR JSON
SHA-256 分别为
`6fd0766152bcf3e8db2b83ac8238a788f49d38527f3c5f511972b79428dddb7c` 与
`75fa19ce42cb3e2dbdf86296a6038a9aac426bfda4b99b5c8bee795f0ecce7a9`。该聚合事件不能区分
setup marker、动态对象、global actor、直属关系、精确 `march`、`country_type`、首都、
county rank 与类型锁定条件，因此本 attempt 永久分类为 `fixture/harness RED`，不能据此
声称产品缺陷。

EU5 经游戏内菜单正常退出。最终 `game.log` / `error.log` SHA-256 分别为
`0bf809325261a7446237bfa2898981a0dff85ead3cbb956048f1b539cefb42a2` 与
`eda66d1f41ea62ca564cb4ea28a0c8f2c1ee2f32b061057a04ea12ca6d521f4b`；`error.log`
没有任何 `xcrt` key 或产品/fixture 路径。工具覆盖已在主仓 commit `494ec61` 增加只读
`.39` 逐条件诊断，并在 Open Kaishek commit `2ea6b56` 同步增加 `country_rank` 与
`subject_type_is_not_locked` 的 EU5 exact-build 语法和测试。旧投影没有 `.39`，必须用
新投影 fresh retry；在 retry 关闭场景前，本 run 的完整证据仍暂存于 `_runtime`。

### march fresh retry：advance 前置条件定位

run `xcrt-20260918T020000Z-phase2-native-march-retry` 使用加入 `.39` 的 fresh 简中隔离
profile、离线 Steam 与投影 Mod 树 SHA-256
`11731dd84bbaf2bb0affe0c5ecc99e454c7c34bee6bfabf77dab935b802a0531`。塞尔维亚开局执行
`.33` 后，`.34` 仍显示“失败：受限附属关系合同不成立”；截图与 OCR JSON SHA-256
分别为 `9b409bd75187211219d6077f1defe52e1e1a1a280039345366f136ce88ce2ec4` 与
`e06287038a24af45305e016c90e2cdc308bb54e7e7f920207a112c139818530c`。

同一 run 随即执行只读 `.39`。顶部证据确认布置标记、动态对象、global actor 与直属关系
均通过，只有精确附属类型失败；截图与 OCR JSON SHA-256 分别为
`643b914782a89b65371daf02aebc4bd08fb59641c4ed819ad395df3de3ff584e` 与
`a1120a14789ca6d79d3bc4c3d21a63b7a90dc6e75ce2f4316115949d18482d93`。滚动后的底部证据
继续确认 `country_type = location`、首都、county rank 与附属类型未锁定全部通过；截图与
OCR JSON SHA-256 分别为
`c66d0a8752067a03cd2a784634f9b8a4075595be3477b95d776dbb6a9c070d83` 与
`726ed5160d1ce959b435deb8a3ac48789fb488f77899e899901fe5a93a4bf420`。

原版 `game/in_game/common/advances/4_choices_dip.txt` 明确由时代 2 advance
`marcher_lords` 提供 `unlock_subject_type = march`。为验证因果而在本 run 追加诊断性控制台
干预：先执行 `research_advance = advance_type:marcher_lords`，再对同一 XMSPM 直属关系
重新请求 `subject_type:march`；随后 `.34` 立即 GREEN。该 GREEN 截图与 OCR JSON
SHA-256 分别为 `a653282d5b5ad22f5b268364b7ed26cf99a451eccce6da5031b9335e16fe79f0` 与
`e2949be2c5f8a8cd555570a7ef717e62766911bdb232f3e74a361732db94df45`。这组干预只证明根因，
不作为 fresh 场景最终 GREEN。

EU5 经游戏内菜单正常退出。最终 `game.log` / `error.log` SHA-256 分别为
`c6f850fb22e84434b6b1c98ae1863641b7cc6c2d28cd6a31d052cd154e782e6c` 与
`5e920f657939e1f7201d0c4a9326b165a3da2ef72c79c7bf965146aaec89e8d7`；`error.log`
没有 `xcrt` key 或产品/fixture 路径。本 attempt 永久分类为 `fixture/harness RED`：夹具遗漏
原版 advance 解锁前置条件，不是产品缺陷。夹具现已在 `.33` 先研究 `marcher_lords`，`.39`
也新增 advance 独立断言；Open Kaishek commit
`10c6beec2171adce96c7c039e8b4a5ebbdd0361d` 同步覆盖 `has_advance` 与
`research_advance`，完整 fixture 为 syntax 0 / semantic 0。修复后的 fresh retry 关闭场景前，
前两次 March run 的完整证据继续暂存于 `_runtime`。

## Workshop 发布证据

- 发布 run：`xcrt-publish-20260914T164500Z-0.2.0`；Workshop item：
  `3800505751`。
- 正式候选绑定 tag `colonial_region_transfer-v0.2.0`，tag commit
  `c6242e76e9e290be334498ade0be0b9b073afa94`；可复现 ZIP 14,789 字节，
  SHA-256 `690344c58a7f5b3b0892d3496bba84db1e3540ff816dd9f04d6c7cabc3d5ec89`。
- 最终 Steam 内容 manifest：`3814704094601715750`。内置 Mod Tools 返回
  `STEAM_ERESULT_1`，Steam workshop log 明确记录内容与预览上传完成结果为 `OK`。
- 匿名 HTTP 页面回读标题为“献给白绮的附属地整合”，说明正文包含新的通用附属地合同；
  登录页面最新改动说明于 2026-09-15 02:07 显示 `[v0.2.0]` 与五项变化。
- 远端预览原图为 737,585 字节；其 SHA-256 与仓库正式缩略图均为
  `ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a`。
- 旧 cache 被可逆移入发布 run 后，Steam 从不存在的 item 路径下载 manifest
  `3814704094601715750`。fresh cache 共 15 个文件、775,745 字节，与上传投影
  逐路径逐 SHA-256 比对，缺失、额外和不一致均为 0；其中
  `.metadata/thumbnail.png` 也与正式缩略图逐字节一致。
- EU5 在 fresh 下载前正常退出；远端与 fresh-cache 门禁关闭后，Steam 于
  2026-09-15 02:46:23 主动 `LogOff()`，连接日志确认不会自动重连，客户端保持离线。

L1–L3 完成后，本报告仍须补充全部场景的 owner/关系/数量真值、存档重载、失败
attempt 与最终分类，方可把整份 0.2.0 验收报告改为全局 GREEN。Workshop 发布通过不替代
尚未完成的产品运行时验收。
