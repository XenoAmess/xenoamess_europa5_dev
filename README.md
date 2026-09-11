# XenoAmess Europa Universalis V Mods

Europa Universalis V 多 Mod 开发、验收与发布仓库。

本仓库采用“根目录独立产品 + 共享工具链”的结构：每个 `mod_<product_key>/` 都是可独立版本化、构建、验收和发布的 Mod；`docs/`、`tools/`、`tests/`、`fixtures/` 与 `workshop/` 提供跨产品共用能力。

当前状态：首个候选产品“献给白绮的殖民领版图整理”已经完成需求合同、源码与静态工具；受“不启动游戏、不占用屏幕”的硬门禁约束，EU5 原生 stub/metadata 与实机验收尚待后续授权。

## 文档入口

- [知识库索引](docs/README.md)
- [多 Mod 仓库结构](docs/repository-architecture.md)
- [开发生命周期](docs/development-lifecycle.md)
- [测试与 OCR 验收](docs/testing-and-acceptance.md)
- [版本与发布](docs/versioning-and-release.md)
- [当前 EU5 exact-build 静态基线](docs/exact-build-baseline.md)
- [产品登记表](docs/products.md)
- [献给白绮的殖民领版图整理](mod_colonial_region_transfer/README.md)

## 当前边界

- 不启动或占用共享桌面，除非用户明确授权当轮实机操作。
- 当前主要以简体中文 OCR、日志和存档进行 EU5 实机验收，不要求 MCP。
- CK3/Stellaris 的 Paradox 共性经验只作为研究入口；EU5 方言和 metadata 必须用当前 exact build 重新验证。
