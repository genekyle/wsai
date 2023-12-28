# IndeedBotStateManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IndeedBotStateManager:
    def __init__(self, driver):
        self.current_state = "Not Started"
        self.driver = driver

    def update_state(self, new_state):
        self.current_state = new_state
        print(f"State updated to: {self.current_state}")  # For demonstration purposes

    def is_logged_in(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "element_after_login"))  # Replace with a valid ID
            )
            return True
        except TimeoutException:
            return False
