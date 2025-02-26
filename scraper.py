import datetime

import bs4
from bs4 import BeautifulSoup
DATE_FORMAT = '%Y-%m-%d'

import asyncio
import json
import os.path
import string
import random

from playwright.async_api import Page, async_playwright

import pandas as pd

def generate_ucs(length=8) -> str:
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def update_session(name: str, new_data: dict) -> None:
    """Updates or creates a session file."""
    os.makedirs("./sessions", exist_ok=True)
    session_file_path = os.path.join("./sessions", f"{name}.json")
    try:
        with open(session_file_path, "w") as file:
            json.dump(new_data, file, indent=4)
        print(f"Session {name} successfully updated.")
    except Exception as e:
        print(f"Failed to update session {name}: {e}")


async def scroll_down(page: Page, button_selector: str, scroll_amount: int) -> None:
    try:
        await page.mouse.wheel(0,scroll_amount)
        await asyncio.sleep(random.uniform(1, 3))
        await page.click(button_selector, timeout=1000)
    except Exception as e:
        print(f"faild to press button: {e}")


def read_session(session_name: str) -> dict | None:
    """Reads a specific session file."""
    session_file_path = os.path.join("./sessions", f"{session_name}.json")
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


def read_cookies(cookies_name: str) -> dict | None:
    """Reads a specific session file."""
    cookies_file_path = os.path.join("./cookies", f"{cookies_name}-cookies.json")
    try:
        if not os.path.exists(cookies_file_path):
            print(
                f"Cookies file for {cookies_name} not found, not using cookies."
            )
            return None
        with open(cookies_file_path, "r") as file:
            content = file.read()
            if not content.strip():
                print(
                    f"Cookies file for {cookies_name} is empty, not using cookies."
                )
                return None
            return json.loads(content)
    except json.JSONDecodeError:
        print(
            f"Failed to decode cookies {cookies_name}, not using cookies."
        )
        return None
    except Exception as e:
        print(f"Unexpected error reading cookies {cookies_name}: {e}")
        return None

class Scraper:
    def __init__(self, departure_date, return_date, origin_city, destination_city):
        self.departure_date = departure_date
        self.return_date = return_date
        self.origin_city = origin_city
        self.destination_city = destination_city

    def __str__(self):
        return "Scraper"

    def __repr__(self):
        return f'{self.__str__()}({self.departure_date}, {self.return_date}, {self.origin_city}, {self.destination_city})'

    def create_url(self) -> str:
        pass


    async def _get_page_source(self, url, button_selector: list[str] =None, response_url=None, headers:dict = None) -> str:
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
        session = read_session(session_name=self.__str__())
        cookies = read_cookies(cookies_name=self.__str__())
        async with async_playwright() as pw:
            browser = await pw.firefox.launch(headless=False)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36', viewport={'width': 1920, 'height': 1080},
                                                storage_state=session)

            if headers:
                await context.set_extra_http_headers(headers)

            if cookies:
                await context.add_cookies(cookies)

            # Create page from context
            page = await context.new_page()

            # Write flights response to json file
            if response_url:
                page.on('response', _handle_response)

            # Simulate human
            await page.goto(url, timeout=100000)
            await page.wait_for_load_state('domcontentloaded')
            await page.mouse.move(random.randint(1, 200), random.randint(1, 400))
            await page.wait_for_timeout(2000)
            await page.keyboard.press("PageDown")
            await page.wait_for_load_state('domcontentloaded')

            # Wait for and click the button
            if button_selector:
                scroll_mount = 2000
                for button in  button_selector:
                    await scroll_down(page=page, button_selector=button, scroll_amount=scroll_mount)
                    scroll_mount +=2000

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
            update_session(new_data=await context.storage_state(), name=self.__str__())

            await browser.close()
        return full_page_source

    def _get_flights(self, soup: bs4.BeautifulSoup, selector: str)-> list:
        pass #return [{} for item in items]

    async def scarpe_from_page(self, selector, button_selector, response_url=None, headers=None) -> list:
        """
        Extract the data from the website
        """
        soup = BeautifulSoup(await self._get_page_source(url=self.create_url(), button_selector=button_selector, response_url=response_url, headers=headers),'html.parser')
        return self._get_flights(soup, selector)

    def get_data(self)-> pd.DataFrame:
        pass

    async def _add_params(self, ttt: int, los: int) -> pd.DataFrame:
        flights_results = await self.get_data()
        flights_results['ttt'], flights_results['los'], flights_results['snapshot_date'] = ttt, los, datetime.datetime.today().strftime(DATE_FORMAT)
        return flights_results

    async def write_data(self, ttt: int, los: int) -> str:
        data = await self._add_params(ttt=ttt, los=los)
        excel_name = self.__str__()+'.csv'
        file_lock = asyncio.Lock()
        async with file_lock:
            if os.path.exists(excel_name):
                data.to_csv(excel_name, header=False, mode='a')
                print(f"added data to  {excel_name} for {self.__repr__()}")
            else:
                data.to_csv(excel_name, index=False)
        return self.__repr__()


