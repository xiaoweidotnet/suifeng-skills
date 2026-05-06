# 标准 MyBatis 代码生成模板

当用户选择标准 MyBatis（非 MyBatis-Plus）作为 ORM 框架时，使用本文件中的模板生成全套代码。

## 文件位置规范

```
api-service/src/main/java/org/xyog/zrapi/
├── entity/{module}/{EntityName}.java
├── mapper/{module}/{EntityName}Mapper.java
├── mapper/{module}/{EntityName}Mapper.xml
├── manager/{module}/{EntityName}Manager.java
└── manager/impl/{module}/{EntityName}ManagerImpl.java
```

## Entity（实体类）

使用纯 POJO，无框架注解：

```java
package org.xyog.zrapi.entity.{module};

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {EntityName} {

    private Long id;
    // 业务字段...
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private Integer isDeleted;
    private LocalDateTime deletedAt;
}
```

## Mapper 接口

```java
package org.xyog.zrapi.mapper.{module};

import org.xyog.zrapi.entity.{module}.{EntityName};
import java.util.List;

public interface {EntityName}Mapper {

    int insert({EntityName} entity);
    int updateById({EntityName} entity);
    int deleteById(Long id);
    {EntityName} selectById(Long id);
    List<{EntityName}> selectList({EntityName} condition);
}
```

## Mapper XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.xyog.zrapi.mapper.{module}.{EntityName}Mapper">

    <resultMap id="BaseResultMap" type="org.xyog.zrapi.entity.{module}.{EntityName}">
        <id column="id" property="id" jdbcType="BIGINT"/>
        <result column="created_at" property="createdAt" jdbcType="TIMESTAMP"/>
        <result column="updated_at" property="updatedAt" jdbcType="TIMESTAMP"/>
        <result column="is_deleted" property="isDeleted" jdbcType="TINYINT"/>
        <result column="deleted_at" property="deletedAt" jdbcType="TIMESTAMP"/>
    </resultMap>

    <sql id="Base_Column_List">
        id, created_at, updated_at, is_deleted, deleted_at
    </sql>

    <sql id="Not_Deleted">
        AND is_deleted = 0 AND deleted_at IS NULL
    </sql>

    <insert id="insert" useGeneratedKeys="true" keyProperty="id">
        INSERT INTO {table_name} (<!-- 业务字段 -->, created_at, updated_at)
        VALUES (<!-- #{业务字段} -->, NOW(), NOW())
    </insert>

    <update id="updateById">
        UPDATE {table_name} <set> updated_at = NOW() </set>
        WHERE id = #{id} AND is_deleted = 0
    </update>

    <update id="deleteById">
        UPDATE {table_name} SET is_deleted = 1, deleted_at = NOW() WHERE id = #{id}
    </update>

    <select id="selectById" resultMap="BaseResultMap">
        SELECT <include refid="Base_Column_List"/> FROM {table_name}
        WHERE id = #{id} <include refid="Not_Deleted"/>
    </select>

    <select id="selectList" resultMap="BaseResultMap">
        SELECT <include refid="Base_Column_List"/> FROM {table_name}
        WHERE 1=1 <include refid="Not_Deleted"/>
    </select>
</mapper>
```

## Manager 接口

```java
package org.xyog.zrapi.manager.{module};

import org.xyog.zrapi.entity.{module}.{EntityName};
import java.util.List;

public interface {EntityName}Manager {
    int create({EntityName} entity);
    int update({EntityName} entity);
    int delete(Long id);
    {EntityName} getById(Long id);
    List<{EntityName}> list({EntityName} condition);
}
```

## ManagerImpl 实现

```java
package org.xyog.zrapi.manager.{module}.impl;

import org.xyog.zrapi.entity.{module}.{EntityName};
import org.xyog.zrapi.mapper.{module}.{EntityName}Mapper;
import org.xyog.zrapi.manager.{module}.{EntityName}Manager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class {EntityName}ManagerImpl implements {EntityName}Manager {

    @Autowired
    private {EntityName}Mapper {entityName}Mapper;

    @Override public int create({EntityName} entity) { return {entityName}Mapper.insert(entity); }
    @Override public int update({EntityName} entity) { return {entityName}Mapper.updateById(entity); }
    @Override public int delete(Long id) { return {entityName}Mapper.deleteById(id); }
    @Override public {EntityName} getById(Long id) { return {entityName}Mapper.selectById(id); }
    @Override public List<{EntityName}> list({EntityName} condition) { return {entityName}Mapper.selectList(condition); }
}
```
