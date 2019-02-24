#-*- coding=utf8 -*-
from flask import Flask,Response
from flask import render_template
from flask import request
import time
import threading
lock=threading.Lock()
app = Flask(__name__)
from Transaction import Control
c = Control()
RWhelper = c.DataHelperByLock
## 乐观并发
@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/getall')
def getall():
    return Response(c.getAllData(), mimetype='application/json')

@app.route('/clear')
def clear():
    c.Transtions=[]
    return 'success'
@app.route('/getallbylock')
def getallbylock():
    return Response(RWhelper.getData() , mimetype='application/json')
    
#乐观
@app.route('/optimistic')
def optimistic():
    return render_template('optimistic.html')

@app.route('/read')
def show_user_profile():
    # show the user profile for that user
    id = request.args.get('id', '')
    name = request.args.get('name', '')
    t = c.getTransaction(id)
    if(t):
        return t.read(name)
    else:
        return 'null'

@app.route('/update',methods=['POST', 'GET'])
def update():
    # show the user profile for that user
    id = request.args.get('id', '')
    name = request.args.get('name', '')
    value = request.args.get('value','')
    t = c.getTransaction(id)
    if(t):
        t.update(name,value)
    return name

@app.route('/add',methods=['POST', 'GET'])
def add():
    # show the user profile for that user
    id = request.args.get('id', '')
    name = request.args.get('name', '')
    value = request.args.get('value','')
    t = c.getTransaction(id)
    t.add(name,value)
    return 'true'

@app.route('/commit',methods=['POST', 'GET'])
def commit():
    # show the user profile for that user
    lock.acquire()
    id = request.args.get('id', '')
    lock.release()
    return "success" if c.valid(id) else "fail"


@app.route('/register',methods=['POST', 'GET'])
def register():
    id = request.args.get('id', '')
    if(c.register(id)):
        return '注册成功'
    else:
        return '已经注册或注册失败'
    # show the user profile for that user

@app.route('/test',methods=['POST', 'GET'])
def test():
    global lock
    lock.acquire()
    print(threading.currentThread().name)
    time.sleep(6)
    lock.release()
    return "ee"

#悲观控制
@app.route('/readbylock')
def readbylock():
    name = request.args.get('name', '')
    return RWhelper.read(name)
    
@app.route('/writebylock')
def writebylock():
    name = request.args.get('name', '')
    value = request.args.get('value','')
    try:
        RWhelper.update(name,value)
        return "success"
    except Exception as e:
        return "fail"

@app.route('/addbylock')
def addbyblock():
    name = request.args.get('name', '')
    value = request.args.get('value','')
    try:
        RWhelper.add(name,value)
        return "success"
    except Exception as e:
        return "fail"

@app.route('/withdrawbylock')
def withdrawBylock():
    name = request.args.get('name', '')
    value = request.args.get('value','')
    try:
        RWhelper.withdraw(name,value)
        return "success"
    except Exception as e:
        return "fail"