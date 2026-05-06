# 数据源模式：真实 API vs Mock

两种模式各有代价，根据用户的选择落到 spec 里。

## 模式 A：真实 API

**适用**：要验证后端行为（筛选语义、权限、字段映射、排序），本地环境就绪。

**前置**：
- 后端服务已起（本项目 8188）
- 数据库/Redis 已就绪
- 有种子数据（至少 1 条列表数据，否则筛选语义用例全部 skip）

**登录态准备**：沿用 `e2e/global-setup.ts` — captcha + redis-cli + `/auth/login` + 写 localStorage。

**spec 直接调用 API 验证**（绕过 UI 时间选择器等复杂控件）：

```typescript
const result = await page.evaluate(async (u) => {
  const token = localStorage.getItem('token')
  const res = await fetch(u, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  return { status: res.status, body: await res.json() }
}, '/api/admin/customers?tagIds=__nonexistent__')
```

**副作用**：默认只开弹窗不提交。必须提交的用例（如"新增后列表出现"），在测试末尾加清理：
```typescript
test.afterEach(async ({ page }) => {
  // 删除测试创建的数据
})
```

## 模式 B：Mock 数据

**适用**：CI、离线、只测前端渲染/交互、后端未就绪。

**整个 describe 注入拦截**：

```typescript
test.describe('客户列表（Mock 模式）', () => {
  test.beforeEach(async ({ page }) => {
    // 列表
    await page.route(/\/api\/admin\/customers(\?|$)/, (route) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          code: 200,
          data: {
            list: [
              { id: 1, contactName: '张三', phone: '13800000001', status: 1, tags: ['意向高'] },
              { id: 2, contactName: '李四', phone: '13800000002', status: 2, tags: ['VIP客户'] },
            ],
            total: 2,
            page: 1,
            pageSize: 20,
          },
        }),
      })
    })
    // 字典
    await page.route(/\/api\/admin\/dict\/options/, (route) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ code: 200, data: [{ label: '意向高', value: '1' }] }),
      })
    })
    await page.goto('/customer/list')
  })

  test('渲染表格', async ({ page }) => {
    await expect(page.getByText('张三')).toBeVisible()
    await expect(page.getByText('李四')).toBeVisible()
  })
})
```

**按参数返回不同 fixture**：

```typescript
await page.route(/\/api\/admin\/customers/, (route) => {
  const url = new URL(route.request().url())
  const hasKeyword = url.searchParams.get('keyword')
  const list = hasKeyword
    ? [{ id: 1, contactName: '张三' }]  // 搜索命中
    : [{ id: 1, contactName: '张三' }, { id: 2, contactName: '李四' }]  // 全量
  route.fulfill({
    status: 200,
    body: JSON.stringify({ code: 200, data: { list, total: list.length } }),
  })
})
```

**登录 Mock**：跳过 captcha，直接在 storageState 里写死 token；或在 globalSetup 里把后端登录换成 Mock。

**缺点**：
- 测不到后端 bug（如本项目 `CustomerService.java:59` 的筛选失效）
- Mock 数据格式跟真接口漂移会掩盖契约问题

## 模式 C：混合

- 列表/字典/详情等**只读接口** → Mock 固定返回（稳定、快）
- 新增/编辑/删除等**写接口** → 用真实 API 打开弹窗但不点确认（避免污染）
- 导出 → Mock 返回 200 即可

这是 CI 环境的推荐选择。

## 选择建议

| 场景 | 推荐模式 |
|------|---------|
| 本地验证新功能 / 抓后端 bug | A 真实 API |
| CI 流水线 | C 混合（或 B 全 Mock） |
| 前端重构回归 | B Mock（固化契约） |
| 联调期 | A 真实 API |
