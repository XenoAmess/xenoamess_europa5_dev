# 共享工具

本目录放置跨产品基础设施和各产品的薄入口。

约定命名：

- `build_<product_key>_release.py`：精确 allowlist、staging、manifest、可复现 ZIP 与 cache verification。
- `validate_<product_key>_static.py`：产品 metadata、命名空间、本地化、生成器 parity 和业务合同。
- `eu5_acceptance.py`：经屏幕授权后使用的隔离 profile、截图、OCR、输入、日志/存档收集和报告原语。
- `gen_<subject>.py`：从单一权威数据生成运行时或展示投影。

共享模块不得内置某个产品的业务数据、Workshop ID 或故事文案。产品没有真实合同前不创建空实现或虚构 CLI。

## 已实现入口

- `validate_colonial_region_transfer_static.py`：检查“献给白绮的殖民领版图整理”的源码、11 种语言本地化、`白绮`/`Vivhite` 命名合同、版本、metadata 门禁和 EU5 Build `24187685` 原版证据哈希；不会把缺失的 Open Kaishek EU5 profile 冒充为语义通过。
- `build_colonial_region_transfer_release.py`：从匹配 `colonial_region_transfer-v<VERSION>` 的 clean HEAD 只投影精确 allowlist，生成 staging、manifest 与确定性 ZIP；`--check` 在两个临时目录中逐字节复建。当前 EU5 Mod Tools 原生 metadata 缺失时明确拒绝构建。

EU5 安装路径不是产品真值。产品验证器按“显式参数 → `EU5_GAME_ROOT` → 当前 Steam 注册表与 library folders → 仅用于报错展示的旧默认路径”解析，并始终以 exact-build 文件哈希决定是否接受该目录。
