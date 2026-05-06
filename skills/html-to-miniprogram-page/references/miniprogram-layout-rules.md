# 小程序布局与导航栏规则

## 页面文件组成

一个小程序页面由四个文件组成：

| 文件 | 必需 | 说明 |
|------|------|------|
| `.js` | 是 | 页面逻辑 |
| `.wxml` | 是 | 页面结构 |
| `.wxss` | 否 | 页面样式（不写则继承全局） |
| `.json` | 否 | 页面配置（不写则继承 app.json 的 window 配置） |

## 页面 JSON 配置

```json
{
  "navigationBarTitleText": "页面标题",
  "navigationBarTextStyle": "black",
  "navigationBarBackgroundColor": "#ffffff",
  "navigationStyle": "default",
  "backgroundColor": "#f5f5f5",
  "backgroundTextStyle": "dark",
  "enablePullDownRefresh": false,
  "onReachBottomDistance": 50,
  "usingComponents": {},
  "renderer": "skyline"
}
```

### 关键字段

| 字段 | 取值 | 说明 |
|------|------|------|
| `navigationStyle` | `default` / `custom` | 默认使用系统导航栏；custom 完全自定义 |
| `navigationBarTitleText` | 字符串 | 系统导航栏标题，custom 模式下无效 |
| `navigationBarTextStyle` | `black` / `white` | 系统导航栏标题颜色 |
| `navigationBarBackgroundColor` | HexColor | 系统导航栏背景色 |
| `renderer` | `skyline` | 声明使用 Skyline 渲染器 |

## 导航栏模式详解

### 模式一：系统默认导航栏（最常用）

```json
{
  "navigationBarTitleText": "首页",
  "navigationBarTextStyle": "black",
  "navigationBarBackgroundColor": "#ffffff",
  "navigationStyle": "default",
  "renderer": "skyline"
}
```

**WXML 特点**：
- **不写任何导航栏代码**
- 页面内容自动从导航栏下方开始
- 导航栏高度由系统决定（状态栏 + 胶囊按钮区域，约 64~88px 不等）

### 模式二：完全自定义导航栏

当设计稿顶部有特殊样式（渐变色、搜索框嵌入标题栏、透明背景等）时使用。

```json
{
  "navigationStyle": "custom",
  "renderer": "skyline"
}
```

**JS 中获取导航栏高度**：

```javascript
Page({
  data: {
    statusBarHeight: 0,   // 状态栏高度（电量、时间那一行）
    navBarHeight: 44,     // 导航栏区域高度（标题+胶囊）
    totalNavHeight: 0     // 总高度
  },

  onLoad() {
    const sysInfo = wx.getSystemInfoSync();
    const menuInfo = wx.getMenuButtonBoundingClientRect();

    // 计算导航栏高度（胶囊按钮区域）
    const navBarHeight = (menuInfo.top - sysInfo.statusBarHeight) * 2 + menuInfo.height;

    this.setData({
      statusBarHeight: sysInfo.statusBarHeight,
      navBarHeight: navBarHeight,
      totalNavHeight: sysInfo.statusBarHeight + navBarHeight
    });
  }
});
```

**WXML 结构**：

```xml
<view class="page">
  <!-- 自定义导航栏 -->
  <view class="custom-nav" style="padding-top: {{statusBarHeight}}px; height: {{navBarHeight}}px;">
    <view class="nav-back" bindtap="goBack">
      <image src="/images/back.png" class="back-icon" />
    </view>
    <text class="nav-title">页面标题</text>
  </view>

  <!-- 页面内容，顶部增加 totalNavHeight 的 padding 或 margin -->
  <view class="page-content" style="padding-top: {{totalNavHeight}}px;">
    <!-- 原设计稿内容 -->
  </view>
</view>
```

**WXSS**：

```css
.custom-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.nav-back {
  position: absolute;
  left: 20rpx;
  display: flex;
  align-items: center;
}

.back-icon {
  width: 40rpx;
  height: 40rpx;
}

.nav-title {
  font-size: 34rpx;
  font-weight: 500;
  color: #ffffff;
}

.page-content {
  min-height: 100vh;
  background-color: #f5f5f5;
}
```

## TabBar 占位规则

### app.json 配置示例

```json
{
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#333333",
    "backgroundColor": "#ffffff",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "images/tab-home.png",
        "selectedIconPath": "images/tab-home-active.png"
      },
      {
        "pagePath": "pages/profile/profile",
        "text": "我的",
        "iconPath": "images/tab-profile.png",
        "selectedIconPath": "images/tab-profile-active.png"
      }
    ]
  }
}
```

### 页面级处理

**TabBar 页面底部预留**：

```css
.page-container {
  min-height: 100vh;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
  background-color: #f5f5f5;
}
```

**固定底部按钮处理**：

```xml
<view class="page">
  <view class="content">
    <!-- 页面内容 -->
  </view>

  <!-- 固定底部操作栏（非 tabBar） -->
  <view class="bottom-bar" style="padding-bottom: {{safeAreaBottom}}px;">
    <button class="submit-btn">提交</button>
  </view>
</view>
```

```css
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20rpx 30rpx;
  background: #ffffff;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
}

/* 如果页面有 tabBar，固定底部栏要在 tabBar 之上 */
.has-tabbar .bottom-bar {
  bottom: calc(120rpx + env(safe-area-inset-bottom));
}
```

## 页面根结构模板

### 有系统导航栏 + 无 tabBar

```xml
<view class="page">
  <view class="page-content">
    <!-- 内容区域 -->
  </view>
</view>
```

```css
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}
```

### 有系统导航栏 + 有 tabBar

```xml
<view class="page">
  <view class="page-content">
    <!-- 内容区域 -->
  </view>
</view>
```

```css
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.page-content {
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}
```

### 自定义导航栏 + 无 tabBar

```xml
<view class="page">
  <view class="custom-nav" style="padding-top: {{statusBarHeight}}px; height: {{navBarHeight}}px;">
    <text class="nav-title">标题</text>
  </view>
  <view class="page-content" style="padding-top: {{totalNavHeight}}px;">
    <!-- 内容区域 -->
  </view>
</view>
```

```css
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.custom-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
}
```

## 安全区适配

### 顶部安全区
自定义导航栏已通过 `statusBarHeight` 处理。

### 底部安全区

```css
.safe-bottom {
  padding-bottom: constant(safe-area-inset-bottom); /* iOS 11.0 */
  padding-bottom: env(safe-area-inset-bottom);       /* iOS 11.2+ */
}
```

JS 中动态获取：

```javascript
onLoad() {
  const sysInfo = wx.getSystemInfoSync();
  this.setData({
    safeAreaBottom: sysInfo.screenHeight - sysInfo.safeArea.bottom
  });
}
```
