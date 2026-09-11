# XenoAmess Europa Universalis V Mods

Europa Universalis V 多 Mod 开发、验收与发布仓库。

本仓库采用“根目录独立产品 + 共享工具链”的结构：每个 `mod_<product_key>/` 都是可独立版本化、构建、验收和发布的 Mod；`docs/`、`tools/`、`tests/`、`fixtures/` 与 `workshop/` 提供跨产品共用能力。

当前状态：仓库基础设施已建立，尚未创建第一个正式 Mod 产品。产品需求确定后，先按 [产品合同模板](docs/product-contract-template.md) 写出可证伪合同，再创建 EU5 原生 stub 和玩家可见垂直切片。

## 文档入口

- [知识库索引](docs/README.md)
- [多 Mod 仓库结构](docs/repository-architecture.md)
- [开发生命周期](docs/development-lifecycle.md)
- [测试与 OCR 验收](docs/testing-and-acceptance.md)
- [版本与发布](docs/versioning-and-release.md)
- [当前 EU5 exact-build 静态基线](docs/exact-build-baseline.md)
- [产品登记表](docs/products.md)

## 当前边界

- 不启动或占用共享桌面，除非用户明确授权当轮实机操作。
- 当前主要以简体中文 OCR、日志和存档进行 EU5 实机验收，不要求 MCP。
- CK3/Stellaris 的 Paradox 共性经验只作为研究入口；EU5 方言和 metadata 必须用当前 exact build 重新验证。
