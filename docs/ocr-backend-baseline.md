# OCR 后端与算力基线

状态：2026-09-15 已完成历史后端诊断与 Python/CUDA 迁移验证；结论只适用于下述 OS、API、模型和本机依赖状态。

## 目标与范围

目标是确认本仓库既有实机验收所称的 OCR 路径实际使用 CPU 还是 GPU，记录迁移后的权威后端，并给二期验收建立可复现能力边界。历史测量不替代产品实机验收。

## 当前实现状态

- `0.1.0` 验收报告记录的历史后端是 WinRT `Windows.Media.Ocr.OcrEngine`，识别语言为 `zh-CN`；本次复测由系统解析为 `zh-Hans-CN`。
- 当前权威入口是 `tools/eu5_acceptance.py`，后端为 `rapidocr-onnxruntime 1.2.3` + `onnxruntime-gpu 1.29.0`，模型为该 RapidOCR distribution 自带的 PP-OCRv3 中文检测/识别和 PP-OCRv2 方向分类模型。
- 正常验收默认请求 `CUDAExecutionProvider` device 0，并核对三段 session 都以 CUDA 为第一 provider；CPU 只允许显式诊断。
- 已对当前土司 run 的原始 `2560×1440` 截图生成结构化 OCR JSON，中文 `梁王国`、`传统时代`、`游戏已暂停`、`市场`、`政府` 与 `选择选项` 均被正确识别，并保留原图坐标 bbox。

## 环境

- OS：Windows 10 Pro `10.0.19045`，64 位。
- OCR 系统 DLL：`C:\Windows\System32\Windows.Media.Ocr.dll`，文件版本 `10.0.19041.7181`。
- GPU：NVIDIA GeForce RTX 4060 Laptop GPU，驱动 `581.80`，compute capability `8.9`。
- 全局 Python 的历史诊断环境为 `rapidocr 3.9.2` + CPU-only `onnxruntime 1.29.0`。
- 仓库隔离 `.venv` 为 Python `3.14.7`、`rapidocr-onnxruntime 1.2.3`、`onnxruntime-gpu 1.29.0` 和由 pip 固定的 CUDA 13/cuDNN 9 运行库；启动时调用 ONNX Runtime 的 DLL preload，避免 Windows 动态加载器静默退回 CPU。

## 历史 WinRT 实测方法与结果

输入为当前土司 run 的一张原始 `2560×1440` 简中截图。使用 `Windows.Media.Ocr.OcrEngine.RecognizeAsync` 对同一 `SoftwareBitmap` 连续识别 30 次，并同时检查 OCR 宿主进程 CPU 时间、Windows `GPU Engine` 性能计数器和进程模块：

| 指标 | 结果 |
| --- | --- |
| 总识别字符数 | 20,160 |
| 墙钟时间 | 10,149.2 ms |
| OCR 宿主 CPU 时间增量 | 10,531.2 ms |
| CPU 时间 / 墙钟时间 | 1.038，约持续占用一个逻辑核 |
| OCR 宿主 GPU Engine 样本 | 0 |
| OCR/ML/图形相关模块 | 加载 `Windows.Media.Ocr.dll`；未加载 DirectML、D3D、DXGI、CUDA、ONNX 或 Windows ML 模块 |

## 结论与边界

当前机器上的历史 `Windows.Media.Ocr` 路径应分类为 **CPU OCR**；本次没有发现 GPU 卸载。它不再是仓库当前权威 OCR 路径。

当前权威 Python 路径应分类为 **GPU OCR**。实测 provider 列表为 `TensorrtExecutionProvider`、`CUDAExecutionProvider`、`CPUExecutionProvider`；detector、classifier 与 recognizer 的实际 session 顺序均为 `CUDAExecutionProvider` → `CPUExecutionProvider`。一次未 preload CUDA DLL 的诊断确实触发了 CPU 回退并被入口报为 RED；修正 preload 后 provider 探测和原始 EU5 截图识别均通过。

进程级复核对同一原图连续识别 3 次，三次都产生 96 个 span，总墙钟 `9.369 s`，进程 CPU 时间 `11.453 s`。并发调用 `nvidia-smi` 取得 53 个当前 Python PID 的 NVIDIA compute-process 样本；Windows WDDM 对进程显存返回 `[N/A]`，但 PID 注册、三段 CUDA session 与实际推理同时成立，关闭“仅安装 provider、实际没有进入 GPU 进程”的疑点。

RapidOCR 3.9.2 默认 PP-OCRv6 模型在本机 Windows/Python 3.14 下将内嵌中文字符表解析为乱码，因此不作为本仓库中文验收后端。迁移采用 CK3 已使用的 `rapidocr-onnxruntime 1.2.3`；其同图输出恢复正确中文。该问题分类为 `tool-coverage`，不是 Mod 产品缺陷。

Microsoft 的 `OcrEngine` API 合同只声明对 `SoftwareBitmap` 执行异步识别，并不承诺具体硬件后端。因此以上结论来自当前机器实测，不外推到其他 Windows build、语言包或未来实现。若 OS、OCR API、模型或 ONNX Runtime provider 改变，必须重新采样后再更新本基线。

## 验收标准

- runner 必须在报告中记录 OCR API、语言、包/DLL 版本和实际 execution provider。
- 声称 GPU OCR 时，必须同时取得明确的 GPU provider/device 配置与进程级 GPU 活动证据；只安装独显或 DirectML 系统 DLL不算 GPU 已被使用。
- 二期 runner 与同帧 bbox JSON 门禁已关闭；产品互动、owner、日志与重载门禁仍必须由后续实机步骤关闭，不能用 OCR 后端验证代替。
