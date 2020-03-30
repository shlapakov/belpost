import telebot
import bs4
import urllib.request
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)


def get_info(track):
    track = track.replace(" ", "")
    print(f'i have track — {track}')
    site = urllib.request.urlopen(f'https://webservices.belpost.by/searchRu/{quote(track)}').read().decode('utf-8')
    soup = bs4.BeautifulSoup(site, features='html.parser')
    if 'По данному отправлению' in site:
        return 'По данному отправлению ничего не найдено'
    tables = soup.findAll('table')
    text_to_send = ''
    for table in tables[:-2]:
        texts = table.findAll('font')
        texts = texts[3:]

        while len(texts) > 0:
            text_to_send += (texts[0].text.strip('\n') + '\n'
                             + texts[1].text.strip('\n') + '\n'
                             + texts[2].text.strip('\n') + '\n________\n')
            texts = texts[3:]
    print(text_to_send)
    return text_to_send


@bot.message_handler(commands=['start'])
def command_hello(message):
    bot.reply_to(message, "Привет, укажи трек-номер")

@bot.message_handler()
def get_track(message):
    print('hi')
    bot.reply_to(message, get_info(message.text))


while True: # Для постоянной работы
    bot.polling()
