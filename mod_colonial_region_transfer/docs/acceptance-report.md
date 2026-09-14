# 献给白绮的殖民领版图整理：实机验收报告

状态：`FULL_ACCEPTANCE_GREEN / WORKSHOP_RELEASED`

本报告记录正式版本 `0.1.0` 的隔离实机结果。原始过程证据在场景闭合前位于被 Git 忽略的 `_runtime/<run-id>/`；闭合后永久保留下述结论、失败记录和 SHA-256，并清理已被替代的完整运行目录。

## 当前结论

| 层级 | 状态 | 结论 |
| --- | --- | --- |
| L0 静态合同 | `PASS_WITH_GATES` | 七项 exact-build 哈希、metadata、脚本、11 种语言、版本与 allowlist 通过；11 项工具测试通过。Open Kaishek EU5 profile 缺失，单列 `tool-coverage RED`。 |
| L1 隔离加载 | `PASS` | 只加载产品与外置验收 overlay；Build/version 匹配，产品归因 script/localization error 为 0。 |
| L2 主成功路径 | `PASS` | 玩家从真实“附属国行动”执行互动；宗主、直属附属国和下层附属国在目标 Region 的地点全部转给目标，体系外与 Region 外对照不被直接转让。 |
| L2 禁用路径 | `PASS` | 无新待转让地点、战争中和宗主首都同 Region 均显示不可用；后两项取得原生可见条件提示。 |
| L3 生命周期/重载 | `PASS` | 下层 donor 失去全部地点；另一 donor 的 Region 外地点未被直接转让。保存、重载和修正后的引擎审计均通过。 |

因此，产品 L1–L3 运行时验收为 GREEN。2026-09-13 用户明确判定证据充分、停止扩展验证并批准立即公开发布；Open Kaishek profile 缺失只作为独立的 `tool-coverage RED` 保留。

## 补充负路径与发布素材 run

- Run ID：`xcrt-20260912T044732Z-full-gates-runtime`
- 宗主首都同 Region：`screenshots/capital-gate-specific-reason.png`，原生红色条件提示可见。
- 战争门禁：`screenshots/war-gate-specific-reason.png`，原生“我们处于和平”等条件提示可见。
- 同一隔离环境重新执行成功路径，目标地点数由 1 变为 4，地图所有权同步改变。
- 已从该 run 整理三张 `2560x1440` 无控制台实机图，分别展示互动入口、确认警告与执行结果；媒体清单记录文件哈希。

## 成功 run

- Run ID：`xcrt-20260912T064111-dev-runtime`
- 游戏：Europa Universalis V `1.3.11 (Pavia)`，Steam Build `24187685`
- EXE SHA-256：`c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef`
- 启动：`eu5.exe -userdir <isolated-profile> -debug_mode`
- 语言与显示：简体中文，`2560x1440`，默认 UI 缩放
- 最终验收投影 SHA-256：`870b0c4ae712c535ae6ac6e4e4d18ae1b4dfdfab0641927c9e70e375a46f9078`
- 产品文件投影 SHA-256：`976c1436f6d763fec83bba4dbda1930f5443f89cb78a5da9fac2090d98746177`

上述两个投影哈希由 run 的最终 manifest 重新计算；夹具后置断言曾在同一进程热修，产品文件未改变。

## 行为与存档结果

目标 `XCRTT` 最终持有 `tortuga`、`baynoa`、`guahaba`、`marien`；直属 donor `XCRTD` 的 Region 外 `porto_santo` 未被互动转给目标；体系外 `XCRTI` 仍持有 `iguamuco`；下层 donor `XCRTS` 不再持有地点。

存档 SHA-256：`7b935a410c92f0650f8ea07c6d3ea8cc8accd0356eb80ce9619d3ad4e8f55413`。机器审计的 8 项 owner 断言全部通过。`XCRTD` 在保存时仍以已转让的 `guahaba` 为首都指针，重载时由引擎清理；这证明“可能迁都或国家消失”必须保持为生命周期警告，不能承诺一定迁都并存活。

## OCR、日志与隔离

- Windows.Media.Ocr `zh-CN` 从 6 张原始 `2560x1440` 截图提取逐词 bbox，15 项关键文案断言全部通过。
- 已识别互动名、效果说明、不可撤销警告、其他属国可能迁都或消失、后置审计“通过：所有后置条件均成立”与重复执行“条件未满足”。
- `error.log` 中产品归因错误为 0。08:38:59 与 08:44:49 的两条错误属于旧夹具对已被引擎清理对象的无效 `owner` 解引用；夹具改为只断言 `porto_santo` 未直接转给目标后，09:51:06 在同一游戏进程重跑审计并通过，之后无新脚本错误。
- 真实玩家 userdir 前后均为 10,590 个文件；新增、删除、大小或时间戳变化均为 0。

关键证据摘要：

| 证据 | SHA-256 |
| --- | --- |
| `evidence/launch.json` | `11121177a2edb01837cc93dbf7e5ac61f3c9618d2be166133559b1a0fafcefa8` |
| `evidence/prepared-mod-manifest-final.json` | `03adb80692f51476f1c194ecb0354d790d2e076ecf6950b00fd27bc34d710787` |
| `evidence/ocr-acceptance.json` | `a0ce0e32773ceb2d1b4885fbf3fb1f271c583e3d0ef04f0dced42303e81ac623` |
| `evidence/save-owner-audit.json` | `bab96ccd591d9eb107d1ea39f2c32c6171600f3e91de6e4b864eea5e6e0029de` |
| `evidence/runtime-log-audit.json` | `b2d1d591e9287933731d56b88da17baeee081526e67d4642c72d3be4d4cedfdb` |
| `evidence/protected-userdir-diff.json` | `2846a63ef73e676f71ff219adfc95369c9298a5baf8ce766c94289710b543c2a` |

## 永久保留的失败记录

| Run ID | 分类 | 原因 | 替代结果 | 关键摘要 SHA-256 |
| --- | --- | --- | --- | --- |
| `xcrt-20260912T014550-dev-runtime` | `fixture/harness RED` | 进程启动后才启用投影。 | `xcrt-20260912T064111-dev-runtime` GREEN | `CA08B36490A1EEB438D4AE439F74AA7D391D4D608D35D001C0532ED34D30148C` (`evidence/report.json`) |
| `xcrt-20260912T043731Z-negative-media-runtime` | `fixture/harness RED` | 准备阶段中止，只留下空的 stdout，产品未启动。 | `xcrt-20260912T044732Z-full-gates-runtime` GREEN | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` (`evidence/prepare-stdout.json`) |
| `xcrt-20260912T043848Z-negative-media-runtime` | `environment RED` | fresh 隔离 profile 打开法律文档页，产品未执行。 | `xcrt-20260912T044732Z-full-gates-runtime` GREEN | `3AEAF33769B61B32CB0E6D4168C00025A624BC668A27C6805701DCC6F5C544CC` (`evidence/attempt-status.json`) |
| `xcrt-20260912T044017-dev-runtime` | `fixture/harness RED` | 播放集 JSON 经错误编码往返后损坏。 | `xcrt-20260912T064111-dev-runtime` GREEN | `CA25290D72988040D9DE155BA2648DAD41B7D4F237A4EFA616C7A409ACA1935D` (`evidence/report.json`) |
| `xcrt-20260912T055849-dev-runtime` | `fixture/harness RED` | 独立国家创建前没有有效地点 owner。 | `xcrt-20260912T064111-dev-runtime` GREEN | `762D896B407CBC8DF31A02AB2A8464CA75D618B4A368B2C8FEAA1789FB33BD63` (`evidence/report.json`) |
| `xcrt-20260912T062234-dev-runtime` | `product RED` | 互动默认消息类型未定义；产品已用原版 `show_message = no` / `show_message_to_target = no` 修复。 | `xcrt-20260912T064111-dev-runtime` GREEN | `8D6B9961DE87EEFB66F4199D585BD73A21B28A3D82CCBA23F126762C24CEB761` (`evidence/report.json`) |

表中的失败记录永久保留，不会用成功 run 覆盖或改写；0.1.0 场景闭合后，已被替代的完整运行目录按仓库保留策略清理。

## 0.1.0 完整运行证据清理

2026-09-15 按更新后的保留策略完成清理：删除 10 个已闭合的 metadata、实机验收与发布工作目录（包括上述失败 run、两个最终 GREEN run 和 `xcrt-publish-20260913T025500`），以及已被报告或正式媒体替代的 Steam 过程截图、失效指针和图像生成临时目录，共释放约 7.28 GiB。该操作不可从 Git 恢复原始 `_runtime/` 文件；本报告、发布记录、关键 SHA-256、Workshop manifest 和仓库内三张正式实机媒体继续永久保留。

二期 `phase2` run 均未删除；土司场景尚未闭合，其完整运行证据继续保留。

## 发布判定

- 产品验证：GREEN，用户已批准发布。
- 发布资产：三张实机功能图、原创图标与 Workshop BBCode 已齐备。
- 工具覆盖：Open Kaishek EU5 profile 缺失，保持 `tool-coverage RED`，不得表述为已通过。
- 平台步骤：Workshop item [`3800505751`](https://steamcommunity.com/sharedfiles/filedetails/?id=3800505751) 已公开；上传内容 manifest `2596763729356634813` 与预览图均获 Steam `OK`。
- 远端回读：匿名页面返回正式标题；三张 BBCode 实机图均正常显示，且从公开 URL 重新下载后的 SHA-256 与仓库源文件一致。
- Fresh cache：订阅后从新路径下载 14 个文件、742,656 字节，与上传投影逐路径逐 SHA-256 比对，差异为 0。
- 环境收尾：EU5 已正常退出；Steam 于 2026-09-13 05:04:09 `LogOff()`，日志确认不会自动重连，客户端保持运行并显示离线模式。
