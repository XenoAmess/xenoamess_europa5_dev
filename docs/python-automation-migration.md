# Python 自动化迁移合同

状态：`implemented / screenshot-OCR-live-input parity verified`

日期：2026-09-15

## 目标与范围

本仓库禁止 PowerShell。构建、静态验证、验收 profile、窗口绑定、原始分辨率截图、OCR、鼠标键盘输入、运行证据和发布辅助统一为受版本控制的 Python 实现。迁移后不再保留仓库内或 `_runtime/` 中的 PowerShell 助手，也不通过内联 PowerShell 拼装第二套业务逻辑。

这是自动化边界整改，不是全仓单语言改造。Open Kaishek 等现有 Java 组件、Java 测试和 Java 接口保持 Java；只有原先由临时 PowerShell 承担的本仓库操作改由 Python 承担。

本次设计重点参考 `C:\workspace\ck3_eternal_recurrence` 的 Python 自动化边界：惰性 OCR 引擎、结构化文字框、精确进程与窗口绑定、截图与输入回执、CUDA provider 显式验证和失败闭锁。CK3 的游戏语义、坐标与验收结论不移植到 EU5。

## 设计

- `tools/eu5_acceptance.py` 是统一 CLI；实现环境探测、唯一 run 创建、截图、OCR、点击、悬停、滚轮、按键、粘贴和控制台输入。
- `tools/eu5_runtime/` 保存可测试的窗口、OCR、证据与数据模型；产品专属 fixture 和 Workshop ID 不进入共享模块。
- 所有写入使用唯一 run ID，并生成 JSON 回执、UTC 时间、目标 PID/HWND、坐标空间、截图尺寸与 SHA-256。已有 run 不覆盖。
- GUI 动作必须绑定预期进程的唯一可见顶层窗口并在输入前确认前台；默认坐标为 client-relative。发送输入只证明动作已发出，业务成功仍由同帧 OCR、日志、owner、存档或确定性审计验证。
- OCR 接受原始 PNG 和可选裁剪框，输出与原图同坐标系的 bbox。正常验收默认要求 CUDA device 0，并逐个核对 detector、classifier、recognizer session 的 provider；不允许静默退回 CPU。
- CPU OCR 只用于显式后端诊断，报告中必须记录 `requested_provider`、`available_providers` 与每个 session 的实际 provider。
- Python 依赖固定在 `tools/requirements-acceptance.txt`，由 `tools/bootstrap_acceptance_env.py` 处理 GPU distribution 与 CK3 同款 RapidOCR 的安装顺序；隔离虚拟环境不得进入 Git。

## 非目标

- 本迁移不把 CK3 行为当成 EU5 exact-build 事实。
- 本迁移本身不证明 EU5 已加载 Mod、按钮可见、互动成功或 Workshop 已发布。
- 不在没有当前屏幕授权和共享资源检查的情况下启动或操纵 EU5、Steam 或 Mod Tools。

## 验收标准

1. 仓库和 `_runtime/` 不含 PowerShell 脚本或模块；原 PowerShell 自动化入口均由 `.py` 替代，既有 Java 组件不变。
2. 自动化门禁覆盖禁止扩展名及 Python 对禁止 shell 可执行文件的调用。
3. 单元测试覆盖 OCR bbox 投影、provider 失败闭锁、run 不覆盖、窗口选择和 CLI 参数。
4. `probe` 在当前 Python 环境生成可复核的依赖与 provider JSON；CUDA 不可用时明确 RED，不伪装成 GPU。
5. 在获得屏幕授权后，用 Python 完成一次 EU5 原始分辨率截图、同帧 OCR JSON 和带截图回执的输入，关闭旧助手的实机 parity 门禁。
6. 文档、工具 README、OCR 基线和实际实现一致。

## 场景闭合记录

2026-09-15 后台迁移场景已闭合。按证据保留合同，以下失败记录永久保留，所指完整 `_runtime` JSON 在记录哈希后删除：

| attempt | 分类 | 原因 | 原证据 SHA-256 | 替代证据 |
| --- | --- | --- | --- | --- |
| `python-migration-cuda-engine-probe` | `tool-coverage` | GPU distribution 已枚举 CUDA，但隔离 CUDA/cuDNN DLL 未 preload，三段 session 实际退回 CPU；失败闭锁生效。 | `2860a1961dde734ed3405ab53d04dd1a0bbc502e9751507e52c98c7473f8f054` | `python-migration-final-cuda-probe` |
| `python-migration-gpu-ocr` / `python-migration-cpu-ocr` | `tool-coverage` | RapidOCR 3.9.2 的默认 PP-OCRv6 内嵌中文字符表在本机组合下解析为乱码；bbox 与英文正常但不满足简中合同。 | `54f2d382e532e53f9c1b9835ad3f39cea4fdfda9bfc802e584013c79d4907771` / `eb000c410535a7eceaa93fdbaed90c778f8a717b664fcb10e7ffe1f0460b7644` | `python-migration-ck3-stack-ocr` |
| `python-migration-ck3-stack-probe`、`-2`、`-3` | `tool-coverage` | 首版兼容层没有遍历旧 RapidOCR detector 的 `infer.session`，无法核对 detector provider；均在推理前停止。 | `e3103d2eb85c7e5aacd1ae5ec019f5879ca925f6d956191a780df46c94641289` / `732f7b027e99a9f0aea49479ce7e75a7fc1858f2e15db8d6e20a169f26d7b0ea` / `ae4d9cb43b02ecf55b5426070765a2f25997df4a520a94facd57800190144b7c` | `python-migration-final-cuda-probe` |

最终 provider 探测、简中 OCR 与进程级 GPU 证据的 SHA-256 分别为 `bd8b82bd9b48e3e274c224f087236ed3e31939df5f6e33c948d219115b9f73c1`、`f8f2a0c752f6ec5283f4c7a21115c66c2a1acb61bb81108a08eb1895ce5cab27`、`189ba41cfb7afb9c4e97054d35c9597fed78017e1c4d2f671249a7427b0f98fe`。摘要事实已回写本文件与 OCR 基线；完整 JSON 不作为永久仓库资产。

## 2026-09-16 当前 OCR 执行后端复核

在普通附庸实机场景的 2560×1440 原始截图上连续执行 5 次 OCR。RapidOCR 请求
`cuda`，ONNX Runtime 枚举到 TensorRT、CUDA 与 CPU provider；文字检测、方向分类、
文字识别三个实际 session 的 provider 顺序均为
`CUDAExecutionProvider, CPUExecutionProvider`。因此当前配置是 GPU 优先、CPU 回退，
不是纯 CPU；这也不等于每一个算子都保证运行在 GPU。

OCR 子进程被 NVIDIA 进程采样识别为 `C:\Python314\python.exe`，但本机 WDDM 返回的
进程显存值为 `[N/A]`，无法据此量化显存或 GPU 利用率。5 次推理墙钟 13.199 秒、
CPU 时间 13.906 秒，说明 CPU 仍参与预处理、后处理或 fallback。ONNX Runtime 同时输出
`No registered plugin EP device found` 警告，但三个 session 均明确保留 CUDA 为首选，
本次没有发生静默的纯 CPU 回退。完整证据 SHA-256 为
`f6864f50b2b486bd3080d3339019d971242f9bc7b588ea40fb5ef8ea99cad4ec`；
JSON 仅保留至对应普通附庸场景闭合。
