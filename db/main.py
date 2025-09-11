from .models import Course, Assessment, Grade
from .db_connection import Base, engine, Session
import sqlalchemy as db
import sqlalchemy.orm as dbo
from datetime import datetime 

Base.metadata.create_all(engine)

session = Session()

def add_course(name):
    course = session.query(Course).filter_by(name = name).first()
    if course: 
        return
    session.add(Course(name = name))
    session.commit()

def add_assessment(course_name, name, weight, amount, date = None):
    course = session.query(Course).filter_by(name = course_name).first()
    if not course:
        print("This course does not exist.")
        return
    assessment = session.query(Assessment).filter_by(name = name).first()
    cur_assessment = Assessment(
        name = name,
        weight = weight,
        amount = amount, 
        course_id = course.id
    )
    if date:
        cur_assessment.date = date

    if assessment:
        if assessment == cur_assessment:
            return
        assessment.weight = cur_assessment.weight
        assessment.amount = cur_assessment.amount
        assessment.date = cur_assessment.date
    else:
        session.add(cur_assessment)
    session.commit()

def add_grade(course_name, name, value):
    course = session.query(Course).filter_by(name = course_name).first()
    if not course:
        print("This course does not exist.")
        return
    grade = session.query(Grade).filter_by(name = name).first()
    cur_grade = Grade(
        name = name,
        value = value,
        course_id = course.id,
        last_update = datetime.utcnow()
    )

    if grade:
        if grade.value == cur_grade.value:
            return
        grade.value = cur_grade.value
    else:
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