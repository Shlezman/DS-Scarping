import asyncio

import pandas as pd
import string
import random

import bs4

from scraper import Scraper,generate_ucs

CITY_CODES = {
    'LONDON': 'LON',
    'PARIS': 'PAR',
    'ROME': 'ROM',
}

DATE_FORMAT = '%Y-%m-%d'



class Momondo(Scraper):
    def __str__(self):
        return "Momondo-Scraper"
    def generate_ucs(self, length=8) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def create_url(self) -> str:
        url = f"https://www.momondo.com/flight-search/{CITY_CODES[self.origin_city.upper()]}-{CITY_CODES[self.destination_city.upper()]}/{self.departure_date}/{self.return_date}?ucs={generate_ucs(6)}&sort=bestflight_a"

        return url

    def _get_flights(self, soup: bs4.BeautifulSoup, selector)-> list:
        items = [div for div in soup.findAll('div', attrs={'class': 'Fxw9-result-item-container'})] #flight-results-list-wrapper > div:nth-child(4) > div.Fxw9 > div > div
        print(len(items))
        print(items[4])

        return [{
            'departure_hour': (dep_time := item.select_one('div.e2Sc-time')) and dep_time.text.strip(),
            'departure_airport': (dep_air := item.select_one('div.c_cgF span > span')) and dep_air.text.strip(),
            'flight_length': (flight_len := item.select_one('div.kI55-duration')) and flight_len.text.strip(),
            'arrive_hour': (arr_time := item.select_one(
                'div.e2Sc-mod-destination > div.e2Sc-time')) and arr_time.text.strip(),
            'arrive_airport': (arr_air := item.select_one(
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
            'return_arrive_hour': (ret_arr_time := item.select_one(
                'li:nth-child(2) div.e2Sc-mod-destination > div.e2Sc-time')) and ret_arr_time.text.strip(),
            'return_arrive_airport': (ret_arr_air := item.select_one(
                'li:nth-child(2) div.e2Sc-mod-destination > div.c_cgF span > span')) and ret_arr_air.text.strip(),

            # Use the same 'company' selector and get the second part if available
            'return_company': (
                (company := item.select_one(
                    'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive > div > div:nth-child(2) > div > div > div'))
                and company.text.strip().split('/')[-1]
            ),
        } for item in items]

        # return [{
        #     'departure_hour': item.select_one( #flight-results-list-wrapper > div:nth-child(5) > div.Fxw9 > div > div:nth-child(2) > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive > div > div.nrc6-wrapper > div.nrc6-inner > div.nrc6-content-wrapper > div > div > div > ol > li:nth-child(1) > div > div > div > div > div:nth-child(2) > div.e2Sc-time
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div:nth-child(2) > div.e2Sc-time').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div:nth-child(2) > div.e2Sc-time') else None,
        #
        #     'departure_airport': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div:nth-child(2) > div.c_cgF.c_cgF-mod-variant-default > span > span').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div:nth-child(2) > div.c_cgF.c_cgF-mod-variant-default > span > span') else None,
        #
        #     'flight_length': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div.kI55-center-container > div.kI55-duration').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div.kI55-center-container > div.kI55-duration') else None,
        #
        #     'arrive_hour': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div.e2Sc.e2Sc-mod-destination > div.e2Sc-time').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div.e2Sc.e2Sc-mod-destination > div.e2Sc-time') else None,
        #
        #     'arrive_airport': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div.e2Sc.e2Sc-mod-destination > div.c_cgF.c_cgF-mod-variant-default > span > span').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(1) > div > div > div > div > div.e2Sc.e2Sc-mod-destination > div.c_cgF.c_cgF-mod-variant-default > span > span') else None,
        #
        #     'company': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.OSnN > div.OSnN-banner > figure > img').get(
        #         'alt') if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.OSnN > div.OSnN-banner > figure > img') else None,
        #
        #     'return_departure_hour': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div:nth-child(2) > div.e2Sc-time').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div:nth-child(2) > div.e2Sc-time') else None,
        #
        #     'return_departure_airport': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div:nth-child(2) > div.e2Sc-time').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div:nth-child(2) > div.e2Sc-time') else None,
        #
        #     'return_flight_length': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div.kI55-center-container > div.kI55-duration').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div.kI55-center-container > div.kI55-duration') else None,
        #
        #     'return_arrive_hour': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div.e2Sc.e2Sc-mod-destination > div.e2Sc-time').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div.e2Sc.e2Sc-mod-destination > div.e2Sc-time') else None,
        #
        #     'return_arrive_airport': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div:nth-child(2) > div.c_cgF.c_cgF-mod-variant-default > span > span').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-content-wrapper > div > div.nrc6-main > div > ol > li:nth-child(2) > div > div > div > div > div:nth-child(2) > div.c_cgF.c_cgF-mod-variant-default > span > span') else None,
        #
        #     'return_company': item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-price-section > div > div > div > div:nth-child(1) > div > div.M_JD-provider-display-label.M_JD-mod-omnipresent > div').text.strip() if item.select_one(
        #         'div > div.nrc6.nrc6-mod-pres-default.nrc6-mod-frp-responsive.nrc6-mod-sponsored-result > div > div.nrc6-wrapper > div > div.nrc6-price-section > div > div > div > div:nth-child(1) > div > div.M_JD-provider-display-label.M_JD-mod-omnipresent > div') else None,
        #     # 'is_direct': True if item.select_one(
        #     #     '') == 'Direct' else False,
        # } for item in items]

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
        button_selectors = [f'#flight-results-list-wrapper > div.ULvh > div']*10
        selector = '#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(2) > div > div > div > div:nth-child(1)'
        data =  await super().scarpe_from_page(selector=selector,button_selector=button_selectors, headers=headers)
        return pd.DataFrame(data)

# Example
# if __name__ == "__main__":
#     momondo = Momondo(departure_date='2025-03-22', return_date='2025-04-12', origin_city="paris", destination_city="london")
#     print(momondo.create_url())
#     get = asyncio.run(momondo.get_data())
#     print(get.info())
#     print(get.head())
#     get.to_csv('test.csv', index_label=False)