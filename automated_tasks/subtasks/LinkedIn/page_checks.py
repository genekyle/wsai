from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automated_tasks.subtasks.random_sleep import random_sleep

class PageCheck:
    """
    Class that handles different Dialogues/Modals that LinkedIn uses Currntly handles:
    - Application Sent Dialogue 
    """

    def __init__(self, driver):
        self.driver = driver
        """
        Initializes the ModalValidator with a Selenium WebDriver.

        Args:
        driver (selenium.webdriver): WebDriver instance used to control the browser.
        """

    def check_submission_modal(self):
        """
        Checks for a modal that confirms the application submission.

        Returns:
        bool: True if the submission modal is found, False otherwise.
        """
        # Define the XPath for the modal that contains the confirmation text
        modal_xpaths = [ 
            """//div[contains(text(), "Keep track of your application")]""",
            """//p[contains(text(),'You can keep track')]""",
            """//h3[contains(normalize-space(), 'Your application was sent')]"""
        ]
        for xpath in modal_xpaths:
            try:
                print(f"Attempting to find modal using XPath: {xpath}")
                # Wait for the modal to be visible on the page
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                print("Confirmation modal found: Your application was successfully sent. Clicking to dismiss")
                random_sleep(2.5,3.5)
                try:
                    print("Attempting to close using dismiss button #1")
                    # Dismiss button XPath
                    dismiss_button_xpath = "//button[@data-test-modal-close-btn]"
                    dismiss_button = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, dismiss_button_xpath))
                    )
                    print("Dismiss button found")
                    dismiss_button.click()
                    print("Clicked On Dismiss Button for the Submitted Application Modal")
                    return True
                except Exception as e:
                    print(f"Failed to find the dismiss button for the submitted application modal: {str(e)}")
                    return False
            except Exception as e:
                print(f"Failed to find the submission modal using {xpath}, Error: {str(e)}")
                continue  # Try the next XPath if the current one fails
