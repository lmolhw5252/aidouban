from queue import Queue
import random
import threading
import time
import mysql.connector
import requests


class Producer(threading.Thread):
    def __init__(self,t_name,queue):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):
            print("%s,%s is producing %d the queue!\n" %(time.ctime,self.getName(),i))
            self.data.put(i)
            time.sleep(random.randrange(10)/5)
        print("%s:%s finished!" %(time.ctime(),self.getName()))


#consumer thread
class Consumer(threading.Thread):
    def __init__(self,t_name,queue):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):
            self.data.get()
            print("%s,%s is producing %d the queue!\n" %(time.ctime,self.getName(),i))
            time.sleep(random.randrange(10))
        print("%s:%s finished!" %(time.ctime(),self.getName()))


def testset():
    session  = requests.session()
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
        "Connection": "keep-alive",
        "Cookie":'id="BFKy6waSza8"; ll="118254"; viewed="3395865_26232736"; ap=1; __utmt_douban=1; __utmt=1; __utma=30149280.195434174.1433063610.1433067174.1433071714.4; __utmb=30149280.14.10.1433071714; __utmc=30149280; __utmz=30149280.1433067174.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E5%8C%97%E6%9E%81%E7%86%8ACaf%C3%A9; __utma=223695111.1800995804.1433071744.1433071744.1433071744.1; __utmb=223695111.7.10.1433071744; __utmc=223695111; __utmz=223695111.1433071744.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf6=a45a8cc7de19cea4.1433071744.1.1433073446.1433071744.; _pk_ses.100001.4cf6=*'
    }
    reponse = session.get("http://book.douban.com/",headers=headers,)
    print(reponse.headers)
    print(reponse.request.headers)
    print(reponse.status_code)

def test456():
    config = {
    "user":"root",
    "password":"root",
    "host":"127.0.0.1",
    "database":"aidouban",
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    #query
    querysql = "select * from movie WHERE url = %s "
    # queryvalue = "http://movie.douban.com/subject/25823531/"
    queryvalue = "123"
    result = cursor.execute(querysql,(queryvalue,))
    print(len(cursor.fetchall()))
    print(cursor)
    print(result)
if __name__ == '__main__':
    # queue = Queue()
    #
    # producer = Producer('Pro.', queue)
    #
    # consumer = Consumer('Con.', queue)
    #
    # producer.start()
    #
    # consumer.start()
    #
    # # producer.join()
    #
    # # consumer.join()
    #
    # print ("All threads terminate!")
    # testset()
    test456()