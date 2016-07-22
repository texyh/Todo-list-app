from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, jsonify
from forms import *
from functools import wraps
from models import *

app = Flask(__name__)


#CONFIGURATIONS
app.secret_key = 'emeka'

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
                db.session.commit()
                flask ('successfully signed up....')
                return render_template('home.html')
            except:
                db.session.rollback()
                return 'error'
        return render_template('index.html',form=form)

        form.email.errors.append('Email already exist, seems you signup already')
    return render_template('welcome.html', form=form)












@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email_exist = User.query.filter_by(email=form.email.data).first()
        if email_exist is None:
            flash('Email not found, please Register!!')
            form.email.errors.append('Email not found, please signup')
            return render_template('index.html', form=form)
        if bcrypt.check_password_hash(email_exist.password, form.password.data) is False:
            flash('Invalid password, try again!!')
            form.password.errors.append('Invalid password, try again')
            return render_template('index.html', form=form)
        flash ('successfully logged in!!!!')
        return render_template('home.html')

    flash('Email not found, please Register!!')
    return render_template('index.html', form =  form)



@app.route('/home', methods=['POST','GET'])
def home():
    return render_template('home.html')
    

@app.route('/todo', methods = ['POST'])
def todo():
    _todo = request.form['todo']

    if _todo:
        newTodo = _todo[::-1]
        return jsonify({'tidy':newTodo})
    else:
        return render_template('welcome.html')




if __name__ == '__main__':
    app.run(debug=True)