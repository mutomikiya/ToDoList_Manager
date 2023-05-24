from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey 
import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)

class ToDo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer)
    content = db.Column(db.String(100))
    time = db.Column(db.String(10))
    complete = db.Column(db.Boolean)
    complete_at = db.Column(db.Date)

    schedules = relationship('Schedule', back_populates ='todo')

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.String(20))
    endtime = db.Column(db.String(20))
    todo_id = db.Column(db.Integer, ForeignKey('todo.id'))

    todo = relationship("ToDo", back_populates= "schedules")

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
        priority = request.form['priorityOptions']
        time = request.form['time']+request.form['unit']
        complete = False
        todo = ToDo(content = content, priority = priority, time = time, complete = complete)
        db.session.add(todo)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/edit', methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        edit_todo_id = int(request.form['index'])
        edit_todo = ToDo.query.get(edit_todo_id)

        content = request.form['message']
        priority = request.form['priorityOptions']
        time = request.form['time']+request.form['unit']
        complete = False

        edit_todo.content = content
        edit_todo.priority = priority
        edit_todo.time = time
        edit_todo.complete = complete
        
        db.session.add(edit_todo)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/done', methods=['GET','POST'])
def done():
    if request.method == 'POST':
        try:
            id = int(request.form['index'])
            db.session.query(Schedule).filter(Schedule.todo_id == id).delete()
            
            todo_complete = ToDo.query.get(id)
            todo_complete.complete = True 
            todo_complete.complete_at = datetime.date.today()

            db.session.commit()

        except IndexError:
            return redirect(url_for('index'))
            
    return redirect(url_for('index'))

@app.route('/delete', methods=['GET','POST'])
def deleteComplete():
    if request.method == 'POST':
        try:
            id = int(request.form['index'])
            todo_delete = ToDo.query.get(id)
            db.session.query(Schedule).filter(Schedule.todo_id == id).delete()

            db.session.delete(todo_delete)
            db.session.commit()

        except IndexError:
            return redirect(url_for('index'))
            
    return redirect(url_for('complete'))

@app.route('/complete')
def complete():
    data = ToDo.query.where(ToDo.complete == True).all()
    return render_template('complete.html', data = data)

@app.route('/append_calendar', methods=['GET','POST'])
def append_calendar():
    if request.method == 'POST':
        todo_id = request.form['todo']
        day = request.form['date']
        starttime = day + 'T' + request.form['starttime']
        endtime = day + 'T' + request.form['endtime']

        schedule = Schedule(todo_id = todo_id, starttime = starttime, endtime = endtime)
        db.session.add(schedule)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/edit_calendar', methods=['GET','POST'])
def edit_calendar():
    if request.method == 'POST':
        edit_schedule_id = int(request.form['index'])
        edit_schedule = Schedule.query.get(edit_schedule_id)
        
        day = request.form['date']
        starttime = day + 'T' + request.form['starttime']
        endtime = day + 'T' + request.form['endtime']

        edit_schedule.starttime = starttime
        edit_schedule.endtime = endtime

        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete_calendar', methods=['GET','POST'])
def delete_calendar():
    if request.method == 'POST':
        delete_schedule_id = int(request.form['index'])
        delete_schedule = Schedule.query.get(delete_schedule_id)

        db.session.delete(delete_schedule)
        db.session.commit()
    
    return redirect(url_for('index'))

app.run(port=8080, debug=True)