---
title: "22年毕业，培训了2个月Java，多线程，Spring"
date: 2026-03-22T00:53:36+08:00
draft: false
categories:
  - 面经实战
---

# 面试者背景


:::warning
22年毕业，培训了Java 2个月，双非二本，非科班

怎么理解面向对象？什么是多态？Java是值传递还是引用传递？值传递

AQS介绍一下？state是什么类型，state的修改是怎么改的？state=1表示什么？

AQS有哪些具体实现？reentrantLock和synchronized区别是啥？

公平锁和非公平锁区别是啥？公平锁的缺点？reentrantLock是如何实现公平锁和非公平锁的？

你觉得用synchronized和reentrant哪个好？synchronized锁的是什么？锁对象和锁类有区别吗？

同一个类中有两个synchronized方法，能被两个线程同时执行吗？同一个线程可以吗？重入怎么判断？为啥要做成可重入？死锁了解么？什么情况会发生死锁？如何解决死锁的问题？

如何创建一个线程？子线程抛异常，主线程能捕获到吗？start和run区别是啥

主子线程的执行顺序是怎么样的？守护线程知道吗？

实现功能：统计Spring的某个bean中的某个方法被调用多少次？如果不让改动bean的类呢？

用过spring中的哪些注解？@Service、@Compotent区别是啥？

同一个接口有多个实现，如何指定该注入哪个实现？

SpringEvent用过吗？IOC控制反转是啥意思？把什么反转了，谁反转给谁了？

Spring有几种注入方式？平常用哪个？字段注入IDEA有没有给警告？

Spring和SpringBoot最大的区别是啥？简化开发，内置web服务器？内置了哪些web服务器？

讲讲Spring的循环依赖问题？二级缓存就够了？

Mysql主键一定是自增的吗？建表一定要有主键吗？隐藏row_id干嘛用的？聚簇索引

如果没有创建主键，一定会创建隐藏主键吗？如果有这时候有唯一键一定就不会了吗？

主键用自增ID和UUID哪个好？自增ID有缺点吗？

分库分表字段怎么选的，雪花算法？按照ID分表？查询怎么办？

日志输出用的什么框架，slf4j只是个门面，日志怎么输出的？

Maven出现了jar冲突，该怎么解决？删一个，

:::

# 题目解析


:::color4
**怎么理解面向对象？什么是多态？Java是值传递还是引用传递？值传递**

:::



[✅如何理解面向对象和面向过程？]({{< ref "Java基础/✅如何理解面向对象和面向过程？.md" >}})



[✅Java是值传递还是引用传递？]({{< ref "Java基础/✅Java是值传递还是引用传递？.md" >}})



:::color4
**AQS介绍一下？state是什么类型，state的修改是怎么改的？state=1表示什么？**

**AQS有哪些具体实现？**

:::



[✅如何理解AQS？]({{< ref "Java并发/✅如何理解AQS？.md" >}})



:::color4
**reentrantLock和synchronized区别是啥？**

**公平锁和非公平锁区别是啥？公平锁的缺点？reentrantLock是如何实现公平锁和非公平锁的？**

:::



[✅synchronized和reentrantLock区别？]({{< ref "Java并发/✅synchronized和reentrantLock区别？.md" >}})



[✅公平锁和非公平锁的区别？]({{< ref "Java并发/✅公平锁和非公平锁的区别？.md" >}})



:::color4
**你觉得用synchronized和reentrant哪个好？synchronized锁的是什么？锁对象和锁类有区别吗？**

:::



[✅synchronized锁的是什么？]({{< ref "Java并发/✅synchronized锁的是什么？.md" >}})



:::color4
**同一个类中有两个synchronized方法，能被两个线程同时执行吗？同一个线程可以吗？重入怎么判断？为啥要做成可重入？死锁了解么？什么情况会发生死锁？如何解决死锁的问题？**

:::



[✅什么是可重入锁，怎么实现可重入锁？]({{< ref "Java并发/✅什么是可重入锁，怎么实现可重入锁？.md" >}})



[✅什么是死锁，如何解决？]({{< ref "Java并发/✅什么是死锁，如何解决？.md" >}})



:::color4
**如何创建一个线程？子线程抛异常，主线程能捕获到吗？start和run区别是啥**

**主子线程的执行顺序是怎么样的？守护线程知道吗？**

:::



[✅创建线程有几种方式？]({{< ref "Java并发/✅创建线程有几种方式？.md" >}})



[✅run/start、wait/sleep、notify/notifyAll区别?]({{< ref "Java并发/✅run/start、wait/sleep、notify/notifyAll区别？.md" >}})



[✅为什么不能在try-catch中捕获子线程的异常?]({{< ref "Java并发/✅为什么不能在try-catch中捕获子线程的异常_.md" >}})



[https://www.yuque.com/hollis666/ec96i7/dlg6vw](https://www.yuque.com/hollis666/ec96i7/dlg6vw)





:::color4
**实现功能：统计****Spring****的某个****bean****中的某个方法被调用多少次？如果不让改动****bean****的类呢？**

**用过****spring****中的哪些注解？****@Service****、****@Compotent****区别是啥？**

**同一个接口有多个实现，如何指定该注入哪个实现？**

:::



[✅如何统计一个Bean中的方法调用次数]({{< ref "Spring/✅如何统计一个Bean中的方法调用次数.md" >}})



[✅Spring中@Service 、@Component、@Repository等注解区别是什么？]({{< ref "Spring/✅Spring中@Service 、@Component、@Repository等注解区别是什么？.md" >}})



@Qualifier注解



:::color4
**SpringEvent用过吗？IOC控制反转是啥意思？把什么反转了，谁反转给谁了？**

**Spring有几种注入方式？平常用哪个？字段注入IDEA有没有给警告？**

:::



[✅介绍一下Spring的IOC]({{< ref "Spring/✅介绍一下Spring的IOC.md" >}})



[✅为什么Spring不建议使用基于字段的依赖注入？]({{< ref "Spring/✅为什么Spring不建议使用基于字段的依赖注入？.md" >}})



:::color4
**Spring和SpringBoot最大的区别是啥？简化开发，内置web服务器？内置了哪些web服务器？**

:::



[✅SpringBoot和Spring的区别是什么？]({{< ref "Spring/✅SpringBoot和Spring的区别是什么？.md" >}})



:::color4
**讲讲Spring的循环依赖问题？二级缓存就够了？**

:::



[✅三级缓存是如何解决循环依赖的问题的？]({{< ref "Spring/✅三级缓存是如何解决循环依赖的问题的？.md" >}})



[✅Spring解决循环依赖一定需要三级缓存吗？]({{< ref "Spring/✅Spring解决循环依赖一定需要三级缓存吗？.md" >}})



:::color4
**Mysql主键一定是自增的吗？建表一定要有主键吗？隐藏row_id干嘛用的？聚簇索引**

**如果没有创建主键，一定会创建隐藏主键吗？如果有这时候有唯一键一定就不会了吗？**

:::



[✅MySQL的主键一定是自增的吗？]({{< ref "MySQL/✅MySQL的主键一定是自增的吗？.md" >}})



:::color4
**主键用自增ID和UUID哪个好？自增ID有缺点吗？**

:::



[✅uuid和自增id做主键哪个好，为什么？]({{< ref "MySQL/✅uuid和自增id做主键哪个好，为什么？.md" >}})



:::color4
**分库分表字段怎么选的，雪花算法？按照ID分表？查询怎么办？**

:::



[✅分表字段如何选择？]({{< ref "分库分表/✅分表字段如何选择？.md" >}})



:::color4
**日志输出用的什么框架，slf4j只是个门面，日志怎么输出的？**

**Maven出现了jar冲突，该怎么解决？删一个，**

:::



[✅为什么不能直接使用Log4j、Logback中的 API？]({{< ref "日志/✅为什么不能直接使用Log4j、Logback中的 API？.md" >}})



[✅Maven如何解决jar包冲突的问题？]({{< ref "Maven&Git/✅Maven如何解决jar包冲突的问题？.md" >}})

