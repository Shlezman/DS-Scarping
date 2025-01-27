import asyncio

import bs4
from bs4 import BeautifulSoup
import pandas as pd
from playwright.async_api import async_playwright

CITY_CODES = {
    'LONDON': '/m/04jpl',
    'PARIS': '/m/05qtj',
    'ROME': '/m/06c62',
}

DATE_FORMAT = '%Y-%m-%d'

class Scraper:
    def __init__(self, departure_date, return_date, origin_city, destination_city):
        self.departure_date = departure_date
        self.return_date = return_date
        self.origin_city = origin_city
        self.destination_city = destination_city
    def get_flights(self, soup: bs4.BeautifulSoup, selector: str)-> list:
        items = soup.select(selector)
        pass #return [{} for item in items]
    async def get_page_source_after_button_click(self, url, button_selector) -> str:
        """
        Async get page source after expending all the flights using Playwright
        :param url: google-flights url
        :param button_selector: the selector of the button
        :return: page source
        """
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()
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
    def create_url(self) -> str:
        pass
    async def scarpe_from_page(self, selector, button_selector) -> list:
        """
        Extract the data from the website
        :return:
        """
        # selectors for flight divs in the html page

        soup = BeautifulSoup(await self.get_page_source_after_button_click(self.create_url(), button_selector),'html.parser')

        return self.get_flights(soup, selector)