
import datetime

from flask import Flask, render_template
from sqlalchemy import or_

from data.users import User
from data.mes import Message
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_session.global_init("users2.db")
    db_sess = db_session.create_session()
    message = list(db_sess.query(Message).filter((Message.user_name.in_(['Пользователь 2', 'Пользователь 3'])), (Message.user_to_name.in_(['Пользователь 2', 'Пользователь 3']))))
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


    #message = db_sess.query(Message).filter(Message.user_name == "Пользователь 2", Message.user_to_name == "Пользователь 3")
                                            #(Message.user_name == "Пользователь 3", Message.user_to_name == "Пользователь 2"))
    return render_template("index2.html", message=reslst)


if __name__ == '__main__':
    app.run(port=8088, host='127.0.0.1')
