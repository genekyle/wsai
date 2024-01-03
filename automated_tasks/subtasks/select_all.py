from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from automated_tasks.subtasks.random_sleep import random_sleep

def select_all(driver):
    actions = ActionChains(driver)

    random_sleep(0.5, 0.9)
    print("Selecting All by simulting a Left Control + 'a' key combination")
    # Simulates Control + "a" key comibnation
    actions.key_down(Keys.LEFT_CONTROL).send_keys("a").key_up(Keys.LEFT_CONTROL)

    # Perform the action
    actions.perform()