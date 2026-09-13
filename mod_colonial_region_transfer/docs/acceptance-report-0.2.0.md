# 献给白绮的附属地整合 0.2.0 验收报告

状态：L0_GREEN / L1-L3_NOT_RUN / WORKSHOP_NOT_PUBLISHED

本报告只记录 0.2.0。0.1.0 的既有实机与发布事实保留在
[acceptance-report.md](acceptance-report.md)，不得混用。

## 当前结论

| 层级 | 状态 | 结论 |
| --- | --- | --- |
| L0 静态合同 | PASS | 12 项 exact-build 哈希、20 类型清单、metadata、脚本、11 种语言、土司双重原子矩阵、新缩略图与 release allowlist 通过。 |
| Open Kaishek | PASS (static) | eu5-1.3.11-build-24187685 profile 对 interaction 与 scripted triggers 均返回 VALIDATED；profile 明确不声明 runtime 语义。 |
| L1 隔离加载 | NOT_RUN | 等待当前任务的屏幕占用确认后启动 EU5。 |
| L2 玩家行为 | NOT_RUN | 殖民回归、普通附庸、18+2 类型矩阵、关系层级和禁用路径尚待实机。 |
| L3 高风险路径 | NOT_RUN | 土司 14→15 / 14→16 / 15→16、生命周期、取消与保存重载尚待实机。 |
| Workshop 发布 | NOT_RUN | 新缩略图、0.2.0 内容、远端回读与 fresh cache 尚未上传。 |

## L0 证据

- 产品版本：0.2.0；stable ID：xenoamess.colonial_region_transfer。
- EU5：1.3.11 (Pavia)，Steam Build 24187685；eu5.exe SHA-256
  c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef。
- interaction SHA-256：ecc9c26bc2643c8f97714bc075e7489e88e81624e31c0171aef7a0cbe91cff8f。
- scripted triggers SHA-256：
  538a1d316313b8eae8013d46b46510d68707046677c56d421c92ae4abe1686cf。
- 13 项 Python 工具测试通过。
- Open Kaishek 聚合测试通过，其中 EU5 profile 5 项测试通过。
- 选择器和效果侧的土司矩阵均为：既有 1..14 个地点时最多接收 14..1 个地点；
  既有 15 个地点没有成功分支。
- 新缩略图：512×512，SHA-256
  ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a。

L1–L3 与发布完成后，本报告必须补充唯一 run ID、投影与日志哈希、OCR、owner/关系/数量
真值、存档重载、失败 attempt、上传回执、匿名页面和 fresh-cache 对照，方可改为 GREEN。
