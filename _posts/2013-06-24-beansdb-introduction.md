---
layout: post
title: Beansdb学习
tags: [Beansdb, Nosql]
---

## 使用

先从github上获取Beansdb的源代码(https://github.com/douban/beansdb)，然后按照里面INSTALL文件安装beansdb.

查看Python客户端代码dbclient.py，其自带的测试代码如下:

{% highlight python %}
NSDBCFG = {
    "localhost:7901": range(16),
    "localhost:7902": range(16),
    "localhost:7903": range(16),
}

db = Beansdb(BEANSDBCFG, 16)

def _test():
    u = "/test"
    data = "teatdata" * 100
    assert db.set(u, data)
    #assert db.exists(u)
    assert db.get(u) == data
    assert db.get_multi([u]) == {u:data}
    assert db.delete(u)
    assert db.get(u) is None

if __name__ == '__main__':
    _test()
    pass
{% endhighlight %}

安装memcache包后，在本地启动3个实例，然后运行dbclient.py，顺利执行！

## 分析dbclient.py

dbclient.py文件的最顶层包含：

* fnv1a：一个哈希函数。
* MCStore：memcache客户端的封装。
* WriteFailedError：自定义的异常类。
* Beansdb：Beansdb客户端类。

### Beansdb类

Beansdb类包含的函数如下：

* `__init__`
* `print_buckets`
* `_get_servers`
* `set`
* `get`
* `get_multi`
* `delete`

#### 初始化函数

{% highlight python %}
def __init__(self, servers, buckets_count=16, N=3, W=1, R=1):
	self.buckets_count = buckets_count
	self.bucket_size = self.hash_space / buckets_count
	self.servers = {}
	self.server_buckets = {}
	self.buckets = [[] for i in range(buckets_count)]
	for s,bs in servers.items():
	    server = MCStore(s)
	    self.servers[s] = server
	    self.server_buckets[s] = bs
	    for b in bs:
	        self.buckets[b].append(server)
	for b in range(self.buckets_count):
	    self.buckets[b].sort(key=lambda x:fnv1a("%d:%s:%d"%(b,x,b)))
	self.N = N
	self.W = W
	self.R = R
{% endhighlight %}

其中参数servers是服务器的配置，示例中的配置如下：

{% highlight python %}
NSDBCFG = {
    "localhost:7901": range(16),
    "localhost:7902": range(16),
    "localhost:7903": range(16),
}
{% endhighlight %}

配置中的key是server，value是buckets。Beansdb类接受到这个配置后，初始化其内部的变量，我们可以通过`print_buckets`函数查看初始化后的buckets和server_buckets的信息，对于上面的配置其输出如下：

{% highlight bash %}
zzl@zzl:python$ py test_dbclient.py
buckets的值
0 localhost:7901,localhost:7903,localhost:7902
1 localhost:7902,localhost:7903,localhost:7901
2 localhost:7903,localhost:7902,localhost:7901
3 localhost:7901,localhost:7903,localhost:7902
4 localhost:7903,localhost:7902,localhost:7901
5 localhost:7902,localhost:7903,localhost:7901
6 localhost:7901,localhost:7902,localhost:7903
7 localhost:7902,localhost:7903,localhost:7901
8 localhost:7903,localhost:7902,localhost:7901
9 localhost:7901,localhost:7902,localhost:7903
10 localhost:7902,localhost:7903,localhost:7901
11 localhost:7902,localhost:7903,localhost:7901
12 localhost:7902,localhost:7903,localhost:7901
13 localhost:7901,localhost:7902,localhost:7903
14 localhost:7901,localhost:7902,localhost:7903
15 localhost:7902,localhost:7901,localhost:7903

server_buckets的值（严格来说下面的输出并不是server_buckets的值）
localhost:7901 16
localhost:7903 16
localhost:7902 16
{% endhighlight%}

#### set函数

{% highlight python %}
def set(self, key, value):
	 rs = [s.set(key, value) for s in self._get_servers(key)]
	 if not rs.count(True) >= self.W:
	     # try to get, it will return False when set same content into db
	     if self.get(key) != value:
	         raise WriteFailedError(key)
	 return True
{% endhighlight %}

我的理解是set的时候，是向所有key所对应的server中写，只要成功写入W个即可。`但是代码的逻辑是只要get(key)所获得的值等于value就算作写入成功，同时我也没理解那句注释的意思`。

#### get函数

{% highlight python %}
def get(self, key):
    ss = self._get_servers(key)
    for i,s in enumerate(ss):
        r = s.get(key)
        if r is not None:
            # self heal
            for k in range(i):
                ss[k].set(key, r)
            return r
{% endhighlight%}

get的时候就是遍历key所对应的server，直到得到非空的值，同时把这个值写入已经遍历过的那些server中，下次就可以更快返回，这也是一种自我治愈（self heal）的过程。

## 测试函数

最后给出一个测试函数，我用它来检验自己的理解，其他的函数比较直观，在此不再赘述。

{% highlight python %}
#!/usr/bin/python

from dbclient import Beansdb

BEANSDBCFG = {
    "localhost:7901": range(16),
    "localhost:7902": range(16),
    "localhost:7903": range(16),
}


db = Beansdb(BEANSDBCFG, 16, W=2)


def _inspect():
    assert db.set('a', 1)
    assert db.get('a') == 1

    assert db.set('b', 2)
    assert db.get('b') == 2

    assert db.get_multi(['a', 'b']) == {'a':1, 'b':2}

    assert db.delete('a')
    assert db.get('a') == None

if __name__ == '__main__':
    _inspect()
    pass
{% endhighlight %}






