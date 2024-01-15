from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def check_for_page_next(driver):
    try:
        # Wait for the navigation element with aria-label 'pagination' to be present
        navigation = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//nav[@aria-label='pagination']"))
        )

        # Find the list item containing the next page anchor
        next_page_anchor = navigation.find_element(By.XPATH, ".//a[contains(@data-testid, 'pagination-page-next')]")

        # If found, return True (indicating the presence of a next page button)
        return True

    except TimeoutException:
        print("Navigation element with aria-label 'pagination' not found.")
        return False
    except NoSuchElementException:
        print("Next page anchor not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
