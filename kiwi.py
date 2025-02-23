import asyncio

import pandas as pd
import string
import random

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

        url = f"https://www.kiwi.com/en/search/results/{CITY_CODES[self.origin_city.upper()]}/{CITY_CODES[self.destination_city.upper()]}/{self.departure_date}/{self.return_date}"

        return url
    def _get_flights(self, soup: bs4.BeautifulSoup, selector)-> list:
        items = [div for div in soup.findAll('div', attrs={'class': 'group/result-card relative cursor-pointer leading-normal'})]
        print(items[0])
        print(len(items))
        return [{
            'departure_hour': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(1) > div > time').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(1) > div > time') else None,

            'departure_airport': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.w-full.items-center.grid.grid-cols-\\[1fr_auto_1fr\\].gap-400.pb-100.pt-100 > div:nth-child(1) > span > div > div > div > div').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.w-full.items-center.grid.grid-cols-\\[1fr_auto_1fr\\].gap-400.pb-100.pt-100 > div:nth-child(1) > span > div > div > div > div') else None,

            'flight_length': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div.flex.me-100 > div > div > time').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div.flex.me-100 > div > div > time') else None,

            'arrive_hour': item.select_one(
                'div > div > div.relative.lm\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\/result-card\:shadow-result-card-active.lm\:w-\[65\%\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(5) > div > time').text.strip() if item.select_one(
                'div > div > div.relative.lm\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\/result-card\:shadow-result-card-active.lm\:w-\[65\%\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(5) > div > time') else None,

            'arrive_airport': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.w-full.items-center.grid.grid-cols-\\[1fr_auto_1fr\\].gap-400.pb-100.pt-100 > div.text-end > span > div > div.w-full.whitespace-nowrap.lm\\:flex.flex > div > div').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.w-full.items-center.grid.grid-cols-\\[1fr_auto_1fr\\].gap-400.pb-100.pt-100 > div.text-end > span > div > div.w-full.whitespace-nowrap.lm\\:flex.flex > div > div') else None,
            'is_direct': True if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.w-full.items-center.grid.grid-cols-\\[1fr_auto_1fr\\].gap-400.pb-100.pt-100 > p') == 'Direct' else False,

            'company': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div:nth-child(2) > div > span > div > img').get(
                'title') if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(1) > div.px-400.py-300.de\\:p-300 > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div:nth-child(2) > div > span > div > img') else None,

            'return_departure_hour': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(1) > div > time').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(1) > div > time') else None,

            'return_departure_airport': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(5) > div > time').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(5) > div > time') else None,

            'return_flight_length': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div.flex.me-100 > div > div > time').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div.flex.me-100 > div > div > time') else None,

            'return_arrive_hour': item.select_one(
                'div > div > div.relative.lm\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\/result-card\:shadow-result-card-active.lm\:w-\[65\%\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(5) > div > time').text.strip() if item.select_one(
                'div > div > div.relative.lm\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\/result-card\:shadow-result-card-active.lm\:w-\[65\%\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > span:nth-child(5) > div > time') else None,

            'return_arrive_airport': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.w-full.items-center.grid.grid-cols-\\[1fr_auto_1fr\\].gap-400.pb-100.pt-100 > div:nth-child(1) > span > div > div.w-full.whitespace-nowrap.lm\\:flex.flex > div > div').text.strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.w-full.items-center.grid.grid-cols-\\[1fr_auto_1fr\\].gap-400.pb-100.pt-100 > div:nth-child(1) > span > div > div.w-full.whitespace-nowrap.lm\\:flex.flex > div > div') else None,

            'return_company': item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div:nth-child(2) > div > span > div > img').get(
                'title').strip() if item.select_one(
                'div > div > div.relative.lm\\:flex > div.relative.overflow-hidden.rounded-200.bg-card.shadow-result-card.transition-shadow.duration-fast.group-hover\\/result-card\\:shadow-result-card-active.lm\\:w-\\[65\\%\\] > div.relative.z-default.flex.h-full.flex-col > div:nth-child(2) > div > div.flex.flex-col > div.flex.w-full.items-center.justify-between > div.flex.flex-wrap.items-center.justify-center.gap-y-100 > div:nth-child(2) > div > span > div > img') else None,
            'price': item.select_one(
                'body > div > div > div.relative.lm\:flex > div.relative.flex.flex-col.overflow-hidden.rounded-200.border-0.border-t-card.border-dashed.bg-card.px-400.py-300.shadow-result-card.transition-shadow.duration-fast.group-hover\/result-card\:shadow-result-card-active.lm\:flex-1.lm\:border-0.lm\:border-s-card.lm\:pb-300.lm\:pe-300.lm\:pt-400 > div.lm\:mb-300.lm\:flex.lm\:flex-auto.lm\:flex-col.lm\:justify-center.lm\:text-center > div:nth-child(1) > div > div > span').text.strip() if item.select_one(
                'body > div > div > div.relative.lm\:flex > div.relative.flex.flex-col.overflow-hidden.rounded-200.border-0.border-t-card.border-dashed.bg-card.px-400.py-300.shadow-result-card.transition-shadow.duration-fast.group-hover\/result-card\:shadow-result-card-active.lm\:flex-1.lm\:border-0.lm\:border-s-card.lm\:pb-300.lm\:pe-300.lm\:pt-400 > div.lm\:mb-300.lm\:flex.lm\:flex-auto.lm\:flex-col.lm\:justify-center.lm\:text-center > div:nth-child(1) > div > div > span') else None,
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
        button_selectors = ['#cookies_accept'] + [f'#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(3) > div > div > button']*20
        selector = '#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(2) > div > div > div > div:nth-child(1)'
        #"#react-view > div.flex.min-h-screen.flex-col > div.grow.bg-cloud-light > div > div > div > div > div > div.min-w-0.flex-grow.p-400.de\\:p-0.de\\:pb-600.de\\:ps-600.de\\:pt-600 > div > div > div:nth-child(3) > div > div > div"
        data =  await super().scarpe_from_page(selector=selector,button_selector=button_selectors, headers=headers)
        return pd.DataFrame(data)

# Example
if __name__ == "__main__":
    Kiwi = Kiwi(departure_date='2025-03-22', return_date='2025-04-12', origin_city="paris", destination_city="london")
    print(Kiwi.create_url())
    get = asyncio.run(Kiwi.get_data())
    print(get.info())
    print(get.head())