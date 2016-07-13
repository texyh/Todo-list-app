from flask_sqlalchemy import SQLAlchemy
from app import app
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#Flask bycrypt for password hashing    
from flask_bcrypt import Bcrypt




basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'emeka'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'main.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#password hashing
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first name', db.String, nullable=False)
    last_name = db.Column('last name', db.String, nullable=False)
    email = db.Column('email', db.String, nullable=False)
    password = db.Column('password', db.String, nullable=False)


    def __init__(self,first_name,last_name,email,password,confirmed=False):
                self.first_name = first_name
                self.last_name = last_name
                self.email = email
                self.password = bcrypt.generate_password_hash(password)
                


if __name__ == '__main__':
    manager.run()