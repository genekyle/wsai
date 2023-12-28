from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from automated_tasks.subtasks.human_type import human_type
from automated_tasks.subtasks.random_sleep import random_sleep
from automated_tasks.subtasks.check_for_hcaptcha_indeed import check_for_hcaptcha
from automated_tasks.subtasks.is_checkbox_checked_indeed import is_checkbox_checked

import time




def login_to_indeed(driver, username, password):
    """
    Logs into Indeed with the given credentials.

    Args:
        driver: The Selenium WebDriver instance.
        username: The username for Indeed login.
        password: The password for Indeed login.
    """
    
    #Navigate to indeed login
    print("Navigating to Indeed login page...")
    login_url = "https://secure.indeed.com"
    driver.get(login_url)

    random_sleep(1,2)

    # Possibly implement Dynamic URL Checking

    # Check If Navigated To Login Page (Try Block 1)
    try:
        print("Checking To See If Navigated to Login Page...")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[type="email"]')
            )
        )        

    except TimeoutException:
        print(f"Timed out waiting for page to load or element to be present: Email Element")
        return False
    # Email To Login
    login_email = username

    # Send Keys in a human-like fashion
    human_type(email_input,login_email)
    print(f"The '{email_input}' element was selected and sent these keys: '{login_email}'")

    # Introduce a random sleep interval (between 1 and 2 seconds) before the next action
    random_sleep(1, 2)

    # Checks if continue button is clickable (Try Block 2)
    try:
        print("Looking For Continue button to move to next step in logging in...")
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )

    except TimeoutException:
        print(f"Timed out waiting for page to load or element to be present: Continue Button Element")
        return False
    
    # Continues To Next Step...
    print("Continue Button Found/Clicklable, Clicking to next step...")
    continue_button.click()
    
    random_sleep(1,3)

    print("Checking For hCaptcha")
    if check_for_hcaptcha(driver):
        # Handle the captcha here (e.g., pause the task, notify the user, etc.)
        print("Handling hCaptcha...")
        # Check if the checkbox is checked
        if is_checkbox_checked(driver):
            print("Checkbox is checked.")
        else:
            print("Checkbox was not checked within the timeout period.")
        
        
    print("Checked for hCaptcha")
    
    """
        For Handling extra windows

    # Checks if Continue Button is clickable (Try Block 3)
    try:
        print("Looking for Google Login Button ")
        google_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id*='login-google-button']"))
        )
        

    except TimeoutException:
        print(f"Timed out waiting for page to load or element to be present: Google Login Button Element")
        return False
    # Step 1: Get all current window handles before clicking
    original_window = driver.current_window_handle
    existing_windows = driver.window_handles
    
    # implicit random wait to allow for window to load
    random_sleep(1,3)

    # Wait for a new window/tab to open and switch to it
    try:
        print("Waiting For Google Login Window to open...")
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == len(existing_windows) + 1)
        print("Google Login Window Opened")
    except TimeoutException:
        print(f"Timed out waiting for page to load or element to be present: Continue Button Element")
        return False
         # Switching to the newly opened window
    print("Switching to the google login window...")
    new_window = [window for window in driver.window_handles if window not in existing_windows][0]

    driver.switch_to.window(new_window)
    print("Switched to the google login window...")

    try:
        print("Looking for Google Email Input ")
        google_email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
        )
    except TimeoutException:
        print(f"Timed out waiting for page to load or element to be present: Google Email Input Element")
        return False
    
    print("Found Google Email Input")

    human_type(google_email_input,login_email)
    """
    

   