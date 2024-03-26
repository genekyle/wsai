from automated_tasks.subtasks.random_sleep import random_sleep
from automated_tasks.subtasks.human_type import human_type

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from db.DatabaseManager import LinkedInLocation, LinkedInJobSearch

from datetime import datetime
import re

class Jobs:
    def __init__(self, driver, user_profile, selected_location_id, db_session):
        self.driver = driver
        self.user_profile = user_profile
        self.selected_location_id = selected_location_id
        self.db_session = db_session

    def get_location_name_by_id(self, location_id):
        print("Trying to query location name")
        try:
            location = self.db_session.query(LinkedInLocation).filter(LinkedInLocation.id == location_id).first()
            if location:
                return location.name
        except Exception as e:
            print(f"An error occurred while querying the database: {e}")
        return None
        
    def initiate_search(self, search_query):
        print(f"Initiating search for: {search_query}")
        print("attempting to get location")
        location_name = self.get_location_name_by_id(self.selected_location_id)
        print(f"In area: {location_name}")
        random_sleep(1,10)
        try:
            print("Looking for Jobs Link")
            job_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/jobs/")]'))
            )
            print("Jobs Page Link Found")
            random_sleep(1,3)
            job_link.click()
            print("Clicked on the job link successfully.")
        except TimeoutException:
            print("Timed out waiting for the job link to be clickable.")
        except NoSuchElementException:
            print("The job link was not found.")

        # Check to see if we made it
        expected_url = "https://www.linkedin.com/jobs/"
        
        try:
            WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
            print(f"Arrived at the expected URL: {expected_url}")
        except TimeoutException:
            print(f"Timed out waiting for URL to be: {expected_url}")
            return False
        
        # Check to see if job search bar is loaded in
        try:
            print("Looking for Jobs Search Bar")
            job_search_bar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[contains(@id, "jobs-search-box-keyword")]'))
            )
            print("Jobs Page Search Bar Found")
            random_sleep(1,3)
            job_search_bar.click()
            print("Clicked on the job search bar successfully.")
        except TimeoutException:
            print("Timed out waiting for the job search bar to be clickable.")
        except NoSuchElementException:
            print("The job search bar was not found.")

        human_type(job_search_bar, search_query)
        
        # Check to see if job location search bar is loaded in
        try:
            print("Looking for Jobs Search Bar")
            job_location_bar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[contains(@id, "jobs-search-box-location")]'))
            )
            print("Jobs Page Search Location Bar Found")
            random_sleep(1,3)
            job_location_bar.click()
            print("Clicked on the job search location bar successfully.")
        except TimeoutException:
            print("Timed out waiting for the job location bar to be clickable.")
        except NoSuchElementException:
            print("The job location bar was not found.")

        try:
            human_type(job_location_bar, location_name)

            random_sleep(2,4)
            
            job_location_bar.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Error adding search record: {e}")
        
        random_sleep(5,7)

        # Confirm Search
        print("Confirming Search")
        try:
            job_search_title = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//h1[contains(@title, "{search_query}")]'))
            )
            print('Search Confirmed')
        except Exception as e:
            print(f"Error looking for title that contains search query: {e}")

        # Look for Results Counter for current search
        try:
            print("Looking for number of results span")
            results_span = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'jobs-search-results-list')]//span[contains(., 'results')]"))
            )
            pattern = re.compile(r"[^\d]")
            results_span_text = results_span.text
            results_span_parsed = re.sub(pattern, "", results_span_text)
            search_results_amount = int(results_span_parsed)
            print(F'{results_span_parsed} of results found')

        except Exception as e:
            print(f"Error looking results number span: {e}")
    
        # Add Search Record
        print("Trying to add a job search")
        try:
            new_job_search = LinkedInJobSearch(
                user_profile_id = self.user_profile.id,
                search_input = search_query,
                search_results_amount = search_results_amount,
                location_id = self.selected_location_id,
                search_date = datetime.now()
            )

            self.db_session.add(new_job_search)
            self.db_session.commit()
            print("Search record added successfully")
        
        except Exception as e:
            self.db_session.rollback()
            print(f"Error adding search record: {e}")


    def process_results_page(self):
        """Processes the results on the page"""
        print("Starting to process results on the current page")
        # find how many results are on the current page
        try:
            print("Looking for Unordered List of results on current page")
            results_li = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'scaffold-layout__list-container')]/li")
            print("Results list items found")
            num_li_current_page = len(results_li)
        except Exception as e:
            print(f"Error searching for results list: {e}")
        print(f"Number of list items in the current page: {num_li_current_page}")
        # Next is to process each result or all the list items in the ordered list
        for i in range(1, num_li_current_page + 1):
            print("Looking for list item in the unorddered list")
            list_item_xpath = f"//ul[contains(@class, 'scaffold-layout__list-container')]/li[{i}]"
            list_item_element =  WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, list_item_xpath))
            )
            print(f"List item element {i} found")
            random_sleep(3,5)
            # Click on the list element and then scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView();", list_item_element)
            random_sleep(1.5,2.2)
            list_item_element.click()

            # After scrolled into view and clicked on, extract the values
            job_t

    def apply_to_job(self, job_element):
        """Apply to a single job, deciding which resume to use based on job description matching."""
        # Extract job details
        # Decide on the best resume using NLP model
        # Complete the application process

    def iterate_through_results(self):
        """Iterate through all search result pages, processing each page of results."""
        # Loop through all pages, or until a certain condition is met
        # Call process_results_page() for each page

    def execute_search_and_apply(self, search_query):
        """Execute the full process from search initiation to applying to jobs."""
        self.initiate_search(search_query)
        self.iterate_through_results()