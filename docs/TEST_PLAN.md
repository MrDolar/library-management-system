# 图书管理系统 - 测试分析文档

## 1. 测试策略

### 1.1 测试层次
```
┌─────────────────────────────┐
│     E2E 测试 (Cypress)      │  10%
├─────────────────────────────┤
│   集成测试 (API 测试)        │  30%
├─────────────────────────────┤
│    单元测试 (pytest)         │  60%
└─────────────────────────────┘
```

### 1.2 测试工具
| 类型 | 工具 | 用途 |
|------|------|------|
| 单元测试 | pytest + pytest-asyncio | 后端逻辑测试 |
| API 测试 | httpx / TestClient | 接口测试 |
| 前端测试 | Jest + React Testing Library | 组件测试 |
| E2E 测试 | Cypress | 端到端测试 |
| 覆盖率 | pytest-cov / Istanbul | 代码覆盖率 |
| 性能测试 | Locust | 压力测试 |

## 2. 单元测试用例

### 2.1 用户认证模块

#### 2.1.1 用户注册
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-AUTH-001 | 正常注册 | valid_user_data | 201, 返回用户信息 |
| TC-AUTH-002 | 用户名重复 | existing_username | 409, 用户名已存在 |
| TC-AUTH-003 | 邮箱格式错误 | invalid_email | 422, 验证失败 |
| TC-AUTH-004 | 密码太短 | short_password | 422, 密码至少6位 |
| TC-AUTH-005 | 必填字段缺失 | missing_fields | 422, 字段验证失败 |

#### 2.1.2 用户登录
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-AUTH-006 | 正常登录 | valid_credentials | 200, 返回 JWT Token |
| TC-AUTH-007 | 密码错误 | wrong_password | 401, 认证失败 |
| TC-AUTH-008 | 用户不存在 | nonexist_user | 401, 认证失败 |
| TC-AUTH-009 | Token 刷新 | valid_refresh_token | 200, 新 Token |
| TC-AUTH-010 | 过期 Token | expired_token | 401, Token 过期 |

### 2.2 图书管理模块

#### 2.2.1 图书 CRUD
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-BOOK-001 | 新增图书 | valid_book_data | 201, 返回图书信息 |
| TC-BOOK-002 | ISBN 重复 | duplicate_isbn | 409, ISBN 已存在 |
| TC-BOOK-003 | 获取图书列表 | page=1&size=10 | 200, 分页数据 |
| TC-BOOK-004 | 获取单本图书 | valid_id | 200, 图书详情 |
| TC-BOOK-005 | 图书不存在 | invalid_id | 404, 未找到 |
| TC-BOOK-006 | 更新图书 | valid_update | 200, 更新后数据 |
| TC-BOOK-007 | 删除图书（无在借） | available_book | 200, 删除成功 |
| TC-BOOK-008 | 删除图书（有在借） | borrowed_book | 400, 无法删除 |
| TC-BOOK-009 | 按书名搜索 | keyword | 200, 匹配结果 |
| TC-BOOK-010 | 按分类筛选 | category_id | 200, 分类图书 |

#### 2.2.2 权限控制
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-BOOK-011 | 管理员新增图书 | admin_token | 201, 成功 |
| TC-BOOK-012 | 普通用户新增图书 | user_token | 403, 权限不足 |
| TC-BOOK-013 | 未登录访问 | no_token | 401, 未认证 |

### 2.3 借阅管理模块

#### 2.3.1 借书
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-BORROW-001 | 正常借书 | user_id, book_id | 201, 借阅成功 |
| TC-BORROW-002 | 库存不足 | unavailable_book | 400, 无可用库存 |
| TC-BORROW-003 | 重复借阅 | already_borrowed | 400, 已借阅该书 |
| TC-BORROW-004 | 超过借阅上限 | max_borrows_reached | 400, 达到上限 |
| TC-BORROW-005 | 借阅逾期用户 | overdue_user | 400, 有逾期未还 |

#### 2.3.2 还书
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-BORROW-006 | 正常还书 | borrow_id | 200, 归还成功 |
| TC-BORROW-007 | 逾期归还 | overdue_borrow | 200, 标记逾期 |
| TC-BORROW-008 | 重复归还 | returned_borrow | 400, 已归还 |
| TC-BORROW-009 | 归还后库存 | after_return | 库存 +1 |

#### 2.3.3 续借
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-BORROW-010 | 正常续借 | valid_borrow | 200, 延期成功 |
| TC-BORROW-011 | 超过续借次数 | max_renewals | 400, 次数用完 |
| TC-BORROW-012 | 已逾期续借 | overdue_borrow | 400, 无法续借 |

### 2.4 AI 功能模块

#### 2.4.1 智能推荐
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-AI-001 | 正常推荐 | user_id | 200, 推荐列表 |
| TC-AI-002 | 新用户推荐（冷启动） | new_user | 200, 热门推荐 |
| TC-AI-003 | AI 服务不可用 | ai_down | 200, 降级推荐 |
| TC-AI-004 | 推荐结果去重 | user_id | 无重复图书 |

#### 2.4.2 语义搜索
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-AI-005 | 中文语义搜索 | "太空探索" | 200, 相关图书 |
| TC-AI-006 | 英文语义搜索 | "space exploration" | 200, 相关图书 |
| TC-AI-007 | 模糊搜索 | "一本有趣的书" | 200, 推荐结果 |
| TC-AI-008 | 空查询 | "" | 400, 查询不能为空 |
| TC-AI-009 | 向量索引为空 | first_run | 200, 降级关键词搜索 |

#### 2.4.3 智能分类
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-AI-010 | 正常分类 | book_info | 200, 分类标签 + 置信度 |
| TC-AI-011 | 多分类 | ambiguous_book | 200, 多个标签 |
| TC-AI-012 | AI 失败降级 | ai_error | 200, 默认分类 |

#### 2.4.4 密钥安全
| 编号 | 场景 | 输入 | 预期结果 |
|------|------|------|----------|
| TC-AI-013 | 前端不泄露密钥 | frontend_code | 无 API Key |
| TC-AI-014 | .env 不提交 | git_history | .gitignore 生效 |
| TC-AI-015 | API 响应不含密钥 | ai_response | 无 key 信息 |
| TC-AI-016 | 环境变量读取 | process.env | 正确读取 |

## 3. 集成测试用例

### 3.1 完整借阅流程
| 编号 | 流程 | 步骤 | 预期结果 |
|------|------|------|----------|
| TC-INT-001 | 借还全流程 | 注册→登录→借书→还书 | 全程成功 |
| TC-INT-002 | 推荐→借阅 | 登录→获取推荐→借推荐图书 | 推荐有效 |
| TC-INT-003 | 搜索→借阅 | 语义搜索→查看详情→借书 | 搜索准确 |
| TC-INT-004 | 逾期处理 | 借书→超期→还书→标记逾期 | 逾期正确 |

### 3.2 并发场景
| 编号 | 场景 | 操作 | 预期结果 |
|------|------|------|----------|
| TC-INT-005 | 最后一册并发借 | 2 用户同时借 | 1 成功 1 失败 |
| TC-INT-006 | 同时借还 | 借书+还书并发 | 数据一致 |

## 4. E2E 测试用例

| 编号 | 场景 | 步骤 |
|------|------|------|
| TC-E2E-001 | 注册并借书 | 注册→登录→浏览→借书→查看我的借阅 |
| TC-E2E-002 | 管理员管理 | 登录→新增图书→查看借阅记录→统计 |
| TC-E2E-003 | AI 推荐流程 | 登录→借几本书→获取推荐→验证推荐 |
| TC-E2E-004 | 语义搜索 | 登录→输入自然语言→查看结果→借书 |

## 5. 性能测试

### 5.1 基准指标
| 指标 | 目标 | 测试方法 |
|------|------|----------|
| 图书列表响应 | < 200ms (p95) | Locust 100 并发 |
| 搜索响应 | < 500ms (p95) | Locust 50 并发 |
| AI 推荐响应 | < 3s (p95) | Locust 20 并发 |
| 登录响应 | < 300ms (p95) | Locust 100 并发 |
| 数据库查询 | < 50ms (avg) | 慢查询日志 |

### 5.2 压力测试
```python
from locust import HttpUser, task, between

class LibraryUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "password123"
        })
    
    @task(3)
    def list_books(self):
        self.client.get("/api/books?page=1&size=10")
    
    @task(2)
    def search_books(self):
        self.client.get("/api/books/search?keyword=python")
    
    @task(1)
    def ai_recommend(self):
        self.client.post("/api/ai/recommend")
```

## 6. 安全测试

| 编号 | 测试项 | 方法 | 预期 |
|------|--------|------|------|
| TC-SEC-001 | SQL 注入 | 特殊输入 | 无影响 |
| TC-SEC-002 | XSS 攻击 | 脚本注入 | 被转义 |
| TC-SEC-003 | CSRF 防护 | 伪造请求 | 被拒绝 |
| TC-SEC-004 | JWT 篡改 | 修改 Token | 401 |
| TC-SEC-005 | 越权访问 | 低权限操作 | 403 |
| TC-SEC-006 | 密钥泄露 | 代码扫描 | 无泄露 |
| TC-SEC-007 | 暴力破解 | 多次错误登录 | 账号锁定 |

## 7. 测试覆盖率目标

| 模块 | 目标覆盖率 |
|------|-----------|
| models/ | 95% |
| services/ | 90% |
| api/ | 85% |
| core/ | 90% |
| 总体 | 85%+ |

## 8. CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run tests
        run: cd backend && pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4
```
