# repo-to-resume

把代码、项目和经历加工成一套**可学习、可表达、可追问、可迭代**的求职材料。

它既能只完成一个明确步骤，也能在用户明确要求时执行完整准备流程。你可以让它只分析业务链路、只改一条简历、只做压力追问或只进行模拟面试；它不会因为具备后续能力就自动把所有步骤一次做完。

完整流程会理解项目与业务链路，区分项目能力、个人贡献、复现成果、方案设计和叙事补全，再生成简历、学习路径、面试话术与质量报告。即使没有正式实习，也可以从自研项目、开源项目或其他项目中提炼可讲内容。

## 快速开始

1. 按[安装说明](#安装)把技能集安装到当前 Agent 支持的 skills 目录，并新建会话。
2. 单项任务直接调用对应窄技能；组合任务或完整流程调用 `$resume-pipeline`。
3. 在提示词中给出材料、目标产物和明确排除项。

```text
$project-analyzer 只分析 C:\work\my-project 的订单链路，不写简历。

$resume-writer 这是我的个人项目。根据这些已确认事实写 3 条 Java 后端简历要点。

$resume-auditor 只读检查 C:\resume\resume.pdf 的 STAR、水项和加粗，不修改文件。

$resume-pipeline 分析 C:\work\my-project，生成简历和面试话术；跳过模拟面试。
```

最稳妥的提示结构是：

```text
材料：<仓库路径、Git URL、简历文件或工作记录>
目标：<本次唯一产物，或明确列出的多个产物>
范围：<需要读取的目录、模块、要点或面试题量>
排除：<不要执行的步骤>
背景：<目标岗位；涉及简历改写时说明项目来源>
```

## Agent Skills 技能集

本项目遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)。完整安装后会发现 10 个窄入口；单一任务不再加载完整根流程：

| 技能 | 负责内容 | 典型请求 |
|---|---|---|
| `$project-analyzer` | 项目架构、模块和端到端业务链 | “帮我看懂这个项目的架构和请求链路” |
| `$contribution-mapper` | 个人角色、来源与贡献归因 | “区分哪些是团队成果、哪些确实是我做的” |
| `$experience-enhancer` | 可执行、可验证的经历增强任务 | “这段实习太弱，设计两个可以验证的补强任务” |
| `$resume-writer` | 简历要点、完整项目经历和授权后的版本化修订 | “把这些事实改成 3 条简历要点” |
| `$claim-grill` | 一次一问的单条声明压力验证 | “只拷打这条 Redis 优化声明” |
| `$project-learning` | Mermaid 学习路径和浅色交互学习页 | “生成分模块学习路径和达标测验” |
| `$interview-script` | 15 秒、30 秒、2 分钟与深挖话术 | “准备项目介绍的 30 秒和 2 分钟版本” |
| `$mock-interview` | 一次一题模拟面试和真实回答评分 | “现在开始模拟面试，一次问一题” |
| `$resume-auditor` | 只读 STAR、水项、加粗和跨产物质量审查 | “检查 PDF 简历，但不要修改” |
| `$resume-pipeline` | 明确多阶段或完整流程的证据链编排 | “分析项目、写简历并准备话术” |

根 `$repo-to-resume` 保留为单一总入口，适合只安装一个技能或继续使用原有调用方式。

### 如何选择入口

- **只有一个产物**：直接使用对应窄技能，完成后立即停止。
- **同一次请求包含两个及以上产物**：使用 `$resume-pipeline`，它只组合点名的步骤。
- **明确要求全部做完或端到端准备**：使用 `$resume-pipeline` 的完整流程。
- **只安装根技能**：使用 `$repo-to-resume` 总入口；完整技能集则优先使用上面的窄入口。

“完整项目经历”描述的是简历交付格式，不会触发完整流程；“帮我看懂项目”默认进入项目分析，只有明确要求学习路径、模块课程、测验或学习网页时才进入项目学习。

## 三轴路由

每次调用会分别判断三件事：

1. **材料模式**：当前材料和工作状态，决定处理路径。
2. **项目来源**：项目是开源、个人还是实习项目，决定简历能覆盖的职责范围。
3. **本次任务范围**：用户这次具体要什么，决定执行哪些步骤以及在哪里停止。

### 材料来源

| 你的情况 | `source_mode` | 主要处理方式 |
|---|---|---|
| 有真实实习和明确产出 | `REAL_INTERNSHIP` | 提取贡献、生成简历、逐条拷打 |
| 有实习，但工作零散或角色模糊 | `WEAK_INTERNSHIP` | 补齐业务链路、增强经历、校准表达 |
| 没有实习，但有自己完成的项目 | `SELF_PROJECT` | 分析项目、补工程闭环、形成项目经历 |
| 想基于开源、团队或他人项目准备经历 | `PROJECT_MIGRATION` | 区分来源，完成复现、设计或叙事迁移 |
| 已有简历，希望查漏洞和补强 | `EXISTING_RESUME` | 反查证据、压力追问、修正高风险表述 |

`EXISTING_RESUME` 只说明材料来自已有简历，不代表项目来源已经明确。凡是生成或改写简历要点，系统都会先确认：这是开源项目、个人项目还是实习项目。用户回答前不会先给示例或改写稿。

### 项目来源

| 项目来源 | `project_origin` | 简历范围 |
|---|---|---|
| 已复现或二次开发的开源项目 | `OPEN_SOURCE` | 有实现与掌握证据后，可写需求、设计、实现、验证的完整流程，但不冒充原作者 |
| 自己独立或合作完成的项目 | `SELF_OWNED` | 按真实角色可写端到端设计与实现 |
| 实习期间参与的团队项目 | `INTERNSHIP` | 只写负责的高价值环节或核心闭环，如意图识别链路、知识反馈闭环 |
| 课程、团队或其他来源 | `OTHER` | 默认按实习项目的聚焦边界处理，直到所有权得到证实 |

### 本次任务范围

| 你这次要做什么 | `task_scope` | 执行范围 |
|---|---|---|
| 只分析项目或核心业务链路 | `ANALYZE_ONLY` | 只执行项目分析 |
| 只确认个人贡献和内容归因 | `CONTRIBUTION_ONLY` | 只执行贡献映射 |
| 只补工程闭环或复现计划 | `ENHANCE_ONLY` | 只执行经历增强 |
| 只写简历或修改一条表述 | `RESUME_ONLY` | 只执行简历处理 |
| 只检查某条简历能否经住追问 | `GRILL_ONLY` | 只执行逐条拷打 |
| 只生成风险驱动的学习路线，或开始学习 | `LEARNING_ONLY` | 生成带 Mermaid 的学习路径；“开始学习”时生成浅色交互 HTML |
| 只准备项目面试话术 | `SCRIPT_ONLY` | 只生成分层话术 |
| 只进行一轮模拟面试 | `MOCK_INTERVIEW_ONLY` | 只执行模拟面试 |
| 只检查现有材料的质量 | `QUALITY_CHECK_ONLY` | 只检查已提供产物 |
| 明确要求全部做完或端到端准备 | `FULL_PIPELINE` | 执行完整流程 |

支持本地目录、Git 仓库、压缩包、已有简历和零散工作记录。分析代码时会优先读取真实入口、调用链、数据流和工程约束，不依赖一份写得漂亮的 README。

单步骤默认直接在对话中交付，不创建分析目录或 `evidence-manifest.json`。缺少输入时只索取当前步骤所需的最小材料；简历任务缺少项目来源时，只询问来源并停止。如果确实需要扩大范围，会先说明原因并等待确认。多个明确任务可以组合，例如“改两条简历并准备话术”，但不会自动插入未请求的分析、增强、拷打或学习步骤。

### 交付模式

| 模式 | 适用场景 | 写入行为 |
|---|---|---|
| `DIRECT` | 单步骤、只需对话结果 | 不创建分析目录或 manifest |
| `FILE_ARTIFACT` | 明确要求保存学习 Markdown 或生成 HTML | 创建版本化学习文件，不创建 manifest |
| `FILE_REVISION` | 明确授权修改现有简历文件 | 创建相邻的 `-vN` 修订版，不覆盖原文件 |
| `ARTIFACT` | 多阶段任务需要共享事实状态 | 创建版本化产物并更新 `evidence-manifest.json` |

请求生成文件只授权对应产物，不授权修改目标项目源码；请求“优化简历”默认仍是只读审查，只有“修改、写回、保存修订版”等明确表达才构成文件写入授权。

## 它解决什么问题

- **项目看不懂**：从入口追踪到最终消费者，建立技术结构和核心业务链路。
- **不知道自己做了什么**：将团队成果、项目能力和个人贡献拆开，找到可表达的价值节点。
- **没有传统实习经历**：允许通过自研、复现、方案设计和叙事补全构建候选经历，而不是直接拒绝服务。
- **简历经不起追问**：对每条核心简历要点进行事实、角色、实现、选型、验证和边界六层追问。
- **会写但不会讲**：按风险生成学习任务，以及 15 秒、30 秒、2 分钟和深挖版本的话术。
- **产物前后矛盾**：用统一证据清单串联分析、简历、拷打、学习和面试材料。

## 工作流程

### 单步骤

```text
识别 task_scope
   ↓
简历任务确认 project_origin；缺失则询问并停止
   ↓
检查最小输入；缺什么只问什么
   ↓
执行指定 Phase
   ↓
到达停止点，交付结果与风险
```

### 完整流程

```text
Phase 0  识别材料模式、项目来源、任务范围和授权边界
   ↓
Phase 1  分析技术结构与核心业务链路
   ↓
Phase 2  映射个人贡献、内容来源与掌握程度
   ↓
Phase 3  复现、增强或设计缺失的工程闭环
   ↓
Phase 4  生成 STAR 经历与简历要点
   ↓
Phase 5  对核心声明执行六层压力追问
   ↓
Phase 6  生成带 Mermaid 架构/链路图的学习路径；“开始学习”时生成浅色交互学习页
   ↓
Phase 7A 生成分层话术
   ↓
Phase 7B 进行模拟面试
   ↓
Phase 8  执行最终质量门禁
```

只有用户明确要求“全部做完”“完整准备”或“端到端处理”时才进入完整流程。没有“只”字不等于完整授权：“帮我写简历”“分析这个项目”“准备一轮模拟面试”仍分别按最小范围执行。完整流程会保留每个检查点的记录，并在关键授权处等待确认。

## 核心机制

### 证据清单

`evidence-manifest.json` 是多阶段和完整流程的事实索引。单步骤对话交付不强制创建它。启用后，每项声明都会记录：

- 内容来自用户亲历、代码事实、团队成果、外部项目，还是推演补全；
- 用户承担的角色、当前掌握程度和可用证据；
- 当前风险与下一步动作；
- 下游应该读取的最新产物版本。

只要 manifest 含有简历产物或 `resume_text`，就必须同时记录 `project_origin`；语义校验器会拒绝无来源简历。

这使项目迁移和叙事补全可以继续进行，同时不会把“仓库里存在”直接等同于“用户本人已经完成并掌握”。

### 四类增强结果

| 状态 | 含义 |
|---|---|
| `IMPLEMENTED` | 已实际实现并完成验证 |
| `REPRODUCED` | 已完成最小复现或等价实验 |
| `DESIGNED` | 已形成可解释、可落地的完整方案 |
| `NARRATIVE_READY` | 已补齐叙事与学习材料，但仍需要训练或验证 |

### 质量状态

最终只会给出以下四种状态之一：

| 状态 | 含义 |
|---|---|
| `INTERVIEW_READY` | 核心声明已具备证据、掌握度和抗追问能力 |
| `REVIEW_REQUIRED` | 基本可用，但仍有需要人工确认的内容 |
| `TRAINING_REQUIRED` | 可以继续作为训练材料，暂不建议直接对外使用 |
| `BLOCKED` | 核心事实或角色冲突尚未解决 |

高风险内容不会被自动删除，但也不会在缺少依据时被错误标成 `INTERVIEW_READY`。

## 主要产物

完整流程和需要落盘的多阶段任务会在目标项目中创建 `{项目名}-analysis/`，并按需生成：

```text
{项目名}-analysis/
|- project-analysis.md          # 架构、技术栈与六维分析
|- business-chains.md           # 核心业务链路和价值节点
|- contribution-map.md          # 个人贡献、来源与掌握度映射
|- evidence-manifest.json       # 跨产物事实索引和状态清单
|- enhancement-plan.md          # 复现、增强或方案设计任务
|- resume.md                    # STAR 经历与简历要点
|- claim-grill-report.md        # 六层追问和漏洞分级
|- learning-path.md             # 含 Mermaid 架构图、核心链路和环节详解的学习路径
|- learning-interactive.html    # 固定浅色的交互学习页面
|- interview-scripts.md         # 分层面试话术
|- interview-report.md          # 基于实际回答的面试反馈
`- quality-gate-report.md       # 最终质量状态和剩余风险
```

单步骤默认不创建整套目录，只生成用户明确要求的结果；用户要求落盘时才写入对应产物。普通产物不会覆盖旧文件，而是保存新版本；manifest 始终指向当前有效版本。

## 安装

前置条件：Git、Python 3.9+，以及一个支持 [Agent Skills 开放格式](https://agentskills.io/) 的智能体。安装器不调用任何特定厂商 CLI，只把每个技能打包为独立、可移植的 `SKILL.md + references/ + scripts/` 目录。

### 安装完整技能集

1. 将仓库克隆到任意源码目录：

```powershell
git clone https://github.com/Brave-Maker/repo-to-resume.git "$env:USERPROFILE\repo-to-resume"
```

macOS/Linux 使用：

```bash
git clone https://github.com/Brave-Maker/repo-to-resume.git "$HOME/repo-to-resume"
```

2. 选择当前 Agent 的 skills 目录作为 `--target`。项目级通用目录可使用 `.agents/skills`：

```powershell
python "$env:USERPROFILE\repo-to-resume\scripts\install_skills.py" --target ".agents\skills"
```

```bash
python3 "$HOME/repo-to-resume/scripts/install_skills.py" --target ".agents/skills"
```

用户级目录和其他项目级目录由具体 Agent 决定，直接把对应路径传给 `--target` 即可。安装后新建会话，让宿主重新发现技能。

### 只安装部分技能

`--skill` 可以重复使用；不传时默认安装根入口与全部 10 个窄技能：

```powershell
python scripts/install_skills.py --target ".agents\skills" --skill project-analyzer --skill resume-writer
```

只需要总入口时：

```powershell
python scripts/install_skills.py --target ".agents\skills" --skill repo-to-resume
```

### 更新与卸载

仓库发布新版本后拉取源码，并只替换由本安装器管理的技能目录：

```powershell
git -C "$env:USERPROFILE\repo-to-resume" pull --ff-only
python "$env:USERPROFILE\repo-to-resume\scripts\install_skills.py" --target ".agents\skills" --replace
```

卸载同样只处理带有本项目安装标记的目录，不会删除源码仓库，也不会触碰同一目录下的其他技能：

```powershell
python "$env:USERPROFILE\repo-to-resume\scripts\install_skills.py" --target ".agents\skills" --uninstall
```

安装器拒绝覆盖没有本项目标记的同名目录；遇到该错误时先移动现有目录，或改用另一个 `--target`。

## 使用

### 单技能示例

```text
$project-analyzer 分析 C:\work\shop 的 src/order/，追踪两条核心链路；跳过 tests 和 vendor。

$contribution-mapper 这是 mentor 给的整体方案，我只实现了退款状态机。帮我做贡献归因。

$experience-enhancer 我只有一个基础 CRUD 项目，目标是 Java 后端，用一周补两个可验证的工程能力。

$resume-writer 这是实习项目。只把“退款状态机”改成一条中文 STAR 简历要点，不要补数字。

$claim-grill 逐层追问这条“使用 Redis 将接口性能提升 80%”的声明，一次只问一个问题。

$project-learning 根据这个仓库生成 Mermaid 架构图、核心请求链路、模块学习顺序和达标测验。

$interview-script 根据已确认的项目事实生成 15 秒、30 秒和 2 分钟介绍，不做模拟面试。

$mock-interview 基于 resume.pdf 面试 Java 后端，一次只问一题；我提前结束时不要给总分。

$resume-auditor 只读检查 resume.tex 和 PDF，按 STAR、水项、加粗的顺序给建议，不写回。
```

### 组合与完整流程

```text
$resume-pipeline 这是我的个人项目。只生成 3 条简历要点，并准备对应的 30 秒和 2 分钟话术。

$resume-pipeline 分析 C:\work\my-project，目标岗位是 Java 后端，完整完成整套材料。
```

组合请求不会自动补齐未点名阶段。例如“改两条简历并准备话术”不会插入项目分析、经历增强、逐条拷打、学习路径或模拟面试。

### 自然语言触发

```text
帮我分析这个 GitHub 项目，提炼成可面试的项目经历。

我没有正式实习，想基于这个开源项目做复现、补学习材料和简历话术。

这是我实习项目的现有简历，帮我逐条找漏洞，补齐证据和面试回答。

我只想快速看懂这个项目的核心业务链路，不需要生成简历或学习路径。

项目分析和学习路径已经生成，现在开始学习。
```

需要限制范围时直接说明任务、目录、模块或目标链路，例如“只分析 `src/order/`”“只改这一条”或“只模拟面试”。系统会把“只、不要、不需要”视为硬边界，并在完成指定步骤后停止。

## 安全与授权边界

- 默认只读取目标项目并生成分析材料，不读取或展示密钥、Token、密码等敏感内容。
- “全部做完”只授权执行完整准备流程，**不等于授权修改目标项目源码**。
- 修改源码前必须单独展示写入范围、预计文件和验证命令，并取得明确授权。
- 未经实际回答，不会虚构模拟面试得分；此时只生成待实战问题集和预评估风险。
- 估算数据会保留口径和来源，不会仅凭 Redis、MQ、线程池等技术名词编造性能百分比。
- 远程 Git 仓库如需检出，只使用系统临时目录；单步骤分析不会在目标仓库创建报告或索引。
- 交互学习页使用固定浅色模板；Mermaid 无法加载时保留源码和文字链路，不留下空白图。

## 仓库结构

```text
repo-to-resume/
|- skill-collection.json           # 宿主无关的技能集合与版本清单
|- skills/                         # 10 个可独立发现的 Agent Skills 源技能
|- SKILL.md                       # 主流程、路由与行为契约
|- references/                    # 分析、包装、拷打和质量门禁模块
|- scripts/
|  |- install_skills.py           # 安装到任意 Agent 的 skills 目录
|  |- validate_manifest.py        # manifest 数据结构与语义校验
|  |- migrate_manifest.py         # 旧版 manifest 迁移
|  |- run_evals.py                # 评估断言执行器
|  |- test_contracts.py           # 负向契约测试
|  |- test_skill_collection.py    # 11 个可移植技能包与安装契约
|  `- validate_skill.ps1          # 一键仓库自检
|- evals/                          # 评估配置、manifest 样例与回归场景
|- artifacts/                      # Darwin 优化与验证结果卡
`- test-prompts.json               # 根兼容入口的真实前向测试提示词
```

## 验证

在仓库根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate_skill.ps1
```

单独校验生成的证据清单：

```powershell
python scripts/validate_manifest.py <manifest路径> --analysis-dir <分析目录> --require-artifacts
```

当前回归套件覆盖 6 个代表性场景，以及来源门禁、弱实习、项目迁移、现有简历、范围路由、版本化产物、中文输出一致性和未授权源码修改等关键路径。`test-prompts.json` 还包含“来源未知时停止、开源/个人项目允许真实全流程、实习项目聚焦高价值环节或核心闭环”等前向场景。具体断言数量以 `scripts/validate_skill.ps1` 的输出为准。

当前版本预期结果：

```text
Manifest validation passed
Eval assertions: 83 passed, 0 failed
Contract tests: 18 passed, 0 failed
Agent Skills collection contracts: 11 skills passed
```

每个 `skills/<name>/test-prompts.json` 同时维护该技能的正向、边界和负向提示。修改触发词、交付模式或停止规则时，应同步新增最接近冲突边界的测试提示，而不是只修改说明文字。

## 常见问题

### 为什么只让我确认项目来源，没有直接写简历？

生成或事实性改写简历前必须区分开源、个人和实习项目。来源决定可以使用的职责动词与归因范围；确认前不会先生成看似可用的草稿。

### “优化简历”会直接修改文件吗？

不会。默认由 `$resume-auditor` 只读审查。只有明确要求修改、写回或保存修订版时，才由 `$resume-writer` 创建相邻的 `-vN` 文件；原文件不会被覆盖。

### `$claim-grill` 和 `$mock-interview` 有什么区别？

`$claim-grill` 聚焦一条简历声明的事实、角色、实现、选型、验证和边界；`$mock-interview` 基于整份材料进行一次一题的完整面试。没有用户真实回答时，两者都不会虚构得分。

### 为什么单步骤没有生成 `evidence-manifest.json`？

这是预期行为。`DIRECT` 只交付当前结果；只有多个阶段需要共享事实和版本状态时才启用 `ARTIFACT` 与 manifest。

## 设计目标

`repo-to-resume` 的目标不是替用户制造一句听起来漂亮但无法解释的话，而是把可用素材一路加工到“知道来源、讲得清实现、答得住追问、明白剩余风险”的状态。开源或个人项目可以在真实掌握范围内讲完整设计与实现；实习项目聚焦个人负责的高价值环节或核心闭环。没有证据或掌握度时，系统会继续给出复现、学习和训练路径，直到内容具备可用条件。
