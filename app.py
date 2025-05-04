from flask import Flask,request, url_for, redirect, flash, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import sqlite3
import logging
app = Flask(__name__)

class GlobalLogger():
    lgname = ""
    def __init__(self,logger_name:str) -> None:
        self.lgname = logger_name
        self.info = logging.Logger(self.lgname,logging.INFO)
        self.error = logging.Logger(self.lgname,logging.ERROR)
        self.debug = logging.Logger(self.lgname,logging.DEBUG)
        self.warning = logging.Logger(self.lgname,logging.WARNING)

logger = GlobalLogger("Server")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goodtake_server_data.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique = True , nullable = False)
#     password = db.Column(db.String(80), nullable = False)
#     email = db.Column(db.String(120), unique = True, nullable = False)

#     def __repr__(self):
#         return f'<User {self.username}>'

class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)

    def __repr__(self) -> str:
        return f'Sentence {self.id} : {self.content}'

# All server functions

with app.app_context():
    db.create_all()

@app.route('/',methods=["GET","POST"])
def home_page():
    if request.method == "POST":
        search = '' + str(request.form.get("search")) + ''
    #     print(f"Search for {search}.")
    #     t = Sentence.query.filter(Sentence.content.endswith(search))
    #     print(t)
    #     contents = t.all()
        contents = Sentence.query.all()
        if search != "#all":
            for i in contents:
                if not (search in str(i.content)):
                    contents.remove(i)
        return render_template("home/search.htm", all_content=contents)
    else:
        return render_template("home/index.htm")

@app.route('/post_sentence',methods=["GET","POST"])
def post_sentence():
    if request.method == "POST":
        new_sentence = Sentence(content=request.form.get("sentence"))
        db.session.add(new_sentence)
        db.session.commit()
        return "You have successfully posted a sentence!"
    else:
        return render_template("home/post_sentence.htm")

@app.route('/droptable/<key>')
def droptable(key):
    if key=="clear111":
        for i in Sentence.query.all():
            db.session.delete(i)
        db.session.commit()
        return "Query free.jpg"
    

if __name__ == '__main__':
    app.run(debug=True)