import asyncio

import pandas as pd
import string
import random

import bs4
from scraper import Scraper

CITY_CODES = {
    'LONDON': 'LON',
    'PARIS': 'PAR',
    'ROME': 'ROM',
}

DATE_FORMAT = '%Y-%m-%d'



class Kayak(Scraper):
    def generate_ucs(self, length=8) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def create_url(self) -> str:
        return f"https://www.il.kayak.com/flights/{CITY_CODES[self.origin_city.upper()]}-{CITY_CODES[self.destination_city.upper()]}/{self.departure_date}/{self.return_date}?ucs={self.generate_ucs()}&sort=bestflight_a"

    def get_flights(self, soup: bs4.BeautifulSoup, selector)-> list:
        items = soup.select(selector)
        return [{
            'start_hour': item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.VY2U > div.vmXl.vmXl-mod-variant-large > span:nth-child(1)').text if item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.VY2U > div.vmXl.vmXl-mod-variant-large > span:nth-child(1)') else None,

            'return_flight_departure_hour': item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div.VY2U > div.vmXl.vmXl-mod-variant-large > span:nth-child(1)').text if item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div.VY2U > div.vmXl.vmXl-mod-variant-large > span:nth-child(1)') else None,

            'haloch_origin_airport': item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(1) > span > span:nth-child(1)').text if item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(1) > span > span:nth-child(1)') else None,

            'haloch_dest_airport': item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(3) > span > span:nth-child(1)').text if item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(3) > span > span:nth-child(1)') else None,
            'return_dest_airport': item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(3) > span > span:nth-child(1)').text if item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(3) > span > span:nth-child(1)') else None,
            'return_origin_airport': item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(1) > span > span:nth-child(1)').text if item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div.VY2U > div.c_cgF.c_cgF-mod-variant-full-airport > div > div:nth-child(1) > span > span:nth-child(1)') else None,

            'is_direct': bool(item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.JWEO > div.vmXl.vmXl-mod-variant-default > span').text == 'nonstop'),

            'middle_airport': item.select_one(
                ' div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.JWEO > div.c_cgF.c_cgF-mod-variant-full-airport > span > span').get_text() if item.select_one(
                ' > div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div.JWEO > div.c_cgF.c_cgF-mod-variant-full-airport > span > span') else None,

            'price': item.select_one(' > div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-price-section > div > div.Oihj-bottom-booking > div > div.M_JD-large-display > div.oVHK > a > div > div > div > div').text if item.select_one(
                ' > div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-price-section > div > div.Oihj-bottom-booking > div > div.M_JD-large-display > div.oVHK > a > div > div > div > div') else None,

            'company': item.select_one(' > div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-default-footer > div > div > div.J0g6-operator-text').text if item.select_one(
                ' > div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-content-section > div.nrc6-default-footer > div > div > div.J0g6-operator-text') else None,

            'handbag': bool(item.select_one(
                'div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-price-section > div > div.Oihj-top-fees > div > div.ac27-fee-box.ac27-mod-unknown > div:nth-child(2)')),
            'luggage': bool(item.select_one('div.nrc6.nrc6-mod-pres-default > div > div > div > div.nrc6-price-section > div > div.Oihj-top-fees > div > div:nth-child(2) > div:nth-child(2)'))
        } for item in items]

    async def get_data(self) -> pd.DataFrame:
        """
        Extract the data from the website
        :return:
        """
        # selectors for flight divs in the html page
        button_selector = None
        selector = "div > div:nth-child(3) > div.Fxw9 > div > div"
        data =  await super().scarpe_from_page(selector=selector,button_selector=button_selector)
        return pd.DataFrame(data)

if __name__ == "__main__":
    kayak = Kayak(departure_date='2025-02-25', return_date='2025-02-29', origin_city="rome", destination_city="paris")
    get = asyncio.run(kayak.get_data())
    print(kayak.create_url())
    print(get.info())