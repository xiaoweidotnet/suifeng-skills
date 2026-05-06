# 课件 HTML 模板规范（Tailwind CSS 版）

## 核心原则：文字为主，图片为辅

> 课件的主角是**文字讲解和逻辑梳理**。
> 图片仅作为"📷 参考图"出现在右侧，且必须附带说明文字。
>
> | 内容类型 | 在课件中的角色 |
> |---------|--------------|
> | 文字解释、背景原理 | **主角**，左栏 60%，醒目展示 |
> | 数字指标、进度条对比 | **主角**，右栏可视化 |
> | 原文图表（已提取数据） | **配角**，右栏小参考图，≤右栏 80% 宽 |
> | 产品截图、界面图 | **配角**，带说明文字 |
> | 纯装饰图、品牌图 | **忽略**，不出现在课件中 |

---

## 技术栈

使用 **Tailwind CSS Play CDN**（无需构建工具，单文件可运行）：

```html
<script src="https://cdn.tailwindcss.com"></script>
```

通过内联 `tailwind.config` 注入品牌色，只保留**极少量**自定义 CSS（仅限 `@keyframes` 动画和进度条宽度过渡，这两类 Tailwind 无法纯靠类名实现）。

---

## HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[课件标题]</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '#f97316',   /* 主色，根据品牌换 */
            accent:  '#fb923c',   /* 强调色 */
            muted:   '#8892aa',   /* 次要文字 */
            card:    '#1c1f2e',   /* 卡片背景 */
            border:  '#252838',   /* 边框 */
          },
          fontFamily: {
            sans: ['-apple-system', 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'sans-serif'],
          },
        }
      }
    }
  </script>
  <style>
    /* 仅保留 Tailwind 无法覆盖的部分 */

    /* 进入动画（JS 用 .visible 触发） */
    .anim { opacity: 0; transform: translateY(32px); transition: opacity .6s ease, transform .6s ease; }
    .anim.visible { opacity: 1; transform: none; }
    .d1 { transition-delay: .1s }
    .d2 { transition-delay: .22s }
    .d3 { transition-delay: .36s }
    .d4 { transition-delay: .5s }

    /* 进度条宽度过渡（Tailwind 的 w-* 不支持动态数值） */
    .bar-fill { height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 12px; font-weight: 700; color: white; width: 0; transition: width 1.2s cubic-bezier(.25,.46,.45,.94); }

    /* 封面浮动动画 */
    @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
    .float { animation: float 3s ease-in-out infinite; }

    /* 底部滚动提示 */
    @keyframes bounce-y { 0%,100%{transform:translateX(-50%) translateY(0)} 50%{transform:translateX(-50%) translateY(6px)} }
    .scroll-hint { animation: bounce-y 2s ease-in-out infinite; }

    /* 导航圆点激活态 */
    .dot.active { background-color: var(--tw-dot-color, #fb923c); border-color: var(--tw-dot-color, #fb923c); transform: scale(1.5); }

    /* 渐变文字（cover title） */
    .gradient-text { background: linear-gradient(135deg, #fff 20%, #fed7aa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  </style>
</head>
<body class="bg-gray-950 text-gray-100 font-sans overflow-x-hidden">

  <!-- 侧边导航圆点 -->
  <nav id="dot-nav" class="fixed right-5 top-1/2 -translate-y-1/2 flex flex-col gap-2 z-50">
    <a href="#s1" class="dot w-2 h-2 rounded-full bg-white/25 border border-white/40 transition-all duration-300 cursor-pointer block"></a>
    <!-- 每个 section 各一个 <a> -->
  </nav>

  <!-- 全屏区块 -->
  <section class="section min-h-screen w-full flex flex-col items-center justify-center relative overflow-hidden px-20 py-14" id="s1">
    <!-- 内容 -->
  </section>

  <script>/* JS 见下方 */</script>
</body>
</html>
```

---

## 配色方案（修改 `tailwind.config` 中的 `colors`）

| 主题 | primary | accent | 背景 class |
|------|---------|--------|-----------|
| 🔥 科技橙（默认） | `#f97316` | `#fb923c` | `bg-[#0f1117]` |
| 🔴 活力红 | `#e8374e` | `#f87085` | `bg-[#0d0b0c]` |
| 🔵 科技蓝 | `#3b82f6` | `#60a5fa` | `bg-[#0a0f1e]` |
| 🟢 自然绿 | `#22c55e` | `#4ade80` | `bg-[#0a1410]` |
| 🟣 优雅紫 | `#a855f7` | `#c084fc` | `bg-[#0f0a1e]` |

根据网页品牌色选择，或用任意十六进制色通过 `bg-[#hex]` 直接使用。

---

## 区块类型与 Tailwind 写法

### 封面页

```html
<section class="section min-h-screen flex flex-col items-center justify-center text-center px-20 py-14 relative overflow-hidden"
         id="s1"
         style="background: linear-gradient(150deg, #07080d, #1a0b04, #2d1000)">

  <!-- 径向光晕背景（decorative） -->
  <div class="absolute inset-0 pointer-events-none"
       style="background: radial-gradient(ellipse at 50% 50%, rgba(249,115,22,.15), transparent 70%)"></div>

  <div class="anim">
    <div class="text-6xl mb-3 float">🚀</div>
  </div>
  <div class="anim d1">
    <div class="text-xs tracking-widest uppercase text-white/40 mb-2">[来源] · [日期]</div>
  </div>
  <div class="anim d2">
    <h1 class="gradient-text font-black leading-tight mb-4" style="font-size: clamp(48px,7vw,86px)">[大标题]</h1>
  </div>
  <div class="anim d3">
    <div class="text-lg font-bold border border-white/25 rounded-full px-6 py-1.5 inline-block mb-5 text-white/90">
      [核心亮点一句话]
    </div>
  </div>
  <div class="anim d4">
    <p class="text-base text-white/60 max-w-xl mx-auto leading-relaxed mb-6">[2-3句简介，包含最震撼的数字]</p>
    <div class="flex flex-wrap gap-2 justify-center">
      <span class="px-3.5 py-1.5 bg-white/6 border border-white/15 rounded-full text-sm text-white/80">📌 [亮点1]</span>
      <span class="px-3.5 py-1.5 bg-white/6 border border-white/15 rounded-full text-sm text-white/80">📌 [亮点2]</span>
      <span class="px-3.5 py-1.5 bg-white/6 border border-white/15 rounded-full text-sm text-white/80">📌 [亮点3]</span>
    </div>
  </div>

  <!-- 滚动提示 -->
  <div class="scroll-hint absolute bottom-5 left-1/2 text-xs text-white/30 tracking-widest">↓ 向下滚动</div>
</section>
```

### 目录页

```html
<section class="section min-h-screen flex flex-col items-center justify-center px-20 py-14" id="s2">
  <div class="anim text-center mb-8">
    <div class="text-xs tracking-widest uppercase text-accent font-bold mb-2">课件目录</div>
    <h2 class="text-4xl font-black mb-3">📋 今天讲 N 个核心要点</h2>
    <p class="text-muted text-base leading-relaxed">副标题说明</p>
  </div>
  <div class="anim d1 w-full max-w-lg flex flex-col gap-2.5">
    <div class="flex items-center gap-4 bg-card border border-border rounded-xl px-5 py-3 text-base font-medium">
      <span class="text-xs font-extrabold text-primary bg-primary/10 w-7 h-7 rounded-lg flex items-center justify-center shrink-0">01</span>
      [图标] [知识点1]
    </div>
    <div class="flex items-center gap-4 bg-card border border-border rounded-xl px-5 py-3 text-base font-medium">
      <span class="text-xs font-extrabold text-primary bg-primary/10 w-7 h-7 rounded-lg flex items-center justify-center shrink-0">02</span>
      [图标] [知识点2]
    </div>
    <!-- 按需重复 -->
  </div>
</section>
```

### 知识点页（双栏，核心布局）

```html
<section class="section min-h-screen flex flex-col items-center justify-center px-20 py-14" id="s3">

  <!-- 标题区 -->
  <div class="anim w-full max-w-5xl mb-6">
    <div class="text-xs tracking-widest uppercase text-accent font-bold mb-1">知识点 01</div>
    <h2 class="text-4xl font-black leading-tight">[图标] [标题]</h2>
  </div>

  <!-- 双栏内容 -->
  <div class="anim d1 w-full max-w-5xl grid grid-cols-2 gap-5 items-start">

    <!-- 左栏：文字讲解（主体） -->
    <div class="flex flex-col gap-3.5">

      <!-- 核心洞察（必须有） -->
      <div class="bg-card border-l-4 border-primary rounded-r-xl p-5">
        <div class="text-xs text-muted mb-1.5">🔑 核心洞察</div>
        <p class="text-sm text-gray-200 leading-relaxed">
          [2-3句解释：这个知识点是什么、为什么重要。用通俗语言，可用类比。]
        </p>
      </div>

      <!-- 原理/背景（推荐有） -->
      <div class="bg-card border-l-4 border-primary rounded-r-xl p-5">
        <div class="text-xs text-muted mb-1.5">💡 原理/背景</div>
        <p class="text-sm text-gray-200 leading-relaxed">
          [解释背后原理，或这个结果是怎么来的。]
        </p>
      </div>

      <!-- 补充说明（可选） -->
      <div class="bg-white/[.04] border-l-[3px] border-accent rounded-r-lg px-4 py-3 text-sm text-muted leading-relaxed">
        [补充说明、注意事项、与其他知识点的关联。]
      </div>

    </div>

    <!-- 右栏：数据可视化 + 可选小参考图 -->
    <div class="flex flex-col gap-3">

      <!-- 大数字卡片 -->
      <div class="flex gap-4 flex-wrap">
        <div class="bg-card border border-border rounded-2xl px-6 py-5 text-center flex-1 min-w-[140px]">
          <div class="font-black leading-none text-primary" style="font-size: clamp(44px,6vw,64px)">[数字]<span class="text-[.45em] text-accent">[单位]</span></div>
          <div class="text-xs text-muted mt-1">[数字说明]</div>
          <div class="inline-block mt-1.5 px-2.5 py-0.5 rounded-lg text-xs font-bold bg-primary/10 text-accent">[标签]</div>
        </div>
      </div>

      <!-- 进度条对比 -->
      <div class="text-xs text-muted mb-1">📊 [指标名称]对比（越高越好）</div>
      <div class="flex flex-col gap-2" id="bars-xxx">
        <div class="flex items-center gap-2.5">
          <div class="w-28 text-right text-xs text-accent shrink-0">[主角名称]</div>
          <div class="flex-1 h-5 bg-white/[.06] rounded-md overflow-hidden">
            <div class="bar-fill bg-gradient-to-r from-orange-900 to-primary" data-w="80">80%</div>
          </div>
        </div>
        <div class="flex items-center gap-2.5">
          <div class="w-28 text-right text-xs text-muted shrink-0">[对比项]</div>
          <div class="flex-1 h-5 bg-white/[.06] rounded-md overflow-hidden">
            <div class="bar-fill bg-gradient-to-r from-gray-700 to-gray-500" data-w="75">75%</div>
          </div>
        </div>
      </div>

      <!-- 📷 参考图（可选，仅折线/架构/散点图才放） -->
      <div class="text-xs text-muted mt-1">📷 参考图：[图片说明]</div>
      <img src="[图片路径]" alt="[描述]" class="rounded-xl shadow-2xl opacity-85 max-w-full">
      <div class="bg-white/[.04] border-l-[3px] border-accent rounded-r-lg px-4 py-3 text-xs text-muted leading-relaxed">
        [一句话说明这张图的核心信息]
      </div>

    </div>
  </div>
</section>
```

### 步骤/流程页

```html
<section class="section min-h-screen flex flex-col items-center justify-center px-20 py-14" id="sN">
  <div class="anim w-full max-w-5xl mb-6">
    <div class="text-xs tracking-widest uppercase text-accent font-bold mb-1">知识点 0N</div>
    <h2 class="text-4xl font-black">[图标] [标题]</h2>
    <p class="text-muted text-sm mt-2 leading-relaxed">[一句话说明]</p>
  </div>
  <div class="anim d1 w-full max-w-5xl grid grid-cols-2 gap-5 items-start">
    <!-- 左栏：背景说明 -->
    <div class="flex flex-col gap-3.5">
      <div class="bg-card border-l-4 border-primary rounded-r-xl p-5">
        <div class="text-xs text-muted mb-1.5">💡 背景</div>
        <p class="text-sm text-gray-200 leading-relaxed">[背景说明]</p>
      </div>
    </div>
    <!-- 右栏：步骤 -->
    <div class="flex flex-col">
      <!-- 步骤1 -->
      <div class="flex gap-3.5 items-start">
        <div class="w-8 h-8 rounded-full bg-primary text-white font-extrabold text-sm flex items-center justify-center shrink-0">1</div>
        <div class="pb-4 flex-1">
          <h4 class="text-base font-bold mb-1">[步骤标题]</h4>
          <p class="text-xs text-muted leading-relaxed">[步骤说明]</p>
        </div>
      </div>
      <!-- 连接线 -->
      <div class="w-0.5 h-6 bg-gradient-to-b from-primary to-border ml-[15px] my-1"></div>
      <!-- 步骤2 -->
      <div class="flex gap-3.5 items-start">
        <div class="w-8 h-8 rounded-full bg-primary text-white font-extrabold text-sm flex items-center justify-center shrink-0">2</div>
        <div class="pb-4 flex-1">
          <h4 class="text-base font-bold mb-1">[步骤标题]</h4>
          <p class="text-xs text-muted leading-relaxed">[步骤说明]</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

### 金句/引用页（可选）

```html
<section class="section min-h-screen flex flex-col items-center justify-center text-center px-20 py-14" id="sN">
  <div class="anim max-w-2xl">
    <div class="text-7xl text-accent/20 leading-none font-serif mb-2">"</div>
    <p class="italic font-light text-white/90 leading-relaxed" style="font-size: clamp(17px,2.5vw,26px)">
      [原文最有价值的一句话]
    </p>
    <div class="text-sm text-muted mt-4">— [来源]</div>
  </div>
</section>
```

### 总结页（必须有）

```html
<section class="section min-h-screen flex flex-col items-center justify-center px-20 py-14" id="sLast">
  <div class="anim text-center mb-6">
    <div class="text-xs tracking-widest uppercase text-accent font-bold mb-1">总结回顾</div>
    <h2 class="text-4xl font-black">🎯 今天学到了什么</h2>
  </div>
  <div class="anim d1 flex gap-3.5 flex-wrap justify-center max-w-5xl">
    <div class="bg-card border border-border rounded-2xl p-5 w-40 flex flex-col items-center gap-2 text-center">
      <span class="text-3xl">🏆</span>
      <p class="text-xs text-muted leading-relaxed"><strong class="text-gray-200">[关键数字]</strong> [一句话说明]</p>
    </div>
    <!-- 3-5 个要点，按需重复 -->
  </div>
  <div class="anim d2 mt-6">
    <p class="text-xs text-muted/60">
      内容来源：<a href="[原始URL]" target="_blank" class="text-accent hover:underline">[网页标题]</a>
    </p>
  </div>
</section>
```

---

## JavaScript（完整，复制粘贴可用）

```javascript
// 初始化进度条宽度为 0（由 JS 动画驱动）
document.querySelectorAll('.bar-fill[data-w]').forEach(b => { b.style.width = '0%'; });

function animateBarsIn(sectionEl) {
  sectionEl.querySelectorAll('.bar-fill[data-w]').forEach(bar => {
    bar.style.width = '0%';
    requestAnimationFrame(() => requestAnimationFrame(() => { bar.style.width = bar.dataset.w + '%'; }));
  });
}

const sections = document.querySelectorAll('.section');
const dots = document.querySelectorAll('#dot-nav .dot');
let currentIdx = 0;

// 区块进入视口：触发进入动画 + 更新导航圆点
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      dots.forEach(d => d.classList.toggle('active', d.getAttribute('href') === '#' + e.target.id));
      e.target.querySelectorAll('.anim').forEach(el => el.classList.add('visible'));
      animateBarsIn(e.target);
    }
  });
}, { threshold: 0.3 });
sections.forEach(s => io.observe(s));

// 键盘方向键控制
const secArr = Array.from(sections);
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown' || e.key === 'PageDown') {
    e.preventDefault();
    currentIdx = Math.min(currentIdx + 1, secArr.length - 1);
    secArr[currentIdx].scrollIntoView({ behavior: 'smooth' });
  }
  if (e.key === 'ArrowUp' || e.key === 'PageUp') {
    e.preventDefault();
    currentIdx = Math.max(currentIdx - 1, 0);
    secArr[currentIdx].scrollIntoView({ behavior: 'smooth' });
  }
});
const ioIdx = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) currentIdx = secArr.indexOf(e.target); });
}, { threshold: 0.5 });
secArr.forEach(s => ioIdx.observe(s));

// 触摸滑动
let touchY = 0;
document.addEventListener('touchstart', e => { touchY = e.touches[0].clientY; });
document.addEventListener('touchend', e => {
  const d = touchY - e.changedTouches[0].clientY;
  if (Math.abs(d) > 50) {
    currentIdx = d > 0
      ? Math.min(currentIdx + 1, secArr.length - 1)
      : Math.max(currentIdx - 1, 0);
    secArr[currentIdx].scrollIntoView({ behavior: 'smooth' });
  }
});
```

---

## 常用 Tailwind 类速查

| 效果 | Tailwind 类 |
|------|------------|
| 深色卡片 | `bg-card border border-border rounded-2xl p-5` |
| 左边框卡片 | `border-l-4 border-primary rounded-r-xl p-5` |
| 淡背景说明卡 | `bg-white/[.04] border-l-[3px] border-accent rounded-r-lg px-4 py-3` |
| 大数字 | `font-black leading-none text-primary text-6xl` |
| Eyebrow 标签 | `text-xs tracking-widest uppercase text-accent font-bold` |
| 章节大标题 | `text-4xl font-black leading-tight` |
| 次要文字 | `text-sm text-muted leading-relaxed` |
| 双栏布局 | `grid grid-cols-2 gap-5 items-start` |
| 左宽双栏 | `grid grid-cols-[1.4fr_1fr] gap-6 items-start` |
| 目录列表项 | `flex items-center gap-4 bg-card border border-border rounded-xl px-5 py-3` |
| 标签徽章 | `inline-block px-2.5 py-0.5 rounded-lg text-xs font-bold bg-primary/10 text-accent` |
| 绿色标签 | `bg-green-950 text-green-400` |
| 蓝色标签 | `bg-blue-950 text-blue-400` |
| 圆形数字 | `w-8 h-8 rounded-full bg-primary text-white font-extrabold text-sm flex items-center justify-center shrink-0` |

---

## 图片使用规则

| 图片类型 | 处理方式 |
|---------|---------|
| 数据柱状/饼图 → 提取数值 | 转为 `bar-fill` 进度条，**不需要放原图** |
| 折线趋势图 | 转文字 + 进度条，**同时放小参考图**（趋势难以文字化）|
| 散点分布图 | 转文字说明，**同时放小参考图** |
| 架构/流程图 | 转步骤卡片文字，**同时放小参考图** |
| 产品截图 | 直接放小图 + 文字说明关键点 |
| 品牌/装饰图 | **完全忽略** |

---

## 质量检查清单

- [ ] `<script src="https://cdn.tailwindcss.com"></script>` 已引入
- [ ] `tailwind.config` 中的品牌色与网页主题一致
- [ ] 每个知识点区块：左侧有 ≥2 段文字解释
- [ ] 从图片提取的数据已转化为进度条或大数字
- [ ] 每张放入课件的图片都有 `📷 参考图：[说明]` 标签 + 说明文字
- [ ] 没有图片单独占满整屏
- [ ] 封面有大标题 + 一句话简介 + 3 个 pill
- [ ] 总结页有 3-5 个要点卡片
- [ ] 侧边 `#dot-nav` 的 `<a>` 数量与 `section` 数量一致
- [ ] 进度条使用 `bar-fill` + `data-w` 属性（JS 动画驱动）
- [ ] 背景为深色（`bg-gray-950` 或自定义深色 hex）
- [ ] 仅 `<style>` 中保留 4 类自定义 CSS：`.anim`/`.bar-fill`/`@keyframes`/`.dot.active`
- [ ] 文件单独可运行（无本地依赖）
