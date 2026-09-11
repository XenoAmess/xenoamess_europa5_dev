# Europa Universalis V 多 Mod 仓库规划

状态：现行总纲。

## 1. 设计目标

本仓库同时容纳多个可独立发布的 EU5 Mod，并共享 exact-build 研究、静态验证、OCR 驱动、证据保全、构建和 Workshop 发布能力。

核心边界是：产品彼此独立，共用工具但不共用隐式状态；每个产品都能单独构建、单独验收、单独发布和单独维护版本历史。

## 2. 目标目录树

```text
.
├─ AGENTS.md
├─ README.md
├─ CHANGELOG.md                  # 仓库级变化，不代替产品 changelog
├─ docs/
│  ├─ README.md
│  ├─ repository-architecture.md
│  ├─ development-lifecycle.md
│  ├─ testing-and-acceptance.md
│  ├─ versioning-and-release.md
│  ├─ exact-build-baseline.md
│  ├─ products.md
│  ├─ product-contract-template.md
│  └─ release-changelogs/
│     └─ <product_key>/<version>.md
├─ mod_<product_a>/
│  ├─ .metadata/metadata.json    # 由 EU5 当前 build 的 Mod Tools 生成
│  ├─ VERSION                    # 该产品唯一版本源
│  ├─ README.md
│  ├─ docs/
│  │  ├─ acceptance-plan.md
│  │  └─ acceptance-report.md
│  ├─ common/
│  ├─ events/
│  ├─ localization/
│  ├─ gui/                       # 按需
│  ├─ gfx/                       # 按需
│  └─ thumbnail.png              # 按 EU5 实测要求按需加入
├─ mod_<product_b>/
├─ tools/
│  ├─ README.md
│  ├─ build_<product_key>_release.py
│  ├─ validate_<product_key>_static.py
│  └─ eu5_acceptance.py
├─ tests/
│  ├─ README.md
│  └─ test_<product_key>_*.py
├─ fixtures/
│  ├─ README.md
│  └─ <product_key>/
│     ├─ mod-contract.json
│     └─ scenarios.json
├─ workshop/
│  ├─ README.md
│  └─ <product_key>/
│     ├─ description.bbcode
│     └─ media/
├─ _runtime/                     # 本地 run；不入 Git
├─ artifacts/                    # 大型过程证据；默认不入 Git
└─ dist/                         # staging/manifest/ZIP；不入 Git
```

目录按产品实际需要裁剪。没有 GUI 的产品不创建空 `gui/`；没有资产的产品不创建空 `gfx/`。

## 3. 产品身份

每个产品必须拥有：

1. 唯一 `product_key`，用于目录、脚本 key、事件 namespace、本地化、工具和证据前缀。
2. EU5 stable ID，用于依赖和 Mod Tools；创建后不得随展示名称变化。
3. 独立 `VERSION` 与发布 tag。
4. 独立玩家行为合同、兼容范围、验收矩阵和 Workshop item。
5. 独立 release allowlist、manifest 与 fresh-cache 复核记录。

`docs/products.md` 是产品登记表，但不代替各产品 metadata 或版本文件。

## 4. 六层结构

| 层 | 内容 | 约束 |
| --- | --- | --- |
| 产品权威数据 | 数值、稳定 ID、文案 schema、配置 | 同一规则只存在一个权威来源 |
| 生成器 | 重复脚本、本地化、图片或文档投影 | generated 文件禁止手改 |
| EU5 运行时 | common、events、GUI、gfx、localization | 不混入验收专用入口 |
| 验收 | 外置 fixtures、测试定义、日志 marker、OCR runner | 不进入正式 staging |
| 发布投影 | allowlist、staging、manifest、ZIP | 不直接上传开发树 |
| 证据 | report、日志、截图、OCR JSON、存档、hash | append-only；RED 不覆盖 |

## 5. 共享工具边界

- 通用工具负责文件清单、哈希、可复现 ZIP、metadata 基础检查、OCR 原语、隔离 profile 和报告 schema。
- 产品工具只负责该产品的合同、场景、特殊数据生成和发布投影。
- 通用工具不得内置某个 Mod 的标题、剧情、Workshop ID 或业务断言。
- 产品必须显式传入配置，不能依赖“当前目录里恰好只有一个 Mod”。

## 6. 源码与运行身份

以下四种树必须分开：

| 身份 | 用途 | 可否发布 |
| --- | --- | --- |
| 产品源码 | 日常开发和审阅 | 否 |
| 外置 fixture | 到达场景和记录断言 | 否 |
| release staging | builder 生成的生产投影 | 是 |
| Workshop cache | 玩家实际下载内容 | 只用于 P 层复核 |

每次报告必须记录实际加载的是哪一种树及其 SHA-256，不能只写“启用了 Mod”。

## 7. 新产品接入顺序

1. 在 `docs/products.md` 登记 provisional 产品。
2. 按模板写产品合同与非目标。
3. 在可用屏幕窗口中用 EU5 当前 build 生成 stub。
4. 将 stub 原样引入 `mod_<product_key>/`，冻结 metadata schema。
5. 建立产品 `VERSION`、README、验收计划和 release builder 空合同。
6. 完成一条玩家可见垂直切片。
7. 扩展功能并完成与风险相称的 L0–L3。
