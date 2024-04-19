from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageCheck:
    """
    Class that handles different Dialogues/Modals that LinkedIn uses Currntly handles:
    - Application Sent Dialogue 
    """

    def __init__(self, driver):
        """
        Initializes the ModalValidator with a Selenium WebDriver.

        Args:
        driver (selenium.webdriver): WebDriver instance used to control the browser.
        """
          