# from app import db
from flask import Flask
from datetime import date
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy()

#授業クラス
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    evaluation = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Float)
    comments = db.relationship('Comment', backref='course', lazy=True)
    file = db.relationship('File', backref='course', lazy=True)

#コメントクラス（授業クラスの子クラス）
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(100), nullable=False) #学部
    grade = db.Column(db.Integer, nullable=False)       #学年
    student_comment = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False, default=date.today)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# ファイルクラス（授業クラスの子クラス）
class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    path = db.Column(db.String(300))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# 学生（ユーザ）クラス
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

# 質問クラス
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    student_program = db.Column(db.String(100), nullable=False)
    student_grade = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=date.today)
    
    replies = db.relationship('Reply', backref='question', lazy=True)

# 回答クラス（質問クラスの子クラス）
class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    student_program = db.Column(db.String(100), nullable=False)
    student_grade = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=date.today)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)