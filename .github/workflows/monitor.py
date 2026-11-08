import os
import requests
from bs4 import BeautifulSoup

# Retrieve secrets safely from Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def send_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Missing Telegram Secret Keys.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")

def monitor_clasificados_online():
    url = "https://www.clasificadosonline.com/BienesRaices.asp?LowPrice=50000&HighPrice=70000"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            listings = soup.find_all("td", class_="ClasLinks")
            for item in listings[:5]:
                title = item.get_text(strip=True)
                link_tag = item.find("a")
                if link_tag:
                    link = "https://www.clasificadosonline.com/" + link_tag["href"]
                    send_alert(f"🏠 *New PR Classified Listing Found!*\n*Title:* {title}\n*Link:* {link}")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Scraper Error: {e}")

if __name__ == "__main__":
    monitor_clasificados_online()
