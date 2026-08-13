# 声明来源与风险政策

本模块定义简历、面试话术和学习材料共同遵守的声明模型。任何用户可见的项目声明都必须先登记到 `evidence-manifest.json`，再由下游模块消费。

## 1. 声明来源

| 类型 | 定义 | 可用范围 |
|---|---|---|
| `PERSONAL_FACT` | 用户亲自完成且能描述实现 | 可写个人 Action |
| `TEAM_FACT` | 团队完成，用户实际参与 | 写团队成果并限定个人部分 |
| `MENTOR_DIRECTED` | 他人决策，用户负责实现 | 写实现、验证和理解，不写主导选型 |
| `CODE_INFERRED` | 仓库存在该能力，用户角色未知 | 先进入贡献确认，不直接写个人成果 |
| `SELF_PROJECT` | 用户独立或共同完成的自研项目 | 按实际角色写项目经历 |
| `REPRODUCED` | 用户完成开源/他人项目复现或改造 | 写复现、迁移、扩展和验证 |
| `BORROWED_CONTEXT` | 来自团队或他人，用户尚未实现 | 可进入学习、复现和叙事准备，高风险 |
| `DESIGNED_ONLY` | 用户完成方案设计或完整推演，未上线 | 写设计、评估、对比和验证计划 |
| `NARRATIVE_FILL` | 为补齐工程闭环而生成的合理环节 | 允许包装，但必须高强度拷打 |

## 2. 掌握度

| 等级 | 可观察行为 |
|---|---|
| `L0` | 只知道名词，不能解释主流程 |
| `L1` | 能说明用途和基本原理 |
| `L2` | 能定位关键代码并画出主流程 |
| `L3` | 能解释方案选择、替代方案和失败边界 |
| `L4` | 能独立实现、测试、排错和复盘 |

核心 Bullet 最低要求 `L3`。来源为 `BORROWED_CONTEXT` 或 `NARRATIVE_FILL` 时，满足以下任一条件才可进入最终简历：

1. 达到 `L4`；
2. 达到 `L3`，且连续两轮拷打无 `RED`，并完成一项实现或验证任务。

## 3. 风险计算

按以下顺序确定风险：

```text
无法解释核心实现或角色冲突 -> BLOCKED
BORROWED_CONTEXT / NARRATIVE_FILL / 无来源数字 -> HIGH
TEAM_FACT / MENTOR_DIRECTED / DESIGNED_ONLY -> MEDIUM
PERSONAL_FACT / SELF_PROJECT / 已验证 REPRODUCED -> LOW
```

风险决定验证强度，不自动决定删除。用户明确要求保留高风险声明时，保留该声明并在内部记录风险，同时生成对应补强任务和拷打题。

## 4. 角色与动词

| 已确认角色 | 可用动词 | 禁止夸大的动词 |
|---|---|---|
| 方案主导 | 设计、主导、推动、制定 | 无 |
| 独立实现 | 实现、重构、改造、建立 | 主导整体架构 |
| 团队参与 | 参与、协同、配合、负责其中 | 独立完成、从零主导 |
| 复现迁移 | 复现、迁移、扩展、验证 | 原创、首创 |
| 方案推演 | 设计、对比、评估、规划 | 上线、落地、稳定运行 |
| 阅读学习 | 梳理、分析、定位、总结 | 实现、重构、建立 |

“参与”不是默认弱词。动词是否有力取决于后续是否接具体模块、技术动作和结果。

## 5. 数字证据

每个数字必须登记 `evidence_type`：

| 类型 | 定义 | 表达规则 |
|---|---|---|
| `PRODUCTION` | 线上监控、业务报表 | 可直接写，记录口径 |
| `BENCHMARK` | 本地或测试环境压测 | 写明环境和样本 |
| `STATIC_COUNT` | 文件、端点、模块、规则数量 | 可直接写，保留计算方法 |
| `USER_REPORTED` | 用户根据经历提供 | 可写，标记待复核 |
| `ESTIMATED` | 基于合理假设推算 | 仅在用户确认后写，准备估算口径 |
| `NARRATIVE` | 为形成完整故事设定 | 高风险，必须通过数据追问 |

禁止仅凭“使用 Redis、线程池、消息队列、索引”推导性能提升百分比。没有可靠性能数据时，优先写覆盖范围、链路闭环、故障类型、模块数量或验证动作。

## 6. evidence-manifest 最小结构

```json
{
  "schema_version": "1.1",
  "mode": "REAL_INTERNSHIP",
  "current_artifacts": {
    "project_analysis": "project-analysis.md",
    "business_chains": "business-chains.md",
    "learning_path": "learning-path.md",
    "quality_gate_report": "quality-gate-report.md"
  },
  "code_mutation": {"authorized": false, "scope": []},
  "project": {"name": "sample-project"},
  "business_chains": [],
  "contributions": [],
  "enhancement_tasks": [],
  "claims": [],
  "evidence": [],
  "grill_results": [],
  "learning_gaps": [],
  "risk_flags": [],
  "quality_status": "TRAINING_REQUIRED"
}
```

每条 `claim` 必须包含：`id`、`text`、`source_type`、`role`、`mastery_level`、`risk`、`chain_id`、`evidence_ids`、`status`、`grill_status` 和 `is_core`。`status` 只能是 `READY / NEEDS_EVIDENCE / NEEDS_TRAINING / NEEDS_BUILD / BLOCKED`。

### 更新规则

`evidence-manifest.json` 始终表示当前状态，不使用 `-v1/-v2` 文件名。每次更新必须：

1. 将旧文件复制到 `history/evidence-manifest-{时间戳}.json`；
2. 将新内容写入同目录临时文件；
3. 按 `evidence-manifest.schema.json` 校验结构，再运行 `python scripts/validate_manifest.py <manifest>` 校验 ID 唯一性、引用完整性、产物指针、模式约束和代码修改授权；最终门禁额外传入 `--analysis-dir <分析目录> --require-artifacts`；
4. 校验通过后原子替换当前文件；
5. 校验失败则删除临时文件并继续使用旧文件。

其他模块只读取固定的当前 manifest，并从 `current_artifacts` 获取普通产物当前版本；历史文件仅用于审计和恢复。写入普通产物成功后先更新 `current_artifacts`，再按上述原子流程替换 manifest。

旧 manifest 的 `schema_version=1.0` 时，运行 `python scripts/migrate_manifest.py <manifest> --output <临时文件>`。迁移器只补确定性默认值并报告需要人工补齐的字段；迁移结果通过结构和语义校验、且用户确认差异后才能替换当前 manifest。未知版本不得猜测迁移。

## 7. 失败处理

| 触发条件 | 一线处理 | 仍失败则 |
|---|---|---|
| 用户无法说明角色 | 逐文件或逐链路询问“你改了什么” | 标记 `CODE_INFERRED/HIGH` |
| 数字无来源 | 追问口径、环境和前后值 | 降级为定性结果或 `NARRATIVE/HIGH` |
| 代码与用户说法冲突 | 展示冲突证据并要求选择版本 | 保留双方记录，状态设为 `BLOCKED` |
| 高风险声明无法通过拷打 | 生成复现/增强任务 | 删除、降级或继续训练，不标记 Ready |

## 8. 反例黑名单

- 不要把仓库存在的能力自动归为用户个人成果。
- 不要用统一强动词覆盖真实角色差异。
- 不要凭技术组件推导虚假的性能百分比。
- 不要把 `DESIGNED_ONLY` 默认写成已上线运行。
- 不要静默隐藏高风险来源；必须进入 manifest 和拷打报告。
- 不要因为来源高风险就停止服务；应生成学习、复现、增强和抗追问路径。
