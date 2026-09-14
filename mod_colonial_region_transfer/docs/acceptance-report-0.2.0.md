# 献给白绮的附属地整合 0.2.0 验收报告

状态：L0_GREEN / L1-L3_IN_PROGRESS / WORKSHOP_PUBLISHED

本报告只记录 0.2.0。0.1.0 的既有实机与发布事实保留在
[acceptance-report.md](acceptance-report.md)，不得混用。

## 当前结论

| 层级 | 状态 | 结论 |
| --- | --- | --- |
| L0 静态合同 | PASS | 12 项 exact-build 哈希、20 类型清单、metadata、脚本、11 种语言、土司双重原子矩阵、新缩略图与 release allowlist 通过。 |
| Open Kaishek | PASS (static) | eu5-1.3.11-build-24187685 profile 对 interaction 与 scripted triggers 均返回 VALIDATED；profile 明确不声明 runtime 语义。 |
| L1 隔离加载 | IN_PROGRESS | 已进入当前 exact build 的隔离简中验收；完整场景矩阵仍未关闭。 |
| L2 玩家行为 | IN_PROGRESS | 已推进到真实 UI 与原生土司场景；殖民回归、普通附庸、18+2 类型矩阵、关系层级和其余禁用路径仍待关闭。 |
| L3 高风险路径 | IN_PROGRESS | 原生土司 14→16 已正确禁用；14→15 当前被宗主首都同 Region 门禁拦截，正在按 fixture/harness 诊断，15→16、生命周期、取消与保存重载仍待完成。 |
| Workshop 发布 | PASS | 0.2.0 内容、标题、说明、改动说明与白绮主题缩略图已更新；匿名回读、远端原图及空路径 fresh cache 均通过。 |

## L0 证据

- 产品版本：0.2.0；stable ID：xenoamess.colonial_region_transfer。
- EU5：1.3.11 (Pavia)，Steam Build 24187685；eu5.exe SHA-256
  c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef。
- interaction SHA-256：ecc9c26bc2643c8f97714bc075e7489e88e81624e31c0171aef7a0cbe91cff8f。
- scripted triggers SHA-256：
  e5e2b974a67a464f2c7448db2caac4fff722a229572ee2c74ca388e71fcc00cb。
- 29 项 Python 工具测试通过。
- Open Kaishek 聚合测试通过，其中 EU5 profile 5 项测试通过。
- 选择器和效果侧的土司矩阵均为：既有 1..14 个地点时最多接收 14..1 个地点；
  既有 15 个地点没有成功分支。
- 新缩略图：512×512，SHA-256
  ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a。

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
