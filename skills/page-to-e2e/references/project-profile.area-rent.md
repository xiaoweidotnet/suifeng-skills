# Project Profile 示例：area-rent

这是 area-rent 项目勘探出的配置结果，也是 `references/project-profile.md` 应该长的样子。换到别的项目时，按同样的字段重新勘探一遍即可。

## 基础信息

| Key | Value |
|-----|-------|
| `project_name` | area-rent |
| `test_framework` | `@playwright/test` |
| `e2e_dir` | `frontend/e2e/` |
| `config_file` | `frontend/playwright.config.ts` |

## 服务地址

| Key | Value |
|-----|-------|
| `frontend_base_url` | `http://localhost:5175` |
| `backend_base_url` | `http://localhost:8188` |
| `api_proxy_prefix` | `/api` → 8188（vite 代理） |
| `api_path_prefix` | `/api/admin/**` |

## 认证

| Key | Value |
|-----|-------|
| `auth_method` | Bearer Token |
| `token_storage` | `localStorage.getItem('token')` |
| `auth_header` | `Authorization: Bearer ${token}` |
| `login_setup` | `frontend/e2e/global-setup.ts`（captcha + redis-cli 自动登录，注入 localStorage token） |

## UI 库

| Key | Value |
|-----|-------|
| `ui_library` | Element Plus |
| `ui_locale` | **英文**（未配中文 locale） |
| `pagination_text` | `20/page`、`50/page`（不是 `20 条/页`） |
| `dropdown_selector` | `getByRole('option', { name, exact: true })` |
| `testid_convention` | 无统一 `data-testid`，优先 ARIA role + `.el-form-item` + `hasText` 组合 |

## 业务约定

| Key | Value |
|-----|-------|
| `export_api_pattern` | `/api/admin/xxx/export`，用 `waitForResponse` 监听 |
| `list_response_shape` | `{ code, data: { list, total }, message }` |
| `semantic_filter_baseline` | 时间范围用 `2000-01-01 ~ 2000-01-02`，字符串字段用 `__nonexistent__`，断言 `total === 0` |

## 已知坑

- IDEA 启动的 Spring Boot 改代码后需要重启
- `pagination` 找 `50/page` 而不是 `50 条/页`（因为 locale 未配中文）
- Element Plus 下拉/弹窗用了 teleport，避免 CSS class 选择器，用 ARIA role
- 历史 bug：MyBatis-Plus 顶层 `.or()` 打断 AND 链会让筛选失效（见 [CustomerService.java:59](file:///Users/xiaowei/work/code/waibao/area-rent/api-service/src/main/java/org/xyog/zrapi/service/CustomerService.java#L59)），所以过滤用例必须做语义校验而非仅入参校验
