from moodle.grade.fetcher import fetch_grades
import moodle.syllabus.syllabus_parser
from moodle.syllabus.syllabus_parser import parse_syllabus
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

grades_json = fetch_grades(driver, url, course_linklist)
try: 
    grades_json = fetch_grades(driver, url, course_linklist)
except:
    print("Erorr. Can not fetch the grades.")

# removing duplicates 
modified_grades_json = {}
for key in grades_json.keys():
    cur_name = ""
    cmpname = 0
    component_name = ""
    for cur in key:
        if cur == ",":
            break
        if cur == "-":
            if cmpname:
                break
            cmpname = 1
            continue
        if not cmpname: 
            cur_name += cur
        else:
            component_name += cur
    component_name = component_name.lower()
    if cur_name in modified_grades_json.keys():
        if "lab" in component_name:
            for inner_key in grades_json[key].keys():
                if inner_key == "Attendance":
                    continue
                modified_grades_json[cur_name].update({inner_key : grades_json[key][inner_key]})
        else: 
            modified_grades_json[cur_name].update(grades_json[key])
    else:
        modified_grades_json.update({cur_name : grades_json[key]})
grades_json = json.dumps(modified_grades_json, indent=4)
print(grades_json)

try:
    syllabus_json = parse_syllabus(driver, url, course_linklist)    
except:
    print("Erorr. Can not fetch the grades.")


# removing duplicates 
modified_syllabus_json = {}
for key in syllabus_json.keys():
    cur_name = ""
    cmpname = 0
    component_name = ""
    for cur in key:
        if cur == ",":
            break
        if cur == "-":
            if cmpname:
                break
            cmpname = 1
            continue
        if not cmpname: 
            cur_name += cur
        else:
            component_name += cur
    component_name = component_name.lower()
    if cur_name in modified_syllabus_json.keys():
        if "lab" in component_name:
            continue
        else: 
            modified_syllabus_json[cur_name].update(syllabus_json[key])
    else:
        modified_syllabus_json.update({cur_name : syllabus_json[key]})
syllabus_json = json.dumps(modified_syllabus_json, indent=4)
print(syllabus_json)
driver.quit()
