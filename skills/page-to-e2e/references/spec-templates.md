# Spec 代码模板

按功能分组的 Playwright 代码片段。生成 spec 时直接拷贝改造。

## 跨项目使用：先替换占位

下面的代码片段用的是 area-rent 的具体值。在别的项目使用时，必须按 [`references/project-profile.md`](./project-profile.md) （首次运行时勘探生成）替换以下部分：

| 占位 | area-rent 实际值 | 换项目时替换为 |
|------|---------------|---------------|
| 页面路由 `/customer/list` | `/customer/list` | 实际路由 |
| API 路径 `/api/admin/customers` | `/api/admin/customers` | `api_path_prefix` + 业务名 |
| UI 库 class `.el-xxx` | Element Plus | Ant Design 用 `.ant-xxx`；Naive 用 `.n-xxx`；尽量用 `getByRole` |
| 分页文案 `50/page` | 英文 locale | 中文 locale 改 `50 条/页` |
| 中文按钮文案【查询/新增/导出】| 本项目用中文 | 全英文界面改英文 |
| Token 键 `localStorage.getItem('token')` | 该项目用 `token` | 按项目的 `token_storage` |
| 响应体结构 `body.data.{list,total}` | 该项目的 `list_response_shape` | 按实际 shape |
| 导出正则 `/api/admin/customers/export` | `export_api_pattern` | 按实际 |

约定：代码片段里不再用 `{{占位}}` 语法（代码会编译报错），而是写上 area-rent 的实际值作为样本，Agent 在生成 spec 时按上表映射替换。

## 文件骨架

```typescript
import { test, expect, Page } from '@playwright/test'

const PAGE_URL = '/customer/list'
const LIST_API = /\/api\/admin\/customers(\?|$)/

async function gotoPage(page: Page) {
  await page.goto(PAGE_URL)
  await page.waitForResponse(
    (r) => LIST_API.test(r.url()) && r.status() === 200,
    { timeout: 10_000 },
  )
}

test.describe('页面 /xxx', () => {
  test.beforeEach(async ({ page }) => {
    await gotoPage(page)
  })

  // 用例...
})
```

## 渲染类

```typescript
test('页面标题和核心按钮渲染', async ({ page }) => {
  await expect(page).toHaveURL(/\/customer\/list/)
  await expect(page.getByPlaceholder('名称/公司/手机号')).toBeVisible()
  await expect(page.getByRole('button', { name: '查询' })).toBeVisible()
  await expect(page.getByRole('button', { name: '新增' })).toBeVisible()
})

test('筛选表单包含全部 label', async ({ page }) => {
  const filter = page.locator('.filter-form')
  for (const label of ['关键词', '类型', '状态', '创建时间']) {
    await expect(filter.getByText(label, { exact: true }).first()).toBeVisible()
  }
})

test('表格列头齐全', async ({ page }) => {
  const table = page.locator('.el-table').first()
  for (const col of ['序号', '联系人', '电话', '状态', '操作']) {
    await expect(table.locator('thead').getByText(col, { exact: true })).toBeVisible()
  }
})
```

## 筛选类（入参 + 语义双重校验）

```typescript
// 入参下发
test('关键词搜索下发 keyword 参数', async ({ page }) => {
  const reqPromise = page.waitForRequest(
    (r) => LIST_API.test(r.url()) && r.url().includes('keyword='),
  )
  await page.getByPlaceholder('名称/公司/手机号').fill('测试')
  await page.getByRole('button', { name: '查询' }).click()
  const req = await reqPromise
  expect(decodeURIComponent(req.url())).toContain('keyword=测试')
})

// 下拉单选
test('来源筛选下发 source 参数', async ({ page }) => {
  const item = page.locator('.el-form-item', { hasText: '来源' }).first()
  await item.locator('.el-select').first().click()
  await page.getByRole('option', { name: '线下拜访', exact: true }).click()
  const reqPromise = page.waitForRequest(
    (r) => LIST_API.test(r.url()) && r.url().includes('source='),
  )
  await page.getByRole('button', { name: '查询' }).click()
  await reqPromise
})

// 多选
test('标签多选下发逗号分隔 tagIds', async ({ page }) => {
  const item = page.locator('.el-form-item', { hasText: '标签' }).first()
  await item.locator('.el-select').first().click()
  await page.getByRole('option', { name: '意向高', exact: true }).click()
  await page.getByRole('option', { name: 'VIP客户', exact: true }).click()
  await page.keyboard.press('Escape')
  const reqPromise = page.waitForRequest(
    (r) => LIST_API.test(r.url()) && r.url().includes('tagIds='),
  )
  await page.getByRole('button', { name: '查询' }).click()
  const req = await reqPromise
  expect(decodeURIComponent(req.url())).toMatch(/tagIds=[^&]*意向高/)
})
```

## 过滤语义校验（必须有！）

只验证入参会漏 bug（如顶层 `.or()` 打断 AND 链）。用不匹配值直接发 API 验证 total：

```typescript
test.describe('过滤在后端真的生效', () => {
  async function apiList(page: Page, params: Record<string, string | number> = {}) {
    await page.goto(PAGE_URL, { waitUntil: 'domcontentloaded' })
    const query = new URLSearchParams(
      Object.entries(params).map(([k, v]) => [k, String(v)]),
    ).toString()
    const result = await page.evaluate(async (u) => {
      const token = localStorage.getItem('token')
      const res = await fetch(u, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      })
      return { status: res.status, body: await res.json() }
    }, `/api/admin/customers${query ? '?' + query : ''}`)
    expect(result.status).toBe(200)
    return result.body.data as { list: any[]; total: number }
  }

  test('时间范围过滤：历史空区间 total=0', async ({ page }) => {
    const baseline = await apiList(page, { page: 1, pageSize: 10 })
    test.skip(baseline.total === 0, '库无数据，无法验证')
    const filtered = await apiList(page, {
      startDate: '2000-01-01',
      endDate: '2000-01-02',
    })
    expect(filtered.total).toBe(0)
  })

  test('标签过滤：不存在值 total=0', async ({ page }) => {
    const filtered = await apiList(page, { tagIds: '__nonexistent__' })
    expect(filtered.total).toBe(0)
  })
})
```

## 分页

```typescript
test('切换每页条数重新请求并带 pageSize', async ({ page }) => {
  await page.locator('.el-pagination .el-select').first().click()
  const reqPromise = page.waitForRequest(
    (r) => LIST_API.test(r.url()) && /pageSize=50/.test(r.url()),
  )
  // 项目未配中文 locale 就用英文
  await page.getByRole('option', { name: '50/page', exact: true }).click()
  await reqPromise
})
```

## 行操作（只开弹窗不提交）

```typescript
test('详情弹窗渲染扩展字段', async ({ page }) => {
  const rows = page.locator('.el-table__body-wrapper tbody tr')
  test.skip((await rows.count()) === 0, '列表无数据')
  await rows.first().getByRole('button', { name: '详情' }).click()
  const dialog = page.locator('.el-dialog', { hasText: '客户详情' })
  await expect(dialog).toBeVisible()
  for (const label of ['联系人', '电话', '企业名称']) {
    await expect(dialog.getByText(label, { exact: true }).first()).toBeVisible()
  }
  await page.keyboard.press('Escape')
  await expect(dialog).toBeHidden()
})

test('删除确认框点取消不实际执行', async ({ page }) => {
  const btns = page.locator('tbody tr button', { hasText: '删除' })
  test.skip((await btns.count()) === 0, '无可删数据')
  await btns.first().click()
  const confirm = page.locator('.el-message-box')
  await expect(confirm).toBeVisible()
  await confirm.getByRole('button', { name: '取消' }).click()
  await expect(confirm).toBeHidden()
})
```

## 跳转

```typescript
test('新增按钮跳转表单页', async ({ page }) => {
  await page.getByRole('button', { name: '新增' }).click()
  await expect(page).toHaveURL(/\/customer\/form/)
})
```

## 导出/下载

```typescript
test('导出按钮触发导出接口', async ({ page }) => {
  // ⚠️ blob + a.click 不一定触发 Playwright download 事件，改监听响应
  const respPromise = page.waitForResponse(
    (r) => /\/api\/admin\/customers\/export/.test(r.url()) && r.status() === 200,
    { timeout: 15_000 },
  )
  await page.getByRole('button', { name: '导出' }).click()
  const resp = await respPromise
  expect(resp.ok()).toBeTruthy()
})
```
