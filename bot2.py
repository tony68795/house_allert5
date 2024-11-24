import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from flask import Flask

# Telegram instellingen
TELEGRAM_API_TOKEN = '7826115707:AAFZSMaITChD_KJifuhvepcVuBub5kUrmxs'
CHAT_ID = '1940095586'

# URL van de Pararius-huurwoningenpagina voor Zwolle
URL = "https://www.pararius.nl/huurwoningen/zwolle"

# Maak een Flask-applicatie
app = Flask(__name__)

# Route voor Render's port binding
@app.route('/')
def home():
    return "Bot is running!"

# Functie om de website te scrapen
def get_new_listings():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    listings = soup.find_all('a', class_='listing-search-item__link listing-search-item__link--title')
    new_listings = []
    for listing in listings:
        title = listing.get_text(strip=True)
        link = "https://www.pararius.nl" + listing.get('href')
        new_listings.append(f"{title}: {link}")
     
    return new_listings

# Functie om een Telegram-bericht te sturen
async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_API_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Functie om nieuwe woningen te controleren en berichten te sturen
async def check_for_new_listings():
    previous_listings = []

    while True:
        print("Checking for new listings...")
        
        current_listings = get_new_listings()
        new_entries = set(current_listings) - set(previous_listings)

        if new_entries:
            for new_entry in new_entries:
                await send_telegram_message(f"Nieuwe woning gevonden: {new_entry}")
        
        previous_listings = current_listings
        await asyncio.sleep(30)

# Start Flask-server en bot samen
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(check_for_new_listings())  # Start bot-taak
    
    # Flask-server draait op 0.0.0.0 (Render's vereiste)
    app.run(host='0.0.0.0', port=5000)
