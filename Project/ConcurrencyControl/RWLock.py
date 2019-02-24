#-*- coding=utf8 -*-
# @Time 	:2018-11-27
# @Author	:ehds

import threading
import queue
class RWLock:
		"""
		A simple reader-writer lock Several readers can hold the lock
		simultaneously, XOR one writer. Write locks have priority over reads to
		prevent write starvation. wake up writer accords to FIFO
		"""
		def __init__(self):
			self.wait_writers_q=queue.Queue()
			self.rwlock = 0
			self.writers_waiting = 0
			self.monitor = threading.RLock()
			self.readers_ok = threading.Condition(self.monitor)

		def acquire_read(self):
			"""Acquire a read lock. Several threads can hold this typeof lock.
		It is exclusive with write locks."""
			self.monitor.acquire()
			while self.rwlock < 0 or self.writers_waiting:
				self.readers_ok.wait()
			self.rwlock += 1
			self.monitor.release()

		def acquire_write(self):
			"""Acquire a write lock. Only one thread can hold this lock, and
		only when no read locks are also held."""
			self.monitor.acquire()
			while self.rwlock != 0:
			  self.writers_waiting += 1
			  writers_ok= threading.Condition(self.monitor)
			  self.wait_writers_q.put(writers_ok)
			  writers_ok.wait()
			  self.writers_waiting -= 1
			self.rwlock = -1
			self.monitor.release()

		def release(self):
			"""Release a lock, whether read or write."""
			self.monitor.acquire()
			if self.rwlock < 0:
			  self.rwlock = 0
			else:
			  self.rwlock -= 1
			wake_writers = self.writers_waiting and self.rwlock == 0
			wake_readers = self.writers_waiting == 0
			self.monitor.release()
			if wake_writers:
			  # print "wake write..."
			  writers_ok=self.wait_writers_q.get_nowait()
			  writers_ok.acquire()
			  writers_ok.notify()
			  writers_ok.release()
			elif wake_readers:
			  self.readers_ok.acquire()
			  self.readers_ok.notifyAll()
			  self.readers_ok.release()