from flask import Flask, redirect, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'vk': {
        'id': '	7582182',
        'secret': 'r5fX4H8qPkCHNtp3qM9P'
    },
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user() # Выход юзера
    return redirect(url_for('index')) # Редирект на домашнюю страницу


@app.route('/authorize/')
def oauth_authorize():
    print(request.args)
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)