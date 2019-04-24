# 漫画算法：什么是 B 树？

2017/07/09 · [IT技术](http://blog.jobbole.com/category/it-tech/), [趣文小说](http://blog.jobbole.com/category/humor-comic/) · [5 评论 ](http://blog.jobbole.com/111757/#article-comment)· [算法](http://blog.jobbole.com/tag/algorithm/)



本文作者： [伯乐在线](http://blog.jobbole.com/) - [玻璃猫](http://www.jobbole.com/members/bjweimengshu) 。未经作者许可，禁止转载！
欢迎加入伯乐在线 [专栏作者](http://blog.jobbole.com/99322)。

> 伯乐在线补充：本文提到的「B-树」，就是「B树」，都是 B-tree 的翻译，里面不是减号-，是连接符-。因为有人把 B-tree 翻成 「B-树」，让人以为「B树」和「B-树」是两种树，实际上两者就是同一种树。

![img](http://jbcdn2.b0.upaiyun.com/2017/07/f4156a04d1ce10e1d6b6e119ce1fc3db.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/fc713400ca8ce73e4d4f7b656974a270.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/98d1b3066e41fa6e28ad131e4f04f2d5.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/4cb37c6fcae8dbb405cb4b8ed10112aa.jpg)

————————————

![img](http://jbcdn2.b0.upaiyun.com/2017/07/70f82597c6205ae0b915cf9446605986.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/fbb934ec8ef90054d26303d34bb27a24.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/616f5e86b4cf206dcfee036fd55e9602.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/ce70b97a696efa28520a19e5adea080c.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/54f122a98313bd4f61c2e95d9858eaf6.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/06556ae2f9f1dbf3bc798b350a97290a.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/b159585a12d50e1fbfffa2d892fde68f.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/40fb54cfbec0e48c40e3f01d79f2cc3e.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/89cca300c77afb89a592d252de98f012.jpg)

————————————

![img](http://jbcdn2.b0.upaiyun.com/2017/07/f2ab28eb6aa7b3efce6c000aed8ccba2.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/29249cf3f3edddb4eb738a4b05eff361.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/0264f0d13bce4acf176e0e67412e02d8.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/093de5649072fa0e9118d6b47ea4c39f.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/0aa46ad4cff77069122a89d83238dd02.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/1516c8202da7f5df1ba479edeff75d9e.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/70d834f21e6e7a482270817f1ef9b66a.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/6a5c3760c3b6375ab7f3db270c833205.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/423081a186bb730f6246d4fc88fe8397.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/35e21257dd7649cbf648f8a12c9526bf.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/be4e8c9eea941021983b3a0ec2e30fe7.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/c8115df892823961e16b58e50f2745f7.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/3fc378e0a26f0a455b5de0c2b9085d0e.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/2540a2a93236be26570e7cfed001dd0c.jpg)

**二叉查找树的结构：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/a48d291a87e8f7451d7096f06c28a266.jpg)

**第1次磁盘IO：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/c3afbbed4dc8d9ab0eb28f36c525eb64.jpg)

**第2次磁盘IO：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/eaaadd8563fe9c2ce028b356b4b1b972.jpg)

**第3次磁盘IO：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/29510bc7455978e0a4b76538c481d211.jpg)

**第4次磁盘IO：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/e776aad15f9db6791ed4ece4cebf179b.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/519a5ecae2049027e151f56404221cd6.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/57a3d2232bdc3602101d26de6af70629.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/dfe811439d5a4b83908d1aece65b2858.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/a551a5af0899d0f4487d5174c879fbee.jpg)

**下面来具体介绍一下B-树（Balance Tree），一个m阶的B树具有如下几个特征：**

1.根结点至少有两个子女。

2.每个中间节点都包含k-1个元素和k个孩子，其中 m/2 <= k <= m

3.每一个叶子节点都包含k-1个元素，其中 m/2 <= k <= m

4.所有的叶子结点都位于同一层。

5.每个节点中的元素从小到大排列，节点当中k-1个元素正好是k个孩子包含的元素的值域分划。

![img](http://jbcdn2.b0.upaiyun.com/2017/07/3bdde769e986c29df17ee5a05e2283f5.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/1053258e35bc3a11daa6a35c0a4876a5.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/7b6f7416cab11f23fa141cbcbe5ae97b.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/e4bab35b22e04f408f20d9d78dd1ada7.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/1da23fc560320dd7fc33c4250f7bc62f.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/a18c14c033cc7773cbc5417b47c8433e.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/e00c03897682ce16665f1fc6a103fae5.jpg)

**第1次磁盘IO：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/a9bff5a34ad1b721c406d49aa5f71c7f.jpg)

**在内存中定位（和9比较）：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/e7aad0107f143df4d294f6d4ddc2efca.jpg)

**第2次磁盘IO：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/55f9ffb7ec69c5624d3d38c3e487619f.jpg)

**在内存中定位（和2，6比较）：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/7181bf7db0d93d67a6d19e98bdec086a.jpg)

第3次磁盘IO：

![img](http://jbcdn2.b0.upaiyun.com/2017/07/c7d939ddbd73ea5a28ab7c895e996d1e.jpg)

**在内存中定位（和3，5比较）：**

![img](http://jbcdn2.b0.upaiyun.com/2017/07/6e00c658824f6979d5c2a6526adcdd07.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/6a8d6dd48be32ff61f0a20955c3f1231.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/e067432832fd13a46e588a4165f6f2e9.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/150acc7b44a31e028d53b97e44e6a7f7.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/301f7f8c3add3183aa7fcc85a6ac584c.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/07469afd080afb68036063ba808965f1.jpg)

自顶向下查找4的节点位置，发现4应当插入到节点元素3，5之间。

![img](http://jbcdn2.b0.upaiyun.com/2017/07/b19105d47fd35c8b0d1e7ed2248bdaa0.jpg)

节点3，5已经是两元素节点，无法再增加。父亲节点 2， 6 也是两元素节点，也无法再增加。根节点9是单元素节点，可以升级为两元素节点。于是**拆分**节点3，5与节点2，6，让根节点9升级为两元素节点4，9。节点6独立为根节点的第二个孩子。

![img](http://jbcdn2.b0.upaiyun.com/2017/07/1a708a324257d422e594224c6f7afad4.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/60daf22a13c44bec7cd0384a04fe9e12.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/ebf569b446c84c77405395ea1503477c.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/ed7fea3cc0eeab4fac24420dfa6a57c0.jpg)

自顶向下查找元素11的节点位置。

![img](http://jbcdn2.b0.upaiyun.com/2017/07/ca7856622c48d55fbf9502f4ef8219b7.jpg)

删除11后，节点12只有一个孩子，不符合B树规范。因此找出12,13,15三个节点的中位数13，取代节点12，而节点12自身下移成为第一个孩子。（这个过程称为**左旋**）

![img](http://jbcdn2.b0.upaiyun.com/2017/07/f5f4b28523d3d381b63c11b7ab3ac7d3.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/8d567b18da9582a3dbed613232117001.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/7041d2780cb7fa9bf64af19b6476dc2f.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/04191ffe9d9fa92c54b4375b8b3da210.jpg)

![img](http://jbcdn2.b0.upaiyun.com/2017/07/0fd1168e35ccc3953584f971f38c75b5.jpg)