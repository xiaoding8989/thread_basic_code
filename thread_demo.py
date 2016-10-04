# usr/bin/env python
# -*-coding:utf-8 -*-
import threading
import time
import random

def worker_func():
    print('worker thread is start ad %s'%threading.current_thread())
    random.seed()#seed( ) 用于指定随机数生成时所用算法开始的整数值，
    time.sleep(random.random())#random.random()生成一个0到1的随机浮点数
    print('worker thread is finished at %s'%threading.current_thread())


#带锁的线程
def worker_func_lock(lock):#传个锁进来  一个时间只会有一个线程在执行这个函数
    lock.acquire()#上锁   当第一个线程进来的时候它会请求这个锁，当第二个线程进来的时候它会在外面等待
    worker_func()#当第一个进程释放锁后第二线程才会进来执行这个函数
    lock.release()#释放锁

gLock=threading.Lock()#定义一个锁
gSem=threading.Semaphore(3)  #信号量 同一时间允许3个线程在执行
gRlock=threading.RLock()

def simple_thread_demo():
    for i in range(10):
        #threading.Thread(target=worker_func).start()
        #threading.Thread(target=worker_func_lock,args=[gLock]).start()
        threading.Thread(target=worker_func_lock,args=[gSem]).start()

#构建生产者与消费者模型
gPool=1000 #金库里原始的钱
gCondition=threading.Condition()

class Producer(threading.Thread):  #生产者的线程往金库里存钱
    def run(self):  #重写run方法
        print('%s started' % threading.current_thread())
        while True:   #不停地往金库里放钱
            global gPool #申明全局变量
            global gCondition

            gCondition.acquire()  # 上锁
            random.seed()
            p = random.randint(500,1000)
            gPool += p#往金库里放钱
            print('%s: Produced %d. Left %d' % (threading.current_thread(), p, gPool))
            time.sleep(random.random())
            gCondition.notify_all()  # 这时门口排了很长的队，需要通知所有人
            gCondition.release()  # 通知完后释放锁
#构建消费者模型，不停的往金库里拿钱
class Consumer(threading.Thread):
    def run(self):
        print('%s started' % threading.current_thread())
        while True:
            global gPool
            global gCondition

            gCondition.acquire() #上锁
            random.seed()
            c = random.randint(100, 200)
            print('%s: Trying to consume %d. Left %d' % (threading.current_thread(), c, gPool))
            while gPool < c:
                gCondition.wait()
            gPool -= c
            time.sleep(random.random())
            print('%s: Consumed %d. Left %d' % (threading.current_thread(), c, gPool))
            gCondition.release()

def consumer_producer_demo():
    for i in range(10):  #创建一个消费者
        Consumer().start()

    for i in range(1):   #创建一个生产者
        Producer().start()

if __name__=="__main__":
    #simple_thread_demo()
    consumer_producer_demo()


