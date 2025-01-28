import asyncio

import bs4
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
DATE_FORMAT = '%Y-%m-%d'

class Scraper:
    def __init__(self, departure_date, return_date, origin_city, destination_city):
        self.departure_date = departure_date
        self.return_date = return_date
        self.origin_city = origin_city
        self.destination_city = destination_city
    def create_url(self) -> str:
        pass
    async def _get_page_source_after_button_click(self, url, button_selector) -> str:
        """
        Async get page source after expending all the flights using Playwright
        :param url: website url
        :param button_selector: the selector of the button
        :return: page source
        """
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            # Create page from context
            page = await context.new_page()

            # Set extra HTTP headers
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            })
            await page.goto(url)

            # Wait for and click the button
            if button_selector:
                await page.wait_for_selector(button_selector)
                await page.click(button_selector)

                # Random delay to simulate human-like behavior
                await asyncio.sleep(5)

                # Wait for page to load
                await page.wait_for_load_state('networkidle')

            # Get page source
            full_page_source = await page.content()

            await browser.close()
        return full_page_source
    def _get_flights(self, soup: bs4.BeautifulSoup, selector: str)-> list:
        items = soup.select(selector)
        pass #return [{} for item in items]
    async def scarpe_from_page(self, selector, button_selector) -> list:
        """
        Extract the data from the website
        :return:
        """
        # selectors for flight divs in the html page

        soup = BeautifulSoup(await self._get_page_source_after_button_click(self.create_url(), button_selector),'html.parser')

        return self._get_flights(soup, selector)
    def get_data(self):
        pass