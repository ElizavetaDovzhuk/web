import datetime
import sqlite3

from flask import Flask, render_template
from sqlalchemy import or_

from data.users import User
from data.mes import Message
from data import db_session
from flask import request

q = 0
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        res = []
        con = sqlite3.connect('users3.db')
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM users""").fetchall()
        for elem in result:
            if elem[0] not in res:
                res.append(elem[0])
            print(elem[0])
        con.close()
        return render_template("register.html", pos=res)
    elif request.method == 'POST':
        pos1 = request.form['пользователь']
        print(pos1)
        res = []
        con = sqlite3.connect('users3.db')
        cur = con.cursor()
        result = cur.execute("""SELECT user_to_name FROM messages 
            WHERE user_name='"""+pos1+"""'""").fetchall()
        for elem in result:
            if elem[0] not in res:
                res.append(elem[0])
            print(elem[0])
        con.close()
        return render_template("register2.html", pos=res)

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
            mes = Message(content='', photo=request.form['отправить'], user_name='Пользователь 3',
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
        db_session.global_init("users.db")
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


if __name__ == '__main__':
    app.run(port=8089, host='127.0.0.1')
