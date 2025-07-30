from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import sys
from dotenv import load_dotenv, dotenv_values

sys.path.append(".")

from moodle.grade.fetcher import fetch_grades

load_dotenv()

# Moodle Information
url = "https://moodle.nu.edu.kz"
user_data = {
    'username' : os.getenv("username"),
    'password': os.getenv("password")
}

url_login = f'{url}/login/index.php'
url_my = f'{url}/my/'
url_course = f'{url_my}courses.php'

driver = webdriver.Chrome()
driver.get(url_login)


# Selenium Driver Activation
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.send_keys(user_data['username'])
password.send_keys(user_data['password'])
driver.find_element(By.ID, "loginbtn").click()
time.sleep(2)

# Check if It's Successful
if driver.current_url != url_my: 
    sys.exit("Error occured. Wrong username or/and password.")
# Fetching course list
driver.get(url_course)
time.sleep(2)

course_linklist = []
for cur_link in driver.find_elements(By.TAG_NAME, 'a'):
    cur_href = cur_link.get_attribute('href')
    course_linkPattern = '/course/view.php?id='
    if not cur_href:
        continue
    if course_linkPattern in cur_href: 
        course_linklist.append(cur_href)
        
course_linklist = list(set(course_linklist)) # Delete Duplicates

if not course_linklist: 
    sys.exit("No course is found")


try:
    grades_json = fetch_grades(driver, url, course_linklist)
    print(grades_json)
except:
    print("Error.")

driver.quit()
