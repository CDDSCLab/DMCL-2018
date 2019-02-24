#-*- coding=utf8 -*-
import threading
import queue
class RWLock:
		def __init__(self):
			self.wait_writers_q=queue.Queue()
			self.rwlock = 0
			self.writers_waiting = 0
			self.monitor = threading.RLock()
			self.readers_ok = threading.Condition(self.monitor)

		def acquire_read(self):
			self.monitor.acquire()
			#判断当前对象是否可读
			while self.rwlock < 0 or self.writers_waiting:
				#等待信号量
				self.readers_ok.wait()
			self.rwlock += 1
			self.monitor.release()

		def acquire_write(self):
			self.monitor.acquire()
			#判断是否可读
			while self.rwlock != 0:
			  self.writers_waiting += 1
			  writers_ok= threading.Condition(self.monitor)
			  #放入写者队列
			  self.wait_writers_q.put(writers_ok)
			  #等待信号量
			  writers_ok.wait()
			  self.writers_waiting -= 1
			self.rwlock = -1
			self.monitor.release()

		def release(self):
			self.monitor.acquire()
			if self.rwlock < 0:
			  self.rwlock = 0
			else:
			  self.rwlock -= 1
			wake_writers = self.writers_waiting and self.rwlock == 0
			wake_readers = self.writers_waiting == 0
			self.monitor.release()
			if wake_writers:
			  writers_ok=self.wait_writers_q.get_nowait()
			  writers_ok.acquire()
			  #通知一个读者
			  writers_ok.notify()
			  writers_ok.release()
			elif wake_readers:
			  self.readers_ok.acquire()
			  #通知所有读者
			  self.readers_ok.notifyAll()
			  self.readers_ok.release()
if __name__ == '__main__':
		import time
		rwl = RWLock()
		rw2 = RWLock()
		class Reader2(threading.Thread):
			def run(self):
				print(self,'start2')
				rw2.acquire_read()
				print(self,'acquired2')
				time.sleep(2)
				print(self,'stop2')
				rw2.release()

		class Writer2(threading.Thread):
			def run(self):
				print(self,'start2')
				rw2.acquire_write()
				print(self,'acquired2')
				time.sleep(3)
				print(self,'stop2')
				rw2.release()
		class Reader(threading.Thread):
			def run(self):
				print(self,'start')
				rwl.acquire_read()
				print(self,'acquired')
				time.sleep(2)
				print(self,'stop')
				rwl.release()

		class Writer(threading.Thread):
			def run(self):
				print(self,'start')
				rwl.acquire_write()
				print(self,'acquired')
				time.sleep(3)
				print(self,'stop')
				rwl.release()
		threads = []
		# Writer().start()
		for i in range(4):
			threads.append(Writer())
		for i in range(4):
			threads[i].start()
		# Writer().start()
		# Reader().start()
	
		# Reader().start()
		# Writer().start()
		# time.sleep(1)
		# Reader().start()
	
