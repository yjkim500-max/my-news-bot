import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # 메시지가 너무 길면 잘릴 수 있으니 안전하게 전송
    params = {"chat_id": CHAT_ID, "text": message[:4000]} 
    requests.get(url, params=params)

def get_news():
    query = "인공지능"
    # PC 버전 주소로 변경: PC 버전이 뉴스 제목(.news_tit)을 추출하기 가장 안정적입니다.
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}"
    
    # [핵심 수정] 봇 차단을 피하기 위해 헤더 정보를 꼼꼼하게 일반 크롬 브라우저처럼 위장합니다.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.naver.com/"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status() # HTTP 통신 에러가 나면 바로 except로 빠지게 함
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # PC 네이버 뉴스 검색 결과의 제목 클래스는 보통 'news_tit' 입니다.
        articles = soup.select(".news_tit") 
        
        # 기사를 아예 찾지 못했을 경우
        if not articles:
            send_telegram("❌ 기사를 찾지 못했습니다. (네이버 봇 차단 또는 검색결과 없음)")
            return

        msg = f"📢 오늘의 [{query}] 뉴스\n"
        msg += "━━━━━━━━━━━━━━━━━━\n\n"
        
        count = 0
        for article in articles:
            # 텍스트 추출 시도, 없으면 title 속성에서 추출
            title = article.get_text(strip=True)
            if not title and article.has_attr('title'):
                title = article['title']
                
            link = article.get('href', '#')
            
            if title and link.startswith("http"):
                msg += f"{count+1}. {title}\n🔗 {link}\n\n"
                count += 1
            
            if count >= 5: # 5개만 채우면 중단
                break
        
        if count == 0:
            send_telegram("❌ 기사 요소를 찾았으나 제목이나 링크를 파싱하지 못했습니다.")
            return

        send_telegram(msg)
        
    except Exception as e:
        send_telegram(f"⚠️ 에러 발생: {str(e)}")

if __name__ == "__main__":
    get_news()
