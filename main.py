from datetime import *
from flask import Flask,render_template,request,flash,url_for,redirect,session
from flask_sqlalchemy import SQLAlchemy
from models import db,Todo,User
from auth_helper import AuthHelper
from dotenv import dotenv_values
import os

config = dotenv_values()
print(os.environ)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URL']if "PROD" == config['ENV'] else 'sqlite:///db.sqlite3'

app.config['SECRET_KEY'] = 'todo_list'
app.permanent_session_lifetime = timedelta(days=100)
db.init_app(app)

authHelper = AuthHelper()

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'jwt' in session:
        #TODO:insert the snippet
        user = authHelper.decodeJwt(session['jwt'])
        todos = authHelper.getAllTodos(user['id'])
        # for t in todos:
        #     print(t.content,t.user_id)
        return render_template("all_todos.html",todos=todos,name=user['name'],email=user['email'],)
    else:
        return redirect(url_for('signup'))


@app.route('/create', methods=["GET", "POST"])
def create():
    if request.form['content'] != "":
        user = authHelper.decodeJwt(session['jwt'])
        print(user['id'])
        todo = Todo(
            content=request.form['content'],
            user_id=user['id'],
            createdAt=datetime.now(),
        )
        db.session.add(todo)
        db.session.commit()
    else:
        flash("Type something to add")
    return redirect(url_for('home'))


@app.route('/delete/<id>',methods=['GET','DELETE'])
def delete(id):
    Todo.query.filter(Todo.id == id).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        response = authHelper.login(request.form['email'],request.form['password'])
        if response != 'error':
            session['jwt'] = response
            user = authHelper.decodeJwt(session['jwt'])
            flash("Login was Successfull")
            return redirect(url_for('home',name=user['name'],email=user['email']))
        else:
            print("An error occured check your password")
            return redirect(url_for("login",error="Check your email and password"))
    else:
        if 'jwt' in session:
            user = authHelper.decodeJwt(session['jwt'])
            return redirect(url_for('home',name=user['name'],email=user['email']))
    return render_template("login.html",error=None)

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST":
        #user = User(name=request.form['name'],email=request.form['email'])
        jwt = authHelper.signup(name=request.form['name'],email=request.form['email'],password=request.form['password'])
        if jwt:
            session['jwt'] = jwt
            user = authHelper.decodeJwt(session['jwt'])
            # print(user)
            return redirect(url_for('home',name=user['name'],email=user['email']))
        else:
            print("Sign up Error")
    else:
        if 'jwt' in session:
            user = authHelper.decodeJwt(session['jwt'])
            return redirect(url_for('home',name=user['name'],email=user['email']))
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('jwt',None)
    return render_template("login.html",error=None)
if __name__ == '__main__':
   app.run(debug=True)