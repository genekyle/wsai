from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

def check_current_pagination(driver):
    try:
        # Wait for the navigation element with aria-label 'pagination' to be present
        navigation = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//nav[@aria-label='pagination']"))
        )

        # Find the list item containing the current page anchor
        current_page_anchor = navigation.find_element(By.XPATH, ".//a[contains(@data-testid, 'pagination-page-current')]")

        # Extract the page number from the text of the anchor
        current_page_text = current_page_anchor.text.strip()
        print(current_page_text)

        return current_page_text

    except TimeoutException:
        print("Navigation element with aria-label 'pagination' not found.")
        return None
    except NoSuchElementException:
        print("Current page anchor not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
