# repo-to-resume

把代码仓库、项目经历和现有简历整理成可验证、可学习、能经住面试追问的求职材料。

本项目采用开放的 [Agent Skills 规范](https://agentskills.io/specification)，可安装到任何兼容的智能体，不依赖特定厂商或模型。

## 有什么用

- 看懂项目架构、核心模块和端到端业务链路。
- 区分项目能力、团队成果与个人贡献，避免冒领。
- 把薄弱实习、自研或开源复现补成可验证的工程经历。
- 生成或修改 STAR 简历要点，并审查现有 PDF、DOCX、LaTeX 简历。
- 逐条拷打简历声明，检查事实、角色、实现、数据与失败边界。
- 生成项目学习路径、面试话术，并进行一次一题的模拟面试。

它既能只完成一个步骤，也能在你明确要求时执行完整流程。单项任务完成后会停止，不会自动扩展到未请求的步骤。

## 技能入口

| 技能 | 用途 |
|---|---|
| `$project-analyzer` | 分析架构、模块和业务链路 |
| `$contribution-mapper` | 确认个人角色与贡献证据 |
| `$experience-enhancer` | 设计可执行、可验证的项目增强任务 |
| `$resume-writer` | 生成简历要点或保存修订版 |
| `$resume-auditor` | 只读审查简历内容与版式 |
| `$claim-grill` | 一次一问地验证单条简历声明 |
| `$project-learning` | 生成带 Mermaid 的项目学习路径 |
| `$interview-script` | 准备 15 秒、30 秒和 2 分钟面试话术 |
| `$mock-interview` | 开展一次一题的项目模拟面试 |
| `$resume-pipeline` | 组合多个任务或执行完整流程 |

只安装根技能时也可以使用 `$repo-to-resume` 作为总入口。

## 安装

需要 Git、Python 3.9+ 和一个支持 Agent Skills 的智能体。

```bash
git clone https://github.com/Brave-Maker/repo-to-resume.git
cd repo-to-resume
python scripts/install_skills.py --target ../your-project/.agents/skills
```

把 `../your-project/.agents/skills` 替换为实际的 skills 目录；不同智能体可以使用不同路径。安装后新建会话，让智能体重新发现技能。

只安装部分技能：

```bash
python scripts/install_skills.py --target ../your-project/.agents/skills \
  --skill project-analyzer \
  --skill resume-writer
```

只安装总入口：

```bash
python scripts/install_skills.py --target ../your-project/.agents/skills --skill repo-to-resume
```

## 如何使用

直接调用对应技能，并说明材料、目标、范围和排除项：

```text
材料：<仓库路径、Git URL、简历文件或工作记录>
目标：<本次要得到什么>
范围：<需要处理的目录、模块或要点>
排除：<不要执行的步骤>
背景：<目标岗位；改简历时说明项目来源>
```

常用示例：

```text
$project-analyzer 只分析 C:\work\shop 的订单链路，不写简历。

$resume-writer 这是我的个人项目。根据已确认事实写 3 条 Java 后端简历要点，不补数字。

$resume-auditor 只读检查 resume.pdf 的 STAR、水项和加粗，不修改文件。

$claim-grill 拷打这条“使用 Redis 将接口性能提升 80%”的声明，一次只问一个问题。

$resume-pipeline 分析 C:\work\shop，生成简历和面试话术，跳过模拟面试。
```

不确定入口时可以直接用自然语言描述需求；安装完整技能集后，智能体会根据技能描述选择对应入口。

## 使用边界

- 生成或事实性改写简历前，需要确认项目属于开源、个人还是实习项目。
- “优化简历”默认只读审查；只有明确要求修改、写回或保存修订版时才写文件，并且不覆盖原文件。
- “全部做完”不代表允许修改目标项目源码；源码写入需要单独授权。
- 不根据技术名词编造性能数字，不把仓库已有能力直接算作个人贡献。
- 没有真实面试回答时，不虚构模拟面试得分。

## 更新与卸载

```bash
git pull --ff-only
python scripts/install_skills.py --target ../your-project/.agents/skills --replace
```

```bash
python scripts/install_skills.py --target ../your-project/.agents/skills --uninstall
```

安装器只更新或删除带有本项目标记的技能目录，不会覆盖同名的用户自有技能。

## 验证

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate_skill.ps1
```

该命令会检查技能结构、评估断言、证据清单契约和可移植安装结果。
