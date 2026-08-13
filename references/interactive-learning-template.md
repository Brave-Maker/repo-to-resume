# 交互式学习页面模板

基于 Step 2 产出的学习路径内容，生成单文件自包含交互式 HTML。用户在浏览器中打开即可按模块学习，核心模块附带随堂测验。

## 核心约束（强制）

**设计稳定性——以下内容严禁修改：**
- 所有 CSS 自定义属性（`--color-*`、`--font-*`、`--space-*`、`--radius-*`、`--shadow-*`）的值**必须原样使用，不得修改任何颜色、字号、间距**
- 字体栈**必须原样使用**，不得替换
- JS 脚本**必须原样使用**，不得增删功能
- 可替换的只有：HTML 注释中标注 `{占位符}` 的内容、模块数量、测验题目和选项

**内容来源：**
- 不从零生成内容——把 Step 2 产出的 learning-path.md 中的内容转换为 HTML
- 系统全景图 → 角色卡片 + 步骤动画
- 模块详解 → 代码对照块 + 设计决策卡片 + 文件树
- 测验题：核心模块各 1 道，从模块的「面试可能追问」中衍生，考察应用而非记忆

---

## 完整 HTML 模板

生成时按以下结构输出。CSS 块和 JS 块**逐字复制**，只替换 HTML 注释标注的占位符。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{项目名称} - 交互式学习</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* ===== CSS 变量（严禁修改） ===== */
    :root {
      /* 背景色 */
      --color-bg:             #FAF7F2;
      --color-bg-warm:        #F5F0E8;
      --color-bg-code:        #1E1E2E;
      /* 文字色 */
      --color-text:           #2C2A28;
      --color-text-secondary: #6B6560;
      --color-text-muted:     #9E9790;
      /* 边框 */
      --color-border:         #E5DFD6;
      --color-border-light:   #EEEBE5;
      /* 表面 */
      --color-surface:        #FFFFFF;
      --color-surface-warm:   #FDF9F3;
      /* 强调色——固定 vermillion，不可更改 */
      --color-accent:         #D94F30;
      --color-accent-hover:   #C4432A;
      --color-accent-light:   #FDEEE9;
      --color-accent-muted:   #E8836C;
      /* 语义色 */
      --color-success:        #2D8B55;
      --color-success-light:  #E8F5EE;
      --color-error:          #C93B3B;
      --color-error-light:    #FDE8E8;
      /* 角色色 */
      --color-actor-1:        #D94F30;
      --color-actor-2:        #2A7B9B;
      --color-actor-3:        #7B6DAA;
      --color-actor-4:        #D4A843;
      --color-actor-5:        #2D8B55;
      /* 字体（严禁替换） */
      --font-display:  'Bricolage Grotesque', Georgia, serif;
      --font-body:     'DM Sans', -apple-system, sans-serif;
      --font-mono:     'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
      /* 字号 */
      --text-xs:   0.75rem;
      --text-sm:   0.875rem;
      --text-base: 1rem;
      --text-lg:   1.125rem;
      --text-xl:   1.25rem;
      --text-2xl:  1.5rem;
      --text-3xl:  1.875rem;
      --text-4xl:  2.25rem;
      --text-5xl:  3rem;
      --text-6xl:  3.75rem;
      /* 间距 */
      --space-1:  0.25rem;
      --space-2:  0.5rem;
      --space-3:  0.75rem;
      --space-4:  1rem;
      --space-5:  1.25rem;
      --space-6:  1.5rem;
      --space-8:  2rem;
      --space-10: 2.5rem;
      --space-12: 3rem;
      --space-16: 4rem;
      --space-20: 5rem;
      /* 圆角 */
      --radius-sm:  8px;
      --radius-md:  12px;
      --radius-lg:  16px;
      --radius-full: 9999px;
      /* 阴影（暖色调，不可用纯黑） */
      --shadow-sm:  0 1px 2px rgba(44, 42, 40, 0.05);
      --shadow-md:  0 4px 12px rgba(44, 42, 40, 0.08);
      --shadow-lg:  0 8px 24px rgba(44, 42, 40, 0.1);
      --shadow-xl:  0 16px 48px rgba(44, 42, 40, 0.12);
      /* 动画 */
      --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
      --duration-fast:   150ms;
      --duration-normal: 300ms;
      --duration-slow:   500ms;
      /* 布局 */
      --content-width: 800px;
      --nav-height: 52px;
    }

    /* ===== 全局重置 ===== */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html {
      scroll-snap-type: y proximity;
      scroll-behavior: smooth;
    }
    body {
      font-family: var(--font-body);
      font-size: var(--text-base);
      line-height: 1.6;
      color: var(--color-text);
      background: var(--color-bg);
      background-image: radial-gradient(ellipse at 20% 50%, rgba(217, 79, 48, 0.03) 0%, transparent 50%);
    }

    /* ===== 导航栏 ===== */
    .nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
      height: var(--nav-height);
      background: rgba(250, 247, 242, 0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--color-border);
      display: flex; align-items: center;
      padding: 0 var(--space-6);
    }
    .nav-inner {
      max-width: var(--content-width); width: 100%; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between;
    }
    .nav-title {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: var(--text-sm);
      color: var(--color-text);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      max-width: 40%;
    }
    .nav-dots { display: flex; gap: var(--space-2); align-items: center; }
    .nav-dot {
      width: 12px; height: 12px;
      border-radius: 50%;
      border: 2px solid var(--color-text-muted);
      background: transparent;
      cursor: pointer;
      transition: all var(--duration-fast);
      position: relative;
    }
    .nav-dot:hover { border-color: var(--color-accent); }
    .nav-dot.active { border-color: var(--color-accent); background: var(--color-accent); box-shadow: 0 0 8px rgba(217, 79, 48, 0.3); }
    .nav-dot.visited { background: var(--color-accent); border-color: var(--color-accent); opacity: 0.6; }
    /* 提示 */
    .nav-dot::after {
      content: attr(data-tooltip);
      position: absolute; bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%);
      background: var(--color-bg-code); color: #CDD6F4;
      padding: var(--space-1) var(--space-3);
      border-radius: var(--radius-sm);
      font-size: var(--text-xs); font-family: var(--font-body);
      white-space: nowrap; pointer-events: none;
      opacity: 0; transition: opacity var(--duration-fast);
    }
    .nav-dot:hover::after { opacity: 1; }

    /* 进度条 */
    .progress-bar {
      position: fixed; top: 0; left: 0; height: 2px;
      background: var(--color-accent);
      z-index: 1001;
      transition: width 100ms linear;
    }

    /* ===== 模块容器 ===== */
    .module {
      min-height: 100dvh;
      scroll-snap-align: start;
      padding: calc(var(--nav-height) + var(--space-12)) var(--space-6) var(--space-16);
      display: flex; align-items: center; justify-content: center;
    }
    .module:nth-child(even) { background: var(--color-bg); }
    .module:nth-child(odd)  { background: var(--color-bg-warm); }
    .module-content { max-width: var(--content-width); width: 100%; }

    .module-number {
      font-family: var(--font-display);
      font-size: var(--text-6xl); font-weight: 800;
      color: var(--color-accent); opacity: 0.15;
      line-height: 1; display: block; margin-bottom: var(--space-2);
    }
    .module-title {
      font-family: var(--font-display);
      font-size: var(--text-4xl); font-weight: 700;
      color: var(--color-text);
      margin-bottom: var(--space-2);
    }
    .module-subtitle {
      font-size: var(--text-lg); color: var(--color-text-secondary);
      margin-bottom: var(--space-10);
    }
    .module-body { display: flex; flex-direction: column; gap: var(--space-10); }

    /* 区块标题 */
    .section-heading {
      font-family: var(--font-display);
      font-size: var(--text-2xl); font-weight: 600;
      color: var(--color-text);
      margin-bottom: var(--space-4);
    }

    /* ===== 角色卡片网格 ===== */
    .role-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: var(--space-4);
    }
    .role-card {
      background: var(--color-surface);
      border-radius: var(--radius-md);
      padding: var(--space-5);
      box-shadow: var(--shadow-sm);
      border-top: 3px solid var(--color-accent);
      transition: transform var(--duration-normal) var(--ease-out), box-shadow var(--duration-normal);
    }
    .role-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
    .role-card.star-3 { border-top-color: var(--color-accent); }
    .role-card.star-2 { border-top-color: var(--color-actor-2); }
    .role-card.star-1 { border-top-color: var(--color-text-muted); }
    .role-card-name {
      font-family: var(--font-display); font-weight: 700;
      font-size: var(--text-lg); margin-bottom: var(--space-1);
    }
    .role-card-layer {
      font-size: var(--text-xs); color: var(--color-text-muted);
      text-transform: uppercase; letter-spacing: 0.05em;
      margin-bottom: var(--space-2);
    }
    .role-card-desc {
      font-size: var(--text-sm); color: var(--color-text-secondary);
      margin-bottom: var(--space-3);
    }
    .role-card-meta {
      font-size: var(--text-xs); color: var(--color-text-muted);
      display: flex; gap: var(--space-4);
    }
    .role-card-meta span { display: flex; align-items: center; gap: var(--space-1); }

    /* ===== 步骤动画（一条请求走到底） ===== */
    .flow-steps {
      display: flex; align-items: flex-start; gap: 0;
      flex-wrap: wrap; justify-content: center;
    }
    .flow-step {
      display: flex; flex-direction: column; align-items: center;
      text-align: center; max-width: 120px;
    }
    .flow-step-num {
      width: 40px; height: 40px; border-radius: 50%;
      background: var(--color-accent); color: #fff;
      font-family: var(--font-display); font-weight: 700; font-size: var(--text-lg);
      display: flex; align-items: center; justify-content: center;
      margin-bottom: var(--space-2);
    }
    .flow-step-label {
      font-size: var(--text-sm); font-weight: 600; color: var(--color-text);
      margin-bottom: var(--space-1);
    }
    .flow-step-detail {
      font-size: var(--text-xs); color: var(--color-text-secondary);
    }
    .flow-arrow {
      font-size: var(--text-xl); color: var(--color-accent-muted);
      display: flex; align-items: center;
      padding: 0 var(--space-2);
      margin-top: 8px;
    }
    @media (max-width: 768px) {
      .flow-steps { flex-direction: column; align-items: center; }
      .flow-arrow { transform: rotate(90deg); padding: var(--space-2) 0; }
    }

    /* ===== 代码 ↔ 白话对照 ===== */
    .translation-block {
      display: grid; grid-template-columns: 1fr 1fr; gap: 0;
      border-radius: var(--radius-md); overflow: hidden;
      box-shadow: var(--shadow-md);
    }
    .translation-code {
      background: var(--color-bg-code);
      color: #CDD6F4;
      padding: var(--space-6);
      font-family: var(--font-mono);
      font-size: var(--text-sm);
      line-height: 1.7;
      overflow: hidden;
    }
    .translation-code pre, .translation-code code {
      white-space: pre-wrap; word-break: break-word; overflow-x: hidden;
    }
    .translation-english {
      background: var(--color-surface-warm);
      padding: var(--space-6);
      font-size: var(--text-sm); line-height: 1.7;
      border-left: 3px solid var(--color-accent);
    }
    .translation-english .tl {
      padding: 2px 0;
      color: var(--color-text-secondary);
    }
    .translation-english .tl + .tl { border-top: 1px solid var(--color-border-light); padding-top: 6px; margin-top: 4px; }
    @media (max-width: 768px) {
      .translation-block { grid-template-columns: 1fr; }
      .translation-english { border-left: none; border-top: 3px solid var(--color-accent); }
    }

    /* ===== 设计决策卡片 ===== */
    .decision-card {
      background: var(--color-surface);
      border-radius: var(--radius-md);
      padding: var(--space-6);
      box-shadow: var(--shadow-sm);
      border-left: 4px solid var(--color-accent);
    }
    .decision-card h4 {
      font-family: var(--font-display); font-size: var(--text-lg); font-weight: 700;
      margin-bottom: var(--space-3);
    }
    .decision-card .decision-row {
      margin-bottom: var(--space-2);
      font-size: var(--text-sm);
    }
    .decision-card .decision-row strong {
      color: var(--color-accent);
      display: inline-block; min-width: 5em;
    }

    /* ===== 文件树 ===== */
    .file-tree {
      font-family: var(--font-mono); font-size: var(--text-sm);
      background: var(--color-surface);
      border-radius: var(--radius-md);
      padding: var(--space-5);
      box-shadow: var(--shadow-sm);
    }
    .file-tree .ft-item {
      padding: var(--space-1) 0;
      display: flex; align-items: baseline; gap: var(--space-2);
    }
    .file-tree .ft-name { color: var(--color-accent); font-weight: 600; white-space: nowrap; }
    .file-tree .ft-desc {
      color: var(--color-text-secondary);
      font-family: var(--font-body);
      font-size: var(--text-xs);
    }

    /* ===== 测验 ===== */
    .quiz-container {
      background: var(--color-surface);
      border-radius: var(--radius-md);
      padding: var(--space-6);
      box-shadow: var(--shadow-sm);
    }
    .quiz-question {
      font-family: var(--font-display); font-size: var(--text-lg); font-weight: 600;
      margin-bottom: var(--space-5);
    }
    .quiz-options { display: flex; flex-direction: column; gap: var(--space-3); }
    .quiz-option {
      display: flex; align-items: center; gap: var(--space-3);
      padding: var(--space-3) var(--space-4);
      border: 2px solid var(--color-border);
      border-radius: var(--radius-sm);
      background: var(--color-surface);
      cursor: pointer;
      transition: border-color var(--duration-fast), background var(--duration-fast);
      font-family: var(--font-body); font-size: var(--text-base);
      text-align: left;
    }
    .quiz-option:hover { border-color: var(--color-accent-muted); }
    .quiz-option.selected { border-color: var(--color-accent); background: var(--color-accent-light); }
    .quiz-option.correct { border-color: var(--color-success); background: var(--color-success-light); }
    .quiz-option.incorrect { border-color: var(--color-error); background: var(--color-error-light); }
    .quiz-option.disabled { pointer-events: none; opacity: 0.8; }
    .quiz-feedback {
      margin-top: var(--space-4); padding: var(--space-4);
      border-radius: var(--radius-sm);
      font-size: var(--text-sm);
      display: none;
    }
    .quiz-feedback.show { display: block; }
    .quiz-feedback.correct { background: var(--color-success-light); color: var(--color-success); }
    .quiz-feedback.wrong { background: var(--color-error-light); color: var(--color-error); }
    .quiz-submit {
      margin-top: var(--space-4);
      padding: var(--space-2) var(--space-6);
      background: var(--color-accent); color: #fff;
      border: none; border-radius: var(--radius-sm);
      font-family: var(--font-display); font-weight: 600; font-size: var(--text-sm);
      cursor: pointer;
      transition: background var(--duration-fast);
    }
    .quiz-submit:hover { background: var(--color-accent-hover); }

    /* ===== 词汇提示 ===== */
    .term {
      border-bottom: 1.5px dashed var(--color-accent-muted);
      cursor: pointer;
    }
    .term:hover { border-bottom-color: var(--color-accent); color: var(--color-accent); }
    .term-tooltip {
      position: fixed;
      background: var(--color-bg-code); color: #CDD6F4;
      padding: var(--space-3) var(--space-4);
      border-radius: var(--radius-sm);
      font-size: var(--text-sm); font-family: var(--font-body);
      line-height: 1.5;
      width: min(320px, 80vw);
      box-shadow: var(--shadow-lg);
      pointer-events: none;
      opacity: 0; transition: opacity var(--duration-fast);
      z-index: 10000;
    }
    .term-tooltip.visible { opacity: 1; }

    /* ===== 快速导航按钮 ===== */
    .nav-buttons {
      display: flex; justify-content: space-between; gap: var(--space-4);
      margin-top: var(--space-8);
    }
    .nav-btn {
      padding: var(--space-2) var(--space-5);
      background: transparent;
      border: 2px solid var(--color-border);
      border-radius: var(--radius-full);
      font-family: var(--font-display); font-weight: 600;
      font-size: var(--text-sm);
      color: var(--color-text-secondary);
      cursor: pointer;
      transition: all var(--duration-fast);
    }
    .nav-btn:hover { border-color: var(--color-accent); color: var(--color-accent); }

    /* ===== 重要度徽标 ===== */
    .importance-badge {
      display: inline-block;
      padding: 2px 10px;
      border-radius: var(--radius-full);
      font-size: var(--text-xs); font-weight: 700;
      font-family: var(--font-display);
    }
    .importance-badge.core { background: var(--color-accent-light); color: var(--color-accent); }
    .importance-badge.important { background: var(--color-info-light); color: var(--color-info); }
    .importance-badge.support { background: #f0f0f0; color: var(--color-text-muted); }

    /* ===== 模块关系标签 ===== */
    .module-relations {
      display: flex; gap: var(--space-6); flex-wrap: wrap;
      margin-bottom: var(--space-6);
      font-size: var(--text-sm); color: var(--color-text-secondary);
    }
    .module-relations strong { color: var(--color-text); }

    /* ===== 响应式 ===== */
    @media (max-width: 768px) {
      :root { --text-4xl: 1.875rem; --text-6xl: 3rem; }
      .role-cards { grid-template-columns: 1fr 1fr; }
      .module { padding: calc(var(--nav-height) + var(--space-8)) var(--space-4) var(--space-10); }
    }
    @media (max-width: 480px) {
      :root { --text-4xl: 1.5rem; --text-6xl: 2.25rem; }
      .role-cards { grid-template-columns: 1fr; }
      .nav-title { display: none; }
    }

    /* 滚动条 */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: var(--radius-full); }
  </style>
</head>
<body>

  <!-- 进度条 -->
  <div class="progress-bar" id="progressBar"></div>

  <!-- 导航栏 -->
  <nav class="nav">
    <div class="nav-inner">
      <span class="nav-title">{项目名称}</span>
      <div class="nav-dots" id="navDots">
        <!-- 按模块数生成 nav-dot，data-tooltip 为模块简称 -->
        <!-- 示例：
        <button class="nav-dot active" data-target="module-0" data-tooltip="全景图"></button>
        <button class="nav-dot" data-target="module-1" data-tooltip="Pipeline"></button>
        ...
        -->
      </div>
    </div>
  </nav>

  <!--
    ===== 模块列表 =====
    每个模块是一个 <section class="module" id="module-N">
    module-0 固定为「系统全景图」
    module-1 起为各模块详解

    结构顺序：
    1. module-0：系统全景图（角色卡片 + 一条请求走到底）
    2. module-1..N：核心/重要模块（完整：文件树 + 代码对照 + 设计决策 + 测验）
    3. module-N+1..M：支撑模块（精简：文件列表 + 一句话）
    =====
  -->

  <!-- ===== module-0：系统全景图（固定结构） ===== -->
  <section class="module" id="module-0">
    <div class="module-content">
      <span class="module-number">00</span>
      <h1 class="module-title">🗺️ 系统全景图</h1>
      <p class="module-subtitle">{一句话定位，从 learning-path.md 第一层复制}</p>

      <div class="module-body">

        <!-- 角色卡片 -->
        <div>
          <h2 class="section-heading">角色表</h2>
          <div class="role-cards">
            <!-- 每个模块一张卡片，按重要度加 class：
                 ⭐⭐⭐ → star-3
                 ⭐⭐   → star-2
                 ⭐     → star-1
            -->
            <!-- 示例：
            <div class="role-card star-3">
              <div class="role-card-name">Pipeline 编排引擎</div>
              <div class="role-card-layer">核心业务层</div>
              <div class="role-card-desc">{一句话职责}</div>
              <div class="role-card-meta">
                <span>⬆ 依赖: {模块列表}</span>
                <span>⬇ 被依赖: {模块列表}</span>
              </div>
            </div>
            -->
          </div>
        </div>

        <!-- 一条请求走到底 -->
        <div>
          <h2 class="section-heading">一条请求走到底</h2>
          <p style="color: var(--color-text-secondary); margin-bottom: var(--space-6);">
            {从 learning-path.md 第一层复制的用户操作描述}
          </p>
          <div class="flow-steps">
            <!-- 每一步一个 flow-step，步骤间夹 flow-arrow → -->
            <!-- 示例：
            <div class="flow-step">
              <div class="flow-step-num">1</div>
              <div class="flow-step-label">CLI 输入</div>
              <div class="flow-step-detail">用户执行 run batch</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
              <div class="flow-step-num">2</div>
              <div class="flow-step-label">Router</div>
              <div class="flow-step-detail">解析命令参数</div>
            </div>
            ...
            -->
          </div>
        </div>

        <!-- 阅读策略 -->
        <div>
          <h2 class="section-heading">📖 学习策略</h2>
          <p style="color: var(--color-text-secondary);">
            {从 learning-path.md 的「你应该优先看哪些」复制，转换为自然语言}
          </p>
        </div>

      </div>

      <div class="nav-buttons">
        <span></span>
        <button class="nav-btn" onclick="document.getElementById('module-1').scrollIntoView()">开始学习 →</button>
      </div>
    </div>
  </section>

  <!-- ===== module-1..N：核心/重要模块（完整模板） ===== -->
  <!--
  <section class="module" id="module-N">
    <div class="module-content">
      <span class="module-number">{0N}</span>
      <h1 class="module-title">{模块名} <span class="importance-badge core">{⭐⭐⭐}</span></h1>
      <div class="module-relations">
        <span><strong>依赖：</strong>{模块列表或"—"}</span>
        <span><strong>被依赖：</strong>{模块列表}</span>
      </div>

      <div class="module-body">

        <div>
          <h2 class="section-heading">为什么需要这个模块</h2>
          <p style="color: var(--color-text-secondary);">{从 learning-path.md 复制}</p>
        </div>

        <div>
          <h2 class="section-heading">📁 关键文件</h2>
          <div class="file-tree">
            {每条文件一行，ft-name 为路径，ft-desc 为说明}
          </div>
        </div>

        <div>
          <h2 class="section-heading">🔍 核心逻辑</h2>
          <div class="translation-block">
            <div class="translation-code">
              <pre><code>{5-10 行源码，不做任何修改}</code></pre>
            </div>
            <div class="translation-english">
              {逐行白话解释，每行用 <p class="tl"> 包裹}
            </div>
          </div>
        </div>

        <div>
          <h2 class="section-heading">💡 设计决策</h2>
          <div class="decision-card">
            <h4>{决策标题}</h4>
            <div class="decision-row"><strong>为什么</strong>{理由}</div>
            <div class="decision-row"><strong>备选方案</strong>{曾考虑的其他做法}</div>
            <div class="decision-row"><strong>代价</strong>{局限性和不适用场景}</div>
          </div>
        </div>

        <div>
          <h2 class="section-heading">🎯 随堂测验</h2>
          <div class="quiz-container">
            <div class="quiz-question">{场景应用题——不是考记忆，是考理解}</div>
            <div class="quiz-options">
              <button class="quiz-option" data-correct="false" onclick="selectQuizOption(this)">选项 A</button>
              <button class="quiz-option" data-correct="true"  onclick="selectQuizOption(this)">选项 B（正确答案）</button>
              <button class="quiz-option" data-correct="false" onclick="selectQuizOption(this)">选项 C</button>
              <button class="quiz-option" data-correct="false" onclick="selectQuizOption(this)">选项 D</button>
            </div>
            <div class="quiz-feedback" id="feedback-module-N"></div>
            <button class="quiz-submit" onclick="checkQuiz(this)">提交</button>
          </div>
        </div>

      </div>

      <div class="nav-buttons">
        <button class="nav-btn" onclick="document.getElementById('module-{N-1}').scrollIntoView()">← 上一模块</button>
        <button class="nav-btn" onclick="document.getElementById('module-{N+1}').scrollIntoView()">下一模块 →</button>
      </div>
    </div>
  </section>
  -->

  <!-- ===== module-X..Y：支撑模块（精简模板） ===== -->
  <!--
  <section class="module" id="module-N">
    <div class="module-content">
      <span class="module-number">{0N}</span>
      <h1 class="module-title">{模块名} <span class="importance-badge support">⭐</span></h1>
      <div class="module-relations">
        <span><strong>依赖：</strong>{模块列表}</span>
        <span><strong>被依赖：</strong>{模块列表}</span>
      </div>

      <div class="module-body">
        <div>
          <h2 class="section-heading">一句话职责</h2>
          <p style="color: var(--color-text-secondary);">{从 learning-path.md 复制}</p>
        </div>
        <div>
          <h2 class="section-heading">📁 关键文件</h2>
          <div class="file-tree">
            {每条文件一行}
          </div>
        </div>
      </div>

      <div class="nav-buttons">
        <button class="nav-btn" onclick="document.getElementById('module-{N-1}').scrollIntoView()">← 上一模块</button>
        <button class="nav-btn" onclick="document.getElementById('module-{N+1}').scrollIntoView()">下一模块 →</button>
      </div>
    </div>
  </section>
  -->

  <!-- ===== JS 脚本（严禁修改） ===== -->
  <script>
    (function() {
      // ===== 进度条 =====
      const progressBar = document.getElementById('progressBar');
      function updateProgress() {
        const scrollTop = window.scrollY;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
        progressBar.style.width = progress + '%';
      }
      window.addEventListener('scroll', () => requestAnimationFrame(updateProgress), { passive: true });

      // ===== 导航圆点高亮 =====
      const modules = document.querySelectorAll('.module');
      const dots = document.querySelectorAll('.nav-dot');
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            dots.forEach(d => {
              d.classList.remove('active');
              if (d.dataset.target === id) d.classList.add('active');
            });
            // 标记已访问
            dots.forEach(d => {
              if (d.dataset.target === id) d.classList.add('visited');
            });
          }
        });
      }, { threshold: 0.4 });
      modules.forEach(m => observer.observe(m));

      // 圆点点击跳转
      dots.forEach(dot => {
        dot.addEventListener('click', () => {
          const target = document.getElementById(dot.dataset.target);
          if (target) target.scrollIntoView();
        });
      });

      // ===== 测验逻辑 =====
      window.selectQuizOption = function(btn) {
        const container = btn.closest('.quiz-options');
        if (container.classList.contains('answered')) return;
        container.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
        btn.classList.add('selected');
      };

      window.checkQuiz = function(submitBtn) {
        const container = submitBtn.closest('.quiz-container');
        const options = container.querySelector('.quiz-options');
        const feedback = container.querySelector('.quiz-feedback');
        const selected = options.querySelector('.quiz-option.selected');
        if (!selected) return;

        const isCorrect = selected.dataset.correct === 'true';
        options.classList.add('answered');
        options.querySelectorAll('.quiz-option').forEach(o => {
          o.classList.add('disabled');
          if (o.dataset.correct === 'true') o.classList.add('correct');
        });
        if (!isCorrect) selected.classList.add('incorrect');

        feedback.className = 'quiz-feedback show ' + (isCorrect ? 'correct' : 'wrong');
        feedback.textContent = isCorrect
          ? '✅ 正确！' + (selected.dataset.explanation || '')
          : '❌ 不对。' + (selected.dataset.explanation || '再想想看？');

        submitBtn.style.display = 'none';
      };

      // ===== 词汇提示 =====
      let activeTooltip = null;
      document.querySelectorAll('.term').forEach(term => {
        const tip = document.createElement('span');
        tip.className = 'term-tooltip';
        tip.textContent = term.dataset.definition;

        function showTip() {
          if (activeTooltip && activeTooltip !== tip) {
            activeTooltip.classList.remove('visible');
            activeTooltip.remove();
          }
          document.body.appendChild(tip);
          const rect = term.getBoundingClientRect();
          const tipWidth = Math.min(320, window.innerWidth * 0.8);
          let left = rect.left + rect.width / 2 - tipWidth / 2;
          left = Math.max(8, Math.min(left, window.innerWidth - tipWidth - 8));
          tip.style.left = left + 'px';
          const tipHeight = tip.offsetHeight || 60;
          if (rect.top - tipHeight - 8 < 0) {
            tip.style.top = (rect.bottom + 8) + 'px';
          } else {
            tip.style.top = (rect.top - tipHeight - 8) + 'px';
          }
          requestAnimationFrame(() => tip.classList.add('visible'));
          activeTooltip = tip;
        }

        function hideTip() {
          tip.classList.remove('visible');
          setTimeout(() => { if (!tip.classList.contains('visible') && tip.parentNode) tip.remove(); }, 150);
          if (activeTooltip === tip) activeTooltip = null;
        }

        term.addEventListener('mouseenter', showTip);
        term.addEventListener('mouseleave', hideTip);
        term.addEventListener('click', (e) => {
          e.stopPropagation();
          if (tip.classList.contains('visible')) { hideTip(); }
          else { showTip(); }
        });
      });

      document.addEventListener('click', () => {
        if (activeTooltip) {
          activeTooltip.classList.remove('visible');
          activeTooltip.remove();
          activeTooltip = null;
        }
      });

      // ===== 键盘导航 =====
      document.addEventListener('keydown', (e) => {
        if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;
        const currentIdx = Array.from(modules).findIndex(m => {
          const rect = m.getBoundingClientRect();
          return rect.top >= -100 && rect.top < window.innerHeight / 2;
        });
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
          e.preventDefault();
          const next = modules[Math.min(currentIdx + 1, modules.length - 1)];
          if (next) next.scrollIntoView();
        }
        if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
          e.preventDefault();
          const prev = modules[Math.max(0, currentIdx - 1)];
          if (prev) prev.scrollIntoView();
        }
      });
    })();
  </script>
</body>
</html>
```

---

## 生成规则

### 内容来源映射

| learning-path.md 内容 | HTML 元素 | 位置 |
|----------------------|-----------|------|
| 一句话定位 | `.module-subtitle` | module-0 |
| 角色表 | `.role-cards` > `.role-card` | module-0 |
| 一条请求走到底 | `.flow-steps` > `.flow-step` + `.flow-arrow` | module-0 |
| 学习策略 | 最后一段 `<p>` | module-0 |
| 模块的「为什么需要」 | `<p>` 段落 | 各模块 |
| 模块的关键文件 | `.file-tree` > `.ft-item` | 各模块 |
| 模块的核心逻辑（代码片段） | `.translation-block` | 核心模块 |
| 模块的设计决策（四段式） | `.decision-card` | 核心模块 |
| 模块的面试追问 | **衍生**为测验题 | 核心模块 |

### 测验题生成规则

- 只在 ⭐⭐⭐ 核心模块生成测验（⭐ 支撑模块不生成）
- 每题 4 个选项，1 个正确答案
- 题目类型：场景应用题——「如果要加 X 功能，改哪个模块？」「A 挂了会怎样？」「为什么选 X 方案而不是 Y？」
- 禁止：定义题（"XXX 是什么？"）、文件名回忆题、语法细节题
- 错误选项也要合理（不能让用户一眼排除），反馈文案简短鼓励

### 词汇提示规则

- 对学习路径中出现的**技术术语**添加 `<span class="term" data-definition="...">`
- 每个术语在首次出现时标记一次即可
- 定义用 1-2 句白话，不用术语解释术语
- 常见需标记的术语：CLI、API、SDK、中间件、端点、回调、异步、序列化、池化、熔断、管道、路由、依赖注入、ORM、CRUD、RPC、消息队列

### 重要度徽标

```html
<!-- ⭐⭐⭐ 核心 -->
<span class="importance-badge core">核心</span>

<!-- ⭐⭐ 重要 -->
<span class="importance-badge important">重要</span>

<!-- ⭐ 支撑 -->
<span class="importance-badge support">支撑</span>
```

### 导航圆点

每个模块对应一个圆点，`data-tooltip` 用模块简称（≤6 个中文字）。`module-0` 的 tooltip 固定为「全景图」。

---

## 质量检查清单

生成 HTML 后，逐项自检：

- [ ] CSS 变量是否完全未修改？
- [ ] 字体栈是否完全未修改？
- [ ] JS 脚本是否完全未修改？
- [ ] 暖色背景 (`#FAF7F2` / `#F5F0E8`) 是否正确交替？
- [ ] 强调色是否固定为 vermillion (`#D94F30`)？
- [ ] 模块 0 是否为「系统全景图」？
- [ ] 核心模块是否有测验？支撑模块是否**没有**测验？
- [ ] 测验题是否为场景应用题（非记忆题）？
- [ ] 代码对照块中的代码是否为项目源码原文（未修改）？
- [ ] `{项目名称}` 等占位符是否全部替换为实际内容？
- [ ] 导航圆点数量是否与实际模块数一致？
