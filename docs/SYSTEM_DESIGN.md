# 图书管理系统 - 系统设计文档

## 1. 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│  │图书  │ │借阅  │ │用户  │ │AI    │ │统计  │          │
│  │管理  │ │管理  │ │管理  │ │助手  │ │报表  │          │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘          │
└─────┼────────┼────────┼────────┼────────┼───────────────┘
      │        │        │        │        │
      ▼        ▼        ▼        ▼        ▼
┌─────────────────────────────────────────────────────────┐
│                  API Gateway (FastAPI)                    │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│  │图书  │ │借阅  │ │认证  │ │AI    │ │统计  │          │
│  │API   │ │API   │ │API   │ │API   │ │API   │          │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘          │
└─────┼────────┼────────┼────────┼────────┼───────────────┘
      │        │        │        │        │
      ▼        ▼        ▼        ▼        ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Database │ │  Auth    │ │AI Service│ │  Cache   │
│(SQLite/  │ │ (JWT)    │ │(OpenAI   │ │ (Redis)  │
│ Postgres)│ │          │ │ Compat.) │ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

## 2. 数据库设计

### 2.1 ER 图

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   users     │       │   books     │       │  borrows    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──┐   │ id (PK)     │◄──┐   │ id (PK)     │
│ username    │   │   │ title       │   │   │ user_id(FK) │──┐
│ email       │   │   │ author      │   │   │ book_id(FK) │──┤
│ password_hash│  │   │ isbn        │   │   │ borrow_date │  │
│ role        │   │   │ category    │   │   │ due_date    │  │
│ avatar      │   │   │ description │   │   │ return_date │  │
│ created_at  │   │   │ cover_url   │   │   │ status      │  │
│ updated_at  │   │   │ location    │   │   │ created_at  │  │
└─────────────┘   │   │ total_copies│   │   └─────────────┘  │
                  │   │ available   │   │                    │
┌─────────────┐   │   │ embedding   │   │   ┌─────────────┐  │
│ categories  │   │   │ ai_summary  │   │   │reviews      │  │
├─────────────┤   │   │ created_at  │   │   ├─────────────┤  │
│ id (PK)     │   │   │ updated_at  │   │   │ id (PK)     │  │
│ name        │   │   └─────────────┘   │   │ user_id(FK) │◄─┘
│ parent_id   │   │                     │   │ book_id(FK) │
│ description │   │   ┌─────────────┐   │   │ rating      │
└─────────────┘   │   │book_tags    │   │   │ comment     │
                  │   ├─────────────┤   │   │ created_at  │
                  │   │ book_id(FK) │───┘   └─────────────┘
                  │   │ tag_id (FK) │
                  │   └─────────────┘
                  │
                  │   ┌─────────────┐
                  │   │ai_logs      │
                  │   ├─────────────┤
                  └───│ id (PK)     │
                      │ user_id(FK) │
                      │ type        │
                      │ query       │
                      │ response    │
                      │ model       │
                      │ tokens_used │
                      │ created_at  │
                      └─────────────┘
```

### 2.2 表结构

#### users 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| username | VARCHAR(50) UNIQUE | 用户名 |
| email | VARCHAR(100) UNIQUE | 邮箱 |
| password_hash | VARCHAR(255) | 密码哈希 (bcrypt) |
| role | ENUM('admin','user') | 角色 |
| avatar | VARCHAR(255) | 头像 URL |
| is_active | BOOLEAN | 是否激活 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### books 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| title | VARCHAR(200) | 书名 |
| author | VARCHAR(100) | 作者 |
| isbn | VARCHAR(20) UNIQUE | ISBN |
| publisher | VARCHAR(100) | 出版社 |
| publish_date | DATE | 出版日期 |
| category_id | INTEGER FK | 分类 |
| description | TEXT | 简介 |
| cover_url | VARCHAR(255) | 封面 URL |
| location | VARCHAR(50) | 馆藏位置 |
| total_copies | INTEGER | 总册数 |
| available_copies | INTEGER | 可借册数 |
| embedding | BLOB | 向量 embedding |
| ai_summary | TEXT | AI 生成摘要 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### borrows 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| user_id | INTEGER FK | 借阅人 |
| book_id | INTEGER FK | 图书 |
| borrow_date | DATETIME | 借阅时间 |
| due_date | DATETIME | 应还时间 |
| return_date | DATETIME | 实际归还时间 |
| status | ENUM('borrowed','returned','overdue') | 状态 |
| renew_count | INTEGER | 续借次数 |
| created_at | DATETIME | 创建时间 |

## 3. API 设计

### 3.1 认证 API
```
POST   /api/auth/register     注册
POST   /api/auth/login        登录
POST   /api/auth/refresh      刷新 Token
GET    /api/auth/me           获取当前用户
```

### 3.2 图书 API
```
GET    /api/books             图书列表（分页、筛选）
POST   /api/books             新增图书（管理员）
GET    /api/books/{id}        图书详情
PUT    /api/books/{id}        更新图书（管理员）
DELETE /api/books/{id}        删除图书（管理员）
GET    /api/books/search      搜索图书
GET    /api/books/categories  分类列表
```

### 3.3 借阅 API
```
POST   /api/borrows           借书
PUT    /api/borrows/{id}/return  还书
PUT    /api/borrows/{id}/renew   续借
GET    /api/borrows/my        我的借阅记录
GET    /api/borrows           所有借阅记录（管理员）
```

### 3.4 AI API
```
POST   /api/ai/recommend      智能推荐
POST   /api/ai/search         语义搜索
POST   /api/ai/classify       智能分类
POST   /api/ai/summarize      摘要生成
POST   /api/ai/chat           对话助手
```

### 3.5 统计 API
```
GET    /api/stats/overview     总览数据
GET    /api/stats/borrows      借阅统计
GET    /api/stats/popular      热门图书
```

## 4. AI 服务架构

### 4.1 LLM 调用层
```python
class AIService:
    """统一 AI 服务层，支持多种 LLM 后端"""
    
    def __init__(self):
        self.api_key = os.getenv("AI_API_KEY")  # 仅从环境变量读取
        self.base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    
    async def chat(self, messages, **kwargs) -> str:
        """通用对话接口"""
        
    async def embed(self, text: str) -> list[float]:
        """文本向量化"""
        
    async def recommend(self, user_profile, books) -> list:
        """智能推荐"""
        
    async def semantic_search(self, query, book_embeddings) -> list:
        """语义搜索"""
```

### 4.2 向量搜索流程
```
用户查询 → Query Embedding → 余弦相似度计算 → Top-K 结果返回
                ↓
        图书 Embedding 库（预计算存储）
```

### 4.3 密钥安全方案
```
┌─────────────────────────────────────────┐
│              安全边界                    │
│                                         │
│  环境变量 (.env)                        │
│  ┌─────────────────┐                    │
│  │ AI_API_KEY=sk-..│ ◄── 仅服务端读取   │
│  │ AI_BASE_URL=... │                    │
│  └────────┬────────┘                    │
│           │                             │
│           ▼                             │
│  ┌─────────────────┐                    │
│  │   AI Service    │ ◄── 后端代理       │
│  └────────┬────────┘                    │
│           │                             │
│           ▼                             │
│  ┌─────────────────┐                    │
│  │   /api/ai/*     │ ◄── 前端调用       │
│  └─────────────────┘                    │
│                                         │
└─────────────────────────────────────────┘

✅ 前端永远不接触 API Key
✅ .env 加入 .gitignore
✅ 支持 Key 轮换（重启服务即可）
```

## 5. 目录结构

```
library-management-system/
├── docs/                    # 文档
│   ├── PRD.md              # 产品需求
│   ├── SYSTEM_DESIGN.md    # 系统设计（本文档）
│   └── TEST_PLAN.md        # 测试计划
├── backend/                 # 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── auth.py
│   │   │   ├── books.py
│   │   │   ├── borrows.py
│   │   │   ├── ai.py
│   │   │   └── stats.py
│   │   ├── models/         # 数据模型
│   │   │   ├── user.py
│   │   │   ├── book.py
│   │   │   └── borrow.py
│   │   ├── services/       # 业务逻辑
│   │   │   ├── auth_service.py
│   │   │   ├── book_service.py
│   │   │   ├── borrow_service.py
│   │   │   └── ai_service.py
│   │   ├── core/           # 核心模块
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── deps.py
│   │   └── main.py         # 应用入口
│   ├── requirements.txt
│   ├── .env.example        # 环境变量模板
│   └── .gitignore
├── frontend/                # 前端
│   ├── src/
│   │   ├── api/            # API 调用
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── hooks/          # 自定义 Hook
│   │   ├── utils/          # 工具函数
│   │   └── App.tsx
│   ├── package.json
│   └── .gitignore
├── README.md
├── docker-compose.yml
└── Makefile
```

## 6. 部署方案

### 6.1 开发环境
```bash
# 后端
cd backend && pip install -r requirements.txt
cp .env.example .env  # 配置 API Key
uvicorn app.main:app --reload

# 前端
cd frontend && npm install && npm start
```

### 6.2 Docker 部署
```bash
docker-compose up -d
```

### 6.3 生产环境
- Nginx 反向代理
- Gunicorn + Uvicorn Workers
- PostgreSQL 数据库
- Redis 缓存
- Let's Encrypt SSL
