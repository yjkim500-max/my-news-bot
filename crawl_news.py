import os
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message[:4000]} 
    requests.get(url, params=params)

def get_news():
    query = "인공지능"
    # 네이버는 해외 IP(깃허브 액션 등)를 강력하게 차단하므로,
    # 봇 차단이 없는 구글 뉴스 RSS 기능을 사용하여 안정성을 확보합니다.
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        
        # 파이썬 기본 내장 라이브러리인 XML 파서를 사용합니다 (에러 확률 낮음)
        root = ET.fromstring(response.text)
        items = root.findall('.//item')
        
        if not items:
            send_telegram(f"❌ '{query}' 관련 기사를 찾지 못했습니다. (구글 뉴스 검색결과 없음)")
            return

        msg = f"📢 오늘의 [{query}] 뉴스\n"
        msg += "━━━━━━━━━━━━━━━━━━\n\n"
        
        count = 0
        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            
            if title and link:
                msg += f"{count+1}. {title}\n🔗 {link}\n\n"
                count += 1
            
            if count >= 5: # 5개만 채우면 중단
                break
        
        send_telegram(msg)
        
    except Exception as e:
        send_telegram(f"⚠️ 에러 발생: {str(e)}")

if __name__ == "__main__":
    get_news()
