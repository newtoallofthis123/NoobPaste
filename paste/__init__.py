from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
import flask_login as login
import os

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'pulse'
db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = '/login_error'
mail = Mail(app)
from flask_migrate import Migrate

from paste import routes
from paste.models import Bin, User
# Create customized model view class
class NoobPasteModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class NoobPasteAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect('/admin_login')
        if login.current_user.username == "noobscience123":
            return super(NoobPasteAdminIndexView, self).index()
        else:
        	return redirect('/admin_login')

admin = Admin(app, 'NoobPaste Admin', index_view=NoobPasteAdminIndexView(), template_mode='bootstrap4')
admin.add_view(NoobPasteModelView(User, db.session))
admin.add_view(NoobPasteModelView(Bin, db.session))
migrate = Migrate(app, db)
