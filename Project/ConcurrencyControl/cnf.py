#cnf.py
import multiprocessing
import asyncio

lock = multiprocessing.Lock()
 
def pre_request(worker, req)
    req.headers['FLASK_LOCK'] = lock
 
pre_request = pre_request
bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count()
worker_class = 'gevent'
