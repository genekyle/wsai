from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, json

from db.DatabaseManager import QuestionAnswer

from automated_tasks.subtasks.random_sleep import random_sleep

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