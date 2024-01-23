from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from automated_tasks.subtasks.random_sleep import random_sleep

import datetime

def get_all_listings_on_current_page(driver):
    def extract_data_from_item(card_outline_div):
        # Extract data from the current context (item)
        # Current Date
        current_date = datetime.date.today()
        date_recorded = current_date.isoformat()

        try:
            # Extracting Job Title
            job_title_span = card_outline_div.find_element(By.XPATH, ".//span[contains(@id, 'jobTitle')]")
            job_title = job_title_span.text
            print("Job Title: " + job_title)

            # Extracting Company Name
            company_name_span = card_outline_div.find_element(By.XPATH, ".//span[contains(@data-testid, 'company-name')]")
            company_name = company_name_span.text
            print("Company Name: " + company_name)

            # Extracting Location
            location_span = card_outline_div.find_element(By.XPATH, ".//span[contains(@data-testid, 'company-name')]")
            location = location_span.text
            print("Location: " + location)

            # Extracting Date Scraped
            try:
                print("Trying for Jobs State first for date")
                date_scraped_span = card_outline_div.find_element(By.XPATH, ".//span[contains(@class, 'myJobsState')]")
                date_scraped = date_scraped_span.text
                print(date_scraped)
            except NoSuchElementException:
                try:
                    print("jobs state span not found for date_scraped, trying date span")
                    date_scraped_span = card_outline_div.find_element(By.XPATH, ".//span[contains(@class, 'date')]")
                    date_scraped_full_text = date_scraped_span.text

                    # Split the text at the newline and keep the second part
                    date_scraped_parts = date_scraped_full_text.split('\n')
                    date_scraped = date_scraped_parts[1] if len(date_scraped_parts) > 1 else date_scraped_parts[0]
                    
                except NoSuchElementException:
                    print("no elements found with either span logic")
                    date_scraped = None

            # Need to check if the Right Pane(Where Job Description) has loaded in by checking if both the 
            print("Checking If the Job Post Title matches with the title that is opened in the right hand pane")
            try:
                right_pane_job_title = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//div[contains(@class, 'jobsearch-RightPane')]//h2[contains(@class, 'jobsearch-JobInfoHeader-title')]/span[contains(text(), '{job_title}')]")
                    )
                )
                print("The Text '" + right_pane_job_title.text + "' matches with: " + job_title )
            except NoSuchElementException:
                # If the element is not found, the text is not present
                print("The span on the right panel doesn't match")
            except Exception as e:
                print(e)

            # Extracting Skills
            print("Starting To Extract Skills")
            # Check for a show more button
            try:
                print("Looking for Show More Button")
                right_paneshow_more_skills_button = WebDriverWait(driver, 0.5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(), 'show more')]")
                    )
                )
                print("Show more button found")
                right_paneshow_more_skills_button.click()
            except NoSuchElementException:
                print("Show More Button not found when trying to extract skills")
            
            except TimeoutException:
                print("Timed out for looking for for show more button")
            
            # Looping thorugh each item in the skills list
            skills_list = []    
            
            try:
                print("Starting to loop through each skill")
                list_items = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//ul[contains(@class, 'match-insights')]/li//span[contains(@class, 'match-insights')]")
                    )
                )
                print("Skills list found")

                print("Looping through each item in the skills list")
                for item in list_items:
                    try:
                        span_text = item.text.strip()
                        if "(required)" not in span_text.lower():
                            skills_list.append(span_text)
                    except NoSuchElementException:
                        print("Span not found in the skills list item")
                        continue
                    except Exception as e:
                        print(f"An error occured: {e}")
                        continue
                    
            except NoSuchElementException:
                print("No list item found")
            
            except TimeoutException:
                print("No skills found")

            # Checking for Pay
            try:
                print("Checking for Pay")
                pay_span = WebDriverWait(driver, 0.1).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//h3[contains(text(), 'Pay')]/ancestor::div[1]/following-sibling::div//span[contains(text(), '$')]")
                    )
                )
                print("Pay span found")
                pay = pay_span.text

            except NoSuchElementException:
                print("No Pay Element found")
                pay = None
            
            except TimeoutException:
                print("Looking for Pay Element timedout...")
                pay = None

            except Exception as e:
                print(e)

            try:
                # Locate the div with the specified ID
                print("Searching for Job Description Text")
                job_description_div = driver.find_element(By.ID, "jobDescriptionText")

                # Get all text from the div and its descendants
                job_description_text = job_description_div.text
                
                # Replace newline characters with a space
                job_description_text = job_description_text.replace("\n", " ")

            except NoSuchElementException:
                print("Job description div not found.")


            # ... other data extraction logic, using relative XPaths ...
            return {
                'job_title': job_title,
                'company_name': company_name,
                'location': location,
                'date_scraped': date_scraped,                
                "date_recorded" : date_recorded,
                'skills': skills_list,
                'pay': pay,
                'job_description': job_description_text                

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
                random_sleep(0.5,0.75)

                # Extract data for this item
                item_data = extract_data_from_item(card_outline_div)
                all_listings_data.append(item_data)

            except NoSuchElementException:
                print("cardOutline div not found in this list item.")
        
        return all_listings_data

    except TimeoutException:
        print("Timeout occurred while retrieving list items.")
        return []