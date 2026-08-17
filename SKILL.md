---
name: repo-to-resume
description: 将本地路径、GitHub 仓库、开源/他人项目、真实或薄弱实习、自研项目和现有简历转化为可面试、可学习的项目材料。既可只执行代码分析、贡献映射、经历增强、简历改写、逐条拷打、带 Mermaid 的学习路径、浅色交互学习页、面试话术、模拟面试或质量检查，也可在用户明确要求时执行完整流程。用户提到“分析项目”“看懂代码”“写简历”“开始学习”“学习项目”“画架构图”“Mermaid”“只改一条”“开源项目包装”“项目面试”“STAR”“拷打简历”“模拟面试”或提供项目路径/Git URL 时使用。
---

# repo-to-resume

把代码和经历加工成一套可学习、可表达、可追问、可迭代的面试材料。既支持真实实习，也支持弱实习、自研项目、开源/他人项目迁移和现有简历反向补强。

## 总原则

1. 先识别用户本次明确要求的产物，再选择最短路径；默认只完成被请求的步骤，不把能力清单当作待办清单。
2. 区分项目能力、团队成果、个人贡献、复现内容、方案设计和叙事补全。
3. 高风险内容不自动删除；为它生成复现、增强、学习和拷打路径。
4. 多阶段或完整流程的下游产物共享 `evidence-manifest.json`，并只通过 `current_artifacts` 解析当前文件，不得猜测 `-vN` 或各自重新解释事实；单步骤对话交付不强制创建 manifest。
5. 每条简历要点都按紧凑 STAR 顺序包含情境、个人任务、技术行动和结果；量化结果缺失时使用显式待补占位符，不得省略结果或编造数字。
6. 完整流程中的每个核心简历要点都要通过事实、角色、实现、选型、验证和边界六层追问；单条改写只核验影响当前表述真实性的最小必要事实。
7. 需要落盘的阶段产出文件并保留版本，不得覆盖已有文件；用户只要求对话结果时不为流程完整性强制写文件。
8. 用户可见内容遵循用户语言：用户使用中文或未指定语言时，以自然中文为主；用户明确要求英文时使用英文。内部英文状态、字段名和流程术语不得直接泄漏到中文成品。
9. 任何生成或改写简历要点的任务都先确认项目来源；来源未确认时只问来源并停止，不输出示例、候选或改写稿。

## 入口路由

入口必须先确定三个互不替代的轴：

1. `source_mode`：当前材料和工作状态，决定事实处理路径。
2. `project_origin`：项目本身来自哪里，决定简历要点能覆盖的职责范围。
3. `task_scope`：用户这次要什么，决定执行哪些阶段以及在哪里停止。

### 材料来源

只选择一个 `source_mode`。多阶段流程写入 manifest；单步骤对话可只在当前上下文记录：

| `source_mode` | 判定 | `FULL_PIPELINE` 路径 |
|---|---|---|
| `REAL_INTERNSHIP` | 有真实实习和明确个人产出 | 1 -> 2 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `WEAK_INTERNSHIP` | 有实习但产出零散或角色模糊 | 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `SELF_PROJECT` | 无实习，有自己完成的项目 | 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `PROJECT_MIGRATION` | 从开源、团队或他人项目迁移内容 | 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `EXISTING_RESUME` | 已有简历，需要核验、改写或面试准备 | 2 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |

`source_mode` 不能代替 `project_origin`。例如，`EXISTING_RESUME` 只说明材料是已有简历，仍需确认其底层项目属于开源、个人还是实习项目。

### 项目来源

当 `task_scope` 包含 `RESUME_ONLY` 或任何简历生成/改写动作时，必须得到一个明确的 `project_origin`：

| `project_origin` | 判定 | 简历职责边界 |
|---|---|---|
| `OPEN_SOURCE` | 开源项目、已复现或计划二次开发的公开项目 | 通过复现/实现门禁后，可写覆盖需求、设计、实现和验证的完整流程 |
| `SELF_OWNED` | 用户独立或合作完成的个人项目 | 按真实角色，可写端到端设计与实现 |
| `INTERNSHIP` | 实习期间参与的公司或团队项目 | 只写用户负责的高价值环节或一个核心闭环 |
| `OTHER` | 课程、团队、外包或来源尚不能归入前三类 | 先按实习项目的聚焦边界处理，再根据角色证据收紧或放宽 |

用户原话未明确 `project_origin` 时，只问一个问题：“这个项目属于哪一种：开源项目、你自己的个人项目，还是实习项目？”用户回答前不得分析候选简历要点、提供示例或改写正文。一次涉及多个项目时逐项目记录来源，不得用其中一个项目的来源覆盖其余项目。

不生成或改写简历要点时，不强制追问 `project_origin`。例如，只分析代码、只生成学习路径、只拷打用户已提供的要点或只做模拟面试，可按该步骤的最小输入继续。

`ARTIFACT` 执行沿用 manifest 的 `mode` 字段存储 `source_mode`，并用顶层 `project_origin` 存储项目来源。存在 `current_artifacts.resume`、`current_artifacts.resume_clean` 或任一 `claims[].resume_text` 时，`project_origin` 必须存在并通过 `scripts/validate_manifest.py` 校验。只有分析、不涉及经历来源时可用兼容值 `UNDERSTAND_ONLY`。`task_scope` 属于本次执行计划，记录在对话与产物摘要中，不写入当前 manifest schema。

### 本次任务范围

从用户明确要求中选择一个或多个 `task_scope`。范围词优先于来源模式和默认能力：

| `task_scope` | 触发表达 | 只执行 |
|---|---|---|
| `ANALYZE_ONLY` | 只分析项目、只看业务链路、只看懂代码 | Phase 1 |
| `CONTRIBUTION_ONLY` | 只确认我的贡献、只做归因 | Phase 2 |
| `ENHANCE_ONLY` | 只补项目、只做增强/复现计划 | Phase 3 |
| `RESUME_ONLY` | 只写/改简历、只改这一条 | Phase 4 |
| `GRILL_ONLY` | 只拷打这条简历、找漏洞 | Phase 5 |
| `LEARNING_ONLY` | 只生成学习路线、只补知识、开始学习、生成学习网页 | Phase 6 |
| `SCRIPT_ONLY` | 只准备面试话术/逐字稿 | Phase 7A |
| `MOCK_INTERVIEW_ONLY` | 只模拟面试、现在开始问我 | Phase 7B |
| `QUALITY_CHECK_ONLY` | 只检查现有材料是否能面试 | Phase 8 的范围化检查 |
| `FULL_PIPELINE` | 全部做完、完整准备、端到端处理 | 按来源选择完整路径 |

用户同时明确要求多个产物时，只组合对应范围，例如“改两条简历并准备话术”=`RESUME_ONLY + SCRIPT_ONLY`，不自动插入分析、增强、拷打、学习或模拟面试。没有“只”字不等于完整流程；“帮我写简历”“分析这个项目”“准备一轮模拟面试”分别默认最小对应范围。只有明确表达“全部、完整、端到端”才选择 `FULL_PIPELINE`。

### 最小依赖与停止规则

| 范围 | 最小输入 | 缺失时的动作 |
|---|---|---|
| `ANALYZE_ONLY` | 项目路径、仓库或代码材料 | 只索取项目材料 |
| `CONTRIBUTION_ONLY` | 候选链路/代码证据与用户角色 | 只索取相关材料；不得擅自全仓扫描 |
| `ENHANCE_ONLY` | 当前项目能力与目标缺口 | 只索取缺口上下文 |
| `RESUME_ONLY` | 已确认的 `project_origin` + 用户提供的事实、要点或已有简历 | 先只追问项目来源；来源明确后再追问影响当前表述真实性的事实 |
| `GRILL_ONLY` | 待拷打的要点 | 直接逐条追问，一次一个问题 |
| `LEARNING_ONLY` | 项目材料、当前学习路径或目标主题 | “开始学习”时优先读取当前学习路径；不存在则只索取项目路径或学习材料 |
| `SCRIPT_ONLY` | 简历要点/项目事实与目标岗位 | 只索取缺失的表达材料 |
| `MOCK_INTERVIEW_ONLY` | 简历/项目摘要与目标岗位 | 只索取面试必需材料，然后开始提问 |
| `QUALITY_CHECK_ONLY` | 待检查的现有产物 | 只检查已提供范围，不补造其他产物 |

缺少最小输入时，一次只问一个区分度最高的问题。不得把“补齐输入”改写成自动执行未请求的前置阶段；如果确实必须扩大范围，先说明新增阶段、原因和产物，并等待用户确认。完成所选范围后立即停止，只展示结果、风险和可选下一步，不自动执行可选下一步。

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

### Phase 0：路由、初始化与范围确认

1. 从用户原话提取 `task_scope`，再判断必要的 `source_mode`、目标岗位、时间约束和期望产物。
2. 若范围包含简历生成或改写，从用户原话提取 `project_origin`；未明确时进入下方来源检查点并停止。
3. 列出本次会执行的阶段、明确跳过的阶段和停止点；显式“只/不要/不需要”是硬边界。
4. 确定输出语言：用户明确指定 > 用户当前使用的语言 > 默认中文；仅在范围包含代码分析时确认扫描范围与跳过目录。
5. 单个 `*_ONLY` 默认使用 `DIRECT` 执行：在对话中交付，不创建分析目录或 manifest。用户明确要求落盘、说“开始学习”而触发 HTML 文件，或多个阶段需要共享事实状态时，切换为 `ARTIFACT` 执行。
6. `ARTIFACT` 执行才在被分析项目根目录创建 `{项目名}-analysis/`，并按 `references/evidence-manifest.schema.json` 初始化 `evidence-manifest.json`。若检测到 `schema_version=1.0`，先运行 `python scripts/migrate_manifest.py <manifest> --output <临时文件>`，校验迁移结果并让用户确认差异后再原子替换；其他旧版本停止并报告不支持。`1.1` 版本先运行 `python scripts/validate_manifest.py <manifest>`，通过后增量更新。若校验只缺 `project_origin`，先询问项目来源、写入用户回答并重新校验，不得猜测。

🔴 CHECKPOINT · PROJECT ORIGIN · 🛑 STOP

仅在任务包含简历生成或改写且 `project_origin` 缺失时触发。只询问项目属于开源项目、个人项目还是实习项目，然后停止本轮简历处理；不得同时追问角色、数字、技术细节，不得先给“参考版本”。

🔴 CHECKPOINT · MODE & SCOPE

展示 `source_mode`、`project_origin`（简历相关任务）、`task_scope`、执行阶段、停止点、预计产物和风险路径后暂停。用户已明确给出单步骤边界、项目来源且不涉及写代码或范围扩张时，可直接执行；`FULL_PIPELINE` 或组合多个范围时等待确认。用户已授权自动完成时写入自动确认记录并继续，但自动确认不能替代缺失的项目来源。

### 阶段门禁

进入每个 Phase 前检查：该 Phase 是否在 `task_scope` 中，或是否属于已确认的 `FULL_PIPELINE` 路径。否则跳过，不加载该阶段资源、不生成该阶段产物，也不因为发现风险而自动追加该阶段。风险只记录为可选下一步。单步骤完成后立即结束。

下文所有“写入当前版本”“更新 `current_artifacts`”“更新 manifest”仅适用于 `ARTIFACT` 或 `FULL_PIPELINE`。`DIRECT` 执行把同等内容交付在对话中，不创建占位文件，也不为了满足旧产物契约切换为多阶段流程。

### Phase 1：项目与业务链路分析

仅 `ANALYZE_ONLY`、包含项目分析的组合范围或 `FULL_PIPELINE` 执行。

1. 使用代码分析引擎生成技术栈、架构、模块、入口和六维分析。
2. 使用业务链路提取器从入口追踪到最终消费者。
3. 先覆盖全仓库的业务域、平台能力、可靠性、性能、安全、测试与交付节点，再深挖最高价值链路；不得从单个提交或用户先提到的功能直接收敛为简历候选。
4. 为每条链路记录关键代码、工程能力、验证证据、缺口、价值评分和不确定项，并形成跨链路价值节点排序。
5. 写入当前版本的项目分析与业务链路报告，更新 `current_artifacts.project_analysis`、`current_artifacts.business_chains` 和 manifest。

只读代码时优先使用仓库已有索引工具；存在 `.codegraph/` 时先用 CodeGraph。代码关系不确定时标记 `[待确认]`，不得猜测。

### Phase 2：贡献与来源映射

仅 `CONTRIBUTION_ONLY`、包含贡献映射的组合范围或 `FULL_PIPELINE` 执行：

1. 逐条确认用户在高价值链路中的角色。
2. 代码证据决定候选“做了什么、难在哪里、产生什么结果”；Git 历史仅用于核对作者、时间、改动边界和演进顺序，不用于决定候选价值。
3. 从不同业务链路与工程类别建立候选池，按业务/架构关键性、工程深度、方案取舍、验证结果、岗位相关性和可追问深度排序；要求 N 条简历要点时至少比较 `max(6, 2N)` 个候选，仓库确实不足时记录扫描缺口。
4. 为候选声明标记来源、掌握度、证据和风险，将内容分为 `READY / NEEDS_EVIDENCE / NEEDS_TRAINING / NEEDS_BUILD / BLOCKED`。
5. 只有通过价值排序和角色门禁的候选才能写入核心 claim；写入当前版本的贡献映射，更新 `current_artifacts.contribution_map` 和 manifest。

🔴 CHECKPOINT · ROLE & SOURCE

展示候选经历、角色、来源、掌握度、风险和下一步。自动模式下继续，但完整保留风险记录。

### Phase 3：经历增强与项目迁移

仅 `ENHANCE_ONLY`、包含经历增强的组合范围或 `FULL_PIPELINE` 执行。完整流程中符合任一条件时进入：

- 模式为 `WEAK_INTERNSHIP` 或 `PROJECT_MIGRATION`；
- 存在 `NEEDS_TRAINING/NEEDS_BUILD`；
- 项目缺少可讲的工程闭环；
- 用户要求补监控、容错、性能、测试、灰度等方案。

为 1-3 个最高价值缺口生成任务。默认只生成计划、复现、设计或完整叙事推演。只有 manifest 中 `code_mutation.authorized=true` 时才允许修改被分析项目，并将写入范围限制在 `code_mutation.scope`。写入当前版本的增强计划，更新 `current_artifacts.enhancement_plan`、掌握度和风险。

🔴 CHECKPOINT · CODE MUTATION

修改被分析项目代码前，单独展示写入目录、预计文件和验证命令并等待明确授权。“直接全部做完”、`auto_confirmed=true` 或允许生成分析产物都不等于代码修改授权。未授权时保持 `code_mutation.authorized=false`，自动降级为 `REPRODUCED`、`DESIGNED` 或 `NARRATIVE_READY`。

### Phase 4：STAR 简历

仅 `RESUME_ONLY`、包含简历生成的组合范围或 `FULL_PIPELINE` 执行。

进入本阶段前必须已有明确 `project_origin`。缺失时回到 `CHECKPOINT · PROJECT ORIGIN`，只问来源并停止。`DIRECT + RESUME_ONLY` 在来源确认后可直接处理用户提供的要点或事实，不要求 manifest、候选池或全仓扫描；只对角色、数字口径、因果关系等会改变当前表述真实性的缺口做一次一个的最小追问。缺少可信量化结果时，先生成带待补占位符的 STAR 草稿；用户还要求可投递版本时，再给不含占位符的稳妥版。不得把单条改写扩张为六层拷打。

按 `project_origin` 选择唯一叙事边界：

| 项目来源 | 允许的简历范围 | 强制限制 |
|---|---|---|
| `OPEN_SOURCE` | 用户已完成复现、二次开发或等价实现并达到 `L3/L4` 时，可将多条要点组织成需求理解、架构设计、核心实现、测试验证的完整流程 | 使用“基于…复现/改造/扩展/实现”等来源准确的动词；未实现或不理解的步骤不得写成个人成果，不得冒充原作者 |
| `SELF_OWNED` | 按用户真实角色，可写从需求拆解、方案选型、架构设计、核心实现到验证交付的端到端流程 | 合作完成的部分必须标明个人边界；只有计划或推演的环节不能写成已完成 |
| `INTERNSHIP` | 每条只聚焦一个有含金量的重要环节，或围绕同一业务目标形成的一个核心闭环，例如意图识别链路、知识反馈闭环、召回排序链路、故障发现-处置-复盘闭环 | 不得把整个产品、全系统架构或跨团队端到端流程写成个人成果；闭环可跨多个步骤，但这些步骤必须属于用户实际负责范围 |
| `OTHER` | 默认采用 `INTERNSHIP` 的聚焦边界 | 只有用户补充明确所有权和实现证据后，才能放宽为端到端表达 |

1. `ARTIFACT` 或 `FULL_PIPELINE` 只消费 manifest 中允许进入草稿的 claims；`DIRECT` 只消费用户当前提供的事实。
2. `ARTIFACT` 或 `FULL_PIPELINE` 直接沿用贡献映射阶段的 12 分 `candidate_value_score` 从高到低选择，不在简历阶段另建评分公式；角色、来源、掌握度和风险只决定是否准入。任何未入选的合格候选分数更高时，必须替换较弱要点；仅因与已入选项主题重复而不替换时，在内部索引写明理由。`DIRECT` 保持用户指定的要点范围，不建立候选池或替换其他要点。
3. 先按 `project_origin` 应用上表的职责范围，再按 claim 来源和用户角色选择动词。
4. 每条要点以一句紧凑表述按 `情境 -> 任务 -> 行动 -> 结果` 排列：情境说明问题或约束，任务说明用户负责范围，行动给出技术决策与实现，结果给出量化变化。情境与任务可压缩在同一分句，但四项均不可缺失，不用 `S/T/A/R` 标签机械分段。
5. 结果按以下唯一分支处理：有可信证据时写真实指标与口径；缺少可信指标时写 `[待补：{指标}从 __ 变为 __，变化 __%，口径/环境 __]`，并将该版本标记为“待补数据，不可直接投递”；若同时输出稳妥版，则只能用用户材料或 evidence 已确认的覆盖范围、正确性验证或工程闭环作为结果，且不得保留占位符。技术组件名称不能补足事实：仅知道“使用 Redis”时，不得推断缓存键、过期、回源、命中行为或数据库压力变化。连定性结果也未确认时，不生成所谓“可直接投递版”，只追问一个结果事实。
6. 将高风险声明保留在草稿时，写入内部 claim ID 和风险，不在用户可见正文堆内部标签。提交文件数、增删行数、commit 大小和文档数量只属于审计元数据，不能充当结果或含金量证明。
7. 生成当前版本简历，更新 `current_artifacts.resume`；最多 10 条简历要点，每条保持紧凑。
8. 中文成品执行术语本地化：使用“简历要点、意图、大语言模型、智能体、数据结构约束、检查点、行动与结果”等自然中文，不把 `Bullet`、`Intent`、`LLM`、`Agent`、`Schema`、`checkpoint`、`Action & Result` 当作普通中文词直接混排。
9. 只为准确性保留必要英文：产品/框架/协议/行业通用缩写和真实代码标识符。代码标识符使用反引号并在首次出现时补中文职责，如 `decompose`（步骤拆分）；确需后续使用缩写时首次写“大语言模型（LLM）”，否则只写中文。
10. 发布前逐句检查标题和正文；发现可翻译的通用英文术语或用 Git 规模冒充成果时自动改写一次，仍不合格则标记 `REVIEW_REQUIRED`，不得称为最终版。

🔴 CHECKPOINT · RESUME

展示简历、声明映射摘要和待验证项。只有 `FULL_PIPELINE` 或范围明确包含 `GRILL_ONLY` 时进入拷打；`RESUME_ONLY` 在此停止。

### Phase 5：简历要点逐条拷打

仅 `GRILL_ONLY`、包含拷打的组合范围或 `FULL_PIPELINE` 执行。对每条被请求拷打的核心简历要点逐一执行六层追问。

交互时一次问一个；自动评估时根据现有代码、manifest 和用户材料做干跑，并明确标记未获得用户回答的部分。

`ARTIFACT` 或 `FULL_PIPELINE` 从 `current_artifacts.resume` 读取当前简历并输出新版本拷打报告，再更新 `current_artifacts.claim_grill_report`；`DIRECT + GRILL_ONLY` 直接读取用户提供的要点并在对话中拷打。完整流程存在 `RED` 时自动回退一次：

1. 角色冲突 -> Phase 2；
2. 实现不熟 -> Phase 3 或 Phase 6；
3. 数据无来源 -> Phase 4；
4. 边界不完整 -> Phase 3。

重测后仍为 `RED` 时：核心声明将最终状态设为 `BLOCKED`；非核心声明移出最终简历、保留为训练材料，最终状态最高为 `TRAINING_REQUIRED`。

### Phase 6：风险驱动学习与交互页面

仅 `LEARNING_ONLY`、包含学习路径的组合范围或 `FULL_PIPELINE` 执行。

1. 先确定 `learning_delivery`：用户明确说“不要网页/只要学习路径”时为 `MARKDOWN_ONLY`；用户说“开始学习/进入学习/生成学习网页/交互学习/HTML”时为 `LIGHT_HTML`；其余 `LEARNING_ONLY` 默认为 `MARKDOWN_ONLY`，`FULL_PIPELINE` 默认为 `MARKDOWN_AND_HTML`。显式拒绝 HTML 的表达优先级最高。
2. 根据“声明风险 x 面试概率 x 掌握缺口”排序学习任务，生成当前版本学习路径并更新 `current_artifacts.learning_path`。每份学习路径必须包含一个 Mermaid `flowchart` 架构图和一个 Mermaid `sequenceDiagram` 核心链路图，并为核心环节说明职责、输入、输出、上下游、关键文件、核心逻辑、设计决策、失败边界和达标标准。
3. Mermaid 节点与连线只能来自当前项目分析、业务链路或代码证据。关系不确定时使用虚线并在边标签写“待确认”；不得为了图完整而猜测中间模块、调用方向或异步关系。
4. `LIGHT_HTML/MARKDOWN_AND_HTML` 从 `current_artifacts.learning_path` 生成版本化 `learning-interactive.html` 并更新 `current_artifacts.learning_interactive`，不得重新分析或改写事实。“开始学习”且当前学习路径缺失时，若已有项目分析则先在本 Phase 生成学习路径；连项目材料也缺失时只索取一个项目路径或学习材料。
5. HTML 固定为浅色主题，按“系统全景 -> 核心链路 -> 相关环节详解 -> 随堂测验”组织。Mermaid 运行时加载失败时保留可读的 Mermaid 源码和文字链路，显示降级提示，不得留下空白图或静默跳过。
6. 生成 HTML 后检查桌面和移动端：导航可达、文字不溢出、图表非空、浅色对比度可读、测验可操作。可用浏览器自动化时截图验证；工具不可用时执行静态检查并明确标记未完成视觉验证。
7. 完成 Phase 6 后停止；不得因为用户开始学习而自动生成简历、话术、拷打或模拟面试。

### Phase 7A：分层话术

仅 `SCRIPT_ONLY`、包含面试话术的组合范围或 `FULL_PIPELINE` 执行。

1. 为 `GREEN/YELLOW` 声明生成 15 秒、30 秒、2 分钟和深挖材料，写入当前版本话术并更新 `current_artifacts.interview_scripts`。

### Phase 7B：模拟面试

仅 `MOCK_INTERVIEW_ONLY`、包含模拟面试的组合范围或 `FULL_PIPELINE` 执行。

1. `MOCK_INTERVIEW_ONLY` 只读取用户提供或指定的简历/项目摘要和目标岗位，不要求先生成贡献映射、拷打报告、学习路径或分层话术。
2. 按暖场、技术深挖、系统视角、收尾四阶段模拟面试，一次只问一个问题并等待用户实际回答。
3. 有现成风险清单时优先追问高风险声明；没有时根据简历内容直接提问，不自动生成学习路径。
4. 用户实际回答时生成面试反馈；`ARTIFACT` 或 `FULL_PIPELINE` 才写入当前版本面试报告并更新 `current_artifacts.interview_report`。未回答时只保留待实战问题，不写入虚构评分。

用户未实际回答时，不伪造面试得分；生成“待实战”问题集和预评分风险即可。

### Phase 8：最终质量门禁

仅 `QUALITY_CHECK_ONLY`、包含质量检查的组合范围或 `FULL_PIPELINE` 执行。`QUALITY_CHECK_ONLY` 只检查用户提供或指定的现有产物，不要求补造缺失阶段；`FULL_PIPELINE` 运行全部八道门禁。

完整门禁检查来源、代码、角色、数字、抗追问、学习闭环、跨产物一致性和敏感信息。`FULL_PIPELINE` 判定最终状态前必须运行 `python scripts/validate_manifest.py <manifest> --analysis-dir <分析目录> --require-artifacts`，保证映射存在且文件真实可读；失败时不得给出 `INTERVIEW_READY`。`DIRECT + QUALITY_CHECK_ONLY` 给出范围化结论和未检查项，不调用 manifest 校验，也不宣称完整流程状态。

输出当前版本质量门禁报告并更新 `current_artifacts.quality_gate_report`，最终状态只能是：

- `BLOCKED`
- `TRAINING_REQUIRED`
- `REVIEW_REQUIRED`
- `INTERVIEW_READY`

🔴 CHECKPOINT · FINAL GATE

展示最终状态、可直接使用的声明、剩余风险和唯一优先动作。

## 产物目录

`ARTIFACT` 或 `FULL_PIPELINE` 的产物写入被分析项目内的 `{项目名}-analysis/`。下表是完整流程的逻辑产物集合；单步骤只生成所选范围的产物，`DIRECT` 不强制创建目录或文件：

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
| Git 历史缺失或作者映射失败 | 继续基于代码建立价值候选池，向用户确认个人范围 | 来源标为 `CODE_INFERRED/HIGH`，不得停止代码分析 |
| 候选仅来自单个提交或单一功能 | 回到 Phase 1 补扫其他业务域和工程类别 | 标记候选池不完整，不生成最终简历 |
| 入选要点价值低于未入选合格候选 | 用高价值候选替换；未通过角色准入的候选不参与比较 | 仅因与已入选项主题重复时允许去重，记录理由并标记 `REVIEW_REQUIRED` |
| 无法识别技术栈 | 搜索入口、构建文件和公开接口 | 输出通用结构分析 |
| 无标准入口 | 搜索消费者、任务、main 或公开接口 | 输出模块数据流 |
| 用户角色不清 | 按链路和文件追问 | 标记高风险，进入增强与拷打 |
| 项目无法运行 | 建立最小复现或设计验证计划 | 使用 `DESIGNED/NARRATIVE_READY` |
| manifest 缺失/损坏 | 备份后从现有产物重建 | 状态设为 `TRAINING_REQUIRED` |
| `current_artifacts` 指向缺失文件 | 扫描同逻辑名的最高版本并展示候选 | 用户确认后修复映射，未确认则停止下游阶段 |
| 未授权代码修改 | 保持只读并输出增强计划 | 降级为复现、设计或叙事推演 |
| 用户跳过阶段 | 记录 override 和未完成门禁 | 继续，但不虚报最终状态 |
| 单步骤缺少最小输入 | 只索取该步骤必需的一项材料 | 说明无法完成的部分并停止，不自动执行其他阶段 |
| 简历任务缺少 `project_origin` | 只问“开源项目、个人项目还是实习项目” | 用户未回答则停止，不生成或改写任何简历要点 |
| `source_mode` 与 `project_origin` 冲突 | 展示冲突并让用户确认项目真实来源 | 保持原简历不变，标记 `REVIEW_REQUIRED` |
| 开源项目要求写全流程但用户尚未复现/实现 | 将对应环节标为 `NEEDS_BUILD/NEEDS_TRAINING`，生成复现任务 | 只保留来源准确的训练草稿，不写成已完成成果 |
| 实习候选覆盖整个产品或跨团队流程 | 收窄到用户负责的高价值环节或单一核心闭环 | 找不到可归因范围时停止生成最终要点，继续追问职责 |
| 执行中发现可选后续任务 | 记录风险和下一步 | 完成当前范围后停止，等待用户另行授权 |
| STAR 要点缺少任一要素 | 按情境、任务、行动、结果顺序自动重写一次 | 仍缺失则标记 `REVIEW_REQUIRED`，不得称为最终版 |
| 量化结果无可信证据 | 改为统一待补占位符并标记不可投递 | 仅有已确认定性结果时生成稳妥版；否则只追问一个结果事实，不伪造可投递版 |
| Mermaid 关系缺少代码或分析证据 | 使用虚线边并标“待确认”，同时保留文字说明 | 仍无法确定方向时移除该边，不猜测关系 |
| “开始学习”但当前学习路径缺失 | 有项目分析时在 Phase 6 先生成路径 | 连项目材料也没有时只索取一个项目路径或学习材料 |
| Mermaid 运行时加载或渲染失败 | 保留 Mermaid 源码并展示降级提示和文字链路 | 交付 HTML 但标记“图表未渲染”，不得称视觉检查通过 |
| HTML 浏览器验证不可用 | 执行占位符、链接、主题和 Mermaid 源码静态检查 | 明确记录未完成桌面/移动端视觉验证 |

所有异常必须告知用户并写入风险记录；不得静默跳过。

## 反例黑名单

- 不要把代码仓库拥有的能力自动归为用户个人成果。
- 不要在项目来源未知时生成、改写或示范简历要点；先问来源并停止。
- 不要把“已有简历”误当作项目来源；必须继续确认底层项目是开源、个人还是实习项目。
- 不要把实习项目写成用户独立完成的全产品或全系统流程；只写高价值环节或核心闭环。
- 不要把开源项目原作者的设计直接写成用户原创；只有实际复现、改造、实现和验证过的部分才能组成全流程表述。
- 不要按 Git 提交列表逐条生成简历，也不要把最近提交、最大提交或用户点名的提交默认视为最高价值贡献。
- 不要把 commit hash、改动文件数、增删行数、提交次数或 ADR/文档数量写成核心成果；它们只能帮助归因或说明审计范围。
- 不要在发现更高价值且角色合格的代码候选后仍保留低价值要点；必须替换，而不是用“均基于真实提交”解释其合理性。
- 不要因为用户没有实习而拒绝服务或只给泛泛建议。
- 不要凭 Redis、线程池、MQ 或索引推导虚假性能百分比，也不要把组件的典型工作方式推断为该项目实际采用的实现或结果。
- 不要强制所有简历要点使用“主导、设计”等动词；角色匹配优先。
- 不要把增强任务计划自动当作已完成成果。
- 不要生成缺少情境、个人任务、技术行动或结果中任一项的简历要点，也不要用 `S:`、`T:`、`A:`、`R:` 把一句话机械切成四段。
- 不要把待补占位符当作已验证结果；含 `__`、`[待补：...]` 或同类未填写标记的版本不得称为可投递或 `INTERVIEW_READY`。
- 不要发现高风险内容后静默删除；应给出学习、复现和拷打路径。
- 不要一次向用户抛出多个面试问题。
- 不要在用户未回答时伪造模拟面试得分。
- 不要覆盖已有产物或读取密钥、token、密码内容。
- 不要把分析或“全部做完”的授权解释为修改目标项目代码的授权。
- 不要把 `source_mode` 的默认完整路径当成用户本次授权；`task_scope` 才决定执行范围。
- 不要因 skill 具备分析、增强、简历、拷打、学习和面试能力，就在一次调用中依次执行全部能力。
- 不要在 `DIRECT` 单步骤请求中为流程完整性创建分析目录、manifest、学习路径或质量门禁报告。
- 不要在完成用户指定步骤后自动进入“合理的下一步”；只展示它并停止。
- 不要用 ASCII 图替代学习路径中要求的 Mermaid 架构图与核心链路图。
- 不要根据目录名猜测 Mermaid 连线；不确定关系必须标“待确认”或删除。
- 不要把“开始学习”理解成继续输出一段文字；应生成固定浅色 HTML，但用户明确说“不要网页”时不得生成。
- 不要让 Mermaid 加载失败后留下空白区域，也不要把未验证的 HTML 宣称为视觉检查通过。
- 不要绕过 `current_artifacts` 按固定文件名读取可能过期的产物。
- 不要跳过最终跨产物一致性检查。
- 中文成品不要使用 `Bullet 1`、`Action & Result`、`Claim`、`Intent`、`Agent`、`Schema`、`checkpoint` 等英文作普通标题或叙述词；优先写“简历要点、行动与结果、声明、意图、智能体、数据结构约束、检查点”。
- 不要机械翻译产品名、协议名、框架名、行业通用缩写或真实代码标识符；保留英文时必须有准确性理由，代码标识符首次出现时补中文职责。

## 完成标准

单步骤交付完成的条件：

1. 用户请求的范围已经完成；
2. 没有执行或生成范围外阶段与产物；
3. 影响当前结果真实性的风险已明确标记；
4. 已在约定停止点结束。

只有 `FULL_PIPELINE` 同时满足以下条件才算完整交付：

1. 用户要求的路径已完成；
2. 所有生成文件真实存在；
3. 核心声明可映射到 manifest；
4. 每个风险有明确状态和下一步；
5. 最终质量门禁已执行；
6. 对话中给出产物路径和最终状态。
