# EU5 Mod 开发与维护生命周期

状态：现行总纲。

## 1. 统一工作循环

```text
定义玩家行为合同
  → 冻结 exact build
  → 查 EU5 原版与 scope
  → 用当前 Mod Tools 建最小 stub
  → 完成一条玩家可见垂直切片
  → 扩展内容并保持单一权威来源
  → L0–L3 分层验收
  → 从 clean commit 构建 release staging
  → 发布并从 fresh Workshop cache 复核
  → 写 changelog、commit、push
```

解析通过、OCR 看见窗口、上传成功分别不能冒充机制、闭环或发布完成。

## 2. 阶段与退出条件

| 阶段 | 产物 | 退出条件 |
| --- | --- | --- |
| 立项 | 产品合同与非目标 | 每项需求都能转成可观察断言 |
| 原版研究 | exact-build 依据与 scope 链 | 不再依赖字段名猜测 |
| 骨架 | EU5 原生 stub、版本、命名空间 | 游戏能识别真实产品身份 |
| 垂直切片 | 第一条正式玩家闭环 | 入口、动作、效果、反馈成立 |
| 扩展 | 功能候选与生成器 | 单一权威来源和边缘合同成立 |
| 验收 | L0–L3 报告 | GREEN 或可复现且分类正确的 RED |
| 发布候选 | tag、staging、manifest、ZIP | 候选可复现且无测试内容 |
| 发布 | Workshop 与 fresh-cache 证据 | 玩家下载字节和行为均正确 |
| 维护 | 新版本与增量 changelog | 兼容与迁移得到处理并已 push |

## 3. 原版优先

每项机制先研究当前安装 build 的：

- 同类型原版 definition、event、interaction、mission、on_action、scripted effect/trigger、GUI。
- 相应 `.info` 文件和 `common/tests` 语法。
- 调用者提供的 root、scope、saved scope 和可能为空的对象。
- 可见、可用、AI、成本、取消和延迟执行路径。
- 同名定义的覆盖/合并规则及 metadata 的 `replace_paths` 行为。
- 本地化、图片和 GUI provider 的真实绑定方式。

只提取最小结构与语义，不整文件复制原版。高风险链写成：

```text
入口 → scope → scope 转换 → trigger/effect → 状态所有者 → 可见后置条件
```

## 4. 垂直切片原则

第一轮只做证明玩法价值所需的最小闭环，并同时覆盖：

- 正常成功。
- 条件不足或不可用。
- 取消且无部分副作用。
- 重复执行或重复点击。
- 保存重载后状态。
- 玩家与 AI 边界。

测试入口可以帮助到达前置状态，但不能替代产品真实入口和真实 effect。

## 5. 状态与兼容

每个机制必须写明：

- 状态属于 country、location、character、estate、international organization、global 或其他对象。
- 创建者、读取者、修改者、清理者和迁移者。
- 对象消失、国家切换、延迟事件、保存重载和版本升级时的行为。
- 旧存档字段不存在时的默认值。
- 稳定 ID、变量和事件 key 的迁移策略。

业务前置条件应同时保护真正 effect；仅把 UI 隐藏不能防止 AI 或其他脚本调用。

## 6. 每个维护目标的交付顺序

```text
读取产品合同和上一公开 changelog
  → 复现问题或写新增断言
  → 查 exact-build 原版
  → 做最小修改
  → 运行相称验证
  → 更新文档和证据
  → git diff/status 检查
  → fetch + rebase
  → commit + push
```

只有 commit 已推到当前跟踪远端后，用户要求的目标才算仓库交付完成。发布到 Workshop、创建 tag 或 GitHub Release 仍需独立的明确发布指令。
