# 语义陷阱与反模式

这些坑会让测试"看起来全绿"但 bug 照样线上翻车。生成 spec 时主动规避。

## 陷阱 1：筛选假阳性

**症状**：点完"查询"收到 200 响应，测试就过了。

**问题**：只验证了请求发出去、URL 带了参数，没验证返回的数据**真的被过滤**。如果后端筛选语义坏了（比如本项目 `CustomerService.list` 顶层 `.or()` 打断 AND 链导致所有筛选都返回全量），测试照样全绿。

**正确做法**：任何筛选项至少一组用**不匹配值**的语义用例：

```typescript
test('时间范围过滤真的生效', async ({ page }) => {
  const baseline = await apiList(page, {})
  test.skip(baseline.total === 0, '库无数据')

  const filtered = await apiList(page, {
    startDate: '2000-01-01',
    endDate: '2000-01-02',
  })
  // 关键：total 必须为 0，否则筛选等于没做
  expect(filtered.total).toBe(0)
  expect(filtered.list.length).toBe(0)
})
```

## 陷阱 2：副作用真实提交污染数据

**症状**：CI 跑几轮后数据库里多出几百条 `自动化测试客户_20260501_xxx`。

**正确做法**：
- 默认副作用操作**只点到弹窗打开**，然后点"取消"关闭，断言已关闭
- 必须提交的用例放在独立 describe，用 Mock 模式或 `afterEach` 清理

## 陷阱 3：Element Plus teleport 多实例

**症状**：`.el-select-dropdown` 选不到或选到旧实例（`nth=0` 是上次关掉的）。

```typescript
// ❌ bad
await page.locator('.el-select-dropdown .el-select-dropdown__item', { hasText: '意向高' }).click()

// ✅ good
await page.getByRole('option', { name: '意向高', exact: true }).click()
```

## 陷阱 4：Element Plus locale 英文默认

项目没显式配 `ElConfigProvider` + `zhCn` 时，分页渲染成 `20/page` 而非 `20/页`。

```typescript
// ❌ 假设中文
await page.getByText('50/页').click()

// ✅ 就按实际看到的
await page.getByRole('option', { name: '50/page', exact: true }).click()
```

## 陷阱 5：blob 下载不触发 download 事件

前端 `URL.createObjectURL(blob) + a.click()` 的下载方式，Playwright 的 `page.waitForEvent('download')` 会超时。

```typescript
// ❌ 超时
const downloadPromise = page.waitForEvent('download')
await page.getByRole('button', { name: '导出' }).click()
await downloadPromise

// ✅ 监听响应
const respPromise = page.waitForResponse(
  (r) => /\/api\/admin\/.+\/export/.test(r.url()) && r.status() === 200,
)
await page.getByRole('button', { name: '导出' }).click()
await respPromise
```

## 陷阱 6：waitForTimeout 掩盖 flaky

```typescript
// ❌ 脆弱，4s 在慢机器上不够，快机器上浪费
await page.waitForTimeout(4000)
await page.click('.el-dialog button')

// ✅ 等到弹窗可见再点
await page.locator('.el-dialog').waitFor({ state: 'visible' })
await page.locator('.el-dialog').getByRole('button', { name: '确定' }).click()
```

## 陷阱 7：跨浏览器下 data-testid 缺失

很多业务项目不加 `data-testid`。不要固执要求加，灵活用：
1. `getByRole` + 文案（首选）
2. `getByPlaceholder` / `getByLabel`
3. `.el-form-item` 带 `hasText` 过滤后链式定位（Element Plus 专用）
4. CSS class（最后手段，容易被重构打破）

## 陷阱 8：baseline 为空导致 vacuous pass

数据库真的空的时候，`total === 0` 的断言 vacuously pass，筛选用例看起来通过但没测到任何东西。

```typescript
const baseline = await apiList(page, {})
test.skip(baseline.total === 0, '测试库无数据，无法验证过滤语义')
// ...
```

## 陷阱 9：测试污染 storageState

在 test 里 `localStorage.clear()` 或用未登录页面，下个 test 的 storageState 里 token 可能被吃掉。

- storageState 由 globalSetup 一次性生成并只读
- 要测未登录流程，用 `test.use({ storageState: { cookies: [], origins: [] } })`

## 陷阱 10：测试和实现一起改

"测试在改 A 文件的时候跟着改了 A.spec"——通常意味着测试在验证实现细节而不是行为，反模式。

**正确姿态**：测试描述的是"用户看到/点到什么"，不是"组件内部 state 变成什么"。
