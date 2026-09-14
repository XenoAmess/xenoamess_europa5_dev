# OCR 后端与算力基线

状态：2026-09-15 已完成当前机器只读诊断；结论只适用于下述 OS、API 和本机依赖状态。

## 目标与范围

目标是确认本仓库既有实机验收所称的 OCR 路径实际使用 CPU 还是 GPU，并记录当前二期验收可以依赖的能力边界。非目标是替换 OCR 后端、实现新的 runner 或重新执行 EU5 实机验收。

## 当前实现状态

- `0.1.0` 验收报告记录的后端是 WinRT `Windows.Media.Ocr.OcrEngine`，识别语言为 `zh-CN`；本次复测由系统解析为 `zh-Hans-CN`。
- 仓库当前没有受 Git 管理的 OCR runner；`tools/README.md` 中的 `eu5_acceptance.py` 是约定名称，文件尚未实现。
- 当前二期 `_runtime/` run 尚未产生受控 OCR JSON。因此“当前项目使用 Windows OCR”是对已完成 `0.1.0` 路径的事实描述，不代表二期已经由可复现 runner 完成 OCR。

## 环境

- OS：Windows 10 Pro `10.0.19045`，64 位。
- OCR 系统 DLL：`C:\Windows\System32\Windows.Media.Ocr.dll`，文件版本 `10.0.19041.7181`。
- GPU：NVIDIA GeForce RTX 4060，驱动 `32.0.15.8180`。
- Python 环境另有 `rapidocr 3.9.2` 与 `onnxruntime 1.29.0`；ONNX Runtime 可用 provider 只有 `AzureExecutionProvider` 和 `CPUExecutionProvider`，没有 CUDA 或 DirectML provider。

## 实测方法与结果

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

当前机器上的既有 `Windows.Media.Ocr` 路径应分类为 **CPU OCR**；本次没有发现 GPU 卸载。当前 Python 环境若直接使用 RapidOCR，也会因 ONNX Runtime 只有 `CPUExecutionProvider` 而使用 CPU。

Microsoft 的 `OcrEngine` API 合同只声明对 `SoftwareBitmap` 执行异步识别，并不承诺具体硬件后端。因此以上结论来自当前机器实测，不外推到其他 Windows build、语言包或未来实现。若 OS、OCR API、模型或 ONNX Runtime provider 改变，必须重新采样后再更新本基线。

## 验收标准

- 后续 runner 必须在报告中记录 OCR API、语言、包/DLL 版本和实际 execution provider。
- 声称 GPU OCR 时，必须同时取得明确的 GPU provider/device 配置与进程级 GPU 活动证据；只安装独显或 DirectML 系统 DLL不算 GPU 已被使用。
- 二期 OCR 在 runner 落地并产生同帧 bbox JSON 前保持未完成，不能用本次后端诊断代替产品 OCR 验收。
