from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def is_checkbox_checked(driver, timeout=30):
    """
    Continuously checks if the checkbox div's aria-checked attribute is true.

    Args:
        driver: The Selenium WebDriver instance.
        timeout: Maximum time to wait (in seconds) before timing out.

    Returns:
        True if the checkbox is checked within the timeout, otherwise False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        print("Checking For hCaptcha")
        try:
            # Wait for the captcha checkbox to be present on the page
            checkbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "checkbox"))
            )
            print("checkbox found")
            # Periodically check if the aria-checked attribute is 'true'
            max_attempts = 30  # Number of attempts before giving up (e.g., 30 attempts)
            attempt = 0
            while attempt < max_attempts:
                if checkbox.get_attribute("aria-checked") == "true":
                    print("Captcha is marked as checked.")
                    break
                time.sleep(1)  # Wait for 1 second before checking again
                attempt += 1

            if attempt == max_attempts:
                print("Captcha was not marked as checked in time.")
                # Handle the case where captcha is not marked as checked (e.g., fail the login process)

        except TimeoutException:
            print("Captcha checkbox not found within the timeout period.")
            # Handle the case where captcha checkbox is not found

    return False
