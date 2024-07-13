from flask import Flask,request, url_for, redirect, flash, render_template
import json
import sqlite3
import logging
app = Flask(__name__)

connection = sqlite3.Connection("texts.db")
cursor = sqlite3.Cursor(connection)
cursor.execute('DROP TABLE IF EXISTS USER')
cursor.execute("create table user ( name varchar(51) not null, content varchar(1025) not null )")
cursor.close()
connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        name = str(request.form.get('name')) # 传入表单对应输入字段的 name 值
        content = str(request.form.get('content'))
        connection = sqlite3.Connection("texts.db")
        cursor = sqlite3.Cursor(connection)
        cursor.execute('insert into user (name, content) values (?,?)',(name,content))
        cursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('index.htm')

@app.route('/user-all-texts/<name>')
def user_all_texts(name:str):
    logging.info("Select texts for user "+str(name))
    connection = sqlite3.Connection("texts.db")
    cursor = sqlite3.Cursor(connection)
    cursor.execute("select * from user where name = ?",(str(name),))
    return json.dumps(cursor.fetchall())

@app.route('/all-texts/')
def all_texts():
    connection = sqlite3.Connection("texts.db")
    cursor = sqlite3.Cursor(connection)
    cursor.execute("select * from user")
    # request.headers.add_header("Access-Control-Allow-Origin","*")
    return render_template("all-texts.htm",texts=cursor.fetchall())

@app.route('/clear-all-text/<code>')
def clear(code:int):
    logging.info("Someone wants to clear the table with code "+str(code) )
    if int(code) == 1457348:
        connection = sqlite3.Connection("texts.db")
        cursor = sqlite3.Cursor(connection)
        cursor.execute('DROP TABLE IF EXISTS USER')
        cursor.execute("create table user ( name varchar(51) not null, content varchar(1025) not null )")
        cursor.close()
        connection.close()
        return "Successfully droped table!"
    return "You have no right to drop table!"