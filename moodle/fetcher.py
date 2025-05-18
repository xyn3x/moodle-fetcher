from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import pprint
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


#
# There are a lot of backup or same assessments with another time. They haven't graded, so not needed
# So, I should implement function that deletes unnecessary information in assessment links (such as Backup / 9-11am).
# And then delete all duplicates. Because they are all the same assessment, but only one is graded#
def delete_unneccessary(name): 
    if not name:
        return ""
    
    name = name.lower()

    #Delete spaces
    def delete_space(cur_name):
        while cur_name and cur_name[0] == ' ':
            cur_name = cur_name[1:]
        while cur_name and cur_name[-1] == ' ':
            cur_name = cur_name[:-1]
        return cur_name

    name = delete_space(name)

    #Delete "BACKUP", "MAKEUP", "Seminar", "Lockdown"
    name = name.replace("backup", "")
    name = name.replace("makeup", "")
    name = name.replace("seminar", "")
    name = name.replace("lockdown", "")
    
    name = delete_space(name)

    #Delete time

    #Delete day
    days = ["sunday", "monday", "tuesday", "thursday", "wednesday", "friday", "saturday"]
    for day in days:
        name = name.replace(day, "")

    #Be careful with quizz/assessment names that are look like '1.5'
    while ":" in name or "." in name:
        pos = name.rfind(":")
        if pos > 0 and name[pos - 1].isdigit() and pos < len(name) - 2 and name[pos + 2].isdigit():
            name = name[:pos] + name[pos + 1:]
            # if ':'/'.' occurs with 'am'/'pm' then extra 'am'/'pm' will be in the name
            pos1 = name.rfind("am")
            if pos1 == -1: 
                pos1 = name.rfind("pm")
            while name and pos1 < len(name) and name[pos1] == " ":
                name = name[:pos1] + name[pos1 + 1:]
                pos1 -= 1
            pos1 += 1
            if name and pos1 > 0 and name[pos1 - 1].isdigit():
                name = name[:pos1] + name[pos1 + 2:]
            else:
                pos1 = name.rfind("pm")
                if pos1 != -1:
                    pos1 -= 1
                    while name and pos1 < len(name) and name[pos1] == " ":
                        name = name[:pos1] + name[pos1 + 1:]
                        pos1 -= 1
                    pos1 += 1
                    if name and pos1 > 0 and name[pos1 - 1].isdigit():
                        name = name[:pos1] + name[pos1 + 2:]
            # Checked prev comm, now continue
            while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"): 
                name = name[:pos] + name[pos + 1:]
            pos -= 1
            while name and pos and (name[pos].isdigit() or name[pos] == "-"):
                name = name[:pos] + name[pos + 1:]
                pos -= 1
        else:
            pos = name.rfind(".")
            if pos > 0 and name[pos - 1].isdigit() and pos < len(name) - 2 and name[pos + 2].isdigit():
                name = name[:pos] + name[pos + 1:]
                pos1 = name.rfind("am")
                if pos1 == -1: 
                    pos1 = name.rfind("pm")
                while name and pos1 < len(name) and name[pos1] == " ":
                    name = name[:pos1] + name[pos1 + 1:]
                    pos1 -= 1
                pos1 += 1
                if name and pos1 > 0 and name[pos1 - 1].isdigit():
                    name = name[:pos1] + name[pos1 + 2:]
                else:
                    pos1 = name.rfind("pm")
                    if pos1 != -1:
                        pos1 -= 1
                        while name and pos1 < len(name) and name[pos1] == " ":
                            name = name[:pos1] + name[pos1 + 1:]
                            pos1 -= 1
                        pos1 += 1
                        if name and pos1 > 0 and name[pos1 - 1].isdigit():
                            name = name[:pos1] + name[pos1 + 2:]
                # Checked prev comm, now continue
                while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"): 
                   name = name[:pos] + name[pos + 1:]
                pos -= 1
                while name and pos and (name[pos].isdigit() or name[pos] == "-"):
                    name = name[:pos] + name[pos + 1:]
                    pos -= 1
            else: 
                break

    #Be careful with words that contain "am" or "pm"
    while "am" in name or "pm" in name: 
        pos = name.rfind("am")
        if pos == -1: 
            pos = name.rfind("pm")
        pos -= 1
        while name and pos < len(name) and name[pos] == " ":
            name = name[:pos] + name[pos + 1:]
            pos -= 1
        pos += 1
        if name and pos > 0 and name[pos - 1].isdigit():
            name = name[:pos] + name[pos + 2:]
            pos -= 1
            while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"):
                name = name[:pos] + name[pos + 1:]
                pos -= 1
        else: 
            pos = name.rfind("pm")
            if pos == -1:
                break
            pos -= 1
            while name and pos < len(name) and name[pos] == " ":
                name = name[:pos] + name[pos + 1:]
                pos -= 1
            pos += 1
            if name and pos > 0 and name[pos - 1].isdigit():
                name = name[:pos] + name[pos + 2:]
                pos -= 1
                while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"):
                    name = name[:pos] + name[pos + 1:]
                    pos -= 1
            else:
                break

    if "(" in name:
        pos = name.rfind("(")
        while pos < len(name) - 1 and name[pos + 1] == ' ':
            name = name[:pos + 1] + name[pos + 2:]
        if pos < len(name) - 1 and name[pos + 1] == '-':
            name = name[:pos + 1] + name[pos + 2:]
        while pos < len(name) - 1 and name[pos + 1] == ' ':
            name = name[:pos + 1] + name[pos + 2:]
        if pos < len(name) - 1 and name[pos + 1] == ')':
            name = name[:pos] + name[pos + 2:]

    if "-" in name:
        pos = name.rfind("-")
        while pos < len(name) - 1 and name[pos + 1] == ' ':
            name = name[:pos + 1] + name[pos + 2:]
        if pos == len(name) - 1: 
            name = name[:pos]
    name = delete_space(name)

    while name and (name[-1] == ' ' or name[-1] == ':' or name[-1] == '-'):
        name = name[:-1]
    name = name.title()
    return name

# Grade object
class Grade:
    def __init__(self, grade, range, type, feedback=None):
        self.grade = grade
        if grade == "Pass":
            self.range = ""
        else: 
            self.range = range
        self.type = type
        if not feedback:
            self.feedback = ""
        else: 
            self.feedback = feedback

grade_tree = {}
# Fetcher
for course_link in course_linklist:
    # Course Id
    course_id = 0
    flag = False
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

    #
    # Maybe I should save grades as a tree (with depth of 3), idk if it would be useful in advance, but mb I should try
    #
    grade_table = driver.find_elements(By.CSS_SELECTOR, 'table.user-grade tr')
    group_stack = []
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
        
        # Grade type
        # Types of grades (img icon):
        # Quiz (quiz)
        # Turnitin Assessment (turnitintooltwo)
        # Attendance (attendance) 
        # Assign (assign)
        # Total Mean/Grade (agg_mean, agg_sum; useless should be deleted)
        # Types of grades (with class name):
        # Manual item (fa-pencil-square-o)
        grade_type = ""
        try: 
            grade_type = row_heading.find_element(By.TAG_NAME, 'img')
        except:
            grade_type = "other"
        
        if grade_type != "other":
            # Quiz (quiz) = 'quiz'
            # Turnitin Assessment (turnitintooltwo) = 'turnitin'
            # Attendance (attendance) = 'attendance' 
            # Total (agg_mean, agg_sum; useless should be deleted) = 'total'
            grade_type = grade_type.get_attribute('src')
            if "quiz" in grade_type:
                grade_type = "quiz"
            elif "turnitintooltwo" in grade_type:
                grade_type = "turnitin"
            elif "attendance" in grade_type:
                grade_type = "attendance"
            elif "assign" in grade_type:
                grade_type = "assign"
            elif "agg_mean" in grade_type or "agg_sum" in grade_type:
                grade_type = "total"
            else:
                grade_type = "useless"
        else:
            # Grade group name (Course name, 'Weekly Writing Portfolio') = 'group_name'
            # Manual item (fa-pencil-square-o) = 'manual'
            span_list = row_heading.find_elements(By.TAG_NAME, 'span')
            if len(span_list) == 2:
                if ("gradeitemheader" in span_list[1].get_attribute('class')) and ("fa-pencil-square-o" in row_heading.find_element(By.TAG_NAME, 'i').get_attribute('class')):
                    grade_type = "manual"
                else:
                    grade_type = "useless"
            else:
                if not span_list[-1].get_attribute('class'):
                    grade_type = "group-name"
                else:
                    grade_type = "ueseless"

        if grade_type == "useless":
            row_pos += 1
            continue
        
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

        if grade_type == "total":
            group_stack.pop()
            cur_level -= 1
            row_pos += 1
            continue

        if grade_type == "group-name":
            # If I found grade group name, then the next level starts
            span_list = row_heading.find_elements(By.TAG_NAME, 'span')
            cur_level += 1
            group_stack.append(span_list[-1].get_attribute('innerHTML'))
            if len(group_stack) == 1:
                grade_tree[group_stack[-1]] = {}
            else:
                grade_tree[group_stack[0]][group_stack[-1]] = {}
            row_pos += 1
            continue
        
        # Check if level is correct
        row_level = row_heading.get_attribute('class').find("level")
        row_level += 5
        row_level = int(row_heading.get_attribute('class')[row_level])
        while row_level < cur_level:
            group_stack.pop()
            cur_level -= 1
        
        # Now, we fetch grades
        grade_name = ""
        if grade_type == "manual":    
            for cur_span in row_heading.find_elements(By.TAG_NAME, 'span'):
                try:
                    grade_name = cur_span.get_attribute('innerHTML')
                except:
                    continue
        else:
            assigment_info = ""
            try:
                assigment_info = row_heading.find_element(By.TAG_NAME, 'a')
            except:
                row_pos += 1
                continue
            # assigment_link = assigment_info.get_attribute('src')  -> Mb I will use that for something later
            grade_name = assigment_info.get_attribute('innerHTML')

        grade_name = delete_unneccessary(grade_name) # Delete all unneccassary stuff

        # Grade, Range, Feeback(?)
        grade_info = row.find_elements(By.TAG_NAME, 'td')
        
        # Useless if it doesn't have persentage
        if not grade_info[3].get_attribute('innerHTML'):
            row_pos += 1
            continue

        try:
            grade_points = grade_info[1].find_elements(By.TAG_NAME, 'div')[1].get_attribute('innerHTML')
        except:
            grade_points = grade_info[1].get_attribute('innerHTML')

        if grade_points == "-":
            grade_points = 0.0
        elif grade_points != "Pass" and grade_points != "Fail":
            grade_points = grade_points.replace(',', '.')
            grade_points = float(grade_points)

        grade_range = 0
        if isinstance(grade_points, float):
            grade_range = grade_info[2].get_attribute('innerHTML')
            grade_range = grade_range[grade_range.find("–") + 1:]
            grade_range = int(grade_range)

        # Grade
        grade = Grade(grade_points, grade_range, grade_type)
        if len(group_stack) == 1:
            if grade_name in grade_tree[group_stack[-1]]:
                grade_tree[group_stack[-1]][grade_name].grade = max(grade_tree[group_stack[-1]][grade_name].grade, grade.grade)
            else: 
                grade_tree[group_stack[-1]][grade_name] = grade
        else:
            if grade_name in grade_tree[group_stack[0]][group_stack[-1]]:
                grade_tree[group_stack[0]][group_stack[-1]][grade_name].grade = max(grade_tree[group_stack[0]][group_stack[-1]][grade_name].grade, grade.grade)
            else: 
              grade_tree[group_stack[0]][group_stack[-1]][grade_name] = grade
        row_pos += 1

pprint.pprint(grade_tree)
driver.quit()

