# 交互逻辑转换模式

## 事件映射总表

| HTML/JS 事件 | 小程序事件 | 说明 |
|--------------|------------|------|
| `onclick` | `bindtap` | 单击 |
| `ondblclick` | 无直接对应 | 需自行实现双击检测（记录时间戳） |
| `onmousedown` | `bindtouchstart` | 手指按下 |
| `onmouseup` | `bindtouchend` | 手指抬起 |
| `onmousemove` | `bindtouchmove` | 手指移动 |
| `onmouseenter` | 无直接对应 | 触摸设备无悬停概念 |
| `onmouseleave` | 无直接对应 | 触摸设备无悬停概念 |
| `onfocus` | `bindfocus` | 输入框聚焦 |
| `onblur` | `bindblur` | 输入框失焦 |
| `oninput` | `bindinput` | 输入中 |
| `onchange` | `bindchange` | 值改变（失焦或确认后） |
| `onsubmit` | `bindsubmit` | 表单提交 |
| `onreset` | `bindreset` | 表单重置 |
| `onscroll` | `bindscroll` | 滚动（scroll-view） |
| `onload` | `bindload` | 图片加载完成 |
| `onerror` | `binderror` | 图片加载失败 |

**注意**：`catchtap` 与 `bindtap` 的区别——`catch` 阻止事件冒泡，`bind` 允许事件冒泡。

## 点击交互

### 基础点击

```xml
<view class="btn" bindtap="onTap">点击我</view>
```

```javascript
Page({
  onTap() {
    console.log('被点击了');
  }
});
```

### 带参数点击（data-*）

```xml
<view 
  class="item" 
  wx:for="{{list}}" 
  wx:key="id"
  bindtap="onItemTap"
  data-id="{{item.id}}"
  data-name="{{item.name}}"
>
  <text>{{item.name}}</text>
</view>
```

```javascript
Page({
  onItemTap(e) {
    const { id, name } = e.currentTarget.dataset;
    console.log('点击了:', id, name);
  }
});
```

### 按钮禁用状态

```xml
<button class="submit-btn" disabled="{{isSubmitting}}" bindtap="submitForm">
  {{isSubmitting ? '提交中...' : '提交'}}
</button>
```

## 页面跳转

### 保留当前页跳转（可返回）

```javascript
wx.navigateTo({
  url: '/pages/detail/detail?id=123'
});
```

### 关闭当前页跳转（不可返回）

```javascript
wx.redirectTo({
  url: '/pages/login/login'
});
```

### 跳转到 tabBar 页面

```javascript
wx.switchTab({
  url: '/pages/index/index'
});
```

### 返回上一页

```javascript
wx.navigateBack({
  delta: 1
});
```

### navigator 组件方式

```xml
<navigator url="/pages/detail/detail?id={{item.id}}" hover-class="none">
  <view class="item">跳转到详情</view>
</navigator>

<!-- 关闭当前页跳转 -->
<navigator url="/pages/login/login" open-type="redirect" hover-class="none">
  <view>登录</view>
</navigator>

<!-- 跳转到 tabBar 页 -->
<navigator url="/pages/index/index" open-type="switchTab" hover-class="none">
  <view>回首页</view>
</navigator>
```

## 表单交互

### 输入框双向绑定

```xml
<input 
  type="text"
  placeholder="请输入姓名"
  value="{{form.name}}"
  data-field="name"
  bindinput="onInput"
/>
<input 
  type="number"
  placeholder="请输入手机号"
  value="{{form.phone}}"
  data-field="phone"
  bindinput="onInput"
/>
```

```javascript
Page({
  data: {
    form: {
      name: '',
      phone: ''
    }
  },

  onInput(e) {
    const field = e.currentTarget.dataset.field;
    const value = e.detail.value;
    this.setData({
      [`form.${field}`]: value
    });
  }
});
```

### 表单提交

```xml
<form bindsubmit="onSubmit">
  <input name="username" placeholder="用户名" />
  <input name="password" password placeholder="密码" />
  <button form-type="submit">提交</button>
</form>
```

```javascript
Page({
  onSubmit(e) {
    const formData = e.detail.value;
    console.log('表单数据:', formData);
    // { username: 'xxx', password: 'xxx' }
  }
});
```

### 单选 / 复选

```xml
<radio-group bindchange="onRadioChange" data-field="gender">
  <label wx:for="{{genderOptions}}" wx:key="value">
    <radio value="{{item.value}}" checked="{{item.checked}}" />
    <text>{{item.label}}</text>
  </label>
</radio-group>

<checkbox-group bindchange="onCheckboxChange" data-field="hobbies">
  <label wx:for="{{hobbyOptions}}" wx:key="value">
    <checkbox value="{{item.value}}" checked="{{item.checked}}" />
    <text>{{item.label}}</text>
  </label>
</checkbox-group>
```

```javascript
Page({
  onRadioChange(e) {
    const field = e.currentTarget.dataset.field;
    const value = e.detail.value;
    this.setData({ [`form.${field}`]: value });
  },

  onCheckboxChange(e) {
    const field = e.currentTarget.dataset.field;
    const values = e.detail.value; // 数组
    this.setData({ [`form.${field}`]: values });
  }
});
```

### 下拉选择（picker）

```xml
<picker bindchange="onPickerChange" value="{{pickerIndex}}" range="{{pickerArray}}">
  <view class="picker">
    当前选择：{{pickerArray[pickerIndex]}}
  </view>
</picker>
```

```javascript
Page({
  data: {
    pickerArray: ['选项一', '选项二', '选项三'],
    pickerIndex: 0
  },

  onPickerChange(e) {
    this.setData({ pickerIndex: e.detail.value });
  }
});
```

## 弹窗 / 遮罩层

### 基础弹窗

```xml
<view class="mask" wx:if="{{showModal}}" bindtap="closeModal">
  <view class="modal-content" catchtap="preventBubble">
    <text class="modal-title">提示</text>
    <text class="modal-desc">确定要执行此操作吗？</text>
    <view class="modal-actions">
      <view class="btn-cancel" bindtap="closeModal">取消</view>
      <view class="btn-confirm" bindtap="confirmAction">确定</view>
    </view>
  </view>
</view>
```

```css
.mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  width: 560rpx;
  background: #ffffff;
  border-radius: 16rpx;
  padding: 40rpx;
}
```

```javascript
Page({
  data: { showModal: false },

  openModal() { this.setData({ showModal: true }); },
  closeModal() { this.setData({ showModal: false }); },
  confirmAction() {
    this.closeModal();
    // 执行确认逻辑
  },
  preventBubble() {
    // catchtap 已阻止冒泡，无需额外代码
  }
});
```

### 底部弹出面板

```xml
<view class="mask" wx:if="{{showSheet}}" bindtap="closeSheet">
  <view class="sheet" catchtap="preventBubble">
    <!-- 底部面板内容 -->
  </view>
</view>
```

```css
.sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #ffffff;
  border-radius: 24rpx 24rpx 0 0;
  padding-bottom: env(safe-area-inset-bottom);
}
```

## 图片预览

```xml
<image 
  wx:for="{{images}}" 
  wx:key="*this"
  src="{{item}}" 
  mode="aspectFill"
  bindtap="previewImage"
  data-src="{{item}}"
/>
```

```javascript
Page({
  data: {
    images: [
      'https://example.com/1.jpg',
      'https://example.com/2.jpg'
    ]
  },

  previewImage(e) {
    const current = e.currentTarget.dataset.src;
    wx.previewImage({
      current,
      urls: this.data.images
    });
  }
});
```

## 列表加载更多 / 下拉刷新

### 下拉刷新

页面 JSON：
```json
{ "enablePullDownRefresh": true }
```

```javascript
Page({
  onPullDownRefresh() {
    // 刷新数据
    this.loadData().finally(() => {
      wx.stopPullDownRefresh();
    });
  }
});
```

### 上拉加载更多

页面 JSON：
```json
{ "onReachBottomDistance": 100 }
```

```javascript
Page({
  data: { page: 1, list: [], hasMore: true },

  onReachBottom() {
    if (!this.data.hasMore) return;
    this.loadMore();
  },

  async loadMore() {
    const { page, list } = this.data;
    const res = await fetchList(page + 1);
    this.setData({
      page: page + 1,
      list: [...list, ...res.data],
      hasMore: res.data.length > 0
    });
  }
});
```

### scroll-view 实现

```xml
<scroll-view 
  scroll-y 
  style="height: 100vh;"
  refresher-enabled="{{true}}"
  refresher-triggered="{{isRefreshing}}"
  bindrefresherrefresh="onRefresh"
  bindscrolltolower="onLoadMore"
>
  <view wx:for="{{list}}" wx:key="id">{{item.name}}</view>
  <view wx:if="{{!hasMore}}" class="no-more">没有更多了</view>
</scroll-view>
```

## 轮播图

```xml
<swiper 
  class="banner-swiper" 
  indicator-dots="{{true}}" 
  autoplay="{{true}}" 
  interval="3000"
  circular="{{true}}"
>
  <swiper-item wx:for="{{banners}}" wx:key="id">
    <image src="{{item.imageUrl}}" mode="aspectFill" class="banner-img" />
  </swiper-item>
</swiper>
```

```css
.banner-swiper {
  height: 400rpx;
}

.banner-img {
  width: 100%;
  height: 100%;
}
```

## 网络请求封装

```javascript
// 基础请求
wx.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  header: { 'Authorization': 'Bearer ' + token },
  success: (res) => {
    if (res.statusCode === 200) {
      this.setData({ list: res.data });
    }
  },
  fail: (err) => {
    wx.showToast({ title: '请求失败', icon: 'none' });
  }
});

// 使用 Promise 封装
function request(options) {
  return new Promise((resolve, reject) => {
    wx.request({
      ...options,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(res);
        }
      },
      fail: reject
    });
  });
}
```
