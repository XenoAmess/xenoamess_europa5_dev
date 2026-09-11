# Metadata 生成门禁

这里有意不提交猜测的 `metadata.json`。

必须在用户明确释放屏幕并授权启动 EU5 后，使用当前 Steam Build `24187685` 的内置 Mod Tools 为 `mod_colonial_region_transfer` 创建 stub，再原样审查并提交生成的 `.metadata/metadata.json`。生成前不得运行 release builder，也不得宣称本目录可以被 EU5 加载。

生成后还必须：

1. 记录稳定 ID、Mod 版本、支持的游戏版本和生成文件 SHA-256；
2. 默认国际化标题使用 `For Vivhite: Colonial Border Cleanup`，简体中文展示标题使用“献给白绮的殖民领版图整理”；
3. 确认 metadata 中的 Mod 版本与 `VERSION` 一致；
4. 更新产品登记表与静态校验器的 schema 断言；
5. 执行隔离加载、fresh 日志和简中 OCR 验收。
