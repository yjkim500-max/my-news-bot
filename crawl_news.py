import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # HTML 모드 대신 일반 텍스트 모드로 보내서 태그 에러를 방지합니다.
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=params)

def get_news():
    query = "인공지능"
    # 검색 주소를 단순화하고 헤더를 강화합니다.
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 네이버 뉴스의 최신 제목 클래스인 'news_tit'를 찾습니다.
        articles = soup.find_all('a', class_='news_tit')
        
        if not articles:
            send_telegram("기사를 찾지 못했습니다. 구조가 바뀌었을 수 있습니다.")
            return

        # 결과물 조립 (HTML 태그 없이 깔끔하게 텍스트로만 구성)
        msg = f"📢 오늘의 [{query}] 뉴스\n\n"
        
        for i, article in enumerate(articles[:5], 1):
            title = article.get_text(strip=True)
            link = article['href']
            msg += f"{i}. {title}\n링크: {link}\n\n"
        
        # 최종 전송
        print(f"전송할 메시지 내용:\n{msg}") # 로그 확인용
        send_telegram(msg)
        
    except Exception as e:
        send_telegram(f"실행 중 에러 발생: {str(e)}")

if __name__ == "__main__":
    get_news()
