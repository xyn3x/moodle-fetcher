import sqlalchemy as db
import sqlalchemy.orm as dbo
import os
from datetime import datetime
from .db_connection import Base

# 3 tables: Courses, Assessments (Syllabus), and current Grades
class Course(Base):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    grades = dbo.relationship("Grade", back_populates="course")
    assessments = dbo.relationship("Assessment", back_populates="course")

class Assessment(Base):
    __tablename__ = "assessments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    date = db.Column(db.Date, nullable=True)
    weight = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    course = dbo.relationship("Course", back_populates="assessments")

class Grade(Base):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    value = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    course = dbo.relationship("Course", back_populates="grades")