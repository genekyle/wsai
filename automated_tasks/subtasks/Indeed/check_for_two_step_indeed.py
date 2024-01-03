from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_for_2step(driver, timeout=3):
    """
    Checks for the presence of "2-Step Verification" text within a given timeout period.

    Args:
        driver: Selenium WebDriver instance.
        timeout: The maximum time to wait for hCaptcha (in seconds).

    Returns:
        A boolean indicating whether the hCaptcha iframe is present.
    """
    try:
        # Wait for the hCaptcha iframe to appear
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@id='pageHeaderText' and text()='2-Step Verification']"))
        )
        print("2-Step Verification page detected.")
        return True
    except TimeoutException:
        print("2-Step Verification page not detected within the timeout period.")
        return False
