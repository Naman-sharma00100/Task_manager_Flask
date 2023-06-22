from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
db = SQLAlchemy(app)

class Users(db.Model):
    taskId = db.Column(db.Integer,primary_key = True)
    TaskName = db.Column(db.String(200),nullable=False)
    Desc = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.userId}-{self.TaskName}"


@app.route('/',methods = ['GET','POST'])
def hello_world():
    # creating Task
    if request.method == "POST":
        TaskName = request.form["TaskName"]
        desc = request.form["desc"]
        # print(desc)
        user = Users(TaskName=TaskName,Desc = desc)
        db.session.add(user)
        db.session.commit()
    # return "Hello World..!!"
    allUser = Users.query.all()
    return render_template('index.html',allUser = allUser)

@app.route('/update/<int:taskId>',methods=['GET','POST'])
def update(taskId):
    if request.method == "POST":
        TaskName = request.form["TaskName"]
        desc = request.form["desc"]
        user = Users.query.filter_by(taskId = taskId).first()
        user.TaskName = TaskName
        user.Desc = desc
        # db.session.add(user)
        db.session.commit()
        return redirect("/")

    user = Users.query.filter_by(taskId = taskId).first()
    return render_template("update.html", user = user)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/delete/<int:taskId>')
def delete(taskId):
    user = Users.query.filter_by(taskId = taskId).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

@app.route('/show')
def new_func():
    allUser = Users.query.all()
    print(allUser)
    return "this is my new func..!!"

if __name__ == "__main__":
    app.run(debug=True)