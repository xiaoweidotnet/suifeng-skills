# MyBatis-Plus 代码生成模板

当用户选择 MyBatis-Plus 作为 ORM 框架时，使用本文件中的模板生成全套代码。

## 文件位置规范

```
api-service/src/main/java/org/xyog/zrapi/
├── entity/{module}/{EntityName}.java
├── mapper/{module}/{EntityName}Mapper.java
├── manager/{module}/{EntityName}Manager.java
└── manager/impl/{module}/{EntityName}ManagerImpl.java
```

## 项目相关配置

| 配置项 | 值 |
|--------|-----|
| 逻辑删除字段 | `deletedAt`（`logic-delete-field: deletedAt`） |
| 逻辑删除值 | `now()`（设置删除时间） |
| 逻辑未删除值 | `null`（NULL 表示未删除） |
| 自动填充 | `createdAt` → `FieldFill.INSERT`, `updatedAt` → `FieldFill.INSERT_UPDATE` |

## Entity（实体类）

```java
package org.xyog.zrapi.entity.{module};

import com.baomidou.mybatisplus.annotation.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@TableName("{table_name}")
public class {EntityName} {

    @TableId(type = IdType.AUTO)
    private Long id;

    // 业务字段...

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;

    private Integer isDeleted;

    @TableLogic
    private LocalDateTime deletedAt;
}
```

## Mapper 接口

```java
package org.xyog.zrapi.mapper.{module};

import org.xyog.zrapi.entity.{module}.{EntityName};
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface {EntityName}Mapper extends BaseMapper<{EntityName}> {
}
```

## Manager 接口

```java
package org.xyog.zrapi.manager.{module};

import org.xyog.zrapi.entity.{module}.{EntityName};
import com.baomidou.mybatisplus.extension.service.IService;

public interface {EntityName}Manager extends IService<{EntityName}> {
}
```

## ManagerImpl 实现

```java
package org.xyog.zrapi.manager.{module}.impl;

import org.xyog.zrapi.entity.{module}.{EntityName};
import org.xyog.zrapi.mapper.{module}.{EntityName}Mapper;
import org.xyog.zrapi.manager.{module}.{EntityName}Manager;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class {EntityName}ManagerImpl extends ServiceImpl<{EntityName}Mapper, {EntityName}> implements {EntityName}Manager {
}
```
