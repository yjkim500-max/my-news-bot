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
    # 주소를 모바일 버전(m.search.naver.com)으로 바꿉니다. 모바일 버전이 구조가 단순해서 차단이 덜합니다!
    search_url = f"https://m.search.naver.com/search.naver?where=m_news&query={query}&sm=mtb_pge&sort=0"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # [갈고리 1] 모바일 네이버 뉴스 제목 클래스
        articles = soup.select(".news_tit") 
        
        # [갈고리 2] 만약 위에서 못 찾으면 다른 클래스도 시도
        if not articles:
            articles = soup.select(".tit_main")
            
        # [갈고리 3] 이것도 안 되면 모든 <a> 태그 중 제목 같은 걸 다 뒤짐
        if not articles:
            articles = [a for a in soup.find_all('a') if 'news_tit' in a.get('class', [])]

        if not articles:
            send_telegram("❌ 여전히 기사를 찾지 못했습니다. 네이버가 강하게 막고 있네요.")
            return

        msg = f"📢 오늘의 [{query}] 뉴스\n"
        msg += "━━━━━━━━━━━━━━━━━━\n\n"
        
        count = 0
        for article in articles:
            title = article.get_text(strip=True)
            link = article.get('href', '#')
            
            if title and link.startswith("http"):
                msg += f"{count+1}. {title}\n🔗 {link}\n\n"
                count += 1
            
            if count >= 5: # 5개만 채우면 중단
                break
        
        send_telegram(msg)
        
    except Exception as e:
        send_telegram(f"⚠️ 에러 발생: {str(e)}")

if __name__ == "__main__":
    get_news()
