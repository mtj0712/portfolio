# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code downloads all images on a given web page.

import urllib.request as ur
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import os

beginTime = time.time()

def getAbsoluteURL(baseURL: str, src: str) -> str:
    if src.startswith("http://") or src.startswith("https://"):
        result = src
    elif src.startswith("www."):
        result = baseURL.split("://", maxsplit=1)[0] + "://" + src
    elif src.startswith("/"):
        result = baseURL + src
    else:
        result = baseURL + "/" + src

    if baseURL not in result:
        return None
    return result

def getDownloadPath(baseURL: str, absoluteURL: str, downloadDir: str) -> str:
    path = absoluteURL.replace(baseURL, downloadDir)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return path

baseURL = "https://www.w3schools.com"
downloadDir = "imgDownload_download"

try:
    html = ur.urlopen(baseURL)
    bsObj = BeautifulSoup(html, "html.parser")
    imageTags = bsObj.findAll("img", src=True)
except HTTPError as e:
    print(e)
except:
    print("Unexpected error!!!")

for tag in imageTags:
    absoluteURL = getAbsoluteURL(baseURL, tag["src"])
    if absoluteURL != None:
        downloadPath = getDownloadPath(baseURL, absoluteURL, downloadDir)
        ur.urlretrieve(absoluteURL, downloadPath)

endTime = time.time()
print("Total time it took: {}s".format(endTime - beginTime))