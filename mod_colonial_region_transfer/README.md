# 献给白绮的殖民领版图整理

英文名：For Vivhite: Colonial Border Cleanup

Product key：`colonial_region_transfer`

版本：以 `VERSION` 为准

目标游戏：Europa Universalis V，Steam Build `24187685`

宗主可在附属国互动中选择“整理殖民领地区”，把目标殖民领首都所在 Region 内由宗主及其任意层级附属国持有的全部可拥有地点划给目标殖民领。

## 当前状态

P 脚本和 11 种语言本地化已经实现。当前目录还不是可加载或可发布的 Mod：用户明确要求不启动游戏、不占用屏幕，因此尚未通过当前 EU5 build 的内置 Mod Tools 生成 `.metadata/metadata.json`。不得从其他 Paradox 游戏或旧版本手写该文件。

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

release builder 会在 metadata 缺失时拒绝构建：

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
