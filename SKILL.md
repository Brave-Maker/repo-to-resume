---
name: repo-to-resume
description: 将本地路径、GitHub 仓库、开源/他人项目、真实或薄弱实习、自研项目和现有简历转化为可面试、可学习的项目材料。既可只执行代码分析、贡献映射、经历增强、简历改写、逐条拷打、带 Mermaid 的学习路径、浅色交互学习页、面试话术、模拟面试或质量检查，也可在用户明确要求时执行完整流程。用户提到“分析项目”“看懂代码”“写简历”“开始学习”“学习项目”“画架构图”“Mermaid”“只改一条”“开源项目包装”“项目面试”“STAR”“拷打简历”“模拟面试”或提供项目路径/Git URL 时使用。
---

# repo-to-resume

把代码和经历加工成一套可学习、可表达、可追问、可迭代的面试材料。既支持真实实习，也支持弱实习、自研项目、开源/他人项目迁移和现有简历反向补强。

## 总原则

1. 先识别用户本次明确要求的产物，再选最短路径；默认只完成被请求的步骤，不把能力清单当作待办清单。
2. 区分项目能力、团队成果、个人贡献、复现内容、方案设计和叙事补全。
3. 高风险内容不自动删除；为它生成复现、增强、学习和拷打路径。
4. 多阶段或完整流程的下游产物共享 `evidence-manifest.json`，并只通过 `current_artifacts` 解析当前文件，不得猜测 `-vN` 或各自重新解释事实；单步骤对话交付不强制创建 manifest。
5. 每条简历要点都按紧凑 STAR 顺序包含情境、个人任务、技术行动和结果；量化结果缺失时使用显式待补占位符，不得省略结果或编造数字。
6. 用户可见内容遵循用户语言：用户使用中文或未指定语言时，以自然中文为主；用户明确要求英文时使用英文。内部英文状态、字段名和流程术语不得直接泄漏到中文成品。
7. 任何生成或改写简历要点的任务都先确认项目来源；来源未确认时只问来源并停止，不输出示例、候选或改写稿。

## 入口路由

入口先确定三个互不替代的轴：`source_mode`（材料与工作状态，决定事实路径）、`project_origin`（项目来自哪里，决定简历职责范围）、`task_scope`（本次要什么，决定执行阶段与停止点）。

### 材料来源

只选一个 `source_mode`。多阶段流程写入 manifest；单步骤可只在当前上下文记录：

| `source_mode` | 判定 | `FULL_PIPELINE` 路径 |
|---|---|---|
| `REAL_INTERNSHIP` | 有真实实习和明确个人产出 | 1 -> 2 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `WEAK_INTERNSHIP` | 有实习但产出零散或角色模糊 | 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `SELF_PROJECT` | 无实习，有自己完成的项目 | 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `PROJECT_MIGRATION` | 从开源、团队或他人项目迁移内容 | 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |
| `EXISTING_RESUME` | 已有简历，需要核验、改写或面试准备 | 2 -> 4 -> 5 -> 6 -> 7A/7B -> 8 |

`source_mode` 不能代替 `project_origin`。例如 `EXISTING_RESUME` 只说明材料是已有简历，仍需确认底层项目属于开源、个人还是实习项目。

### 项目来源

当 `task_scope` 含 `RESUME_ONLY` 或任何简历生成/改写动作时，必须得到明确的 `project_origin`：

| `project_origin` | 判定 | 简历职责边界 |
|---|---|---|
| `OPEN_SOURCE` | 开源项目、已复现或计划二次开发的公开项目 | 通过复现/实现门禁后，可写覆盖需求、设计、实现和验证的完整流程 |
| `SELF_OWNED` | 用户独立或合作完成的个人项目 | 按真实角色，可写端到端设计与实现 |
| `INTERNSHIP` | 实习期间参与的公司或团队项目 | 只写用户负责的高价值环节或一个核心闭环 |
| `OTHER` | 课程、团队、外包或来源尚不能归入前三类 | 先按实习项目的聚焦边界处理，再根据角色证据收紧或放宽 |

用户原话未明确 `project_origin` 时，只问一个问题：“这个项目属于哪一种：开源项目、你自己的个人项目，还是实习项目？”用户回答前不得分析候选简历要点、提供示例或改写正文。一次涉及多个项目时逐项目记录来源，不得用一个项目的来源覆盖其余项目。

不生成或改写简历要点时，不强制追问 `project_origin`。例如只分析代码、只生成学习路径、只拷打用户已提供的要点或只做模拟面试，可按该步骤的最小输入继续。

`ARTIFACT` 执行沿用 manifest 的 `mode` 字段存储 `source_mode`，顶层 `project_origin` 存储项目来源。存在 `current_artifacts.resume`、`resume_clean` 或任一 `claims[].resume_text` 时，`project_origin` 必须存在并通过 `scripts/validate_manifest.py` 校验。只有分析、不涉及经历来源时可用 `UNDERSTAND_ONLY`。`task_scope` 属于本次执行计划，记录在对话与产物摘要中，不写入当前 manifest schema。

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

用户同时要求多个产物时，只组合对应范围，不自动插入分析、增强、拷打、学习或模拟面试。没有“只”字不等于完整流程；“帮我写简历”“分析这个项目”“准备一轮模拟面试”分别默认最小对应范围。只有明确表达“全部、完整、端到端”才选 `FULL_PIPELINE`。

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

缺少最小输入时，一次只问一个区分度最高的问题。不得把“补齐输入”改写成自动执行未请求的前置阶段；确实必须扩大范围时，先说明新增阶段、原因和产物并等待确认。完成所选范围后立即停止，只展示结果、风险和可选下一步，不自动执行可选下一步。

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
| 异常处理 | [failure-recovery.md](references/failure-recovery.md) |

## 工作流

### Phase 0：路由、初始化与范围确认

1. 从用户原话提取 `task_scope`，再判断必要的 `source_mode`、目标岗位、时间约束和期望产物。
2. 若范围含简历生成或改写，从用户原话提取 `project_origin`；未明确时进入下方来源检查点并停止。
3. 列出本次会执行的阶段、明确跳过的阶段和停止点；显式“只/不要/不需要”是硬边界。
4. 确定输出语言：用户明确指定 > 用户当前使用的语言 > 默认中文；仅在范围含代码分析时确认扫描范围与跳过目录。
5. 单个 `*_ONLY` 默认 `DIRECT`：在对话中交付，不创建分析目录或 manifest。用户明确要求落盘、说“开始学习”而触发 HTML，或多个阶段需共享事实状态时，切换为 `ARTIFACT`。
6. `ARTIFACT` 执行才在被分析项目根目录创建 `{项目名}-analysis/`，并按 `references/evidence-manifest.schema.json` 初始化 `evidence-manifest.json`。检测到 `schema_version=1.0` 先运行 `python scripts/migrate_manifest.py <manifest> --output <临时文件>`，校验迁移结果并让用户确认差异后原子替换；其他旧版本停止并报告不支持。`1.1` 版本先运行 `python scripts/validate_manifest.py <manifest>`，通过后增量更新。校验只缺 `project_origin` 时，先询问项目来源、写入用户回答并重新校验，不得猜测。

🔴 CHECKPOINT · PROJECT ORIGIN · 🛑 STOP

仅在任务包含简历生成或改写且 `project_origin` 缺失时触发。只询问项目属于开源项目、个人项目还是实习项目，然后停止本轮简历处理；不得同时追问角色、数字、技术细节，不得先给“参考版本”。

🔴 CHECKPOINT · MODE & SCOPE

展示 `source_mode`、`project_origin`（简历相关任务）、`task_scope`、执行阶段、停止点、预计产物和风险路径后暂停。用户已明确给出单步骤边界、项目来源且不涉及写代码或范围扩张时，可直接执行；`FULL_PIPELINE` 或组合多个范围时等待确认。用户已授权自动完成时写入自动确认记录并继续，但自动确认不能替代缺失的项目来源。

### 阶段门禁

进入每个 Phase 前检查：该 Phase 是否在 `task_scope` 中，或是否属于已确认的 `FULL_PIPELINE` 路径。否则跳过，不加载该阶段资源、不生成该阶段产物，也不因发现风险而自动追加该阶段。风险只记录为可选下一步。单步骤完成后立即结束。

下文所有“写入当前版本”“更新 `current_artifacts`”“更新 manifest”仅适用于 `ARTIFACT` 或 `FULL_PIPELINE`。`DIRECT` 执行把同等内容交付在对话中，不创建占位文件，也不为满足旧产物契约切换为多阶段流程。

### Phase 1：项目与业务链路分析

仅 `ANALYZE_ONLY`、含项目分析的组合范围或 `FULL_PIPELINE` 执行。

1. 使用代码分析引擎生成技术栈、架构、模块、入口和六维分析。
2. 使用业务链路提取器从入口追踪到最终消费者。
3. 先覆盖全仓库的业务域、平台能力、可靠性、性能、安全、测试与交付节点，再深挖最高价值链路；不得从单个提交或用户先提到的功能直接收敛为简历候选。
4. 为每条链路记录关键代码、工程能力、验证证据、缺口、价值评分和不确定项，形成跨链路价值节点排序。
5. 写入当前版本的项目分析与业务链路报告，更新 `current_artifacts.project_analysis`、`current_artifacts.business_chains` 和 manifest。

只读代码时优先使用仓库已有索引工具；存在 `.codegraph/` 时先用 CodeGraph。代码关系不确定时标记 `[待确认]`，不得猜测。

### Phase 2：贡献与来源映射

仅 `CONTRIBUTION_ONLY`、含贡献映射的组合范围或 `FULL_PIPELINE` 执行：

1. 逐条确认用户在高价值链路中的角色。
2. 代码证据决定候选“做了什么、难在哪里、产生什么结果”；Git 历史仅用于核对作者、时间、改动边界和演进顺序，不用于决定候选价值。
3. 从不同业务链路与工程类别建立候选池，按业务/架构关键性、工程深度、方案取舍、验证结果、岗位相关性和可追问深度排序；要求 N 条简历要点时至少比较 `max(6, 2N)` 个候选，仓库确实不足时记录扫描缺口。
4. 为候选声明标记来源、掌握度、证据和风险，将内容分为 `READY / NEEDS_EVIDENCE / NEEDS_TRAINING / NEEDS_BUILD / BLOCKED`。
5. 只有通过价值排序和角色门禁的候选才能写入核心 claim；写入当前版本的贡献映射，更新 `current_artifacts.contribution_map` 和 manifest。

🔴 CHECKPOINT · ROLE & SOURCE

展示候选经历、角色、来源、掌握度、风险和下一步。自动模式下继续，但完整保留风险记录。

### Phase 3：经历增强与项目迁移

仅 `ENHANCE_ONLY`、含经历增强的组合范围或 `FULL_PIPELINE` 执行。完整流程中符合任一条件时进入：模式为 `WEAK_INTERNSHIP` 或 `PROJECT_MIGRATION`；存在 `NEEDS_TRAINING/NEEDS_BUILD`；项目缺少可讲的工程闭环；用户要求补监控、容错、性能、测试、灰度等方案。

为 1-3 个最高价值缺口生成任务。默认只生成计划、复现、设计或完整叙事推演。只有 manifest 中 `code_mutation.authorized=true` 时才允许修改被分析项目，并将写入范围限制在 `code_mutation.scope`。写入当前版本的增强计划，更新 `current_artifacts.enhancement_plan`、掌握度和风险。

🔴 CHECKPOINT · CODE MUTATION

修改被分析项目代码前，单独展示写入目录、预计文件和验证命令并等待明确授权。“直接全部做完”、`auto_confirmed=true` 或允许生成分析产物都不等于代码修改授权。未授权时保持 `code_mutation.authorized=false`，自动降级为 `REPRODUCED`、`DESIGNED` 或 `NARRATIVE_READY`。

### Phase 4：STAR 简历

仅 `RESUME_ONLY`、含简历生成的组合范围或 `FULL_PIPELINE` 执行。

进入本阶段前必须已有明确 `project_origin`。缺失时回到 `CHECKPOINT · PROJECT ORIGIN`，只问来源并停止。`DIRECT + RESUME_ONLY` 在来源确认后可直接处理用户提供的要点或事实，不要求 manifest、候选池或全仓扫描；只对角色、数字口径、因果关系等会改变当前表述真实性的缺口做一次一个的最小追问。

按 `project_origin` 选择唯一叙事边界：

| 项目来源 | 允许的简历范围 | 强制限制 |
|---|---|---|
| `OPEN_SOURCE` | 用户已完成复现、二次开发或等价实现并达到 `L3/L4` 时，可将多条要点组织成需求理解、架构设计、核心实现、测试验证的完整流程 | 使用“基于…复现/改造/扩展/实现”等来源准确的动词；未实现或不理解的步骤不得写成个人成果，不得冒充原作者 |
| `SELF_OWNED` | 按用户真实角色，可写从需求拆解、方案选型、架构设计、核心实现到验证交付的端到端流程 | 合作完成的部分必须标明个人边界；只有计划或推演的环节不能写成已完成 |
| `INTERNSHIP` | 每条只聚焦一个有含金量的重要环节，或围绕同一业务目标形成的一个核心闭环 | 不得把整个产品、全系统架构或跨团队端到端流程写成个人成果；闭环可跨多个步骤，但这些步骤必须属于用户实际负责范围 |
| `OTHER` | 默认采用 `INTERNSHIP` 的聚焦边界 | 只有用户补充明确所有权和实现证据后，才能放宽为端到端表达 |

核心规则：

1. `ARTIFACT/FULL_PIPELINE` 只消费 manifest 中允许进入草稿的 claims，并直接沿用贡献映射阶段的 12 分 `candidate_value_score` 从高到低选择，不在简历阶段另建评分公式；任何未入选的合格候选分数更高时，必须替换较弱要点。`DIRECT` 只消费用户当前提供的事实，保持用户指定的要点范围，不建候选池。
2. 每条要点以一句紧凑表述按 `情境 -> 任务 -> 行动 -> 结果` 排列；情境与任务可压缩在同一分句，但四项均不可缺失，不用 `S/T/A/R` 标签机械分段。
3. 结果按唯一分支处理：有可信证据时写真实指标与口径；缺少可信指标时写 `[待补：{指标}从 __ 变为 __，变化 __%，口径/环境 __]`，并标记“待补数据，不可直接投递”；若同时输出稳妥版，只能用用户材料或 evidence 已确认的覆盖范围、正确性验证或工程闭环作为结果，不得保留占位符。连定性结果也未确认时，不生成所谓“可直接投递版”，只追问一个结果事实。仅知道“使用 Redis”时，不得推断缓存键、过期、回源、命中行为或数据库压力变化。
4. 高风险声明保留在草稿时，写入内部 claim ID 和风险，不在用户可见正文堆内部标签。提交文件数、增删行数、commit 大小和文档数量只属审计元数据，不能充当结果或含金量证明。
5. 生成当前版本简历，更新 `current_artifacts.resume`；最多 10 条，每条保持紧凑。
6. 中文成品执行术语本地化：使用“简历要点、意图、大语言模型、智能体、数据结构约束、检查点、行动与结果”等自然中文，不把 `Bullet`、`Intent`、`LLM`、`Agent`、`Schema`、`checkpoint`、`Action & Result` 当普通中文词混排；只为准确性保留必要的产品/框架/协议/行业缩写和真实代码标识符。
7. 发布前逐句检查；发现可翻译的通用英文术语或用 Git 规模冒充成果时自动改写一次，仍不合格则标记 `REVIEW_REQUIRED`，不得称为最终版。

🔴 CHECKPOINT · RESUME

展示简历、声明映射摘要和待验证项。只有 `FULL_PIPELINE` 或范围明确包含 `GRILL_ONLY` 时进入拷打；`RESUME_ONLY` 在此停止。

### Phase 5：简历要点逐条拷打

仅 `GRILL_ONLY`、含拷打的组合范围或 `FULL_PIPELINE` 执行。对每条被请求拷打的核心简历要点逐一执行事实、角色、实现、选型、验证和边界六层追问。交互时一次问一个；自动评估时根据现有代码、manifest 和用户材料做干跑，明确标记未获得用户回答的部分。

`ARTIFACT/FULL_PIPELINE` 从 `current_artifacts.resume` 读取当前简历并输出新版本拷打报告，更新 `current_artifacts.claim_grill_report`；`DIRECT + GRILL_ONLY` 直接读取用户提供的要点并在对话中拷打。完整流程存在 `RED` 时自动回退一次：角色冲突 -> Phase 2；实现不熟 -> Phase 3 或 Phase 6；数据无来源 -> Phase 4；边界不完整 -> Phase 3。

重测后仍为 `RED` 时：核心声明最终状态设为 `BLOCKED`；非核心声明移出最终简历、保留为训练材料，最终状态最高为 `TRAINING_REQUIRED`。

### Phase 6：风险驱动学习与交互页面

仅 `LEARNING_ONLY`、含学习路径的组合范围或 `FULL_PIPELINE` 执行。

1. 先确定 `learning_delivery`：用户明确说“不要网页/只要学习路径”时为 `MARKDOWN_ONLY`；用户说“开始学习/进入学习/生成学习网页/交互学习/HTML”时为 `LIGHT_HTML`；其余 `LEARNING_ONLY` 默认为 `MARKDOWN_ONLY`，`FULL_PIPELINE` 默认为 `MARKDOWN_AND_HTML`。显式拒绝 HTML 的表达优先级最高。
2. 根据“声明风险 x 面试概率 x 掌握缺口”排序学习任务，生成当前版本学习路径并更新 `current_artifacts.learning_path`。每份学习路径必须包含一个 Mermaid `flowchart` 架构图和一个 Mermaid `sequenceDiagram` 核心链路图，并为核心环节说明职责、输入、输出、上下游、关键文件、核心逻辑、设计决策、失败边界和达标标准。
3. Mermaid 节点与连线只能来自当前项目分析、业务链路或代码证据。关系不确定时使用虚线并在边标签写“待确认”；不得为图完整而猜测中间模块、调用方向或异步关系。
4. `LIGHT_HTML/MARKDOWN_AND_HTML` 从 `current_artifacts.learning_path` 生成版本化 `learning-interactive.html` 并更新 `current_artifacts.learning_interactive`，不得重新分析或改写事实。“开始学习”且当前学习路径缺失时，若已有项目分析则先在本 Phase 生成学习路径；连项目材料也缺失时只索取一个项目路径或学习材料。
5. HTML 固定浅色主题，按“系统全景 -> 核心链路 -> 相关环节详解 -> 随堂测验”组织。Mermaid 运行时加载失败时保留可读的 Mermaid 源码和文字链路，显示降级提示，不得留下空白图或静默跳过。
6. 生成 HTML 后检查桌面和移动端：导航可达、文字不溢出、图表非空、浅色对比度可读、测验可操作。可用浏览器自动化时截图验证；工具不可用时执行静态检查并明确标记未完成视觉验证。
7. 完成 Phase 6 后停止；不得因为用户开始学习而自动生成简历、话术、拷打或模拟面试。

### Phase 7A：分层话术

仅 `SCRIPT_ONLY`、含面试话术的组合范围或 `FULL_PIPELINE` 执行。为 `GREEN/YELLOW` 声明生成 15 秒、30 秒、2 分钟和深挖材料，写入当前版本话术并更新 `current_artifacts.interview_scripts`。

### Phase 7B：模拟面试

仅 `MOCK_INTERVIEW_ONLY`、含模拟面试的组合范围或 `FULL_PIPELINE` 执行。

1. `MOCK_INTERVIEW_ONLY` 只读取用户提供或指定的简历/项目摘要和目标岗位，不要求先生成贡献映射、拷打报告、学习路径或分层话术。
2. 按暖场、技术深挖、系统视角、收尾四阶段模拟面试，一次只问一个问题并等待用户实际回答。
3. 有现成风险清单时优先追问高风险声明；没有时根据简历内容直接提问，不自动生成学习路径。
4. 用户实际回答时生成面试反馈；`ARTIFACT/FULL_PIPELINE` 才写入当前版本面试报告并更新 `current_artifacts.interview_report`。

用户未实际回答时，不伪造面试得分；生成“待实战”问题集和预评分风险即可。

### Phase 8：最终质量门禁

仅 `QUALITY_CHECK_ONLY`、含质量检查的组合范围或 `FULL_PIPELINE` 执行。`QUALITY_CHECK_ONLY` 只检查用户提供或指定的现有产物，不要求补造缺失阶段；`FULL_PIPELINE` 运行全部八道门禁。

完整门禁检查来源、代码、角色、数字、抗追问、学习闭环、跨产物一致性和敏感信息。`FULL_PIPELINE` 判定最终状态前必须运行 `python scripts/validate_manifest.py <manifest> --analysis-dir <分析目录> --require-artifacts`，保证映射存在且文件真实可读；失败时不得给出 `INTERVIEW_READY`。`DIRECT + QUALITY_CHECK_ONLY` 给出范围化结论和未检查项，不调用 manifest 校验，也不宣称完整流程状态。

输出当前版本质量门禁报告并更新 `current_artifacts.quality_gate_report`，最终状态只能是 `BLOCKED`、`TRAINING_REQUIRED`、`REVIEW_REQUIRED`、`INTERVIEW_READY`。

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

异常处理按 [failure-recovery.md](references/failure-recovery.md) 执行：先按表一线修复，仍失败则降级。所有异常必须告知用户并写入风险记录，不得静默跳过。

## 反例黑名单

- 不要把代码仓库拥有的能力自动归为用户个人成果。
- 不要在项目来源未知时生成、改写或示范简历要点；先问来源并停止。
- 不要把实习项目写成用户独立完成的全产品或全系统流程；只写高价值环节或核心闭环。
- 不要按 Git 提交列表逐条生成简历，也不要把 commit hash、改动文件数、增删行数、提交次数或 ADR/文档数量写成核心成果。
- 不要凭 Redis、线程池、MQ 或索引推导虚假性能百分比，也不要把组件的典型工作方式推断为该项目实际采用的实现或结果。
- 不要把增强任务计划自动当作已完成成果。
- 不要生成缺少情境、个人任务、技术行动或结果中任一项的简历要点，也不要用 `S:`、`T:`、`A:`、`R:` 机械分段。
- 不要把待补占位符当作已验证结果；含 `__`、`[待补：...]` 或同类未填写标记的版本不得称为可投递或 `INTERVIEW_READY`。
- 不要一次向用户抛出多个面试问题；不要伪造模拟面试得分；不要覆盖已有产物或读取密钥、token、密码内容。
- 不要把分析或“全部做完”的授权解释为修改目标项目代码的授权。
- 不要因 skill 具备全部能力就在一次调用中依次执行全部能力；完成用户指定步骤后不要自动进入“合理的下一步”。
- 不要绕过 `current_artifacts` 按固定文件名读取可能过期的产物；不要跳过最终跨产物一致性检查。
- 中文成品不要用 `Bullet 1`、`Action & Result`、`Claim`、`Intent`、`Agent`、`Schema`、`checkpoint` 等英文作普通标题或叙述词；优先写“简历要点、行动与结果、声明、意图、智能体、数据结构约束、检查点”。

## 完成标准

单步骤交付完成：用户请求的范围已经完成；没有执行或生成范围外阶段与产物；影响当前结果真实性的风险已明确标记；已在约定停止点结束。

只有 `FULL_PIPELINE` 同时满足以下条件才算完整交付：用户要求的路径已完成；所有生成文件真实存在；核心声明可映射到 manifest；每个风险有明确状态和下一步；最终质量门禁已执行；对话中给出产物路径和最终状态。
