# 图书管理系统 - Backend

基于 FastAPI 的智能图书管理系统后端。

## 功能特性

- 📚 图书 CRUD 管理
- 🔄 借阅/归还/续借
- 👤 用户认证 (JWT)
- 🤖 AI 智能推荐
- 🔍 语义搜索
- 📊 数据统计

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 AI API Key

# 3. 启动服务
uvicorn app.main:app --reload --port 8000
```

## API 文档

启动后访问: http://localhost:8000/docs

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| AI_API_KEY | LLM API Key | 是 |
| AI_BASE_URL | LLM API 地址 | 否 |
| AI_MODEL | 模型名称 | 否 |
| JWT_SECRET | JWT 密钥 | 否(自动生成) |
| DATABASE_URL | 数据库地址 | 否(默认 SQLite) |
