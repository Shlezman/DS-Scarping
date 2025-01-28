import asyncio
import base64

import bs4
import pandas as pd
from scraper import Scraper

CITY_CODES = {
    'LONDON': '/m/04jpl',
    'PARIS': '/m/05qtj',
    'ROME': '/m/06c62',
}

DATE_FORMAT = '%Y-%m-%d'


class GoogleFlights(Scraper):
    def _get_flights(self, soup: bs4.BeautifulSoup, selector: str) -> list:
        """
        Extract the exact data from the full html file
        :param soup: bs4.BeautifulSoup google flights html based
        :param selector: the general CSS selector for flight box
        :return:
        """
        items = soup.select(selector)
        return [{
            'start_hour': item.select_one(
                'div.Ir0Voe div.zxVSec span > span:nth-child(1) span span span').text.removesuffix(
                "\\u202fAM") if item.select_one(
                'div.Ir0Voe div.zxVSec span > span:nth-child(1) span span span') else None,

            'arrive_hour': item.select_one(
                'div.Ir0Voe div.zxVSec span > span:nth-child(2) span span span').text.removesuffix(
                "\\u202fAM") if item.select_one(
                'div.Ir0Voe div.zxVSec span > span:nth-child(2) span span span') else None,

            'origin_airport': item.select_one(
                'div.Ak5kof span > div:nth-child(1) span span span').text if item.select_one(
                'div.Ak5kof span > div:nth-child(1) span span span') else None,

            'dest_airport': item.select_one(
                'div.Ak5kof span > div:nth-child(2) span span span').text if item.select_one(
                'div.Ak5kof span > div:nth-child(2) span span span') else None,

            'is_direct': not bool(item.select_one(
                'div.yR1fYc div.OgQvJf.nKlB3b div.KhL0De div.BbR8Ec div.sSHqwe.tPgKwe.ogfYpf span span span')),

            'middle_airport': item.select_one(
                'div.yR1fYc div.OgQvJf.nKlB3b div.KhL0De div.BbR8Ec div.sSHqwe.tPgKwe.ogfYpf span span span').get_text() if item.select_one(
                'div.yR1fYc div.OgQvJf.nKlB3b div.KhL0De div.BbR8Ec div.sSHqwe.tPgKwe.ogfYpf span span span') else None,

            'co2_kg': item.select_one('div.y0NSEe div.O7CXue div').text if item.select_one(
                'div.y0NSEe div.O7CXue div') else None,

            'price': item.select_one('div.U3gSDe div.YMlIz span').text if item.select_one(
                'div.U3gSDe div.YMlIz span') else None,

            'company': item.select_one('div.Ir0Voe div.sSHqwe span').text if item.select_one(
                'div.Ir0Voe div.sSHqwe span') else None,

            'handbag': bool(item.select_one(
                'div.yR1fYc div.OgQvJf.nKlB3b div.KhL0De div.U3gSDe div.BVAVmf.I11szd.POX3ye div.MEDXEe span span span'))
        } for item in items]

    def create_url(self) -> str:
        """
        Creates a Google Flights search URL

        Args:
            departure_date: Date string in format 'YYYY-MM-DD'
            return_date: Date string in format 'YYYY-MM-DD'
            origin_code: Google's location code (e.g., '/m/04jpl' for London)
            destination_code: Google's location code (e.g., '/m/05qtj' for Paris)

        Returns:
            Complete Google Flights search URL
        """
        # Construct the binary string following Google's pattern
        origin_code = CITY_CODES[self.origin_city.upper()]
        destination_code = CITY_CODES[self.destination_city.upper()]
        binary_data = (
                b'\x08\x1c\x10\x02\x1a\x28\x12\x0a' +
                self.departure_date.encode() +
                b'j\x0c\x08\x03\x12\x08' +
                origin_code.encode() +
                b'r\x0c\x08\x03\x12\x08' +
                destination_code.encode() +
                b'\x1a\x28\x12\x0a' +
                self.return_date.encode() +
                b'j\x0c\x08\x03\x12\x08' +
                destination_code.encode() +
                b'r\x0c\x08\x03\x12\x08' +
                origin_code.encode() +
                b'@\x01H\x01p\x01\x82\x01\x0b\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x98\x01\x01'
        )

        # Encode to base64
        encoded_params = base64.b64encode(binary_data).decode('utf-8')

        # Create the full URL
        base_url = "https://www.google.com/travel/flights/search?tfs="
        return (base_url + encoded_params).replace("///////////", "___________")

    async def get_data(self) -> pd.DataFrame:
        """
        Extract the data from the website
        :return:
        """
        # selectors for flight divs in the html page
        pushed_flights = 'c-wiz.zQTmif div.cKvRXe div.PSZ8D.EA71Tc div.FXkZv div.XwbuFf div div:nth-child(2) div:nth-child(1) ul li'
        other_flights = 'c-wiz.zQTmif div.cKvRXe div.PSZ8D.EA71Tc div.FXkZv div.XwbuFf div div:nth-child(2) div:nth-child(4) ul li'
        button_selector = 'c-wiz.zQTmif.SSPGKf > div > div:nth-child(2) > c-wiz > div.cKvRXe > c-wiz > div.PSZ8D.EA71Tc > div.FXkZv > div.XwbuFf > div > div:nth-child(2) > div:nth-child(4) > ul > li.ZVk93d > div > span.XsapA > div > button'
        data =  await super().scarpe_from_page(selector=pushed_flights,button_selector=button_selector) + await super().scarpe_from_page(selector=other_flights,button_selector=button_selector)
        return pd.DataFrame(data)

# # Vlidate
# if __name__ == "__main__":
#     print(GoogleFlights(departure_date='2025-02-25', return_date='2025-02-27', origin_city="paris", destination_city="london").create_url())
#     get = asyncio.run(GoogleFlights(departure_date='2025-02-25', return_date='2025-02-27', origin_city="paris", destination_city="london").get_data())
#     print(get.info())
#     print(get.head())