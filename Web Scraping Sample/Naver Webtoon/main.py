from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep

urlEncoding = {
    " " : "+", "\t" : "+", "@" : "%40", "#" : "%23",
    "$" : "%24", "%" : "%25", "&" : "%26", "=" : "%3D",
    "+" : "%2B", ";" : "%3B", ":" : "%3A", "," : "%2C",
    "/" : "%2F", "?" : "%3F"
}

baseURL = "https://comic.naver.com"

# Get the title of the webtoon
search = input("웹툰 제목: ")
for k in urlEncoding:
    search = search.replace(k, urlEncoding[k])
searchLink = baseURL + "/search?keyword=" + quote(search)

# Get the genre number
genre = input("종류 (1. 웹툰, 2. 베스트도전만화, 3. 도전만화)\n"
    "숫자만 입력: ")
genreValid = False
while not genreValid:
    try:
        genre = int(genre)
        if 1 <= genre and genre <= 3:
            genreValid = True
        else:
            genre = input("1 ~ 3 사이의 숫자로만 입력해 주십시오: ")
    except ValueError as e:
        print(e)
        genre = input("1 ~ 3 사이의 숫자로만 입력해 주십시오: ")

print("검색 제목: {}, 장르 번호: {}".format(search, genre))

try:
    searchHtml = urlopen(searchLink)
    searchSoup = BeautifulSoup(searchHtml, "html.parser")

    try:
        searchResultExists = False
        link = searchSoup("div", class_="resultBox")[genre - 1]. \
            find("h5").find("a", href=True)["href"]
        searchResultExists = True
        print("웹툰 발견")
    except AttributeError as e:
        print("검색결과가 없습니다.")
    except TypeError as e:
        print("검색결과가 없습니다.")

    if searchResultExists:
        listLink = baseURL + link.replace("detail", "list").split("&", maxsplit=1)[0]
        listHtml = urlopen(listLink)
        listSoup = BeautifulSoup(listHtml, "html.parser")

        currentNewest = listSoup.find("td", class_="title").find("a", href=True)["href"]
        print("현재 최신화: " + currentNewest)

        # 30초마다 새로고침
        while True:
            sleep(30)
            listHtml = urlopen(listLink)
            listSoup = BeautifulSoup(listHtml, "html.parser")
            print("새로고침") # debug
            newest = listSoup.find("td", class_="title").find("a", href=True)["href"]
            if newest != currentNewest:
                print("다음 화가 올라왔습니다. 링크: " + newest)
                currentNewest = newest

except HTTPError as e:
    print(e)
except Exception as e:
    print (e)
except:
    print("Unexpected error!!!")
