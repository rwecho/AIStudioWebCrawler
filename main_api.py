import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from website_crawler import WebsiteCrawler
from typing import Dict, List, Optional

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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
