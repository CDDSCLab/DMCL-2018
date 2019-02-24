# 并发控制
## 介绍


这是新生学习的并发控制Project，本项目主要是实现了[乐观并发](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)和[悲观并发](http://iryndin.net/post/optimistic_and_pessimistic_concurrency_control/)两种方式
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





## 如何使用

项目入口文件为hello.py,按照[flask官方文档](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application)的方式启动即可。

windows下可以右击start.ps1，选择PowerShell运行即可。

## 结果展示
### 1. 悲观控制界面 http://127.0.0.1:5000：
![](https://i.loli.net/2019/02/24/5c724246cbc19.png)

说明：一共有三个操作，Add,Read和Write，因为只是并发控制测试所以没有加入删除操作，为了查看效果每个操作都加入了适当的延迟。

界面上共有三个操作框代表三个Client，可以在三个客户端同时操作，绿色框下面是结果展示方便查看当前状态和结果。



### 2. 乐观并发控制界面：http://127.0.0.1:5000/optimistic

![](https://i.loli.net/2019/02/24/5c724365a5457.png)

说明：和悲观控制一样，一共有三个Client。开始事务之前需要点击Start，然后可以开始三个操作，操作完成后要点击Commit提交本次操作。这么做的原因是方便测试查看结果。

# 说明

如果需要测试多个客户端并发情况，具体可以查看test.py下面的代码，测试是用协程写的，可以通过修改测试代码来自定义测试。

如果发现Bug或者需优化的地方欢迎Issue和PullRequest