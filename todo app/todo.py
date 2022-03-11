from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////todo app/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos=todos)

@app.route("/add",methods=["POST"])
def add():
    title = request.form.get("title")
    content = request.form.get("content")
    
    new_todo = Todo(title = title,content = content,complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>",methods = ["GET"])
def complete(id):
    todo = Todo.query.filter_by(id=id).first()
    if (todo.complete == False):
        todo.complete = True
    else:
        todo.complete = True
    
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))
    

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)
    

if __name__ == "__main__":
    app.run(debug=True)