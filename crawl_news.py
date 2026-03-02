import os
import requests
from bs4 import BeautifulSoup

# GitHub Secrets에 저장한 값을 시스템 환경변수에서 가져옵니다.
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    """텔레그램 메시지 전송 함수"""
    if not BOT_TOKEN or not CHAT_ID:
        print("에러: 텔레그램 토큰이나 채팅 ID가 설정되지 않았습니다.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False # 링크 미리보기 허용
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print("텔레그램 메시지 전송 성공!")
    except Exception as e:
        print(f"전송 실패: {e}")

def get_news():
    """네이버 뉴스 수집 함수"""
    query = "인공지능" # 원하는 키워드로 변경 가능
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select(".news_tit")
        
        if not articles:
            print("수집된 기사가 없습니다.")
            return

        msg = f"📢 <b>오늘의 [{query}] 뉴스</b>\n"
        msg += "<i>3시간마다 자동으로 업데이트됩니다.</i>\n\n"
        
        for article in articles[:5]:
            title = article.get_text()
            link = article['href']
            msg += f"• <b>{title}</b>\n<a href='{link}'>기사 읽기</a>\n\n"
        
        send_telegram(msg)
        
    except Exception as e:
        print(f"크롤링 에러: {e}")

if __name__ == "__main__":
    get_news()
