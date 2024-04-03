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

class JobPost:
    def __init__(self, date_posted, date_extracted, job_title, posted_by, job_post_link, job_apply_type, job_location, posted_benefits, job_highlights, company_highlights, skills_highlights, job_post_description):
        self.date_posted = date_posted
        self.date_extracted = date_extracted
        self.job_title = job_title
        self.posted_by = posted_by
        self.job_post_link = job_post_link
        self.job_apply_type = job_apply_type
        self.job_location = job_location
        self.posted_benefits = posted_benefits
        self.job_highlights = job_highlights
        self.company_highlights = company_highlights
        self.skills_highlights = skills_highlights
        self.job_post_description = job_post_description

    def __repr__(self):
        return (f"JobPost(date_posted={self.date_posted}, job_title={self.job_title}, "
                f"posted_by={self.posted_by}, job_location={self.job_location}, job_post_description={self.job_post_description[0:100]})")

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
            print("Looking for list item in the unordered list")
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
            print(f"List Item {i} scrolled into view... Extracting Values")

            # Get Current Date for date_extracte field

            try:
                # After scrolled into view and clicked on, extract the values
                job_post_anchor_xpath = ".//a[contains(@class, 'job-card-list__title')]"
                job_post_anchor_element = WebDriverWait(list_item_element, 10).until(
                    EC.element_to_be_clickable((By.XPATH, job_post_anchor_xpath))
                )

                # Job Title Extraction
                job_post_title = job_post_anchor_element.get_attribute('aria-label')
                print(f'Job Title: {job_post_title}')
                random_sleep(3.5, 4.4)

                # Job Link Extraction
                job_link = job_post_anchor_element.get_attribute('href')

                # Job Posted By
                job_posted_by_span_xpath = ".//span[contains(@class,'primary-description')]"
                job_posted_by = WebDriverWait(list_item_element, 10).until(
                    EC.element_to_be_clickable((By.XPATH, job_posted_by_span_xpath))
                ).text

                # Job Location
                job_location_li_xpath = ".//div[contains(@class, 'artdeco-entity-lockup__caption')]//li[contains(@class,'job-card-container__metadata-item')]"
                job_post_loctation = WebDriverWait(list_item_element, 10).until(
                    EC.element_to_be_clickable((By.XPATH, job_location_li_xpath))
                ).text

                # Posted Benefits (Doesn't Exist For All)
                try:
                    posted_benefits_li_xpath = ".//div[contains(@class,'t-sans t-12')]//li[contains(@class,'job-card-container__metadata-item')]"
                    job_posted_benefits = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, posted_benefits_li_xpath))
                    ).text
                except TimeoutException:
                    print("Timed out waiting for the Posted Benefits Div to be clickable.")
                except NoSuchElementException:
                    print("The Posted Benefits Div was not found.")
                except Exception as e:
                    print(f"Error extracting Posted Benefits Div from list item {i}: {e}")
                
                # See if Job Description loads in and check to see if the what we clicked on 
                try:
                    print("Checking To see if the job post we clicked on matches the full sized job description panel")
                    # Job Description Panel(JDP)
                    job_title_jdp_span_xpath = "//span[contains(@class, 'job-details-jobs-unified-top-card__job-title-link')]"
                    job_title_jdp = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, job_title_jdp_span_xpath))
                    ).text
                    if job_post_title in job_title_jdp:
                        print("Job Title Clicked and JDP Job Title Matches")
                    else:
                        print("Job Title Clicked and JDP Job Title DOES NOT Match")
                except TimeoutException:
                    print("Timed out waiting for the job search bar to be clickable.")
                except NoSuchElementException:
                    print("The job search bar was not found.")
                except Exception as e:
                    print(f"Error extracting data from list item {i}: {e}")
                
                # Job Highlights(Found in the JDP next to suitcase sprite)
                try:        
                    job_highlights_li_xpath = "//li[contains(@class, 'job-details-jobs-unified-top-card__job-insight')]//li-icon[@type='job']/ancestor::li[1]/span"
                    job_highlihgts_li_element = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, job_highlights_li_xpath))
                    )

                    aria_hidden_spans = job_highlihgts_li_element.find_elements(By.XPATH, './/span[@aria-hidden="true"]')
                    if aria_hidden_spans:
                        print("Found spans with 'aria-hidden=true'")
                        span_elements = job_highlihgts_li_element.find_elements(By.XPATH, ".//span[not(@*) or (@aria-hidden='true')]")
                    else:
                        print("No spans with the attribute 'aria-hidden' found in current context")
                        span_elements = job_highlihgts_li_element.find_elements(By.XPATH, ".//span[not(contains(@class,'visually-hidden'))]")

                    span_texts = [span.text for span in span_elements]
                    job_highlights_text = ' '.join(span_texts)
                except TimeoutException:
                    print("Timed out waiting for the job search bar to be clickable.")
                except NoSuchElementException:
                    print("The job search bar was not found.")
                except Exception as e:
                    print(f"Error extracting data from list item {i}: {e}")
                
                # Company Highlights(JDP)
                try:
                    company_highlights_span_xpath = "//li[contains(@class, 'job-details-jobs-unified-top-card__job-insight')]//li-icon[@type='company']/ancestor::li[1]/span"
                    company_highlights_jdp = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, company_highlights_span_xpath))
                    ).text
                except TimeoutException:
                    print("Timed out waiting for the job search bar to be clickable.")
                except NoSuchElementException:
                    print("The job search bar was not found.")
                except Exception as e:
                    print(f"Error extracting data from list item {i}: {e}")
                
                # Skills Highlights(JDP)
                try:
                    skills_highlights_anchor_xpath = "//li[contains(@class, 'job-details-jobs-unified-top-card__job-insight')]//*[local-name()='svg' and @data-test-icon='checklist-medium']/ancestor::li[1]/button/a"
                    skills_highlights_jdp = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, skills_highlights_anchor_xpath))
                    ).text
                except TimeoutException:
                    print("Timed out waiting for the job search bar to be clickable.")
                except NoSuchElementException:
                    print("The job search bar was not found.")
                except Exception as e:
                    print(f"Error extracting data from list item {i}: {e}")

                # Job Description(JDP)
                try:
                    job_description_span_xpath = "//div[contains(@id,'job-details')]/span"
                    job_description = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, job_description_span_xpath))
                    ).text
                except TimeoutException:
                    print("Timed out waiting for job description span to be clickable.")
                except NoSuchElementException:
                    print("The job description span was not found.")
                except Exception as e:
                    print(f"Error extracting job description span from list item {i}: {e}")

                # Date Posted(JDP)
                try:
                    date_posted_span_xpath = "//span[contains(@class, 'tvm__text tvm__text--neutral')]/span[contains(., 'day') or contains(., 'week') or contains(., 'month')]"
                    job_date_posted = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, date_posted_span_xpath))
                    ).text
                except TimeoutException:
                    print("Timed out waiting for Date Posted Span to be clickable.")
                except NoSuchElementException:
                    print("The Date Posted span was not found.")
                except Exception as e:
                    print(f"Error extracting Date Posted span from list item {i}: {e}")
                
                # Apply Type(JDP)
                try:
                    print("Looking For Apply Type")
                    apply_type_button_xpath = "//button[contains(@class, 'jobs-apply-button')]"
                    apply_type_button = WebDriverWait(list_item_element, 10).until(
                        EC.element_to_be_clickable((By.XPATH, apply_type_button_xpath))
                    )
                    # Check the aria-label attribute to determine the apply type
                    aria_label = apply_type_button.get_attribute("aria-label")
                    if "easy apply" in aria_label.lower():
                        print("This is an Easy Apply button.")
                        apply_type = "Easy Apply"
                    else:
                        print("This is a Company Apply button.")
                        apply_type = "Company Apply"
                except TimeoutException:
                    print("Timed out waiting for apply type button to be clickable.")
                except NoSuchElementException:
                    print("The apply type button was not found.")
                except Exception as e:
                    print(f"Error extracting apply type button from list item {i}: {e}")
                

                job_post = JobPost(
                    date_posted=job_date_posted,
                    date_extracted=datetime.now(),
                    job_title=job_post_title,
                    posted_by=job_posted_by,
                    job_post_link=job_link,
                    job_apply_type=apply_type,
                    job_location=job_post_loctation,
                    posted_benefits=job_posted_benefits,
                    job_highlights=job_highlights_text,
                    company_highlights=company_highlights_jdp,
                    skills_highlights=skills_highlights_jdp,
                    job_post_description=job_description
                )
                print(f'Job Post {i}: {job_post}')
            except Exception as e:
                print(f"Error extracting data from list item {i}: {e}")
            
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