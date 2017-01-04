#the movue queue
from queue import Queue
import random
import threading
import re
import mysql.connector
import requests
import time

q =  Queue(-1)
mutex = threading.Lock()
headers = [{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
          {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
          {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
def geturl(start_url):
    urlspattern = "http://movie.douban.com/subject/\d+/"
    time.sleep(random.randint(1,10))
    index = random.randint(0,2)
    header = headers[index]
    response  =requests.get(start_url,headers=header)
    status_code = int(response.status_code)
    print(status_code)
    if(status_code==403):
        time.sleep(120)
        response  =requests.get(start_url,headers=headers[random.randint(0,2)])
        status_code = int(response.status_code)
        print(status_code)

    #change the proxy url
    html = response.text
    urls = re.findall(urlspattern,html,re.I|re.M)
    #change list to set
    urls = set(urls)
    return urls

def parseHtml(url):
    #insert into db
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
    queryvalue = url
    cursor.execute(querysql,(queryvalue,))
    if not len(cursor.fetchall())==0:
        return
    time.sleep(random.randint(1,10))
    response = requests.get(url,headers=headers[random.randint(0,2)])
    print(response.status_code)
    text = response.text

    #get the show info
    pattern = "<div id=\"info\">\W*.*?</div>"
    items = re.findall(pattern,text,re.M |re.S)
    titlepattern = "<span property=\"v:itemreviewed\">(.*?)</span>"
    title = re.search(titlepattern,text)
    titleinfo = ""
    if(title):
        titleinfo =title.group(1)
        #用空格来区分中文明和英文名
        index = titleinfo.find(" ")
        chntitle = titleinfo[:index]
        print(chntitle)
        entitle = titleinfo[index+1:]
        print(entitle)
    #
    # #get summary
    # summarypattern = "<span property= \"v:summary \" > \((.*?)\) </span>"
    # summary = re.findall(summarypattern)
    # summaryinfo = ""
    # if(summary):
    #     summaryinfo = summary.group(1)

    #get the year
    yearpattern = "<span class=\"year\">\((.*?)\)</span>"
    year = re.search(yearpattern,text)
    if(year):
        print(year.group(1))
        year = year.group(1)

    #get the movie type
    genrepattern = "<span property=\"v:genre\">(.*?)</span>"
    genre =re.findall(genrepattern,text)
    print(genre)
    if len(genre) >1:
        genre = genre[0]
    else:
        genre = "1"

    #get the rating
    ratingpattern = "<strong class=\"ll rating_num\" property=\"v:average\">(.*?)</strong>"
    rating = re.search(ratingpattern,text)
    if rating :
        print(rating.group(1))
        rating = rating.group(1)
        rating = "5"

    #get the imageurl
    imgpattern = "<img src=\"(.*?)\".*?rel=\"v:image\""
    imgurl = re.search(imgpattern,text)
    if(imgurl):
        print(imgurl.group(1))
        imgurl = imgurl.group(1)



    sql = "insert into  movie(url,type,name,alias,genre,year,rating,imgurl) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (url,0,titleinfo,"",0,year,rating,imgurl)
    print(values)
    try:
        cursor.execute(sql,values)
    except Exception as e:
        print(e)
        pass
    cnx.commit()
    cursor.close()
    cnx.close()
    return values


class movieQueue(threading.Thread):
    def __init__(self,start_url,name,queue):
        threading.Thread.__init__(self,name=name)
        self.start_url = start_url
        self.queue = queue

    def run(self):
        urls = geturl(self.start_url)
        #add url to queue
        print(self.name)
        mutex.acquire()
        for url in urls:
            self.queue.put(url)
            q.put(url)
        mutex.release()

class decodemovie(threading.Thread):
    def __init__(self,name,queue):
        threading.Thread.__init__(self,name=name)
        self.queue = queue


    def run(self):
        while not q.empty():
            # url = self.queue.get()
            print(q.qsize(),self.name)
            url = q.get()
            print(url,q.qsize())
            data = parseHtml(url)

if __name__ == '__main__':
    # getProxyIP()
    queue = Queue()
    start = movieQueue("http://movie.douban.com/subject/23766551/","Thread-1",queue)
    start2 = movieQueue("http://movie.douban.com/subject/21355504/","Thread-2",queue)
    start2.start()
    start.start()
    time.sleep(20)
    html = decodemovie("html",queue)
    html.start()
    html2 = decodemovie("html2",queue)
    html2.start()
    html3 = decodemovie("html3",queue)
    html3.start()
    html4 = decodemovie("html4",queue)
    html4.start()
    while True:
        if start.is_alive() == False and start2.is_alive() == False:
            print(q.qsize())
            start = movieQueue(queue.get(),"Thread-3",queue)
            start.start()
            start2 = movieQueue(queue.get(),"Thread-4",queue)
            start2.start()