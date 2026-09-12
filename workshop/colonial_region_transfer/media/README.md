# 媒体来源与图标生成记录

## 图标

- 生成方式：Codex 内置图像生成工具。
- 日期：2026-09-12。
- 用途：Mod 图标与 Steam Workshop 预览候选。
- 内容约束：原创、无文字、无 EU5/Steam 标志、无商标、无水印；古地图上的零散殖民边界汇聚为统一版图，白色绸带表达“献给白绮”的题献意象。

最终生成提示：

```text
Use case: logo-brand
Asset type: square game mod icon and Steam Workshop preview icon
Primary request: an original heraldic cartographic emblem representing scattered colonial territories being consolidated into one clean regional map
Scene/backdrop: deep navy circular field with a subtle antique parchment-map texture
Subject: four small fragmented parchment land shapes and broken burgundy border lines visually converging into one coherent island-region silhouette enclosed by a crisp antique-gold boundary; a restrained white silk ribbon curves behind the map as a dedication motif
Style/medium: polished painted strategy-game UI icon, original design, strong silhouette, period cartography atmosphere without copying any existing game branding
Composition/framing: centered square composition, generous safe margin, readable at 64 px, no tiny details at the edges
Lighting/mood: dignified, precise, calm, lightly luminous gold accents
Color palette: deep navy, parchment ivory, antique gold, restrained burgundy, clean white ribbon
Constraints: no text, no letters, no flags, no people, no UI screenshot, no Europa Universalis or Steam logo, no trademarks, no watermark, no frame extending beyond the canvas
```

`icon-source.png` 为生成母版；`icon-512.png` 是高质量双三次缩放的上传候选。最终上传接受情况由当前 EU5 Mod Tools/Steam 回读确认。

## 实机截图

三张功能展示图取自隔离简中 run `xcrt-20260912T044732Z-full-gates-runtime`，均为 `2560x1440` PNG，不含控制台、debug 面板、验收事件弹窗或 `XCRT` 测试标签：

- `game-interaction-zh-cn.png`：展示直属殖民领的互动入口、说明与可执行状态。
- `game-confirmation-zh-cn.png`：展示不可撤销、迁都或国家消失的确认警告。
- `game-result-zh-cn.png`：展示执行后目标地点数由 1 增至 4 的地图结果。

该存档场景由外置验收 fixture 布置，图片只表述为游戏内功能演示，不冒充自然推进存档。逐文件尺寸、字节数和 SHA-256 见 `manifest.json`。
