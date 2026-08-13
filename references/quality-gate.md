# 最终质量门禁

本模块在简历、学习材料、话术和模拟面试完成后执行跨产物一致性检查。它不重写内容，只输出问题、回退模块和最终状态。

## 输入

- `evidence-manifest.json`
- `project-analysis.md`
- `business-chains.md`
- `contribution-map.md`
- `enhancement-plan.md`（如存在）
- `resume.md`
- `claim-grill-report.md`
- `learning-path.md`
- `interview-scripts.md`（如存在）
- `interview-report.md`（如存在）

## 八道门禁

### Gate 1：来源完整性

每条简历 Bullet 必须有 `claim_id`、`source_type`、`role` 和 `chain_id`。缺任一项为 `RED`。

### Gate 2：代码与业务一致性

关键文件必须存在，调用链和技术名词必须与代码分析一致。动态关系允许 `[待确认]`，不允许把推测写成确定事实。

### Gate 3：角色一致性

简历、话术、拷打和模拟面试中的个人角色必须一致。团队成果不得在另一份产物中变成个人主导，除非 manifest 已更新并有依据。

### Gate 4：数字口径

每个数字必须能映射到 evidence。检查环境、样本、前后值、统计口径和是否为估算。无来源且被作为关键结果时为 `RED`。

### Gate 5：抗追问状态

所有核心 Bullet 必须至少为 `YELLOW`。存在 `RED` 时不得标记 `INTERVIEW_READY`；高风险来源需要满足 `claim-policy.md` 的额外门禁。

### Gate 6：学习闭环

所有 `RED/ORANGE/YELLOW` 薄弱点必须在学习路径或增强计划中有明确任务、参考位置和达标标准。

### Gate 7：跨产物一致性

检查简历、15 秒、30 秒、2 分钟话术和面试回答是否使用同一背景、角色、方案和结果。

### Gate 8：敏感信息与表达

检查密钥、token、密码、内部地址、真实客户敏感数据和不应公开的公司信息。检查是否包含用户明确不想公开的内容。

## 状态判定

```text
存在角色/事实冲突或核心 RED -> BLOCKED
存在 ORANGE，或高风险内容未完成门禁 -> TRAINING_REQUIRED
无 RED/ORANGE，但有 YELLOW 或数字待复核 -> REVIEW_REQUIRED
核心声明均 GREEN，跨产物一致，敏感检查通过 -> INTERVIEW_READY
```

用户可以选择带风险继续，但状态不得被静默改为更高等级。

## 报告模板

```markdown
# 最终质量门禁报告

## 总览
- 最终状态：{状态}
- 核心声明：{N}
- GREEN / YELLOW / ORANGE / RED：{数量}
- 高风险来源：{N}
- 未完成增强任务：{N}

## 八道门禁
| Gate | 状态 | 关键发现 | 回退模块 |
|---|---|---|---|
| 来源完整性 | | | contribution-mapper |
| 代码一致性 | | | code-analysis-engine |
| 角色一致性 | | | contribution-mapper |
| 数字口径 | | | star-resume-generator |
| 抗追问 | | | claim-grill |
| 学习闭环 | | | learning-path-generator |
| 跨产物一致性 | | | interview-script-generator |
| 敏感信息 | | | 对应生成模块 |

## 必须修复
1. {问题 -> 具体动作 -> 达标标准}

## 建议修复
1. {问题 -> 具体动作}

## 可直接使用的声明
| Claim | 状态 | 推荐使用场景 |
|---|---|---|

## 下一步
{按状态给出唯一优先动作}
```

## 🔴 CHECKPOINT · FINAL GATE

展示报告并暂停。用户已授权自动完成时：

- `BLOCKED`：自动回退修复一次，再重新检查；
- `TRAINING_REQUIRED`：完成可自动执行的任务，其余保留清单；
- `REVIEW_REQUIRED`：修复格式和一致性问题后重检；
- `INTERVIEW_READY`：完成交付。

不得通过删除报告中的风险来提高最终状态。

## 失败模式

| 触发条件 | 一线修复 | 仍失败则 |
|---|---|---|
| 某产物缺失 | 只检查已有产物并列出缺口 | 状态最高 `REVIEW_REQUIRED` |
| manifest 损坏 | 备份后从现有产物重建索引 | 状态设为 `TRAINING_REQUIRED` |
| 同一 Claim 多个版本冲突 | 以用户最后确认和代码证据重建 | 状态设为 `BLOCKED` |
| 用户要求忽略风险 | 保留内容并记录 override | 不提升状态 |

## 不要做

- 不要只检查单份简历。
- 不要用平均分抵消事实或角色冲突。
- 不要静默修正用户角色。
- 不要把缺失文件当作通过。
- 不要为了给出“通过”结论而删除高风险项。
