from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_for_hcaptcha(driver, timeout=30):
    """
    Checks for the presence of an hCaptcha iframe within a given timeout period.

    Args:
        driver: Selenium WebDriver instance.
        timeout: The maximum time to wait for hCaptcha (in seconds).

    Returns:
        A boolean indicating whether the hCaptcha iframe is present.
    """
    try:
        # Wait for the hCaptcha iframe to appear
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'hcaptcha')]"))
        )
        print("hCaptcha iframe detected.")
        return True
    except TimeoutException:
        print("hCaptcha iframe not detected within the timeout period.")
        return False
