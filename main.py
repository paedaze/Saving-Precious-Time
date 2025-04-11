from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import elementchecks as checks
import webpageactions as actions
import math

# Formats string to be readable for the randomizer
def default_string(string):
    return string.strip().lower().replace(" ", "")

username = str(input("Enter your username: "))
password = str((input("Enter your password: ")))
security_question_answer = str(input("Enter your security question answer: "))

service = Service(executable_path='chromewebdriver.exe')
driver = webdriver.Chrome()

driver.get('https://parkviewhs.learn-to-drive-safely.com/')

# Login in with email and password
login = driver.find_element(By.TAG_NAME, 'form')
username_box = login.find_element(By.CLASS_NAME, 'pull-left')
password_box = login.find_element(By.CLASS_NAME, 'pull-right')

username_box.find_element(By.XPATH, '//input[1]').send_keys(username)
password_box.find_element(By.NAME, 'password').send_keys(password)
password_box.find_element(By.XPATH, '//button[1]').click()

# Create wait object to wait for elements to load
wait = WebDriverWait(driver, 10)

# Click Continue button and verify security question
continue_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='terms']/center/a")))
driver.execute_script("arguments[0].click();", continue_button)

security_question_box = wait.until(EC.presence_of_element_located((By.XPATH, "//form[@method='POST']/div/input")))
security_question_box.send_keys(security_question_answer)
log_me_in_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-success btn_question mt-5']")))
log_me_in_button.click()

# Go to course page
course_page_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@style='min-height:550px']/div[@class='row']/div[2]/a")))
driver.execute_script("arguments[0].click();", course_page_button)

# Creates a dict for the attempted questions and their answers
attempted_questions = {}
wait = WebDriverWait(driver, math.inf)

# Automatically naviagates through the course
while True:
    # Checks if currently on a course page
    try:
        actions.navigate_page(driver)
        continue
    except:
        pass

    # Checks if the course is prompting for a quiz/test
    if checks.check_element_exists_by_xpath(driver, "//form[@action='https://parkviewhs.learn-to-drive-safely.com/drive/index.php/student/test/take/sq_question']"):
        actions.check_for_security(driver, security_question_answer)
    elif checks.check_element_exists_by_xpath(driver, "//a[@class='btn btn-success btn_show_block']"):
        actions.start_quiz(driver)

    # Answers the questions randomly and clicks the next/redo button upon completing the quiz
    if checks.check_element_visible_by_xpath(driver, "//input[@name='option']"):
        actions.answer_questions(driver, attempted_questions)
    # Checks if the quiz has ended
    elif checks.check_element_exists_by_xpath(driver, "//a[@class='btn btn-success pull-right']") and checks.check_element_exists_by_xpath(driver, "//table[@id='table_id']"): # Checks if the next/redo button and table of questions is present
        table = driver.find_element(By.XPATH, "//table[@id='table_id']/tbody")
        table_rows = table.find_elements(By.TAG_NAME, 'tr')

        # Iterates through each row and checks if the answer was correct: adds it to the dictionary if correct
        for row in table_rows:
            if row.find_elements(By.TAG_NAME, 'td')[3].text == 'InCorrect':
                continue
            if attempted_questions.get(default_string(row.find_elements(By.TAG_NAME, 'td')[1].text)) is None:
                attempted_questions[default_string(row.find_elements(By.TAG_NAME, 'td')[1].text)] = default_string(row.find_elements(By.TAG_NAME, 'td')[2].text)

        next_button = driver.find_element(By.XPATH, "//a[@class='btn btn-success pull-right']")
        driver.execute_script("arguments[0].click();", next_button)


