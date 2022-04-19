# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code reads a csv file online and prints it.

from urllib.request import urlopen
from urllib.error import HTTPError
from io import StringIO
import csv
import time

beginTime = time.time()

try:
    data = urlopen(
        "http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode(
        "ascii", "ignore")
    dataFile = StringIO(data)
    csvReader = csv.DictReader(dataFile)

    for row in csvReader:
        print("The album \"{}\" was released in {}.".format(row["Name"], row["Year"]))
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)
except:
    print("Unexpected error!!!")

endTime = time.time()
print("Total time it took: {}s".format(endTime - beginTime))