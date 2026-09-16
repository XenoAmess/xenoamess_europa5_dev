# 献给白绮的附属地整合 0.2.0 验收计划

本计划从仓库级
[二期增量合同](../../docs/requirements/colonial-region-transfer-phase-2.md)派生。
没有 fresh 证据的层级保持 NOT_RUN，不得用 0.1.0 的殖民专属结果替 0.2.0 背书。

## L0 静态与 exact-build profile

运行：

    python tools/validate_colonial_region_transfer_static.py --require-metadata --require-open-kaishek
    python -m unittest tests.test_colonial_region_transfer_tools
    mvn -o -pl kaishek-eu5-1311-profile,kaishek-cli -am test
    git diff --check

通过条件：

- VERSION、EU5 Mod Tools metadata、stable ID 与 0.2.0 一致。
- interaction 与 scripted triggers 均为 UTF-8 BOM、括号平衡，11 种语言键完整。
- 源码不含 is_colonial_overlord / is_colonial_subject 入口门禁；候选来自
  actor.every_subject，按 building/pop/army、有效 capital 与直属关系筛选。
- selector、effect 使用同一 xcrt_is_eligible_direct_subject_target 谓词。
- target Region 始终来自 scope:recipient.capital.region。
- 先冻结 xcrt_transfer_locations，效果侧再复核全部硬条件后才改变 owner。
- 土司 1..14 个既有地点与最多可接收数量 14..1 一一对应；选择器 count 与快照
  list_size 矩阵完全一致，15 个地点时没有可执行分支。
- exact build 的 20 个 subject type 清单与 12 项原版/EXE 哈希不漂移。
- Open Kaishek eu5-1.3.11-build-24187685 对两个产品脚本返回 VALIDATED。
- 新缩略图为 512×512，SHA-256
  ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a。
- release allowlist 包含产品 scripted trigger，但不包含 fixture。

## L1 隔离加载

前置硬门禁：用户在当前任务中明确确认屏幕可供本任务占用；任务总线无 EU5/Steam/屏幕
冲突；Steam 在启动游戏时保持离线。

每个 attempt 使用新的 run ID 与全新 userdir/profile，只启用由
prepare_colonial_region_transfer_acceptance.py 合成的产品 + 外置 fixture 投影。记录
Build、EXE SHA、Mod 树 SHA、DLC、播放集、简体中文、2560×1440、UI 缩放、DPI、
启动参数和受保护真实 userdir 前后差异。

fresh error.log 中不得出现归因于 xcrt_、interaction 或 scripted trigger 的错误；尤其
不得有 unknown trigger、wrong scope、坏参数、缺失本地化或未定义消息类型。

## L2 玩家行为

所有产品动作必须从真实“附属国行动 → 整合附属地”界面执行；fixture 只布置/审计状态。

1. 殖民领回归：全新葡萄牙开局执行 event xcrt_acceptance.1，使用 .3 审计前置；
   真实互动选择白绮附属地，先取消一次并核对 owner 不变，再确认执行；用 .2 审计 Region
   内宗主、直属 donor、下层 donor 均转让，体系外与 Region 外不变。
2. 普通附庸主路径：全新开局执行 event xcrt_acceptance.8，以 .16 审计完整初始状态；
   真实互动选择 vassal 目标，先取消并再次以 .16 精确核对 owner、数量和关系不变，
   再确认执行，以 .9 审计同构结果。审计的失败选项必须用 exact-build 原版已采用的
   `NAND` 表达“至少一个条件不成立”，不得使用多子项 `NOT`。
3. 全类型矩阵：全新开局执行 event xcrt_acceptance.20，以 .21 确认夹具建立 18 个
   location 型直属附属和两个 building 型直属附属；在真实目标列表逐项确认 18 种领土型
   目标出现，state_bank 与 trade_company 不出现，列表无坏 capital scope 提示。若 .21
   聚合审计失败，必须在同一状态调用 .22；.22 对每个 tag 分别核对直属关系、精确
   subject type、country_type 与领土型 capital，并只显示失败类型。该诊断只能分类和修复
   fixture/harness，不能代替后续真实目标列表验收。若失败类型受原版
   `subject_creation_enabled` / 创建入口约束，则夹具先建立独立 location 国家，再用
   `make_subject_of` 赋予精确关系；修正后必须从全新 run 重做 `.20` / `.21`，不能复用
   已失败的世界状态。
4. 禁用路径：复用 0.1.0 的战争、同首都 Region、无工作量路径；每项保存简中禁用原因、
   前后 owner 与 fresh 日志。
5. 关系层级：殖民回归场景的 XCRTS 是 XCRTD 的下层附属；它的地点可作为 donor，但
   XCRTS 不得直接出现在宗主的目标列表。

OCR 只证明玩家可见状态；所有权、关系、类型和数量必须由事件 trigger、存档或确定性
机器审计交叉验证。

## L3 土司、生命周期与重载

1. 全新开局执行 event xcrt_acceptance.10：目标土司 14 个地点、同 Region 两个待转让
   地点；真实互动必须因 14→16 显示不可用，两个 donor owner 均不变。
2. 执行 .11 移走一个 donor，真实互动必须允许 14→15；确认后 .12 只显示通过，
   target.num_locations = 15。
3. 执行 .13 增加一个新 donor；15→16 必须不可用，.14 证明 target 仍为 15 且 donor
   未转让。整个过程不得出现部分转让。
4. 殖民回归主路径继续覆盖 donor 最后地点、donor 首都、国家清理、Region 外保护；完成
   后保存并重载，owner、目标关系、生命周期结果保持。

每次失败 attempt 必须按 product、fixture/harness、environment 或 tool-coverage 分类，
并将 run ID、原因、替代结果和关键证据哈希永久写入受 Git 管理的报告；重试必须新建
run。完整运行证据仅保留至对应场景闭合，报告落盘后清理已被替代的完整 run。

## P Workshop 发布验收

- 发布前写 0.2.0 changelog，从 clean、tagged HEAD 构建两次并逐字节复现。
- 更新同一 Workshop item 3800505751；标题、说明、0.2.0 内容与新缩略图作为同一发布
  目标完成，不创建新 item。
- 上传前 Steam 才临时在线；先确认账号未在其他机器游戏。上传完成后立即恢复离线。
- 匿名回读远端标题、说明、更新时间与新预览图；Steam 实际 64 px 渲染仍须可辨白绮人物
  与附属地汇聚主题。
- 从空路径取得 fresh Workshop cache；runtime 文件逐路径/逐 SHA 与 staging 一致；
  cache 的 .metadata/thumbnail.png 必须与选定 512 px 输入逐字节一致。
- 发布后执行必要的简中 fresh-cache 回归并更新
  acceptance-report-0.2.0.md。GitHub Release 不在本轮范围内。
