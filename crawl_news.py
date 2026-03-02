import os
import requests
from bs4 import BeautifulSoup

# 1. 환경변수 읽기
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=params)

def get_news():
    query = "인공지능"
    # [수정] 네이버 뉴스 검색 URL을 더 구체적으로 변경
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}&sm=tab_pge&sort=0"
    
    # [핵심] 네이버가 로봇으로 인식하지 못하게 '진짜 브라우저'처럼 위장하는 정보
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        # 응답이 정상인지 확인 (200이 아니면 에러)
        if response.status_code != 200:
            send_telegram(f"❌ 네이버 접속 실패 (코드: {response.status_code})")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # [수정] 네이버 뉴스 제목을 찾는 가장 정확한 경로
        articles = soup.select("a.news_tit")
        
        if not articles:
            # 하나도 못 찾았다면, 받아온 본문 중 일부를 로그로 출력 (디버깅용)
            print(f"응답 본문 길이: {len(response.text)}")
            send_telegram("❌ 뉴스를 찾지 못했습니다. 구조 확인이 필요합니다.")
            return

        msg = f"📢 오늘의 [{query}] 뉴스\n"
        msg += "━━━━━━━━━━━━━━━━━━\n"
        
        for i, article in enumerate(articles[:5], 1):
            title = article.get_text(strip=True)
            link = article['href']
            msg += f"{i}. {title}\n🔗 {link}\n\n"
        
        send_telegram(msg)
        
    except Exception as e:
        send_telegram(f"⚠️ 에러 발생: {str(e)}")

if __name__ == "__main__":
    get_news()
