from selenium import webdriver

def execute_task(config):
    url = config.get("url", "http://example.com")
    driver = webdriver.Chrome()
    driver.get(url)
