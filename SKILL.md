---
name: repo-to-resume
description: 将本地路径、GitHub 仓库、开源/他人项目、真实或薄弱实习、自研项目和现有简历转化为可面试的项目经历。执行代码与业务链路分析、个人贡献映射、经历增强/复现、STAR 简历、Bullet 逐条拷打、风险驱动学习、分层话术、模拟面试和最终质量门禁。用户提到“分析项目”“看懂代码”“写简历”“没有实习怎么包装”“开源项目包装”“项目面试”“STAR”“拷打简历”“模拟面试”“项目答辩”或提供项目路径/Git URL 时使用。
---

# repo-to-resume

把代码和经历加工成一套可学习、可表达、可追问、可迭代的面试材料。既支持真实实习，也支持弱实习、自研项目、开源/他人项目迁移和现有简历反向补强。

## 总原则

1. 先识别用户目标和已有材料，再选择最短路径。
2. 区分项目能力、团队成果、个人贡献、复现内容、方案设计和叙事补全。
3. 高风险内容不自动删除；为它生成复现、增强、学习和拷打路径。
4. 所有下游产物共享 `evidence-manifest.json`，不得各自重新解释事实。
5. 每个核心 Bullet 都要通过事实、角色、实现、选型、验证和边界六层追问。
6. 每个阶段都产出文件并保留版本；不得覆盖已有文件。

## 入口路由

只选择一个主模式，记录到 manifest：

| 模式 | 判定 | 默认路径 |
|---|---|---|
| `REAL_INTERNSHIP` | 有真实实习和明确个人产出 | 分析 -> 贡献 -> 简历 -> 拷打 |
| `WEAK_INTERNSHIP` | 有实习但产出零散或角色模糊 | 分析 -> 贡献 -> 增强 -> 简历 -> 拷打 |
| `SELF_PROJECT` | 无实习，有自己完成的项目 | 分析 -> 增强 -> 简历 -> 拷打 |
| `PROJECT_MIGRATION` | 从开源、团队或他人项目迁移内容 | 分析 -> 复现/推演 -> 简历 -> 强化拷打 |
| `EXISTING_RESUME` | 已有简历，需要核验和补强 | 贡献反查 -> 拷打 -> 补漏 |
| `UNDERSTAND_ONLY` | 只想看懂代码 | 分析 -> 学习路径；不生成简历 |

模式不明确时，一次只问一个区分度最高的问题。用户已明确要求“直接全部做完”时，根据现有材料选择最合理模式，记录 `auto_confirmed=true` 并继续。

## 资源加载

按当前阶段读取对应文件，不要一次加载全部引用：

| 阶段 | 必读 |
|---|---|
| 项目分析 | [code-analysis-engine.md](references/code-analysis-engine.md)、[business-chain-extractor.md](references/business-chain-extractor.md) |
| 贡献确认 | [contribution-mapper.md](references/contribution-mapper.md)、[claim-policy.md](references/claim-policy.md) |
| Manifest 校验 | [evidence-manifest.schema.json](references/evidence-manifest.schema.json) |
| 经历增强 | [experience-lab.md](references/experience-lab.md)、[claim-policy.md](references/claim-policy.md) |
| 简历生成 | [star-resume-generator.md](references/star-resume-generator.md)、[star-framework.md](references/star-framework.md) |
| Bullet 拷打 | [claim-grill.md](references/claim-grill.md) |
| 学习路径 | [learning-path-generator.md](references/learning-path-generator.md) |
| 交互学习 | [interactive-learning-template.md](references/interactive-learning-template.md) |
| 面试话术 | [interview-script-generator.md](references/interview-script-generator.md) |
| 模拟面试 | [mock-interviewer.md](references/mock-interviewer.md)、[interview-question-templates.md](references/interview-question-templates.md) |
| 最终门禁 | [quality-gate.md](references/quality-gate.md) |
| 对话展示 | [output-contracts.md](references/output-contracts.md) |

## 工作流

### Phase 0：初始化与范围确认

1. 解析本地目录、Git URL、压缩包或现有文档。
2. 判断用户模式、目标岗位、时间约束和期望产物。
3. 确认扫描范围与跳过目录。
4. 在被分析项目根目录创建 `{项目名}-analysis/`。
5. 按 `references/evidence-manifest.schema.json` 初始化 `evidence-manifest.json`；若已存在则校验后增量更新。

🔴 CHECKPOINT · MODE & SCOPE

展示模式、范围、预计产物和风险路径后暂停。用户已授权自动完成时写入自动确认记录并继续。

### Phase 1：项目与业务链路分析

1. 使用代码分析引擎生成技术栈、架构、模块、入口和六维分析。
2. 使用业务链路提取器从入口追踪到最终消费者。
3. 为每条链路记录关键代码、工程能力、缺口、价值评分和不确定项。
4. 写入 `project-analysis.md`、`business-chains.md` 和 manifest。

只读代码时优先使用仓库已有索引工具；存在 `.codegraph/` 时先用 CodeGraph。代码关系不确定时标记 `[待确认]`，不得猜测。

### Phase 2：贡献与来源映射

`UNDERSTAND_ONLY` 跳过本阶段。其他模式：

1. 逐条确认用户在高价值链路中的角色。
2. 为候选声明标记来源、掌握度、证据和风险。
3. 将内容分为 `READY / NEEDS_EVIDENCE / NEEDS_TRAINING / NEEDS_BUILD / BLOCKED`。
4. 写入 `contribution-map.md` 和 manifest。

🔴 CHECKPOINT · ROLE & SOURCE

展示候选经历、角色、来源、掌握度、风险和下一步。自动模式下继续，但完整保留风险记录。

### Phase 3：经历增强与项目迁移

符合任一条件时执行：

- 模式为 `WEAK_INTERNSHIP` 或 `PROJECT_MIGRATION`；
- 存在 `NEEDS_TRAINING/NEEDS_BUILD`；
- 项目缺少可讲的工程闭环；
- 用户要求补监控、容错、性能、测试、灰度等方案。

为 1-3 个最高价值缺口生成任务。优先实际实现；环境不足时降级为复现、设计或完整叙事推演。写入 `enhancement-plan.md`，更新掌握度和风险。

### Phase 4：STAR 简历

`UNDERSTAND_ONLY` 跳过本阶段。

1. 只消费 manifest 中允许进入草稿的 claims。
2. 按来源和角色选择动词。
3. 将高风险声明保留在草稿时，写入内部 claim ID 和风险，不在用户可见正文堆内部标签。
4. 数字沿用 manifest 的来源与口径；无数字时使用范围、闭环、故障或验证结果。
5. 生成 `resume.md`，最多 10 条 Action，每条保持紧凑。

🔴 CHECKPOINT · RESUME

展示简历、声明映射摘要和待验证项。自动模式下立即进入拷打，不将草稿标记为最终版。

### Phase 5：Bullet 逐条拷打

对每条核心 Bullet 逐一执行六层追问。交互时一次问一个；自动评估时根据现有代码、manifest 和用户材料做干跑，并明确标记未获得用户回答的部分。

输出 `claim-grill-report.md`。存在 `RED` 时自动回退一次：

1. 角色冲突 -> Phase 2；
2. 实现不熟 -> Phase 3 或 Phase 6；
3. 数据无来源 -> Phase 4；
4. 边界不完整 -> Phase 3。

重测仍为 `RED` 时保留训练材料，最终状态不得高于 `TRAINING_REQUIRED`。

### Phase 6：风险驱动学习与交互页面

根据“声明风险 x 面试概率 x 掌握缺口”排序学习任务，生成 `learning-path.md`。用户要求交互学习或执行完整流程时，再生成 `learning-interactive.html`；HTML 只转换学习路径，不重新分析代码。

### Phase 7：分层话术与模拟面试

1. 为 `GREEN/YELLOW` 声明生成 15 秒、30 秒、2 分钟和深挖材料，写入 `interview-scripts.md`。
2. 按暖场、技术深挖、系统视角、收尾四阶段模拟面试。
3. 优先追问高风险声明和学习薄弱点。
4. 生成 `interview-report.md`。

用户未实际回答时，不伪造面试得分；生成“待实战”问题集和预评分风险即可。

### Phase 8：最终质量门禁

运行八道门禁，检查来源、代码、角色、数字、抗追问、学习闭环、跨产物一致性和敏感信息。

输出 `quality-gate-report.md`，最终状态只能是：

- `BLOCKED`
- `TRAINING_REQUIRED`
- `REVIEW_REQUIRED`
- `INTERVIEW_READY`

🔴 CHECKPOINT · FINAL GATE

展示最终状态、可直接使用的声明、剩余风险和唯一优先动作。

## 产物目录

所有产物写入被分析项目内的 `{项目名}-analysis/`：

```text
{项目名}-analysis/
|- project-analysis.md
|- business-chains.md
|- contribution-map.md
|- evidence-manifest.json
|- enhancement-plan.md
|- resume.md
|- claim-grill-report.md
|- learning-path.md
|- learning-interactive.html
|- interview-scripts.md
|- interview-report.md
`- quality-gate-report.md
```

写入前确认目录存在。同名文件存在时创建 `-v1`、`-v2`，取现有最大版本号加一；禁止覆盖。

## 失败与恢复

| 触发条件 | 一线修复 | 仍失败则 |
|---|---|---|
| Git clone 失败 | 检查 URL、网络和权限，尝试现有 Git 凭据 | 要求本地路径或压缩包 |
| 路径不存在/不可读 | 展示解析后的绝对路径 | 终止扫描，保留已有材料处理能力 |
| 项目过大或超时 | 从文件级降为模块级，再降为 2-3 条关键链路 | 标记分析不完整 |
| 无法识别技术栈 | 搜索入口、构建文件和公开接口 | 输出通用结构分析 |
| 无标准入口 | 搜索消费者、任务、main 或公开接口 | 输出模块数据流 |
| 用户角色不清 | 按链路和文件追问 | 标记高风险，进入增强与拷打 |
| 项目无法运行 | 建立最小复现或设计验证计划 | 使用 `DESIGNED/NARRATIVE_READY` |
| manifest 缺失/损坏 | 备份后从现有产物重建 | 状态设为 `TRAINING_REQUIRED` |
| 用户跳过阶段 | 记录 override 和未完成门禁 | 继续，但不虚报最终状态 |

所有异常必须告知用户并写入风险记录；不得静默跳过。

## 反例黑名单

- 不要把代码仓库拥有的能力自动归为用户个人成果。
- 不要因为用户没有实习而拒绝服务或只给泛泛建议。
- 不要凭 Redis、线程池、MQ 或索引推导虚假性能百分比。
- 不要强制所有 Bullet 使用“主导、设计”等动词；角色匹配优先。
- 不要把增强任务计划自动当作已完成成果。
- 不要发现高风险内容后静默删除；应给出学习、复现和拷打路径。
- 不要一次向用户抛出多个面试问题。
- 不要在用户未回答时伪造模拟面试得分。
- 不要覆盖已有产物或读取密钥、token、密码内容。
- 不要跳过最终跨产物一致性检查。

## 完成标准

只有同时满足以下条件才算完整交付：

1. 用户要求的路径已完成；
2. 所有生成文件真实存在；
3. 核心声明可映射到 manifest；
4. 每个风险有明确状态和下一步；
5. 最终质量门禁已执行；
6. 对话中给出产物路径和最终状态。
