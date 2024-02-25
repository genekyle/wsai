from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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

        random_sleep(2,3)

        if not self.verify_login():
            print("Failed to login to LinkedIn")
            return False
        # Add any necessary logic to handle login verification
        print("Logged into LinkedIn")
    
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