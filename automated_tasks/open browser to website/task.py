from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def execute_task(config, should_continue):
    url = config.get("url", "http://example.com")
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        
        while should_continue[0]:  # Access the flag as a list to ensure it's updated across threads
            pass

    except WebDriverException as e:
        print(f"Error during task execution: {e}")
    finally:
        driver.quit()


