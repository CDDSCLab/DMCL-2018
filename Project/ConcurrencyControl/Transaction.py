#-*- coding=utf8 -*-
import json

from threading import Lock
from RWLock import RWLock
from Lock import Lock
import time
from abc import ABCMeta, abstractmethod
MAX_NUMBER = 1000000
ItemWriteSet ={}
ItemReadSet= {}

class Transtion(object):
	def __init__(self, id):
		super(Transtion, self).__init__()
		self.id = id
		self.WTS = {}
		self.RTS = []
		self.start = MAX_NUMBER
		self.end = MAX_NUMBER
		self.datahelper = DataHelper()

	def addWriteSet(self,name):
		global ItemWriteSet
		if(name not in ItemWriteSet):
			ItemWriteSet[name] = []
		if(self in ItemWriteSet[name]):
			return
		ItemWriteSet[name].append
	def addReadSet(self,name):
		global ItemWriteSet
		if(name not in ItemWriteSet):
			ItemReadSet[name] = []
		if(self in ItemReadSet[name]):
			return
		ItemReadSet[name].append(self)

	def read(self,name):
		if(name in self.WTS):
			self.RTS.append(name)
			self.addReadSet(name)
			return self.WTS[name]
		res = self.datahelper.read(name)
		if(res):
			self.RTS.append(name)
			self.addReadSet(name)
			return res
		else:
			return "error"


	def add(self,name,value):
		return self.datahelper.add(name,value)

	def update(self,name,value):
		self.WTS[name] = value
		self.addWriteSet(name)
		print(name,value)

	def commit(self):
		for each in self.WTS:
			self.datahelper.update(each,self.WTS[each])

	def rollback(self):
		pass

class Control(object):
	"""用于事件的控制"""
	def __init__(self):
		super(Control, self).__init__()
		self.Transtions = []
		self.DataHelperByLock = DataHelperByLock()
		self.id = 0
	#判断事务是否存活
	def isActive(self,id):
		return len(list(filter(lambda x:x.id == id,self.Transtions)))>0

	#事务注册
	def register(self,id):
		 # TODO: There maybe id is greter than MAX_NUMBER
		 # TODO: mutex
		if(self.isActive(id)):
			return False
		self.id+=1
		t = Transtion(id)
		t.start = self.id
		self.Transtions.append(t)
		return t
	#移除事务
	def remove(self,id):
		for each in list(filter(lambda x,y:x == y.id,self.Transtions)):
			self.Transtions.remove(each)

	def getTransaction(self,id):
		if(self.isActive(id)):
			return (list(filter(lambda x:id == x.id,self.Transtions))[0])
		else:
			return False
	def getAllData(self):
		datahelper = DataHelper()
		return datahelper.getData()

	#判断事务是否合法
	def valid(self,id):
		if(self.isActive(id)):
			#获取事务
			T = self.getTransaction(id)
			#比当前事务要早的事务
			#优化当前验证，去除不必要的事务
			# for item in self.getConflicTrans(T):
			for i in range(self.Transtions.index(T)):
				#如果早点的事务已经提交了，则忽略
				if(self.Transtions[i].end < T.start):
					self.Transtions.remove(self.Transtions[i])
					index = i
					continue
				#比较当前事务的读集是否与较早的事务的写集冲突
				for each in self.Transtions[i].WTS:
					if(each in T.RTS):
						#回滚事务
						T.rollback()
						self.Transtions.remove(T)
						return False
			#事务ID加一
			self.id+=1
			T.end = self.id
			T.commit()
			return True

	def getConflicTrans(self,T):
		res = {}
		for each in T.RTS:
			#合并写的事务
			res |= ItemWriteSet[each]
		#并上比自己先发生的事务
		res &= list(filter(lambda x:x.start<T.start,self.Transtions))
		return res


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

## 整个过程的IO
## 暂且不考虑硬盘
class DataHelper(metaclass=Singleton):
	"""docstring for Data"""
	def __init__(self):
		super(DataHelper, self).__init__()
		self.cache = {}

	def read(self,name):
		if(name in self.cache.keys()):
			return self.cache[name]
		else:
			return False
		#否则从文件里面找
		# else:
		# 	with open(filename,'r') as f:
		# 		data = json.load(f)
		# 		if (data.has_key(name)):
		# 			self.cache[name] = data[name]
		# 			return data[name]
		# 		else:
		# 			return False	
	def update(self,name,value):
		if(name in self.cache):
			self.cache[name] = value
			return True
		else:
			return False
	def add(self,name,value):
		if(name in self.cache):
			self.cache[name] = value
		else:
			self.cache[name] = value
		print(name,value)
		#否则从文件里面找
		# else:
		# 	with open(filename,'r') as f:
		# 		data = json.load(f)
		# 		if (data.has_key(name)):
		# 			self.cache[name] = data[name]
		# 			return data[name]
		# 		else:
		# 			return False
	def getData(self):
		return json.dumps(self.cache)

class Item(object):
	def __init__(self, name,value):
		super(Item, self).__init__()
		self._name = name
		self._value = value
		self.wrlock = Lock()

	@property
	def name(self):
		return self._name

	#Item的属性，相当于read
	@property
	def value(self):
		self.wrlock.acquire_read()
		print("acquire")
		res = self._value
		self.wrlock.release()
		print("release")
		return res

	@value.setter
	def value(self,value):
		self.write(value)

	def read(self):
		pass

	def write(self,value):
		self.wrlock.acquire_write()
		print("acquire write")
		self._value = value
		time.sleep(3)
		self.wrlock.release()
		print("release")
	def withdraw(self,value):
		time.sleep(2)
		self.wrlock.acquire_write()
		self._value=str(int(self.value)-int(value))
		time.sleep(1)
		self.wrlock.release()

class DataHelperByLock(DataHelper):
	"""docstring for DataHelperByLock"""
	def __init__(self):
		super(DataHelperByLock, self).__init__()
	def read(self,name):
		if(name not in self.cache.keys()):
			raise ValueError('Invalid Name %s' % name)
		return self.cache[name].value

	def add(self,name,value):
		if(name in self.cache.keys()):
			return False
		self.cache[name] = Item(name,value)
		print("success")

	def update(self,name,value):
		if(name not in self.cache.keys()):
			raise ValueError('Invalid Name %s' % name)
		self.cache[name].write(value)
	def withdraw(self,name,value):
		if(name not in self.cache.keys()):
			raise ValueError('Invalid Name %s' % name)
		self.cache[name].withdraw(value)
	def remove(self,name,value):
		self.cache.pop(name)
		return True

	def getData(self):
		res = {}
		for each in self.cache:
			res[each] = self.cache[each].value
		return json.dumps(res)
if __name__ == '__main__':
	# v=Valid("uestc")
	# a=Item ("ehds","1994")
	# t = Transtion(0)
	# t2 = Transtion(0)
	# t.appendWTS(a)
	# t2.appendRTS(a)
	# v.register(t)
	# v.register(t2)
	# print(t.id)
	# print(t2.id)

	# c = Control()
	# t1 = c.register(1)
	# t2 = c.register(2)
	# t1.add("hds",1)
	# t1.update("hds",222)
	# t2.read("hds")
	# print(c.valid(t1.id))
	# print(c.valid(t2.id))

	c = DataHelperByLock()
	c.add("ehds",1994)
	c.add("ehds2",1994)
	c.update("ehds2",1995)
	c.read("ehds2")
	print(c.read("ehds2"))
	

