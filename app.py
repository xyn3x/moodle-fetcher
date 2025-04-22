import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import re

# Moodle Information
url = "https://moodle.nu.edu.kz"
#Delete when git commit, .gitingore needed
user_data = {
    'username' : '',
    'password' : ''
} # DB is needed
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
    print("Error occured. Wrong username or/and password.")
    sys.exit(0)

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
    print("No course is found")

def delete_unneccessary(name): 
    name = name.lower()

    #Delete spaces
    def delete_space(cur_name):
        while cur_name and cur_name[0] == ' ':
            cur_name = cur_name[1:]
        while name and name[-1] == ' ':
            cur_name = cur_name[:-1]
        return cur_name

    name = delete_space(name)

    #Delete "BACKUP" and "MAKEUP"
    if len(name) >= 6 and (name[:6] == "backup" or name[:6] == "makeup"):
        name = name[6:] 

    name = delete_space(name)

    #Delete time
    if len(name) >= 2 and (name[-2:] == "am" or name[-2:] == "pm"):
        name = name[:-2]
        name = delete_space(name)
        while name and (name[-1].isdigit() or name[-1] == '.'):
            name = name[:-1]
    while name and (name[-1] == '-' or name[-1] == ' '): 
        name = name[:-1]
    if len(name) >= 2 and (name[-2:] == "am" or name[-2:] == "pm"):
        name = name[:-2]
        name = delete_space(name)
        while name and name[-1].isdigit():
            name = name[:-1]

    #Delete spaces if exist
    name = delete_space(name)

    name = name.title()
    return name

for course_link in course_linklist:
    # Course Id
    course_id = 0
    flag = False
    print(course_link)
    cur = 0
    while cur < len(course_link):
        if course_link[cur] == '?':
            flag = True
            cur += 3
        elif flag:
            course_id *= 10
            course_id += int(course_link[cur])
        cur += 1

    url_grade = f'{url}/grade/report/user/index.php?id={course_id}'
    driver.get(url_grade)
    time.sleep(2)

    # Types of grades (img icon):
    # Quiz (quiz)
    # Turnitin Assessment (turnitintooltwo)
    # Attendance (attendance) 
    # Mean (agg_mean; useless should be deleted)
    # Types of grades (with class name):
    # Manual item (fa-pencil-square-o)

    #
    # My obesvations:
    # Table is nested with 3 levels:
    # level1 (name of course usually)
    # === level2 (name of quizzes/assessments group)
    # ====== level3 (quiz/assessment)
    # ====== level3 (quiz/assessment)
    # ====== level3 (quiz/assessment)
    # === level2 (assessment)
    # === level2 (assessment)
    # ... 
    # If level 3 exists, then prev level 2 is not a assessment, but quizzes/assessments group #

    #
    # There are a lot of backup or same assessments with another time. They haven't graded, so not needed
    # So, I should implement function that deletes unnecessary information in assessment links (such as Backup / 9-11am).
    # And then delete all duplicates. Because they are all the same assessment, but only one is graded#


    #
    # Maybe I should save grades as a tree (with depth of 3), idk if it would be useful in advance, but mb I should try
    #
    grade_table = driver.find_elements(By.CSS_SELECTOR, 'table.user-grade tr')
    cur_level = 1
    row_pos = 1
    while row_pos < len(grade_table):
        row = grade_table[row_pos]
        #If there are no <th> tag then there are no grades
        try:
            row_heading = row.find_element(By.TAG_NAME, 'th')
        except:
            row_pos += 1
            continue
        #Check for the row level
        
        grade_name = ""
        for cur_span in row_heading.find_elements(By.CSS_SELECTOR, "span"):
            try:
                grade_name = cur_span.get_attribute('innerHTML')
            except:
                continue
        delete_unneccessary(grade_name)
        print(grade_name)
        print(row_heading.get_attribute("class"))
        row_pos += 1
        
driver.quit()

class Grade:
    def __init__(self, grade, range, feedback=None):
        self.grade = grade
        self.range = range
        if not feedback:
            self.feedback = ""
        else: 
            self.feedback = feedback
