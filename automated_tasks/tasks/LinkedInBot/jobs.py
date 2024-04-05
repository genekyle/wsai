from automated_tasks.subtasks.random_sleep import random_sleep
from automated_tasks.subtasks.human_type import human_type

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from db.DatabaseManager import LinkedInLocation, LinkedInJobSearch, Resumes, ResumeVariations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from datetime import datetime
import re

class JobPost:
    def __init__(self, date_posted, date_extracted, job_title, posted_by, job_post_link, job_apply_type, job_location, posted_benefits, job_highlights, company_highlights, skills_highlights, job_post_description, applied):
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
        self.applied = applied

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
                    date_posted_span_xpath = "//span[contains(@class, 'tvm__text tvm__text--low-emphasis')]/span[contains(., 'day') or contains(., 'week') or contains(., 'month')]"
                    job_date_posted = WebDriverWait(list_item_element, 2).until(
                        EC.element_to_be_clickable((By.XPATH, date_posted_span_xpath))
                    ).text
                except Exception as e:
                    print(f"Error extracting Date Posted span from list item {i}: {e}")
                    print("trying to find alternate job date posted")
                    try:
                        job_date_posted_span_xpath = "//span[contains(@class, '//span[contains(@class, 'tvm__text tvm__text--neutral')]/span[contains(., 'day') or contains(., 'week') or contains(., 'month')]')]/span[contains(., 'day') or contains(., 'week') or contains(., 'month')]"
                        job_date_posted = WebDriverWait(list_item_element, 1).until(
                            EC.element_to_be_clickable((By.XPATH, job_date_posted_span_xpath))
                        ).text
                    except Exception as e:
                        print(f"Error #2 extracting Job Date Posted span from list item {i}: {e}")
                # Apply Type(JDP)
                try:
                    print("Looking For Apply Type")
                    apply_type_button_xpath = "//button[contains(@class, 'jobs-apply-button')]"
                    apply_type_button = WebDriverWait(list_item_element, 2).until(
                        EC.element_to_be_clickable((By.XPATH, apply_type_button_xpath))
                    )
                    # Check the aria-label attribute to determine the apply type
                    aria_label = apply_type_button.get_attribute("aria-label")
                    if "easy apply" in aria_label.lower():
                        print("This is an Easy Apply button.")
                        apply_type = "Easy Apply"
                        applied = self.apply_to_job(job_post_title, job_post_loctation, list_item_element)
                    else:
                        print("This is a Company Apply button.")
                        apply_type = "Company Apply"
                        applied = False
                except TimeoutException:
                    print("Timed out waiting for apply type button to be clickable.")
                    try:
                        print("Trying to look if applied already")
                        applied_span_xpath = "//div[contains(@role, 'alert')]//span[contains(., 'Applied')]"
                        applied_span = WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, applied_span_xpath))
                        )
                        print(job_post_title, ': ', applied_span.text)
                        apply_type = "Applied"
                        applied = True
                    except Exception as e:
                        print(f"Error extracting applied span from list item {i}: {e}")
                except NoSuchElementException:
                    print("The apply type button was not found.")
                    try:
                        print("Trying to look if applied already")
                        applied_span_xpath = "//div[contains(@role, 'alert')]//span[contains(., 'Applied')]"
                        applied_span = WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, applied_span_xpath))
                        )
                        print(job_post_title, ': ', applied_span.text)
                        apply_type = "Applied"
                        applied = True
                    except Exception as e:
                        print(f"Error extracting applied span from list item {i}: {e}")
                except Exception as e:
                    print(f"Error extracting apply type button from list item {i}: {e}")
                    try:
                        print("Trying to look if applied already")
                        applied_span_xpath = "//div[contains(@role, 'alert')]//span[contains(., 'Applied')]"
                        applied_span = WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, applied_span_xpath))
                        )
                        print(job_post_title, ': ', applied_span.text)
                        apply_type = "Applied"
                        applied = True
                    except Exception as e:
                        print(f"Error extracting applied span from list item {i}: {e}")


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
                    job_post_description=job_description,
                    applied=applied
                )
                print(f'Job Post {i}: {job_post}')
            except Exception as e:
                print(f"Error extracting data from list item {i}: {e}")
            
    def apply_to_job(self, job_title, job_location, list_item_element):
        """Apply to a single job, deciding which resume to use based on job description matching."""
        print(f'Trying to apply for {job_title} at {job_location}')
        random_sleep(1,9)
        easy_apply_button_xpath = "//button[contains(@class, 'jobs-apply-button')][contains(@aria-label, 'Easy Apply')]"
        easy_apply_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, easy_apply_button_xpath))
        )
        easy_apply_button.click()
        print("Clicked On the Easy Apply Button")
        random_sleep(1,2)
        
        print("Easy Apply Modal Opened Confirmed")
        random_sleep(2,3)
        while self.modal_is_open():
            modal_xpath = "//h2[contains(@id, 'jobs-apply-header')]"
            modal_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, modal_xpath))
            )
            print("Checking for current stage of applying")
            h3_xpath = "//div[contains(@class, 'jobs-easy-apply-content')]//h3[contains(@class, 't-16 t-bold')]"
            h3_header = modal_element.find_element(By. XPATH, h3_xpath)
            current_header_text = h3_header.text.strip().lower()

            print(f'current applier modal page: {current_header_text}')
            random_sleep(5,10)

            # Pages We would encounter in Apply Modal
            if "contact info" in current_header_text:
                print("In the Contact Info Page, Confirming Contacts")
                email_address_select_option_xpath = "//label[span[@aria-hidden='true' and contains(text(), 'Email address')]]/following-sibling::select[contains(@id, 'text-entity-list')]/option[@value='genomags@gmail.com']"
                email_address_select_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, email_address_select_option_xpath))
                ).text
                if "genomags@gmail.com" in email_address_select_option:
                    print("Email is confirmed in apply modal")
                else:
                    print("Wrong Email Selected in Modal")
                    break
                phone_cc_select_xpath = "//label[span[@aria-hidden='true' and contains(text(), 'Phone country code')]]/following-sibling::select[contains(@id, 'text-entity-list')]"
                phone_cc_select_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, phone_cc_select_xpath))
                )
                selected_phone_cc_obj = Select(phone_cc_select_element)
                selected_phone_cc = selected_phone_cc_obj.first_selected_option.text
                if "United States (+1)" in selected_phone_cc:
                    print("Phone Country Code is confirmed")
                else:
                    print("ERROR: Phone Country Code selected is incorrect")
                mobile_num_input_xpath = "//label[contains(text(), 'Mobile phone number')]/following-sibling::input[contains(@id, 'single-line-text-form')]"
                mobile_num_input_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, mobile_num_input_xpath))
                )

                mobile_num_input_value = mobile_num_input_element.get_attribute("value")
                print("Current value in the input field:", mobile_num_input_value)
                # Usually the contact page ends at mobile phone number so it will end here may need to account for other possibilities

            elif "resume" in current_header_text:
                print("In the Resumes Page, Selecting the correct resume")
                random_sleep(1,2)
                print("Working with Current Job Post Title: ", job_title, 'At location: ', job_location)
                resumes = self.db_session.query(Resumes).all()
                resume_titles = [resume.resume_title for resume in resumes]

                # Include the job title for comparison
                all_titles = resume_titles + [job_title]

                # Generate TF-IDF matrix
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(all_titles)

                # Calculate cosine similarity with the job title
                cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

                # Rank the resumes based on similarity scores
                sorted_indexes = np.argsort(cosine_sim)[::-1]  # Sort in descending order

                # Print the top 10 matches
                print("Top 10 Matching Resumes:")
                for rank, index in enumerate(sorted_indexes[:10], start=1):
                    print(f"{rank}. Resume Title: '{resumes[index].resume_title}' - Score: {cosine_sim[index]:.4f}")

                # Select the highest-scoring resume
                best_match_index = sorted_indexes[0]
                best_match_resume = resumes[best_match_index]
                print(f"Best Match Resume: '{best_match_resume.resume_title}' - Score: {cosine_sim[best_match_index]:.4f}")

                location_groups = {
                    "California": ["California", "CA"],  # Add other cities or areas as needed
                    "New York Metropolitan": ["New York", "NY", "New Jersey", "NJ", "Manhattan", "Brooklyn", "Queens"],
                    "Greater Boston Area": ["Boston", "MA", "Massachusetts", "New Hampshire", "NH"]
                }

                # Determine the job location group directly in the function
                job_location_group = None
                for group, locations in location_groups.items():
                    if any(loc.lower() in job_location.lower() for loc in locations):
                        job_location_group = group
                        break

                # Handle no matching location group
                if job_location_group is None:
                    print(f"No location group found for '{job_location}'. Using default resume variation or handling otherwise.")
                else:
                    print(f"Job location '{job_location}' falls under the '{job_location_group}' group.")
                    # Query for the best matching resume variation based on the location group
                    best_variation = self.db_session.query(ResumeVariations) \
                                                    .filter_by(resume_id=best_match_resume.id, location=job_location_group) \
                                                    .first()

                    if best_variation:
                        print(f"Selected Resume Variation for '{job_location_group}': {best_variation.file_name}")
                    else:
                        print(f"No resume variation found for '{job_location_group}'.")
                random_sleep(10,20)
                
            if not self.next_or_review_button():
                print("Neither next or review button found")
            
            # Checking for exit condition if next or review button not found
            if self.exit_condition_met():
                print("ready to submit application")
                break
            else:
                print("Not ready to submit yet, continuing with modal processing.")

        print("exited the modal processing loop")

    def modal_is_open(self):
        try:
            modal_xpath = "//h2[contains(@id, 'jobs-apply-header')]"
            modal_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, modal_xpath))
            )
            print("Apply Modal found")
            return True
        except NoSuchElementException:
            print("ERROR: apply modal not found")
            return False

    def next_or_review_button(self):
        # for "Next" or "review" button cases
            try:
                # Starting to look for Next button first
                print("Looking for next button")
                next_button_xpath = "//button[contains(@aria-label, 'Continue to next step')]"
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                )
                print("Next button found")
                next_button.click()
                print("Next Button Clicked")
                return True
            except NoSuchElementException:
                print("next button in apply modal not found, looking for reveiw button")
                try:
                    print("Looking for review button")
                    review_button_xpath = "//button[contains(@aria-label, 'Review your application')]"
                    review_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, review_button))
                    )
                    print("review button found")
                    review_button.click()
                    print("Review button clicked")
                    return True
                except NoSuchElementException:
                    print("Error: Next Button or Review button not found")
                    print("Breaking the apply modal loop")
                    return(False)

    def exit_condition_met(self):
        # Logic to determine if the condition to exit is met, meaning look for submit application button button
        try:
            # Starting to look for Submit Application Button
            print("Looking for Submit button")
            submit_application_button_xpath = "//button[contains(@aria-label, 'Submit application')]"
            submit_application_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, submit_application_button_xpath))
            )
            print("Submit application button found")
            # have yet to click the submit application button need to ensure all parts working first
            print("Exit condition met")
            return True
        except Exception as e:
            print(f"ERROR: submit application button in apply modal not found actual error: {e}")
            print("Exit Condition not yet met met")
            return False
        
    def iterate_through_results(self):
        """Iterate through all search result pages, processing each page of results."""
        # Loop through all pages, or until a certain condition is met
        # Call process_results_page() for each page

