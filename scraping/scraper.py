import datetime
import asyncio
import json
import os.path
import string
import random
import re

import bs4
from bs4 import BeautifulSoup
from playwright.async_api import Page, async_playwright

import pandas as pd

DATE_FORMAT = '%Y-%m-%d'

VIEWPORTS = [
    {'width': 1920, 'height': 1080},
    {'width': 1366, 'height': 768},
    {'width': 1440, 'height': 900},
    {'width': 1536, 'height': 864},
    {'width': 1600, 'height': 900},
    {'width': 1280, 'height': 720},
    {'width': 2560, 'height': 1440},
    {'width': 3840, 'height': 2160},
    {'width': 7680, 'height': 4320},

    # Tablets
    {'width': 1024, 'height': 1366},
    {'width': 1366, 'height': 1024},
    {'width': 800, 'height': 1280},
    {'width': 1280, 'height': 800},

    # Smartphones
    {'width': 375, 'height': 812},
    {'width': 414, 'height': 896},
    {'width': 390, 'height': 844},
    {'width': 430, 'height': 932},
    {'width': 320, 'height': 568},
    {'width': 360, 'height': 640},
    {'width': 412, 'height': 915},
    {'width': 412, 'height': 869},
    {'width': 480, 'height': 854},
]


def generate_ucs(length=8) -> str:
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def update_session(name: str, new_data: dict) -> None:
    """Updates or creates a session file."""
    os.makedirs("sessions", exist_ok=True)
    session_file_path = os.path.join("sessions", f"{name}.json")
    try:
        with open(session_file_path, "w") as file:
            json.dump(new_data, file, indent=4)
        print(f"Session {name} successfully updated.")
    except Exception as e:
        print(f"Failed to update session {name}: {e}")


async def perform_random_mouse_movements(page: Page, min_actions: int = 5, max_actions: int = 15,
                                         min_pause: float = 0.5, max_pause: float = 3.0):
    """
    Performs random mouse movements and scrolling actions on a Playwright page
    without any clicking.

    Args:
        page: Playwright Page object
        min_actions: Minimum number of mouse actions to perform
        max_actions: Maximum number of mouse actions to perform
        min_pause: Minimum pause between actions (seconds)
        max_pause: Maximum pause between actions (seconds)
    """
    # Get page dimensions
    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            scrollHeight: document.documentElement.scrollHeight
        }
    }''')

    viewport_width = dimensions['width']
    viewport_height = dimensions['height']
    scroll_height = dimensions['scrollHeight']

    # Determine number of actions to perform
    num_actions = random.randint(min_actions, max_actions)

    for _ in range(num_actions):
        # Choose a random action (no clicks)
        action = random.choice(['move', 'hover_element', 'scroll_down', 'scroll_up', 'pause'])

        # Random pause between actions
        await asyncio.sleep(random.uniform(min_pause, max_pause))

        if action == 'move':
            # Move to random position
            x = random.randint(0, viewport_width)
            y = random.randint(0, viewport_height)
            await page.mouse.move(x, y)

        elif action == 'hover_element':
            # Find a random clickable element and hover over it
            clickable_elements = await page.evaluate('''() => {
                const elements = Array.from(document.querySelectorAll('a, button, [role="button"], input[type="submit"]'));
                return elements.map(el => {
                    const rect = el.getBoundingClientRect();
                    return {
                        x: rect.left + rect.width / 2,
                        y: rect.top + rect.height / 2,
                        width: rect.width,
                        height: rect.height,
                        visible: rect.width > 0 && rect.height > 0 &&
                                rect.top >= 0 && rect.left >= 0 &&
                                rect.bottom <= window.innerHeight &&
                                rect.right <= window.innerWidth
                    };
                }).filter(el => el.visible);
            }''')

            if clickable_elements:
                element = random.choice(clickable_elements)
                await page.mouse.move(element['x'], element['y'])

        elif action == 'scroll_down':
            # Random scroll down amount (between 100 and 800 pixels)
            scroll_amount = random.randint(100, 800)
            current_scroll = await page.evaluate('window.scrollY')

            # Ensure we don't scroll past the bottom
            max_scroll = scroll_height - viewport_height
            if current_scroll < max_scroll:
                # Use smooth scrolling
                await page.evaluate(f'window.scrollBy({{ top: {scroll_amount}, behavior: "smooth" }})')

        elif action == 'scroll_up':
            # Random scroll up amount (between 100 and 400 pixels)
            if await page.evaluate('window.scrollY') > 0:
                scroll_amount = random.randint(100, 400)
                await page.evaluate(f'window.scrollBy({{ top: -{scroll_amount}, behavior: "smooth" }})')

        elif action == 'pause':
            # Just pause for a random time (already handled above)
            pass

    # Final random pause
    await asyncio.sleep(random.uniform(min_pause, max_pause))


async def scroll_down(page: Page, button_selector: str, scroll_amount: int) -> None:
    try:
        await page.mouse.wheel(0, scroll_amount)
        await asyncio.sleep(random.uniform(1, 3))
        await page.click(button_selector, timeout=1000)
    except Exception as e:
        print(f"faild to press button: {e}")


def read_session(session_name: str) -> dict | None:
    """Reads a specific session file."""
    session_file_path = os.path.join("sessions", f"{session_name}.json")
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
    cookies_file_path = os.path.join("cookies", f"{cookies_name}-cookies.json")
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


def time_to_minutes(time_str: str) -> int:
    if pd.isna(time_str):
        return 0

    # Extract hours and minutes using regex
    hours = 0
    minutes = 0

    # Match patterns like "2h 45m", "2h", or "45m"
    h_match = re.search(r'(\d+)h', time_str)
    m_match = re.search(r'(\d+)m', time_str)

    if h_match:
        hours = int(h_match.group(1))
    if m_match:
        minutes = int(m_match.group(1))

    return hours * 60 + minutes


def detect_and_calculate_layover(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects flights with layovers based on flight duration comparison and calculates layover times.

    Args:
        df: Pandas DataFrame containing flight information

    Returns:
        DataFrame with added/updated layover information
    """
    # Create a copy to avoid modifying the original
    df_result = df.copy()

    # Dictionary of expected direct flight (in minutes) after checking the avrage flight lenght from these destinations
    direct_flight_times = {
        ('ROME', 'PARIS'): 140,  # 2h 20m
        ('ROME', 'LONDON'): 180,  # 3h 0m
        ('PARIS', 'ROME'): 130,  # 2h 10m
        ('PARIS', 'LONDON'): 90,  # 1h 30m
        ('LONDON', 'ROME'): 170,  # 2h 50m
        ('LONDON', 'PARIS'): 85,  # 1h 25m
    }

    # New columns
    df_result['layover_time'] = "0m"
    df_result['return_layover_time'] = "0m"

    for idx, row in df_result.iterrows():
        origin = row['origin_city']
        destination = row['destination_city']

        # Get expected direct flight times
        expected_outbound_time = direct_flight_times.get((origin, destination), 0)
        expected_return_time = direct_flight_times.get((destination, origin), 0)

        # Get actual flight times
        actual_outbound_time = time_to_minutes(row['flight_length'])
        actual_return_time = time_to_minutes(row['return_flight_length'])

        # Calculate potential layover times
        # With domain knowlage i can tell that a layover is at least 45 minutes
        outbound_threshold = expected_outbound_time * 1.5
        return_threshold = expected_return_time * 1.5

        # Check if the flight has any layover
        has_outbound_layover = actual_outbound_time > outbound_threshold and expected_outbound_time > 0
        has_return_layover = actual_return_time > return_threshold and expected_return_time > 0

        # Update the layover boolean field (validating the existing value)
        df_result.at[idx, 'layover'] = has_outbound_layover or has_return_layover

        # Format layover times to hours and minutes for readability
        def format_layover_time(actual_time, expected_time, has_layover):
            if not has_layover:
                return "0m"

            layover_minutes = actual_time - expected_time
            hours = layover_minutes // 60
            mins = layover_minutes % 60

            if hours > 0 and mins > 0:
                return f"{hours}h {mins}m"
            elif hours > 0:
                return f"{hours}h"
            else:
                return f"{mins}m"

        # Calculate and store formatted layover times
        df_result.at[idx, 'layover_time'] = format_layover_time(
            actual_outbound_time, expected_outbound_time, has_outbound_layover
        )

        df_result.at[idx, 'return_layover_time'] = format_layover_time(
            actual_return_time, expected_return_time, has_return_layover
        )

    return df_result


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

    async def _get_page_source(self, url, button_selector: list[str] = None, response_url=None,
                               headers: dict = None) -> str:
        """
        Async get page source after expending all the flights using Playwright
        :param url: website url
        :param button_selector: the selector of the button
        :return: page source
        # """

        async def _handle_response(response) -> None:
            if (response.url.startswith(response_url) or response.url.startswith(
                    response_url)) and response.status == 200 and response.url.endswith('.json'):
                with open("flights.json", "w") as f:
                    flights = response.json()
                    json.dumps(flights, f, indent=4)

        session = read_session(session_name=self.__str__())
        cookies = read_cookies(cookies_name=self.__str__())
        async with async_playwright() as pw:
            browser = await pw.firefox.launch(headless=False)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
                viewport=random.choice(VIEWPORTS),
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
            await perform_random_mouse_movements(page)
            await page.wait_for_timeout(2000)
            await page.keyboard.press("PageDown")
            await page.wait_for_load_state('domcontentloaded')

            # Wait for and click the button
            if button_selector:
                scroll_mount = 2000
                for button in button_selector:
                    await scroll_down(page=page, button_selector=button, scroll_amount=scroll_mount)
                    scroll_mount += 2000

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

    def _get_flights(self, soup: bs4.BeautifulSoup, selector: str) -> list:
        pass  # return [{} for item in items]

    async def scarpe_from_page(self, selector, button_selector, response_url=None, headers=None) -> list:
        """
        Extract the data from the website
        """
        soup = BeautifulSoup(await self._get_page_source(url=self.create_url(), button_selector=button_selector,
                                                         response_url=response_url, headers=headers), 'html.parser')
        return self._get_flights(soup, selector)

    def get_data(self) -> pd.DataFrame:
        pass

    async def _add_params(self, ttt: int, los: int) -> pd.DataFrame:
        flights_results = await self.get_data()
        flights_results['ttt'], flights_results['los'], flights_results['snapshot_date'], flights_results[
            'origin_city'], flights_results['destination_city'], flights_results['departure_date'], flights_results[
            'return_date'], flights_results['website'] = \
            ttt, los, datetime.datetime.today().strftime(
                DATE_FORMAT), self.origin_city, self.destination_city, self.departure_date, self.return_date, self.__str__().lower()

        return detect_and_calculate_layover(flights_results)

    async def write_data(self, ttt: int, los: int) -> str:
        data = await self._add_params(ttt=ttt, los=los)
        excel_name = 'Flights.csv'
        file_lock = asyncio.Lock()
        async with file_lock:
            if os.path.exists(excel_name):
                data.to_csv(excel_name, header=False, mode='a', index=False)
                print(f"added data to  {excel_name} for {self.__repr__()}")
            else:
                data.to_csv(excel_name, index=False)
        return self.__repr__()
