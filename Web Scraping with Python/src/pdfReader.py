# This code is based on a sample code from the book "Web Scraping with Python" by Ryan Mitchell.
# This code reads a pdf file online and prints it.

from urllib.request import urlopen
from urllib.error import HTTPError
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import time

beginTime = time.time()

try:
    pdfFile = urlopen("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf")

    rscMgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rscMgr, retstr, laparams=laparams)

    process_pdf(rscMgr, device, pdfFile)
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)
except:
    print("Unexpected error!!!")
finally:
    device.close()
    content = retstr.getvalue()
    retstr.close()

    print(content)
    pdfFile.close()

endTime = time.time()
print("Total time it took: {}s".format(endTime - beginTime))