# 本机 Europa Universalis V 静态基线

状态：静态调查完成；2026-09-12 已获屏幕授权并开始隔离实机验收，运行时事实见下方接管复核和各产品验收报告。

调查日期：2026-09-11。

## Steam 与可执行文件

| 项目 | 值 |
| --- | --- |
| Steam App ID | `3450310` |
| Steam Build ID | `24187685` |
| 安装目录 | `D:\Program Files (x86)\Steam\steamapps\common\Europa Universalis V` |
| 可执行文件 | `binaries\eu5.exe` |
| EXE 大小 | `142660216` bytes |
| EXE SHA-256 | `c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef` |
| `binaries/checksum.txt` | `0d6cd6f7e3dde34d73585d4a51ef54cd` |
| Caesar branch/revision | `develop` / `42f8b31e` |
| Clausewitz branch/revision | `caesar/develop` / `27ae177fab` |

Steam manifest 的本机 `LastPlayed` 为 `0`。调查时不存在 `Documents\Paradox Interactive\Europa Universalis V`，也不存在 `steamapps\workshop\content\3450310`；因此当前不能凭其他 Paradox 游戏猜测用户目录、播放集或缓存结构。

## 数据层级

原版 `game/` 分为：

- `loading_screen/`：启动设置、defines、输入、基础 GUI/本地化和加载资源。
- `main_menu/`：主菜单 common、GUI、Mod 管理、setup 和大部分本地化。
- `in_game/`：玩法 common、events、GUI、gfx、map_data、setup 和测试定义。

Mod 的 VFS 合并和跨层路径行为必须用 EU5 自己生成的 stub 与实际加载日志确认。

## Mod metadata 与内置工具

静态检查 `eu5.exe` 与 `game/main_menu/gui/mod_tools.gui` 已确认：

- canonical metadata 路径为 `.metadata/metadata.json`。
- metadata 涉及 `supported_game_version`、`short_description`、`relationships`、`game_custom_data` 和 `replace_paths` 等字段。
- 主菜单 Mod Tools 提供 `CreateStubMod`、`UploadNewMod` 和 `UploadFromFolder`。
- 创建表单包含名称、稳定 ID、路径、Mod 版本、游戏支持版本、说明和标签。
- UI 建议 stable ID 形如 `mynick.mymod`，用于声明依赖。
- 说明输入上限为 8000 字符。

第一份产品 metadata 必须由当前 build 创建 stub 后原样冻结，不能在未运行工具的情况下补全猜测字段。

## 原版开发资料

- `game/in_game/common` 包含约百种玩法定义目录，如 advances、building_types、character_interactions、country_interactions、missions、on_action、scripted_effects、scripted_guis、scripted_triggers 和 traits。
- 原版提供多份 `.info` 文件，说明 on_action、scripted GUI、script values、traits、game rules 等格式。
- `game/in_game/events/readme.txt` 与实际事件提供 EU5 event 方言样例。
- `game/in_game/common/tests/readme.txt` 说明原生测试定义格式，包括 `year`、`success`、`failure`、`end_year`、`fail_on_end_year` 和受限日志 effect。
- 抽查的 `.txt` 与简体中文 `.yml` 均使用 UTF-8 BOM；正式 validator 应按每类原版文件实测约定检查，不将抽样冒充全目录事实。

## 静态工具边界

`D:\workspace\open_kaishek` 当前有 CK3 1.19.0.6 与 Stellaris 4.4.6 profile，没有 EU5 profile。首个 Mod 的 L0 工作包含建立 exact-build EU5 profile；完成前可以进行文件、编码和合同检查，但不能宣称 EU5 P 语言语义已由该工具验证。

## 实机阶段待补齐或持续复核

1. 无 Mod 简中主菜单的实际版本名、版本号和 checksum。
2. EU5 真实用户目录、日志、settings、playsets 和存档路径。
3. 隔离 userdir/profile 参数是否成立。
4. 内置 Mod Tools 生成的完整 stub 与 metadata schema。
5. 直启和 Steam 启动差异、焦点、DPI、分辨率与 UI 缩放。
6. fresh 日志的 session marker、加载成功与产品错误归因规则。
7. Workshop cache、远端 metadata 规范化和 fresh-cache 下载流程。

## 2026-09-12 接管环境复核

当前执行环境只挂载 `C:`，Steam 实际根目录为 `C:\Program Files (x86)\Steam`，EU5 实际安装目录为 `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis V`。App manifest 仍为 Build ID `24187685`，上述 EXE、checksum 与五项原版依据哈希全部未变。原先记录的 `D:` 路径是上一环境的位置，不是产品身份或 exact-build 依据。

静态验证器应优先接受显式 `--game-root`/`EU5_GAME_ROOT`，否则从当前 Steam 注册表与 `libraryfolders.vdf` 发现安装目录；不得把易变的盘符写成唯一默认值。发现结果仍须通过六项哈希，路径发现本身不证明 exact build。

接管时还发现真实 Documents userdir 已存在，且已有一次无命令行参数、无 Mod 的非隔离运行日志：游戏日志报告 `u26q2/release/1.3.11`、Git `69f9fa5a5`，设置为简体中文、`2560x1440`、DX12。该运行不属于本产品的唯一 run，也没有输入 manifest、保护目录快照或任务总线记录，因此只能作为环境调查事实，不能计入 L1–L3 验收。正式验收仍必须先实测隔离参数，且不得改写该真实 userdir。
