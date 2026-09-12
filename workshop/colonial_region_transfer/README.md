# 献给白绮的殖民领版图整理：Workshop 发布合同

本目录保存 Workshop 页面与媒体的仓库真源，不进入 Mod runtime ZIP。

## 发布材料

- `description.bbcode`：中英双语商店说明；实机图使用公开仓库的 raw URL，可在首次发布时直接嵌入。
- `media/icon-source.png`：原创图标母版。
- `media/icon-512.png`：上传预览候选；必须在当前 EU5 Mod Tools/Steam 上传流程中实测接受后才能冻结为正式规格。
- `media/game-*.png`：简中实机互动入口、确认警告和执行结果三张功能展示图；来源与哈希见 `media/manifest.json`。

验收 fixture 可以用来构造可复现演示局，但对外截图不得出现 debug 面板、控制台、审计事件或 `XCRT` 测试标签。若场景由 fixture 布置，BBCode 图片说明必须明确写“实机功能演示场景”，不得暗示来自自然推进的普通存档。

## 首次发布顺序

1. 在离线模式完成文案、图标与实机截图审阅。
2. 候选通过验收、commit/tag/build 后，才因上传需要临时切换 Steam 在线。
3. 启动游戏前检查账号是否已在其他机器游戏；若正在游戏，禁止启动或顶号。
4. 先创建非公开 Workshop item，记录 stable item ID；遇到新 EULA 立即停止等待所有者处理。
5. 上传图标，预览并确认 BBCode 中公开仓库托管的三张实机图可以正常显示。
6. 回读标题、说明、标签、版本、图标、媒体和可见性；全部正确后再公开。
7. 上传任务结束后第一时间把 Steam 恢复为离线模式。
8. 从空路径取得 fresh Workshop cache，严格比对 manifest 并完成简中复验。
