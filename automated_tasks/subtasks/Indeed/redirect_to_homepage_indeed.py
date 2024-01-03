from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def redirect_to_homepage_indeed(driver):
    """
    Redirects to the homepage by clicking on the indeed (h)

    Args:
        driver: The Selenium WebDriver instance.

    """
    # Attempt to redirect
    try:
        print("Attempting to redirect to home page using logo icon...")
        nav_logo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, 'gnav-passport')]")
            )
        )
        print("Indeed Homepage Nav Element Found")
        nav_logo.click()
        print("Redirecting to Indeed Homepage via Nav Logo Element...")
    except TimeoutException:
        print("Indeed Homepage Nav Logo Element Not Found")

    # Check if fully redirected
    try:
        print("Checking if redirection to Indeed Homepage is complete...")
        home_nav_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,  "//a[@aria-label='Home'  and @aria-current='page']")
            )
        )
        print("Navigate To Homepage Successful")

    except TimeoutException:
        print("Indeed Homepage Top Nav Element Not Found")