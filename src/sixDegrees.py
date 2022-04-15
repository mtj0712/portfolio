# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code uses BFS algorithm to search for the shortest path from one Wikipedia page to another
# by only using the hyperlinks.

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time

beginTime = time.time()

startUrl = "/wiki/Eric_Idle"
endUrl = "/wiki/Kevin_Bacon"
linkRe = re.compile(
    "^(/wiki/)(?!(File|Help|Category|Special|Wikipedia|Template|Template_talk):)")

try:
    # urls = list of (url, previous url index) tuples
    urls = [(startUrl, 0)]
    # checkedUrls = set of checked urls
    checkedUrls = {startUrl}

    # BFS
    i = 0
    found = False
    while i < len(urls) and not found:
        print("Currently exploring this page:", urls[i][0])
        html = urlopen("https://en.wikipedia.org" + urls[i][0])
        bs = BeautifulSoup(html, "html.parser")

        for link in bs.find("div", id="bodyContent").findAll("a", href=linkRe):
            # skip if this link doesn't have url
            if "href" not in link.attrs:
                continue
            # remove the id part from the url
            url = link.attrs["href"].split("#", maxsplit=1)[0]
            # add this url to the list if it's new
            if url not in checkedUrls:
                checkedUrls.add(url)
                urls.append((url, i))
                # if the end page is reached, end
                if url == endUrl:
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
        print(startUrl)
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