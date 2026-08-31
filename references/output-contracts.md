# 对话输出契约

本模块定义各阶段在对话中的简洁交付格式。文件正文完整写入磁盘，对话只展示摘要和必要的展开内容。

## 通用规则

- 第一行展示动作、文件名和 1-2 个核心指标。
- 完整正文较长时放入 `<details>`；文件中的标题层级不变，对话嵌入时整体降两级。
- 二维映射用表格，行动项用列表。
- 不把内部执行日志、manifest 全量 JSON 或敏感路径内容直接展示。
- 每个检查点明确显示“等待确认”或“已按自动授权继续”。
- 普通产物使用 `-vN` 保留旧版；`evidence-manifest.json` 固定为当前状态，旧版进入 `history/`。
- 用户使用中文或未指定语言时，标题和叙述以自然中文为主；内部状态可用反引号保留，但先给出中文含义。用户明确要求英文时统一使用英文。
- 中文对话中使用“简历要点、声明、智能体、大语言模型、意图、检查点”，不使用 `Bullet`、`Claim`、`Agent`、`LLM`、`Intent`、`checkpoint` 充当普通叙述词。

## 模式与范围

```markdown
> 模式已确定 · `{mode}` · 扫描范围 `{scope}`

- 已有材料：{材料}
- 目标产物：{产物}
- 高风险路径：{有/无，一句话}
- 跳过目录：{目录}
```

## 项目分析

`DIRECT + ANALYZE_ONLY` 使用：

```markdown
> 项目分析完成 · 范围 `{scope}` · 未创建分析文件

| 指标 | 结果 |
|---|---|
| 技术栈 | {内容} |
| 核心链路 | {N} 条 |
| 高价值节点 | {N} 个 |
| 不确定关系 | {N} 个 |

**最高价值链路**：{一句话数据流}
```

`ARTIFACT/FULL_PIPELINE` 使用：

```markdown
> 项目分析完成 · `{current_artifacts.project_analysis}` / `{current_artifacts.business_chains}`

| 指标 | 结果 |
|---|---|
| 技术栈 | {内容} |
| 核心链路 | {N} 条 |
| 高价值节点 | {N} 个 |
| 不确定关系 | {N} 个 |

**最高价值链路**：{一句话数据流}
```

## 贡献映射

`DIRECT + CONTRIBUTION_ONLY` 使用：

```markdown
> 贡献映射完成 · 未创建贡献文件

| 可直接使用 | 需要证据 | 需要训练 | 需要补建 | 已阻断 |
|---:|---:|---:|---:|---:|
| {N} | {N} | {N} | {N} | {N} |

**最高风险候选**：{内容和下一步}
```

`ARTIFACT/FULL_PIPELINE` 使用：

```markdown
> 贡献映射完成 · `{current_artifacts.contribution_map}`

| 可直接使用 | 需要训练 | 需要补建 | 已阻断 |
|---:|---:|---:|---:|
| {N} | {N} | {N} | {N} |

**最高风险声明**：{内容和下一步}
```

## 经历增强

`DIRECT + ENHANCE_ONLY` 使用：

```markdown
> 增强计划完成 · 未修改项目源码 · {N} 个任务

1. **{任务}**：{模式}，验收为 {达标标准}
2. **{任务}**：{模式}，验收为 {达标标准}
```

`ARTIFACT/FULL_PIPELINE` 使用：

```markdown
> 增强计划完成 · `{current_artifacts.enhancement_plan}` · {N} 个任务

1. **{任务}**：{模式}，完成后可支持 `{声明编号}`
2. **{任务}**：{模式}，完成后可支持 `{声明编号}`
```

## 简历

`DIRECT + RESUME_ONLY` 使用：

```markdown
> 简历内容已生成 · {N} 条简历要点 · 未创建文件

- 可直接投递：{N} 条
- 待补数据：{N} 条；大于 0 时明确标记“不可直接投递”
- 仍需确认：{一个最高风险事实或“无”}
```

`FILE_REVISION` 使用：

```markdown
> 简历修订版已生成 · `{versioned_output_path}` · 原文件未覆盖

- 修改位置：{N} 处
- 保留待确认事实：{N} 项
- 格式/渲染验证：{结果}
```

`ARTIFACT/FULL_PIPELINE` 使用：

```markdown
> STAR 简历已生成 · `{current_artifacts.resume}` · {N} 条简历要点

- 低 / 中 / 高风险：{数量}
- 待拷打：{N} 条
- 数字来源待复核：{N} 项
- 未填写量化占位符：{N} 项；大于 0 时标记“不可直接投递”
```

## 拷打

```markdown
> 简历要点拷打完成 · `{current_artifacts.claim_grill_report}`

| 通过 | 待补充 | 高风险 | 阻断 |
|---:|---:|---:|---:|
| {N} | {N} | {N} | {N} |

**优先修复**：{一个具体动作}
```

## 学习与话术

学习 `DIRECT` 使用：

```markdown
> 学习路径完成 · 未创建文件

- Mermaid：架构图 {N} 张 / 核心链路图 {N} 张
- 核心环节：{N} 个
- 待确认关系：{N} 条
```

学习 `FILE_ARTIFACT` 使用：

```markdown
> 学习材料完成 · `{learning_path}`{如生成 HTML： / `{learning_interactive}`}

- 交互页面：{固定浅色 / 未请求}
- 桌面/移动端视觉验证：{结果}
- Mermaid 回退：{可用 / 不适用}
```

学习单步骤使用：

```markdown
> 学习材料完成 · `{current_artifacts.learning_path}`{如生成 HTML： / `current_artifacts.learning_interactive`}

- Mermaid：架构图 {N} 张 / 核心链路图 {N} 张
- 核心环节：{N} 个，均含输入、输出、上下游和失败边界
- 交互页面：{固定浅色 / 未请求}
- 待确认关系：{N} 条
```

学习与话术组合范围使用：

```markdown
> 面试准备完成 · `{current_artifacts.learning_path}` / `{current_artifacts.interview_scripts}`

- 必读模块：{列表}
- 最高风险话题：{内容}
- 已生成：15 秒 / 30 秒 / 2 分钟 / 深挖材料
```

`UNDERSTAND_ONLY` 不使用上面的面试准备模板，改用：

```markdown
> 代码理解材料完成 · `{current_artifacts.learning_path}`

- Mermaid：架构图 {N} 张 / 核心链路图 {N} 张
- 核心环节：{N} 个
- 必读模块：{列表}
- 待确认关系：{N} 项
- 交互页面：{固定浅色 / 未请求}
```

不得在该模式宣称生成 `interview-scripts.md`、分层话术或模拟面试报告。

## 最终门禁

```markdown
> 质量门禁完成 · `{current_artifacts.quality_gate_report}` · **{STATUS}**

- 可直接使用：{N} 条
- 需要训练：{N} 条
- 阻断项：{N} 条
- 唯一优先动作：{动作}
```

## 不要做

- 不要在对话里重复整份文件。
- 不要用卡片隐藏 `RED/BLOCKED`。
- 不要展示用户没有要求的内部执行细节。
- 不要在同一张表格单元格塞入多段列表。
- 不要在中文成品中使用 `Bullet 1`、`Action & Result` 或未解释的内部英文状态名。
- 不要机械翻译产品名、协议名、框架名和真实代码标识符。
