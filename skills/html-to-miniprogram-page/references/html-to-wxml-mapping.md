# HTML 到 WXML 标签映射

## 基础标签映射

| HTML | WXML | 说明 |
|------|------|------|
| `<div>` | `<view>` | 通用块级容器 |
| `<span>` | `<text>` | 行内文本；若不需要 text 特殊能力也可用 `<view>` |
| `<p>` | `<view>` | 段落 |
| `<h1>` ~ `<h6>` | `<view>` | 标题，配合 class 设置样式 |
| `<img>` | `<image>` | 图片，必须写闭合标签或自闭合 |
| `<a href="...">` | `<navigator url="...">` | 页面跳转；若是执行操作而非跳转，用 `<view bindtap="...">` |
| `<button>` | `<button>` | 按钮，注意覆盖小程序默认按钮样式 |
| `<input>` | `<input>` | 输入框，属性映射见下方 |
| `<textarea>` | `<textarea>` | 多行输入 |
| `<form>` | `<form>` | 表单，事件用 `bindsubmit` / `bindreset` |
| `<label>` | `<label>` | 标签，可提升表单可点击区域 |
| `<ul>` / `<ol>` | `<view>` | 列表容器 |
| `<li>` | `<view>` | 列表项 |
| `<table>` | `<view>` | 表格建议用 flex / grid 布局模拟 |
| `<tr>` | `<view>` | 表格行 |
| `<td>` / `<th>` | `<view>` | 单元格 |
| `<section>` | `<view>` | 区块 |
| `<header>` | `<view>` | 头部区域 |
| `<footer>` | `<view>` | 底部区域 |
| `<article>` | `<view>` | 文章区域 |
| `<nav>` | `<view>` | 导航区域 |
| `<main>` | `<view>` | 主体区域 |
| `<aside>` | `<view>` | 侧边栏 |
| `<br>` | — | 用 margin/padding 或换行文本处理，WXML 无 `<br>` |
| `<hr>` | `<view>` | 用带边框的 `<view>` 模拟 |
| `<iframe>` | `<web-view>` | 仅全屏页面可用，限制较多 |

## 属性映射

| HTML 属性 | WXML 属性 | 示例 |
|-----------|-----------|------|
| `class` | `class` | `<view class="container">` |
| `id` | `id` | `<view id="header">` |
| `style` | `style` | `<view style="color: red;">` |
| `src` | `src` | `<image src="/images/logo.png" />` |
| `alt` | — | 图片无 alt，可用 title 或旁白文字替代 |
| `placeholder` | `placeholder` | `<input placeholder="请输入" />` |
| `value` | `value` | `<input value="{{inputValue}}" />` |
| `name` | `name` | `<input name="username" />` |
| `type` | `type` | `<input type="text" />`（取值有差异）|
| `disabled` | `disabled` | `<button disabled="{{isDisabled}}">` |
| `checked` | `checked` | `<checkbox checked="{{isChecked}}">` |
| `selected` | — | 下拉框用 `<picker>` |
| `data-*` | `data-*` | `<view data-id="{{item.id}}">` |

## input 类型差异

| HTML type | 小程序 input type | 说明 |
|-----------|-------------------|------|
| `text` | `text` | 文本 |
| `password` | — | 用 `password="{{true}}"` 属性 |
| `number` | `number` | 数字键盘 |
| `tel` | — | 用 `type="number"` 或自定义 |
| `email` | `text` | 小程序无专门 email 类型 |
| `search` | `text` | 可配合 `confirm-type="search"` |
| `date` | — | 用 `<picker mode="date">` |

## 条件与列表渲染

```xml
<!-- 条件渲染 -->
<view wx:if="{{condition}}">显示内容</view>
<view wx:elif="{{otherCondition}}">其他内容</view>
<view wx:else>默认内容</view>

<!-- 列表渲染 -->
<view wx:for="{{list}}" wx:key="id" wx:for-item="item" wx:for-index="idx">
  <text>{{idx}}: {{item.name}}</text>
</view>

<!-- 多节点条件 -->
<block wx:if="{{showLoading}}">
  <view class="loading-icon"></view>
  <text>加载中...</text>
</block>
```

## 文本嵌套规则

- 简单文本可直接放在 `<view>` 中
- 需要局部样式变化或可选中时，用 `<text>` 包裹
- `<text>` 内部可嵌套 `<text>` 实现局部样式

```xml
<view>
  <text>普通文本</text>
  <text class="highlight">高亮文本</text>
</view>
```
