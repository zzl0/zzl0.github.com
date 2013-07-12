---
layout: post
title: 邻近整数对
tags: [Python, Algorithm]
---

## 问题来源

用户在点了某个商品的收藏连接时，可以直接对齐评论，现在想知道这种点收藏连接后理解对商品进行评论的次数。


## 问题描述

两个整数集合A和B，返回符合下面条件的整数对(a, b)

1. a属于A，b属于B
2. 0 <= b - a < K （K是一个常数，如2）
3. 每个数字只能属于一个整数对

## 一个简单的解答

{% highlight python %}
def int_pairs(A, B, K):
    """两个整数集合A和B，返回符合下面条件的整数对(a, b)

    1. a属于A，b属于B
    2. 0 <= b - a < K （K是一个常数，如2）
    3. 每个数字只能属于一个整数对
    """
    A, B = sorted(A), sorted(B)
    pairs = []
    i, j = 0, 0
    while i < len(A) and j < len(B):
        diff = B[j] - A[i]
        if diff >= K:
            i += 1
        elif diff < 0:
            j += 1
        else:
            pairs.append((A[i], B[j]))
            i += 1
            j += 1
    return pairs

if __name__ == '__main__':
    A = [1, 7, 8, 3]
    B = [2, 10,  4, 8]
    print int_pairs(A, B, 2)
{% endhighlight %}

该算法首先对两个整数集合进行排序，然后遍历两个列表。如果记```n = max(len(A), len(B))```其时间复杂度为O(nlog(n)).

## 完了吗？

上面的方法是否最优的，如果其中有个集合的length比较小呢，例如如果A的length为1，那么我们不需要对集合B排序，就可以很方便找到线性的方法。如果允许数字重复出现呢？如何改现有的算法？

## 结束语

其实这个问题比较简单，但是考虑多了也挺有意思的。
