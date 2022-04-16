# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code downloads table data from a wikipedia page in csv file.

import urllib.request as ur
from urllib.error import HTTPError
import csv
from bs4 import BeautifulSoup
import time

beginTime = time.time()

try:
    csvFile = open("../csvTest_file/test.csv", "w")
    writer = csv.writer(csvFile)

    html = ur.urlopen("https://en.wikipedia.org/wiki/Comparison_of_text_editors")
    bsObj = BeautifulSoup(html, "html.parser")
    table = bsObj.find("table", class_="wikitable")
    rows = table.find_all("tr")

    for row in rows:
        csvRow = []
        for cell in row.find_all(["th", "td"]):
            text = cell.get_text().strip()
            if text != "":
                csvRow.append(text)

        writer.writerow(csvRow)
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)
except:
    print("Unexpected error!!!")
finally:
    csvFile.close()

endTime = time.time()
print("Total time it took: {}s".format(endTime - beginTime))