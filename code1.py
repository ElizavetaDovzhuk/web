from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask
from flask import redirect, render_template
import datetime
from flask import url_for
from flask import request
from sqlalchemy import or_
import sqlite3
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session

SqlAlchemyBase = dec.declarative_base()

__factory = None


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    def __repr__(self):
        return f"<Message> {self.id} {self.title} {self.content}"

    id = sa.Column(sa.Integer,
                           primary_key=True, autoincrement=True)

    content = sa.Column(sa.String, nullable=True)
    photo = sa.Column(sa.String, nullable=True)
    created_date = sa.Column(sa.DateTime,
                                     default=datetime.datetime.now)
    user_name = sa.Column(sa.Integer,
                                  sa.ForeignKey("users.name"), index=True, nullable=False)
    user_to_name = sa.Column(sa.Integer,
                                index=True, nullable=False)
    #is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user = orm.relation('User')


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    name = sa.Column(sa.String, primary_key=True, unique=True, nullable=True)
    # about = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    message = orm.relation("Message", back_populates='user')

    # message = orm.relation("Message", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


user = User()


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


global_init("users3.db")
table = create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    s = ''


class Search(FlaskForm):
    r = StringField('Найти пользователя', validators=[DataRequired()])
    submit = SubmitField('Найти')
    p = ''


class RegistrationForm(FlaskForm):
    name = StringField('Придумайте логин', validators=[DataRequired()])
    email = StringField('Введите электронную почту', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
    s = ''


@app.route("/search", methods=['POST', 'GET'])
def search():
    form = Search()
    form.p = ''
    if form.validate_on_submit():
        d = form.r.data
        print(d, 9128)
        result = []
        for us in table.query(User).all():
            result.append(us.name)
        if d not in result:
            form.p = 'Пользователя с таким именем не существует'
            return render_template('a.html', title='соцсеть.рф', form=form)
        else:
            return redirect('/пользователь3')
    return render_template('a.html', title='соцсеть.рф', form=form)


@app.route("/пользователь2", methods=['POST', 'GET'])
def index2():
    if request.method == 'GET':
        db_session.global_init("users3.db")
        db_sess = db_session.create_session()
        message = list(db_sess.query(Message).filter((Message.user_name.in_(['Пользователь 2', 'Пользователь 3'])),
                                                     (Message.user_to_name.in_(['Пользователь 2', 'Пользователь 3']))))
        lst = []
        lst2 = []
        for i in message:
            lst.append(i.created_date)
            lst2.append(i.created_date)
        lst.sort()
        reslst = []
        count2 = 0
        for i in lst:
            count = 0
            for q in lst2:
                if i == q:
                    reslst.append(message[count])
                count += 1
            count2 += 1
        return render_template("index23.html", message=reslst)
    elif request.method == 'POST':
        db_session.global_init("users3.db")
        db_sess = db_session.create_session()
        w = str(request.form)[20:-2]
        if "('text', '')" in w:
            print('пустое сообщение')
        if 'text' in w:
            if request.form['text'] is not None:
                mes = Message(content=request.form['text'], photo='', user_name='Пользователь 2',
                              user_to_name='Пользователь 3')
                db_sess.add(mes)
                db_sess.commit()
        else:
            mes = Message(content='', photo=request.form['отправить'], user_name='Пользователь 2',
                          user_to_name='Пользователь 3')
            db_sess.add(mes)
            db_sess.commit()
        message = list(db_sess.query(Message).filter((Message.user_name.in_(['Пользователь 2', 'Пользователь 3'])),
                                                     (Message.user_to_name.in_(['Пользователь 2', 'Пользователь 3']))))
        lst = []
        lst2 = []
        for i in message:
            lst.append(i.created_date)
            lst2.append(i.created_date)
        lst.sort()
        reslst = []
        count2 = 0
        for i in lst:
            count = 0
            for q in lst2:
                if i == q:
                    reslst.append(message[count])
                count += 1
            count2 += 1
        if 'text' in w:
            if len(request.form['text']) > 0:
                return render_template("index23.html", message=reslst)
            elif len(request.form['text']) == 0:
                return render_template("index3.html", message='Нельзя отправить пустое сообщение')
        else:
            return render_template("index23.html", message=reslst)


@app.route("/пользователь3", methods=['POST', 'GET'])
def index3():
    if request.method == 'GET':
        db_session.global_init("users3.db")
        db_sess = db_session.create_session()
        message = list(db_sess.query(Message).filter((Message.user_name.in_(['Пользователь 2', 'Пользователь 3'])),
                                                     (Message.user_to_name.in_(['Пользователь 2', 'Пользователь 3']))))
        lst = []
        lst2 = []
        for i in message:
            lst.append(i.created_date)
            lst2.append(i.created_date)
        lst.sort()
        reslst = []
        count2 = 0
        for i in lst:
            count = 0
            for q in lst2:
                if i == q:
                    reslst.append(message[count])
                count += 1
            count2 += 1
        return render_template("index2.html", message=reslst)
    elif request.method == 'POST':
        db_session.global_init("users3.db")
        db_sess = db_session.create_session()
        w = str(request.form)[20:-2]
        if "('text', '')" in w:
            print('пустое сообщение')
        if 'text' in w:
            if request.form['text'] is not None:
                mes = Message(content=request.form['text'], photo='', user_name='Пользователь 3',
                              user_to_name='Пользователь 2')
                db_sess.add(mes)
                db_sess.commit()
        else:
            mes = Message(content='', photo=request.form['отправить'], user_name='Пользователь 3',
                          user_to_name='Пользователь 2')
            db_sess.add(mes)
            db_sess.commit()
        message = list(db_sess.query(Message).filter((Message.user_name.in_(['Пользователь 2', 'Пользователь 3'])),
                                                     (Message.user_to_name.in_(['Пользователь 2', 'Пользователь 3']))))
        lst = []
        lst2 = []
        for i in message:
            lst.append(i.created_date)
            lst2.append(i.created_date)
        lst.sort()
        reslst = []
        count2 = 0
        for i in lst:
            count = 0
            for q in lst2:
                if i == q:
                    reslst.append(message[count])
                count += 1
            count2 += 1
        if 'text' in w:
            if len(request.form['text']) > 0:
                return render_template("index2.html", message=reslst)
            elif len(request.form['text']) == 0:
                return render_template("index3.html", message='Нельзя отправить пустое сообщение')
        else:
            return render_template("index2.html", message=reslst)


@app.route('/')
def start():
    return '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                        <title>соцсеть.рф</title>
                      </head>
                      <body>
                        <h1 align=center>Добро пожаловать!</h1>
                        <style>
                        a {text-align: center;}
                        </style>
                        <div align=center>
                          <a href='http://127.0.0.1:8080/login'>Войти</a>
                          <p>или</p>
                          <a href='http://127.0.0.1:8080/registration'>Зарегистрироваться</a>
                        </div>
                      </body>
                    </html>'''


flag = False


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        a = form.username.data
        p = form.password.data
        d = 0
        for y in a:
            if y.isalpha() or y in '1234567890':
                d += 1
        s = 0
        if d < len(a) or ' ' in a:
            s = 'Имя пользователя должно состоять только из букв и цифр'
        if len(p) < 8 and s == 0:
            s = 'Длина пароля не может быть меньше 8 символов'
        g = 0
        h = 0
        o = 0
        for i in p:
            if i.islower():
                g = 1
            if i.isupper():
                o = 1
            if i in '0123456789':
                h = 1
        if g == 0 and s == 0:
            s = 'В пароле должны присутствовать маленькие буквы'
        if o == 0 and s == 0:
            s = 'В пароле должны присутствовать заглавные буквы'
        if h == 0 and s == 0:
            s = 'В пароле должны присутствовать цифры'
        if s != 0:
            form.s = s
            return render_template('login.html', title='соцсеть.рф', form=form)
        else:
            form.s = ''
            dr = 0
            for us in table.query(User).all():
                if us.name == a and us.check_password(p):
                    dr = 1
                    break
            if dr == 0:
                s = 'Неправильно введён логин или пароль.'
                form.s = s
                return render_template('login.html', title='соцсеть.рф', form=form)
        return redirect('/search')
    return render_template('login.html', title='соцсеть.рф', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        a = form.name.data
        p = form.password.data
        p2 = form.password_again.data
        e = form.email.data
        s = 0
        if '@' in e:
            if '.' in e.split('@')[1]:
                if not e.split('@')[1].split('.')[1] in ['ru', 'com'] and len(e.split('@')[1].split('.')[0]) > 1:
                    s = 'Некорректно введена почта'
            else:
                s = 'Некорректно введена почта'
        else:
            s = 'Некорректно введена почта'
        d = 0
        for y in a:
            if y.isalpha() or y in '1234567890':
                d += 1
        if (d < len(a) or ' ' in a) and s == 0:
            s = 'Имя пользователя должно состоять только из букв и цифр'
        if p != p2 and s == 0:
            s = 'Введённые пароли не совпадают'
        if len(p) < 8 and s == 0:
            s = 'Длина пароля не может быть меньше 8 символов'
        g = 0
        h = 0
        o = 0
        for i in p:
            if i.islower():
                g = 1
            if i.isupper():
                o = 1
            if i in '0123456789':
                h = 1
        if g == 0 and s == 0:
            s = 'В пароле должны присутствовать маленькие буквы'
        if o == 0 and s == 0:
            s = 'В пароле должны присутствовать заглавные буквы'
        if h == 0 and s == 0:
            s = 'В пароле должны присутствовать цифры'
        if s != 0:
            form.s = s
            return render_template('registration.html', title='соцсеть.рф', form=form)
        else:
            form.s = ''
            result = []
            for us in table.query(User).all():
                result.append(us.name)
            if a in result:
                s = 'Это имя пользователя уже занято.'
                form.s = s
                return render_template('registration.html', title='соцсеть.рф', form=form)
            user.name = a
            user.email = e
            user.set_password(form.password.data)
            user.created_date = datetime.datetime.now()
            table.add(user)
            table.commit()
        return redirect('/search')
    return render_template('registration.html', title='соцсеть.рф', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')