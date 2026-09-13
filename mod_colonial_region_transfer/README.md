# 献给白绮的殖民领版图整理

英文名：For Vivhite: Colonial Border Cleanup

Product key：`colonial_region_transfer`

版本：以 `VERSION` 为准

目标游戏：Europa Universalis V，Steam Build `24187685`

二期计划：把同一互动扩展到包含殖民领与非殖民领在内的所有合格直属领土型附属国，并将玩家展示名泛化为“献给白绮的附属地整合”。当前源码、metadata、Workshop 与 `VERSION` 仍是已发布的 `0.1.0`，尚未实现二期；增量合同和分阶段门禁见 [`docs/requirements/colonial-region-transfer-phase-2.md`](../docs/requirements/colonial-region-transfer-phase-2.md)。

宗主可在附属国互动中选择“整理殖民领地区”，把目标殖民领首都所在 Region 内由宗主及其任意层级附属国持有的全部可拥有地点划给目标殖民领。

## 当前状态

P 脚本、11 种语言本地化和当前 EU5 Mod Tools 原生 metadata 已实现。Build `24187685` 的隔离简中实机主路径、存档 owner、重载后审计、无工作量重复执行禁用、OCR、日志归因与真实玩家 userdir 保护均已通过；详见 [`docs/acceptance-report.md`](docs/acceptance-report.md)。

`0.1.0` 已完成主成功路径、战争禁用、宗主首都同 Region 禁用、存档重载、简中 OCR、日志和所有权审计，并已公开发布到 [Steam Workshop item 3800505751](https://steamcommunity.com/sharedfiles/filedetails/?id=3800505751)。三张实机截图已嵌入页面，fresh Workshop cache 与上传投影严格一致。Open Kaishek EU5 profile 缺失继续如实记为独立的 `tool-coverage RED`，不改变已经关闭的产品与发布门禁。

白绮是人名；所有非中文本地化统一写作 `Vivhite`。当前 EU5 build 的 11 种内置语言都提供完整互动本地化；简体中文是唯一实机与 OCR 验收语言。

计划写入 metadata/平台的展示标题：

| 语言 | 展示标题 |
| --- | --- |
| 简体中文 | 献给白绮的殖民领版图整理 |
| English | For Vivhite: Colonial Border Cleanup |
| Português do Brasil | Para Vivhite: Organização das Fronteiras Coloniais |
| Français | Pour Vivhite : Nettoyage des frontières coloniales |
| Deutsch | Für Vivhite: Koloniale Grenzbereinigung |
| 日本語 | Vivhiteに捧げる植民地国境整理 |
| 한국어 | Vivhite를 위한 식민지 국경 정리 |
| Polski | Dla Vivhite: Porządkowanie granic kolonialnych |
| Русский | Для Vivhite: Упорядочение колониальных границ |
| Español | Para Vivhite: Orden de fronteras coloniales |
| Türkçe | Vivhite İçin: Sömürge Sınırı Düzenleme |

静态校验：

```powershell
python tools/validate_colonial_region_transfer_static.py
```

release builder 会拒绝 metadata 缺失、工作树不干净或 HEAD 未绑定精确产品 tag 的构建：

```powershell
python tools/build_colonial_region_transfer_release.py
```

## 行为摘要

- 只允许选择玩家的直属殖民领附属国。
- 目标地理范围固定为该殖民领首都所在 Region。
- 转让宗主及其任意层级附属国在该 Region 内持有的全部可拥有地点。
- 不触碰体系外国家或 Region 外地点。
- 宗主、目标或受影响 donor 处于战争中时禁用。
- 宗主与目标首都在同一 Region 时禁用，避免误转宗主首都区。
- AI 永不主动使用。
- 全量转让包括其他附属国首都，可能导致迁都或国家消失；确认文案会明确警告。

完整合同与验收矩阵见 [`docs/requirements/colonial-region-transfer.md`](../docs/requirements/colonial-region-transfer.md) 和 [`docs/acceptance-plan.md`](docs/acceptance-plan.md)。
