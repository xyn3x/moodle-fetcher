from .models import Course, Assessment, Grade
from .db_connection import Base, engine, Session
import sqlalchemy as db
import sqlalchemy.orm as dbo
from datetime import datetime 

Base.metadata.create_all(engine)

session = Session()

# Adding array of course names to DB
def add_course(name):
    course = session.query(Course).filter_by(name = name).first()

    # If already exists, then return
    if course: 
        return
    
    session.add(Course(name = name))
    session.commit()


# Adding assessments json to DB
def add_assessment(course_name, name, weight, amount, date = None):
    course = session.query(Course).filter_by(name = course_name).first()
    if not course:
        print("This course does not exist.")
        return
    
    # Checking if this assessment already exists
    assessment = session.query(Assessment).filter_by(name = name).first()

    # Our current assessment info
    cur_assessment = Assessment(
        name = name,
        weight = weight,
        amount = amount, 
        course_id = course.id
    )
    if date:
        cur_assessment.date = date

    # If exists
    if assessment:
        # If nothing changed, then return
        if assessment == cur_assessment:
            return
        
        # Otherwise update
        assessment.weight = cur_assessment.weight
        assessment.amount = cur_assessment.amount
        assessment.date = cur_assessment.date
    else:
        # Otherwise add
        session.add(cur_assessment)

    session.commit()


def add_grade(course_name, name, value):
    course = session.query(Course).filter_by(name = course_name).first()
    if not course:
        print("This course does not exist.")
        return
    
    # Checking if this grade already exists
    grade = session.query(Grade).filter_by(name = name).first()

    # Our current grade info
    cur_grade = Grade(
        name = name,
        value = value,
        course_id = course.id,
        last_update = datetime.utcnow()
    )
    
    # If exists
    if grade:
        # If nothing changed, then return
        if grade.value == cur_grade.value:
            return
        
        # Otherwise update
        grade.value = cur_grade.value
    else:
        # Otherwise add
        session.add(cur_grade)

    session.commit()

def insert_course(course_names):
    for cur_course in course_names:
        add_course(cur_course)
    
def insert_grades(grades_json):
    for course_name in grades_json.keys():
        for name in grades_json[course_name].keys():
            if grades_json[course_name][name]["type"] == "attendance":
                continue
            grade = grades_json[course_name][name]["grade"]
            range = grades_json[course_name][name]["range"]
            # Calculate value (<= 100%)
            value = grade * 100.0 / range
            add_grade(course_name, name, value)


def insert_assessments(syllabus_json):
    for course_name in syllabus_json.keys():
        for name in syllabus_json[course_name].keys():
            if name.lower() == "attendance":
                continue
            weight = syllabus_json[course_name][name]["weight"]
            date = syllabus_json[course_name][name]["date"]
            amount = syllabus_json[course_name][name]["amount"]
            if not amount: 
                continue
            add_assessment(course_name, name, weight, amount, date)

def get_assessments(course_name):
    course = session.query(Course).filter_by(name = course_name).first()
    if not course: 
        return "No course found."
    return course.assessments


def get_grades(course_name):
    course = session.query(Course).filter_by(name = course_name).first()
    if not course: 
        return "No course found."
    return course.grades