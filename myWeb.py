import os
import sqlite3
from flask import Flask, render_template, session, redirect, url_for,request,jsonify,json
from flask_wtf import FlaskForm

from wtforms import (StringField, BooleanField, DateTimeField,
RadioField, SelectField, TextField,
TextAreaField,SubmitField,HiddenField)
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete,create_engine
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
import webtest,webtest2
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///sales.db', echo = True)
basedir = os.path.abspath(os.path.dirname(__file__))#路徑
app = Flask(__name__) #建立類別實體 讓呼叫本模組時，可以使程式工作
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir, 'data.sqlite')


class MyForm(FlaskForm):
    name = StringField('你的名字', validators=[DataRequired()])
    email = StringField('你的email', validators=[DataRequired()])
    #agreed = BooleanField('同意加入這個組織？')
    #gender = RadioField('請輸入性別', choices=[('M','男生'),('F','女生')])
    #hobby = SelectField('你的興趣', choices=[('sports','運動'),('travel','旅遊'),('movie','電影')])
    #others= TextAreaField()
    submit = SubmitField("確認")

class MyFormtwo(FlaskForm):
    name = StringField('王的名字', validators=[DataRequired()])
    lv = StringField('王的等級', validators=[DataRequired()])
    hp = StringField('王的血量', validators=[DataRequired()])
    exp = StringField('王的經驗', validators=[DataRequired()])
    url = StringField('王的圖連結', validators=[DataRequired()])
    submit = SubmitField("確認")

class DeleteForm(FlaskForm):
    delete_name = HiddenField("Hidden table row name")
    delete = SubmitField("Delete")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
class students(db.Model):
    id = db.Column('student_id', db.Integer)
    name = db.Column(db.String(100), primary_key = True)
    email = db.Column(db.String(50))  

def __init__(self, name, email):
    self.name = name
    self.email = email
    

class bosses(db.Model):
    id = db.Column('boss_id', db.Integer)
    name = db.Column(db.String(100),primary_key = True)
    lv = db.Column(db.String(50))  
    hp = db.Column(db.String(50))  
    exp = db.Column(db.String(50))
    url = db.Column(db.String(50))   

def __init__(self, bname,lv,hp,exp,url):
    self.bname = bname
    self.lv = lv
    self.hp = hp
    self.exp = exp
    self.url = url




@app.route('/')  #使用route()裝飾器 讓程式知道下面的函式要載入在哪個url位址中
def home(): #2
    return render_template('home.html',**locals())#第一個name 是指版型hello.html上面會用到的參數1，而後面的name則是指透過@route路由傳遞進來hello()函式的name2。
    #name=name 改成**locals()也可以，意思是傳遞所有的參數與區域變數。
    #return f"{name}, Welcome. This is Home Page"

@app.route('/home/tms') 
def tms():
    all_url=[]
    with open("static/data/input.json", "r" ,encoding='UTF-8') as json_data:
        all_url = json.load(json_data)
        json_data.close()
    return render_template("tms.html", input=all_url)

@app.route('/home/tmsnews', methods=['GET']) 
def tmsnews():
    webtest.news()
    return redirect(url_for('tms'))
    

@app.route('/home/submit')
def submit():
        return render_template("/R/submit.html",students = students.query.all())

@app.route('/home/show')
def show():
        return render_template("/R/show.html",students = students.query.all())


@app.route('/home/change2',methods=['GET'])
def change2():
        return render_template("change2.html")

@app.route('/home/rms') 
def rms(): 
    all_urlrms=[]
    with open("static/data/input2.json", "r" ,encoding='UTF-8') as j:
        all_urlrms = json.load(j)
        j.close()
    return render_template("rms.html", input=all_urlrms)

@app.route('/home/rmsnews', methods=['GET']) 
def rmsnews():
    webtest2.rmsnews()
    return redirect(url_for('rms'))

@app.route('/home/rms/A',methods=["POST","GET"]) 
def A():
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
        #session['name'] = form.name.data
        #session['email'] = form.email.data
        #session['agreed'] = form.agreed.data
        #session['gender'] = form.gender.data
        #session['hobby'] = form.hobby.data
        #session['others'] = form.others.data
            addstudent = students(name=form.name.data, email=form.email.data)
            db.session.add(addstudent)
            db.session.commit()
            db.session.close()
            return redirect(url_for('submit')) 
    return render_template('/R/A.html', form=form)

@app.route('/home/rms/B') 
def B():
    return render_template('/R/B.html',**locals())

@app.route('/home/rms/boss') 
def boss():
    return render_template('/R/boss.html',  bosses = bosses.query.all())

@app.route('/home/rms/bossdelete', methods=['GET','POST']) 
def bossdelete():
    delete_form = DeleteForm()
    if request.method == 'POST':
        if delete_form.validate_on_submit():
            boss = bosses.query.get(delete_form.delete_name.data)
            db.session.delete(boss)
            db.session.commit()
            db.session.close()
            return redirect(url_for('boss'))
    return render_template('/R/bossdelete.html', bosses= bosses.query.all(),delete_form=delete_form)



@app.route('/home/rms/bossupdate',methods=["POST","GET"]) 
def bossupdate():
    form = MyFormtwo()
    if request.method == 'POST':
        if form.validate_on_submit():
            addboss = bosses(name=form.name.data, lv=form.lv.data,hp=form.hp.data, exp=form.exp.data,url=form.url.data)
            db.session.add(addboss)
            db.session.commit()
            db.session.close()
            return redirect(url_for('boss'))
    return render_template('/R/bossUpdate.html', form=form)

@app.route('/home/rms/dojo') 
def dojo():
    return render_template('/R/dojo.html',**locals())

    
@app.route('/home/rms/lhc') 
def lhc():
    return render_template('/R/lhc.html',**locals())
    
@app.route('/home/rms/123') 
def kk():
    return render_template('/R/123.html',**locals())

def create_table(db):
    db.create_all()


def drop_table(db):
    db.drop_all()



if __name__ == '__main__':
    create_table(db)
    app.run(host="0.0.0.0", debug = True )
#https://ithelp.ithome.com.tw/articles/10222132
#https://medium.com/seaniap/python-web-flask-get-post%E5%82%B3%E9%80%81%E8%B3%87%E6%96%99-2826aeeb0e28
#https://ithelp.ithome.com.tw/articles/10223616
#https://www.1ju.org/flask/flask-sqlalchemy
#https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/454833/
#https://blog.csdn.net/phoenix339/article/details/96431010
#https://ithelp.ithome.com.tw/articles/10258223
#https://zhuanlan.zhihu.com/p/45471645
#https://ithelp.ithome.com.tw/articles/10282830
#https://stackoverflow.com/questions/19141073/rendering-a-dictionary-in-jinja2
#https://stackoverflow.com/questions/65795295/delete-individual-sqlalchemy-row-from-an-html-table-with-flask
#https://medium.com/seaniap/python-web-flask-%E5%AF%A6%E4%BD%9C-flask-migrate%E6%9B%B4%E6%96%B0%E8%B3%87%E6%96%99%E5%BA%AB-a5ebc930422a
#https://blog.csdn.net/weixin_45477432/article/details/102409230
#https://stackoverflow.com/questions/65795295/delete-individual-sqlalchemy-row-from-an-html-table-with-flask
#https://zhuanlan.zhihu.com/p/23605845
#https://github.com/tototoco/maplepic
#https://stackoverflow.com/questions/57891275/simple-fetch-get-request-in-javascript-to-a-flask-server
#https://stackoverflow.com/questions/56812996/how-to-display-json-data-using-for-loop-with-flask