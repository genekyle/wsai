from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from automated_tasks.subtasks.select_all import select_all
from automated_tasks.subtasks.human_type import human_type
from automated_tasks.subtasks.random_sleep import random_sleep


def start_search_indeed(driver, job_search, location, radius):
    """
    After logged in we start the scrape/search using the inputs

    Args:
        driver: The Selenium WebDriver instance.
        username: The username for Indeed login.
        password: The password for Indeed login.
    """
    print("Initiating the Search")
    try:
        print("Checking To See If Indeed Job Search Bar Is Loaded In")
        job_search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[contains(@placeholder, "Job title, keywords, or company")]')
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load or element to be present: Job Search Input Element")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
    print("Indeed Job Search Bar Loaded In")
    random_sleep(1,2)  
    job_search_input.click()
    random_sleep(2,5)

    print("Inputting Job Search Input...")
    human_type(job_search_input, job_search)

    print("Searching for Location Input Element...")
    try:
        print("Checking To See If Indeed Job Search Bar Is Loaded In")
        job_location_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[contains(@placeholder, "City, state, zip code")]')
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load or element to be present: Job Location Input Element")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    print("Job Location Input Element Found")

    print("Clearing Location Input...")
    

    random_sleep(1,2)
    job_location_input.click()
    # Select All Using select_all subtask
    select_all(driver)
    random_sleep(1,2)

    print("Inputting Job Location Input...")
    human_type(job_location_input,location)
    random_sleep(1,2)
    # think about implementing a check to see if your inputs made it onto the elements themselves.

    try:
        print("Checking To See If Indeed Job Search Submit Button Is Loaded In")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="submit"]')
            )
        )

    except TimeoutException:
        print("Timed out waiting for page to load or element to be present: Job Search Submit Button Element")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
    submit_button.click()

    

    
