import MySQLdb
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    RANK = 100  # 멜론 차트 순위가 1 ~ 100위까지 있음

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://kin.naver.com/search/list.nhn?query=%ED%8C%94+%ED%86%B5%EC%A6%9D',
                       headers=header)  # 주간 차트를 크롤링 할 것임
    html = req.text
    parse = BeautifulSoup(html, 'html.parser')

    #titles = parse.find_all("div", {"class": "ellipsis rank01"})
    #singers = parse.find_all("div", {"class": "ellipsis rank02"})
    ul = parse.select_one('ul.basic1')
    titles = ul.select('li> dl > dt > a')
    answers = ul.select('li>dl>dd:nth-child(3)')
    title =[]
    answer=[]
    for t in titles :
        title.append(t.text)

    for a in answers :
        answer.append(a.text)
        print(a.text)

    items = [item for item in zip(title,answer)]
    #title = []
    #singer = []


   # for t in titles:
    #    title.append(t.find('a').text)

    #for s in singers:
     #   singer.append(s.find('span', {"class": "checkEllipsis"}).text)
    #items = [item for item in zip(title, singer)]


conn = MySQLdb.connect(
    user="root",
    passwd="1234",
    host="localhost",
    db="crawl",
    charset="utf8"
)
# 커서 생성
cursor = conn.cursor()

# 실행할 때마다 다른값이 나오지 않게 테이블을 제거해두기
cursor.execute("DROP TABLE IF EXISTS melon")

# 테이블 생성하기
cursor.execute("CREATE TABLE melon (`rank` int, title text, url text)")
i = 1
# 데이터 저장하기
for item in items:
    cursor.execute(
        f"INSERT INTO melon VALUES({i},\"{item[0]}\",\"{item[1]}\")")
    i += 1

# 커밋하기
conn.commit()
# 연결종료하기
conn.close()