# 速览卡片模式（Quick View）

## 适用场景

- 网页内容有很多**并列知识点**，每个点说清楚即可
- 用户想快速了解一个新事物（"5分钟看懂"式内容）
- 适合在**社交媒体截图分享**，或供人快速浏览
- 内容本身比较简单，不需要深度展开

## 页面结构

```
┌─────────────────────────────────────────────────────────┐
│           顶部 Hero（标题 + 一句话 + 关键数字）           │
├─────────────────────────────────────────────────────────┤
│  ┌──────┐  ┌──────┐  ┌──────┐  ← 3列卡片瀑布流          │
│  │ 卡片 │  │ 卡片 │  │ 卡片 │                           │
│  │（宽）│  └──────┘  └──────┘                           │
│  └──────┘  ┌──────────────┐   ← 宽卡片（重点数据）       │
│  ┌──────┐  │    宽卡片     │                             │
│  │ 卡片 │  └──────────────┘                             │
│  └──────┘  ┌──────┐  ┌──────┐                           │
│            │ 卡片 │  │ 卡片 │                           │
│            └──────┘  └──────┘                           │
├─────────────────────────────────────────────────────────┤
│              底部：核心结论 + 来源链接                     │
└─────────────────────────────────────────────────────────┘
```

---

## HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[标题] | 速览</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '#8b5cf6',   /* 根据品牌色调整 */
            accent:  '#a78bfa',
            muted:   '#94a3b8',
            card:    '#16182a',
            border:  '#272a3e',
          }
        }
      }
    }
  </script>
  <style>
    .fade-up { opacity: 0; transform: translateY(24px); transition: opacity .5s ease, transform .5s ease; }
    .fade-up.visible { opacity: 1; transform: none; }
    .bar-fill { height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 700; color: white; width: 0; transition: width 1s cubic-bezier(.25,.46,.45,.94); }
    @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
    .float { animation: float 3s ease-in-out infinite; }
  </style>
</head>
<body class="bg-[#0e0f1a] text-slate-200 font-sans antialiased">

  <!-- Hero 区域 -->
  <div class="bg-gradient-to-br from-[#0e0f1a] via-[#16182a] to-[#1a1030] border-b border-border">
    <div class="max-w-5xl mx-auto px-8 py-16">
      <div class="float text-5xl mb-5 text-center">🚀</div>
      <div class="text-xs tracking-widest uppercase text-accent font-bold text-center mb-3">[来源] · [日期]</div>
      <h1 class="text-5xl font-black text-white text-center leading-tight mb-4">[大标题]</h1>
      <p class="text-base text-muted text-center max-w-xl mx-auto leading-relaxed mb-8">[一句话核心结论]</p>
      <!-- 关键数字统计 -->
      <div class="flex justify-center gap-8 flex-wrap">
        <div class="text-center">
          <div class="text-4xl font-black text-primary">[数字]</div>
          <div class="text-xs text-muted mt-1">[说明]</div>
        </div>
        <div class="w-px bg-border"></div>
        <div class="text-center">
          <div class="text-4xl font-black text-primary">[数字]</div>
          <div class="text-xs text-muted mt-1">[说明]</div>
        </div>
        <div class="w-px bg-border"></div>
        <div class="text-center">
          <div class="text-4xl font-black text-primary">[数字]</div>
          <div class="text-xs text-muted mt-1">[说明]</div>
        </div>
      </div>
    </div>
  </div>

  <!-- 卡片瀑布区 -->
  <main class="max-w-5xl mx-auto px-8 py-12">

    <!-- 分组标题（可选，按内容分块） -->
    <div class="text-xs tracking-widest uppercase text-accent font-bold mb-5">核心特性</div>

    <!-- 卡片网格：使用 Tailwind CSS columns 实现自适应瀑布流 -->
    <div class="columns-1 md:columns-2 lg:columns-3 gap-5 space-y-5">

      <!-- 卡片类型 A：普通说明卡（小卡片） -->
      <div class="fade-up break-inside-avoid bg-card border border-border rounded-2xl p-5">
        <div class="text-2xl mb-3">[图标]</div>
        <div class="font-bold text-white text-sm mb-2">[标题]</div>
        <p class="text-xs text-muted leading-relaxed">[2-3句说明，简洁直接]</p>
      </div>

      <!-- 卡片类型 B：数字大卡（突出一个核心指标） -->
      <div class="fade-up break-inside-avoid bg-card border border-border rounded-2xl p-5">
        <div class="text-xs text-muted mb-2">[指标名称]</div>
        <div class="text-5xl font-black text-primary leading-none mb-2">[数字]<span class="text-2xl text-accent">[单位]</span></div>
        <p class="text-xs text-muted leading-relaxed">[一句话说明这个数字意味着什么]</p>
        <div class="inline-block mt-3 px-2 py-0.5 rounded text-xs font-bold bg-primary/10 text-accent">[标签]</div>
      </div>

      <!-- 卡片类型 C：进度条对比卡（宽卡，跨列效果靠内容高度自然实现） -->
      <div class="fade-up break-inside-avoid bg-card border border-border rounded-2xl p-5">
        <div class="font-bold text-white text-sm mb-4">[对比标题]</div>
        <div class="flex flex-col gap-2.5" id="bars-card">
          <div class="flex items-center gap-2">
            <div class="w-24 text-right text-xs text-accent shrink-0">[主角]</div>
            <div class="flex-1 h-5 bg-white/[.06] rounded overflow-hidden">
              <div class="bar-fill bg-gradient-to-r from-violet-900 to-primary" data-w="85">85%</div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-24 text-right text-xs text-muted shrink-0">[对比A]</div>
            <div class="flex-1 h-5 bg-white/[.06] rounded overflow-hidden">
              <div class="bar-fill bg-gradient-to-r from-slate-700 to-slate-500" data-w="72">72%</div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-24 text-right text-xs text-muted shrink-0">[对比B]</div>
            <div class="flex-1 h-5 bg-white/[.06] rounded overflow-hidden">
              <div class="bar-fill bg-gradient-to-r from-slate-700 to-slate-500" data-w="60">60%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 卡片类型 D：列表卡（并列特性/功能） -->
      <div class="fade-up break-inside-avoid bg-card border border-border rounded-2xl p-5">
        <div class="text-2xl mb-3">[图标]</div>
        <div class="font-bold text-white text-sm mb-3">[标题]</div>
        <ul class="flex flex-col gap-2">
          <li class="text-xs text-muted flex items-center gap-2"><span class="text-accent">✓</span>[要点1]</li>
          <li class="text-xs text-muted flex items-center gap-2"><span class="text-accent">✓</span>[要点2]</li>
          <li class="text-xs text-muted flex items-center gap-2"><span class="text-accent">✓</span>[要点3]</li>
        </ul>
      </div>

      <!-- 卡片类型 E：步骤卡 -->
      <div class="fade-up break-inside-avoid bg-card border border-border rounded-2xl p-5">
        <div class="font-bold text-white text-sm mb-4">[步骤标题]</div>
        <div class="flex flex-col gap-0">
          <div class="flex gap-3 items-start">
            <div class="w-6 h-6 rounded-full bg-primary text-white font-black text-xs flex items-center justify-center shrink-0">1</div>
            <p class="text-xs text-muted leading-relaxed pb-3 flex-1">[第一步说明]</p>
          </div>
          <div class="w-px h-3 bg-border ml-3 -mt-1 mb-1"></div>
          <div class="flex gap-3 items-start">
            <div class="w-6 h-6 rounded-full bg-primary text-white font-black text-xs flex items-center justify-center shrink-0">2</div>
            <p class="text-xs text-muted leading-relaxed flex-1">[第二步说明]</p>
          </div>
        </div>
      </div>

      <!-- 卡片类型 F：引用金句卡 -->
      <div class="fade-up break-inside-avoid bg-primary/10 border border-primary/25 rounded-2xl p-5">
        <div class="text-4xl text-primary/30 font-serif leading-none mb-2">"</div>
        <p class="text-sm text-slate-200 italic leading-relaxed mb-3">[原文金句]</p>
        <div class="text-xs text-muted">— [来源]</div>
      </div>

      <!-- 卡片类型 G：图片卡（参考图+说明） -->
      <div class="fade-up break-inside-avoid bg-card border border-border rounded-2xl overflow-hidden">
        <img src="[图片路径]" alt="[描述]" class="w-full opacity-85">
        <div class="p-4">
          <div class="text-xs text-muted font-medium mb-1">📷 [图片说明标题]</div>
          <p class="text-xs text-muted leading-relaxed">[一句话说明图片核心信息]</p>
        </div>
      </div>

      <!-- 按需继续添加更多卡片 -->
    </div>

    <!-- 第二分组（可选） -->
    <div class="text-xs tracking-widest uppercase text-accent font-bold mt-12 mb-5">深入了解</div>
    <div class="columns-1 md:columns-2 lg:columns-3 gap-5 space-y-5">
      <!-- 更多卡片 -->
    </div>

    <!-- 底部总结 -->
    <div class="mt-14 pt-8 border-t border-border">
      <div class="text-lg font-black text-white mb-4">🎯 核心结论</div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-card border border-border rounded-xl p-4">
          <span class="text-xl">💡</span>
          <p class="text-xs text-muted mt-2 leading-relaxed"><strong class="text-white">[要点1标题]</strong>：[一句话说明]</p>
        </div>
        <div class="bg-card border border-border rounded-xl p-4">
          <span class="text-xl">🚀</span>
          <p class="text-xs text-muted mt-2 leading-relaxed"><strong class="text-white">[要点2标题]</strong>：[一句话说明]</p>
        </div>
        <div class="bg-card border border-border rounded-xl p-4">
          <span class="text-xl">🎯</span>
          <p class="text-xs text-muted mt-2 leading-relaxed"><strong class="text-white">[要点3标题]</strong>：[一句话说明]</p>
        </div>
      </div>
      <p class="text-xs text-muted/60 mt-6">
        内容来源：<a href="[原始URL]" target="_blank" class="text-accent hover:underline">[网页标题]</a>
      </p>
    </div>
  </main>

  <script>
    document.querySelectorAll('.bar-fill[data-w]').forEach(b => { b.style.width = '0%'; });

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
    }, { threshold: 0.1 });
    document.querySelectorAll('.fade-up').forEach(el => io.observe(el));
  </script>
</body>
</html>
```

---

## 卡片类型速查

| 卡片类型 | 用途 | 特征 |
|---------|------|------|
| A - 普通说明卡 | 介绍一个概念/特性 | 图标 + 标题 + 2-3句描述 |
| B - 数字大卡 | 突出单一核心指标 | 超大数字 + 单位 + 说明 |
| C - 进度条对比卡 | 多项数据横向对比 | 条形图 + 标签 |
| D - 列表卡 | 列举多个并列要点 | ✓ 打勾列表 |
| E - 步骤卡 | 展示流程/操作步骤 | 数字圆点 + 连接线 |
| F - 引用金句卡 | 原文亮眼表述 | 引号装饰 + 斜体 |
| G - 图片卡 | 参考图 + 说明 | 图片铺满顶部 + 文字底部 |

## 与其他模式的区别

| 对比维度 | 速览卡片 | 课件 | 深度讲解 |
|---------|---------|------|---------|
| 布局 | 瀑布流自由卡片 | 全屏分页 | 文章流+侧边目录 |
| 内容密度 | 中（卡片摘要） | 低（每屏1件事） | 高（完整段落） |
| 图片角色 | 卡片底图或内嵌图 | 右侧小参考图 | 内联章节中 |
| 最适合 | 快速分享截图/浏览 | OBS录视频 | 深度阅读/链接分享 |
