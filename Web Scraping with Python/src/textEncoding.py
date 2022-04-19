# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code reads text files from the Internet.

from urllib.request import urlopen
from urllib.error import HTTPError
import time

beginTime = time.time()

try:
    # ASCII text
    asciiPage = urlopen("https://www.pythonscraping.com/pages/warandpeace/chapter1.txt")
    asciiText = str(asciiPage.read()).replace("\\n", "\n").replace("\\\'", "\'")
    print(asciiText)

    # UTF-8 text
    utf8Page = urlopen("https://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
    utf8Text = str(utf8Page.read(), "utf-8")
    print(utf8Text)
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)
except:
    print("Unexpected error!!!")

endTime = time.time()
print("Total time it took: {}s".format(endTime - beginTime))