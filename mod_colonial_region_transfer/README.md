# 献给白绮的附属地整合

英文名：For Vivhite: Subject Territory Consolidation

Product key：colonial_region_transfer

版本：以 VERSION 为准

目标游戏：Europa Universalis V 1.3.11 (Pavia)，Steam Build 24187685

宗主可在“附属国行动”中选择任意合格的直属领土型附属国，把该目标首都所在 Region
内由宗主及其任意层级附属国持有的全部可拥有地点，一次性整合给目标。殖民领和非殖民领
使用同一个互动；building、pop、army 型附属对象以及没有有效首都的对象不会进入候选。

## 二期 0.2.0

- 保留公开脚本 key xcrt_cleanup_colonial_region、stable ID
  xenoamess.colonial_region_transfer 与 Workshop item 3800505751。
- 候选从直属附属国按领土能力和有效首都筛选，不维护 18 类型硬编码 allowlist。
- 目标必须直属宗主；更下层附属国仍可作为地点 donor，但不能越级成为目标。
- 土司批量转让使用双重原子门禁：选择器按待转让数量计算最终地点数，效果侧再以冻结列表
  的 list_size 复核；执行后不得超过 15 个地点。
- 效果先冻结 xcrt_transfer_locations，再复核目标、战争、Region、工作量和类型上限，
  任一条件变化时不转让任何地点。
- 11 种内置语言的玩家文案已泛化；简体中文是唯一实机与 OCR 验收语言。
- 0.2.0 的正式 Workshop 缩略图使用白绮人物形象与附属地汇聚主题的新图，旧发布媒体继续
  作为 0.1.0 历史证据保留。

完整增量合同见
[二期需求分析与实施计划](../docs/requirements/colonial-region-transfer-phase-2.md)。

## 行为边界

- 地理范围固定为目标首都所在 Region。
- 转让宗主及其任意层级附属国在该 Region 内持有的全部可拥有地点。
- 不触碰体系外国家或 Region 外地点。
- 宗主、目标或持有待转让地点的 donor 处于战争中时禁用。
- 宗主与目标首都在同一 Region 时禁用，避免误转宗主首都区。
- 无工作量时禁用；取消确认不会改变所有权。
- AI 永不主动使用。
- 转让可能包括其他附属国首都或最后地点，可能引发迁都或国家清理；确认文案明确警告。

## 验收与构建

静态验证：

    python tools/validate_colonial_region_transfer_static.py --require-metadata --require-open-kaishek
    python -m unittest tests.test_colonial_region_transfer_tools

隔离实机计划与历史证据：

- [0.2.0 验收计划](docs/acceptance-plan.md)
- [0.1.0 已发布验收报告](docs/acceptance-report.md)
- [0.2.0 验收报告](docs/acceptance-report-0.2.0.md)

正式 release builder 会拒绝 metadata 缺失、Open Kaishek profile 未通过、工作树不干净
或 HEAD 未绑定精确产品 tag 的构建：

    python tools/build_colonial_region_transfer_release.py

Workshop：[item 3800505751](https://steamcommunity.com/sharedfiles/filedetails/?id=3800505751)
