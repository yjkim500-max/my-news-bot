import requests
from bs4 import BeautifulSoup

# 1. 수집하고 싶은 뉴스 페이지 (네이버 뉴스 검색 - 인공지능)
url = "https://search.naver.com/search.naver?where=news&query=인공지능"

def get_news():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 2. 기사 제목과 링크 추출 (네이버 뉴스 구조 기준)
    articles = soup.select(".news_tit")
    
    print(f"--- 오늘의 주요 뉴스 ---")
    for article in articles[:5]: # 상위 5개만 출력
        title = article.get_text()
        link = article['href']
        print(f"제목: {title}\n링크: {link}\n")

if __name__ == "__main__":
    get_news()
