from flask_sqlalchemy import SQLAlchemy
from vote import app
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from vote.views import *
from flask_login import UserMixin,LoginManager,current_user,login_user,logout_user
from flask import render_template,url_for,redirect,request

db = SQLAlchemy(app)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(300))

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class Users(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    voterid = db.Column(db.String(50),unique=True)

class Election(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))
    cand = db.relationship("Party",backref="parties")

class Party(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    candidate_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    party_url = db.Column(db.Text())
    votes = db.Column(db.Integer)
    candidate_url = db.Column(db.Text())
    ele = db.Column(db.Integer,db.ForeignKey("election.id"))

class Voted(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    voterid = db.Column(db.String(200),unique=True)


@app.route("/admin_login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("admin.html")
    else:
        pas = request.form["admin_pass"]
        user_pass = User.query.get(1)
        if user_pass.name==pas:
            login_user(user_pass)
            return "logged in"
        else:
            return redirect(url_for("login"))

@app.route("/logout")
def logout():
    logout_user()
    return "Logged out"

    
admin = Admin(app)

admin.add_view(MyModelView(Users,db.session))
admin.add_view(MyModelView(Election,db.session))
admin.add_view(MyModelView(Party,db.session))
admin.add_view(MyModelView(Voted,db.session))

admin.add_view(MyModelView(User,db.session))

