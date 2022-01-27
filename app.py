from flask import Flask, request, render_template, url_for, session, redirect
from flask_session import Session

# connetcting with mongoDB
import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://dbUser:dbUserPassword@cluster0.nwori.mongodb.net/flaskData?retryWrites=true&w=majority")
db = cluster["flaskData"]
collection = db["Flask_mongo"]

app = Flask(__name__, static_url_path="", static_folder="")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    if not session.get("userName"):
        return redirect("/login")
    return render_template('dashboard.html')
  
  
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        userName = collection.find_one({"Email": request.form.get("userName"), "passWord": request.form.get("passWord")})
        if userName is not None:
            session["userName"] = request.form.get("userName")
            return redirect("/dashboard")
        return render_template("login.html", error='Invalid login details!')
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        userName = collection.find_one({"Email": request.form.get("userName")})
        if userName is None:
            x = { "fName": request.form.get("fName"),
                  "lName": request.form.get("lName"),
                  "Email": request.form.get("userName"),
                  "passWord": request.form.get("passWord")
                }
            y = collection.insert_one(x)
            session["userName"] = request.form.get("userName")
            return redirect("/dashboard")
        return render_template("register.html", error='Username already exists!')
    return render_template("register.html")
  
@app.route("/logout")
def logout():
    session["userName"] = None
    return redirect("/")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        return render_template('index.html')
    return render_template('upload.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    # app.secret_key = "mysecret"
    app.run(debug=True)
