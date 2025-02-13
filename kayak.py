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
    def __str__(self):
        return "Kayak-Scraper"

    def generate_ucs(self, length=8) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def create_url(self) -> str:
        return f"https://www.kayak.com/flights/{CITY_CODES[self.origin_city.upper()]}-{CITY_CODES[self.destination_city.upper()]}/{self.departure_date}/{self.return_date}?ucs={self.generate_ucs()}&sort=bestflight_a"

    def _get_flights(self, soup: bs4.BeautifulSoup, selector)-> list:
        items = []
        for div in soup.findAll('div', attrs={'class': 'Fxw9-result-item-container'}):
            items.append(div)
        print(items[0])
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
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=0, i",
    "referer": self.create_url(),
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
}

        button_selector = ['#flight-results-list-wrapper > div.ULvh > div']*2
        selector = "div > div:nth-child(3) > div.Fxw9 > div > div:nth-child(1)" #listWrapper > div > div:nth-child(3) > div.Fxw9 > div
        data =  await super().scarpe_from_page(selector=selector,button_selector=button_selector, cookies_path="./cookies/Kayak-Scraper-cookies.json", response_url='https://www.kayak.com/s/horizon/flights/results', headers=headers)
        return pd.DataFrame(data)


# Example:
# if __name__ == "__main__":
#     kayak = Kayak(departure_date='2025-02-26', return_date='2025-03-24', origin_city="paris", destination_city="london")
#     print(kayak.create_url())
#     get = asyncio.run(kayak.get_data())
#     print(get.info())
#     print(get.head())