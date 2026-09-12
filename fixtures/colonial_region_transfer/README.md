# 殖民领版图整理验收夹具

本目录只用于一次性隔离实机验收，不属于 Mod 产品，也不得进入 release staging、ZIP 或 Workshop。

`overlay/` 叠加到按 run ID 创建的本地 Mod 树。使用 `tools/prepare_colonial_region_transfer_acceptance.py --write-playset` 同时生成只启用该投影的 ASCII/UTF-8 `playsets.json`；不要通过本地化名称做 PowerShell 文本往返。玩家以葡萄牙等首都不在加勒比的国家开局后，在调试控制台执行 `event xcrt_acceptance.1`，再点击“布置验收场景”。夹具使用当前锁定 EU5 Build `24187685` 的原生 `create_country_from_location`、`define_unique_country_tag` 和 `change_location_owner` 方言，建立以下确定性状态。实机确认 `create_country_from_location` 要求地点已有有效 owner 或调用显式提供 overlord，因此独立对照国也要先把地点临时交给玩家，再从该地点创建国家。

| 地点 | 初始持有者 | 作用 | 互动后的期望 |
| --- | --- | --- | --- |
| `tortuga` | `XCRTT` | 直属殖民领及目标 | 保持 `XCRTT` |
| `marien` | 玩家宗主 | 同 Region 宗主直属地 | 转给 `XCRTT` |
| `guahaba` | `XCRTD` | 直属普通附属国首都 | 转给 `XCRTT` |
| `baynoa` | `XCRTS` | `XCRTD` 的下层附属国唯一地点 | 转给 `XCRTT`；检查 `XCRTS` 生命周期 |
| `iguamuco` | `XCRTI` | 同 Region 体系外国家 | 保持 `XCRTI` |
| `porto_santo` | `XCRTD` | Region 外生命周期对照地点 | 不被互动直接转给 `XCRTT`；记录引擎选择迁都或清理 `XCRTD` 的实际结果 |

上述五个加勒比地点都属于原版 `caribbean_region/hispaniola_area/marien_province`；`porto_santo` 属于 `macaronesia_region/south_macaronesia_area/madeira_province`。具体定义来自当前 exact build 的 `game/in_game/map_data/definitions.txt`。

布置后执行 `event xcrt_acceptance.3`，只显示一个由引擎 trigger 判定的“初始状态通过/失败”按钮。通过玩家可见的“整理殖民领地区”互动完成动作后执行 `event xcrt_acceptance.2`；该审计同样只显示一个“通过/失败”按钮，并逐项检查目标 Region 地点 owner、体系边界、Region 外地点未被直接转给目标、下层 donor 消失以及目标附属关系。`XCRTD` 失去首都后的迁都或清理由日志、存档和重载前后状态单独记录，不由夹具强行规定。审计事件只观察和呈现状态，不执行产品互动，也不修正结果。

负向路径使用 `event xcrt_acceptance.4` 将宗主首都移到马里恩，使用 `event xcrt_acceptance.5` 恢复里斯本首都，使用 `event xcrt_acceptance.6` 对体系外对照国开战。若同一进程还要继续主成功路径，可用 `event xcrt_acceptance.7` 仅对该对照战争执行无条件和平。这四个事件只建立或恢复验收前置状态，禁用结果仍必须从真实产品互动界面观察。

国家标签 `XCRTT`、`XCRTD`、`XCRTS`、`XCRTI` 仅存在于验收 overlay。本夹具必须在全新 1337 开局中使用，不支持重复布置。
