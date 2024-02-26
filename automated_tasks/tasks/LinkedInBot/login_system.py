from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from automated_tasks.subtasks.human_type import human_type
from automated_tasks.subtasks.random_sleep import random_sleep

class LinkedInLoginSystem:
    def __init__(self, session_manager, session_id):
        self.driver = session_manager.get_browser_session(session_id)

    def login(self, username, password):
        # Navigate to the LinkedIn login page
        print("Navigating to LinkedIn Login")
        self.driver.get("https://www.linkedin.com/login")

        if not self.verify_login_navigation():
            print("Failed to navigate to LinkedIn login page")
            return False

        print("Successfully navigated to LinkedIn login page")
        print("user: ", username, " ", "pass: ", password)
        
        # Find the username input field and enter the username(email or telephone number)
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='username']"))
        )
        username_input.clear()
        random_sleep(1.2, 2)
        # Send Keys in a human-like fashion
        human_type(username_input, username)

        # Find the password input field and enter the password
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']"))
        )

        password_input.clear()
        random_sleep(1.2, 2)
        # Send Keys in a human-like fashion
        human_type(password_input, password)

        random_sleep(2,3)
        # Find the login button and click it
        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()

        random_sleep(4,5)
        self.check_for_security()
        


        if not self.verify_login():
            print("Failed to login to LinkedIn")
            return False
        # Add any necessary logic to handle login verification
        print("Successfully logged into LinkedIn")    
        
    def verify_login(self):
        try:
            # Wait for a the feed to be present
            linkedin_feed = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//main[@aria-label='Main Feed']"))
            )
            if linkedin_feed:
                print("Logged into LinkedIn")
            return True
        except NoSuchElementException:
            print("Navigation element with aria-label 'Main Feed' not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def check_for_security(self):
        try:
            # Wait for the hCaptcha element to be present
            security_check = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '''//h1[contains(text(), "Let's do a quick security check")] | //h1[contains(text(), "Let's do a quick verification")]'''))
            )
            # Now wait for the security check to no longer be present (i.e., it's been completed)
            start_time = time.time()
            timeout = 300  # Set a timeout for this wait (e.g., 300 seconds)
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    print("Timeout waiting for security check or verification to be completed.")
                    break

                try:
                    # Check for both types of security checks
                    security_check = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '''//h1[contains(text(), "Let's do a quick security check")] | //h1[contains(text(), "Let's do a quick verification")]'''))
                    )
                    print("Security check or verification still present. Waiting...")
                    time.sleep(5)  # Wait for a short period before checking again
                except NoSuchElementException:
                    # If neither element is found, the security checks are completed
                    print("Security checks completed or not found, continuing...")
                    break
        except TimeoutException:
            # Handle the case where the initial security check doesn't appear within the timeout
            print("No security check detected within the initial wait period.")
        
    def wait_for_user_to_complete_security_check(self, timeout=300):
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("Timeout waiting for security check to be completed.")
                break
            try:
                # Attempt to find the security check element
                security_check = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Security Check')]")
                if security_check:
                    print("Security check detected. Please complete it.")
                    time.sleep(5)  # Wait a bit before checking again to give user time to complete it
            except NoSuchElementException:
                print("Security check completed or not found, continuing...")
                break

    def verify_login_navigation(self):
        try:
            # Wait for the login form to be present
            login_form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//form[@class='login__form']"))
            )
            if login_form:
                print("Login form found")
            return True
        except NoSuchElementException:
            print("Navigation element with aria-label 'pagination' not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False