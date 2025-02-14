import logging
import asyncio
import random
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Page
from urllib.parse import urlparse
import os
from util.llm_util import LLMUtil
from supabase import create_client
from typing import Dict, List, Optional
from config import config

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
load_dotenv()


class WebsiteCrawler:
    """网站爬虫类，用于抓取和处理网页内容"""

    def __init__(self):
        """初始化爬虫，设置LLM工具、数据库连接和用户代理"""
        self.llm = LLMUtil()
        self.supabase = create_client(
            config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY
        )
        # 设置多个User-Agent以模拟不同浏览器
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            # ... 其他用户代理 ...
        ]

    @staticmethod
    def get_name_from_url(url: str) -> Optional[str]:
        """从URL中提取唯一标识名称

        Args:
            url: 网页URL

        Returns:
            处理后的标识名称，如果URL为空则返回None
        """
        if not url:
            return None
        domain = urlparse(url).netloc
        path = urlparse(url).path
        if path and path.endswith("/"):
            path = path[:-1]
        return (domain.replace("www.", "") + path.replace("/", "-")).replace(".", "-")

    async def setup_page(self, browser) -> Page:
        """配置浏览器页面设置

        Args:
            browser: Playwright浏览器实例

        Returns:
            配置完成的Page对象
        """
        page = await browser.new_page()
        await page.set_extra_http_headers(
            {"User-Agent": random.choice(self.user_agents)}
        )
        await page.emulate_media(media="screen")
        await page.set_viewport_size({"width": 1920, "height": 1080})
        return page

    async def load_page(self, page: Page, url: str) -> None:
        """加载并等待页面完成

        Args:
            page: Playwright页面实例
            url: 要加载的URL
        """
        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_selector("body", timeout=10000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            await page.evaluate("window.scrollTo(0, 0)")
        except Exception as e:
            logger.info(f"页面加载超时，继续处理已获取的内容: {e}")

    def extract_page_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """提取页面元数据

        Args:
            soup: BeautifulSoup解析对象
            url: 页面URL

        Returns:
            包含标题、描述和名称的字典
        """
        title = soup.title.string.strip() if soup.title else ""
        description = self._get_description(soup)
        name = self.get_name_from_url(url)
        return {"title": title, "description": description, "name": name}

    def _get_description(self, soup: BeautifulSoup) -> str:
        """获取页面描述信息

        Args:
            soup: BeautifulSoup解析对象

        Returns:
            页面描述文本
        """
        meta_description = soup.find("meta", attrs={"name": "description"})
        if meta_description:
            return meta_description["content"].strip()

        og_description = soup.find("meta", attrs={"property": "og:description"})
        return og_description["content"].strip() if og_description else ""

    async def capture_and_upload_screenshot(self, page: Page, name: str) -> str:
        """捕获页面截图并上传到存储

        Args:
            page: Playwright页面实例
            name: 文件名

        Returns:
            上传后的文件键值
        """
        screenshot_key = f"{name}.png"
        screenshot_path = f"./screenshots/{screenshot_key}"
        await page.screenshot(path=screenshot_path)

        with open(screenshot_path, "rb") as f:
            self.supabase.storage.from_("ai-studio").upload(
                screenshot_key,
                f,
                file_options={"cache-control": "3600", "upsert": "true"},
            )
        return screenshot_key

    async def process_languages(
        self, title: str, description: str, detail: str, languages: List[str]
    ) -> List[Dict]:
        """处理多语言内容

        Args:
            title: 标题
            description: 描述
            detail: 详细内容
            languages: 需要处理的语言列表

        Returns:
            处理后的多语言内容列表
        """
        processed_languages = []

        if languages:
            for language in languages:
                logger.info(f"处理语言: {language}")
                processed_languages.append(
                    {
                        "language": language,
                        "title": self.llm.process_language(language, title),
                        "description": self.llm.process_language(language, description),
                        "detail": self.llm.process_language(language, detail),
                    }
                )
        return processed_languages

    async def crawl(self, url: str, tags, languages) -> Dict:
        """执行网页爬取的主要逻辑

        Args:
            url: 要爬取的URL

        Returns:
            包含所有处理结果的字典
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await self.setup_page(browser)

            logger.info(f"开始爬取页面: {url}")
            await self.load_page(page, url)

            # 解析页面内容
            soup = BeautifulSoup(await page.content(), "html.parser")
            metadata = self.extract_page_metadata(soup, url)

            # 处理截图
            screenshot_key = await self.capture_and_upload_screenshot(
                page, metadata["name"]
            )

            # 处理页面文本内容
            content = soup.get_text()
            detail = self.llm.process_detail(content)

            # 处理标签和多语言内容
            processed_tags = self.llm.process_tags(
                f"tag_list is: + {','.join(tags)} content is: {detail}"
            )

            processed_languages = await self.process_languages(
                metadata["title"], metadata["description"], detail, languages
            )

            await page.close()

            # 返回处理结果
            return {
                "name": metadata["name"],
                "url": url,
                "title": metadata["title"],
                "description": metadata["description"],
                "screenshot_key": screenshot_key,
                "tags": processed_tags,
                "languages": processed_languages,
            }


async def main():
    """主函数"""
    crawler = WebsiteCrawler()
    result = await crawler.crawl("https://suno4.cn/", [], [])
    logger.info(f"爬取完成: {result['url']}")
    return result


if __name__ == "__main__":
    asyncio.run(main())
