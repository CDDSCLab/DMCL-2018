#-*- coding=utf8 -*-
import asyncio
import random
import time

async def get(url):
	res = await loop.run_in_executor(None, requests.get, url)
	print(res)

async def hello(i):
    # print("协程" + str(n) +"启动")
    while True:
	    regesiter = await get(generatURL('register',i))
	    add  = await get(generatURL('add',i,name = str(i),value = str(i)))
	    update = await get(generatURL('update',i,name = str(0),value = str(i+1)))
	    read = await get(generatURL('read',i,name=str(0)))
	    commit =  await get(generatURL('commit',i))
	    if(commit):
	    	return
	    else:
	    	print("重做")
	    	await asyncio.sleep(random.randint(0,3))

    # print("协程" + str(n) + "结束")
    # await hello2(n)

if __name__ == "__main__":
    tasks = []
    tasks.append[get('https://baidu.com')]
    tasks.append[get('https://sina.com')]
    tasks.append[get('https://dshale.cn')]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    # tasks = []
    # for i in range(0, 16):
    #     tasks.append(get(""))

    # timestart = time.time()
    # loop = asyncio.get_event_loop()


    # timeend = time.time()
    # print(timeend-timestart)

