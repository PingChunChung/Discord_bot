from flask import Flask, render_template, redirect, url_for
from threading import Thread

app = Flask('')
Users = {}
Rows = {}
data = []

def setUsers(_u):
  global Users
  Users = _u
  print("setUsers")
  
def setRows(_r):
  global Rows
  Rows = _r
  print("setRows")
  
def setDatas(_d):
  global data
  data = _d
  print("setData")

@app.route("/")
def index():
  return render_template("./html/index.html", data=data)


@app.route("/users")
def users():
  return render_template("./html/users.html", Users=Users)

def keep_alive():
  t = Thread(target=run)
  t.start()

def run():
  app.run(host='0.0.0.0', port=8080)#,debug=True)