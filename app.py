from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, jsonify
from forms import *
from functools import wraps
#from models import *
import os

app = Flask(__name__)


#CONFIGURATIONS
app.config.from_object(os.environ['APP_SETTINGS'])


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap




@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html',form=form)



@app.route('/welcome',methods=['GET', 'POST'])
#@login_required
def Register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = User.query.filter_by(email=form.email.data).first()
        if email is None:
            try:
                user = User(first_name = form.firstname.data,
                            last_name = form.lastname.data,
                            email = form.email.data,
                            password=form.password.data
                            )
                db.session.add(user)
            except:
                db.session.rollback()
            else:
                flash ('successfully signed up....')
                session['email'] = form.email.data
                session['logged_in'] = True
                db.session.commit()
                return redirect(url_for('home'))
        form.email.errors.append('Email already exist, seems you signup already')
        return render_template('welcome.html',form=form)
    return render_template('welcome.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email_exist = User.query.filter_by(email=form.email.data).first()
        if email_exist is None:
            form.email.errors.append('Email not found, please signup')
            return render_template('index.html', form=form)
        if bcrypt.check_password_hash(email_exist.password, form.password.data) is False:
            form.password.errors.append('Invalid password, try again')
            return render_template('index.html', form=form)
        session['email'] = form.email.data
        session['logged_in'] = True
        flash ('successfully logged in!!!!')
        return redirect(url_for('home'))
    return render_template('index.html', form =  form)



@app.route('/home', methods=['POST','GET'])
@login_required
def home():
    user = User.query.filter_by(email= session['email']).first()
    todo = Todo.query.filter_by(user_id=user.id)
    #check = Done.query.filter_by(todo_id=todo.id).all()
    return render_template('home.html',todos=todo)
    

@app.route('/todo', methods = ['POST'])
def todo():
    user = User.query.filter_by(email=session['email']).first()
    _todo = request.form['todo']
    #delete = request.form['del']
    if _todo:
        try:
            newTodo = Todo(todo=_todo, user_id = user.id)
            db.session.add(newTodo)
            db.session.commit()
            return jsonify({'tidy':_todo})
        except:
            return 'sometyn went wrong'
            db.session.rollback()
    return 'notin to post'


@app.route('/delete', methods = ['POST'])
def delete():    
    delete = request.form['del']
    if delete:
        try:
            dele = Todo.query.get(int(delete))
            db.session.delete(dele)
            db.session.commit()
            return True
        except:
            db.session.rollback()


@app.route('/edit', methods = ['POST'])
def edit():
    edit = request.form['edit']
    id_ = request.form['id']
    if edit and id_:
        try:
            newTodo = Todo.query.get(int(id_))
            newTodo.todo = edit
            db.session.commit()
            return jsonify({'edited': edit})
        except:
            db.session.rollback()
    else:
        return render_template('welcome.html')


@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()