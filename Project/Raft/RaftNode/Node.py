# -*- coding=utf8 -*-
import math
import os.path
import pickle
import random
import socket
import asyncio
import sys
import logging
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading
import time
from ResetableTimer import TimerReset as Timer#ResetableTimer
from Entry import Loger,Entry
from Role import Role,RoleName

class Node(object):
    
    def __init__(self,id):

        self.id = str(id)
        self.nodes = []
        self.loop = None
        # persistent - update before responding to RPC
        self.currentTerm = 0
        self.maxTerm = 0
        self.votedFor = None
        self.numLog = 0
        self.log = []
        # volatile (all)
        self.commitIndex = 0
        self.lastApplied = 0

        # volatile (leader)
        self.nextIndex = []
        self.matchIndex = []


        self.role = Role.Follower

        self.electionTimeout = self.getTimeout()
        self.startTime = time.clock()
        self.votes = 0

        self.socketTimeout = None

        self.clientRunning = False
        self.leaderLock = threading.Lock()

        self.FollowerTimer = Timer(self.electionTimeout,self.initCandidate)
        self.CandidateTimer = None
        # Used for debugging
        self.nextState = 'None'
        self.nextTerm = -1


        # initial log entry
        self.log.append(Entry(self.id,self.currentTerm,'Start').format())
        self.numLog = 1
        self.initLog()
        self.running = True

    def initLog(self):
        self.loger = Loger('./log/raftlog%s.json'%self.id)

    def writeLog(self):
        self.loger.WriteLog(self.log)

    def readLog(self):
        self.log = self.loger.ReadLog(self.log)
        self.numLog = len(self.log)

    def setCurrentTerm(self, t):
        self.currentTerm = t

    def setVotedFor(self, v):
        self.votedFor = v

    def getTimeout(self):
        return random.randint(1,5)

    def hearbetTimout(self):
        return 5.0

    def getLogIndex(self):
        return self.numLog-1

    def getLogTerm(self):
        if self.numLog == 0:
            return 0
        entry = self.log[self.numLog-1]
        return entry["term"]


    def initFollower(self, term):
        #print 'Convert to Follower'
        self.role = Role.Follower
        self.setCurrentTerm(term)
        self.setVotedFor(None)
        self.runFollower()

    def initCandidate(self):
        self.role = Role.Candidate
        self.setCurrentTerm(self.currentTerm+1)
        self.electionTimeout = self.getTimeout()
        self.runCandidate()

    def initLeader(self):
        self.role = Role.Leader
        self.nextIndex = []
        self.matchIndex = []

        for n in self.nodes:
            self.nextIndex.append(self.getLogIndex()+1)
            self.matchIndex.append(0)
        self.runLeader()


    def runFollower(self):
        #开始follower的定时器
        self.FollowerTimer.cancel()
        self.FollowerTimer=Timer(self.electionTimeout,self.initCandidate)
        self.FollowerTimer.start()
    # Send vote requests to all other nodes

    async def BroadCastCandidate(self,i):
        lastLogIndex = self.getLogIndex()
        lastLogTerm = self.getLogTerm()
        n = self.nodes[i]
        try:
            term,success =await loop.run_in_executor(None,n.requestVoteRPC,self.currentTerm, self.id, lastLogIndex, lastLogTerm)
            if term > self.currentTerm:
                self.maxTerm = term
            if success == True:
                self.votes += 1
        except Exception as e:
            print(e)

    def runCandidate(self):
        self.votes = 1
        #给自己投一票
        self.setVotedFor(self.id)
        tasks = []
        for i in range(len(self.nodes)):
            tasks.append(self.BroadCastCandidate(i))
        loop.run_until_complete(asyncio.wait(tasks))
        if self.maxTerm > self.currentTerm:
            print("选举失败\n")
            self.initFollower(self.maxTerm)
        if self.votes > math.ceil((len(self.nodes))/2.0):
            self.initLeader()
        else:
            print("未获得大多数人同意\n")
            self.initFollower(self.currentTerm)

    async def BroadCastHearbet(self,i):
        global loop
        n = self.nodes[i]
        prevLogIndex = self.nextIndex[i]-1
        prevLogTerm = self.log[prevLogIndex]["term"]
        entries = self.log[self.nextIndex[i]:]
        try:
            socket.setdefaulttimeout(self.socketTimeout)
            term,success = await loop.run_in_executor(None,n.appendEntriesRPC,self.currentTerm, self.id,prevLogIndex, prevLogTerm,entries, self.commitIndex)
            socket.setdefaulttimeout(None)
            if term > self.currentTerm:
                self.maxTerm = term
            if success:
                self.nextIndex[i] = self.getLogIndex()+1
            elif success == False:
                self.nextIndex[i] -= 1
        except Exception as e:
            print("无法达到%s"%str(n))

    def runConcurrentLeader(self):
        print("我是领导者%s\r\n"%self.id)
        global loop
        # leaderloop = asyncio.get_event_loop()
        tasks1 = []
        for i in range(0, len(self.nodes)):
            tasks1.append(self.BroadCastHearbet(i))
        while self.isLeader():
            self.leaderLock.acquire()
            loop.run_until_complete(asyncio.wait(tasks1))
            if self.maxTerm > self.currentTerm:
                self.initFollower(self.maxTerm)
                print("选举失败\n")
                break
            self.initFollower(self.maxTerm)
            time.sleep(1)
            self.leaderLock.release()

    def runLeader(self):
        print("我是领导者%s\r\n"%self.id)
        while self.isLeader():
            self.leaderLock.acquire()
            for i in range(0, len(self.nodes)):
                n = self.nodes[i]
                prevLogIndex = self.nextIndex[i]-1
                prevLogTerm = self.log[prevLogIndex]["term"]
                entries = self.log[self.nextIndex[i]:]
                try:
                    socket.setdefaulttimeout(3)
                    term,success = n.appendEntriesRPC(self.currentTerm, self.id,prevLogIndex, prevLogTerm,entries, self.commitIndex)
                    socket.setdefaulttimeout(None)
                    if term > self.currentTerm:
                        self.initFollower(term)
                        break
                    if success == True:
                        self.nextIndex[i] = self.getLogIndex()+1
                    elif success == False:
                        self.nextIndex[i] -= 1
                except Exception as e:
                    print(e)
                    print("无法达到%s"%str(n))
            self.leaderLock.release()
            time.sleep(1)

    def appendLog(self):
        self.leaderLock.acquire()
        commitCount = 1
        for i in range(0, len(self.nodes)):
            n = self.nodes[i]
            prevLogIndex = self.nextIndex[i]-1
            prevLogTerm = self.log[prevLogIndex]["term"]
            entries = self.log[self.nextIndex[i]:]
            try:
                socket.setdefaulttimeout(self.socketTimeout)
                term,success = n.appendEntriesRPC(self.currentTerm, self.id,prevLogIndex, prevLogTerm,entries, self.commitIndex)
                socket.setdefaulttimeout(None)

                if term > self.currentTerm:
                    self.initFollower(t)
                    break
                if success == True:
                    self.nextIndex[i] = self.getLogIndex()+1
                    commitCount += 1
                elif success == False:
                    self.nextIndex[i] -= 1
            except Exception as e:
                print(e)
        self.leaderLock.release()
        return commitCount

    def runThread(self):
        global loop
        loop = asyncio.get_event_loop()
        handler = { Role.Follower:self.runFollower,
                    Role.Candidate:self.runCandidate,
                    Role.Leader:self.runLeader
                }

        if self.role == Role.Null:
            self.role = self.Follower
        handler[self.role]()

    def requestVoteRPC(self, term, candidateId, lastLogIndex, lastLogTerm):
        print('投票给'+str(candidateId))
        if term < self.currentTerm:
            return (self.currentTerm, False)
        elif term > self.currentTerm:
            self.initFollower(term)

        # 当前term 与当前Term 相等
        if (self.votedFor is None) or (self.votedFor == candidateId):
            # 如果没有比自己多的commit的日志
            if (self.getLogTerm() > lastLogTerm) or (self.getLogTerm() == lastLogTerm) and (self.getLogIndex() > lastLogIndex):
                return (self.currentTerm, False)
            else:
                self.setVotedFor(candidateId)
                return (self.currentTerm, True)
        
        return (self.currentTerm, False)


    # 由领导人负责调用来复制日志指令；也会用作heartbeat 当Entries为空时就是心跳包
    def appendEntriesRPC(self, term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
        print('♡~♡~~♡~~~~ 来自'+str(leaderId)+'任期'+str(term))
        if term < self.currentTerm:
            return (self.currentTerm, False)
        elif term > self.currentTerm:
            self.initFollower(term)

        # 获得心跳
        self.electionTimeout = self.hearbetTimout()
        # 接收到心跳包

        #重置计时器
        self.FollowerTimer.reset(self.electionTimeout+self.getTimeout())

        #如果当前Log的长度大于Leader的log

        if prevLogIndex < len(self.log):
            entry = self.log[prevLogIndex]
            logTerm = entry["term"]

            if logTerm == prevLogTerm:
                self.log = self.log[:(prevLogIndex+1)] + entries
                self.writeLog()
                # 如果LeaderCommit 大于 当前自己提交的日志则覆盖
                if leaderCommit > self.commitIndex:
                    self.commitIndex = leaderCommit

                return (self.currentTerm, True)

        return (self.currentTerm, False)

    def isLeader(self):
        return self.role == Role.Leader

    def RequestClients(self, client, data):

        print('请求 ' + str(client) + ' ' + str(data))
        self.numLog += 1
        self.log.append(Entry(client,self.currentTerm,str(data)).format())
        isCommit = False

        while isCommit == False and self.role == Role.Leader:
            commitCount = self.appendLog()
            if commitCount > math.ceil((len(self.nodes))/2.0):
                isCommit = True
                self.writeLog()
                self.commitIndex += 1
        return isCommit
    
    def getLogs(self):
        return self.log

def main(argv):
    #print argv

    node = Node(argv[0])
    print("Id:%s"%node.id)
    nodes = ["8000", "8001", "8002", "8003", "8004"]
    nodes.remove(node.id)
    print(nodes)

    server = SimpleXMLRPCServer(("", int(node.id)), logRequests=False,allow_none=True)
    server.register_instance(node)

    for nodeId in nodes:
        n = xmlrpc.client.ServerProxy("http://127.0.0.1:"+nodeId, allow_none=True)
        node.nodes.append(n)

    t = threading.Thread(target=server.serve_forever)
    t.start()

    threading.Thread(node.runThread()).start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main(sys.argv[1:])

#TO-DO 更改彩色显示
#TO-DO fix majoriy agreement