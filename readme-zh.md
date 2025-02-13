# AIStudio 网站爬虫

[English](./README.md) | 简体中文

一个基于 FastAPI 和 Playwright 构建的网站爬虫服务，可抓取网站信息、截图，并使用 LLM 能力处理内容。

## 功能特点

- 网站内容提取和截图捕获
- 多语言内容处理
- 基于内容的标签生成
- Supabase 内容存储
- RESTful API 接口

## 系统要求

- Python 3.12
- Supabase 账号
- Groq API 密钥
- Docker（可选）

## 快速开始

1. 克隆仓库
2. 安装依赖：
```sh
pip install -r requirements.txt
```

## 配置

### 环境变量

创建 `.env` 文件并添加以下内容：

```sh
GROQ_API_KEY=你的_groq_api_密钥
GROQ_MODEL=llama3-70b-8192
GROQ_MAX_TOKENS=5000
SUPABASE_URL=你的_supabase_地址
SUPABASE_SERVICE_ROLE_KEY=你的_supabase_密钥
```

## API 参考

### POST /site/crawl

爬取网站并处理其内容。

**请求体：**
```json
{
    "url": "https://example.com",
    "tags": ["可选", "标签"],
    "languages": ["zh", "en"]
}
```

**响应：**
```json
{
    "name": "域名-路径",
    "url": "https://example.com",
    "title": "页面标题",
    "description": "页面描述",
    "detail": "处理后的内容",
    "screenshot_key": "screenshot.png",
    "tags": ["生成的", "标签"],
    "languages": [
        {
            "language": "en",
            "title": "英文标题",
            "description": "英文描述",
            "detail": "英文内容"
        }
    ]
}
```

## 部署

### Docker

使用 Docker 构建和运行：

```sh
docker build -t aistudio-crawler .
docker run -p 8000:8000 aistudio-crawler
```

## 架构

### 核心组件

- **main_api.py**: FastAPI 应用程序和端点定义
- **website_crawler.py**: 核心爬虫实现
- **llm_util.py**: LLM 处理工具
- **common_util.py**: 通用工具

### 核心功能

1. **网站内容提取**
   - 页面元数据（标题、描述）
   - 完整页面内容处理
   - 截图捕获
   - LLM 处理

2. **内容处理**
   - 标签生成
   - 多语言翻译

3. **存储集成**
   - 截图存储在 Supabase
   - 使用 Groq LLM 进行内容处理
