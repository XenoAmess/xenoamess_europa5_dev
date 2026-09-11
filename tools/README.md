# 共享工具

本目录放置跨产品基础设施和各产品的薄入口。

约定命名：

- `build_<product_key>_release.py`：精确 allowlist、staging、manifest、可复现 ZIP 与 cache verification。
- `validate_<product_key>_static.py`：产品 metadata、命名空间、本地化、生成器 parity 和业务合同。
- `eu5_acceptance.py`：经屏幕授权后使用的隔离 profile、截图、OCR、输入、日志/存档收集和报告原语。
- `gen_<subject>.py`：从单一权威数据生成运行时或展示投影。

共享模块不得内置某个产品的业务数据、Workshop ID 或故事文案。产品没有真实合同前不创建空实现或虚构 CLI。
