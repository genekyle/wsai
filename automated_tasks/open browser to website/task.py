from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def execute_task(config):
    url = config.get("url", "http://example.com")  # Default URL if none provided
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        # Add additional Selenium actions as needed
        while True:
            pass
    except WebDriverException as e:
        print(f"An error occurred while executing the Selenium task: {e}")
        # Handle or log the exception as needed
    finally:
        print("task completed")
