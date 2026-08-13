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

```markdown
> 贡献映射完成 · `{current_artifacts.contribution_map}`

| 可直接使用 | 需要训练 | 需要补建 | 已阻断 |
|---:|---:|---:|---:|
| {N} | {N} | {N} | {N} |

**最高风险声明**：{内容和下一步}
```

## 经历增强

```markdown
> 增强计划完成 · `{current_artifacts.enhancement_plan}` · {N} 个任务

1. **{任务}**：{模式}，完成后可支持 `{声明编号}`
2. **{任务}**：{模式}，完成后可支持 `{声明编号}`
```

## 简历

```markdown
> STAR 简历已生成 · `{current_artifacts.resume}` · {N} 条简历要点

- 低 / 中 / 高风险：{数量}
- 待拷打：{N} 条
- 数字来源待复核：{N} 项
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

```markdown
> 面试准备完成 · `{current_artifacts.learning_path}` / `{current_artifacts.interview_scripts}`

- 必读模块：{列表}
- 最高风险话题：{内容}
- 已生成：15 秒 / 30 秒 / 2 分钟 / 深挖材料
```

`UNDERSTAND_ONLY` 不使用上面的面试准备模板，改用：

```markdown
> 代码理解材料完成 · `{current_artifacts.learning_path}`

- 核心链路：{N} 条
- 必读模块：{列表}
- 待确认关系：{N} 项
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
