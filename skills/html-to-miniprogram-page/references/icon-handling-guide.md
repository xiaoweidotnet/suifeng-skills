# 图标处理指南

## 问题背景

HTML 设计稿中常用的图标字体（如 Google Material Symbols、FontAwesome、Iconfont 等）无法在小程序中直接使用：
- 小程序不支持加载外部 CSS/字体文件
- `@font-face` 引入本地字体文件会增加包体积（小程序限制 2MB）
- 字体加载有性能开销，且部分低端机型渲染效果不稳定

## 处理方案

### 方案一：CSS 绘制（优先用于简单图标）

适用于几何形状简单的图标：箭头、放大镜、方块、圆点、铃铛、房子等。

**优点**：零额外资源、矢量清晰、颜色可控
**缺点**：复杂图标难以绘制、维护成本高

```css
/* 示例：放大镜图标 */
.icon-search {
  width: 32rpx;
  height: 32rpx;
  position: relative;
}
.icon-search::before {
  content: '';
  position: absolute;
  width: 18rpx;
  height: 18rpx;
  border: 4rpx solid #727785;
  border-radius: 50%;
}
.icon-search::after {
  content: '';
  position: absolute;
  width: 4rpx;
  height: 14rpx;
  background-color: #727785;
  bottom: 0;
  right: 4rpx;
  transform: rotate(-45deg);
}
```

**适合 CSS 绘制的图标类型**：
- 基础形状：圆点、方块、线条、三角形
- 方向箭头：上/下/左/右、双箭头
- 简单符号：放大镜、加号、减号、叉号
- 基础轮廓：房子、铃铛、人形（简化版）

**不适合 CSS 绘制的图标**：
- 复杂曲线：齿轮、云朵、闪电
- 品牌 Logo
- 需要多色渐变的图标
- 细节丰富的图标（如汽车、动物）

---

### 方案二：本地图片（优先用于复杂图标）

将图标导出为 PNG/SVG，放入小程序 `images/` 目录。

**优点**：100% 还原设计稿、支持复杂图形
**缺点**：增加包体积、需要管理多套尺寸

**图片规格要求**：

| 用途 | 建议尺寸 | 格式 | 备注 |
|------|----------|------|------|
| 页面内图标 | 32×32 ~ 48×48 px | PNG | 透明背景 |
| tabBar 图标 | 81×81 px | PNG | 微信官方建议尺寸 |
| 大图标/插图 | 按实际使用尺寸 | PNG/SVG | SVG 需确认 Skyline 支持 |

**tabBar 图标特别说明**：
- 必须提供 **正常态** 和 **选中态** 两套图标
- 单张图标大小不超过 40KB
- 不支持 GIF
- 颜色建议：正常态用灰色系，选中态用品牌主色

---

### 方案三：iconfont（适用于大量图标）

在 [iconfont.cn](https://www.iconfont.cn) 创建项目，统一管理和使用图标。

**优点**：图标丰富、可在线管理、支持多色
**缺点**：需要额外配置、首次加载有延迟

**使用步骤**：
1. 在 iconfont.cn 创建项目
2. 搜索并添加需要的图标
3. 下载字体文件（推荐 Symbol 方式）
4. 将字体文件放入小程序项目中
5. 使用 `text` 组件 + 字体类名引用

```css
/* app.wxss 全局引入 */
@font-face {
  font-family: 'iconfont';
  src: url('/fonts/iconfont.woff2') format('woff2');
}
.iconfont {
  font-family: "iconfont";
}
```

```xml
<!-- 页面中使用 -->
<text class="iconfont">&#xe6a8;</text>
```

---

### 方案四：微信小程序内置 icon（兜底方案）

使用微信内置的 `icon` 组件，但类型非常有限：

```xml
<icon type="success" size="20" color="#005bbf"/>
```

支持的 `type`：`success`, `success_no_circle`, `info`, `warn`, `waiting`, `cancel`, `download`, `search`, `clear`

**一般不推荐**，因为样式和设计稿差异大。

---

## 决策流程

```
设计稿中的图标
    │
    ├─ 是 tabBar 图标？
    │     ├─ 是 → 导出为 PNG（81×81，正常态+选中态）
    │     └─ 否 → 继续判断
    │
    ├─ 是简单几何形状（箭头、方块、线条等）？
    │     ├─ 是 → CSS 绘制
    │     └─ 否 → 继续判断
    │
    ├─ 页面内图标数量 > 10 个？
    │     ├─ 是 → 考虑 iconfont 方案
    │     └─ 否 → 导出为 PNG 图片
    │
    └─ 是品牌 Logo 或复杂插图？
          └─ 是 → 导出为 PNG/SVG
```

## 常见图标字体映射

| 原字体 | 处理方式 | 说明 |
|--------|----------|------|
| Google Material Symbols | CSS 绘制 或 导出图片 | 图标名称可搜索，但无法直接引用 |
| Google Material Icons | CSS 绘制 或 导出图片 | 同上 |
| FontAwesome | iconfont 或 导出图片 | 可在 iconfont.cn 搜索对应图标 |
| 自定义 Iconfont | 下载字体文件引入 | 如果是团队自有图标库 |
| Emoji / Unicode 符号 | 直接用 text 显示 | 简单场景可用，但样式不可控 |

## 质量检查清单

- [ ] 设计稿中的所有图标都已处理，没有字体图标残留
- [ ] tabBar 图标有正常态和选中态两套
- [ ] 图标颜色与设计稿一致
- [ ] 图标在不同分辨率下显示清晰（无锯齿、不模糊）
- [ ] 图标资源已放入正确的目录（如 `images/icons/`、`images/tabbar/`）
- [ ] 图片资源总大小未超出小程序包体积限制
