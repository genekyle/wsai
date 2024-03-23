from automated_tasks.subtasks import random_sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class Jobs:
    def __init__(self, driver, user_profile):
            self.driver = driver
            self.user_profile = user_profile
            # Additional initialization as necessary, e.g., NLP model for resume matching
        
    def initiate_search(self, search_query):
        print(f"Initiating search for: {search_query}")
        random_sleep(1,10)
        self.driver.get("https://www.linkedin.com/jobs")
        try:
            # Wait for the link to be clickable
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
    

    def process_results_page(self):
        """Process a single page of search results, deciding on which jobs to apply."""
        # Loop through job listings on the current page
        # For each job, decide whether to apply based on criteria (e.g., "Easy Apply" availability)

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