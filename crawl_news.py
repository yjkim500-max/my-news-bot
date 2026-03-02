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
    query = "인공지능"
    # 검색 결과가 '최신순'으로 나오도록 옵션(&sort=1)을 추가하면 더 정확합니다.
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}&sort=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 기사 제목을 잡는 선택자를 더 포괄적으로 변경 (.news_tit 대신 사용할 수 있는 것들)
    articles = soup.select("a.news_tit")
    
    if not articles:
        # 만약 검색 결과가 없으면 알림을 줍니다.
        send_telegram(f"❗ [{query}] 관련 새로운 기사를 찾지 못했습니다.")
        return

    msg = f"📢 <b>오늘의 AI 뉴스</b>\n\n"
    for article in articles[:5]:
        title = article.get_text()
        link = article['href']
        msg += f"• {title}\n<a href='{link}'>바로가기</a>\n\n"
    
    send_telegram(msg)

if __name__ == "__main__":
    get_news()
