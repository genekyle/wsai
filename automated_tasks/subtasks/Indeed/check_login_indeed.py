from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_login_indeed(driver):
    """
    Checks if the user is logged in on Indeed.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        bool: True if logged in, False otherwise.
    """
    try:
        print("Checking If Logged in on Indeed...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, 'account.indeed.com') and text()='Sign in']")
            )
        )
        print("Sign In Element Found")
        return False  # Element found, user is not logged in
    except TimeoutException:
        print ("Sign In Element Not Found")
        return True  # Element not found, user is presumed to be logged in
