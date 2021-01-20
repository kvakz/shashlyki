import time
from threading import Thread
import telebot
from telebot import types
import requests

bot = telebot.AsyncTeleBot('1480925538:AAFwnCellUA8ZzDnOcDCK_SdgetD_CgDUkU')
city_id = 0
appid = "4070a5a915f343711da0bf93f2c481f6"
txt = ''

users = {}
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text='Начать', callback_data='LetsGo')
    keyboard.add(start_button)
    bot.send_message(message.chat.id, f'''Тевирп, {str(message.chat.first_name)}! Меня зовут Рич! Рад тебя видеть! Если нужно выбрать место для шашлыка то, тыкни "Начать"''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda  call: True)
def callback_worker(call):
    if call.data == 'LetsGo':
        bot.send_message(call.message.chat.id, 'В каком городе ты сейчас находишься?')


@bot.message_handler(content_types=['text'])
def get_message(message):
    s_city = message.text
    chat_id = message.chat.id
    users[chat_id] = [s_city]
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
        params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
        city_id = data['list'][0]['id']
        bot.send_message(message.chat.id, 'вас понял')
    except Exception as e:
        print("Exception (find):", e)
        bot.send_message(message.chat.id, 'Город не найден')
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        condit = data['weather'][0]['description']
        temp = int(data['main']['temp'])
                
        if condit=='пасмурно':
            txt = f"Можно идти на шашлыки, но лучше подождать лучшей погоды!"
        elif condit=='снег':
            txt = f"Сейчас не время для шашлыков."
        elif condit=='небольшой снег':
            txt = f"Лучше не ходить сейчас на шашлыки."
        elif condit=='солнечно':
            txt = f"Cейчас самое время для шашлыков!"
        elif condit=='ветрено':
            txt = f"Иди, смотри чтобы не улетели."
        
        if temp>=0:
            if temp%10 in [0,5,6,7,8,9] or temp%100 in [11,12,13,14]:
                bot.send_message(message.chat.id, f"На улице сейчас {condit} и {temp} градусов. "+txt)
            elif temp%10==1:
                bot.send_message(message.chat.id, f"На улице сейчас {condit} и {temp} градус.  "+txt)
            elif temp%10 in [2,3,4]:
                bot.send_message(message.chat.id, f"На улице сейчас {condit} и {temp} градуса. "+txt)
        else:
            if temp%10 in [0,5,4,3,2,1] or temp%100 in [89,88,87,86]:
                bot.send_message(message.chat.id, f"На улице сейчас {condit} и {temp} градусов. "+txt)
            elif temp%10==9:
                bot.send_message(message.chat.id, f"На улице сейчас {condit} и {temp} градус. "+txt)
            elif temp%10 in [8,7,6]:
                bot.send_message(message.chat.id, f"На улице сейчас {condit} и {temp} градуса. "+txt)
    except Exception as e:
        print("Exception (weather):", e)
        bot.send_message(message.chat.id, 'Данные не найдены')
    
bot.polling(none_stop=True, timeout=20)
