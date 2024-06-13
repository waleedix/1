import time
import logging
from telegram import Bot
from telegram.ext import Updater
import requests

TOKEN = '6708110180:AAH0UxHXimsHtX15xexZGHdN8_oKrHmn7Z0'
CHAT_ID = '907855315'
KEYWORD_DETECTED = False

# List of product sites
product_sites = [
    {'url': 'https://www.dzrt.com/en/icy-rush.html', 'name': 'ICY RUSH'},
    {'url': 'https://www.dzrt.com/en/highland-berries.html', 'name': 'HIGHLAND BERRIES'},
    {'url': 'https://www.dzrt.com/en/mint-fusion.html', 'name': 'MINT FUSION'},
    {'url': 'https://www.dzrt.com/en/spicy-zest.html', 'name': 'SPICY ZEST'},
    {'url': 'https://www.dzrt.com/en/garden-mint.html', 'name': 'GARDEN MINT'},
    {'url': 'https://www.dzrt.com/en/purple-mist.html', 'name': 'PURPLE MIST'},
    {'url': 'https://www.dzrt.com/en/seaside-frost.html', 'name': 'SEASIDE FROST'},
    {'url': 'https://www.dzrt.com/en/edgy-mint.html', 'name': 'EDGY MINT'},
    {'url': 'https://www.dzrt.com/en/our-products.html', 'name': 'Our Products'}
]

# Initialize the Bot
bot = Bot(token=TOKEN)

# Function to check if the site has changed
def check_site_change(url, keyword):
    global KEYWORD_DETECTED
    previous_content = get_previous_content(url)
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
    session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
    response = session.get(url)
    current_content = response.text
    if previous_content != current_content:
        if keyword not in current_content and not KEYWORD_DETECTED:
            send_notification(url, keyword, "Keyword not found", product_sites)
            KEYWORD_DETECTED = True
            logging.info(f"Keyword '{keyword}' not found on the page. Sending notification.")
        else:
            logging.info(f"Keyword '{keyword}' found on the page. No notification sent.")
    else:
        logging.info("Page content has not changed.")

# Function to get the previous content of the site
def get_previous_content(url):
    try:
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
        session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
        response = session.get(url)
        return response.text
    except requests.exceptions.RequestException:
        return None

# Function to send notification
def send_notification(url, keyword, message, product_sites):
    chat_id = CHAT_ID
    for product_site in product_sites:
        if product_site['url'] == url:
            product_name = product_site['name']
            bot.send_message(
                chat_id=chat_id,
                text=f"{message}  {product_name}  {url} متوفر الان ",
                parse_mode='HTML'
            )

# Start checking each product site for the target keyword
keyword = 'Back In Stock Soon'
for product_site in product_sites:
    check_site_change(product_site['url'], keyword)
    time.sleep(1)  # Wait for 10 seconds before checking the next site