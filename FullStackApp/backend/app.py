from flask import Flask, render_template, request, redirect, session
import sqlite3
    import os

app = Flask(__name__)
app.secret_key = "secret"

def init_db():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            course TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("register.html")


@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user=cur.fetchone()
        conn.close()

        if user:
            session["user"]=username
            return redirect("/dashboard")
        else:
            return "Login Failed"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html",user=session["user"])
    return redirect("/")


@app.route("/add", methods=["GET","POST"])
def add():
    if "user" not in session:
        return redirect("/")

    if request.method=="POST":
        name=request.form["name"]
        course=request.form["course"]

        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        cur.execute("INSERT INTO students(name,course) VALUES(?,?)",(name,course))
        conn.commit()
        conn.close()
        return redirect("/list")

    return render_template("add.html")


@app.route("/list")
def list_records():
    if "user" not in session:
        return redirect("/")

    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM students")
    data=cur.fetchall()
    conn.close()
    return render_template("list.html",data=data)


@app.route("/delete/<int:id>")
def delete(id):
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/list")


@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")


if __name__=="__main__":


app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
