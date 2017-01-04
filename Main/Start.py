from bs4 import BeautifulSoup
import re
import mysql.connector
import requests

#排行榜开始爬虫
from Main.moviequeue import q


def startSpider():
    # url = "https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action="
    url = "http://movie.douban.com/chart"
    response = requests.get(url)
    content = response.content
    text = response.text
    soup  = BeautifulSoup(text)
    html = text.encode('gbk', 'ignore').decode('gbk')
    #得到每个电影的URL
    pattern2  = "<div class=\"pl2\">\W+<a href=\"(.*?)\".*?>"
    items = re.findall(pattern2,text)
    for item in items:
        print(item)
        q.put(item)
    return items


#url为http://movie.douban.com/subject/25932086/
def getMovieDetail(url):
    response = requests.get(url)
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

    # #get summary
    # summarypattern = "<span class=\"\" property=\"v:summary\">(.*?)</span>"
    # summary = re.findall(summarypattern)
    # summaryinfo = ""
    # if(summary):
    #     summaryinfo = summary.group(1)

    #get the year
    yearpattern = "<span class=\"year\">\((.*?)\)</span>"
    year = re.search(yearpattern,text)
    if(year):
        # print(year.group(1))
        year = year.group(1)

    #get the movie type
    genrepattern = "<span property=\"v:genre\">(.*?)</span>"
    genre =re.findall(genrepattern,text)
    print(genre)
    genre = genre[0]

    #get the rating
    ratingpattern = "<strong class=\"ll rating_num\" property=\"v:average\">(.*?)</strong>"
    rating = re.search(ratingpattern,text)

    # print(rating.group(1))
    rating = rating.group(1)

    #get the imageurl
    imgpattern = "<img src=\"(.*?)\".*?rel=\"v:image\""
    imgurl = re.search(imgpattern,text)
    if(imgurl):
        print(imgurl.group(1))
        imgurl = imgurl.group(1)


    #insert into db
    config = {
    "user":"root",
    "password":"root",
    "host":"127.0.0.1",
    "database":"aidouban",
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    sql = "insert into  movie(url,type,name,alias,genre,year,rating,imgurl) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (url,0,titleinfo,"",0,year,rating,imgurl)
    print(values)
    cursor.execute(sql,values)
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    items = startSpider()
    q.qsize()
    # print(q.qsize())
    # while q.not_empty:
    #     q.get()
    #     getMovieDetail(items[])

    for item in items:
        q.get()
        getMovieDetail(item)
