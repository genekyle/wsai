from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from automated_tasks.subtasks.random_sleep import random_sleep

import re

def check_search_results_amount(driver):
    """
    after checking for search success, we check how many results indeed has for each particular query

    Args:
        driver: The Selenium WebDriver instance.
        job_search: Job Search Input
        location: Location search input
        radius: Radius of search input
    """
    search_amount = 0
    print("Checking to see how many search results our search query generates")
    random_sleep(1,2)
    try:
        print("Checking To See if job results number has loaded in...")
        search_results_amount = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'JobCount')]//span[contains(text(), 'jobs')]")
            )
        )
        print("Search results span found")
    except TimeoutException:
        print("Timed out waiting for page to load or element to be present: Search Results Amount Span Element")
        return False
    search_results_amount_text = search_results_amount.text
    print(search_results_amount_text)
    search_amount = int(search_results_amount_text.split()[0].replace(',', ''))
    print(search_amount)
    return search_amount