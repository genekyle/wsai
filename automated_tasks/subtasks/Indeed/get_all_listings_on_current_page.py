from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_all_listings_on_current_page(driver):
    def extract_data_from_item(card_outline_div):
        # Extract data from the current context (item)
        try:
            job_title_span = card_outline_div.find_element(By.XPATH, ".//span[contains(@id, 'jobTitle')]")
            job_title = job_title_span.text
            # ... other data extraction logic, using relative XPaths ...
            print(job_title)
            return {
                'job_title': job_title,
                # ... other extracted data ...
            }
        except NoSuchElementException:
            print("Necessary element not found in this item.")
            return {}

    try:
        valid_list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id, 'jobResults')]//ul/li[.//div[contains(@class, 'cardOutline')]]"))
        )

        all_listings_data = []
        for item in valid_list_items:
            try:
                card_outline_div = item.find_element(By.XPATH, ".//div[contains(@class, 'cardOutline')]")
                card_outline_div.click()

                # Extract data for this item
                item_data = extract_data_from_item(card_outline_div)
                all_listings_data.append(item_data)
                print(all_listings_data)

            except NoSuchElementException:
                print("cardOutline div not found in this list item.")
        
        return all_listings_data

    except TimeoutException:
        print("Timeout occurred while retrieving list items.")
        return []