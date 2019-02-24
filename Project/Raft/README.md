# SimpleRaft
## 介绍
这是对[raft论文](https://raft.github.io/raft.pdf)提出算法的简单实现

Raft是一种易于理解的共识算法。 它在容错和性能方面与Paxos相当。 不同之处在于它被分解为相对独立的子问题，并且它干净地解决了实际系统所需的所有主要部分

Raft 通过选举一个领导者（Leader），然后给予他全部的管理复制日志的责任来实现一致性。领导人从客户端接收日志条目，把日志条目复制到其他服务器上，并且当保证安全性的时候告诉其他的服务器应用日志条目到他们的状态机中。
本次项目是在学习过程中实现的，可能还存在许多的不足，欢迎指正。
## 环境
### 一 编程语言
![](https://i.loli.net/2019/01/25/5c4ac59ecaa07.png)

版本：3.6+

requires:
1. flask


### 二 框架
![](https://i.loli.net/2019/01/25/5c4ac59ec10b5.png)
![](https://i.loli.net/2019/01/25/5c4ac59ec1dda.png)
![](https://i.loli.net/2019/01/25/5c4ac59ed4916.png)

## 流程图
![](https://i.loli.net/2019/01/25/5c4ac99154af2.png)

## 使用

分别打开Client和RaftNode文件夹start.bat即可
然后打开http://127.0.0.1：5000/hello

## 结果展示
前台：
![](https://i.loli.net/2019/01/25/5c4ac784e89d3.png)
后端日志
![](https://i.loli.net/2019/01/25/5c4ac7c036aef.png)

## TO-DO
1. 未加入动态节点变化
2. 动态配置节点数目(懒）
