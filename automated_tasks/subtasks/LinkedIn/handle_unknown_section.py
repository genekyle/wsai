from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, json, re

from automated_tasks.subtasks.random_sleep import random_sleep
from automated_tasks.subtasks.human_type import human_type

from automated_tasks.tasks.LinkedInBot.match_label_model import ModelHandler

from sentence_transformers import SentenceTransformer, util

with open('C:/Users/genom/code/wsai/automated_tasks/tasks/LinkedInBot/qa_data.json', 'r') as file:
    categories = json.load(file)
    data = [item for category in categories.values() for item in category]

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Separate Model Hanlder for Labels, should modularize for the other QA systems as well
model_handler = ModelHandler()

precomputed_embeddings = {item['question']: model.encode(item['question'], convert_to_tensor=True) for item in data}

def get_answer(question):
    
    question_embedding = model.encode(question, convert_to_tensor=True)
    # Find the question with the highest cosine similarity to the input question
    highest_score = 0
    best_match = None
    for stored_question, embedding in precomputed_embeddings.items():
        similarity = util.pytorch_cos_sim(question_embedding, embedding)[0][0].item()
        if similarity > highest_score:
            highest_score = similarity
            best_match = stored_question
    
    if highest_score > 0.7:  # Example threshold
        matching_data = next((item for item in data if item['question'] == best_match), None)
        return matching_data['answer'], highest_score
    else:
        return "No suitable answer found.", highest_score

def handle_unknown_section(driver, modal_element, current_header_text, job_title, classifier):
    """
    Handle unknown modal sections encountered during the job application process.

    :param driver: WebDriver instance for interacting with the browser.
    :param modal_element: Selenium WebElement representing the modal where the unknown header was found.
    :param current_header_text: The text of the modal header that was not recognized by predefined handlers.
    :param job_title: The title of the job being applied for, providing context for the application process.
    """
    print(f"Handling unknown section with header: {current_header_text} for job: {job_title}")

    predicted_category = classifier.predict(current_header_text)
    print(f'predicted category: {predicted_category}')

    # Contact Info Category Handling
    if 'Contact Information' in predicted_category:
        print("Handling Contact Information Questions")
        print("Looking for how many questions")
        try:
            all_questions_xpath = ".//div[contains(@class, 'jobs-easy-apply-form-section__grouping')]"
            all_questions_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, all_questions_xpath))
            )
            print("All Questions Found")
            num_questions = len(all_questions_elements)
            print(f'Number of Questions Groupings Found: {num_questions}')
        except Exception as e:
            print(f"ERROR: Errored when looking for question groupings in Work Authorization")
        
        for index, question_element in enumerate(all_questions_elements, start=1):
            question_handled = False
            random_sleep(1.2,2.5)
            for index, question_element in enumerate(all_questions_elements, start=1):
                question_handled = False
                random_sleep(1.2,2.5)

                # Check if it's a radio question

                radio_xpath = ".//fieldset[@data-test-form-builder-radio-button-form-component='true']"
                try:
                    print("Trying for radio question search")
                    radio_elements = question_element.find_elements(By.XPATH, radio_xpath)
                    
                except:
                    print("Error looking for radio question")
                if len(radio_elements) > 0:
                    print(f"Question {index} is a Radio Question.")
                    question_handled = True
                    print(f'Question #{index} handled at radio check')
                    try:
                        print("Looking for Question Label")
                        question_xpath = ".//span[@data-test-form-builder-radio-button-form-component__title]/span[@aria-hidden='true']"
                        question = WebDriverWait(question_element, 10).until(
                            EC.presence_of_element_located((By.XPATH, question_xpath))
                        ).text
                        print(f"question {index} found")
                        print(f"Question (Input) #{index}: {question}")

                        answer, score = get_answer(question)
                        print("Question:", question)
                        print("Answer:", answer)
                        print("Score:", score)
                        try:
                            label_xpath = ".//label[@data-test-text-selectable-option__label]"
                            # Locate all the labels for radio inputs
                            labels = WebDriverWait(question_element, 10).until(
                                EC.presence_of_all_elements_located((By.XPATH, label_xpath))
                            )
                            label_texts = []
                            print("Labels Found")
                            for label in labels:
                                text = label.text
                                displayed = label.is_displayed()
                                label_texts.append(text)
                                print(f"Text: {text}, Displayed: {displayed}")

                            print("trying to match answer to labels")
                            matched_label = model_handler.match_answer_to_labels(answer, labels)
                            if matched_label:
                                print(f"Best match: {matched_label[0]}")
                                matched_label[1].click()  # Click the matched label element
                                print("Clicked On Matched Label")
                                # Creating a Question ans object to be put into sql database
                            else:
                                print("No suitable label found for the answer.")

                        except Exception as e:
                            print(f"Errored on label finder for options on radio questions: {e}")
                        
                    except Exception as e:
                        print(f"ERROR Question Label Not found in Input Search: {e}")

                    # Handle radio question specifics here

                # Check if it's an input question
                if not question_handled:
                    print("Trying for input questions")
                     # Mobile Phone Number Check
                    modal_input_elements = [ 
                        """.//div[contains(@class, 'artdeco-text-input--container ember-view')]""",
                        """.//*[contains(@class, 'relative') and @data-test-single-typeahead-entity-form-component='']"""
                    ]
                    for xpath in modal_input_elements:
                        try:
                            print(f"Attempting to find modal input in contact info using XPath: {xpath}")
                            # Wait for the modal to be visible on the page
                            input_elements = WebDriverWait(question_element, 2.5).until(
                                EC.presence_of_all_elements_located((By.XPATH, xpath))
                            )                            
                            print("Modal Input Found: contact info - modal input")
                            random_sleep(1.5,2.5)
                        except Exception as e:
                                print(f"Failed to find or process the modal input element in contact info function: {e}")
                    try:
                        if len(input_elements) > 0:
                            print(f"Question {index} is an Input Question.")
                            question_handled = True
                            try:
                                print("Looking for Question Label")
                                question_xpath = ".//label[contains(@for, 'single-line-text-form-component-formElement')]"
                                question = WebDriverWait(question_element, 10).until(
                                    EC.presence_of_element_located((By.XPATH, question_xpath))
                                ).text
                                print(f"question {index} found")
                                print(f"Question (Input) #{index}: {question}")
                                try:
                                    answer, score = get_answer(question)
                                    print("Question:", question)
                                    print("Answer:", answer)
                                    print("Score:", score)

                                except Exception as e:
                                    print(f"ERROR: Getting answer from qa_model: {e}")

                                print("Looking for Input")
                                input_xpath = ".//input[contains(@id, 'single-line-text-form-component')]"
                                input = WebDriverWait(question_element, 10).until(
                                    EC.presence_of_element_located((By.XPATH, input_xpath))
                                )
                                print("Input Found")
                                print("Checking for numeric error for input")
                                numeric_error_xpath = "//div[contains(@id, 'numeric-error')]"
                                try:
                                    numeric_error = WebDriverWait(question_element, 10).until(
                                        EC.presence_of_element_located((By.XPATH, numeric_error_xpath))
                                    )
                                    print("Numeric Error Found Inputting Numeric Answer")
                                    input.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
                                    print("input cleared")
                                    # Possibly check if there are lettering/non-integers before performing
                                    print(f"Current Answer {answer}")
                                    print("Clearing non integers from answer")
                                    numeric_part = re.search(r'\d+', answer)
                                    if numeric_part:
                                        number_answer = numeric_part.group()
                                    else:
                                        print("ERROR: No Number found in answer")
                                    human_type(input, number_answer)
                                    # Creating a Question ans object to be put into sql database
                                except:
                                    print("Numeric Error Not Found, Inputting regular answer")
                                    human_type(input, answer)
                                    print(f"Answer: {answer}, typed into input question #{index}")
                            except Exception as e:
                                print(f"ERROR Question Label Not found: {e}")
                        else:
                            print(f"Question {index} is not an Input Question.")
                    except Exception as e:
                        print(f"ERROR Looking for input: {e}")

    if 'Work Authorization' in predicted_category:
        print("Handling Work Authorization questions")
        print("Looking for how many questions")
        try:
            all_questions_xpath = ".//div[contains(@class, 'jobs-easy-apply-form-section__grouping')]"
            all_questions_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, all_questions_xpath))
            )
            print("All Questions Found")
            num_questions = len(all_questions_elements)
            print(f'Number of Questions Groupings Found: {num_questions}')
        except Exception as e:
            print(f"ERROR: Errored when looking for question groupings in Work Authorization")
        
        for index, question_element in enumerate(all_questions_elements, start=1):
            question_handled = False
            random_sleep(1.2,2.5)

            # Check if it's a radio question
            try:
                print("Trying for radio question search")
                radio_xpath = ".//fieldset[@data-test-form-builder-radio-button-form-component='true']"
                radio_elements = question_element.find_elements(By.XPATH, radio_xpath)
                print(f'Question #{index} handled, Radio question Identified')
            except Exception as e:
                print(f"ERROR: Errored looking for radio element for Question #{index}")
            if len(radio_elements) > 0:
                print(f"Question {index} is a Radio Question.")
                question_handled = True
                try:
                    print("Looking for Question Label")
                    question_xpath = ".//span[@data-test-form-builder-radio-button-form-component__title]/span[@aria-hidden='true']"
                    question = WebDriverWait(question_element, 10).until(
                        EC.presence_of_element_located((By.XPATH, question_xpath))
                    ).text
                    print(f"question {index} found")
                    print(f"Question (Input) #{index}: {question}")

                    answer, score = get_answer(question)
                    print("Question:", question)
                    print("Answer:", answer)
                    print("Score:", score)
                    try:
                        label_xpath = ".//label[@data-test-text-selectable-option__label]"
                        # Locate all the labels for radio inputs
                        labels = WebDriverWait(question_element, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, label_xpath))
                        )
                        label_texts = []
                        print("Labels Found")
                        for label in labels:
                            text = label.text
                            displayed = label.is_displayed()
                            label_texts.append(text)
                            print(f"Text: {text}, Displayed: {displayed}")

                        print("trying to match answer to labels")
                        matched_label = model_handler.match_answer_to_labels(answer, labels)
                        if matched_label:
                            print(f"Best match: {matched_label[0]}")
                            matched_label[1].click()  # Click the matched label element
                            print("Clicked On Matched Label")
                        else:
                            print("No suitable label found for the answer.")

                    except Exception as e:
                        print(f"Errored on label finder for options on radio questions: {e}")
                    
                except:
                    print("Question Label Not found")
                
            # Check if it's an input question
            if not question_handled:
                print("Trying for input questions")
                input_xpath = ".//div[contains(@class, 'artdeco-text-input--container ember-view')]"
                try:
                    print("Trying for input search")
                    input_elements = WebDriverWait(question_element, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, input_xpath))
                    )
                    if len(input_elements) > 0:
                        print(f"Question {index} is an Input Question.")
                        question_handled = True
                        try:
                            print("Looking for Question Label")
                            question_xpath = ".//label[contains(@for, 'single-line-text-form-component-formElement')]"
                            question = WebDriverWait(question_element, 10).until(
                                EC.presence_of_element_located((By.XPATH, question_xpath))
                            ).text
                            print(f"question {index} found")
                            print(f"Question (Input) #{index}: {question}")
                            try:
                                answer, score = get_answer(question)
                                print("Question:", question)
                                print("Answer:", answer)
                                print("Score:", score)

                            except Exception as e:
                                print(f"ERROR: Getting answer from qa_model: {e}")

                            print("Looking for Input")
                            input_xpath = ".//input[contains(@id, 'single-line-text-form-component')]"
                            input = WebDriverWait(question_element, 10).until(
                                EC.presence_of_element_located((By.XPATH, input_xpath))
                            )
                            print("Input Found")
                            print("Checking for numeric error for input")
                            numeric_error_xpath = "//div[contains(@id, 'numeric-error')]"
                            try:
                                numeric_error = WebDriverWait(question_element, 10).until(
                                    EC.presence_of_element_located((By.XPATH, numeric_error_xpath))
                                )
                                print("Numeric Error Found Inputting Numeric Answer")
                                input.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
                                print("input cleared")
                                # Possibly check if there are lettering/non-integers before performing
                                print(f"Current Answer {answer}")
                                print("Clearing non integers from answer")
                                numeric_part = re.search(r'\d+', answer)
                                if numeric_part:
                                    number_answer = numeric_part.group()
                                else:
                                    print("ERROR: No Number found in answer")
                                human_type(input, number_answer)
                                # Creating a Question ans object to be put into sql database
                            except:
                                print("Numeric Error Not Found, Inputting regular answer")
                                human_type(input, answer)
                                print(f"Answer: {answer}, typed into input question #{index}")
                        except:
                            print("Question Label Not found")
                    else:
                        print(f"Question {index} is not an Input Question.")
                except:
                    print("Error Looking for input")
