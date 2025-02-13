import bs4
from bs4 import BeautifulSoup
DATE_FORMAT = '%Y-%m-%d'

import asyncio
import json
import os.path
import random

from playwright.async_api import Page, async_playwright


class Scraper:
    def __init__(self, departure_date, return_date, origin_city, destination_city):
        self.departure_date = departure_date
        self.return_date = return_date
        self.origin_city = origin_city
        self.destination_city = destination_city

    def __str__(self):
        return "Scraper"

    def create_url(self) -> str:
        pass

    def __update_session(self, new_data: dict) -> None:
        """Updates or creates a session file."""
        os.makedirs("./sessions", exist_ok=True)
        session_file_path = os.path.join("./sessions", f"{self.__str__()}.json")
        try:
            with open(session_file_path, "w") as file:
                json.dump(new_data, file, indent=4)
            print(f"Session {self.__str__()} successfully updated.")
        except Exception as e:
            print(f"Failed to update session {self.__str__()}: {e}")

    async def __scroll_down(self, page: Page, counter: int, button_selector: str) -> int:
        try:
            await asyncio.sleep(random.uniform(1, 4))
            await page.click(button_selector, timeout=0)
        except Exception as e:
            print(f"Click failed: {str(e)}")

    def __read_session(self, session_name: str) -> dict | None:
        """Reads a specific session file."""
        session_file_path = os.path.join("./", f"{session_name}.json")
        try:
            if not os.path.exists(session_file_path):
                print(
                    f"Session file for {session_name} not found, not using session."
                )
                return None
            with open(session_file_path, "r") as file:
                content = file.read()
                if not content.strip():
                    print(
                        f"Session file for {session_name} is empty, not using session."
                    )
                    return None
                return json.loads(content)
        except json.JSONDecodeError:
            print(
                f"Failed to decode session {session_name}, not using session."
            )
            return None
        except Exception as e:
            print(f"Unexpected error reading session {session_name}: {e}")
            return None

    async def _get_page_source(self, url, button_selector: list[str] =None, cookies_path=None, response_url=None, headers:dict = None) -> str:
        """
        Async get page source after expending all the flights using Playwright
        :param url: website url
        :param button_selector: the selector of the button
        :return: page source
        # """
        async def _handle_response(response) -> None:
            if (response.url.startswith(response_url) or response.url.startswith(response_url)) and response.status == 200 and response.url.endswith('.json'):
                with open("flights.json", "w") as f:
                    flights = response.json()
                    json.dumps(flights, f, indent=4)

        async with async_playwright() as pw:
            browser = await pw.firefox.launch(headless=False)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36', viewport={'width': 1920, 'height': 1080},
                                                storage_state=self.__read_session(self.__str__()))

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

            # Simulate human
            await page.goto(url)
            await page.wait_for_load_state('domcontentloaded')
            await page.mouse.move(random.randint(1, 200), random.randint(1, 400))
            await page.wait_for_timeout(2000)
            await page.keyboard.press("PageDown")
            await page.wait_for_load_state('domcontentloaded')

            # Wait for and click the button
            if button_selector:
                for button in  button_selector:
                    await self.__scroll_down(page=page, counter=1, button_selector=button)

                # Random delay to simulate human-like behavior
                await asyncio.sleep(5)

                # Wait for page to load
                await page.wait_for_load_state('domcontentloaded')
                await page.keyboard.press("PageDown")
                await asyncio.sleep(0.9)
                await page.wait_for_load_state('domcontentloaded')

            # Get page source
            full_page_source = await page.content()

            with open(f"./cookies/{self.__str__()}-cookies.json", "w+") as f:
                f.write(json.dumps(await context.cookies()))

            # Save latest Session
            self.__update_session(await context.storage_state())

            await browser.close()
        return full_page_source
    def _get_flights(self, soup: bs4.BeautifulSoup, selector: str)-> list:
        pass #return [{} for item in items]
    async def scarpe_from_page(self, selector, button_selector, cookies_path=None, response_url=None, headers=None) -> list:
        """
        Extract the data from the website
        :return:
        """
        soup = BeautifulSoup(await self._get_page_source(url=self.create_url(), button_selector=button_selector, cookies_path=cookies_path, response_url=response_url, headers=headers),'html.parser')
        return self._get_flights(soup, selector)
    def get_data(self):
        pass