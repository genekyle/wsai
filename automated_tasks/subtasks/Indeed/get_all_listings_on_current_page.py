from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_all_listings_on_current_page(driver):
    # Create a loop that clicks on the listing first so that we can access all data needed
    valid_list_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id, 'jobResults')]//ul/li[.//div[contains(@class, 'cardOutline')]]"))
    )
    
    print(len(valid_list_items))

    for item in valid_list_items:
        try:
            # Find and click the 'cardOutline' div within the list item
            card_outline_div = item.find_element(By.XPATH, ".//div[contains(@class, 'cardOutline')]")
            card_outline_div.click()

            # start performing data extraction
            # 

        except NoSuchElementException:
            print("cardOutline div not found in this list item.")
    '''
    all_listings = []
    for element in job_listing_elements:
        # Extract the necessary information from each element
        # This is just an example, adjust the extraction logic as per your requirements
        job_title = element.find_element(By.CSS_SELECTOR, 'h2.jobTitle').text
        company_name = element.find_element(By.CSS_SELECTOR, 'span.company').text
        # ... extract other details ...

        # Add the structured data to the list
        all_listings.append({
            'job_title': job_title,
            'company_name': company_name,
            # ... other extracted details ...
        })

    return all_listings
    '''