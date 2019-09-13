# 漫画算法：什么是 B 树？

> 本文转载自[伯乐在线-漫画算法：什么是 B 树？](http://blog.jobbole.com/111757/?utm_source=blog.jobbole.com&utm_medium=relatedPosts)

本文提到的「B-树」，就是「B树」，都是 B-tree 的翻译，里面不是减号-，是连接符-。因为有人把 B-tree 翻成 「B-树」，让人以为「B树」和「B-树」是两种树，实际上两者就是同一种树。

![img](http://upload-images.jianshu.io/upload_images/6954572-9dfcee2118fceda3.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-f8013917eb15a30b.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-9c4fef4f6d1ceb06.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-64618ee347956b6a.jpg)
————————————

![img](http://upload-images.jianshu.io/upload_images/6954572-89ebb111297df0dc.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-d851326d08eefd9e.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-83450603a69d7074.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-6cb577a98b3cee1e.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-8a53c2a5fca58104.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-b43d51948ecc18b3.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-fb04799f1946f3e1.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-9c787142599f0ae7.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-ad8f160b1da92620.jpg)
————————————

![img](http://upload-images.jianshu.io/upload_images/6954572-55748da8c917e161.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-966ebab6d3bae295.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-6e642a1dae12f79e.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-e85d045c0a1037eb.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-36e2d70eced1f1a3.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-2ed66797909a4055.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-9d18fd436a2a1d79.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-742916441c26f81a.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-c99f41ec86634aa0.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-27cf2dcc6a7f25a2.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-9a3a8b8d9885ea87.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-4c882b53e59e75c9.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-0951c4a92f287c47.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-cb98a5a1ca7ebf60.jpg)
**二叉查找树的结构：**

![img](http://upload-images.jianshu.io/upload_images/6954572-8144d32410741c98.jpg)
**第1次磁盘IO：**

![img](http://upload-images.jianshu.io/upload_images/6954572-6e584a37f6503ca6.jpg)
**第2次磁盘IO：**

![img](http://upload-images.jianshu.io/upload_images/6954572-33d980ada7f6f3e7.jpg)
**第3次磁盘IO：**

![img](http://upload-images.jianshu.io/upload_images/6954572-dc910ea8ddc1c14c.jpg)
**第4次磁盘IO：**

![img](http://upload-images.jianshu.io/upload_images/6954572-a4750b5df691763b.jpg)![img](http://upload-images.jianshu.io/upload_images/6954572-b0a656e23c613992.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-a918bc6a7f27c3f5.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-f7acd17b5985c070.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-531ffc0604adfa6a.jpg)
**下面来具体介绍一下B-树（Balance Tree），一个m阶的B树具有如下几个特征：**

1.根结点至少有两个子女。

2.每个中间节点都包含k-1个元素和k个孩子，其中 m/2 <= k <= m

3.每一个叶子节点都包含k-1个元素，其中 m/2 <= k <= m

4.所有的叶子结点都位于同一层。

5.每个节点中的元素从小到大排列，节点当中k-1个元素正好是k个孩子包含的元素的值域分划。

![img](http://upload-images.jianshu.io/upload_images/6954572-f74fae8c24b7e745.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-a32ff066f2f7f758.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-aedb385199565f8e.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-a29170d0b85be61d.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-e4609b4c874c63da.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-b6dadfdf6ab7f53f.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-9b539a438510b6a3.jpg)
**第1次磁盘IO：**

![img](http://upload-images.jianshu.io/upload_images/6954572-1d4cd95e0071b14b.jpg)
**在内存中定位（和9比较）：**

![img](http://upload-images.jianshu.io/upload_images/6954572-0149fbe222e0bcd9.jpg)



**第2次磁盘IO：**

![img](http://upload-images.jianshu.io/upload_images/6954572-c0d8d093477b127b.jpg)
**在内存中定位（和2，6比较）：**

![img](http://upload-images.jianshu.io/upload_images/6954572-7caa74fa6f66803e.jpg)
第3次磁盘IO：

![img](http://upload-images.jianshu.io/upload_images/6954572-2ec1b5ac09af8bb2.jpg)
**在内存中定位（和3，5比较）：**

![img](http://upload-images.jianshu.io/upload_images/6954572-34c873ebfba26681.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-8065477f9c339c76.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-4bca25166b883082.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-a275fca37423136f.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-256795a0ed2b7cb5.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-8062de80bbe99080.jpg)

自顶向下查找4的节点位置，发现4应当插入到节点元素3，5之间。

![img](http://upload-images.jianshu.io/upload_images/6954572-336ac9d94d52954c.jpg)

节点3，5已经是两元素节点，无法再增加。父亲节点 2， 6 也是两元素节点，也无法再增加。根节点9是单元素节点，可以升级为两元素节点。于是**拆分**节点3，5与节点2，6，让根节点9升级为两元素节点4，9。节点6独立为根节点的第二个孩子。

![img](http://upload-images.jianshu.io/upload_images/6954572-f58930efca86023d.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-b76436a5af62c3ca.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-d1c73869c8e1df77.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-f04f2127a511b353.jpg)

自顶向下查找元素11的节点位置。

![img](http://upload-images.jianshu.io/upload_images/6954572-3788235572c9fc99.jpg)
删除11后，节点12只有一个孩子，不符合B树规范。因此找出12,13,15三个节点的中位数13，取代节点12，而节点12自身下移成为第一个孩子。（这个过程称为**左旋**）

![img](http://upload-images.jianshu.io/upload_images/6954572-707464cf091ec504.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-4791013a1811b111.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-5fce73f84f44bfba.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-0a159f04aa51c157.jpg)
![img](http://upload-images.jianshu.io/upload_images/6954572-3040eec9263ce0af.jpg)


注：*由于原始网站未能正常打开，本文图片加载自简书*