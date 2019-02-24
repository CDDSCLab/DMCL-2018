#-*- coding=utf8 -*-
# @Time 	:2018-11-27
# @Author	:ehds

import threading
import queue
class Lock:

		def __init__(self):
			self.monitor = threading.RLock()

		def acquire_read(self):
			self.monitor.acquire()


		def acquire_write(self):
			self.monitor.acquire()


		def release(self):
			  self.monitor.release()