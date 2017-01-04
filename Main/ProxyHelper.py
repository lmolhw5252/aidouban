#Todo
#Get the proxy IPs
from queue import Queue
import re
import requests

proxyUrl = []
def getProxyIP():
    url = "http://www.xici.net.co/nt/"
    response = requests.get(url)
    if(int(response.status_code)==200):
        text = response.text
        pattern = "\d{2,3}\.\d{2,3}\.\d{2,3}\.\d{2,3}"
        result = re.findall(pattern,text,re.M|re.I)
        if result:
            proxyUrl  = result

if __name__ == '__main__':
    # getProxyIP()
    test = ["1","2","3"]
    result= test.pop(0)
    print(result)