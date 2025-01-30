import asyncio
import json
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

    async def _get_page_source_after_button_click(self, url, button_selector, cookies_path=None, response_url=None, headers:dict = None) -> str:
        """
        Async get page source after expending all the flights using Playwright
        :param url: website url
        :param button_selector: the selector of the button
        :return: page source
        """
        async def _handle_response(response) -> None:
            if (response.url.startswith(response_url) or response.url.startswith(response_url)) and response.status == 200 and response.url.endswith('.json'):
                with open("flights.json", "w") as f:
                    flights = response.json()
                    json.dumps(flights, f, indent=4)

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
            )
            if headers:
                await context.set_extra_http_headers(headers)
            if cookies_path:
                with open(cookies_path, "r") as f:
                    cookies = json.loads(f.read())
                    await context.add_cookies(cookies)

            # Create page from context
            page = await context.new_page()

            # Write flights response to json file
            if response_url:
                page.on('response', _handle_response)

            await page.goto(url)
            await page.wait_for_load_state('domcontentloaded')
            await page.mouse.move(100, 400)
            await page.wait_for_timeout(2000)
            await page.keyboard.press("PageDown")
            await page.wait_for_load_state('networkidle')

            # Wait for and click the button
            if button_selector:
                await page.wait_for_selector(button_selector)
                await page.click(button_selector, timeout=5000)

                # Random delay to simulate human-like behavior
                await asyncio.sleep(5)

                # Wait for page to load
                await page.wait_for_load_state('networkidle')
                await page.keyboard.press("PageDown")
                await asyncio.sleep(0.9)
                await page.wait_for_load_state('networkidle')

            # Get page source
            full_page_source = await page.content()

            with open("cookies.json", "w") as f:
                f.write(json.dumps(await context.cookies()))
            await browser.close()

        return full_page_source
    def _get_flights(self, soup: bs4.BeautifulSoup, selector: str)-> list:
        items = soup.select(selector)
        pass #return [{} for item in items]
    async def scarpe_from_page(self, selector, button_selector, cookies_path=None, response_url=None, headers=None) -> list:
        """
        Extract the data from the website
        :return:
        """
        # selectors for flight divs in the html page
        if cookies_path:
            soup = BeautifulSoup(await self._get_page_source_after_button_click(self.create_url(), button_selector, cookies_path, response_url, headers),'html.parser')
        else:
            soup = BeautifulSoup(await self._get_page_source_after_button_click(self.create_url(), button_selector, response_url, headers),'html.parser')

        return self._get_flights(soup, selector)
    def get_data(self):
        pass