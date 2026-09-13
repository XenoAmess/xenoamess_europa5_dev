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

## 二期“白绮关联”缩略图候选

状态：`selected-for-phase-2 / not-published`

日期：2026-09-14。

目标：为“献给白绮的附属地整合”制作新的方形图标候选，在缩略图尺寸同时表达两个不可缺少的主题：白绮的人物形象，以及零散宗主体系领土向一个附属国首都 Region 汇聚的版图整理动作。

人物参考由用户提供：<https://i0.hdslb.com/bfs/face/718c36bc01a173d0c42c0d1131f67e31055244c7.jpg>，本地调查副本 SHA-256 为 `b52b0624a3c2b2114f66a6c7ba839880d1dc89adaa91de0f5ca6bfc302160ca6`。该图片只作为人物身份与造型参考，不进入产品或 Workshop 仓库投影；人物要保留浅冰蓝短发、紫红眼睛、圆形金色眼镜、黑金发饰和深色高领等高识别度特征。用户于 2026-09-14 在当前任务中明确确认拥有参考头像的使用权，并选定本图用于二期正式缩略图替换；本次记录关闭权利确认门禁，但不等于已经执行发布。

设计范围：原创二次元绘制风格的半身头像置于深海军蓝古地图徽章中；黑金发饰的金边自然延展为制图边界线，将数块带酒红色断裂边界的羊皮纸领土碎片汇聚成一个完整、清晰的 Region 轮廓。白绮是第一视觉中心，领土汇聚是第二视觉中心；两者必须在 64 px 预览中仍能辨认。

非目标：不复制参考图背景或姿势，不添加其他人物、文字、字母、旗帜、EU5/Steam 标志、商标或水印；本轮不覆盖仓库中的现有 `icon-512.png`，也不提前改写远端 Workshop。新图只在二期实现、验收、发布授权和平台回读全部成立后成为正式缩略图。

首轮生成提示：

```text
Use case: stylized-concept
Asset type: square game mod icon and Steam Workshop preview candidate
Primary request: create an original polished anime-style grand-strategy game icon that clearly connects Vivhite's character identity with the consolidation of scattered subject territories into one clean regional map
Input images: Image 1 is the identity and character-design reference for Vivhite; preserve her recognizable short pale ice-blue hair, vivid magenta eyes, round antique-gold glasses, black ribbon-like hair ornaments with fine gold edging, dark navy high collar, youthful facial proportions, and calm gentle expression; do not copy the reference background or exact pose
Scene/backdrop: a deep navy circular cartographic medallion with subtle antique parchment-map texture and a soft luminous rim
Subject: a refined head-and-shoulders portrait of Vivhite as the clear focal point; around and behind her, several small ivory parchment territory fragments with broken burgundy borders are drawn together by elegant antique-gold cartographic lines that grow naturally from the gold-edged black hair ribbons and resolve into one coherent Region silhouette
Style/medium: original high-end anime illustration fused with a painted historical strategy-game UI icon; crisp facial features, restrained painterly map texture, strong iconic silhouette, not photorealistic
Composition/framing: centered square composition, character face large and readable, map-consolidation motif clearly visible around the lower and outer thirds, generous safe margin, designed to remain recognizable at 64 px, no tiny edge details
Lighting/mood: dignified, affectionate dedication, calm intelligence, cool soft light on the hair and face, lightly luminous gold boundary accents
Color palette: deep navy, pale ice blue, parchment ivory, antique gold, restrained burgundy, vivid magenta eye accents
Constraints: one character only; preserve the identity-defining features from Image 1; clearly show fragmented territories converging into one unified map region; original artwork; no text, no letters, no flags, no extra people, no UI screenshot, no Europa Universalis or Steam logo, no trademarks, no watermark, no cropped hair ornaments, no frame extending beyond the canvas
Avoid: generic fantasy princess styling, realistic photography, exaggerated cleavage, busy background, illegible miniature map labels, duplicated glasses, extra limbs, distorted hands
```

### 生成结果与首轮审阅

- 生成方式：Codex 内置图像生成工具，以用户提供图片作为人物身份参考。
- 母版：`icon-vivhite-subject-consolidation-v2-source.png`，1254×1254，2,847,562 字节，SHA-256 `1868bdba33f394872f44c5fac78b031e7d6e4e47849452b387e075f573d375c7`。
- 512 px 投影：`icon-vivhite-subject-consolidation-v2-512.png`，737,585 字节，SHA-256 `ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a`。
- 64 px 临时审阅：人物浅冰蓝短发、紫红眼睛、圆眼镜和黑金发饰仍可辨认；外围碎片、金色汇聚线路和底部完整 Region 保持清晰的主次关系；无文字、字母、旗帜、平台标志或水印。
- 完整机器可读记录见 `icon-vivhite-subject-consolidation-v2.manifest.json`。

该图没有覆盖 0.1.0 的 `icon-source.png`、`icon-512.png` 或任何已发布事实。用户已确认画面、参考使用权，并将其选定为二期正式缩略图替换输入；当前状态仍是“已选定、未发布”，由后续明确的二期发布任务更新 metadata/Workshop 并完成平台回读。

## 实机截图

三张功能展示图取自隔离简中 run `xcrt-20260912T044732Z-full-gates-runtime`，均为 `2560x1440` PNG，不含控制台、debug 面板、验收事件弹窗或 `XCRT` 测试标签：

- `game-interaction-zh-cn.png`：展示直属殖民领的互动入口、说明与可执行状态。
- `game-confirmation-zh-cn.png`：展示不可撤销、迁都或国家消失的确认警告。
- `game-result-zh-cn.png`：展示执行后目标地点数由 1 增至 4 的地图结果。

该存档场景由外置验收 fixture 布置，图片只表述为游戏内功能演示，不冒充自然推进存档。逐文件尺寸、字节数和 SHA-256 见 `manifest.json`。
