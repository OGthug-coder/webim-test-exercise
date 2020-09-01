# Импортируем модули Flask
from flask import Flask, redirect, url_for, render_template, flash, request
# Импортируем ORM SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Импортируем модули для работы с авторизацией
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
# Подключаем собственный модуль
from api import get_list
# Подключаем библиотеку для ведения логгирования
import logging


# Инициализируем приложение и конфигурируем его
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Создаём базу данных и инициализируем логин-менеджер
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'
# Настраиваем формат вывода логов
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class User(UserMixin, db.Model):
    '''
    Описываем класс модели пользователя
    '''
    # Модель будет хранится в таблице 'users'
    __tablename__ = 'users'
    # В качестве первичного ключа указываем id
    id = db.Column(db.Integer, primary_key=True)
    vk_id = db.Column(db.String(64), nullable=False, unique=True)
    token = db.Column(db.String(100), nullable=False, unique=True)


# Данный декоратор отвечает за работу с сессией
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    '''
        Отображение главной страницы
    '''
    friends_list = None
    if not current_user.is_anonymous:
        # Если пользователь залогинен, получаем список друзей и отображаем его
        friends_list = get_list(current_user.token)['response']['items']
        logging.info('User %s got list of his friends', current_user.vk_id)
    else:
        logging.info('Someone\'s on site')
    # Если пользователь не залогинен, то всё равно отображаем страницу
    return render_template('index.html', friends_list=friends_list)


@app.route('/logout')
def logout():
    '''
    Выход пользователя
    '''
    logging.info('%s logged out', current_user.vk_id)
    logout_user()  # Выход юзера
    return redirect(url_for('index'))  # Редирект на домашнюю страницу


@app.route('/authorize/')
def oauth_authorize():
    '''
    Редирект к провайдеру oauth протокола
    '''
    # При помощи JS достаём необходимую информацию (токен)
    return '''  <script type="text/javascript">
                   var data = window.location.href.split("access_token=")[1]; 
                   window.location = "/authorize/" + data;
               </script> '''


@app.route('/authorize/<data>/', methods=['GET'])
def app_authorize(data):
    '''
    Обработка коллбэка от провайдера
    '''
    # Извлечение данных из строки запроса
    data = data.split("&")
    token = data[0]
    vk_id = data[2][8:]

    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    if vk_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    user = User.query.filter_by(vk_id=vk_id).first()

    # Если пользователь с таким id не найден, записываем его в базу
    if not user:
        user = User(vk_id=vk_id, token=token)
        db.session.add(user)
        db.session.commit()

    # Логиним пользователя и перенаправляем на домашнюю страницу
    login_user(user, True)
    logging.info('%s logged in', current_user.vk_id)
    return redirect(url_for('index'))


# Запуск приложения
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
