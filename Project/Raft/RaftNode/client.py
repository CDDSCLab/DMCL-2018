import xmlrpc.client
import time
import sys
import socket
nodes = []
nodeIds = ["8000", "8001", "8002", "8003", "8004"]
for nodeId in nodeIds:
    node = xmlrpc.client.ServerProxy("http://127.0.0.1:"+nodeId, allow_none=True)

def getLeader(nodes):
    leader = None
    for n in nodes:
        try:
            socket.setdefaulttimeout(3)
            if n.isLeader():
            socket.setdefaulttimeout(None)
                leader = n
                break
        except Exception:
            print('Error')
    return leader

def Request(nodes, clientid, data):
    committed = False
    retryCount = 0
    while committed == False and retryCount < 5:
        try:
            leader = getLeader(nodes)
            print(leader)
            if leader is not None:
                socket.setdefaulttimeout(3)
                committed = leader.RequestClients(clientid, data)
                ocket.setdefaulttimeout(None)
                print(committed)
            if not committed:
                retryCount+=1
        except Exception as e:
            retryCount+=1
            print(e)

    return committed

def request(data):
    clientid = 0 
    global nodes
    return Request(data)

def main():
    return Request('data')

if __name__ == "__main__":
    main()