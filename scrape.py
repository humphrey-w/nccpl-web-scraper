import os
import logging
import requests
from random import choice
from selenium_stealth import stealth
import undetected_chromedriver as uc
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
load_dotenv(find_dotenv())

SCRAPEOPS_API_KEY = os.getenv('scrapeops_api_key', '')
SCRAPEOPS_BASE_URL = os.getenv(
    'scrapeops_base_url', 'https://headers.scrapeops.io/v1')


def get_user_agents_list(num_results=10):
    '''
    Fetch a list of user-agent headers from ScrapeOps API.
    Args:
        num_results (int): Number of user-agent headers to fetch.
    Returns: List of user-agent headers.
    '''
    # Fetch a list of user-agent headers from ScrapeOps API
    response = requests.get(
        url=f'{SCRAPEOPS_BASE_URL}/user-agents',
        params={
            'api_key': SCRAPEOPS_API_KEY,
            'num_results': num_results
        }
    )

    # Parse the JSON response
    json_response = response.json()

    # Return the list of user-agent headers
    # If the 'result' key is not found, return None
    return json_response.get('result', None)


def get_random_user_agent(user_agents_list=None):
    '''
    Get a random user-agent header from the provided list or fetch a new list.
    Args:
        user_agents_list (list): List of user-agent headers.
    Returns: A random user-agent header.
    '''
    # If no user-agents list is provided, fetch a new one
    if user_agents_list is None:
        user_agents_list = get_user_agents_list()

    # Select a random user-agent from the list
    random_user_agent = choice(user_agents_list)
    return random_user_agent


def setup_logger(log_path='logs/scrape.log'):
    '''Sets up the logging configuration.
    Args:
        log_path (str): Path to the log file.
    '''
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def initialize_driver(user_agent=None):
    '''
    Initializes the undetected Chrome driver with stealth settings.
    Args:
        user_agent (str): User-agent header to use.
    Returns: An instance of the undetected Chrome driver.
    '''
    if user_agent is None:
        user_agent = get_random_user_agent()

    try:
        # Set up Chrome options
        options = uc.ChromeOptions()
        # options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        options.add_argument(f'user-agent={user_agent}')

        # Initialize the undetected Chrome driver
        driver = uc.Chrome(options=options)

        logging.info(f'Initializing driver with User-Agent: {user_agent}')

        # Apply stealth settings to the driver
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        logging.info('Driver initialized successfully.')

        return driver
    except Exception as e:
        logging.ERROR(f'Driver error: {e}')


def fetch(url):
    driver = initialize_driver()
    driver.get(url)
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'fipiNormalDateFilter'))
    )
    driver.save_screenshot('data/raw/screenshot.png')
    driver.quit()


if __name__ == '__main__':
    setup_logger()
    url = 'https://www.nccpl.com.pk/market-information'
    fetch(url)
