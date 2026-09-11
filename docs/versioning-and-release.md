# 多 Mod 版本、构建与发布规范

## 1. 独立版本

- 每个 `mod_<product_key>/VERSION` 是该产品 SemVer 唯一来源。
- `.metadata/metadata.json` 的产品版本必须与 `VERSION` 一致。
- `supported_game_version` 表达游戏兼容范围，不能拿游戏版本充当 Mod 版本。
- 成功公开发布过的版本号不得复用；未产生远端更新的失败重试可以沿用同一候选版本。
- 正式版前使用 `-rc.N`；除非用户明确要求，不把预发布版本公开到 Workshop。

## 2. 产品 tag 与 changelog

- tag 格式为 `<product_key>-v<version>`，避免多个产品的 `v1.0.0` 相互冲突。
- 每次公开发布必须先完成 `docs/release-changelogs/<product_key>/<version>.md`。
- changelog 至少包含上一/当前版本、tag、commit、玩家可见变化、兼容与迁移、已知限制和验收证据。
- Workshop Change Note 从同一 changelog 提炼，必须以 `[v<version>]` 开头，不维护相互矛盾的第二份真源。

## 3. 正式构建

每个产品必须拥有独立 release builder，并满足：

- 精确 runtime allowlist；README、产品设计、fixture、测试入口和过程素材不进入 staging。
- metadata 来自产品源码，但 provider/Workshop 字段允许的远端规范化必须先实测后冻结。
- manifest 记录相对路径、字节数和 SHA-256。
- ZIP 使用固定顺序、固定时间戳和稳定压缩参数。
- `--check` 在临时路径构建两次并证明 manifest 与 ZIP 逐字节一致。
- 正式构建只接受 clean commit 与匹配的产品 tag。

## 4. Workshop 发布闭环

1. 用户明确下达发布指令。
2. fetch + rebase 到最新远端，完成发布级文案、资产和验收。
3. 在 clean commit 上创建产品 tag。
4. 从 tag 生成 staging、manifest、ZIP 和 SHA-256。
5. 屏幕可用且任务总线无冲突时，使用当前 EU5 build 的内置 Mod Tools 上传。
6. 首次发布必须确认创建新物品；更新必须确认目标 stable ID/Workshop item，出现歧义立即停止。
7. 如果出现新的法律协议，停止并等待物品所有者亲自处理。
8. 回读标题、说明、版本、标签、依赖、可见性、预览和 Change Note。
9. 从空路径获取 fresh Workshop cache，按 manifest 严格比较。
10. 对 fresh cache 运行产品要求的简中 L1–L3。
11. 提交发布记录、changelog 和必要的 metadata 回写并 push。
12. 核对远端 Git SHA 后才能宣布发布完成。

创建或更新 GitHub Release、修改 Workshop 可见性以及上传媒体均属于明确发布工作，不从普通代码目标自动推导授权。

## 5. 发布完成定义

- VERSION、metadata、tag、commit、staging、manifest、ZIP 和 hash 可互相回链。
- 要求的 L0–L3 在精确候选上通过。
- Workshop 页面与远端内容正确。
- fresh-cache 严格验证和实机复核通过。
- 产品 changelog 和发布证据已提交并推送。
- 任务总线已广播完成并释放 Git、Steam、EU5 和屏幕资源。
