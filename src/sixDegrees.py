# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code uses BFS algorithm to search for the shortest path from one Wikipedia page to another
# by only using the hyperlinks.

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time

start = "/wiki/Eric_Idle"
end = "/wiki/Kevin_Bacon"

beginTime = time.time()

try:
    # urls = list of (url, previous url index) tuples
    urls = [(start, 0)]
    # checkedUrls = set of checked urls
    checkedUrls = {start}

    # BFS
    i = 0
    found = False
    while i < len(urls) and not found:
        print(urls[i][0]) # debug
        html = urlopen("https://en.wikipedia.org" + urls[i][0])
        bs = BeautifulSoup(html, "html.parser")

        for link in bs.find("div", id="bodyContent").findAll(
            "a", href=re.compile("^(/wiki/)(?!(File|Help|Category|Special|Wikipedia|Template|Template_talk):)")
        ):
            # remove the id element of the url
            url = link.attrs["href"].split("#", maxsplit=1)[0]
            if url not in checkedUrls:
                checkedUrls.add(url)
                urls.append((url, i))
                if url == end:
                    found = True
                    break
        i += 1

    if found:
        steps = list()
        i = len(urls) - 1
        while i != 0:
            steps.append(urls[i][0])
            i = urls[i][1]
        
        # print out the result
        print("\n{} degrees from start to end!!!".format(len(steps)))
        print(start)
        while len(steps) > 0:
            print(steps.pop())
    else:
        print("No path to the end link!!!")

except HTTPError as e:
    print(e)
except AttributeError as e:
    print(e)
except:
    print("Unexpected error!!!")

endTime = time.time()
print("Total time it took: {}s".format(endTime - beginTime))