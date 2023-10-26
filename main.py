from flask import Flask, request, render_template, flash, session, redirect
from forms import SignUpForm, SignInForm, TaskForm, ProjectForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LuanNQ Python-Flask Web App'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()

import models

@app.route('/')
def main():
    #return "Hello World! This is a content of Python and Flask web application."
    todolist = [
        {
            'Name': 'Buy milk.',
            'Description': 'Buy 2 liters of milk in Coopmart.'
        },
        {
            'Name': 'Get money.',
            'Description': 'Get 500k on ATM.'
        }
    ]
    return render_template('index.html', todolist = todolist)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()

    #if form.is_submitted():
    if form.validate_on_submit():
        print("Validate on submit")
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data
        print("email", _email)

        nguyenquangluan = db.session.query(models.User).filter_by(email=_email).count()
        print(nguyenquangluan)

        if(db.session.query(models.User).filter_by(email=_email).count() == 0):    
            user = models.User(first_name = _fname, last_name = _lname, email = _email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('signUpSuccess.html', user = user)
        else:
            flash('Email {} is already exists!'.format(_email))
            return render_template('signup.html', form = form)

    #return render_template('signup.html')
    print("Not validate on submit")
    return render_template('signup.html', form = form)

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    form = SignInForm()

    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email=_email).first()
        if (user is None):
            flash('Wrong email address or password!')
        else:
            if (user.check_password(_password)):
                session['user'] = user.user_id
                #return render_template('userhome.html')
                return redirect('/userHome')
            else:
                flash('Wrong email address or password!')
                
    return render_template('signin.html', form = form)

@app.route('/logOut')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user = user)
    else:
        return redirect('/')

@app.route('/newTask', methods=['GET', 'POST'])
def newTask():
    _user_id = session.get('user')
    form = TaskForm()
    form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        if form.validate_on_submit():
            _description = form.inputDescription.data
            _priority_id = form.inputPriority.data
            priority = db.session.query(models.Priority).filter_by(priority_id=_priority_id).first()

            _task_id = request.form['hiddenTaskId']
            if (_task_id == "0"):
                task = models.Task(description = _description, user = user, priority = priority)
                db.session.add(task)
            else:
                task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
                task.description = _description
                task.priority = priority

            db.session.commit()
            return redirect('/userHome')
        
        return render_template('/newtask.html', form = form, user = user)
                
    return redirect('/')

@app.route('/editTask', methods=['GET', 'POST'])
def editTask():
    _user_id = session.get('user')
    form = TaskForm()
    form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
            form.inputDescription.default = task.description
            form.inputPriority.default = task.priority_id
            form.process()
            return render_template('/newtask.html', form = form, user = user, task = task)
                
    return redirect('/')

@app.route('/deleteTask', methods=['GET', 'POST'])
def deleteTask():
    _user_id = session.get('user')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
            db.session.delete(task)
            db.session.commit()

        return redirect('/userHome')
                
    return redirect('/')

@app.route('/doneTask', methods=['GET', 'POST'])
def doneTask():
    _user_id = session.get('user')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
            task.isCompleted = True
            db.session.commit()

        return redirect('/userHome')
                
    return redirect('/')




@app.route('/newProject', methods=['GET', 'POST'])
def newProject():
    form = ProjectForm()
    form.Status.choices = [(s.status_id, s.description) for s in db.session.query(models.Status).all()]
    
    if _project_id:
        project = db.session.query(models.User).filter_by(user_id=session('user_id')).first()

        if form.validate_on_submit():
            _name = form.Name.data
            _description = form.Description.data
            _deadline = form.Deadline.data
            _status_id = form.Status.data
            _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

            _project_id = request.form['hiddenProjectId']

            if _project_id == '0':
                project = models.Project(
                    name=_name,
                    deadline=_deadline,
                    description=_description, status=_status
                )
                db.session.add(project)

            db.session.commit()
            return redirect('/projects')
        else:
            return render_template('newproject.html', form=form)
        
    redirect('/')

@app.route('/editProject', methods=['GET', 'POST'])
def editProject():
    form = ProjectForm()

    form.status.choices = [(s.status_id, s.desc) for s in db.session.query(models.Status).all()]

    _user_id = session.get('user_id')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _project_id = request.form['hiddenProjectId']
        print("_project_id: " + _project_id)
        if _project_id:
            if form.submitUpdate.data:
                print('Update project', form.data)
                _name = form.Name.data
                _description = form.Description.data
                _deadline = form.Deadline.data
                _status_id = form.Status.data
                _status = db.session.query(models.Status).filter_by(status_id=_status_id).first()

                project = db.session.query(models.Project).filter_by(project_id=_project_id).first()

                project.name = _name
                project.description = _description
                project.deadline = _deadline
                project.status = _status

                db.session.commit()
                return redirect('/projects')
            else:
                project = db.session.query(models.Project).filter_by(project_id=_project_id).first()
                form.process()

                form.Name.data = project.name
                form.Description.data = project.description
                form.Deadline.data = project.deadline
                form.Status.data = project.status.status_id

                return render_template('newproject.html', form=form, user=user, project=project)
        elif form.validate_on_submit():
            print('Form validated')

    return redirect('/')

@app.route('/deleteProject', methods=['GET', 'POST'])
def deleteProject():
    _user_id = session.get('user_id')
    if _user_id:
        _project_id = request.form['hiddenProjectId']
        if _project_id:
            project = db.session.query(models.Project).filter_by(project_id=_project_id).first()
            db.session.delete(project)
            db.session.commit()

        return redirect('/projects')

    return redirect('/signIn')

@app.route('/doneProject', methods=['GET', 'POST'])
def doneTask():
    _user_id = session.get('user')
    if _user_id:
        _project_id = request.form['hiddenProjectId']
        if _project_id:
            project = db.session.query(models.Project).filter_by(project_id = _project_id).first()
            project.isCompleted = True
            db.session.commit()

        return redirect('/userHome')
                
    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)