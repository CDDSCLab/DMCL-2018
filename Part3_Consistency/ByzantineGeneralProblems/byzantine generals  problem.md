# byzantine generals  problem

```
introduction
	拜占庭将军在敌军军营之外的几个山上，将军通过士兵往返来传递信息，这些将军需要决定一个进攻的时间，但是这些将军中间可能有背叛者（背叛者会阻止这些忠诚的将军达成一致），在这种情况下，如何用一个算法来保证一致性的达成？需要设计一个算法满足A、B两点
	A.所有忠诚的将军都会决定采取同样的行动计划（All loyal generals decide upon the same plan of action.）
		忠诚的将军按照算法执行，不忠诚的不按照，算法需要消除背叛者的影响
	B.少部分的背叛者不能导致忠诚的将军给出错误的判断
		
```

将军如何达成一致

```
	假设：有N个将军
	1.每个将军观察敌人并且和其他将军交流，vi是将军i观察给出的信息。
	2.每个将军综合分析收到的v1,v2,...,vn 得出一个行动结果。
	用一样的综合分析方法，可以保证A；用一个稳健的方法可以保证B（Condition B is achieved by using a robust method.）
	最终的决定是在v1,v2,...,vn中的大多数。
	只有背叛者在总人数占一半才会影响结果，此时进攻或者撤退都不能说是一个坏决定。
	
	然而此方案不可行，因为满足条件A要求每一个忠诚的将军获得相同的值v(1)……而一个背叛的将军可能会给不同的将军给出不同的值。
	满足条件A需要：
	1.每个忠诚的将军得到相同的v (1) . . . . , v (n).
		此条件表示vi不一定直接从第i个将军处得到，可能导致第i个将军发的值和其他将军收到的不一样，即使i将军是忠诚的。
	2.如果将军i是忠诚的发出vi，那么其他的将军必须用发出的值vi
	1'. Any two loyal generals use the same value of v(i).
	
	Byzantine Generals Problem. A commanding general must send an order to
his n - 1 lieutenant generals such that
	
	IC1. All loyal lieutenants obey the same order.
	IC2. If the commanding general is loyal, then every loyal lieutenant obeys the
order he sends.
 	IC1 and IC2 are called the interactive consistency conditions（交互一致性），这里commander需要是忠诚的。
	
```

2.不能得到一致结果的情况

```
The Byzantine Generals Problem seems deceptively simple. Its difficulty is
indicated by the surprising fact that if the generals can send only oral messages,
then no solution will work unless more than two-thirds of the generals are loyal.
```

![1544527193111](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1544527193111.png)

```
	An oral message is one whose contents are completely under the control of the sender, so a traitorous sender can transmit any possible message.Such a message corresponds to the type of message that computers normally send to one another.
	口头的消息完全取决于发送者，背叛者可以随意发送可能的消息。
```





​	

