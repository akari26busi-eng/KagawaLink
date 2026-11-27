from flask import Flask, render_template, request, redirect, url_for
from models import db, Course, Comment, Student, Question, Reply, File
import os
import csv

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

with app.app_context():
    db.create_all()

bad_words = []
with open('./static/csv/bad_word.csv', encoding='utf8') as f:
    reader = csv.reader(f)
    for row in reader:
        bad_words.append(row[0])

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        student = Student(
            program=request.form.get('program'),
            grade=int(request.form.get('grade'))
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('courses'))

# 授業一覧
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    search = request.args.get('search', '')
    if search:
        courses = Course.query.filter(Course.course_name.contains(search)).all()
    else:
        courses = Course.query.all()
    # db.session.query(Comment).delete()
    # db.session.query(File).delete()
    db.session.commit()
    return render_template('courses.html', courses=courses, search=search)


def is_bad(comment):
    for word in bad_words:
        if word in comment:
            return True
    return False

@app.route('/comment/<int:course_id>', methods=['POST'])
def add_comment(course_id):
    if request.method == 'POST':
        student_comment = str(request.form.get('student_comment'))
        if is_bad(student_comment):
            return redirect(url_for('courses', error="不適切なコメントが含まれています。"))
        
        comment = Comment(
            program=request.form.get('program'),
            grade=int(request.form.get('grade')),
            student_comment=student_comment,
            course_id=course_id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('courses'))
    return redirect(url_for('courses'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<int:course_id>', methods=['POST'])
def upload_file(course_id):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            newFile = File(
                name=file.filename, 
                path=filepath,  
                course_id=course_id
            )
            db.session.add(newFile)
            db.session.commit()
        return redirect(url_for('courses'))

@app.route('/admin/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course = Course(
            course_name=request.form.get('course_name'),
            teacher=request.form.get('teacher'),
            evaluation=request.form.get('evaluation'),
            method=request.form.get('method'),
            difficulty=float(request.form.get('difficulty', 0))
        )
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('add_course'))
    return render_template('add_course.html')

# Q&A
@app.route('/q_and_a')
def q_and_a():
    posts = Question.query.order_by(Question.date.desc()).all()
    # db.session.query(Reply).delete()
    # db.session.commit()

    return render_template('q_and_a.html', posts=posts)

@app.route('/question')
def question():
    return render_template('post_form.html')

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        detail = request.form.get('detail')
        program = request.form.get('program')
        grade = request.form.get('grade')

        if is_bad(detail):
            return redirect(url_for('q_and_a', error="不適切なコメントが含まれています。"))

        new_post = Question(
            student_program=program, 
            student_grade=grade, 
            comment=detail, 
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect('/q_and_a')
    return redirect(url_for('q_and_a'))

@app.route('/reply/<int:question_id>')
def reply(question_id):
    question = db.session.query(Question).get(question_id)
    return render_template('reply_form.html', question=question)

@app.route('/add_reply/<int:question_id>', methods=['GET', 'POST'])
def add_reply(question_id):
    if request.method == 'POST':
        detail = request.form.get('detail')
        program = request.form.get('program')
        grade = request.form.get('grade')

        if is_bad(detail):
            return redirect(url_for('q_and_a', error="不適切なコメントが含まれています。"))

        new_reply = Reply(
            student_program=program, 
            student_grade=grade, 
            comment=detail, 
            question_id=question_id
        )

        db.session.add(new_reply)
        db.session.commit()
        return redirect('/q_and_a')

@app.route('/post_form')
def add_post():
    return render_template('post_form.html')

if __name__ == '__main__':
    app.run(debug=True)
