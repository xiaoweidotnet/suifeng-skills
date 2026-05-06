---
name: page-to-e2e
description: 根据用户提供的页面地址（URL 或路由路径）为该页面生成完整的 Playwright e2e 测试，覆盖页面上所有可见功能（筛选、表格、按钮、弹窗、跳转、导出等）。先询问使用真实 API 还是 Mock 数据两种模式，再读取组件源码推断功能点，最后生成并运行测试。适用于用户说“给这个页面生成 e2e”“测一下 /xxx 页的功能”“写 playwright 测试”“为 xxx 页补 e2e”等场景。
---

# Page → E2E 测试生成

根据用户提供的页面地址（URL、路由路径或组件文件路径），生成一套覆盖页面全部可见功能的 Playwright e2e 测试。

## 工作流

必须严格按顺序执行：

1. **定位页面源码** → 根据用户给的地址找到组件文件
2. **询问 API 模式** → 真实 API 还是 Mock 数据（必须问，不要自作主张）
3. **勘探页面功能** → 读组件源码列出所有可测点
4. **勘探项目约定** → 读现有 e2e 配置/用例，沿用项目既有模式
5. **生成 spec 文件** → 按功能分组，每个功能一个 test
6. **运行并修复** → 跑一次，失败就修，直到全绿
7. **输出测试报告** → 按模板给出通过率、失败项、产物路径

跳过任何一步都会产生低质量测试。

### Step 1：定位页面源码

用户输入可能是：
- URL：`http://localhost:5175/customer/list`
- 路由路径：`/customer/list`
- 组件文件：`frontend/src/views/customer/List.vue`
- 页面描述：`客户列表页`

用工具定位：
- URL/路径 → 搜路由配置（`src/router/**`）找到对应组件
- 描述 → 按语义在 `src/views/**` 或 `pages/**` 搜索

**禁止**在没读组件源码的情况下凭空编写测试。

### Step 2：询问 API 模式（关键）

**必须用 AskUserQuestion 向用户提问**，不要自己决定：

```
问题：这次 e2e 用什么数据源？
选项 A：真实 API（推荐）
  - 贴近生产行为，能抓到后端 bug（如筛选失效、权限漏网）
  - 依赖本地后端 + 数据库/Redis 就绪，需要预先登录态
选项 B：Mock 数据
  - 用 page.route() 拦截 /api/** 返回固定 JSON
  - 不依赖后端，跑得快，CI 稳定
  - 只能测前端渲染和交互，测不到后端筛选/权限语义
选项 C：混合模式
  - 查询类接口 Mock 固定返回，写操作（新增/删除）仅点到 UI 不真实提交
```

记录用户选择，后续 spec 生成按此分支走。两种模式的具体做法见 [references/mock-strategies.md](references/mock-strategies.md)。

### Step 3：勘探页面功能

读组件源码（template + script），列出所有可测点。**输出一份功能清单让用户确认**（可简化为一条消息列出，不必专门 ask），至少覆盖：

| 类别 | 具体点 |
|------|--------|
| 渲染 | 页面标题、核心按钮、表单项（label 是否齐全）、表格列头 |
| 筛选 | 每个筛选项的入参下发 + 后端过滤语义（真实 API 模式下用不匹配值验证 total=0） |
| 分页 | 切页、切页大小 |
| 行操作 | 详情、编辑、删除、分配等（副作用操作只打开弹窗不提交） |
| 弹窗/抽屉 | 打开、字段齐全、关闭 |
| 跳转 | 新增/编辑按钮跳转目标路由 |
| 导出/下载 | 用 `waitForResponse` 验证接口调用，不要用 `waitForEvent('download')` |
| 权限/空态 | 无数据时的空态、无权限时的隐藏按钮 |

### Step 4：勘探项目约定（产出 project-profile）

**先检查** `references/project-profile.md` 是否已存在：
- 存在 → 直接读取并复用，跳过本步
- 不存在 → 按下表勘探，把结果写入 `references/project-profile.md` 作为本项目的配置缓存

| 维度 | 勘探来源 | 典型取值 |
|------|----------|---------|
| 测试框架 | `package.json` devDependencies、`playwright.config.*` | `@playwright/test` / Cypress / 其他 |
| baseURL 与后端地址 | `playwright.config.*`、前端构建配置（vite/webpack/next） | 前端 `:5173-5175`、后端 `:8080/:3000/:8188` |
| API 代理前缀 | 前端构建配置里的 proxy 或环境变量 | `/api` → 后端 |
| 认证方式 | `globalSetup` / fixture / 登录相关源码 | `Authorization: Bearer ${localStorage.token}` / cookie / httpOnly |
| Token 存储键 | 前端 axios 拦截器或登录回调 | `localStorage.token` / `access_token` / `sessionStorage.jwt` |
| UI 库 | `package.json` dependencies | Element Plus / Ant Design Vue / Naive UI / Vant |
| UI 语言包 | `main.ts`/`main.js` 里的 `locale` 配置 | 中文 `50 条/页` / 英文 `50/page` |
| 选择器风格 | 现有 spec 任选一个 | `data-testid` / `getByRole` / UI 库 class |
| API 路径前缀 | 现有接口调用 | `/api/admin/**` / `/api/v1/**` |
| 导出接口约定 | 业务代码搜 `export` | 响应 blob / 返回下载链接 |
| 过滤语义校验基线 | 无需勘探，固定策略 | 用不匹配值（`2000-01-01`、`__nonexistent__`）断言 `total === 0` |

勘探完成后，在 `references/project-profile.md` 以 key-value 形式记录，后续 step 5、6 生成 spec 时直接引用这份 profile，不要再猜。

沿用项目既有模式，不要新造一套。

### Step 5：生成 spec 文件

- 文件路径：与现有 spec 同目录，命名 `{page-name}.spec.ts`
- 按 `test.describe` 分组：渲染 / 筛选 / 行操作 / 弹窗 / 过滤语义
- 每个 test 只测一件事
- **副作用操作**（新增/删除/分配/移入公海/提交表单）默认只验证"能打开弹窗"和"取消按钮能关闭"，不实际提交，避免污染数据库
- 如果用户明确要求测写操作，改用 Mock 模式或在用例末尾手动清理数据

代码模板见 [references/spec-templates.md](references/spec-templates.md)。

### Step 6：运行并修复

```bash
npx playwright test e2e/your.spec.ts --reporter=line
```

常见失败与修法：

| 失败现象 | 原因 | 修法 |
|---------|------|------|
| 下拉选项找不到 | `.el-select-dropdown` 被 teleport 出多个实例 | 改用 `getByRole('option', { name, exact: true })` |
| 分页 "50/页" 找不到 | 项目未设中文 locale | 改用英文 `'50/page'` 或先在项目里配 locale |
| 下载超时 | 前端 blob+a.click 不触发 download 事件 | 改用 `waitForResponse(/\/api\/export/)` |
| 筛选看起来通过但没真过滤 | 只验证了入参 URL，没验证返回 | 加一组"用不匹配值验证 total=0"的语义用例 |
| 点击后元素消失 | 动画未结束 | `locator.waitFor({ state: 'visible' })` + `waitForLoadState('networkidle')` |

跑到全绿为止。**测试全绿不代表功能真的对**，见 [references/semantic-pitfalls.md](references/semantic-pitfalls.md)。

### Step 7：输出测试报告

按以下模板在最终消息里回给用户：

```markdown
## E2E 报告：{page-name}

**Spec 文件**：`e2e/xxx.spec.ts`
**数据源模式**：真实 API / Mock / 混合
**结果**：X passed / Y skipped / Z failed（耗时 Ns）

### 覆盖的功能点
- [x] 页面渲染（标题、按钮、表格列头）
- [x] 关键词搜索（入参 + 语义）
- [x] 标签筛选（入参 + 语义）
- [ ] 导出下载（已跳过，原因：…）

### 已知限制
- 副作用操作（新增/删除）只点到弹窗未提交
- xxx 功能依赖 yyy 数据，当前库为空已 skip
```

## 反模式

- ❌ 不读组件就写测试 → 必然漏功能或选择器错
- ❌ 不问用户就选真实 API / Mock → 每种都有代价，必须问
- ❌ 把其他项目的端口、认证方式、UI 库硬编码进来 → 每次换项目都要改，先勘探 project-profile
- ❌ 只验证入参下发不验证返回数据 → 假阳性，bug 照样漏（典型：MyBatis-Plus 顶层 `.or()` 打断 AND 链导致筛选失效，UI 看起来有下发参数但过滤无效）
- ❌ 副作用操作真实提交 → 污染数据库，跑完测试库里多出 N 条脏数据
- ❌ 用 `waitForTimeout(5000)` → 直接改 `waitForResponse` 或 locator auto-wait
- ❌ 选择器用 CSS class（如 `.el-select-dropdown`）→ teleport 多实例会歧义，优先 ARIA role

## 参考资料

- [references/spec-templates.md](references/spec-templates.md) — 渲染 / 筛选 / 弹窗 / 导出的现成代码片段（含 `{{占位}}` 需按 project-profile 替换）
- [references/mock-strategies.md](references/mock-strategies.md) — `page.route()` 拦截、fixture 构造、登录态 Mock
- [references/semantic-pitfalls.md](references/semantic-pitfalls.md) — 筛选假阳性、副作用污染、flaky 动画等陷阱
- [references/project-profile.area-rent.md](references/project-profile.area-rent.md) — area-rent 项目的 profile 示例，换项目时按此格式重新勘探
