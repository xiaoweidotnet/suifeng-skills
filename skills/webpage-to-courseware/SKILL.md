---
name: webpage-to-courseware
description: 将网页内容转化为精美互动展示页面。提供网页URL和可选的展示模式，自动抓取全文与图片（下载本地后视觉识别），生成文字为主、图片为辅的展示页面。支持三种模式：课件（录视频/录屏）、深度讲解（分享阅读）、速览卡片（快速浏览）。触发关键词：转课件、网页转课件、生成课件、网页讲解、速览、深度解读、webpage to courseware。
argument-hint: "[网页URL] [可选：课件|讲解|速览]"
allowed-tools: WebFetch, Bash, Read, Write, GenerateImage
---

# 网页内容转互动展示页面

将任意网页转化为适合自媒体讲解/深度阅读/快速分享的精美 HTML 页面。

## 核心设计理念

> **文字为主，图片为辅。**
>
> - ✅ 从图片中提取数据 → 转化为进度条/数字卡/步骤文字
> - ✅ 图片缩为小参考图，附带说明文字
> - ❌ 图片占满版面，没有文字解释

---

## 第零步：选择展示模式

在开始之前，**先确定展示模式**。判断优先级：

1. **用户明确指定** → 直接使用
2. **根据关键词推断**：

| 用户说了什么 | 选择模式 |
|------------|---------|
| 录视频、录屏、OBS、课件、幻灯片 | 🎬 **课件模式** |
| 讲清楚、讲透、深度、详细、来龙去脉 | 📖 **深度讲解模式** |
| 快速了解、速览、一眼、5分钟 | ⚡ **速览卡片模式** |

3. **无法判断** → 默认使用 🎬 **课件模式**，并在回复中告知用户"如需其他模式可指定"

### 三种模式简介

| 模式 | 模板文件 | 适合场景 |
|-----|---------|---------|
| 🎬 课件 | `templates/slideshow.md` | 全屏分页，录视频/录屏 |
| 📖 深度讲解 | `templates/explainer.md` | 固定目录+文章流，分享链接/深度阅读 |
| ⚡ 速览卡片 | `templates/quickview.md` | 瀑布流卡片，快速浏览/截图分享 |

详细选择指南见 [courseware-template.md](courseware-template.md)。

---

## 第一步：抓取网页内容

使用 `WebFetch` 工具抓取用户提供的 URL，**同时用 curl 保存原始 HTML**：

```bash
TMPDIR=$(mktemp -d)
PAGE_HTML="$TMPDIR/page.html"
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" "[URL]" -o "$PAGE_HTML"
echo "HTML 大小: $(wc -c < "$PAGE_HTML") bytes"
```

从抓取结果中提取：
- 网页标题、主体文本、段落结构、核心论点
- 关键数字指标（用于 Hero 区和大数字卡）

---

## 第二步：下载图片到本地

使用 [scripts/extract-images.py](scripts/extract-images.py) 提取图片 URL，再用 [scripts/download-images.py](scripts/download-images.py) 批量下载：

```bash
SKILL_DIR="/Users/xiaowei/.cursor/skills/webpage-to-courseware"
IMG_DIR="$TMPDIR/images"

python3 "$SKILL_DIR/scripts/extract-images.py" "[原始URL]" < "$PAGE_HTML" > "$TMPDIR/image_urls.txt"
python3 "$SKILL_DIR/scripts/download-images.py" "$IMG_DIR" --from-file "$TMPDIR/image_urls.txt"

echo "✅ 图片保存至: $IMG_DIR"
ls -lh "$IMG_DIR"
```

---

## 第三步：视觉识别图片 → 文字化

对每张成功下载的图片，使用 `Read` 工具读取，**重点是把图片内容转化为文字和数据**：

```
Read(path="/tmp/xxx/images/00_abc12345.jpg")
```

按图片类型整理为结构化摘要：

| 图片类型 | 识别重点 | 在页面中的处理 |
|---------|---------|--------------|
| 数据图表（柱/折线/散点） | 每个数值、坐标轴、趋势结论 | 转进度条+大数字，图片缩为参考图 |
| 对比表格 | 行列标题、具体数值、最值 | 转 HTML 对比条，图片缩为参考图 |
| 流程/架构图 | 节点、箭头、层级结构 | 转步骤卡片，图片缩为参考图 |
| 截图/产品图 | 界面文字、操作步骤 | 直接小图 + 文字说明 |
| 纯装饰/品牌图 | — | **忽略，不放入页面** |

---

## 第四步：整理内容大纲

汇总文字 + 图片识别结果，整理为与所选模式对应的大纲：

**课件模式大纲：**
```
封面（大标题 + 关键数字 pills）
目录（N 个知识点列表）
知识点1：[标题] → 左栏文字 + 右栏数字/进度条/小参考图
知识点2：...
总结（3-5 个要点卡片）
```

**深度讲解大纲：**
```
Hero（大标题 + 副标题 + 统计数字行）
§ 章节1：背景 → 完整段落 + 内联高亮块
§ 章节2：核心能力 → 段落 + 数字卡 + 特性列表
§ 章节3：数据对比 → 段落说明 + 进度条卡片
§ 章节4：技术原理 → 段落 + 引用 + 步骤流程
§ 总结：要点卡片 + 来源链接
```

**速览卡片大纲：**
```
Hero（标题 + 一句话 + 关键数字统计）
分组1：[主题] → 4-6 张混合类型卡片
分组2：[主题] → 3-4 张卡片
底部总结：3 个要点 + 来源
```

---

## 第五步：生成 HTML 页面

阅读对应模板文件，按规范生成完整单文件 HTML：

- **Tailwind CSS Play CDN**（无需构建，`<script src="https://cdn.tailwindcss.com"></script>`）
- `tailwind.config` 注入品牌色（根据网页主色调选择）
- `<style>` 中**只保留 4 类**无法用 Tailwind 替代的 CSS：
  - `.anim`/`.fade-in`/`.fade-up`：JS 驱动的进入动画
  - `.bar-fill`：进度条宽度过渡（动态数值）
  - `@keyframes`：浮动/弹跳等动画
  - `.dot.active` / `.toc-link.active`：导航激活态
- 图片优先使用本地绝对路径；无法下载的用原始 URL

**输出文件命名：**
- 课件模式：`courseware_[主题词].html`
- 深度讲解：`explainer_[主题词].html`
- 速览卡片：`quickview_[主题词].html`

---

## 输出规范

完成后告知用户：
- 文件路径 + 使用的展示模式
- 图片：共下载 N 张，其中 M 张转化为可视化元素，K 张作为参考图保留
- 页面结构：共 N 页/N 个章节/N 张卡片

---

## 模板参考

- **模板索引 + 通用规范**：[courseware-template.md](courseware-template.md)
- **课件模式详细规范**：[templates/slideshow.md](templates/slideshow.md)
- **深度讲解模式规范**：[templates/explainer.md](templates/explainer.md)
- **速览卡片模式规范**：[templates/quickview.md](templates/quickview.md)
