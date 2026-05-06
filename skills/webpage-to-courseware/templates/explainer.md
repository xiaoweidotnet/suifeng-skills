# 深度讲解模式（Explainer Article）

## 适用场景

- 讲清楚**一个知识点/产品/技术**的来龙去脉
- 内容逻辑性强、有多个子模块需要深入展开
- 希望生成一篇可以**分享链接**、**阅读学习**的精排长页
- 不需要录视频，读者自由滚动阅读

## 页面结构

```
┌─────────────────────────────────────────────────────────┐
│  顶部 Hero：大标题 + 副标题 + 关键数字统计行              │
├──────────┬──────────────────────────────────────────────┤
│          │  § 背景               ← H2 章节              │
│  固定    │    文字说明段落                               │
│  左侧    │    内联数据卡 / 进度条                        │
│  目录    │    参考图（按需）                             │
│  (TOC)   ├──────────────────────────────────────────────┤
│          │  § 核心功能            ← H2 章节              │
│  滚动    │    步骤流程                                   │
│  高亮    │    引用块                                     │
│  当前    ├──────────────────────────────────────────────┤
│  章节    │  § 数据对比                                   │
│          │    完整对比表格                               │
│          ├──────────────────────────────────────────────┤
│          │  § 总结               ← 关键要点卡片          │
└──────────┴──────────────────────────────────────────────┘
```

---

## HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[标题] | 深度解读</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '#3b82f6',   /* 根据品牌色调整 */
            accent:  '#60a5fa',
            muted:   '#94a3b8',
            card:    '#1e2330',
            border:  '#2d3347',
          }
        }
      }
    }
  </script>
  <style>
    /* 进入动画 */
    .fade-in { opacity: 0; transform: translateY(20px); transition: opacity .5s ease, transform .5s ease; }
    .fade-in.visible { opacity: 1; transform: none; }

    /* 进度条 */
    .bar-fill { height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700; color: white; width: 0; transition: width 1.2s cubic-bezier(.25,.46,.45,.94); }

    /* 顶部阅读进度条 */
    #read-progress { position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, #3b82f6, #60a5fa); width: 0%; z-index: 100; transition: width .1s; }

    /* 目录激活项 */
    .toc-link { transition: all .2s; }
    .toc-link.active { color: var(--tw-text-primary, #60a5fa); border-left-color: var(--tw-border-primary, #3b82f6); font-weight: 600; }

    /* 平滑滚动偏移（避免被粘性 header 遮住） */
    .section-anchor { scroll-margin-top: 80px; }

    /* 引用块左边框动画 */
    @keyframes pulse-border { 0%,100%{border-color:#3b82f6} 50%{border-color:#60a5fa} }
  </style>
</head>
<body class="bg-[#0d1117] text-slate-200 font-sans antialiased">

  <!-- 顶部阅读进度条 -->
  <div id="read-progress"></div>

  <!-- 粘性顶部导航栏 -->
  <header class="sticky top-0 z-50 bg-[#0d1117]/90 backdrop-blur border-b border-border">
    <div class="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
      <div class="text-sm font-semibold text-slate-300">[文章/产品名称]</div>
      <div class="text-xs text-muted">[来源] · [日期]</div>
    </div>
  </header>

  <div class="max-w-6xl mx-auto px-6 pb-20">

    <!-- Hero 区域 -->
    <div class="py-14 border-b border-border mb-10">
      <div class="text-xs tracking-widest uppercase text-accent font-bold mb-3">[分类标签]</div>
      <h1 class="text-5xl font-black leading-tight text-white mb-4 max-w-3xl">[大标题]</h1>
      <p class="text-lg text-muted leading-relaxed max-w-2xl mb-8">[副标题：1-2句核心结论]</p>
      <!-- 关键数字统计行 -->
      <div class="flex flex-wrap gap-6">
        <div class="flex flex-col">
          <span class="text-3xl font-black text-primary">[数字]</span>
          <span class="text-xs text-muted mt-0.5">[指标说明]</span>
        </div>
        <div class="w-px bg-border"></div>
        <div class="flex flex-col">
          <span class="text-3xl font-black text-primary">[数字]</span>
          <span class="text-xs text-muted mt-0.5">[指标说明]</span>
        </div>
        <!-- 按需重复 -->
      </div>
    </div>

    <!-- 主体：目录 + 内容 -->
    <div class="flex gap-10 items-start">

      <!-- 左侧固定目录 -->
      <aside class="hidden lg:block w-52 shrink-0 sticky top-20 self-start">
        <div class="text-xs tracking-widest uppercase text-muted font-bold mb-3">目录</div>
        <nav id="toc" class="flex flex-col gap-1">
          <a href="#s-bg" class="toc-link text-sm text-slate-400 border-l-2 border-transparent pl-3 py-1 hover:text-accent">背景与意义</a>
          <a href="#s-feature" class="toc-link text-sm text-slate-400 border-l-2 border-transparent pl-3 py-1 hover:text-accent">核心能力</a>
          <a href="#s-data" class="toc-link text-sm text-slate-400 border-l-2 border-transparent pl-3 py-1 hover:text-accent">数据对比</a>
          <a href="#s-how" class="toc-link text-sm text-slate-400 border-l-2 border-transparent pl-3 py-1 hover:text-accent">技术原理</a>
          <a href="#s-summary" class="toc-link text-sm text-slate-400 border-l-2 border-transparent pl-3 py-1 hover:text-accent">总结要点</a>
          <!-- 按章节数量添加 -->
        </nav>
      </aside>

      <!-- 右侧内容区 -->
      <main class="flex-1 min-w-0 flex flex-col gap-16">

        <!-- ══ 章节：背景 ══ -->
        <section id="s-bg" class="section-anchor fade-in">
          <h2 class="text-2xl font-black text-white mb-5 flex items-center gap-2">
            <span class="text-primary text-lg">§</span> [章节标题]
          </h2>
          <!-- 段落正文 -->
          <p class="text-base text-slate-300 leading-relaxed mb-4">
            [核心讲解段落。这里是文章正文，比课件模式有更高的信息密度。用完整的句子解释背景、来龙去脉。]
          </p>
          <p class="text-base text-slate-300 leading-relaxed mb-6">
            [第二段，展开细节或给出类比。]
          </p>
          <!-- 内联高亮块（重要结论） -->
          <div class="bg-primary/10 border border-primary/25 rounded-xl p-5 my-4">
            <div class="text-xs text-accent font-bold mb-2 tracking-wide">💡 关键结论</div>
            <p class="text-sm text-slate-200 leading-relaxed font-medium">[一句话关键结论，视觉上更突出]</p>
          </div>
        </section>

        <!-- ══ 章节：核心能力（带内联数字卡） ══ -->
        <section id="s-feature" class="section-anchor fade-in">
          <h2 class="text-2xl font-black text-white mb-5 flex items-center gap-2">
            <span class="text-primary text-lg">§</span> [章节标题]
          </h2>
          <p class="text-base text-slate-300 leading-relaxed mb-6">[段落说明]</p>

          <!-- 内联数字卡片行 -->
          <div class="grid grid-cols-3 gap-4 my-6">
            <div class="bg-card border border-border rounded-xl p-4 text-center">
              <div class="text-4xl font-black text-primary leading-none">[数字]</div>
              <div class="text-xs text-muted mt-1.5">[说明]</div>
            </div>
            <div class="bg-card border border-border rounded-xl p-4 text-center">
              <div class="text-4xl font-black text-primary leading-none">[数字]</div>
              <div class="text-xs text-muted mt-1.5">[说明]</div>
            </div>
            <div class="bg-card border border-border rounded-xl p-4 text-center">
              <div class="text-4xl font-black text-primary leading-none">[数字]</div>
              <div class="text-xs text-muted mt-1.5">[说明]</div>
            </div>
          </div>

          <!-- 特性列表 -->
          <div class="flex flex-col gap-3 mt-4">
            <div class="flex gap-4 items-start bg-card border border-border rounded-xl p-4">
              <span class="text-2xl shrink-0">[图标]</span>
              <div>
                <div class="font-bold text-white text-sm mb-1">[特性标题]</div>
                <p class="text-xs text-muted leading-relaxed">[特性说明，2-3句话]</p>
              </div>
            </div>
            <!-- 按需重复 -->
          </div>
        </section>

        <!-- ══ 章节：数据对比（进度条） ══ -->
        <section id="s-data" class="section-anchor fade-in">
          <h2 class="text-2xl font-black text-white mb-5 flex items-center gap-2">
            <span class="text-primary text-lg">§</span> [章节标题]
          </h2>
          <p class="text-base text-slate-300 leading-relaxed mb-6">[讲清楚这组数据的来源和意义]</p>

          <!-- 进度条对比 -->
          <div class="bg-card border border-border rounded-2xl p-6">
            <div class="text-sm font-bold text-white mb-4">[指标名称]（越高越好）</div>
            <div class="flex flex-col gap-3" id="bars-main">
              <div class="flex items-center gap-3">
                <div class="w-32 text-right text-xs text-accent font-medium shrink-0">[主角]</div>
                <div class="flex-1 h-6 bg-white/[.06] rounded-md overflow-hidden">
                  <div class="bar-fill bg-gradient-to-r from-blue-900 to-primary" data-w="82">82%</div>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-32 text-right text-xs text-muted shrink-0">[对比A]</div>
                <div class="flex-1 h-6 bg-white/[.06] rounded-md overflow-hidden">
                  <div class="bar-fill bg-gradient-to-r from-slate-700 to-slate-500" data-w="75">75%</div>
                </div>
              </div>
            </div>
            <!-- 📷 参考图（可选） -->
            <div class="mt-5 pt-5 border-t border-border">
              <div class="text-xs text-muted mb-2">📷 参考图：[图片说明]</div>
              <img src="[图片路径]" alt="[描述]" class="rounded-lg opacity-80 max-w-full">
            </div>
          </div>
        </section>

        <!-- ══ 章节：技术原理（步骤流程） ══ -->
        <section id="s-how" class="section-anchor fade-in">
          <h2 class="text-2xl font-black text-white mb-5 flex items-center gap-2">
            <span class="text-primary text-lg">§</span> [章节标题]
          </h2>
          <p class="text-base text-slate-300 leading-relaxed mb-6">[段落说明]</p>

          <!-- 引用块 -->
          <blockquote class="border-l-4 border-primary bg-primary/[.05] rounded-r-xl pl-5 pr-4 py-4 my-4 italic text-slate-300 text-sm leading-relaxed">
            "[原文最有价值的表述]"
            <cite class="block mt-2 text-xs text-muted not-italic">— [来源]</cite>
          </blockquote>

          <!-- 步骤流程 -->
          <div class="flex flex-col gap-0 mt-4">
            <div class="flex gap-4 items-start">
              <div class="w-7 h-7 rounded-full bg-primary text-white font-extrabold text-xs flex items-center justify-center shrink-0 mt-0.5">1</div>
              <div class="pb-4 flex-1">
                <div class="font-bold text-white text-sm mb-1">[步骤标题]</div>
                <p class="text-xs text-muted leading-relaxed">[步骤说明，具体、有细节]</p>
              </div>
            </div>
            <div class="w-px h-5 bg-gradient-to-b from-primary to-border ml-3.5"></div>
            <div class="flex gap-4 items-start">
              <div class="w-7 h-7 rounded-full bg-primary text-white font-extrabold text-xs flex items-center justify-center shrink-0 mt-0.5">2</div>
              <div class="pb-4 flex-1">
                <div class="font-bold text-white text-sm mb-1">[步骤标题]</div>
                <p class="text-xs text-muted leading-relaxed">[步骤说明]</p>
              </div>
            </div>
          </div>
        </section>

        <!-- ══ 总结章节 ══ -->
        <section id="s-summary" class="section-anchor fade-in">
          <h2 class="text-2xl font-black text-white mb-5 flex items-center gap-2">
            <span class="text-primary text-lg">§</span> 核心要点总结
          </h2>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-card border border-border rounded-xl p-4 flex gap-3 items-start">
              <span class="text-xl shrink-0">🏆</span>
              <p class="text-xs text-muted leading-relaxed"><strong class="text-white">[关键词]</strong>：[一句话说明]</p>
            </div>
            <!-- 3-5 个要点 -->
          </div>
          <!-- 原文链接 -->
          <div class="mt-8 pt-6 border-t border-border text-sm text-muted">
            原文来源：<a href="[原始URL]" target="_blank" class="text-accent hover:underline">[网页标题]</a>
          </div>
        </section>

      </main>
    </div>
  </div>

  <script>
    // 进度条初始化
    document.querySelectorAll('.bar-fill[data-w]').forEach(b => { b.style.width = '0%'; });

    // IntersectionObserver：淡入动画
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          e.target.querySelectorAll('.bar-fill[data-w]').forEach(bar => {
            bar.style.width = '0%';
            requestAnimationFrame(() => requestAnimationFrame(() => { bar.style.width = bar.dataset.w + '%'; }));
          });
        }
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('.fade-in').forEach(el => io.observe(el));

    // 目录高亮：当前章节滚动到视口时激活对应 TOC 链接
    const sections = document.querySelectorAll('section[id]');
    const tocLinks = document.querySelectorAll('#toc .toc-link');
    const tocObserver = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          tocLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
        }
      });
    }, { threshold: 0.4 });
    sections.forEach(s => tocObserver.observe(s));

    // 顶部阅读进度条
    window.addEventListener('scroll', () => {
      const total = document.body.scrollHeight - window.innerHeight;
      document.getElementById('read-progress').style.width = (window.scrollY / total * 100) + '%';
    });
  </script>
</body>
</html>
```

---

## 与课件模式（Slideshow）的区别

| 对比维度 | 课件模式 | 深度讲解模式 |
|---------|---------|------------|
| 滚动方式 | 全屏分页（每页100vh） | 自由连续滚动 |
| 信息密度 | 低（每屏1件事） | 高（完整段落+细节） |
| 导航 | 右侧圆点 | 左侧固定目录 |
| 适合场景 | OBS录视频 | 分享链接/深度阅读 |
| 文字量 | 简短（标题+要点） | 完整（段落+解释） |
| 图片处理 | 右侧小参考图 | 内联于章节中 |
