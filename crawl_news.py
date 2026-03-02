import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message} # HTML 태그 없이 안전하게 전송
    requests.get(url, params=params)

def get_news():
    query = "인공지능"
    # 검색 결과가 잘 나오도록 헤더와 URL을 보강했습니다.
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}&sm=tab_pge&sort=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 현재 네이버 뉴스 제목의 가장 정확한 위치입니다.
    articles = soup.find_all('a', class_='news_tit')
    
    if not articles:
        send_telegram("기사를 찾지 못했습니다. 키워드를 확인해주세요.")
        return

    msg = f"📢 오늘의 [{query}] 뉴스\n\n"
    for i, article in enumerate(articles[:5], 1):
        title = article.get_text(strip=True)
        link = article['href']
        # 기사 제목과 링크를 한 줄씩 정성껏 붙입니다.
        msg += f"{i}. {title}\n🔗 {link}\n\n"
    
    send_telegram(msg)

if __name__ == "__main__":
    get_news()
