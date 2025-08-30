import time
from . import shrink
from selenium.webdriver.common.by import By

grade_tree = {}

# Fetcher
def fetch_grades(driver, url, course_linklist):
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
        #print(url_grade)
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
            # Task (monologo)
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
                elif "monologo" in grade_type:
                    grade_type = "task"
                else:
                    grade_type = "useless"
            else:
                # Grade group name (Course name, 'Weekly Writing Portfolio') = 'group_name'
                # Manual item (fa-pencil-square-o) = 'manual'
                span_list = row_heading.find_elements(By.TAG_NAME, 'span')
                if len(span_list) == 2:
                    if ("gradeitemheader" in span_list[1].get_attribute('class')) and (("fa-pencil-square-o" in row_heading.find_element(By.TAG_NAME, 'i').get_attribute('class')) or ("fa-pen-to-square" in row_heading.find_element(By.TAG_NAME, 'i').get_attribute('class'))):
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
            #print(grade_type)
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

            grade_name = shrink.delete_unneccessary(grade_name) # Delete all unneccassary stuff

            # Grade, Range, Feeback(?)
            grade_info = row.find_elements(By.TAG_NAME, 'td')
            
            # Useless if it doesn't have persentage
            if not grade_info[3].get_attribute('innerHTML'):
                row_pos += 1
                continue

            try:
                grade_points = grade_info[1].find_elements(By.TAG_NAME, 'div')[1].get_attribute('innerText')
            except:
                grade_points = grade_info[1].get_attribute('innerHTML')

            if grade_points[0].isdigit():
                grade_points = grade_points.replace(',', '.')
                grade_points = float(grade_points)

            grade_range = grade_info[2].get_attribute('innerHTML')
            if grade_range[0].isdigit():
                grade_range = grade_range[grade_range.find("–") + 1:]
                grade_range = int(grade_range)
                if grade_points == "-":
                    grade_points = 0.0
            else: 
                if grade_range[0] == 'F':
                    if grade_points == "-":
                        row_pos += 1
                        continue
                    if grade_points[0] == 'F':
                        grade_points = 0
                    else:
                        grade_points = 1
                    grade_range = 1
                else:
                    row_pos += 1
                    continue
                    

            #print(f"==={grade_points, grade_range, grade_type}")
            # Grade
            if len(group_stack) == 1:
                if grade_name in grade_tree[group_stack[-1]]:
                    grade_tree[group_stack[-1]][grade_name]['grade'] = max(grade_tree[group_stack[-1]][grade_name]['grade'], grade_points)
                else:
                    if grade_points == "Pass" or grade_points == "Fail":
                        grade_range = "";
                    grade_tree[group_stack[-1]][grade_name] = {}
                    grade_tree[group_stack[-1]][grade_name].update({
                                                                        'grade' : grade_points, 
                                                                        'range' : grade_range, 
                                                                        'type' : grade_type
                                                                    })
            else:
                if grade_name in grade_tree[group_stack[0]][group_stack[-1]]:
                    grade_tree[group_stack[0]][group_stack[-1]][grade_name]['grade'] = max(grade_tree[group_stack[0]][group_stack[-1]][grade_name]['grade'], grade_points)
                else: 
                    if grade_points == "Pass" or grade_points == "Fail":
                        grade_range = "";
                    grade_tree[group_stack[0]][group_stack[-1]][grade_name] = {}
                    grade_tree[group_stack[0]][group_stack[-1]][grade_name].update({
                                                                        'grade' : grade_points, 
                                                                        'range' : grade_range, 
                                                                        'type' : grade_type
                                                                    })
            row_pos += 1
    return grade_tree
