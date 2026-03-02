import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # HTML 태그 에러를 방지하기 위해 일반 텍스트 모드로 보냅니다.
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=params)

def get_news():
    query = "인공지능"
    # 네이버 뉴스 검색 결과 페이지 (가장 표준적인 주소)
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # [수정 포인트] 네이버 뉴스 제목을 잡는 가장 확실한 클래스명 'news_tit'
        articles = soup.find_all('a', class_='news_tit')
        
        if not articles:
            # 만약 못 찾았다면 텔레그램으로 상황을 보고합니다.
            send_telegram(f"❌ [{query}] 뉴스를 찾지 못했습니다. 구조 확인이 필요합니다.")
            return

        msg = f"📢 오늘의 [{query}] 뉴스\n"
        msg += "------------------------\n"
        
        # 상위 5개만 추출
        for i, article in enumerate(articles[:5], 1):
            title = article.get_text(strip=True)
            link = article['href']
            msg += f"{i}. {title}\n🔗 {link}\n\n"
        
        send_telegram(msg)
        print("전송 완료!")
        
    except Exception as e:
        send_telegram(f"⚠️ 에러 발생: {str(e)}")

if __name__ == "__main__":
    get_news()
