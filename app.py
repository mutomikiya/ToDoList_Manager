from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)

class ToDo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(
        db.Integer, primary_key=True
    )
    content = db.Column(db.String(100))
    time = db.Column(db.String(10))
    complete = db.Column(db.Boolean)
    complete_at = db.Column(db.Date)

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(
        db.Integer, primary_key=True
    )
    todo = db.Column(db.String(100))
    starttime = db.Column(db.String(20))
    endtime = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    data = ToDo.query.where(ToDo.complete == False).all()
    events = Schedule.query.all()
    return render_template('index.html', data = data, events = events)
    
@app.route('/append', methods=['GET','POST'])
def append():
    if request.method == 'POST':
        content = request.form['message']
        time = request.form['time']+request.form['unit']
        complete = False
        todo = ToDo(content = content, time = time, complete = complete)
        db.session.add(todo)
        db.session.commit()
    
    return redirect(url_for('index'))
    
@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        try:
            id = int(request.form['index'])
            todo_complete = ToDo.query.get(id)
            todo_complete.complete = True 
            todo_complete.complete_at = datetime.date.today()
            db.session.commit()

        except IndexError:
            return redirect(url_for('index'))
            
    return redirect(url_for('index'))

@app.route('/complete')
def completed():
    data = ToDo.query.where(ToDo.complete == True).all()
    return render_template('complete.html', data = data)

@app.route('/append_calendar', methods=['GET','POST'])
def append_calendar():
    if request.method == 'POST':
        todo = request.form['todo']
        day = request.form['date']
        starttime = day + 'T' + request.form['starttime']
        endtime = day + request.form['endtime']

        schedule = Schedule(todo = todo, starttime = starttime, endtime = endtime)
        db.session.add(schedule)
        db.session.commit()
    
    return redirect(url_for('index'))

app.run(port=8080, debug=True)