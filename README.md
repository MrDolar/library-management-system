# 📚 智能图书管理系统

AI 驱动的现代化图书管理平台，集成智能推荐、语义搜索、自动分类等 AI 功能。

## ✨ 功能特性

### 核心功能
- 📖 **图书管理** - CRUD、分类、库存管理
- 🔄 **借阅管理** - 借书、还书、续借、逾期处理
- 👤 **用户管理** - 注册、登录、角色权限
- 📊 **数据统计** - 借阅报表、热门图书

### AI 智能功能 🤖
- 🎯 **智能推荐** - 基于借阅历史的个性化推荐
- 🔍 **语义搜索** - 自然语言描述找书（如"关于太空的科幻小说"）
- 🏷️ **智能分类** - AI 自动推荐图书分类
- 📝 **摘要生成** - 自动生成图书简介
- 💬 **对话助手** - AI 回答图书馆相关问题

## 🏗️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18 + TypeScript + Ant Design |
| 后端 | Python 3.11 + FastAPI + SQLAlchemy |
| 数据库 | SQLite (开发) / PostgreSQL (生产) |
| AI | OpenAI Compatible API |
| 认证 | JWT |

## 🚀 快速开始

### 前置要求
- Python 3.11+
- Node.js 18+ (前端开发)
- AI API Key (OpenAI / DeepSeek 等)

### 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 AI_API_KEY

# 启动服务
uvicorn app.main:app --reload --port 8000
```

启动后访问:
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

### Docker 部署

```bash
docker-compose up -d
```

## 📁 项目结构

```
library-management-system/
├── docs/                    # 📄 项目文档
│   ├── PRD.md              # 产品需求文档
│   ├── SYSTEM_DESIGN.md    # 系统设计文档
│   └── TEST_PLAN.md        # 测试分析文档
├── backend/                 # 🐍 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── core/           # 核心模块
│   └── requirements.txt
├── frontend/                # ⚛️ 前端应用 (待实现)
├── docker-compose.yml
└── README.md
```

## 🔐 安全设计

### AI 密钥安全
- ✅ API Key 仅存储在服务端环境变量
- ✅ 前端不接触任何密钥
- ✅ 所有 AI 请求通过后端代理
- ✅ `.env` 已加入 `.gitignore`
- ✅ 支持 Key 轮换

### 认证安全
- JWT Token 认证
- bcrypt 密码哈希
- 角色分级权限
- SQL 注入防护

## 📖 API 接口

### 认证
```
POST /api/auth/register    注册
POST /api/auth/login       登录
GET  /api/auth/me          当前用户
```

### 图书
```
GET    /api/books           图书列表
POST   /api/books           新增图书 (管理员)
GET    /api/books/{id}      图书详情
PUT    /api/books/{id}      更新图书 (管理员)
DELETE /api/books/{id}      删除图书 (管理员)
GET    /api/books/search    搜索图书
```

### 借阅
```
POST /api/borrows              借书
PUT  /api/borrows/{id}/return  还书
PUT  /api/borrows/{id}/renew   续借
GET  /api/borrows/my           我的借阅
```

### AI 功能
```
POST /api/ai/recommend     智能推荐
POST /api/ai/search        语义搜索
POST /api/ai/classify      智能分类
POST /api/ai/summarize     摘要生成
POST /api/ai/chat          对话助手
```

## ⚙️ 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `AI_API_KEY` | LLM API Key | (必填) |
| `AI_BASE_URL` | LLM API 地址 | https://api.openai.com/v1 |
| `AI_MODEL` | 对话模型 | gpt-3.5-turbo |
| `AI_EMBEDDING_MODEL` | 向量模型 | text-embedding-ada-002 |
| `JWT_SECRET` | JWT 密钥 | (自动生成) |
| `DATABASE_URL` | 数据库地址 | sqlite:///./library.db |

## 🤝 支持的 AI 服务

本系统使用 OpenAI Compatible API，支持以下服务：

| 服务 | BASE_URL | 说明 |
|------|----------|------|
| OpenAI | https://api.openai.com/v1 | 官方 API |
| DeepSeek | https://api.deepseek.com/v1 | 国产大模型 |
| 本地模型 | http://localhost:11434/v1 | Ollama 等 |
| 其他 | 自定义 | 兼容 OpenAI 格式即可 |

## 📄 文档

- [产品需求文档 (PRD)](docs/PRD.md)
- [系统设计文档](docs/SYSTEM_DESIGN.md)
- [测试分析文档](docs/TEST_PLAN.md)

## 📝 License

MIT License
