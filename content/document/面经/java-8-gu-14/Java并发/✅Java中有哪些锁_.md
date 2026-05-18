---
title: "Java中有哪些锁_"
date: 2026-03-22T01:02:01+08:00
draft: false
categories:
  - Java并发
---

# 典型回答


这个问题可太大了，因为所有的锁都可以回答。因为我们可以根据不同的分类方式进行介绍。



如果只提Java内置的锁的话，那么主要就是`**synchronized**`** 和**`**ReentrantLock**`这两种锁。



[✅synchronized和reentrantLock区别？]({{< ref "Java并发/✅synchronized和reentrantLock区别？.md" >}})



通过`**synchronized**`** 和**`**ReentrantLock**`的相同点和不同点来说的话，可以有这么几种锁的定义。



+ **阻塞锁&非阻塞锁：**拿不到锁时线程挂起，直到被唤醒，比如 `synchronized` 、ReentrantLock都是阻塞锁。
+ **可重入锁VS不可重入锁**：
    - 可重入锁：一个线程可以多次获取同一把锁（计数器+1，释放时-1），比如 `synchronized`、`ReentrantLock`。
+ **公平锁VS非公平锁**：`synchronized` 和 `ReentrantLock` 默认都是非公平锁。

[✅公平锁和非公平锁的区别？]({{< ref "Java并发/✅公平锁和非公平锁的区别？.md" >}})

+ **偏向锁、轻量级锁、重量级锁**：涉及到`synchronized`的锁膨胀的过程。

[✅synchronized的锁升级过程是怎样的？]({{< ref "Java并发/✅synchronized的锁升级过程是怎样的？.md" >}})

+ **乐观锁VS悲观锁**：这是代码中比较常用的用来做并发防控的，一般在数据库层面出现的比较多。`synchronized`、`ReentrantLock`都是悲观锁，CAS是乐观锁

[✅乐观锁与悲观锁如何实现？]({{< ref "MySQL/✅乐观锁与悲观锁如何实现？.md" >}})

+ **读写锁 VS StampedLock：**StampedLock支持 悲观读锁、写锁，还支持 乐观读，比 `ReadWriteLock` 性能更好。
+ **自旋锁：**线程不会立即阻塞，而是通过循环等待锁释放，避免线程切换开销。JVM 在 `synchronized` 的轻量级锁中用到。

[✅CAS一定有自旋吗？]({{< ref "Java并发/✅CAS一定有自旋吗？.md" >}})

+ **分布式锁VS 单机锁：**

[✅锁和分布式锁的核心区别是什么？]({{< ref "分布式/✅锁和分布式锁的核心区别是什么？.md" >}})

+ **数据库锁**

[✅介绍下InnoDB的锁机制？]({{< ref "MySQL/✅介绍下InnoDB的锁机制？.md" >}})

+ **无锁**：如volatile、不可变模式、ThreadLocal等。（为啥要提这个，因为他也是一种解决并发问题的方案）

[✅如何实现无锁化编程？]({{< ref "Java并发/✅如何实现无锁化编程？.md" >}})

+ **活锁 VS 死锁**

[✅什么是活锁，和死锁有什么区别？]({{< ref "Java并发/✅什么是活锁，和死锁有什么区别？.md" >}})

