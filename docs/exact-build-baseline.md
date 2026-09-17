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

`C:\workspace\open_kaishek` 已建立锁定 Build `24187685` 的
`eu5-1.3.11-build-24187685` profile。2026-09-17 同步演进加入 `NAND`、战争相关
trigger/effect、递归 iterator、HRE IO scope、`set_country_rank` 与
`lock_current_subject_type` 覆盖；最新工具 commit 为
`4616fd38ba66827150ef80f8e5245250a04442b0`。当前产品脚本与验收 fixture 均为 0 条语法、
0 条语义诊断。工具通过只证明已建模语法/语义合同，
不能替代 EU5 运行时、真实 UI 或存档验证；遇到新方言缺口仍必须标为 tool-coverage 并
同步补充 profile，不能冒充产品 RED。

## 受限附属类型上下文

Build `24187685` 的初始外交关系直接提供：`FRA -> ALE` 为 `appanage`、`HSA -> LUB`
为 `hanseatic_member`、`TUN -> BTL` 为 `tributary`。HRE 初始 leader/emperor 为 `UBV`，
但 `direct_imperial_free_city` 只有在 HRE 的直属自由市状态生效后才会稳定存在；`march`
的 `visible` 要求宗主 rank 不低于目标且目标关系未锁定。

实机失败夹具进一步证明：在塞尔维亚下无视这些上下文强制创建时，`appanage`、
`hanseatic_member`、`march`、`tributary` 都会被引擎规范化为普通 `vassal`，而
`direct_imperial_free_city` 会被清理。2026-09-17 的后续 fresh run 又证明同一塞尔维亚
矩阵不能创建 `samanta`、`maha_samanta`、`pradhana_maha_samanta` 与 `tusi`。原版定义说明：
`samanta` 要求宗主拥有印度文化的 `samanta_advance`；`maha_samanta` 与
`pradhana_maha_samanta` 的 `creation_visible` 均固定为 `always = no`，只能沿
`samanta`→`maha_samanta`→`pradhana_maha_samanta` 互动链变更；`tusi` 要求中华帝国组织
上下文且目标处于指定亚洲 Region、非中华文化组并满足 rank/政体条件。全类型验收必须按
合法上下文拆分，不能用单一宗主强造 18 类关系。

本结论锁定的原版证据 SHA-256：

| 文件 | SHA-256 |
| --- | --- |
| `game/main_menu/setup/start/12_diplomacy.txt` | `c2b86e760721342a26f15d54629de32feef29d33e081cf0828c570a058d047d3` |
| `game/main_menu/setup/start/15_international_organizations.txt` | `9398a1ec2095580419370969428264e5fdaeb7e114230aff9e66a444e1d01a3e` |
| `game/in_game/common/subject_types/appanage.txt` | `c41c925e4b6f2e953a9417f1ff83cfdc5e64b385691dcc81c9fb7288e4e5b86d` |
| `game/in_game/common/subject_types/hanseatic_member.txt` | `695904645cc6aa46b98a4b572e7cc8e2c359daadf4beec690eb45680d57799aa` |
| `game/in_game/common/subject_types/march.txt` | `ad6c5b7869c067b5a2a07961a0f3ee2a7210b5aa43619e871211f87a936fd40a` |
| `game/in_game/common/subject_types/hre.txt` | `502fc5b1f3769d47587a0294e55c3ce7335f6899ccd086c1c9698562004c041a` |
| `game/in_game/common/scripted_effects/international_organization_effects.txt` | `66defd13b110b76df72772de58e9010e0030bf0a326dd0d90e4c46d5f5523dce` |
| `game/in_game/common/subject_types/samanta.txt` | `d193f854d6d558a007b452ab8041f12ddb846332d79761e2e025ef15134dbf1e` |
| `game/in_game/common/subject_types/tusi.txt` | `16f4f8237176d083949a90b67de18e0cb95b0c815cfd5724bf7f5b8a51f26d73` |
| `game/in_game/common/advances/culture_indian.txt` | `b4734b1514a87e3642ba71a2277259eac2a167c25acbe5bb7505c4a877bfdf8f` |
| `game/in_game/common/scripted_triggers/country_triggers.txt` | `cd1ef44fe2e2ff72445b2ec40312fe35eb2129a2bb3d7441ecf9b9817f70a54c` |
| `game/in_game/common/country_interactions/samanta_upgrades.txt` | `382f27f0672ddc89263b34374d0c509679c55d5a121f110702f5179037358020` |

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
