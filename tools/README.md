# 共享工具

本目录放置跨产品基础设施和各产品的薄入口。

约定命名：

- `build_<product_key>_release.py`：精确 allowlist、staging、manifest、可复现 ZIP 与 cache verification。
- `validate_<product_key>_static.py`：产品 metadata、命名空间、本地化、生成器 parity 和业务合同。
- `eu5_acceptance.py`：统一实机入口；提供唯一 run、严格进程/窗口绑定、原始分辨率截图、GPU/CPU OCR、带截图回执的输入和无 shell 启动。默认 OCR 要求 CUDA device 0，detector/classifier/recognizer 任一实际退回 CPU 都会失败闭锁。
- `bootstrap_acceptance_env.py`：创建或更新隔离 `.venv`，安装固定的 CUDA 13/cuDNN 9 ONNX Runtime，再以 `--no-deps` 安装与 CK3 路径一致的 `rapidocr-onnxruntime 1.2.3`，避免 CPU 与 GPU 两个 ONNX Runtime distribution 互相覆盖。
- `gen_<subject>.py`：从单一权威数据生成运行时或展示投影。

共享模块不得内置某个产品的业务数据、Workshop ID 或故事文案。产品没有真实合同前不创建空实现或虚构 CLI。

## 已实现入口

- `validate_colonial_region_transfer_static.py`：检查“献给白绮的殖民领版图整理”的源码、11 种语言本地化、`白绮`/`Vivhite` 命名合同、版本、metadata 门禁和 EU5 Build `24187685` 原版证据哈希；不会把缺失的 Open Kaishek EU5 profile 冒充为语义通过。
- `build_colonial_region_transfer_release.py`：从匹配 `colonial_region_transfer-v<VERSION>` 的 clean HEAD 只投影精确 allowlist，生成 staging、manifest 与确定性 ZIP；`--check` 在两个临时目录中逐字节复建。当前 EU5 Mod Tools 原生 metadata 缺失时明确拒绝构建。
- `eu5_acceptance.py` 与 `eu5_runtime/`：窗口、截图、OCR、输入和结构化证据原语。所有 GUI 输入必须同时指定 JSON 回执与事后截图；回执的声明边界固定为 `input-sent-only`。
- `prune_runtime_evidence.py`：只接受 `_runtime` 下逐项列出的已闭合场景证据，拒绝 glob、根目录和越界路径；用于执行“失败记录永久保留、完整运行证据保留至场景闭合”的清理合同。

定点滚动与拖拽示例（`--space` 默认为 `client`；wheel 省略坐标时兼容旧行为）：

```text
.venv\Scripts\python.exe tools\eu5_acceptance.py wheel --pid 1234 --amount -5 --x 1200 --y 700 --space client --receipt receipt.json --screenshot after.png
.venv\Scripts\python.exe tools\eu5_acceptance.py drag --pid 1234 --from-x 1500 --from-y 450 --to-x 1500 --to-y 900 --space client --duration 0.8 --receipt receipt.json --screenshot after.png
```

首次建立验收环境：

```text
python tools/bootstrap_acceptance_env.py
```

环境探测和 OCR：

```text
.venv\Scripts\python.exe tools\eu5_acceptance.py probe --provider cuda --output _runtime\cuda-probe.json
.venv\Scripts\python.exe tools\eu5_acceptance.py ocr --image screenshot.png --output ocr.json
.venv\Scripts\python.exe tools\eu5_acceptance.py gpu-evidence --image screenshot.png --output gpu-evidence.json
```

禁止直接安装 `rapidocr-onnxruntime` 的依赖集合，因为它会额外拉入 CPU-only `onnxruntime` 并与 GPU distribution 写入同一模块目录。始终使用 bootstrap 入口。

EU5 安装路径不是产品真值。产品验证器按“显式参数 → `EU5_GAME_ROOT` → 当前 Steam 注册表与 library folders → 仅用于报错展示的旧默认路径”解析，并始终以 exact-build 文件哈希决定是否接受该目录。
