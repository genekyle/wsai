from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#from automated_tasks.subtasks.select_all import select_all
from automated_tasks.subtasks.random_sleep import random_sleep


def check_search_success(driver, job_search, location, radius):
    """
    After logged in Initiate The Search For Indeed

    Args:
        driver: The Selenium WebDriver instance.
        job_search: Job Search Input
        location: Location search input
        radius: Radius of search input
    """
    print("Checking the the inputs to see if search was successful... ")
    random_sleep(1,2)
    try:
        print("Checking To See If Indeed Job Search Bar Is Loaded In")
        job_search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[contains(@placeholder, "Job title, keywords, or company")]')
            )
        )
        print("Job Search Bar Loaded In")
    except TimeoutException:
        print("Timed out waiting for page to load or element to be present: Job Search Input Element")
        return False
    print("Job Search Input: ")
    print(job_search)
    print("Actual search input:")
    actual_search_result_text = job_search_input.get_attribute('value')
    print(actual_search_result_text)

    if actual_search_result_text == job_search:
        print("Text Matches")
        random_sleep(1,3)
        return True
    else:
        print("text doesn't match")
        random_sleep(1,3)
        return False
    