# CSS 到 WXSS 转换规则

## 单位转换

以设计稿宽度 **750px** 为基准：

| 原单位 | 目标单位 | 转换方式 | 示例 |
|--------|----------|----------|------|
| `px` | `rpx` | 1:1（750px 设计稿下） | `16px` → `16rpx` |
| `rem` | `rpx` | 根字体大小 × rem 值 | `1rem`（根 16px）→ `16rpx` |
| `em` | `rpx` | 当前字体大小 × em 值 | `1.5em`（当前 16px）→ `24rpx` |
| `vw` | `rpx` | `100vw = 750rpx`，按比例换算 | `50vw` → `375rpx` |
| `vh` | `rpx` 或 `%` | 视口高度，视场景转换 | `100vh` → 页面高度用 `100%` |
| `%` | `%` | 百分比保留 | `width: 100%` 保留 |

**注意**：如果设计稿不是 750px 宽，按比例换算。例如 375px 设计稿：`1px = 2rpx`。

## 选择器兼容性

| CSS 选择器 | WXSS 支持 | 处理建议 |
|------------|-----------|----------|
| `*` | ❌ Skyline 不支持 | **禁止使用**，逐个元素设置基础样式 |
| `element` | ✅ 支持 | 可用，但建议优先用 class |
| `.class` | ✅ 支持 | 主力选择器 |
| `#id` | ✅ 支持 | 可用，但小程序中不推荐使用 id 选择器 |
| `[attr]` / `[attr=value]` | ⚠️ 有限支持 | 尽量避免，用 class 替代 |
| `A, B` 分组 | ✅ 支持 | 保留 |
| `A B` 后代 | ✅ 支持 | 保留，但嵌套不宜超过 3 层 |
| `A > B` 子代 | ✅ 支持 | 保留 |
| `A + B` 相邻兄弟 | ✅ 支持 | 保留 |
| `A ~ B` 通用兄弟 | ⚠️ 有限 | 尽量避免 |
| `::before` / `::after` | ✅ 支持 | 保留，`content` 必须写 |
| `:active` | ✅ 支持 | 保留 |
| `:hover` | ❌ 不支持 | 用 `hover-class` 属性替代 |
| `:focus` | ⚠️ 有限 | 输入框聚焦用 `focus` 属性事件 |
| `:first-child` / `:last-child` | ⚠️ 有限 | 尽量避免，用 class 或 wx:if 控制 |
| `:nth-child(n)` | ⚠️ 有限 | 尽量避免 |

## 属性兼容性

### 完全支持的属性（直接保留）

- `width`, `height`, `min-width`, `min-height`, `max-width`, `max-height`
- `margin`, `padding`, `border`
- `display`（`flex`, `block`, `inline`, `none`, `inline-block`）
- `position`（`relative`, `absolute`, `sticky`）
- `top`, `right`, `bottom`, `left`
- `z-index`
- `background`, `background-color`, `background-image`（网络图）, `background-size`, `background-position`, `background-repeat`
- `color`, `font-size`, `font-weight`, `font-family`, `line-height`, `text-align`, `text-decoration`
- `border-radius`, `box-shadow`
- `opacity`, `visibility`
- `overflow`, `overflow-x`, `overflow-y`
- `transform`, `transition`, `animation`, `@keyframes`
- `white-space`, `word-break`, `word-wrap`
- `flex`, `flex-direction`, `justify-content`, `align-items`, `align-self`, `flex-wrap`, `flex-shrink`, `flex-grow`, `order`
- `gap`, `row-gap`, `column-gap`

### 不支持的属性（必须移除或替代）

| CSS 属性 | 替代方案 |
|----------|----------|
| `position: fixed` | 优先用 `position: sticky` 或调整页面结构；Skyline 下 fixed 表现与 WebView 差异大 |
| `cursor` | 移除，触摸设备无鼠标指针 |
| `user-select` | 用 `<text selectable>` 替代 |
| `outline` | 移除，或用 border 模拟 |
| `resize` | 移除，小程序元素不可拖拽调整大小 |
| `float` | 用 flex 布局替代 |
| `clear` | 用 flex 布局替代 |
| `vertical-align` | 用 flex `align-items: center` 替代 |
| `table-layout` | 用 flex/grid 模拟表格 |
| `list-style` | 用自定义样式实现 |
| `@import`（CSS 的） | 用 WXSS 的 `@import`（路径为相对路径） |
| `@media print` | 移除 |

### Skyline 布局特性优化

Skyline 渲染器下以下默认值已生效，**无需重复声明**：

```css
/* 以下可删除，因为 Skyline 默认就是 */
display: flex;
box-sizing: border-box;
```

## 字体处理

```css
/* 推荐系统字体栈 */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* 避免使用自定义字体文件，如需使用： */
/* @font-face 支持但加载性能差，建议用网络图片替代特殊字体场景 */
```

## 滚动容器

```css
/* 垂直滚动 */
.scroll-container {
  height: 100%;
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
}
```

更推荐用 `<scroll-view>` 组件：

```xml
<scroll-view scroll-y class="scroll-container">
  <!-- 内容 -->
</scroll-view>
```

## 安全区适配

```css
/* iPhone X+ 底部安全区 */
.safe-area-bottom {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}

/* 顶部状态栏高度由 JS 动态获取注入 style */
```
