# Studienarbeit python文件记录日日志

## 2021年2月2日晚

~~~
分别写了UDP在PC端和LabView端的python程序，思路如下：
1. PC端通过一个input函数得到需要采样的个数，将这个数字发送给LabView端
2. LabView端收到后判断所接受内容，若是整数（因为采样数只能是整数），则产生对应个数的复数，是以np.array的形式
3. 将np.array用np.savetxt方法保存，名字格式为‘采样数 年月日时分秒’
4. 将此文件分批发送，因为文件太大，UDP一次发送不出去
5. 在PC端做相应工作来接收文件，存在指定文件下
~~~
~~~ 
今天只完成了初步工作，能做到他俩之间彼此通信，互相发送字符串。名字分别是：
[UDP在LabView端.py](https://github.com/fedroger/happyhour/blob/main/UDP%E5%9C%A8LabView%E7%AB%AF.py)
[UDP在PC端.py](https://github.com/fedroger/happyhour/blob/main/UDP%E5%9C%A8PC%E7%AB%AF.py)
~~~
## 2021年2月3日晚
~~~
完成了昨天需要的功能，存在一个问题：
当需要采样的个数小于1000或1000左右，程序完美运行，太大时LabView端成功生成文件并保存，但是PC端接受总是不成功。强制restart kernel后，文件出现在了对应目录里，但是只有部分数据。比如要求5000个采样复数，csv文件里只有1000多，但这种情况下，文件大小都是一样的，均为64kB，正好是UDP所接受的最大数据量，但不知道原因，因为编的时候已经考虑到这种问题所以是把原文件切片了。
~~~
~~~
今天的两个程序分别为：

~~~