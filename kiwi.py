import asyncio

import pandas as pd
import string
import random

from datetime import datetime

import bs4

from scraper import Scraper

CITY_CODES = {
    'LONDON': 'london-united-kingdom',
    'PARIS': 'paris-france',
    'ROME': 'rome-italy',
}

DATE_FORMAT = '%Y-%m-%d'



class Kiwi(Scraper):
    def __str__(self):
        return "Kiwi-Scraper"
    def generate_ucs(self, length=8) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def create_url(self) -> str:

        url = f"https://www.kiwi.com/en/search/results/{CITY_CODES[self.origin_city.upper()]}/{CITY_CODES[self.destination_city.upper()]}/{self.departure_date}/{self.return_date}/"

        return url
    def _get_flights(self, soup: bs4.BeautifulSoup, selector)-> list:
        items = []
        for div in soup.findAll('div', attrs={'class': 'group/result-card relative cursor-pointer leading-normal'}):
            items.append(div)
        print(items[0])
        print(len(items))
        return [{
        'departure_hour': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc div.e2Sc-time').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc div.e2Sc-time') else None,

        'departure_airport': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc div.c_cgF span').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc div.c_cgF span') else None,

        'flight_length': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-center-container div.kI55-duration').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-center-container div.kI55-duration') else None,

        'arrive_hour': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time') else None,

        'arrive_airport': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span') else None,

        'company': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-logo-date-container div.kI55-airline img')['alt'].strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-logo-date-container div.kI55-airline img') else None,

        'return_departure_hour': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc div.e2Sc-time').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc div.e2Sc-time') else None,

        'return_departure_airport': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc div.c_cgF span').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc div.c_cgF span') else None,

        'return_flight_length': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-center-container div.kI55-duration').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-center-container div.kI55-duration') else None,

        'return_arrive_hour': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time') else None,

        'return_arrive_airport': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span').text.strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span') else None,

        'return_company': item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-logo-date-container div.kI55-airline img')['alt'].strip() if item.select_one(
            'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-logo-date-container div.kI55-airline img') else None,
    } for item in items]

    async def get_data(self) -> pd.DataFrame:
        """
        Extract the data from the website
        :return:
        """
        # selectors for flight divs in the html page
        headers = {
            "authority": "www.kiwi.com",
            "method": "GET",
            "path": self.create_url().replace("https://www.kiwi.com", ""),
            "scheme": "https",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "referer": self.create_url(),
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
        }
        button_selectors = ['#cookies_accept'] + ['#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(2) > div > div > button']*10
        selector = '#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(2) > div > div > div > div:nth-child(1)'
        #"#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(3) > div > div > div"
        data =  await super().scarpe_from_page(selector=selector,button_selector=button_selectors, headers=headers, response_url=None)
        return pd.DataFrame(data)


if __name__ == "__main__":
    kayak = Kiwi(departure_date='2025-02-30', return_date='2025-03-12', origin_city="london", destination_city="paris")
    print(kayak.create_url())
    get = asyncio.run(kayak.get_data())
    # print(get.info())
    # print(get.head())