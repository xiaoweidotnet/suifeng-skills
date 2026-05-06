---
name: table-creation
description: 
  数据库表结构创建技能。当用户提出"创建表"、"建表"、"新表"、"新增数据库表"、"设计表结构"、"添加数据库表"、"帮我建个表"、"我需要一张表"等与数据库建表相关的请求时，必须触发此技能。该技能确保所有新建表包含统一的规范字段（创建时间、修改时间、软删除标记和软删除时间），询问用户索引需求，并根据 ORM 框架生成对应的 Entity、Mapper、Manager（接口+实现）等全套代码。即使只是简单的"帮忙建个表"，也要触发此技能以确保一致性。
compatibility:
  - mysql
  - postgresql
  - mybatis-plus
  - mybatis
  - jpa
---

# 数据库表结构创建规范

每次创建新表时，必须按照以下流程操作，确保所有表具有统一的规范字段和一致的代码结构。

> **核心理由**：统一的基础字段（时间戳+软删除）是所有业务表的共同需求。拆分到不同表中手动处理容易遗漏，导致后续维护困难和代码不一致。本技能自动化这一过程，确保每个表都一致。

## 工作流程

### 第 1 步：了解业务需求

主动向用户了解以下信息：

1. **表名**：数据库中的表名（英文 snake_case，如 `user`, `customer_allocation`）
2. **表注释**：表的业务含义
3. **业务字段**：
   - 字段名、类型、长度、是否必填、默认值、注释
   - 是否需要唯一约束
   - 是否有外键关联（注意：通常建议用逻辑关联而非物理外键）
4. **所属模块**：用于确定 Java 包路径（如 `complaint`, `contract`, `order` 等）
5. **数据库类型**：MySQL / PostgreSQL / 其他（默认使用项目当前数据库）

### 第 2 步：询问 ORM 框架（重要）

询问用户使用哪种 ORM 框架，然后**阅读对应的引用文件**来获取代码模板：

| 框架 | 引用文件 | 生成内容 |
|------|---------|---------|
| **MyBatis-Plus**（项目默认） | `references/mybatis-plus.md` | Entity + Mapper + Manager（接口）+ ManagerImpl（实现） |
| **标准 MyBatis** | `references/mybatis.md` | Entity + Mapper（接口）+ Mapper.xml + Manager（接口）+ ManagerImpl（实现） |
| **JPA / Hibernate** | `references/jpa.md` | Entity + Repository |
| **仅 SQL / 无框架** | 不生成代码 | 只生成 DDL |

**重要**：根据用户选择，立即读取对应的引用文件，严格按照模板代码生成，不要自己猜测。

### 第 3 步：询问索引需求（必须）

在写入文件前，**必须**明确询问用户是否需要创建索引。给出合理建议（如外键字段、频繁查询字段建议加索引），但最终由用户决定。

可以这样询问：

```
是否需要为以下字段创建索引？
1. 建议：{外键字段名}（外键字段通常建议加索引）
2. 建议：{频繁查询字段名}
3. 是否有复合索引或唯一索引需求？
```

### 第 4 步：生成标准 DDL

根据数据库类型生成标准的 CREATE TABLE 语句，**必须包含以下基础字段**：

```sql
-- =============================================
-- 统一规范字段（所有表必须包含）
-- =============================================
`id`           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
-- 业务字段插入在这里 --
`created_at`   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`updated_at`   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
`deleted_at`   DATETIME DEFAULT NULL COMMENT '软删除时间（NULL=未删除）',
`is_deleted`   TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除：0=未删除 1=已删除',
PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='{表注释}';
```

#### PostgreSQL 版本

```sql
CREATE TABLE {table_name} (
    id            BIGSERIAL PRIMARY KEY,
    -- 业务字段 --
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ DEFAULT NULL,
    is_deleted    SMALLINT NOT NULL DEFAULT 0 CHECK(is_deleted IN (0, 1))
);
COMMENT ON TABLE {table_name} IS '{表注释}';
```

### 第 5 步：生成 ORM 代码

根据用户在第 2 步选择的 ORM 框架，**读取对应的引用文件**并按照模板生成代码：

| 选择 | 操作 |
|------|------|
| **MyBatis-Plus** | 读取 `references/mybatis-plus.md`，生成 Entity / Mapper / Manager / ManagerImpl |
| **标准 MyBatis** | 读取 `references/mybatis.md`，生成 Entity / Mapper / Mapper.xml / Manager / ManagerImpl |
| **JPA / Hibernate** | 读取 `references/jpa.md`，生成 Entity / Repository |

严格按照引用文件中的包路径、注解、代码结构创建 Java 源文件。

### 第 6 步：生成索引 DDL

根据用户确认的索引需求，追加索引定义。MySQL 可追加在 CREATE TABLE 末尾：

```sql
INDEX `idx_{field}` (`{field}`) COMMENT '索引注释',
UNIQUE KEY `uk_{field}` (`{field}`) COMMENT '唯一约束',
```

或者作为单独的 ALTER TABLE 语句输出。

### 第 7 步：输出并写入文件

1. **DDL SQL**：输出给用户，并写入 `doc/schema.sql` 追加在末尾
2. **Java 文件**：按用户选择的 ORM 框架创建对应文件到 api-service 对应包路径下
3. 告知用户所有文件已创建完成及路径

## 参考：项目现有规范摘要

| 项目 | 规范 |
|------|------|
| 数据库 | MySQL 8.0，InnoDB，utf8mb4 |
| ORM | MyBatis-Plus 3.5.1 |
| 逻辑删除 | `deleted_at` 标注 `@TableLogic`（配置：`logic-delete-field: deletedAt`, `logic-delete-value: now()`） |
| 自动填充 | `created_at` 使用 `FieldFill.INSERT`，`updated_at` 使用 `FieldFill.INSERT_UPDATE` |
| Lombok | `@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor` |
| 注入方式 | `@Autowired` 显式注入（不使用构造函数注入） |
| 分层 | controller → service → manager(impl) → mapper → DB |
| Entity 规范 | 不允许有多余的非表字段 |
