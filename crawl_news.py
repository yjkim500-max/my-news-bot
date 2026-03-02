import requests
from bs4 import BeautifulSoup

# 1. 아까 복사한 정보 넣기
BOT_TOKEN = "8382005817:AAEldU0_UbZ28nOiChmbG1FZS5opq-q68Hg"
CHAT_ID = "6728461785"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.get(url, params=params)

def get_news():
    search_url = "https://search.naver.com/search.naver?where=news&query=인공지능"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.select(".news_tit")
    
    msg = "📢 <b>오늘의 AI 뉴스 (3시간마다 업데이트)</b>\n\n"
    for article in articles[:5]:
        title = article.get_text()
        link = article['href']
        msg += f"• {title}\n<a href='{link}'>바로가기</a>\n\n"
    
    send_telegram(msg)

if __name__ == "__main__":
    get_news()
