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
| L2 玩家行为 | IN_PROGRESS | 原生土司通过真实“附属国行动”完成 14→15；殖民回归、普通附庸、18+2 类型矩阵、关系层级和其余禁用路径仍待关闭。 |
| L3 高风险路径 | IN_PROGRESS | 原生直属土司 14→15 成功并通过 owner/数量/关系审计；15→16 真实 UI 禁用且审计证明无部分转让。14→16 禁用此前已有实机证据，但初始夹具同时触发宗主首都保护，不能把它单独当作土司数量门禁证明；生命周期、取消与保存重载仍待完成。 |
| Workshop 发布 | PASS | 0.2.0 内容、标题、说明、改动说明与白绮主题缩略图已更新；匿名回读、远端原图及空路径 fresh cache 均通过。 |

## L0 证据

- 产品版本：0.2.0；stable ID：xenoamess.colonial_region_transfer。
- EU5：1.3.11 (Pavia)，Steam Build 24187685；eu5.exe SHA-256
  c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef。
- interaction SHA-256：ecc9c26bc2643c8f97714bc075e7489e88e81624e31c0171aef7a0cbe91cff8f。
- scripted triggers SHA-256：
  e5e2b974a67a464f2c7448db2caac4fff722a229572ee2c74ca388e71fcc00cb。
- 32 项 Python 工具测试通过（外置夹具额外 donor 冻结/隔离与历史证据策略亦纳入回归）。
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
