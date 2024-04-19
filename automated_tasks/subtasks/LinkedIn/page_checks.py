from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        try:
            # Define the XPath for the modal that contains the confirmation text
            modal_xpath = "//div[contains(@class, 'artdeco-modal__content')]//h3[contains(text(), 'Your application was sent to')]"
            # Wait for the modal to be visible on the page
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, modal_xpath)))
            print("Confirmation modal found: Your application was successfully sent. Clicking to dismiss")
            try:
                # Dismiss button XPath
                dismiss_button_xpath = "//button[@data-test-modal-close-btn]"
                dismiss_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, dismiss_button_xpath))
                )
                dismiss_button.click()
                print("Clicked On Dismiss Button for the Submitted Application Modal")
            except Exception as e:
                print(f"Failed to find the dismiss button for the submitted application modal: {str(e)}")
                return False
            return True
        except Exception as e:
            print(f"Failed to find the confirmation modal: {str(e)}")
            return False