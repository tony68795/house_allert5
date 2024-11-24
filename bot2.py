import asyncio
from flask import Flask
from telegram import Bot
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Telegram instellingen
TELEGRAM_API_TOKEN = '7826115707:AAFZSMaITChD_KJifuhvepcVuBub5kUrmxs'
CHAT_ID = '1940095586'

# URL van de Pararius-huurwoningenpagina voor Zwolle
URL = "https://www.pararius.nl/huurwoningen/zwolle"

# Functie om de website te scrapen
def get_new_listings():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    listings = soup.find_all('a', class_='listing-search-item__link listing-search-item__link--title')
    new_listings = [f"{listing.get_text(strip=True)}: https://www.pararius.nl{listing.get('href')}" for listing in listings]
    return new_listings

# Functie om een Telegram-bericht te sturen
async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_API_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Functie om nieuwe woningen te controleren en berichten te sturen
async def check_for_new_listings():
    previous_listings = set()
    while True:
        print("Checking for new listings...")
        current_listings = set(get_new_listings())
        new_entries = current_listings - previous_listings

        if new_entries:
            for new_entry in new_entries:
                await send_telegram_message(f"Nieuwe woning gevonden: {new_entry}")

        previous_listings = current_listings
        await asyncio.sleep(30)  # Controleer elke 30 seconden

# Route voor Render's port binding
@app.route('/')
def home():
    return "Bot is running!"

# Start de Flask-server en bot samen
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(check_for_new_listings())  # Start bot-taak
    app.run(host='0.0.0.0', port=5000)  # Start Flask-server op poort 5000
