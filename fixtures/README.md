# 外置验收夹具

每个产品使用 `fixtures/<product_key>/`，至少维护：

- `mod-contract.json`：稳定 ID、版本、脚本数据、业务后置条件和语言范围。
- `scenarios.json`：L0–L3 场景、执行状态、run ID、证据路径和限制。

夹具可以帮助安全到达场景或暴露内部状态，但不能替代产品真实入口。所有 acceptance-only 文件必须被 release allowlist 排除。
