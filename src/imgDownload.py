# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code downloads all images on a given web page.

import urllib.request as ur
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time
import os

baseURL = "https://www.w3schools.com"
downloadDir = "imgDownload_download"
html = ur.urlopen(baseURL)
bsObj = BeautifulSoup(html, "html.parser")
imageTags = bsObj.findAll("img", src=True)

def getAbsoluteURL(src: str) -> str:
    global baseURL
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

def getDownloadPath(absoluteURL):
    global baseURL
    path = absoluteURL.replace(baseURL, downloadDir)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return path

for tag in imageTags:
    absoluteURL = getAbsoluteURL(tag["src"])
    if absoluteURL != None:
        downloadPath = getDownloadPath(absoluteURL)
        ur.urlretrieve(absoluteURL, downloadPath)