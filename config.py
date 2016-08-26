import os
basedir = os.path.abspath(os.path.dirname(__file__))
class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'this is no secret'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	#password hash
	SECURITY_PASSWORD_SALT = 'my_precious_two'

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False



	
