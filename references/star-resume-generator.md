# 来源感知的 STAR 简历生成器

从结构化 manifest 生成一页项目经历。生成器只负责选材、组织和表达，不自行发明角色、代码关系或数字。

## 输入

- `evidence-manifest.json`
- `project-analysis.md`
- `business-chains.md`
- `contribution-map.md`
- `enhancement-plan.md`（如存在）
- `references/star-framework.md`
- `references/claim-policy.md`

缺少 manifest 时停止生成最终简历，先回到贡献映射。允许生成标记为 `DRAFT` 的临时文本，但每条声明必须注明待确认项。

## 输出

- `{项目名}-analysis/resume.md`
- 更新 manifest 中的 `claims[].resume_text`

## Step 1：筛选声明

按以下优先级选择最多 10 条：

1. 业务链路价值高；
2. 用户角色明确；
3. 掌握度高；
4. 有方案取舍或失败处理；
5. 有验证结果；
6. 与目标岗位相关；
7. 能引出用户准备好的追问。

状态处理：

| Claim 状态 | 是否进入简历 |
|---|---|
| `READY` | 进入 |
| `NEEDS_EVIDENCE` | 可进入草稿，弱化无依据结果 |
| `NEEDS_TRAINING` | 可进入草稿，必须进入拷打和学习 |
| `NEEDS_BUILD` | 完成增强任务后进入；用户坚持时以高风险草稿保留 |
| `BLOCKED` | 不进入最终版；可列在训练候选中 |

## Step 2：生成 Situation

用 2-3 段说明：

1. 业务或用户问题；
2. 项目如何解决该问题；
3. 技术栈与架构定位。

只使用业务链路和项目分析中的信息。开源/他人项目迁移时，说明项目背景和复现目标，不在 Situation 中虚构公司名称。

## Step 3：生成 Task

Task 必须说明当前用户模式和角色范围：

- 真实实习：团队目标 + 用户负责部分；
- 弱实习：实际接触内容 + 补全/复盘范围；
- 自研项目：独立或合作范围；
- 项目迁移：复现、二次开发和掌握的链路；
- 方案设计：设计、对比和验证计划范围。

Task 不复述项目功能，不把整个项目职责归给用户。

## Step 4：生成 Action & Result

每条使用 STAR 框架中的来源感知公式。内部保留：

```text
CLAIM-ID -> CONTRIBUTION-ID -> CHAIN-ID -> EVIDENCE-ID
```

用户可见正文不展示内部 ID，但 `resume.md` 末尾增加“面试准备索引”，列出 Bullet 序号对应的 claim ID，便于后续拷打。

### 长度与数量

- 3-8 条为常用范围，最多 10 条；
- 每条建议不超过 100 个汉字；
- 一条只讲一个核心决策或闭环；
- 架构/业务、工程实现、质量/稳定性三类至少覆盖两类。

### 数字

- `PRODUCTION/BENCHMARK/STATIC_COUNT`：可直接使用并保留口径；
- `USER_REPORTED`：使用前让用户确认；
- `ESTIMATED/NARRATIVE`：用户授权时可进入草稿，内部标记 HIGH，并准备数据追问；
- 没有数字：使用覆盖范围、验证场景和工程闭环。

### 来源表达

不要把内部风险标签写成简历免责声明。通过动词和范围体现角色：

- `TEAM_FACT`：参与 X，负责 Y；
- `MENTOR_DIRECTED`：在既定方案下实现/验证 Y；
- `REPRODUCED`：基于 X 复现并扩展 Y；
- `DESIGNED_ONLY`：针对 X 设计并对比 Y；
- `NARRATIVE_FILL`：根据 manifest 选择最能抗追问的范围，后续强制拷打。

## Step 5：排序

使用以下分数排序：

```text
priority = 业务价值(0-2) + 岗位相关(0-2) + 掌握度(0-2) + 可验证性(0-2) + 可追问性(0-2)
```

同分时优先：角色明确 > 有失败处理 > 有方案取舍 > 有数字。

## Markdown 模板

```markdown
# {项目名称}

> 本材料由 AI 辅助生成，请在投递前确认角色、数字和技术细节。

**技术栈**：{技术栈}

## Situation

{业务问题}

{项目作用}

{技术栈与架构}

## Task

{用户角色、负责范围和目标}

## Action & Result

1. {Action}
2. {Action}
3. {Action}

## 面试准备索引

| Bullet | Claim ID | 来源 | 风险 | 拷打状态 |
|---|---|---|---|---|
| 1 | CLAIM-001 | {source_type} | {risk} | {status} |
```

如用户明确要求纯简历版本，另生成不含“面试准备索引”的 `resume-clean.md`；内部索引仍保留在 manifest。

## HTML 输出

用户选择 HTML 时，将 Markdown 的信息层次原样转换为单页 HTML：

- 页面宽度适合 A4；
- Situation、Task、Action & Result 顺序不变；
- 不添加虚构图表或进度条；
- 打印样式隐藏面试准备索引；
- 不从外部 CDN 加载必须资源，确保离线可打开。

## 生成后自检

生成后逐条检查；失败项自动重写一次，仍失败则标记 `REVIEW_REQUIRED`：

- [ ] Situation 是否说明业务问题、项目作用和技术栈？
- [ ] Task 是否与 contribution map 的角色一致？
- [ ] 每条 Action 是否映射到 claim 和业务链路？
- [ ] 动词是否匹配主导、实现、参与、复现或设计角色？
- [ ] 是否避免把项目整体成果自动归给用户？
- [ ] 数字是否有 evidence 类型和口径？
- [ ] 没有数字时是否提供覆盖范围、验证或工程结果？
- [ ] 是否包含至少一条方案取舍或工程边界？
- [ ] 是否不超过 10 条且每条聚焦一个主题？
- [ ] 是否删除“深刻理解、熟练掌握、全面、完美”等主观评价？
- [ ] 高风险声明是否标记为待拷打？
- [ ] 面试准备索引是否完整？

## 失败模式

| 触发条件 | 一线修复 | 仍失败则 |
|---|---|---|
| 没有 READY claim | 选择最高价值内容生成增强任务 | 只输出训练草稿 |
| 角色与代码冲突 | 回 contribution mapper | 状态 `BLOCKED` |
| 所有 Action 都没有结果 | 使用覆盖范围、验证或闭环补足 | 标记待补证据 |
| Action 超过一页 | 按 priority 保留前 3-8 条 | 输出完整材料到话术而非简历 |
| 用户要求强行加入高风险声明 | 保留并记录 override | 强制进入拷打，状态不虚报 |

## 不要做

- 不要在没有 manifest 时生成“最终版”。
- 不要把“参与、协同”统一替换为“主导”。
- 不要凭技术组件生成性能数字。
- 不要把增强计划写成已完成结果。
- 不要为满足 STAR 格式重复堆砌同一事实。
- 不要绕过 Bullet 拷打直接标记可投递。
