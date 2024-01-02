from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_for_password_page(driver):

    try:
        print("Checking If Logged in on Indeed...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[text()='Password']")
            )
        )
        print("Password Element Found")
        return True  # Element found, user is not logged in
    except TimeoutException:
        print ("Password Element Not Found")
        return False  # Element not found, user is presumed to be logged in