import requests
from bs4 import BeautifulSoup
import os

from dotenv import load_dotenv
load_dotenv()

def parser (url:str):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text,"lxml")
    texts = soup.find_all("div", class_="grafik_string_list_item")
    strings = ""
    for text in texts:
        jj = text.get_text()
        strings = ("Світла не буде: ", jj)
    hours = soup.find_all("div",  class_="scale_el_r")
    items = []
    for hour in hours:
        time = hour.get_text()
        items.append(time)
    print(items, strings)
    return items, strings


def send_message(message):

    TG_BOT_ID = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHANNEL_ID')

    url = f'https://api.telegram.org/bot{TG_BOT_ID}/sendMessage'

    params = {
        'chat_id': CHAT_ID,
        'text': f'{message}'
    }

    res = requests.post(url, params=params)
    res.raise_for_status()

    return res.json()

if __name__ == "__main__":
    off_times = parser(url="https://lviv.energy-ua.info/grupa/1.1")
    if off_times:
        send_message(off_times)
    # print(off_times)