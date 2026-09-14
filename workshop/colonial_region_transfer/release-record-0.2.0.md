# 献给白绮的附属地整合 0.2.0：Workshop 发布记录

发布日期：2026-09-15

Workshop 页面：<https://steamcommunity.com/sharedfiles/filedetails/?id=3800505751>

发布 run：`xcrt-publish-20260914T164500Z-0.2.0`

## 候选身份

- Stable ID：`xenoamess.colonial_region_transfer`
- 版本：`0.2.0`
- Git tag：`colonial_region_transfer-v0.2.0`
- Tag commit：`c6242e76e9e290be334498ade0be0b9b073afa94`
- ZIP：`colonial_region_transfer-0.2.0.zip`，14,789 字节
- ZIP SHA-256：`690344c58a7f5b3b0892d3496bba84db1e3540ff816dd9f04d6c7cabc3d5ec89`
- Release manifest SHA-256：`4a85355f971a33f29732dbc0d22e87bd48e0bfaefd1ea1de2c4a64d920259c32`

正式 release staging 按产品 allowlist 保持 14 个 runtime 文件。当前 EU5 Mod Tools 要求把
正式缩略图作为上传目录中的 `.metadata/thumbnail.png`，因此 Workshop 上传投影在 staging
之外只增加这一项，共 15 个文件、775,745 字节；没有把平台预览资产误称为普通 runtime
源码或塞进可复现 ZIP。

## 平台结果

- 更新原 Workshop item `3800505751`，未创建第二个产品身份。
- 第一次 0.2.0 内容上传使用纯 release staging，生成 manifest
  `4574515409486675461`；内容成功，但因为 staging 不含
  `.metadata/thumbnail.png`，远端预览仍为旧图。该 attempt 与 manifest 永久保留为已知失败
  记录，不覆盖为 GREEN。
- 依据 0.1.0 的当前-build Steam 日志回溯，第二次从隔离 Workshop 上传投影加入唯一的
  `.metadata/thumbnail.png`，最终内容 manifest 为 `3814704094601715750`。EU5 Mod Tools
  显示未本地化的 `STEAM_ERESULT_1`；Steam 日志明确记录内容 manifest、737,585 字节
  预览文件与整体完成结果均为 `OK`。
- 远端标题为“献给白绮的附属地整合”；说明来自 `description.bbcode`，SHA-256
  `c736a303a9044fe3395bd4604b26f91fc649e9ea06bfecebdfd2f936730d56b7`。
- 最新改动说明于 2026-09-15 02:07 显示 `[v0.2.0]` 与五项玩家变化；仓库真源
  `change-note-0.2.0.txt` 的 SHA-256 为
  `50fff1befb41c5d1e8a799730a7c3f34b7d96fa8b4fdc737d1a1179b21dae013`。
- 匿名 HTTP 页面返回正式新标题与通用附属地说明，并引用二期白绮主题图；页面主预览
  原图重新下载为 737,585 字节，SHA-256
  `ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a`，与仓库正式
  512 px 输入逐字节一致。

## Fresh Workshop cache

发布前已安装的 0.1.0 cache 仍绑定 manifest `2596763729356634813`，其缩略图 SHA-256
为 `8db0837c6e1e7804543a0b80bfe038a4534f882f060ed0fc0c52beadb19b9e8d`。EU5 正常退出后，
该精确 item 路径被验证并可逆移动到发布 run 内，确保下列目标路径此前不存在：

`C:\Program Files (x86)\Steam\steamapps\workshop\content\3450310\3800505751`

Steam 随后下载 manifest `3814704094601715750` 的 15 个 chunks，content log 于
2026-09-15 02:41:06 记录 commit 完成且 scheduler 结果为 `No Error`。新 cache 包含 15 个
文件、775,745 字节；与 Workshop 上传投影逐相对路径、逐文件 SHA-256 比对，缺失 0、
额外 0、不一致 0。`.metadata/thumbnail.png` 的 SHA-256 为
`ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a`，与远端原图和仓库
输入完全一致。

## 收尾与边界

完成远端与 fresh-cache 发布门禁后，Steam 于 2026-09-15 02:46:23 主动 `LogOff()`；
连接日志记录 `not auto reconnecting due to user initiated logoff`，客户端保持离线模式。

本记录只声明 0.2.0 Workshop 发布完成。L1–L3 的剩余简中运行时矩阵仍在继续；发布成功
不能替代尚未关闭的产品行为验收。若后续确认产品缺陷，将使用新的 SemVer、候选、tag、
manifest 与发布 run 修复后再次发布，不复用已经公开的 0.2.0。
