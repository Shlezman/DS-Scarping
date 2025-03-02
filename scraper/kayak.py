import pandas as pd

import bs4
from scraper import Scraper, generate_ucs

CITY_CODES = {
    'LONDON': 'LON',
    'PARIS': 'PAR',
    'ROME': 'ROM',
}

DATE_FORMAT = '%Y-%m-%d'


class Kayak(Scraper):
    def __str__(self):
        return "Kayak"

    def create_url(self) -> str:
        return f"https://www.kayak.com/flights/{CITY_CODES[self.origin_city.upper()]}-{CITY_CODES[self.destination_city.upper()]}/{self.departure_date}/{self.return_date}?ucs={generate_ucs()}&sort=bestflight_a"

    def _get_flights(self, soup: bs4.BeautifulSoup, selector) -> list:
        items = []
        for div in soup.findAll('div', attrs={'class': selector}):
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

            'landing_hour': item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time').text.strip() if item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time') else None,

            'landing_airport': item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span').text.strip() if item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span') else None,

            'to_dest_company': item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(1) div.kI55-logo-date-container div.kI55-airline img')[
                'alt'].strip() if item.select_one(
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

            'return_landing_hour': item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time').text.strip() if item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.e2Sc-time') else None,

            'return_landing_airport': item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span').text.strip() if item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-flight-segments div.e2Sc.e2Sc-mod-destination div.c_cgF span') else None,
            'return_company': item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-logo-date-container div.kI55-airline img')[
                'alt'].strip() if item.select_one(
                'div.nrc6-wrapper div.nrc6-content-wrapper ol li:nth-child(2) div.kI55-logo-date-container div.kI55-airline img') else None,
            'price': item.select_one(
                'div.nrc6-price-section div.f8F1.f8F1-mod-frp-responsive div.f8F1-price-text').text.strip() if item.select_one(
                'div.nrc6-price-section div.f8F1.f8F1-mod-frp-responsive div.f8F1-price-text') else None,
            'is_direct': True if len(item.findAll("div", attrs={'class': "kI55-stop-dot"})) > 0 else False
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

        button_selector = ['#flight-results-list-wrapper > div.ULvh > div'] * 5
        selector = "Fxw9-result-item-container"
        data = await super().scarpe_from_page(selector=selector, button_selector=button_selector, headers=headers)
        return pd.DataFrame(data)
