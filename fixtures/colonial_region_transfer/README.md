# 附属地整合验收夹具

本目录只用于一次性隔离实机验收，不属于 Mod 产品，也不得进入 release staging、ZIP 或 Workshop。

`overlay/` 叠加到按 run ID 创建的本地 Mod 树。使用 `tools/prepare_colonial_region_transfer_acceptance.py --write-playset` 同时生成只启用该投影的 ASCII/UTF-8 `playsets.json`；不要通过本地化名称做编码不安全的 shell 文本往返。殖民领、普通附庸与类型矩阵以葡萄牙等首都不在加勒比的国家开局；土司场景必须先用 `tag LNG` 切换为原版 `GYT` 的直属宗主再运行 `.10`。夹具使用当前锁定 EU5 Build `24187685` 的原生 `create_country_from_location`、`create_building_country_in_location`、`make_subject_of`、`set_capital`、`define_unique_country_tag` 和 `change_location_owner` 方言。实机确认 `create_country_from_location` 要求地点已有有效 owner 或调用显式提供 overlord，因此独立对照国也要先把地点临时交给玩家，再从该地点创建国家。

每个主场景必须从全新 1337 开局开始，不能在同一存档重复布置：

- `event xcrt_acceptance.1`：0.1.0 殖民领回归主路径；`.3` 前置审计，`.2` 后置审计。
- `event xcrt_acceptance.8`：普通 `vassal` 目标的同构二期主路径；布置后及真实取消后
  分别用 `.16` 精确审计所有 owner、数量和关系均为初始状态，真实确认后用 `.9`
  审计同构结果。
- `event xcrt_acceptance.20`：建立 13 个可通用构造的领土型与两个 building 型直属附属
  对象；先用
  `.21` 做聚合审计。若 `.21` 失败，必须在同一 run 调用 `.22`；`.22` 只显示未满足
  `直属关系 + 精确 subject type + country_type + capital` 合同的具体类型，禁止仅凭
  聚合 FAIL 猜测产品问题。若 `.22` 仍指向受限类型，`.23`–`.27` 分别把
  `appanage`、`hanseatic_member`、`direct_imperial_free_city`、`march`、
  `tributary` 拆为对象存在、直属关系、精确类型、country_type 与首都子条件；`.28`
  继续确认四个幸存关系是否被引擎规范化为普通 `vassal`。这些事件只保留历史 RED 的
  根因诊断，不再承担最终矩阵。
- 五个受限类型按原版合法上下文分别验收：`.30` 审计法国原生 `ALE appanage`，`.31`
  审计 HSA 原生 `LUB hanseatic_member`，`.32` 审计突尼斯原生 `BTL tributary`；`.33/.34`
  建立并审计显式 county rank 的塞尔维亚 `march`；`.35/.36` 在 HRE 直属自由市状态下
  建立并审计皇帝 `UBV` 的 `direct_imperial_free_city`。每类仍须进入真实产品目标列表。
  Build `24187685` 实机已证明 `appanage`、
  `hanseatic_member`、`direct_imperial_free_city`、`march`、`tributary` 不能可靠地通过
  `create_country_from_location` 的 `overlord + subject_type` 一步式路径建立；这五种类型
  必须先创建独立 location 国家，并在 `create_country_from_location` 的新国家 scope 内以
  `hidden_effect + make_subject_of` 明确建立关系。不得在同一 option 紧接着用新定义的
  `c:XM*` tag 重新取 scope：Build `24187685` 会在 option 完成前把该 tag 视为未注册。
  该差异只属于夹具布置机制，不改变产品的类型 allowlist。
- `tag LNG` 后执行 `event xcrt_acceptance.10`：保持 1337 开局中引擎已建立的原生
  `LNG`→`GYT` 土司关系与 `nixi` 首都，在 `south_china_region` 布置 14→16 禁用；
  此时 `LNG` 首都也在目标 Region，故该负向场景还受到产品既有的宗主首都保护。
  `.11` 移走一个候选，把 `LNG` 首都迁到其 Region 外自有地点 `porto_santo`，并将
  原生附属树在目标 Region 的其他合格 donor 地点隔离给独立对照国 `XCRTI`；
  只在只读诊断 `.15` 确认全 Region 的合格候选确实仅剩一个、双方和平
  后，才能以真实互动验证 14→15；`.12` 审计成功结果；`.13` 再建立 15→16
  禁用，`.14` 审计没有部分转让。`.10` 的按钮同时要求 `GYT` 在布置前确为 `LNG` 的
  三地点直属土司，防止错误国家或重复运行污染证据；不得在该路径调用
  `make_subject_of` 或迁移 `GYT` 首都，因为两者均已由实机证明会使关系降级。
- `event xcrt_acceptance.20`：18 种领土型直属附属国与 `state_bank`/`trade_company` 两种 building 型直属附属对象的候选矩阵；`.21` 审计夹具结构，再从真实互动选择器核对前 18 种出现且后 2 种不出现。

| 地点 | 初始持有者 | 作用 | 互动后的期望 |
| --- | --- | --- | --- |
| `tortuga` | `XCRTT` | 直属殖民领及目标 | 保持 `XCRTT` |
| `marien` | 玩家宗主 | 同 Region 宗主直属地 | 转给 `XCRTT` |
| `guahaba` | `XCRTD` | 直属普通附属国首都 | 转给 `XCRTT` |
| `baynoa` | `XCRTS` | `XCRTD` 的下层附属国唯一地点 | 转给 `XCRTT`；检查 `XCRTS` 生命周期 |
| `iguamuco` | `XCRTI` | 同 Region 体系外国家 | 保持 `XCRTI` |
| `porto_santo` | `XCRTD` | Region 外生命周期对照地点 | 不被互动直接转给 `XCRTT`；记录引擎选择迁都或清理 `XCRTD` 的实际结果 |

土司场景的目标是原版真实标签 `GYT`：其三个云南地点连同 `tortuga` 和十个葡萄牙地点
组成初始 14 地点，首都继续是原版 `nixi`；同属
`south_china_region/dali_area/lijiang_province` 的 `tongan_lijiang` / `linxi` 是两个宗主
候选地点，`iguamuco` 仍为体系外对照，`porto_santo` 是 Region 外宗主对照及 14→15
成功路径使用的临时宗主首都。`.11` 把 `linxi` 交给体系外对照国、把 `LNG` 首都迁至
`porto_santo`；`LNG` 在实机有 63 个附属国，隔离前的只读 `.15` 已明确显示整个
`south_china_region` 还有多个合格候选，不能根据两处手动地点推断仅剩
`tongan_lijiang`。修正后的 `.11` 在迁都之后仅把其他宗主附属树 donor 地点交给
独立 `XCRTI`，显式排除 `GYT` 的全部原有地点及 `tongan_lijiang`；这是为了独立
验收夹具的目标 Region 状态隔离，其他原生 donor 的生命周期不属于本场景验收对象。
`.15` 在玩家国家 `LNG` 的当前状态只读诊断双方战争状态、首都 Region 和整个附属树
的候选数量；新 run 若仍发现多个 donor，该场景保持 `fixture/harness RED`，
不得执行成功路径或把通用 tooltip 归咎于产品。
`.13` 仅在成功后把 `linxi` 交还宗主以建立 15→16 禁用。

上述五个加勒比地点都属于原版 `caribbean_region/hispaniola_area/marien_province`；`porto_santo` 属于 `macaronesia_region/south_macaronesia_area/madeira_province`。具体定义来自当前 exact build 的 `game/in_game/map_data/definitions.txt`。

殖民回归场景布置后执行 `event xcrt_acceptance.3`，只显示一个由引擎 trigger 判定的“初始状态通过/失败”按钮。通过玩家可见的“整合附属地”互动完成动作后执行 `event xcrt_acceptance.2`；该审计同样只显示一个“通过/失败”按钮，并逐项检查目标 Region 地点 owner、体系边界、Region 外地点未被直接转给目标、下层 donor 消失以及目标附属关系。`XCRTD` 失去首都后的迁都或清理由日志、存档和重载前后状态单独记录，不由夹具强行规定。所有审计事件只观察和呈现状态，不执行产品互动，也不修正结果。

所有多条件审计的失败选项使用当前 exact build 原版脚本已经采用的 `NAND`，表示
“并非全部条件成立”。不得用 `NOT` 直接包住多个并列条件；该写法会要求所有子条件
都不成立，导致部分满足状态下通过与失败选项可能同时不可见。

负向路径使用 `event xcrt_acceptance.4` 将宗主首都移到马里恩，使用 `event xcrt_acceptance.5` 恢复里斯本首都，使用 `event xcrt_acceptance.6` 对体系外对照国开战。若同一进程还要继续主成功路径，可用 `event xcrt_acceptance.7` 仅对该对照战争执行无条件和平。这四个事件只建立或恢复验收前置状态，禁用结果仍必须从真实产品互动界面观察。

国家标签 `XCRT*`、`XM*` 仅存在于验收 overlay。本夹具必须在全新 1337 开局中使用，不支持重复布置。
