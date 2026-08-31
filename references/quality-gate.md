# 最终质量门禁

本模块在简历、学习材料、话术和模拟面试完成后执行跨产物一致性检查。它不重写内容，只输出问题、回退模块和最终状态。

## 输入

- `DIRECT + QUALITY_CHECK_ONLY`：用户提供或点名的现有简历/材料，只检查该范围并列出未检查项
- `ARTIFACT/FULL_PIPELINE`：`evidence-manifest.json` 与 `current_artifacts` 指向的当前产物

运行门禁前，完整模式要求 `project_analysis`、`business_chains`、`contribution_map`、`resume`、`claim_grill_report`、`learning_path` 和 `interview_scripts`；`enhancement_plan`、`learning_interactive`、`interview_report` 按流程是否执行决定。`UNDERSTAND_ONLY` 只要求 `project_analysis`、`business_chains` 和 `learning_path`。`ARTIFACT/FULL_PIPELINE` 门禁完成后写入新报告并更新 `current_artifacts.quality_gate_report`；`DIRECT` 只在对话中交付范围化发现，不创建报告文件。

`ARTIFACT/FULL_PIPELINE` 中映射缺失、文件不存在或路径越出分析目录时，该产物视为缺失；不要读取同名旧文件兜底。完整检查前必须运行：

```text
python scripts/validate_manifest.py <分析目录>/evidence-manifest.json --analysis-dir <分析目录> --require-artifacts
```

命令失败时将错误写入门禁报告，最终状态不得为 `INTERVIEW_READY`。

## 八道门禁

`UNDERSTAND_ONLY` 使用轻量门禁：只执行 Gate 2 的代码/链路一致性、Gate 6 的学习闭环和 Gate 8 的敏感信息检查，并确认未意外生成简历、拷打和话术。缺少这些被跳过的产物不算失败。

### Gate 1：来源完整性

存在简历产物时，manifest 必须有用户已确认的 `project_origin`。每条简历要点必须有 `claim_id`、`source_type`、`role` 和 `chain_id`。缺任一项为 `RED`。

随后检查职责跨度：

- `OPEN_SOURCE`：全流程表述只能覆盖用户实际复现、改造、实现和验证的内容，不能冒充原作者；
- `SELF_OWNED`：端到端表述必须与个人或合作角色一致；
- `INTERNSHIP`：每条必须收敛到用户负责的高价值环节或核心闭环，不能冒领全产品、全系统或跨团队流程；
- `OTHER`：默认按实习项目的聚焦边界检查。

违反职责跨度为 `RED`，回退到贡献映射和简历生成阶段。

### Gate 2：代码与业务一致性

关键文件必须存在，调用链和技术名词必须与代码分析一致。动态关系允许 `[待确认]`，不允许把推测写成确定事实。

### Gate 3：角色一致性

简历、话术、拷打和模拟面试中的个人角色必须一致。团队成果不得在另一份产物中变成个人主导，除非 manifest 已更新并有依据。

### Gate 4：STAR 完整性与数字口径

逐条先解析首个分隔冒号：中文要点必须是“2-6 个汉字标签：正文”，英文要点必须是“1-4 word label: body”。标签须非空、概括主题、区别于相邻要点且不得使用 `S/T/A/R`；缺少标签、标签为空/过长/重复或冒号格式错误时为 `YELLOW`，回退简历生成阶段重写。

随后确认正文按顺序包含情境、个人任务、技术行动和结果；标签不承担 STAR 要素。由多条共同拼出 STAR、只写技术动作与效果或缺少任一要素时为 `YELLOW`，回退简历生成阶段重写。长度限制仅计算首个分隔冒号后的正文，标签不计入正文字数；`[待补：...]` 内部冒号不得触发二次切分，未填写占位符按生成契约不计入建议长度。

行动还必须通过关键方法筛选：每个方法应直接解释核心决策或结果，通常只保留 1-2 个最小充分方法。正文出现 3 个以上并列方法、工具、框架或能力时先执行删除测试；删掉任一项不影响问题、决策与结果的因果链，则为 `YELLOW`，回退简历生成阶段重写。检查并列项时不能只数顿号，还要识别逗号和“结合/通过/并使用/以及”等连接词。确属不可拆因果链且逐项说明独立作用的内容可保留。

每个真实数字必须能映射到 evidence。检查指标、基线、结果、环境、样本、统计口径和是否为估算。无来源且被作为已验证结果时为 `RED`。`[待补：...]`、`__` 或同类占位标记只能存在于待完善草稿；任何当前简历仍含未填写占位符时，最终状态不得高于 `REVIEW_REQUIRED`，也不得称为可直接投递。稳妥版中的定性结果同样必须来自用户材料或 evidence；补造上线稳定、压力下降、覆盖范围或反馈按事实冲突处理。从组件名称推导缓存键、TTL、失效、回源、命中行为等项目实现，再把推导内容用作 Result，同样按事实冲突处理。

### Gate 5：抗追问状态

所有核心 Bullet 必须至少为 `YELLOW`。未解决的核心 `RED` 直接触发 `BLOCKED`；非核心 `RED` 必须移出最终简历并进入训练清单。高风险来源需要满足 `claim-policy.md` 的额外门禁。

### Gate 6：学习闭环

所有 `RED/ORANGE/YELLOW` 薄弱点必须在学习路径或增强计划中有明确任务、参考位置和达标标准。学习路径还必须包含基于当前证据的 Mermaid 架构图与核心链路图；核心环节必须具备输入、输出、上下游、失败边界和达标标准。

当用户说“开始学习”或明确请求交互学习时，必须存在真实的版本化 HTML：`FILE_ARTIFACT` 直接报告文件路径，`ARTIFACT/FULL_PIPELINE` 还必须由 `current_artifacts.learning_interactive` 指向该文件。页面必须固定浅色主题，并包含架构图、核心链路、环节讲解和测验；Mermaid 渲染失败时必须保留源码与文字回退。缺任一项时学习门禁不通过，回退 Phase 6。

### Gate 7：跨产物一致性

检查简历、15 秒、30 秒、2 分钟话术和面试回答是否使用同一背景、角色、方案和结果。

### Gate 8：敏感信息与表达

检查密钥、token、密码、内部地址、真实客户敏感数据和不应公开的公司信息。检查是否包含用户明确不想公开的内容。

## 状态判定

```text
存在角色/事实冲突或核心 RED -> BLOCKED
存在 ORANGE，或高风险内容未完成门禁 -> TRAINING_REQUIRED
无 RED/ORANGE，但有 YELLOW、数字待复核或未填写量化占位符 -> REVIEW_REQUIRED
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
| STAR 完整性与数字口径 | | | star-resume-generator |
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
| 学习路径缺 Mermaid 或环节契约 | 回 Phase 6 补架构图、链路图与输入输出/失败边界 | 仍缺失则学习门禁失败 |
| “开始学习”后 HTML 缺失或非浅色 | 从当前学习路径重建版本化浅色 HTML | 仍失败则不宣称交互学习已交付 |
| manifest 损坏 | 备份后从现有产物重建索引 | 状态设为 `TRAINING_REQUIRED` |
| 同一 Claim 多个版本冲突 | 以用户最后确认和代码证据重建 | 状态设为 `BLOCKED` |
| 用户要求忽略风险 | 保留内容并记录 override | 不提升状态 |

## 不要做

- 不要只检查单份简历。
- 不要用平均分抵消事实或角色冲突。
- 不要静默修正用户角色。
- 不要把缺失文件当作通过。
- 不要为了给出“通过”结论而删除高风险项。
- 不要放行缺少任一 STAR 要素的简历要点。
- 不要放行缺少主题标签、标签为空/过长/重复、冒号格式错误或把标签计入正文字数的简历要点。
- 不要放行用顿号、逗号或连接词堆砌非关键方法、工具、框架和能力的简历要点。
- 不要把待补占位符当作 evidence，或让含未填写占位符的简历进入 `INTERVIEW_READY`。
