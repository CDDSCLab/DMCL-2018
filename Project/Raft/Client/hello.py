from flask import Flask
from flask import render_template
from client import request,requestNode
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	#return 'hello'+str(name)
	return render_template('index.html', name=name)


@app.route('/addValue/<data>')
def addValue(data=None):
	if request(data):
		return 'success'
	else:
		return '无法正确写入数据'

@app.route('/getNodeData/<id>')
def getNodeData(id=None):
	return json.dumps(requestNode(id))