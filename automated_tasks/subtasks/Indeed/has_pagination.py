from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyautogui
import time

def has_pagination(driver):
    try:
        # Wait for the navigation element with aria-label 'pagination' to be present
        navigation = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//nav[@aria-label='pagination']"))
        )

        # Find all list items within the navigation element
        list_items = navigation.find_elements(By.XPATH, ".//ul/li")
        print(len(list_items))
        return len(list_items) > 0

    except TimeoutException:
        print("Navigation element with aria-label 'navigation' not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
