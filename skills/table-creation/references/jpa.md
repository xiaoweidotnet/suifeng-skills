# JPA / Hibernate 代码生成模板

当用户选择 JPA / Hibernate 作为 ORM 框架时，使用本文件中的模板生成全套代码。

## 文件位置规范

```
api-service/src/main/java/org/xyog/zrapi/
├── entity/{module}/{EntityName}.java
└── repository/{module}/{EntityName}Repository.java
```

## Entity（实体类）

```java
package org.xyog.zrapi.entity.{module};

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "{table_name}")
public class {EntityName} {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 业务字段...

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @Column(name = "is_deleted", nullable = false)
    private Integer isDeleted = 0;

    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;

    @PrePersist
    public void prePersist() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (isDeleted == null) isDeleted = 0;
    }

    @PreUpdate
    public void preUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

## Repository

```java
package org.xyog.zrapi.repository.{module};

import org.xyog.zrapi.entity.{module}.{EntityName};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface {EntityName}Repository extends JpaRepository<{EntityName}, Long> {

    @Modifying
    @Query("UPDATE {EntityName} e SET e.isDeleted = 1, e.deletedAt = CURRENT_TIMESTAMP WHERE e.id = :id AND e.isDeleted = 0")
    int softDeleteById(@Param("id") Long id);

    @Query("SELECT e FROM {EntityName} e WHERE e.isDeleted = 0 AND e.deletedAt IS NULL")
    java.util.List<{EntityName}> findAllActive();
}
```
