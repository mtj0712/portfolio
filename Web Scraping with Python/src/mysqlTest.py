# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code uses BFS algorithm to search for the shortest path from Eric Idle Wikipedia page
# to the end page by only using the hyperlinks.
# In this version, MySQL is used in place of Python set to keep the list of visited links.

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pymysql
import re
from getpass import getpass
import time

mysqlPwd = getpass("Database password: ")

beginTime = time.time()

def linksLength(cur) -> int:
    cur.execute("SELECT MAX(id) FROM links")
    return cur.fetchone()[0]

def urlFromId(cur, i: int) -> str:
    cur.execute("SELECT url FROM links WHERE id=%s", (i,))
    return cur.fetchone()[0]

def hasUrl(cur, url: str) -> bool:
    cur.execute("SELECT id FROM links WHERE url=%s", (url,))
    return (cur.fetchone() != None)

endUrl = "/wiki/Kevin_Bacon"
linkRe = re.compile(
    "^(/wiki/)(?!(File|Help|Category|Special|Wikipedia|Template|Template_talk):)")

try:
    # setup for MySQL
    connection = pymysql.connect(host="127.0.0.1", user="root", passwd=mysqlPwd, db="mysql")
    cursor = connection.cursor()
    cursor.execute("USE scraping")

    # BFS
    i = 1
    found = False
    while i <= linksLength(cursor) and not found:
        # fetch the url of the current index
        currentUrl = urlFromId(cursor, i)
        print("Currently exploring this page:", currentUrl)
        # get the html of the web page
        html = urlopen("https://en.wikipedia.org" + currentUrl)
        bs = BeautifulSoup(html, "html.parser")

        for link in bs.find("div", id="bodyContent").findAll("a", href=linkRe):
            # skip if this link doesn't have url
            if "href" not in link.attrs:
                continue
            # remove the id part from the url
            newUrl = link.attrs["href"].split("#", maxsplit=1)[0]
            # add this url to the database if it's new
            if not hasUrl(cursor, newUrl):
                # adding the url to the database
                cursor.execute(
                    "INSERT INTO links (url, prevId) VALUES (%s, %s)",
                    (newUrl, i))
                connection.commit()
                # if the end page is reached, end
                if newUrl == endUrl:
                    found = True
                    break
        i += 1

    if found:
        steps = list()
        i = linksLength(cursor)
        while i != 0:
            cursor.execute("SELECT url, prevId FROM links WHERE id=%s", (i,))
            url, i = cursor.fetchone()
            steps.append(url)
        
        # print out the result
        print("\n{} degrees from start to end!!!".format(len(steps) - 1))
        while len(steps) > 0:
            print(steps.pop())
    else:
        print("No path to the end link!!!")

except HTTPError as e:
    print(e)
except AttributeError as e:
    print(e)
except Exception as e:
    print(e)
except:
    print("Unexpected error!!!")
finally:
    cursor.close()
    connection.close()

endTime = time.time()
print("Total time it took: {}s".format(endTime - beginTime))