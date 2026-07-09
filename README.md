# repo-to-resume

代码仓库 → STAR 简历 → 模拟面试，一站式项目面试准备工具。

## 是什么

`repo-to-resume` 是一个 AI Skill，自动分析你的项目代码，生成面试用的 STAR 简历、模块级学习路径，并进行多轮模拟面试拷打。纯代码驱动，不依赖 README 或外部文档。

## 能做什么

| 场景 | 用法 |
|------|------|
| 分析本地项目 | 「帮我分析 `C:\work\my-project`」 |
| 分析 GitHub 仓库 | 「分析 https://github.com/xxx/yyy」 |
| 生成面试简历 | 「给这个项目写一份 STAR 简历」 |
| 准备项目面试 | 「我明天要面试，帮我准备这个项目的面试」 |
| 快速理解陌生代码 | 「我刚接手这个项目，帮我快速看懂」 |
| 只分析某一部分 | 「只看 `src/core/` 目录」 |

## 四步流程

```
Step 0: 项目概览 → 深度分析（6 维度）
    ↓
Step 1: STAR 简历（一页纸，≤10 条 Action）
    ↓
Step 2: 学习路径（全景图 → 模块详解 → 跨模块面试题）
    ↓
Step 3: 模拟面试（暖场 → 技术深挖 → 系统视角 → 收尾 + 评分报告）
```

每步产出后都会停下来等你确认，你可以随时说「只看 XX」「跳过这步」「重新生成」。

## 架构

主 Skill 负责编排流程，5 个子模块各司其职：

| 子模块 | 职责 |
|--------|------|
| `code-analysis-engine` | 扫描结构、识别架构、6 维度深度分析、提取亮点 |
| `star-resume-generator` | 套 STAR 框架生成一页纸简历 |
| `learning-path-generator` | 三层递进：全景图 → 模块详解 → 跨模块面试题 |
| `interactive-learning-template` | 单文件 HTML 交互式学习页面 |
| `mock-interviewer` | 出题 + 追问梯度 + 行为锚定评分 + 复习行动清单 |

## 目录结构

```
repo-to-resume/
├── SKILL.md                                  # Skill 主文件（编排流程 + 卡片式输出规范）
├── skillhub.json                             # Skill 注册信息
├── evals/
│   └── evals.json                            # 评估用例
└── references/
    ├── code-analysis-engine.md               # 代码分析引擎
    ├── star-resume-generator.md              # STAR 简历生成器
    ├── star-framework.md                     # STAR 框架 + 量化估算规则
    ├── learning-path-generator.md            # 学习路径生成器
    ├── interactive-learning-template.md      # 交互式学习 HTML 模板
    ├── mock-interviewer.md                   # 模拟面试官
    └── interview-question-templates.md       # 通用面试题库
```

## 边界约束

- 纯代码分析，不依赖外部信息
- 不碰敏感信息（密钥、token、密码）
- 不分析第三方依赖源码（node_modules、vendor 等）
- 不分析测试代码和 Git 历史
- 全语言通用，AI 自动识别技术栈
