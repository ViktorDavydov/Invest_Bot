import requests
import telebot
from bs4 import BeautifulSoup

token = "6436709903:AAFzn9x4EJHdnVq4kBRtOSaCrUJrfKNOW1A"
bot = telebot.TeleBot(token)


def parsing_funds():
    all_funds = ""
    investments_names = {
        "LQDT": "ВИМ - Ликвидность",
        "EQMX": "ВИМ - Индекс Мосбиржи",
        "GOLD": "ВИМ - Золото",
        "SBMX": "Первая - Топ Российских акций"
    }
    investments = ["LQDT", "EQMX", "GOLD", "SBMX"]
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    url = 'https://smart-lab.ru/q/etf'

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')
    for tr in table:
        td = tr.find_all('tr')
        for f in td:
            td_price = f.find_all('td')
            if (len(td_price)) != 0 and td_price[2].text[:4] in investments:
                all_funds += f"""Фонд: {investments_names[td_price[2].text[:4]]}
Стоимость акции: {float(td_price[6].text)} руб.
Изм. за последний час, %: {float(td_price[7].text)}

"""
    return all_funds


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я слежу за акциями "
                                      "и сообщаю текущую стоимость!"
                                      "Жми /run!")


@bot.message_handler(commands=['run'])
def run(message):
    bot.send_message(message.chat.id, parsing_funds())


bot.infinity_polling()
