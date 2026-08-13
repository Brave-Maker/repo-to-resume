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
4. 所有下游产物共享 `evidence-manifest.json`，并只通过 `current_artifacts` 解析当前文件，不得猜测 `-vN` 或各自重新解释事实。
5. 每个核心简历要点都要通过事实、角色、实现、选型、验证和边界六层追问。
6. 每个阶段都产出文件并保留版本；不得覆盖已有文件。
7. 用户可见内容遵循用户语言：用户使用中文或未指定语言时，以自然中文为主；用户明确要求英文时使用英文。内部英文状态、字段名和流程术语不得直接泄漏到中文成品。

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
| Manifest 校验 | [evidence-manifest.schema.json](references/evidence-manifest.schema.json)，并运行 `scripts/validate_manifest.py` |
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
3. 确定输出语言：用户明确指定 > 用户当前使用的语言 > 默认中文；确认扫描范围与跳过目录。
4. 在被分析项目根目录创建 `{项目名}-analysis/`。
5. 按 `references/evidence-manifest.schema.json` 初始化 `evidence-manifest.json`。若检测到 `schema_version=1.0`，先运行 `python scripts/migrate_manifest.py <manifest> --output <临时文件>`，校验迁移结果并让用户确认差异后再原子替换；其他旧版本停止并报告不支持。`1.1` 版本先运行 `python scripts/validate_manifest.py <manifest>`，通过后增量更新。

🔴 CHECKPOINT · MODE & SCOPE

展示模式、范围、预计产物和风险路径后暂停。用户已授权自动完成时写入自动确认记录并继续。

### Phase 1：项目与业务链路分析

1. 使用代码分析引擎生成技术栈、架构、模块、入口和六维分析。
2. 使用业务链路提取器从入口追踪到最终消费者。
3. 为每条链路记录关键代码、工程能力、缺口、价值评分和不确定项。
4. 写入当前版本的项目分析与业务链路报告，更新 `current_artifacts.project_analysis`、`current_artifacts.business_chains` 和 manifest。

只读代码时优先使用仓库已有索引工具；存在 `.codegraph/` 时先用 CodeGraph。代码关系不确定时标记 `[待确认]`，不得猜测。

### Phase 2：贡献与来源映射

`UNDERSTAND_ONLY` 跳过本阶段。其他模式：

1. 逐条确认用户在高价值链路中的角色。
2. 为候选声明标记来源、掌握度、证据和风险。
3. 将内容分为 `READY / NEEDS_EVIDENCE / NEEDS_TRAINING / NEEDS_BUILD / BLOCKED`。
4. 写入当前版本的贡献映射，更新 `current_artifacts.contribution_map` 和 manifest。

🔴 CHECKPOINT · ROLE & SOURCE

展示候选经历、角色、来源、掌握度、风险和下一步。自动模式下继续，但完整保留风险记录。

### Phase 3：经历增强与项目迁移

`UNDERSTAND_ONLY` 跳过本阶段。其他模式符合任一条件时执行：

- 模式为 `WEAK_INTERNSHIP` 或 `PROJECT_MIGRATION`；
- 存在 `NEEDS_TRAINING/NEEDS_BUILD`；
- 项目缺少可讲的工程闭环；
- 用户要求补监控、容错、性能、测试、灰度等方案。

为 1-3 个最高价值缺口生成任务。默认只生成计划、复现、设计或完整叙事推演。只有 manifest 中 `code_mutation.authorized=true` 时才允许修改被分析项目，并将写入范围限制在 `code_mutation.scope`。写入当前版本的增强计划，更新 `current_artifacts.enhancement_plan`、掌握度和风险。

🔴 CHECKPOINT · CODE MUTATION

修改被分析项目代码前，单独展示写入目录、预计文件和验证命令并等待明确授权。“直接全部做完”、`auto_confirmed=true` 或允许生成分析产物都不等于代码修改授权。未授权时保持 `code_mutation.authorized=false`，自动降级为 `REPRODUCED`、`DESIGNED` 或 `NARRATIVE_READY`。

### Phase 4：STAR 简历

`UNDERSTAND_ONLY` 跳过本阶段。

1. 只消费 manifest 中允许进入草稿的 claims。
2. 按来源和角色选择动词。
3. 将高风险声明保留在草稿时，写入内部 claim ID 和风险，不在用户可见正文堆内部标签。
4. 数字沿用 manifest 的来源与口径；无数字时使用范围、闭环、故障或验证结果。
5. 生成当前版本简历，更新 `current_artifacts.resume`；最多 10 条简历要点，每条保持紧凑。
6. 中文成品执行术语本地化：使用“简历要点、意图、大语言模型、智能体、数据结构约束、检查点、行动与结果”等自然中文，不把 `Bullet`、`Intent`、`LLM`、`Agent`、`Schema`、`checkpoint`、`Action & Result` 当作普通中文词直接混排。
7. 只为准确性保留必要英文：产品/框架/协议/行业通用缩写和真实代码标识符。代码标识符使用反引号并在首次出现时补中文职责，如 `decompose`（步骤拆分）；确需后续使用缩写时首次写“大语言模型（LLM）”，否则只写中文。
8. 发布前逐句检查标题和正文；发现可翻译的通用英文术语时自动改写一次，仍混用则标记 `REVIEW_REQUIRED`，不得称为最终版。

🔴 CHECKPOINT · RESUME

展示简历、声明映射摘要和待验证项。自动模式下立即进入拷打，不将草稿标记为最终版。

### Phase 5：简历要点逐条拷打

`UNDERSTAND_ONLY` 跳过本阶段。其他模式对每条核心简历要点逐一执行六层追问。

交互时一次问一个；自动评估时根据现有代码、manifest 和用户材料做干跑，并明确标记未获得用户回答的部分。

从 `current_artifacts.resume` 读取当前简历并输出新版本拷打报告，再更新 `current_artifacts.claim_grill_report`。存在 `RED` 时自动回退一次：

1. 角色冲突 -> Phase 2；
2. 实现不熟 -> Phase 3 或 Phase 6；
3. 数据无来源 -> Phase 4；
4. 边界不完整 -> Phase 3。

重测后仍为 `RED` 时：核心声明将最终状态设为 `BLOCKED`；非核心声明移出最终简历、保留为训练材料，最终状态最高为 `TRAINING_REQUIRED`。

### Phase 6：风险驱动学习与交互页面

根据“声明风险 x 面试概率 x 掌握缺口”排序学习任务，生成当前版本学习路径并更新 `current_artifacts.learning_path`。用户要求交互学习或执行完整流程时，再生成交互页面并更新 `current_artifacts.learning_interactive`；HTML 只转换学习路径，不重新分析代码。

### Phase 7：分层话术与模拟面试

`UNDERSTAND_ONLY` 跳过本阶段。

1. 为 `GREEN/YELLOW` 声明生成 15 秒、30 秒、2 分钟和深挖材料，写入当前版本话术并更新 `current_artifacts.interview_scripts`。
2. 按暖场、技术深挖、系统视角、收尾四阶段模拟面试。
3. 优先追问高风险声明和学习薄弱点。
4. 用户实际回答时生成当前版本面试报告并更新 `current_artifacts.interview_report`；未回答时只生成待实战问题集，不写入虚构评分。

用户未实际回答时，不伪造面试得分；生成“待实战”问题集和预评分风险即可。

### Phase 8：最终质量门禁

`UNDERSTAND_ONLY` 只检查代码证据、业务链路、学习路径和敏感信息，不要求简历、贡献、拷打或话术产物；其他模式运行全部八道门禁。

完整门禁检查来源、代码、角色、数字、抗追问、学习闭环、跨产物一致性和敏感信息。判定最终状态前必须运行 `python scripts/validate_manifest.py <manifest> --analysis-dir <分析目录> --require-artifacts`，保证映射存在且文件真实可读；失败时不得给出 `INTERVIEW_READY`。

输出当前版本质量门禁报告并更新 `current_artifacts.quality_gate_report`，最终状态只能是：

- `BLOCKED`
- `TRAINING_REQUIRED`
- `REVIEW_REQUIRED`
- `INTERVIEW_READY`

🔴 CHECKPOINT · FINAL GATE

展示最终状态、可直接使用的声明、剩余风险和唯一优先动作。

## 产物目录

所有产物写入被分析项目内的 `{项目名}-analysis/`。下表是完整模式的逻辑产物集合；`UNDERSTAND_ONLY` 只生成项目分析、业务链路、学习路径、manifest 和质量门禁报告：

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

写入前确认目录存在。普通交付文件同名时创建 `-v1`、`-v2`，取现有最大版本号加一；禁止覆盖。每次成功写入后，将 manifest 的 `current_artifacts.{逻辑名}` 更新为新文件的相对路径。所有下游先读取该映射；映射缺失或文件不存在时停止该阶段并重建索引，禁止回退到猜测固定文件名。

`evidence-manifest.json` 是唯一例外：它是下游共同读取的当前状态文件，必须保持固定文件名。更新前将旧版复制到 `history/evidence-manifest-{时间戳}.json`，再把新内容写入临时文件，同时完成 Schema 与 `scripts/validate_manifest.py` 语义校验后原子替换当前 manifest。校验失败时保留旧版并报告错误。下游禁止读取历史快照作为当前状态。

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
| `current_artifacts` 指向缺失文件 | 扫描同逻辑名的最高版本并展示候选 | 用户确认后修复映射，未确认则停止下游阶段 |
| 未授权代码修改 | 保持只读并输出增强计划 | 降级为复现、设计或叙事推演 |
| 用户跳过阶段 | 记录 override 和未完成门禁 | 继续，但不虚报最终状态 |

所有异常必须告知用户并写入风险记录；不得静默跳过。

## 反例黑名单

- 不要把代码仓库拥有的能力自动归为用户个人成果。
- 不要因为用户没有实习而拒绝服务或只给泛泛建议。
- 不要凭 Redis、线程池、MQ 或索引推导虚假性能百分比。
- 不要强制所有简历要点使用“主导、设计”等动词；角色匹配优先。
- 不要把增强任务计划自动当作已完成成果。
- 不要发现高风险内容后静默删除；应给出学习、复现和拷打路径。
- 不要一次向用户抛出多个面试问题。
- 不要在用户未回答时伪造模拟面试得分。
- 不要覆盖已有产物或读取密钥、token、密码内容。
- 不要把分析或“全部做完”的授权解释为修改目标项目代码的授权。
- 不要绕过 `current_artifacts` 按固定文件名读取可能过期的产物。
- 不要跳过最终跨产物一致性检查。
- 中文成品不要使用 `Bullet 1`、`Action & Result`、`Claim`、`Intent`、`Agent`、`Schema`、`checkpoint` 等英文作普通标题或叙述词；优先写“简历要点、行动与结果、声明、意图、智能体、数据结构约束、检查点”。
- 不要机械翻译产品名、协议名、框架名、行业通用缩写或真实代码标识符；保留英文时必须有准确性理由，代码标识符首次出现时补中文职责。

## 完成标准

只有同时满足以下条件才算完整交付：

1. 用户要求的路径已完成；
2. 所有生成文件真实存在；
3. 核心声明可映射到 manifest；
4. 每个风险有明确状态和下一步；
5. 最终质量门禁已执行；
6. 对话中给出产物路径和最终状态。
