import telebot
import random
from telebot import types
from bs4 import BeautifulSoup as soup
import requests

token = '1741702144:AAGDR06O9nl2lRRb2PiNQdzaxaHtULY4JcQ' # Вставь свой токен
bot = telebot.TeleBot(token)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
answers = ["meow","murr","murrmeow!"]

def getWeather():
    url = "https://ua.sinoptik.ua/"
    result = requests.get(url, headers = headers)
    page = result.text
    doc = soup(page, "html5lib")
    links = [element for element in doc.find_all('p') if element.get("class") and "today-temp" in element.get("class")]
    return links

def getCurrency():
    url = "https://minfin.com.ua/ua/currency/eur/"
    result = requests.get(url, headers = headers)
    page = result.text
    doc = soup(page, "html5lib")
    links = [element.span for element in doc.find_all('td') if element.get("class") and "mfm-text-nowrap" in element.get("class") and element.get('data-title') and "Купівля" in element.get('data-title')]
    buy_cost = links[0].contents[0]
    links = [element.span for element in doc.find_all('td') if element.get('data-title') and "Продаж" in element.get('data-title')]
    sell_cost = links[0].contents[0]
    return "EUR {} / {}".format(buy_cost, sell_cost)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    markup = types.ReplyKeyboardMarkup()
    weatherbut = types.KeyboardButton('Weather')
    currbut = types.KeyboardButton('Currency')
    markup.row(weatherbut, currbut)
    if message.text == "Weather":
        bot.send_message(message.chat.id, getWeather())
    elif message.text == "Currency":
        bot.send_message(message.chat.id, getCurrency())
    elif message.text == "meow":
        bot.send_message(message.chat.id, "YOU ARE NOT MEOW!!! Impostor!")
    else:
        bot.send_message(message.chat.id, answers[random.randint(0,2)], reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)