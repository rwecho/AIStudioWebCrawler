# AIStudio Web Crawler

English | [简体中文](./README-zh.md)

A web crawler service that captures website information, screenshots, and processes content using LLM capabilities. Built with FastAPI and Playwright.

## Features

- Website content extraction and screenshot capture
- Multi-language content processing
- Tag generation based on content
- Content storage in Supabase
- RESTful API interface

## Prerequisites

- Python 3.12
- Supabase account
- Groq API key
- Docker (optional)

## Quick Start

1. Clone the repository
2. Install dependencies:
```sh
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file with the following:

```sh
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-70b-8192
GROQ_MAX_TOKENS=5000
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_key
```

## API Reference

### POST /site/crawl

Crawls a website and processes its content.

**Request Body:**
```json
{
    "url": "https://example.com",
    "tags": ["optional", "tags"],
    "languages": ["zh", "en"]
}
```

**Response:**
```json
{
    "name": "domain-path",
    "url": "https://example.com",
    "title": "Page Title",
    "description": "Page Description",
    "detail": "Processed Content",
    "screenshot_key": "screenshot.png",
    "tags": ["generated", "tags"],
    "languages": [
        {
            "language": "en",
            "title": "English Title",
            "description": "English Description",
            "detail": "English Content"
        }
    ]
}
```

## Deployment

### Docker

Build and run using Docker:

```sh
docker build -t aistudio-crawler .
docker run -p 8000:8000 aistudio-crawler
```

## Architecture

### Key Components

- **main_api.py**: FastAPI application and endpoint definitions
- **website_crawler.py**: Core crawler implementation
- **llm_util.py**: LLM processing utilities
- **common_util.py**: Common utilities

### Core Features

1. **Website Content Extraction**
   - Page metadata (title, description)
   - Full page content processing
   - Screenshot capture
   - LLM Processing

2. **Content Processing**
   - Tag generation
   - Multi-language translation

3. **Storage Integration**
   - Screenshots stored in Supabase
   - Content processing with Groq LLM