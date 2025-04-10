from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Checks to see if elements exists by xpath
def check_element_exists_by_xpath(driver, xpath):
    wait = WebDriverWait(driver, 1)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        return False
    return True

# Checks to see if element exists by xpath
def check_elements_exists_by_xpath(driver, xpath):
    wait = WebDriverWait(driver, 1)
    try:
        wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except:
        return False
    return True

# Checks to see if elements is visible by xpath
def check_element_visible_by_xpath(driver, xpath):
    wait = WebDriverWait(driver, 3)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except:
        return False
    return True

# Formats string to be readable for the randomizer
def default_string(string):
    return string.strip().lower().replace(" ", "")