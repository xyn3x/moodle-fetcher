from moodle.grade.fetcher import fetch_grades
from moodle.syllabus.syllabus_parser import parse_syllabus
from db.main import insert_assessments, insert_course, insert_grades
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import sys
import json
from dotenv import load_dotenv, dotenv_values

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
time.sleep(0.5)

# Selenium Driver Activation
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.send_keys(user_data['username'])
time.sleep(1)
password.send_keys(user_data['password'])
time.sleep(1)
driver.find_element(By.ID, "loginbtn").click()
time.sleep(5)

# Check if It's Successful
if driver.current_url != url_my: 
    sys.exit("Error occured. Wrong username or/and password.")

# Fetching course list
driver.get(url_course)
time.sleep(4)

course_linklist = []
course_name = []
for cur_link in driver.find_elements(By.TAG_NAME, 'a'):
    cur_href = cur_link.get_attribute('href')
    course_linkPattern = '/course/view.php?id='
    if not cur_href:
        continue
    if course_linkPattern in cur_href: 
        needed_elements = cur_link.find_elements(By.TAG_NAME, "span")
        for cur_element in needed_elements: 
            if cur_element.get_attribute('title'):
                cur_name = cur_element.get_attribute('title')
                shrinked_name = ""
                for cur_letter in cur_name:
                    if cur_letter == "," or cur_letter == "-":
                        break
                    shrinked_name += cur_letter
                course_name.append(shrinked_name)
                break
        course_linklist.append(cur_href)
        
# Delete Duplicates
course_linklist = list(set(course_linklist))
course_name = list(set(course_name))

#print(course_name)

if not course_linklist: 
    sys.exit("No course is found")

# Insert courses to DB
insert_course(course_name)

# Trying to fetch the grades
try: 
    grades_json = json.loads(fetch_grades(driver, url, course_linklist))
except:
    sys.exit("Erorr. Can not fetch the grades.")

#print(grades_json)

# Insert grades to DB
insert_grades(grades_json)

# Trying to parse assessments from syllabus
try: 
    syllabus_json = json.loads(parse_syllabus(driver, url, course_linklist))   
except:
    sys.exit("Erorr. Can not fetch the grades.") 

#print(syllabus_json)

# Insert assessments to DB
insert_assessments(syllabus_json)

driver.quit()
