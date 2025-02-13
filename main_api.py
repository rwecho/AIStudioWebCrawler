import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from website_crawler import WebsiteCrawler
from typing import Dict, List, Optional

app = FastAPI()
crawler = WebsiteCrawler()


class URLRequest(BaseModel):
    url: str
    tags: Optional[List[str]] = None
    languages: Optional[List[str]] = None


@app.post("/site/crawl")
async def crawl_site(request: URLRequest) -> Dict:
    """
    Crawl the content of a website using the WebsiteCrawler.

    Args:
        url (str): The URL of the website to crawl.

    Returns:
        Dict: The result of the crawl operation.
    """

    url = request.url
    tags = request.tags if request.tags else []
    languages = request.languages if request.languages else ["zh", "en"]

    result = await crawler.crawl(url, tags=tags, languages=languages)
    return result


if __name__ == "__main__":
    import uvicorn

    asyncio.run(uvicorn.run(app, host="0.0.0.0", port=8000))
