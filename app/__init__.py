from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

#Объект класса Flask
app = Flask(__name__)
#Установка уонфигурации
app.config.from_object(Config)
#Объявление базы данных
db = SQLAlchemy(app)
#Объявление объекта для внесения изменений в БД
migrate = Migrate(app, db)
#Менеджер логинов и управление входом пользователей
login = LoginManager(app)
#Функция для того, чтобы страницы могли просматривать только вошедшые пользователи
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)


from app import routes, models