from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import elementchecks as checks
import time
import math
import random
        
# Checks for a page and then interacting with it
def navigate_page(driver):
    # Throws an exception if the page is not a course page (neither a video nor image is present)
    wait = WebDriverWait(driver, 3)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@class='img img-responsive']"))) # Waits for the page to completely load as indicated by image load status
    except:
        time.sleep(1)
    
    # Sets required time to 0 and moves to next page
    min_time = driver.find_element(By.XPATH, "//input[@class='min_required_time']")
    driver.execute_script("arguments[0].setAttribute('value', 0)", min_time)
    next_button = driver.find_element(By.XPATH, "//a[@class='btn btn-success pull-right btn-zoomed btn-next']")
    driver.execute_script("arguments[0].click();", next_button)

# Answers the questions in the quiz/test
def answer_questions(driver, wait, attempted_questions):
    question = checks.default_string(driver.find_element(By.XPATH, "//div[@class='test-question']/strong/strong").text)
    labels = driver.find_elements(By.XPATH, "//div[@class='radio']/label")

    # Checks if the randomizer has arrived at a correct answer, if so, it will click the correct answer, if not, it will randomize again
    if attempted_questions.get(question) is not None:
        for label in labels:
            if checks.default_string(label.find_element(By.TAG_NAME, 'span').text) == attempted_questions[question]:
                driver.execute_script("arguments[0].click();", label.find_element(By.TAG_NAME, 'input'))
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-success pull-right test_next_btn_dat']"))).click()
                break
    else:
        options = driver.find_elements(By.XPATH, "//input[@name='option']")            
        driver.execute_script("arguments[0].click();", options[random.randint(0, len(options) - 1)])
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-success pull-right test_next_btn_dat']"))).click()

# Starts the quiz/test
def start_quiz(driver):
    start_test_button = driver.find_element(By.XPATH, "//a[@class='btn btn-success btn_show_block']")
    driver.execute_script("arguments[0].click();", start_test_button)

# Checks if the test has prompted for a security question
def check_for_security(driver, security_question_answer):
    security_question_box = driver.find_element(By.XPATH, "//form[@action='https://parkviewhs.learn-to-drive-safely.com/drive/index.php/student/test/take/sq_question']/div[1]/input")
    security_question_box.send_keys(security_question_answer)
    log_me_in_button = driver.find_element(By.XPATH, "//form[@action='https://parkviewhs.learn-to-drive-safely.com/drive/index.php/student/test/take/sq_question']/div[2]/button")
    log_me_in_button.click()
