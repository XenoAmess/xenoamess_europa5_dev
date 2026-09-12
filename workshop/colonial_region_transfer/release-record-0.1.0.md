# 献给白绮的殖民领版图整理 0.1.0：Workshop 发布记录

发布日期：2026-09-13

Workshop 页面：<https://steamcommunity.com/sharedfiles/filedetails/?id=3800505751>

发布 run：`xcrt-publish-20260913T025500`

## 候选身份

- Stable ID：`xenoamess.colonial_region_transfer`
- 版本：`0.1.0`
- Git tag：`colonial_region_transfer-v0.1.0`
- Tag commit：`0e26c1ea12dbde40024db67d135994ac80cf8e56`
- ZIP：`colonial_region_transfer-0.1.0.zip`，12,671 字节
- ZIP SHA-256：`abb055e6dc80c97ce0125657216d5c1a4192e0054c1af7c3b7ed71d237f595fc`
- Release manifest SHA-256：`721a443f0d9cab07f6ef70e53ecf38c51197758e3c277bf5653844e99cfd7d3f`

## 平台结果

- EU5 Build `24187685` 的内置 Mod Tools 创建 item `3800505751`。
- Steam 内容 manifest：`2596763729356634813`。
- 内容上传、512×512 预览图上传与整体完成结果均为 `OK`（上传器显示未本地化的 `STEAM_ERESULT_1`，Steam 日志将该结果明确记录为 `OK`）。
- 页面已从隐藏切换为公开；匿名 HTTP 回读返回正式中文标题，而非 Steam Error 页面。
- 页面标签为 Diplomacy；图标显示正常；BBCode 中的互动入口、确认警告和执行结果三张简中实机图均实际显示。
- 从三个公开 raw URL 重新下载媒体，文件大小与 SHA-256 均与仓库 `media/` 真源一致。

## Fresh Workshop cache

发布后在此前不存在的 item 路径订阅并下载：

`C:\Program Files (x86)\Steam\steamapps\workshop\content\3450310\3800505751`

Steam 日志记录下载 `No Error`。该缓存包含 14 个文件、742,656 字节；与上传投影逐相对路径、逐文件 SHA-256 比对，差异为 0。

## 收尾

完成远端回读与 fresh-cache 比对后，EU5 正常退出。Steam 于 2026-09-13 05:04:09 主动 `LogOff()`，连接日志记录 `not auto reconnecting due to user initiated logoff`；客户端保持运行并显示离线模式。
