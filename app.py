from flask import Flask,request, url_for, redirect, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from urllib import parse
import json
import sqlite3
import logging
import random
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
    tags = db.Column(db.Text)

    def __repr__(self) -> str:
        return f'Sentence {self.id}<br><h6 class="badge rounded-pill bg-primary">Tags : {self.tags}</h6><br>{self.content}'

# All server functions

with app.app_context():
    db.create_all()

@app.route('/',methods=["GET","POST"])
def home_page():
    if request.method == "POST":
        randomres=request.form.get("random","false")
        if randomres=="false":
            search = '' + str(request.form.get("search")) + ''
            search = parse.quote(search)
    #     print(f"Search for {search}.")
    #     t = Sentence.query.filter(Sentence.content.endswith(search))
    #     print(t)
    #     contents = t.all()
        # contents = Sentence.query.all()
        # if search != "#all":
        #     for i in contents:
        #         if not (search in str(i.content)):
        #             contents.remove(i)
            return redirect(f"/search/{search}")
        contents = Sentence.query.all()
        r = random.choice(contents)
        return redirect(f"/sentence/{r.id}")
        
    else:
        return render_template("home/index.htm")

@app.route('/search/<text>')
def searchfor(text):
    # search = '' + str(request.form.get("search")) + ''
    search = parse.unquote(text)
    contents = Sentence.query.all()
    if search != "#all":
        flag = False
        if search[0] == "#":
            flag = True
            search = search[1:]
        for i in contents:
            if flag:
                if not (search in str(i.tags)):
                    contents.remove(i)
            elif not (search in str(i.content)):
                contents.remove(i)
    return render_template("home/search.htm", all_content=contents)

@app.route('/sentence/<int:id>')
def getsentence(id):
    res = Sentence.query.filter(Sentence.id==id)[0]
    return render_template("home/getsentence.htm", id=res.id , sentence = res.content, tags=res.tags)

@app.route('/post_sentence',methods=["GET","POST"])
def post_sentence():
    if request.method == "POST":
        new_sentence = Sentence(content=request.form.get("sentence"),tags=request.form.get("tags"))
        db.session.add(new_sentence)
        db.session.commit()
        return "You have successfully posted a sentence!"
    else:
        return render_template("home/post_sentence.htm")

@app.route('/droptable/<key>/<id>')
def droptable(key,id):
    if key=="clear111":
        for i in Sentence.query.all():
            if (id=="all")or(str(id)==str(i.id)):
                db.session.delete(i)
        db.session.commit()
        return "Query free.jpg"
    

if __name__ == '__main__':
    app.run(debug=True)