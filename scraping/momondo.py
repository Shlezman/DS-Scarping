import asyncio
import string
import random

import pandas as pd

import bs4

from scraper import Scraper, generate_ucs

CITY_CODES = {
    'LONDON': 'LON',
    'PARIS': 'PAR',
    'ROME': 'ROM',
}

DATE_FORMAT = '%Y-%m-%d'


class Momondo(Scraper):
    def __str__(self):
        return "Momondo"

    def generate_ucs(self, length=8) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def create_url(self) -> str:
        url = f"https://www.momondo.com/flight-search/{CITY_CODES[self.origin_city.upper()]}-{CITY_CODES[self.destination_city.upper()]}/{self.departure_date}/{self.return_date}?ucs={generate_ucs(6)}&sort=bestflight_a"

        return url

    def _get_flights(self, soup: bs4.BeautifulSoup, selector) -> list:
        items = [div for div in soup.findAll('div', attrs={'class': 'Fxw9-result-item-container'})]
        print(items[4])

        return [{
            'departure_hour': (dep_time := item.select_one('div.e2Sc-time')) and dep_time.text.strip(),
            'departure_airport': (dep_air := item.select_one('div.c_cgF span > span')) and dep_air.text.strip(),
            'flight_length': (flight_len := item.select_one('div.kI55-duration')) and flight_len.text.strip(),
            'landing_hour': (arr_time := item.select_one(
                'div.e2Sc-mod-destination > div.e2Sc-time')) and arr_time.text.strip(),
            'landing_airport': (arr_air := item.select_one(
                'div.e2Sc-mod-destination > div.c_cgF span > span')) and arr_air.text.strip(),

            'company': (company := item.select_one(
                'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive > div > div:nth-child(2) > div > div > div')) and
                       company.text.strip().split('/')[0],

            'return_departure_hour': (ret_dep_time := item.select_one(
                'li:nth-child(2) div.e2Sc-time')) and ret_dep_time.text.strip(),
            'return_departure_airport': (ret_dep_air := item.select_one(
                'li:nth-child(2) div.c_cgF span > span')) and ret_dep_air.text.strip(),
            'return_flight_length': (ret_flight_len := item.select_one(
                'li:nth-child(2) div.kI55-duration')) and ret_flight_len.text.strip(),
            'return_landing_hour': (ret_arr_time := item.select_one(
                'li:nth-child(2) div.e2Sc-mod-destination > div.e2Sc-time')) and ret_arr_time.text.strip(),
            'return_landing_airport': (ret_arr_air := item.select_one(
                'li:nth-child(2) div.e2Sc-mod-destination > div.c_cgF span > span')) and ret_arr_air.text.strip(),

            # Use the same 'company' selector and get the second part if available
            'return_company': (
                    (company := item.select_one(
                        'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive > div > div:nth-child(2) > div > div > div'))
                    and company.text.strip().split('/')[-1]
            ),
            'price': (price := item.select_one(
                'div.nrc6-price-section div.f8F1 > div > div > div')) and price.text.strip()
        } for item in items]

    async def get_data(self) -> pd.DataFrame:
        """
        Extract the data from the website
        :return:
        """
        # selectors for flight divs in the html page
        headers = {
            ":authority": "www.momondo.com",
            ":method": "GET",
            ":path": self.create_url().replace("https://www.momondo.com", ""),
            ":scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "referer": "https://www.google.com/",
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
        button_selectors = [f'#flight-results-list-wrapper > div.ULvh > div'] * 10
        selector = '#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(2) > div > div > div > div:nth-child(1)'
        data = await super().scarpe_from_page(selector=selector, button_selector=button_selectors, headers=headers)
        return pd.DataFrame(data)


# Example
if __name__ == "__main__":
    momondo = Momondo(departure_date='2025-03-22', return_date='2025-04-12', origin_city="paris",
                      destination_city="london")
    print(momondo.create_url())
    get = asyncio.run(momondo.get_data())
    print(get.info())
    print(get.head())
#     get.to_csv('test.csv', index_label=False)
