# -*-coding=utf8 -*-
# @Author： ehds
import json
import datetime
#日志使用Json格式保存，方便转换成字典#

#日志的格式
class Entry(object):
	"""docstring for Entry"""
	def __init__(self, id,term,data):
		super(Entry, self).__init__()
		self._id = id
		self._term = term
		self._data = data

	def format(self):
		entry = {}
		entry['timestamp'] = str(datetime.datetime.now())
		entry["term"] = self._term
		entry["client"] = self._id
		entry["data"] = str(self._data)
		return entry
        
#用于记录和读取日志的类
class Loger(object):
	def __init__(self,path):
		self._path = path
		print(self._path)

	def WriteLog(self,log):
		#TO-DO：优化日志的写
		with open(self._path,'w+') as f:
			json.dump(log,f)
		return True

	def ReadLog(self):
		#TO-DO：优化日志的读
		with open(self._path,'r') as f:
			log = json.load(f)
			return log

def test():
	log = []
	loger = Loger('./log/raftlogjson%s.json'%'23')
	entry = {}
	entry['timestamp'] = str(datetime.datetime.now())
	entry['client'] =132
	entry['term'] =123
	entry['data'] ='存钱100'
	log.append(entry)
	loger.WriteLog(log)
	logread = loger.ReadLog()

	if(logread[0]['client']==log[0]['client']):
		print("success")



if __name__ == '__main__':
	test()