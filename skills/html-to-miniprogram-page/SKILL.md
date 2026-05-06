---
name: html-to-miniprogram-page
description: 将完整的HTML网页设计稿（含CSS、图片资源）转化为微信小程序原生页面（WXML/WXSS/JS）。Use when the user wants to: (1) Convert an HTML design/mockup to a WeChat Mini Program page, (2) Transform web frontend code to WXML/WXSS, (3) Port a web UI layout to mini-program with 1:1 visual fidelity, (4) Generate mini-program pages from HTML/CSS snippets or screenshots. 特别注意小程序顶部导航栏（自定义/系统默认）和底部tabBar的配置差异，项目使用Skyline渲染器。
---

# HTML 转小程序页面

## 核心原则

- **1:1 视觉复刻**：最终小程序页面必须与原HTML设计稿在布局、配色、间距、字体上完全一致。
- **小程序语法正确**：生成的 WXML/WXSS/JS/JSON 必须符合微信小程序原生语法规范。
- **导航栏意识**：顶部导航栏高度需适配，底部 tabBar 不写在页面中（由 app.json 统一配置）。
- **Skyline 兼容**：项目使用 Skyline 渲染器（glass-easel），注意默认 flex 布局和 border-box。
- **先检查后转换**：动手写代码前，必须先检查目标项目的 `app.json` 现有配置，避免与已有结构冲突。

## 转换流程

### 0. 转换前检查（必须先做）

在分析设计稿之前，**务必先读取目标小程序项目的 `app.json`**，确认以下关键配置：

#### 0.1 检查 `tabBar` 配置

```json
// 目标项目的 app.json
{
  "tabBar": { ... }   // <-- 是否存在？
}
```

| 场景 | 处理方式 |
|------|----------|
| `app.json` **已有** `tabBar` | 页面内**绝对不要写**底部导航代码；内容区域用 `padding-bottom` 预留 tabBar 高度 |
| `app.json` **没有** `tabBar`，但设计稿**有**底部导航 | 需要**在 `app.json` 中补充 `tabBar` 配置**；为每个 tab 准备 `iconPath` / `selectedIconPath` 图标；页面内不写底部导航 |
| `app.json` **没有** `tabBar`，设计稿**也没有**底部导航 | 页面内不写，无需处理 |

> **禁忌**：绝不允许在每个页面内重复写自定义底部导航。如果设计稿有底部导航而 `app.json` 没有 `tabBar`，必须先补充 `app.json` 配置，而不是把导航写到页面里。

#### 0.2 检查 `renderer` 和 `rendererOptions`

```json
{
  "renderer": "skyline",
  "rendererOptions": {
    "skyline": {
      "defaultDisplayBlock": true,     // <-- 注意这个！
      "defaultContentBox": true        // <-- 注意这个！
    }
  }
}
```

- 如果 `defaultDisplayBlock: true` → 元素默认是 `block`，不是 `flex`，需要时**显式写 `display: flex`**
- 如果 `defaultContentBox: true` → 元素默认是 `content-box`，不是 `border-box`，需要时**显式写 `box-sizing: border-box`**
- 不要 blindly 相信"Skyline 默认 flex + border-box"的说法，必须以 `app.json` 的实际配置为准

#### 0.3 检查 `navigationStyle`

```json
{
  "window": {
    "navigationStyle": "custom"   // <-- 全局自定义导航栏？
  }
}
```

- 如果全局 `navigationStyle: custom`，所有页面都不写系统导航栏，自行实现顶部标题栏
- 如果是 `default`，按单个页面的需求决定

---

### 1. 分析输入

- 识别 HTML 结构层次（容器、文本、图片、表单、列表等）
- 提取所有 CSS 样式（行内、内联、外链），记录颜色、字号、间距、圆角、阴影
- 列出图片资源及尺寸，标注是背景图还是 `<img>` 内容图
- 识别交互元素（按钮点击、表单提交、轮播、弹窗、下拉刷新等）
- **识别图标类型**：记录设计稿中使用的图标字体（如 Material Symbols、FontAwesome 等），这些无法直接在小程序中使用

### 2. 规划页面结构

- **判断导航栏模式**：原设计稿顶部是否有自定义标题栏？如果有，页面 JSON 配 `navigationStyle: custom`；否则用系统默认导航栏。
- **确认 tabBar**（基于 0.1 的检查结果）：
  - 若该页面属于底部 tab 页 → 页面内**不写**底部导航代码；内容区底部预留 `padding-bottom: calc(120rpx + env(safe-area-inset-bottom))`
  - 若 `app.json` 没有 `tabBar` 但设计稿有 → 先补充 `app.json` 的 `tabBar` 配置，再写页面
- **选择滚动方案**：
  - **优先使用 `page` 自身滚动**（推荐）
  - 避免使用 `scroll-view` 作为页面主滚动容器，尤其是嵌套在 flex 容器内时，Skyline 下高度计算极易失效
  - 只有局部滚动区域（如横向滚动卡片、固定高度的列表）才使用 `scroll-view`
- **识别可复用组件**：如卡片、列表项、弹窗等，评估是否需要拆分为自定义组件。

### 3. 图标处理策略

设计稿中的图标通常来自图标字体（如 Material Symbols），小程序无法直接加载外部字体。按优先级处理：

| 方案 | 适用场景 | 实现方式 |
|------|----------|----------|
| **CSS 绘制** | 简单几何图标（箭头、放大镜、方块等） | 用 `::before`/`::after` + `border`/`background` 绘制 |
| **本地图片** | 复杂图标、品牌 Logo | 导出为 PNG/SVG，放入 `images/` 目录 |
| **iconfont** | 大量图标需统一管理 | 在 iconfont.cn 创建项目，下载字体文件引入 |
| **系统图标** | 通用操作（如设置、分享） | 使用微信内置的 `icon` 组件（类型有限） |

**注意**：
- 绝不要把 `<span class="material-symbols-outlined">...</span>` 这类字体图标直接搬到 WXML 中，小程序无法渲染外部字体
- 图标颜色必须与设计稿一致，不能只画形状不管配色

### 4. HTML → WXML 转换

- 按标签映射表替换（详见 `references/html-to-wxml-mapping.md`）
- 保留 `class` 和 `id` 作为 WXSS 选择器依据
- 将事件属性转换为小程序事件（`onclick` → `bindtap` 等）
- 用 `wx:if` / `wx:for` 替代模板条件/循环语法

### 5. CSS → WXSS 转换

- 将 `px` 按 750px 设计稿基准转为 `rpx`（`1px = 1rpx`）
- 移除小程序不支持的属性（如 `cursor`、`*` 选择器，详见 `references/css-to-wxss-mapping.md`）
- **根据 `app.json` 的实际 `rendererOptions` 决定是否需要显式声明 `display: flex` 和 `box-sizing: border-box`**
- 页面根节点设置 `page { background-color: #xxx; }`

### 6. JS 逻辑转换

- 将 DOM 操作（`document.querySelector`、`innerHTML` 等）转换为小程序数据驱动（`setData`）
- 将原生事件处理转换为 Page 生命周期和事件函数
- 将 AJAX/Fetch 请求转换为 `wx.request`
- 常见交互模式参考 `references/interaction-patterns.md`

### 7. 图片资源处理

- 页面内使用的图片建议放入页面同级目录（如 `images/`）或上传到 CDN
- `<img src="...">` 转为 `<image src="..." mode="aspectFill|widthFix" />`
- 背景图优先用网络地址；如需本地背景图，用 `<image>` 模拟或确认 base64 方案

### 8. 质量检查

生成完成后逐项确认：

- [ ] **已读取 `app.json`**，确认 `tabBar` / `rendererOptions` / `navigationStyle` 配置
- [ ] WXML 中无 HTML 残留标签（如 `<div>`、`<span>`、`<br>`）
- [ ] WXSS 无 `*` 通配符选择器，无小程序不支持的伪类（如 `:hover`）
- [ ] **页面滚动正常**：使用 `page` 自身滚动，内容超出屏幕可上下滑动
- [ ] 若使用自定义导航栏，导航栏高度计算正确，内容不被遮挡
- [ ] **若页面是 tabBar 页**：`app.json` 已配置 `tabBar`，页面内**无**底部导航代码，内容底部已预留 `padding-bottom`
- [ ] **若设计稿有底部导航但 `app.json` 无 `tabBar`**：已补充 `app.json` 配置，不是把导航写到页面里
- [ ] 所有图标已处理（CSS 绘制 / 本地图片 / iconfont），无字体图标残留
- [ ] 所有交互元素有对应 `bindtap` / `bindinput` / `bindsubmit` 事件
- [ ] 图片路径正确，`mode` 属性设置合理
- [ ] 页面 `.json` 配置完整（`navigationBarTitleText`、`navigationStyle`、`renderer: skyline` 等）

## 关键注意事项

### 顶部导航栏

| 模式 | 页面 JSON 配置 | WXML 处理 |
|------|---------------|-----------|
| 系统默认导航栏 | `"navigationStyle": "default"` | **不写导航栏代码**，页面内容从导航栏下方自动开始 |
| 完全自定义导航栏 | `"navigationStyle": "custom"` | 自行实现标题栏，需计算状态栏高度+胶囊按钮高度 |

自定义导航栏 JS 计算示例：
```javascript
Page({
  data: {
    statusBarHeight: 0,
    navBarHeight: 44
  },
  onLoad() {
    const sys = wx.getSystemInfoSync();
    const menu = wx.getMenuButtonBoundingClientRect();
    this.setData({
      statusBarHeight: sys.statusBarHeight,
      navBarHeight: (menu.top - sys.statusBarHeight) * 2 + menu.height
    });
  }
});
```

### 底部 TabBar（反复强调）

**`tabBar` 只能在 `app.json` 中配置，页面内绝对不要写底部固定导航条代码。**

正确的分工：
- `app.json`：配置 `tabBar.list`，定义 tab 的页面路径、文字、图标
- 页面 `.wxss`：内容区底部预留高度 `padding-bottom: calc(120rpx + env(safe-area-inset-bottom))`
- 页面 `.js`：无 tab 切换逻辑（由系统 tabBar 处理）

### 滚动方案选择

| 方案 | 适用场景 | 注意事项 |
|------|----------|----------|
| `page` 自身滚动 | **页面主内容滚动（首选）** | 无额外配置，最稳定 |
| `scroll-view` | 局部固定高度区域滚动 | 必须设置明确 `height`，避免嵌套在 flex 容器内作为全页滚动 |
| `onPullDownRefresh` | 下拉刷新 | 页面 JSON 配 `enablePullDownRefresh: true` |

**Skyline 下 `scroll-view` 的坑**：
- `scroll-view` 嵌套在 `display: flex` 的父容器中时，`flex: 1` 无法正确计算可滚动高度
- 即使设置了 `height: 100%`，如果父容器高度不确定，也会导致无法滚动
- **结论**：页面级滚动不要用 `scroll-view`，让 `page` 自己滚

### Skyline 渲染器特性

- 是否默认 `display: flex` 取决于 `app.json` 的 `rendererOptions.skyline.defaultDisplayBlock`
- 是否默认 `box-sizing: border-box` 取决于 `rendererOptions.skyline.defaultContentBox`
- 不支持 `*` 通配符选择器
- 废弃组件/API 不可用
- 自定义组件框架：`componentFramework: "glass-easel"`

## 参考文档

按需加载对应参考文件：

| 文件 | 何时查阅 |
|------|----------|
| `references/html-to-wxml-mapping.md` | 进行标签映射时 |
| `references/css-to-wxss-mapping.md` | 转换样式、处理单位、排查不兼容属性时 |
| `references/miniprogram-layout-rules.md` | 处理导航栏、tabBar 占位、页面 JSON 配置时 |
| `references/interaction-patterns.md` | 转换按钮点击、表单、页面跳转、弹窗等交互时 |
| `references/icon-handling-guide.md` | 处理设计稿中的图标字体时（新增）