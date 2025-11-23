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
